# Tier Processing Guide

Hướng dẫn xử lý tài liệu đã convert theo kích thước. Load file này khi input là tài liệu đã convert (có structure.json).

## Tier Detection

Đọc `structure.json` để xác định tier:

```python
structure = read("input-handling/structure.json")
word_count = structure["stats"]["word_count"]
tier = structure["tier_recommendation"]["tier"]
```

| Tier | Word Count | Strategy |
|---|---|---|
| **Standard** | < 50K words | Xử lý 1 lượt, tạo tất cả outline cùng lúc |
| **Tier 2** | 50K-100K | Content map trước, batch ~10 outline/lượt |
| **Tier 3** | >= 100K | Fast path, minimal analysis, batch ~10 outline/lượt |

**Direct Path check** (nằm trong Standard):

```
structure.json → direct_path.eligible?
├─ YES AND capacity_ok → Standard (xử lý 1 lượt)
├─ YES BUT NOT capacity_ok → Standard nhưng cảnh báo dung lượng
└─ NO → Xác định tier theo word count
```

## Standard Tier (< 50K words)

### Workflow

1. **Đọc structure.json**: outline, stats, tier
2. **Tạo content map**: dùng outline từ JSON, group sections theo cluster
3. **Tạo outline cho tất cả bài**: 1 lượt, không cần batch

### Xác định số bài

```python
if user_specified_article_count:
    target_articles = user_specified_count
else:
    # Ước lượng từ word count và detail ratio
    detail_ratio = detail_level_ratio  # VD: Standard = 0.35
    total_output = word_count * detail_ratio
    target_articles = max(3, round(total_output / 2500))
    target_articles = min(target_articles, 10)
```

### Content-Type Detection

Xác định `content_type` cho mỗi bài: `tutorial`, `conceptual`, `narrative`, `analysis`, `mixed`.

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

```markdown
## Coverage Checklist
- [x] Batch 1 (Chương 1-4): 10/10 outlines
- [ ] Batch 2 (Chương 5-8): 0/10
- [ ] Batch 3 (Chương 9-12): 0/10
```

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

## Detail Level và Ước lượng Output

| Detail Level | Ratio | Ý nghĩa |
|---|---|---|
| Concise | 15-25% | Tóm lược, giữ ý chính |
| Standard | 30-40% | Cân bằng (Default) |
| Comprehensive | 50-65% | Chi tiết, giữ nhiều ví dụ |
| Faithful | 75-90% | Gần như đầy đủ nội dung gốc |

**Tính toán:**

```python
target_ratio = (min_ratio + max_ratio) / 2  # VD: Standard = 0.35
total_target_words = word_count * target_ratio
articles_estimate = round(total_target_words / 2500)  # ~2500 words/bài
```

Chi tiết về các mức: xem [detail-levels.md](detail-levels.md).
