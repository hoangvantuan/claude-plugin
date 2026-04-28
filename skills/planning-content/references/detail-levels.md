# Output Detail Levels

Cho phép user chọn mức độ chi tiết cho output articles.

## Quick Reference

| Mode          | Ratio  | Mô tả                           |
| ------------- | ------ | -------------------------------- |
| Concise       | 15-25% | Tóm lược, giữ ý chính            |
| **Standard**  | 30-40% | Cân bằng (Default)               |
| Comprehensive | 50-65% | Chi tiết, giữ nhiều ví dụ        |
| Faithful      | 75-90% | Gần như đầy đủ nội dung gốc      |

## Content Handling per Mode

| Mode          | Critical sections | Non-critical       | Examples | Quotes       |
| ------------- | ----------------- | ------------------ | -------- | ------------ |
| Concise       | 100% meaning      | 1-2 câu/section    | ~30%     | Quan trọng nhất |
| Standard      | 100% meaning      | Summarize + key ex | ~60%     | Key quotes   |
| Comprehensive | 100% meaning      | Most content       | ~85%     | Most quotes  |
| Faithful      | 100% meaning      | Full content       | 100%     | All quotes   |

## Validation Rules

```yaml
section_coverage: 100%        # Tất cả sections phải được đề cập
critical_faithful: 100%       # Critical sections giữ 100% meaning ở MỌI detail level

# Word count chỉ mang tính thống kê
# PASS/FAIL dựa trên section_coverage (100%)
# Target ratio là tham khảo, không bắt buộc
# Priority: section_coverage > critical_faithful > output_ratio
```

## Tính toán Target Words (Tham khảo)

Target words dùng để ước lượng khi chia bài (Step 3.3).

### Formula

```
target_ratio = (min_ratio + max_ratio) / 2
total_target = source_words × target_ratio

Per article:
article_target = (article_source_words / total_source_words) × total_target
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
4. Faithful (75-90%): Gần như đầy đủ nội dung gốc
```
