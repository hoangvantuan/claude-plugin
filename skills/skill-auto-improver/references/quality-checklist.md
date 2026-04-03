# Quality Checklist — Đánh giá chất lượng Skill

Dùng 8 tiêu chí dưới đây để chấm điểm skill (thang 1-5 mỗi tiêu chí).

## 1. Clarity (Rõ ràng)

| Điểm | Mô tả |
|------|-------|
| 1 | Hướng dẫn mơ hồ, nhiều cách hiểu, thiếu ví dụ |
| 2 | Hiểu được nhưng phải đoán ý ở nhiều chỗ |
| 3 | Phần lớn rõ ràng, 1-2 chỗ mơ hồ |
| 4 | Rõ ràng, ranh giới hành vi được định nghĩa cụ thể |
| 5 | Không cách hiểu nào khác ngoài cách đúng |

**Kiểm tra:**
- Mỗi bước trong workflow có hành động cụ thể (động từ + đối tượng)?
- Có chỗ nào "tuỳ trường hợp" mà không nói rõ trường hợp nào?
- Output format có template/ví dụ cụ thể?

## 2. Specificity (Cụ thể hóa đúng mức)

| Điểm | Mô tả |
|------|-------|
| 1 | Quá chung chung, LLM phải tự đoán hầu hết quyết định |
| 2 | Có hướng dẫn nhưng thiếu constraints quan trọng |
| 3 | Đủ constraints cho happy path, thiếu edge cases |
| 4 | Constraints đầy đủ, edge cases được handle |
| 5 | Mọi quyết định quan trọng đều có hướng dẫn, kèm lý do |

**Kiểm tra:**
- Audience, tone, format được định nghĩa?
- Có constraints cho output length/structure?
- Edge cases được liệt kê (hoặc có quy tắc chung để xử lý)?

## 3. Coverage (Phạm vi)

| Điểm | Mô tả |
|------|-------|
| 1 | Chỉ cover 1 scenario đơn giản |
| 2 | Cover happy path, fail ở inputs khác biệt |
| 3 | Cover 2-3 scenarios phổ biến |
| 4 | Cover diverse scenarios, có fallback cho cases chưa biết |
| 5 | Cover rộng với quy tắc tổng quát thay vì liệt kê từng case |

**Kiểm tra:**
- Skill hoạt động với inputs đa dạng (ngắn/dài, đơn giản/phức tạp)?
- Có quy tắc chung cho trường hợp ngoài danh sách?
- References có đủ để hỗ trợ các trường hợp khác nhau?

## 4. Structure (Cấu trúc)

| Điểm | Mô tả |
|------|-------|
| 1 | Không có cấu trúc, text liên tục |
| 2 | Có headings nhưng logic không rõ |
| 3 | Cấu trúc hợp lý, flow theo thứ tự |
| 4 | Phân tầng tốt (SKILL.md → references), progressive disclosure |
| 5 | Mỗi section có mục đích rõ, không overlap, dễ navigate |

**Kiểm tra:**
- Frontmatter đúng format (name, description)?
- Workflow steps có thứ tự logic?
- Nội dung chi tiết có được tách vào references/?
- Có mục lục hoặc pointer rõ ràng đến references?

## 5. Cognitive Load (Tải nhận thức)

| Điểm | Mô tả |
|------|-------|
| 1 | Quá nhiều thông tin dump cùng lúc, LLM bị overload |
| 2 | Nhiều thông tin không cần thiết cho task chính |
| 3 | Chấp nhận được, có vài phần dư thừa |
| 4 | Lean — chỉ chứa thông tin cần thiết cho workflow |
| 5 | Tối ưu — progressive loading, chi tiết ở references, SKILL.md chỉ chứa decisions |

**Kiểm tra:**
- SKILL.md có quá 300 dòng không?
- Có thông tin nào repeat giữa các sections?
- Ví dụ/API details có nên chuyển vào references?
- Mỗi câu có contribute vào hành vi mong muốn không?

## 6. Bloat Score (Mức phình to)

| Điểm | Mô tả |
|------|-------|
| 1 | Cực kỳ phình — nhiều nội dung dead, lặp, hoặc không liên quan |
| 2 | Có bloat rõ ràng (sections lặp, ví dụ thừa, caveats dư) |
| 3 | Vài chỗ có thể cắt mà không mất chức năng |
| 4 | Lean — gần như mọi dòng đều cần thiết |
| 5 | Tối ưu — không cắt được gì thêm mà không mất chức năng |

**Dấu hiệu bloat:**
- Cùng ý nói lại bằng cách khác ở section khác
- MUST/NEVER/ALWAYS quá nhiều (>5 instances) → thay bằng giải thích lý do
- Ví dụ quá dài hoặc quá nhiều cho cùng concept
- Sections "nice to have" không ảnh hưởng output
- Comments/notes giải thích điều hiển nhiên

## 7. Anti-patterns (Mẫu sai)

| Điểm | Mô tả |
|------|-------|
| 1 | Nhiều anti-patterns nghiêm trọng (over-engineering, magic numbers, anti-laziness prompts) |
| 2 | 3-4 anti-patterns rõ ràng |
| 3 | 1-2 anti-patterns nhỏ |
| 4 | Không có anti-patterns phổ biến |
| 5 | Chủ động phòng tránh anti-patterns, có failure mode registry |

**Kiểm tra:**
- Có đưa quá nhiều lựa chọn thay vì 1 default + ngoại lệ?
- Có "be thorough" / "think carefully" gây overtriggering?
- Có magic numbers không giải thích?
- Có thông tin nhạy cảm thời gian (ngày/tháng cụ thể sẽ lỗi thời)?
- Có thuật ngữ không nhất quán (dùng nhiều từ cho cùng concept)?
- Scripts có xử lý lỗi tường minh hay "punt" cho Claude?

## 8. Description Quality (Chất lượng mô tả)

| Điểm | Mô tả |
|------|-------|
| 1 | Không có description hoặc quá chung chung ("A helpful skill") |
| 2 | Mô tả chức năng nhưng thiếu trigger phrases |
| 3 | Có chức năng + trigger phrases, nhưng thiếu ranh giới "khi nào KHÔNG dùng" |
| 4 | Trả lời đủ "làm gì" + "khi nào dùng", viết ngôi thứ ba |
| 5 | Cụ thể, có trigger phrases đa dạng, phân biệt rõ với skill tương tự |

**Kiểm tra:**
- Description trả lời "skill này làm gì" + "khi nào nên dùng"?
- Viết ngôi thứ ba (không dùng "I can help you...")?
- Có trigger phrases cụ thể (các từ/cụm từ user hay nói)?
- YAML frontmatter hợp lệ (name + description)?
- Phân biệt rõ với skill tương tự (tránh trigger nhầm)?

## Cách sử dụng

1. Đọc SKILL.md + references
2. Chấm điểm từng tiêu chí (1-5)
3. Ghi nhận xét ngắn cho mỗi tiêu chí (1 dòng)
4. Tính tổng (/40) và xếp loại:
   - 33-40: Xuất sắc — chỉ cần tinh chỉnh nhỏ
   - 25-32: Tốt — có cơ hội cải tiến rõ ràng
   - 17-24: Trung bình — cần refactor
   - <17: Yếu — cần viết lại đáng kể
