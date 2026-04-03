# Improvement Patterns — Các mẫu cải tiến tổng quát

Mỗi pattern là một giải pháp tổng quát áp dụng được cho nhiều skill. Khi phân tích skill, đối chiếu với danh sách này để tìm cải tiến phù hợp.

## P1: Tách tầng (Extract to References)

**Khi nào:** SKILL.md > 300 dòng, hoặc chứa API specs, ví dụ dài, danh sách chi tiết.

**Hành động:** Chuyển nội dung chi tiết vào `references/`, giữ lại pointer + 1 dòng mô tả khi nào cần đọc.

**Trước:**

```markdown
## API Reference
### Endpoint 1: /users
... (50 dòng chi tiết)
### Endpoint 2: /posts  
... (50 dòng chi tiết)
```

**Sau:**

```markdown
## API Reference
Chi tiết API → [api-reference](references/api-reference.md). Đọc khi cần gọi API cụ thể.
```

**Hiệu quả:** Giảm cognitive load, SKILL.md chỉ chứa workflow decisions.

---

## P2: Gộp trùng lặp (Merge Redundancy)

**Khi nào:** Cùng một ý được diễn đạt ở 2+ nơi trong skill (dù khác wording).

**Hành động:** Giữ phiên bản rõ nhất ở vị trí hợp lý nhất, xoá các bản trùng.

**Dấu hiệu:** Grep các keyword chính — nếu xuất hiện ở nhiều sections với context tương tự → trùng lặp.

**Hiệu quả:** Giảm bloat, tránh mâu thuẫn giữa các phiên bản.

---

## P3: Thay lệnh cứng bằng lý do (Replace Commands with Reasoning)

**Khi nào:** Nhiều MUST/NEVER/ALWAYS (>5 instances) mà không giải thích tại sao.

**Hành động:** Chuyển từ "MUST do X" → "Do X because [lý do]. Nếu không, [hậu quả]."

**Trước:**

```markdown
MUST ALWAYS use Vietnamese diacritics. NEVER write without dấu.
```

**Sau:**

```markdown
Viết đầy đủ dấu tiếng Việt — text không dấu gây hiểu sai nghĩa và thiếu chuyên nghiệp.
```

**Hiệu quả:** LLM hiểu intent, tự quyết định đúng trong edge cases thay vì chỉ tuân theo rule cứng.

---

## P4: Tổng quát hóa ví dụ (Generalize Examples)

**Khi nào:** Ví dụ quá cụ thể (tên người thật, data thật, case đặc thù) hoặc quá nhiều ví dụ cho cùng concept.

**Hành động:**

- Giữ 2-3 ví dụ diverse (thay vì 5+ ví dụ tương tự)
- Chọn ví dụ cover edge cases khác nhau (ngắn/dài, đơn giản/phức tạp)
- Thêm 1 dòng giải thích pattern chung mà ví dụ minh hoạ

**Hiệu quả:** LLM học pattern thay vì copy ví dụ cụ thể.

---

## P5: Làm rõ ranh giới quyết định (Clarify Decision Boundaries)

**Khi nào:** Workflow có chỗ "tuỳ trường hợp" / "nếu phù hợp" mà không nói rõ điều kiện.

**Hành động:** Thêm điều kiện cụ thể dạng if/then hoặc bảng quyết định.

**Trước:**

```markdown
Chọn format phù hợp cho nội dung.
```

**Sau:**

```markdown
| Nội dung | Format |
|----------|--------|
| < 500 từ, 1 ý chính | Đoạn văn ngắn |
| 500-2000 từ, nhiều ý | Heading + bullet points |
| > 2000 từ | Tách sections với mục lục |
```

**Hiệu quả:** Giảm ambiguity, output nhất quán hơn giữa các lần chạy.

---

## P6: Thêm progressive disclosure (Add Loading Layers)

**Khi nào:** Skill load toàn bộ references ngay từ đầu, hoặc SKILL.md chứa quá nhiều context cho mọi trường hợp.

**Hành động:** Thêm trigger rõ ràng cho việc đọc references — "Đọc file X khi gặp trường hợp Y".

**Hiệu quả:** Tiết kiệm context window, skill phản hồi nhanh hơn.

---

## P7: Chuẩn hóa output (Standardize Output Format)

**Khi nào:** Skill không định nghĩa rõ output format, hoặc output format không nhất quán.

**Hành động:** Thêm template output với placeholder rõ ràng. Bao gồm:

- Đường dẫn lưu file (nếu tạo file)
- Cấu trúc sections
- Naming convention

**Hiệu quả:** Output nhất quán, dễ tìm lại, dễ tự động hoá.

---

## P8: Sắp xếp lại thứ tự hướng dẫn (Reorder Instructions)

**Khi nào:** Thông tin quan trọng bị chôn ở giữa hoặc cuối skill, nội dung ít quan trọng ở đầu.

**Hành động:** Sắp xếp theo primacy/recency bias:

1. **Đầu:** Persona + core workflow (quan trọng nhất)
2. **Giữa:** Context, references, chi tiết
3. **Cuối:** Output format, constraints, final checks

**Hiệu quả:** LLM ghi nhớ tốt hơn thông tin ở đầu và cuối prompt.

---

## P9: Loại bỏ dead content (Remove Dead Content)

**Khi nào:** Có sections không ảnh hưởng output — comments giải thích điều hiển nhiên, disclaimers, meta-notes về skill.

**Hành động:** Xoá. Nếu không chắc → tạm comment out, test, xác nhận output không đổi → xoá.

**Dấu hiệu dead content:**

- "Note: ..." giải thích điều model đã biết
- Sections chưa implement ("TODO", "planned")
- Phiên bản cũ được comment out thay vì xoá

**Hiệu quả:** Giảm noise, tăng signal-to-noise ratio.

---

## P10: Thống nhất ngôn ngữ (Unify Language)

**Khi nào:** Skill trộn lẫn tiếng Anh/Việt không có pattern rõ ràng, hoặc terminology không nhất quán (dùng nhiều từ khác nhau cho cùng concept).

**Hành động:**

- Chọn ngôn ngữ chính dựa trên target audience
- Technical terms giữ tiếng Anh nếu dịch gây mất nghĩa
- Tạo glossary ngắn nếu skill dùng thuật ngữ domain-specific

**Hiệu quả:** Giảm confusion, tăng consistency.

---

## P11: Chẩn đoán qua quan sát hành vi (Observation-based Diagnosis)

**Khi nào:** Skill đã deploy nhưng output không như mong đợi, hoặc muốn tinh chỉnh dựa trên thực tế sử dụng.

**Hành động:** Quan sát cách Claude điều hướng skill và nhận diện tín hiệu:

| Tín hiệu quan sát | Vấn đề | Giải pháp |
|-------------------|--------|-----------|
| Claude đọc file theo thứ tự bất ngờ | Cấu trúc chưa trực giác | Sắp xếp lại flow, thêm pointer rõ hơn |
| Claude không theo reference đến file quan trọng | Link không nổi bật | Đưa link lên cao hơn, thêm mô tả khi nào cần đọc |
| Claude đọc đi đọc lại cùng 1 section | Section đó quan trọng hơn vị trí hiện tại | Đưa vào SKILL.md chính thay vì references |
| Claude không bao giờ mở 1 file đi kèm | File không cần thiết hoặc tín hiệu kém | Cân nhắc xoá hoặc cải thiện pointer |
| Claude over-engineer output | Skill thiếu constraints hoặc Degrees of Freedom sai | Thêm constraints rõ, giảm mức tự do |

**Hiệu quả:** Cải tiến dựa trên hành vi thực tế thay vì phỏng đoán — chính xác hơn bất kỳ static analysis nào.

---

## P12: Tối ưu Description (Optimize Trigger Mechanism)

**Khi nào:** Skill không được kích hoạt khi cần, hoặc bị kích hoạt nhầm.

**Hành động:**
- Description phải trả lời: "làm gì" + "khi nào dùng"
- Viết ngôi thứ ba (không "I can help you...")
- Thêm trigger phrases đa dạng (các cách user hay nói)
- Phân biệt rõ với skill tương tự
- Công thức: `[Chức năng cụ thể] + [Trigger contexts] + [Khi nào KHÔNG dùng]`

**Trước:**
```yaml
description: A skill for creating content
```

**Sau:**
```yaml
description: >
  Lên kế hoạch và viết bài Facebook + Blog. Kích hoạt khi user muốn
  viết bài, lên content plan, hoặc nói "viết post", "content cho FB".
  Không dùng cho email marketing (dùng email-writer).
```

**Hiệu quả:** Tăng trigger accuracy — skill được gọi đúng lúc, không bị bỏ sót hay nhầm lẫn.

---

## Cách sử dụng

1. Chạy quality-checklist → xác định tiêu chí điểm thấp
2. Map tiêu chí thấp → patterns liên quan:
   - Clarity thấp → P3, P5, P10
   - Specificity thấp → P5, P7
   - Coverage thấp → P4, P5
   - Structure thấp → P1, P6, P8
   - Cognitive Load cao → P1, P2, P6, P8
   - Bloat cao → P2, P4, P9
   - Anti-patterns nhiều → P3, P9, P10
   - Description yếu → P12
3. Nếu skill đã deploy, dùng P11 (quan sát hành vi) để bổ sung insights
4. Đối chiếu với [design-patterns](design-patterns.md) — chọn pattern phù hợp loại skill
5. Chọn max 5 patterns áp dụng, ưu tiên high-impact + low-effort
6. Ước tính tác động dòng (+/-) cho mỗi pattern
