# Báo cáo cải tiến skill: social-post

**Ngày**: 2026-04-20
**Skill**: `skills/social-post/`
**Xếp loại**: Tốt → Xuất sắc (29/40 → 33/40)

## Điểm trước / sau

| Tiêu chí | Trước | Sau | Delta |
|---|---|---|---|
| Clarity | 4 | 4 | 0 |
| Specificity | 4 | 4 | 0 |
| Coverage | 4 | 4 | 0 |
| Structure | 4 | 5 | +1 |
| Cognitive Load | 3 | 4 | +1 |
| Bloat Score | 2 | 4 | +2 |
| Anti-patterns | 3 | 4 | +1 |
| Description Quality | 5 | 5 | 0 |
| **Tổng (/40)** | **29** | **33** | **+5** |
| **SKILL.md dòng** | **177** | **137** | **-40 (-22.6%)** |

## Cải tiến đã thực hiện

### 1. Xoá Bước 5 "Apply Power Techniques" (lặp với craft-techniques.md)

- Power Techniques ở SKILL.md Bước 5 (11 bullets) trùng gần như nguyên văn với `references/craft-techniques.md` dòng 95-105.
- Hành động: merge thành 1 câu pointer trong Bước 4 kèm tóm tắt ngắn các keyword ("xưng bạn, strategic vagueness, memorable phrase, xuống dòng mỗi đoạn, không emoji/hashtag/citation/link/CTA").
- Renumber các bước sau: 6→5, 7→6, 8→7. Heading "Quy trình 8 bước" → "Quy trình 7 bước".

### 2. Xoá section "Constraints (tóm lại một chỗ)"

- Section 9 dòng ở cuối file lặp lại nội dung đã có trong workflow steps.
- Có 3 instances "TUYỆT ĐỐI KHÔNG" — anti-pattern lệnh cứng thay vì giải thích lý do.
- Các constraint thực sự quan trọng (độ dài, tone, tuyệt đối không...) đã nằm trong các workflow steps tương ứng.

### 3. Rút gọn "Output Format"

- Template ASCII 11 dòng chỉ lặp lại cấu trúc 5 phần đã định nghĩa chi tiết ở Bước 4 (Tiêu đề / Hook / Tension / Escalation / Turn).
- Thay bằng 2 câu ngắn: độ dài + output chỉ chứa bài viết + pointer đến example.

### 4. Rút gọn Bước 6 "Anti-AI Writing" tóm tắt

- 6 bullet tóm tắt thành 3 bullet critical nhất (em dash, staccato, AI vocab).
- Thêm rationale 1 câu giải thích tại sao anti-AI quan trọng ("người đọc nhận ra và scroll qua") — áp dụng P3 Replace Commands with Reasoning.

## Bài học rút ra (áp dụng được cho skill khác)

### 1. Power Techniques / Core rules không nên lặp giữa SKILL.md và references

Khi SKILL.md có một Bước "Apply X Techniques" nhưng references đã liệt kê chi tiết các techniques đó — đó là red flag cho Single Source violation. Giải pháp: SKILL.md chỉ pointer, references chứa chi tiết.

### 2. "Constraints (tóm lại một chỗ)" thường là dead section

Mọi constraint quan trọng đã phải xuất hiện trong workflow steps. Section tóm tắt cuối file chỉ khuếch đại redundancy và dễ sinh ra anti-pattern "TUYỆT ĐỐI KHÔNG" kiểu khẩu hiệu. Check khi audit skill: nếu có section "Constraints" / "Summary" / "Rules" ở cuối workflow — khả năng cao là bloat.

### 3. Output template ASCII thường trùng với workflow definition

Nếu Bước X đã định nghĩa cấu trúc output (5 phần, 3 sections...) thì template ASCII ở cuối file thường chỉ vẽ lại cùng cấu trúc đó. Thay bằng 1-2 câu pointer + ví dụ trong references.

### 4. Heading renumber khi xoá step

Khi xoá 1 step trong workflow đánh số, phải renumber các step sau + heading tổng "Quy trình N bước". Dễ sót — cần grep toàn file xác nhận.

### 5. "TUYỆT ĐỐI KHÔNG" đếm được là chỉ số bloat

Số instances MUST/NEVER/"TUYỆT ĐỐI KHÔNG" tỷ lệ nghịch với chất lượng skill. >3 instances thường là dấu hiệu cần convert sang lý do (P3). Skill social-post có 3 instances → 0 instances sau cải tiến.
