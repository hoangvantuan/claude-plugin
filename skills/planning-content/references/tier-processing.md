# Tier Processing Guide

Hướng dẫn xử lý tài liệu đã convert theo kích thước. Load file này khi input là tài liệu đã convert (có structure.json).

## Tier Detection

Đọc `structure.json` để xác định tier:

```python
structure = read("input-handling/structure.json")
word_count = structure["stats"]["word_count"]
tier = structure["tier_recommendation"]["tier"]  # 1, 2, hoặc 3
```

| JSON tier value | Tên | Word Count | Strategy |
|---|---|---|---|
| `1` | Tier 1 (Standard) | < 50K words | Xử lý 1 lượt, tạo tất cả outline cùng lúc |
| `2` | Tier 2 | 50K-100K | Content map trước, batch ~10 outline/lượt |
| `3` | Tier 3 | >= 100K | Fast path, minimal analysis, batch ~10 outline/lượt |

## Direct Path (chỉ Tier 1)

Direct Path cho phép xử lý toàn bộ tài liệu trong 1 lượt, không cần batch.

### Tiêu chí eligible

Từ `extract_structure.py`:

```
eligible = (word_count < 20,000) HOẶC (word_count < 50,000 VÀ estimated_articles ≤ 3)
```

Tài liệu nhỏ hoặc ít nội dung phân tán: xử lý trực tiếp hiệu quả hơn chia batch.

### Tiêu chí capacity_ok

Tùy ngôn ngữ tài liệu, context window có giới hạn khác nhau:

| Ngôn ngữ | Capacity limit | Lý do |
|---|---|---|
| EN | ~44K words | Token/word ratio thấp (~1.3) |
| VI | ~32K words | Token/word ratio cao (~1.8) |
| Mixed | ~38K words | Trung bình (~1.5) |

### Decision tree

```
structure.json → direct_path.eligible?
├─ YES AND capacity_ok → Xử lý 1 lượt, không batch
├─ YES BUT NOT capacity_ok → Cảnh báo, cân nhắc dùng subagent (xem mục Subagent)
└─ NO → Xử lý theo tier workflow bên dưới
```

## Tier 1: Standard (< 50K words)

### Workflow

1. **Đọc structure.json**: outline, stats, tier. KHÔNG đọc content.md (xem [context-optimization.md](context-optimization.md))
2. **Tạo content map**: dùng outline từ JSON, group sections theo cluster
3. **Tạo outline cho tất cả bài**: 1 lượt, không cần batch

### Xác định số bài

Dùng công thức từ SKILL.md Phase 4.2: `word_count / 2500`. `structure.json.stats.estimated_articles` là ước lượng sơ bộ (dựa trên heading count), chỉ dùng tham khảo.

### Quality Gate

- [ ] Tất cả sections đã được map vào outline
- [ ] Critical sections được đánh dấu
- [ ] Coverage 100%

## Tier 2 (50K-100K words)

### Workflow

1. **Đọc structure.json**: outline, stats, tier. KHÔNG đọc content.md (xem [context-optimization.md](context-optimization.md))
2. **Tạo content map**: bắt buộc trước khi tạo outline
3. **Batch processing**: ~10 outline/batch
4. **Coverage check**: sau mỗi batch, đối chiếu content map

### Batch Processing

- Hỏi user confirm trước khi làm batch tiếp
- Mỗi batch cập nhật `index.md`

### Đọc content.md khi cần

Khi cần chi tiết cho outline cụ thể, đọc theo section:

```python
section = structure["outline"][i]
Read(content_md, offset=section["line"], limit=section["line_end"] - section["line"] + 1)
```

### Quality Gate

- [ ] Content map hoàn chỉnh
- [ ] Tất cả sections mapped
- [ ] Coverage 100% sau tất cả batches
- [ ] Critical sections marked

## Tier 3 (>= 100K words): Fast Path

### Nguyên tắc

Giảm 40% overhead bằng cách tối giản analysis. Tài liệu quá lớn để đọc chi tiết, tập trung vào cấu trúc.

### Workflow

1. **Đọc structure.json**: outline, stats, chunks
2. **Tạo content map**: dùng `suggested_chunks` + `outline` từ JSON
3. **Batch processing**: ~10 outline/batch, dùng heading_path từ chunks để hiểu context

### Xử lý chunks

```python
for chunk in structure["suggested_chunks"]:
    # chunk có sẵn: line_start, line_end, word_count, heading_path
    # Dùng heading_path để hiểu vị trí trong tài liệu
    # Chỉ đọc content.md khi cần chi tiết cụ thể
```

### Đọc content.md selective

- Chỉ đọc section cụ thể khi cần chi tiết cho outline
- Ưu tiên critical sections
- Không đọc toàn bộ content.md

### Quality Gate

- [ ] Content map từ structure.json
- [ ] Tất cả chunks covered
- [ ] Coverage 100% sau tất cả batches
- [ ] Critical sections marked

## Subagent Workflow (khi capacity vượt giới hạn)

Khi `direct_path.capacity_ok = false` hoặc tài liệu lớn cần xử lý song song:

1. **Main agent**: đọc structure.json, tạo content map, phân chia chunks cho subagent
2. **Subagent**: nhận chunk (line_start, line_end) + context (heading_path), đọc content.md section đó, tạo outline cho các bài thuộc chunk
3. **Main agent**: tổng hợp outline từ subagents, chạy coverage check, tạo index.md

Mỗi subagent xử lý 1 chunk (~11,500 words). Chunks có overlap (~10 dòng) để đảm bảo continuity.

## Lưu ý chất lượng conversion

**XLSX/PPTX**: Docling chuyển spreadsheet/presentation sang markdown có thể mất cấu trúc (table layout, cell formatting, slide layout). Sau khi convert, kiểm tra nhanh content.md:
- Nếu bảng bị vỡ hoặc data không đọc được: báo user, đề xuất export sang CSV/PDF trước rồi convert lại.
- Nếu slide chỉ có hình ảnh (ít text): báo user nội dung text có thể không đủ để tạo outline.
