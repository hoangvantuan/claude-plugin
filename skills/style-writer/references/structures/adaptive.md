---
name: adaptive
recommended_voice: any
best_for:
  - Mixed content types
  - Content that doesn't fit a single structure
  - Multi-topic articles
  - Exploratory writing
version: 1.0.0
---

# Adaptive (Linh Hoạt)

## Overview

Cấu trúc linh hoạt, tự chọn tổ chức dựa trên nội dung thực tế. Subagent quyết định cách tổ chức tối ưu nhất cho bài viết, trong khuôn khổ guardrails dưới đây. Dùng khi content là hỗn hợp nhiều loại hoặc không fit vào 7 structures cố định.

**Triết lý:** Content-driven organization, không ép nội dung vào khuôn

## Guardrails (BẮT BUỘC)

1. Opening: MUST use SERIES_CONTEXT.opening_technique (from Opening Palette of any structure)
2. Must have clear 3-part flow: Hook → Development → Closing
3. Each H2 section MUST have a clear purpose (implicit or explicit)
4. Closing MUST connect to SERIES_CONTEXT.next_article

## Development Strategy (chọn theo CONTENT_TYPE)

| Content Type | Strategy                                                       | Style Reference  |
| ------------ | -------------------------------------------------------------- | ---------------- |
| `tutorial`   | Intuition → Concept → Example → Apply                          | Building Blocks  |
| `conceptual` | Surface → Deeper → Connections                                 | Five Layers      |
| `narrative`  | Scene → Encounter → Transformation                             | Story Arc        |
| `analysis`   | Conclusion → Evidence → Implications                           | BLUF-Evidence    |
| `mixed`      | Combine techniques. Start with dominant type, weave others in. | Subagent decides |


**Khi `mixed`:** Xác định loại content chiếm >50% → dùng strategy đó làm backbone → weave các loại khác vào.

## Opening Palette

> Mô tả chi tiết từng technique xem [shared-rules.md](../shared-rules.md#opening-palette-master).

Adaptive có thể dùng Opening Palette từ BẤT KỲ structure nào. Lựa chọn dựa trên content_type hint:

- `tutorial` → question-first, scenario, provocation
- `conceptual` → assumption-challenge, contrast, question-first
- `narrative` → scene-setting, in-medias-res, memory-flash
- `analysis` → bold-claim, contrast, scene-setting
- `mixed` → bất kỳ technique nào phù hợp

**KHÔNG lặp technique giữa 2 bài liên tiếp trong series.**

## Constraints

- Max 5 H2 sections per article (prevent sprawl)
- Each H2: 300-800 words (balanced depth)
- Transitions between H2s MUST be narrative (not mechanical "Tiếp theo...")
- DO NOT switch organization style mid-section (pick per H2, not per paragraph)
- Closing: match voice register
  - casual → open question hoặc hình ảnh
  - formal → summary + action items
  - neutral → bridge to next article

## Quality Checklist

- [ ] Opening dùng technique từ SERIES_CONTEXT?
- [ ] 3-part flow rõ ràng (Hook/Development/Closing)?
- [ ] Mỗi H2 có purpose?
- [ ] <=5 H2 sections?
- [ ] Transitions narrative, không mechanical?
- [ ] Closing kết nối với bài sau?
