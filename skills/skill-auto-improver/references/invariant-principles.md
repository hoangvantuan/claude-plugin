# Nguyên lý bất biến khi viết / cải tiến Skill

Mười nguyên lý này áp dụng cho mọi skill bất kể domain — content creation, automation, hay analysis. Dùng làm kim chỉ nam khi phân tích và cải tiến.

## 1. Giải thích lý do thay vì ra lệnh

LLM hiểu **"tại sao"** tốt hơn **"phải làm"**. Khi hiểu intent, model tự quyết định đúng trong edge cases mà lệnh cứng không cover được.

- `MUST do X` → `Do X because [lý do]. Nếu không, [hậu quả]`
- Nếu thấy >5 instances MUST/NEVER/ALWAYS → cờ đỏ, cần rewrite

## 2. Tổng quát hóa > Cụ thể hóa

Mọi hướng dẫn phải áp dụng được cho nhiều trường hợp. Fix cho 1 case cụ thể = overfitting.

- Pattern chung + 2-3 ví dụ diverse > 10 ví dụ cùng loại
- Ví dụ nên cover edge cases khác nhau (ngắn/dài, đơn giản/phức tạp, niche khác nhau)
- Thêm 1 dòng giải thích pattern mà ví dụ minh hoạ

## 3. Progressive Disclosure (Tải theo nhu cầu)

Không dump toàn bộ thông tin cùng lúc. Tận dụng primacy/recency bias — LLM ghi nhớ tốt nhất thông tin ở đầu và cuối prompt.

- SKILL.md chỉ chứa **workflow + quyết định**
- Chi tiết/ví dụ/API → `references/`, load khi cần
- Sắp xếp: persona + core workflow (đầu) → context (giữa) → output format + constraints (cuối)

## 4. Mỗi dòng phải earn chỗ đứng

Nếu xoá 1 dòng mà output không thay đổi → dòng đó là dead content. Thêm nội dung = phải cắt nội dung khác hoặc chứng minh nó cần thiết.

- Signal-to-noise ratio quan trọng hơn độ dài
- Dead content: notes giải thích điều hiển nhiên, TODO sections, code comment out
- Thêm nội dung mới → budget: tổng dòng sau <= trước (trừ skill quá ngắn thiếu coverage)

## 5. Single Source of Truth

Mỗi thông tin chỉ định nghĩa **1 nơi duy nhất**. Trùng lặp giữa sections → risk mâu thuẫn khi cập nhật, gây confusion cho model.

- Grep keyword chính — nếu xuất hiện ở nhiều sections với context tương tự → trùng lặp
- Giữ phiên bản rõ nhất ở vị trí hợp lý nhất, xoá các bản trùng
- SKILL.md chứa pointer, references chứa chi tiết — không ngược lại

## 6. Đo trước, sửa sau

Chấm điểm baseline → sửa → chấm lại → so sánh delta. Không sửa dựa trên cảm tính.

- Dùng quality-checklist (6 tiêu chí, thang 1-5) làm công cụ đo
- Cải tiến phải chứng minh được: điểm tăng hoặc dòng giảm (hoặc cả hai)
- Nếu điểm không tăng → cải tiến đó không hiệu quả, cân nhắc revert

## 7. Ranh giới quyết định phải rõ ràng

Bất kỳ chỗ nào nói "tuỳ trường hợp" / "nếu phù hợp" mà không kèm điều kiện cụ thể → model đoán → output không nhất quán giữa các lần chạy.

- Dùng bảng if/then hoặc decision table
- Nếu skill có 3+ strategies song song → cần trigger rõ cho mỗi strategy
- "Freestyle" / "sáng tạo tự do" là anti-pattern — thay bằng "sáng tạo trong khuôn khổ" (đưa kỹ thuật, để model chọn)

## 8. Ngắn ≠ Tốt, Dài ≠ Xấu

Skill 60 dòng thiếu coverage còn tệ hơn skill 150 dòng đầy đủ. Tiêu chuẩn đúng: **ngắn nhất có thể mà không thiếu sót**.

- Skill <80 dòng → kiểm tra coverage: thiếu edge cases? output format? constraints?
- Skill >300 dòng → kiểm tra bloat: có thể tách references? gộp trùng? cắt dead content?
- Sweet spot: SKILL.md 100-250 dòng, chi tiết ở references

## 9. Degrees of Freedom — Mức tự do phù hợp

Không phải mọi hướng dẫn đều cần cùng mức chi tiết. Chọn mức tự do dựa trên độ nhạy cảm của task:

| Mức | Khi nào | Ví dụ |
|-----|---------|-------|
| **Cao** (văn bản hướng dẫn) | Nhiều cách đều hợp lệ, phụ thuộc ngữ cảnh | Code review, brainstorming |
| **Vừa** (pseudocode/template) | Có pattern ưu tiên nhưng cho phép biến thể | Template báo cáo, output format |
| **Thấp** (script cụ thể) | Nhạy cảm, dễ lỗi, cần nhất quán tuyệt đối | Database migration, API calls |

Phép so sánh: Hãy tưởng tượng Claude đi trên đường — cầu hẹp vực hai bên (tự do thấp) vs. cánh đồng trống (tự do cao). Cung cấp đúng mức hướng dẫn cho từng đoạn đường.

## 10. Skill = Interface, không phải Implementation

Skill nên được thiết kế như **interface** — định nghĩa contract giữa user và AI, không phải triển khai chi tiết từng bước.

- **Description** = "khi nào gọi tôi" (trigger mechanism)
- **SKILL.md** = "tôi cam kết giao gì" (output contract)
- **References/scripts** = "chi tiết kỹ thuật khi cần" (implementation details)

Tư duy này giúp tránh over-specification — thay vì nói Claude cách làm step-by-step, định nghĩa tiêu chí thành công và để Claude phát huy sức mạnh suy luận. Outcome delegation > task execution.
