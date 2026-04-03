# Framework Mapping

Quy tắc chọn và áp dụng framework theo content type.

## Content Type → Framework

| Content Type       | Primary Framework              | Opening Pattern                                   | Body Pattern                                                                   | Closing Pattern                                  |
| ------------------ | ------------------------------ | ------------------------------------------------- | ------------------------------------------------------------------------------ | ------------------------------------------------ |
| Hướng dẫn/Giáo dục | Gagné's 9 Events + Scaffolding | Mục tiêu học → Recall kiến thức cũ → Hook câu hỏi | Concept scaffolding: simple→complex, Def→Example→Non-example, Knowledge checks | Tóm tắt + Bài tập thực hành + Tài liệu tham khảo |
| Business/Báo cáo   | Pyramid Principle (default)    | Kết luận/Đề xuất trước → Context                  | Top-down: Recommendation → 3 supporting args → Data evidence                   | Key takeaways + Next steps + Decision needed     |
| Business/Báo cáo   | SCQA (alternative)             | Situation → Complication → Question               | Answer trước → Supporting evidence → Data drill-down                           | Key takeaways + Next steps + Decision needed     |
| Thuyết phục/Pitch  | PAS + Sparkline (Duarte)       | Problem hook → Agitate (amplify pain)             | What IS vs What COULD BE oscillation, social proof, benefits                   | Strong CTA + Urgency + Contact                   |
| Technical/Process  | SCR + Step-by-step             | Situation → Complication → Why solve now          | Sequential steps, comparison tables, architecture flow, cause-effect           | Summary + Implementation roadmap + Resources     |

**Lưu ý Business/Báo cáo:** User chọn framework ở Step 1A. Pyramid = answer-first (audience đã biết vấn đề), SCQA = frame vấn đề trước (audience cần được convince về severity). Recommend SCQA cho Executive audience, Pyramid cho Mixed/General.

### Gagné's 9 Events (Hướng dẫn/Giáo dục)

1. Gain attention (hook/câu hỏi mở)
2. Inform objectives (slide mục tiêu)
3. Stimulate recall (kết nối kiến thức cũ)
4. Present content (nội dung chính, scaffolding)
5. Provide guidance (ví dụ, analogy, mental models)
6. Elicit performance (câu hỏi kiểm tra/bài tập)
7. Provide feedback (đáp án/giải thích)
8. Assess performance (quiz tổng hợp)
9. Enhance retention (tóm tắt + tài liệu + call to practice)

### SCQA Framework (Business/Báo cáo — Alternative)

Dùng khi audience cần được "framed" vấn đề trước khi nghe answer. Đặc biệt hiệu quả cho executive briefings.

1. **Situation** — Bối cảnh không thể tranh luận, facts mọi người đều biết
2. **Complication** — Tension/vấn đề phát sinh từ situation, tạo urgency
3. **Question** — Câu hỏi cốt lõi mà presentation sẽ trả lời (explicit hóa vấn đề)
4. **Answer** — Recommendation/solution, đặt ngay sau Question (top-down like Pyramid)

**SCQA Slide Pattern:**

- Slide 1 `[title]`: Title + tagline framing the question
- Slide 2 `[content]`: Situation — 2-3 bullets facts/context
- Slide 3 `[content]`: Complication — tension, data showing problem severity
- Slide 4 `[statement]`: Question — 1 câu hỏi lớn, centered
- Slide 5+ `[content]`: Answer — recommendations rồi supporting evidence (top-down)
- Closing: Key takeaways + Decision needed

**Khác biệt với Pyramid:** Pyramid bỏ qua Situation/Complication, nhảy thẳng vào Answer. SCQA dành 2-3 slides đầu để frame vấn đề → hiệu quả hơn khi audience chưa fully aware severity.

### Educational Slide Patterns

- Definition → Example → Non-example
- Analogy/Metaphor: giải thích phức tạp bằng so sánh quen thuộc
- Before/After comparison
- Misconception: "Nhiều người nghĩ X, thực tế là Y"
- Knowledge check: câu hỏi reflection giữa sections
- Vietnamese pattern: Mục tiêu → Nội dung → Ví dụ → Bài tập → Tóm tắt

## Narrative Arc per Framework

Mỗi framework có narrative arc ngầm định. Áp dụng khi tạo outline để đảm bảo flow tự nhiên.

| Framework         | Narrative Arc                                  | Tension Source                             | Release Source                            |
| ----------------- | ---------------------------------------------- | ------------------------------------------ | ----------------------------------------- |
| Pyramid Principle | Inverted pyramid (answer-first, justify after) | Supporting arguments challenge assumptions | Recommendations confirmed by data         |
| SCQA              | Problem framing → Answer                       | Complication escalates severity            | Question được answer rõ ràng              |
| PAS + Sparkline   | "What IS" ↔ "What COULD BE" oscillation        | Current pain (What IS slides)              | Vision/possibility (What COULD BE slides) |
| Gagné             | Progressive disclosure (build up)              | Knowledge gap/question chưa answer         | Worked example/answer/feedback            |
| SCR               | Problem → Solution linear                      | Complication tạo urgency                   | Resolution steps giải quyết               |

### Áp dụng trong outline

- **Pyramid/SCQA**: Body slides alternate giữa recommendation (release) và evidence/challenge (tension)
- **PAS + Sparkline**: Cứ 2-3 slides "What IS" (pain) → 1-2 slides "What COULD BE" (vision). Kết thúc bằng "New Bliss" (CTA)
- **Gagné**: Build từ simple → complex, xen knowledge checks giữa sections. Tension = câu hỏi chưa answer, Release = worked example
- **SCR**: Complication chiếm 20-30% body, Resolution chiếm 70-80%. Không kéo dài complication quá lâu

Narrative arc được auto-assign theo framework — KHÔNG cần hỏi user.
