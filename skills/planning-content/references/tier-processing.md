# Tier Processing Guide

Hướng dẫn xử lý tài liệu đã convert theo kích thước. Load file này khi input là tài liệu đã convert (có structure.json).

## Context Rule (quan trọng)

**Luôn đọc structure.json TRƯỚC, KHÔNG đọc content.md toàn bộ.**

structure.json chứa đủ thông tin cho content map: outline (section titles, word counts, critical markers), stats, tier. Chỉ đọc content.md theo section cụ thể (`offset`/`limit` từ `line`/`line_end`) khi cần chi tiết cho outline.

Lý do: tài liệu 35K words chiếm ~37K context nếu đọc cả hai. Chỉ đọc structure.json chiếm ~2K. Tiết kiệm ~75% context budget.

## Tier Detection

Đọc `structure.json`:

```python
word_count = structure["stats"]["word_count"]
tier = structure["tier_recommendation"]["tier"]  # 1, 2, hoặc 3
```

| Tier | Word Count | Strategy |
|---|---|---|
| 1 (Standard) | < 50K | Content map + tạo tất cả outline 1 lượt |
| 2 | 50K-100K | Content map trước, batch ~10 outline/lượt |
| 3 | >= 100K | Fast path, minimal analysis, batch ~10 outline/lượt |

### Xác định số bài

Công thức chính (áp dụng mọi tier):

```python
target = user_specified_count or max(3, round(word_count / 2500))
```

`structure.json.stats.estimated_articles` là ước lượng sơ bộ (dựa trên heading count), chỉ dùng tham khảo.

## Direct Path (chỉ Tier 1)

Direct Path xử lý toàn bộ tài liệu trong 1 lượt, không cần batch.

**Eligible khi:** `word_count < 20K` HOẶC `word_count < 50K VÀ estimated_articles <= 3`

**Capacity limit theo ngôn ngữ:**

| Ngôn ngữ | Limit | Token/word ratio |
|---|---|---|
| EN | ~44K words | ~1.3 |
| VI | ~32K words | ~1.8 |
| Mixed | ~38K words | ~1.5 |

```
eligible?
├─ YES AND capacity_ok → Xử lý 1 lượt
├─ YES BUT NOT capacity_ok → Dùng subagent (xem mục Subagent)
└─ NO → Xử lý theo tier workflow
```

## Tier Workflows

### Tier 1 (< 50K words)

1. Đọc structure.json: outline, stats, tier
2. Tạo content map: group sections theo cluster từ outline
3. Tạo outline cho tất cả bài (1 lượt)

### Tier 2 (50K-100K words)

1. Đọc structure.json: outline, stats, tier
2. Tạo content map (bắt buộc trước khi tạo outline)
3. Batch processing: ~10 outline/batch
4. Coverage check sau mỗi batch
5. Hỏi user confirm trước batch tiếp

### Tier 3 (>= 100K words): Fast Path

Giảm 40% overhead bằng cách tối giản analysis.

1. Đọc structure.json: outline, stats, `suggested_chunks`
2. Tạo content map: dùng `suggested_chunks` + outline
3. Batch processing: ~10 outline/batch, dùng `heading_path` từ chunks để hiểu context

### Đọc content.md khi cần (mọi tier)

```python
section = structure["outline"][i]
Read(content_md, offset=section["line"], limit=section["line_end"] - section["line"] + 1)
```

## Fallback: structure.json không có hoặc lỗi

Khi conversion thành công nhưng structure.json không tạo được (script báo `structure_error`):

1. Đọc content.md trực tiếp (toàn bộ nếu < 20K words, 5K words đầu nếu lớn hơn)
2. Tự tạo content map thủ công từ headings trong content.md
3. Ước lượng số bài: `max(3, round(word_count / 2500))` (đếm word_count bằng `wc -w`)
4. Xử lý như Tier 1 (không batch) nếu < 50K, như Tier 2 (batch) nếu lớn hơn

## Subagent Workflow

Dùng khi `direct_path.capacity_ok = false` hoặc tài liệu lớn cần xử lý song song.

### Flow

1. **Main agent**: đọc structure.json, tạo content map, phân chia chunks
2. **Subagent**: nhận chunk, đọc content.md section đó, tạo outline
3. **Main agent**: tổng hợp outline, coverage check, tạo index.md

Mỗi subagent xử lý 1 chunk (~11,500 words). Chunks có overlap (~10 dòng) để đảm bảo continuity.

### Prompt template cho subagent

```
Bạn là content planner. Nhiệm vụ: tạo outline cho các bài viết từ đoạn tài liệu được giao.

**Context:**
- Tài liệu: {title}
- Audience: {audience}
- Goal: {goal}
- Chunk {chunk_id}: dòng {line_start}-{line_end} ({word_count} words)
- Heading path: {heading_path}
- Tổng quan content map: {content_map_summary}

**Nhiệm vụ:**
1. Đọc file {content_md_path} từ dòng {line_start} đến {line_end}
2. Xác định các ý chính có thể tách thành bài riêng
3. Tạo outline cho mỗi bài theo format:
   ### Bài [N]: [Tiêu đề]
   - Thesis: [1 câu]
   - Key points: [ý chính + data/ví dụ + nguồn]
   - Takeaway: [insight chính]
   - Open questions: [data còn thiếu]

**Ràng buộc:**
- 1 bài = 1 chủ đề duy nhất
- KHÔNG viết draft, KHÔNG đề xuất cách viết/tone/style
- Output tiếng Việt, giữ thuật ngữ gốc trong ngoặc

Ghi output vào {output_dir}/chunk-{chunk_id}-outlines.md
```

## Quality Gate (áp dụng mọi tier)

| Tiêu chí | Mô tả |
|---|---|
| Sections mapped | Tất cả sections trong structure.json đã được map vào ít nhất 1 outline |
| Critical sections | Sections có `critical: true` được ưu tiên cover |
| Coverage 100% | Sau tất cả batches, mọi concept trong content map có outline |
| Số bài hợp lý | Gần với `max(3, round(word_count / 2500))`, sai lệch > 30% cần giải thích |

## Lưu ý chất lượng conversion

**XLSX/PPTX**: Docling chuyển spreadsheet/presentation sang markdown có thể mất cấu trúc. Sau khi convert, kiểm tra content.md:
- Bảng bị vỡ hoặc data không đọc được: báo user export sang CSV/PDF trước
- Slide chỉ có hình ảnh (ít text): báo user nội dung text có thể không đủ
