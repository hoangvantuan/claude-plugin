# Content Analysis Map Rules

Trước khi tạo outline, BẮT BUỘC tạo Content Analysis Map từ source material. Content Analysis Map không chỉ liệt kê topics mà còn **phân tích mối quan hệ** giữa chúng và **liên kết với Thesis**.

## Process

1. **Parse source**: Chia source thành sections dựa trên headings, paragraph breaks, topic shifts
2. **Extract**: Với mỗi section, ghi nhận:
   - Topic name (tên ngắn gọn)
   - Key concepts (khái niệm chính)
   - Key data (số liệu, metrics, examples đáng chú ý)
3. **Map Relationships**: Xác định mối quan hệ giữa các topics:
   - **Nhân quả**: Topic A dẫn đến Topic B (→)
   - **Bổ trợ**: Topic A và Topic B hỗ trợ lẫn nhau (↔)
   - **Tương phản**: Topic A vs Topic B (tension/contrast)
   - **Bao hàm**: Topic A là phần của Topic B
4. **Link to Thesis**: Mỗi topic được gán vai trò với Thesis:
   - `supports` — hỗ trợ trực tiếp thesis/key argument
   - `nuances` — bổ sung góc nhìn, làm sâu hơn
   - `counters` — phản bác, tạo tension
   - `contextualizes` — cung cấp bối cảnh
5. **Silent Clustering**: Tự động nhóm topics tương đồng thành "section buckets" — dựa trên relationships đã map. Nếu source đã có heading structure rõ ràng → dùng thẳng headings làm section buckets
6. **Rank priority** theo detail level đã chọn (xem bảng dưới)
7. **Giữ Content Analysis Map trong context** (KHÔNG show cho user), dùng làm checklist khi tạo outline

## Priority Assignment Rules

| Priority | L1                                            | L2                                               | L3                                     |
| -------- | --------------------------------------------- | ------------------------------------------------ | -------------------------------------- |
| `must`   | Thesis/kết luận chính, key metrics quyết định | Thesis + arguments + 1 example mỗi concept chính | Tất cả concepts + examples + code      |
| `should` | Supporting arguments, secondary metrics       | Additional examples, comparisons, config details | Edge cases, advanced details           |
| `nice`   | Examples, explanations, details               | Edge cases, caveats nhỏ                          | References, footnotes, tangential info |

## Coverage Thresholds

- **L1**: ≥ 100% `must` topics phải xuất hiện trong outline
- **L2**: ≥ 100% `must` + ≥ 70% `should` topics
- **L3**: ≥ 100% `must` + ≥ 90% `should` + best-effort `nice` topics

## Content Analysis Map Format (internal)

```
=== CONTENT ANALYSIS MAP ===
THESIS: [Core message 1 câu assertion]
KEY ARGUMENTS:
  1. [Argument 1]
  2. [Argument 2]
  3. [Argument 3]
INTENDED TRANSFORMATION: [educate/persuade/activate] — [mô tả]

TOPIC RELATIONSHIPS:
- Topic 1 → Topic 4 (nhân quả)
- Topic 2 ↔ Topic 5 (bổ trợ)
- Topic 3 vs Topic 6 (tension/contrast)

TOPICS:
1. [must] Topic name — key concept A, metric B → supports Argument 1
2. [must] Topic name — concept C, example D → supports Argument 1
3. [should] Topic name — comparison X vs Y → nuances Argument 2
4. [should] Topic name — config detail Z → contextualizes Argument 3
5. [nice] Topic name — edge case W → counters Argument 1
6. [R][should] Researched topic — statistic (Source: url) → supports Argument 2
7. [R][nice] Researched example — case study (Source: url) → contextualizes
=== END CONTENT ANALYSIS MAP ===
```

## Tag `[R]` (Researched)

Items có prefix `[R]` là thông tin bổ sung từ web research (Step 2), không có trong source gốc.

- `[R]` items vẫn phải gán priority (`must`/`should`/`nice`) theo tiêu chí bình thường
- `[R]` items KHÔNG được gán `must` trừ khi source gốc thiếu data critical cho topic chính
- Thông thường `[R]` items là `should` hoặc `nice`
- Max 10 `[R]` items trong 1 Content Analysis Map
- Coverage Report phải phân biệt source gốc vs researched items
