# Output Detail Levels

Cho phép user chọn mức độ chi tiết của output.

## Quick Reference

| Mode          | Ratio  | Mô tả                               |
| ------------- | ------ | ----------------------------------- |
| Concise       | 15-25% | Tóm lược, giữ ý chính               |
| **Standard**  | 30-40% | Cân bằng (Default)                  |
| Comprehensive | 50-65% | Chi tiết, giữ nhiều ví dụ           |
| Faithful      | 75-90% | Gần như đầy đủ, viết lại theo style |

## Chi tiết từng Mode

### Concise (Tóm lược)

```yaml
ratio: 15-25%
use_case: Người đọc bận, cần overview nhanh

content_handling:
  critical_sections: Full content, faithful rewrite (100% meaning, Vietnamese, style voice)
  non_critical: 1-2 câu tóm tắt mỗi section
  examples: Giữ ~30%, chọn tiêu biểu nhất
  quotes: Chỉ quotes quan trọng nhất

style_application: Viết mới, tóm lược theo style đã chọn
```

### Standard (Tiêu chuẩn) - Default

```yaml
ratio: 30-40%
use_case: Cân bằng giữa chi tiết và ngắn gọn

content_handling:
  critical_sections: Full content, faithful rewrite (100% meaning, Vietnamese, style voice)
  non_critical: Summarize nhưng giữ key examples
  examples: Giữ ~60%
  quotes: Giữ key quotes

style_application: Viết lại theo style, cân bằng
```

### Comprehensive (Chi tiết)

```yaml
ratio: 50-65%
use_case: Người muốn học sâu, tham khảo

content_handling:
  critical_sections: Full content, faithful rewrite (100% meaning, Vietnamese, style voice)
  non_critical: Include most content, light editing
  examples: Giữ ~85%
  quotes: Giữ most quotes

style_application: Viết lại theo style, chi tiết
```

### Faithful (Trung thành)

```yaml
ratio: 75-90%
use_case: Archive, reference, cần giữ gần như đầy đủ nội dung

content_handling:
  critical_sections: Full content, faithful rewrite (100% meaning, Vietnamese, style voice)
  non_critical: Full content, viết lại theo style
  examples: Giữ 100%
  quotes: Giữ all quotes

style_application: |
  Viết lại TOÀN BỘ theo style đã chọn.
  KHÔNG phải copy-paste hay chỉ format.
  Áp dụng voice, structure, sentence length của style.
  Giữ nguyên thuật ngữ và trích dẫn gốc.
```

## Validation Rules (Thống nhất)

Áp dụng cho TẤT CẢ modes:

```yaml
section_coverage: 100%        # Tất cả sections phải được đề cập
critical_faithful: 100%      # Critical sections MUST preserve 100% meaning (faithful rewrite) at ALL detail levels

# IMPORTANT: Word count chỉ mang tính thống kê
# - PASS/FAIL dựa trên section_coverage (100%)
# - KHÔNG yêu cầu viết lại nếu đã đủ ý (all sections covered)
# - Target ratio là tham khảo, không phải yêu cầu bắt buộc

# NOTE: Concise mode may exceed target ratio when critical sections are large.
# Priority: section_coverage (100%) > critical_faithful (100%) > output_ratio.
# If content is complete but word count differs from target, ACCEPT as-is.
```

## Tính toán Target Words (Tham khảo)

**LƯU Ý**: Target words chỉ mang tính tham khảo để định hướng độ dài bài viết.
Không dùng để đánh giá PASS/FAIL. Subagent không cần viết lại nếu đã cover hết ý.

### Formula

```
target_ratio = (min_ratio + max_ratio) / 2
total_target = source_words × target_ratio

Per article (reference only):
article_target = (article_source_words / total_source_words) × total_target
# NOTE: Không còn min/max cứng - word count chỉ để thống kê
```

### Ví dụ với source 26,791 words

| Mode          | Ratio | Total Target | Art 01 (8,877w) | Art 02 (6,419w) | Art 03 (4,025w) | Art 04 (4,609w) |
| ------------- | ----- | ------------ | --------------- | --------------- | --------------- | --------------- |
| Concise       | 20%   | \~5,400      | \~1,800         | \~1,300         | \~800           | \~900           |
| Standard      | 35%   | \~9,400      | \~3,100         | \~2,250         | \~1,400         | \~1,600         |
| Comprehensive | 57.5% | \~15,400     | \~5,100         | \~3,700         | \~2,300         | \~2,700         |
| Faithful      | 82.5% | \~22,100     | \~7,300         | \~5,300         | \~3,300         | \~3,800         |

## AskUserQuestion Format

```markdown
"Bạn muốn output với mức độ chi tiết nào?"

Options:
1. Concise (15-25%): Tóm lược, giữ ý chính
2. Standard (30-40%): Cân bằng chi tiết và ngắn gọn (Recommended)
3. Comprehensive (50-65%): Chi tiết, giữ nhiều ví dụ
4. Faithful (75-90%): Gần như đầy đủ, viết lại theo style
```

## Subagent Prompt Addition

Thêm vào subagent prompt:

```
TARGET: {target_words} words (reference only, source: {source_words} words)
MODE: {detail_level}

DEPTH RULES:
- Critical [Sxx]*: {critical_handling based on mode}
- Non-critical: {non_critical_handling based on mode}
- Examples: Keep {example_percentage}%
```

## Coverage Report Addition

```
DONE: {filename} | {output_words} words (stats)
COVERAGE (determines PASS/FAIL):
| Section | Status |
|---------|--------|
| S01 | ✅ summarized |
| S02 ⭐ | ✅ faithful |
RESULT: {PASS if all sections covered, FAIL if missing}
MODE: {detail_level}

# NOTE: Word count chỉ để thống kê, không ảnh hưởng PASS/FAIL
# PASS/FAIL chỉ dựa trên section coverage (100% = PASS)
```

