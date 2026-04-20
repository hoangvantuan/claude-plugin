# Anti-patterns — Những lỗi phổ biến cần tránh

File này liệt kê đầy đủ các lỗi Claude hay mắc khi phân tích văn phong, kèm ví dụ sai → đúng. Đọc kỹ trước khi soạn style guide.

---

## A. Lỗi về bằng chứng

### A1. Suy diễn không trích dẫn

- **Sai**: "Tác giả có xu hướng dùng câu ngắn để tạo nhịp nhanh."
- **Đúng**: "Câu cụt 3-5 từ xuất hiện TB 2-3 lần/bài, dùng để kết đoạn — VD: `'Thế thôi.'` (bài 3), `'Không cãi được.'` (bài 7)."

**Nguyên tắc**: mọi phát biểu về đặc điểm phải có ≥1 trích dẫn nguyên văn kèm theo. Không trích → không phát biểu.

### A2. Paraphrase thành "trích dẫn"

- **Sai**: `"Tác giả nói đại ý là cuộc sống này vô thường và chúng ta phải chấp nhận."`
- **Đúng**: `"Cuộc đời nó thế, không thích cũng phải chịu."` (nguyên văn từ bài 5).

**Nguyên tắc**: trích dẫn trong ngoặc kép phải **COPY y nguyên** từ corpus. Không sửa chính tả, không đổi từ, không rút gọn bằng "...". Tối đa 30 từ; nếu dài hơn, chọn phần đắt nhất.

### A3. Pattern lặp 1 lần → quả quyết thành "signature"

- **Sai**: Bài 2 có 1 câu `"Tôi nghĩ thế."` → ghi vào signature phrases.
- **Đúng**: Cụm phải xuất hiện **≥2 lần qua ≥2 bài khác nhau** mới được đưa vào bảng top 15.

**Nguyên tắc**: một lần là trùng hợp, hai lần là gợi ý, ba lần là pattern. Bảng signature yêu cầu tối thiểu 2 lần.

---

## B. Lỗi về nội dung (content) vs. hình thức (form)

### B1. Tóm tắt nội dung thay vì phân tích cách viết

- **Sai**: "Tác giả viết về cuộc đời, về những suy ngẫm sâu sắc về con người."
- **Đúng**: "Tác giả dùng ngôi 'tôi', câu đơn ngắn (TB 12 từ), mở bài bằng anecdote đời thường, kết bằng reflection."

**Nguyên tắc**: style guide mô tả **CÁCH** viết, không mô tả **CÁI GÌ** được viết. Nếu bạn đang thấy mình viết về chủ đề/thông điệp tác giả — dừng lại, quay về form.

### B2. Lẫn chủ đề vào "signature phrases"

- **Sai** (đưa vào bảng signature): "cuộc đời" (xuất hiện 30 lần).
- **Đúng**: "cuộc đời" là **chủ đề** của tác giả, không phải **chữ ký văn phong**. Signature phrases là cụm cấu trúc/lối nói cá nhân (VD: "kiểu gì cũng", "thế thôi", "ai mà chẳng").

**Nguyên tắc**: signature phrases là cụm **cấu trúc** hoặc **lối nói quirky** đặc trưng cá nhân, không phải danh từ chủ đề. Danh từ chủ đề (tình yêu, công việc, Sài Gòn...) thường chỉ phản ánh content tác giả viết về, không phải cách viết.

---

## C. Lỗi về đánh giá chất lượng

### C1. Dùng virtue words chung chung

- **Sai**: "Tác giả viết rất sâu sắc, lôi cuốn, có chiều sâu."
- **Đúng**: "Tác giả dùng TB 3 ẩn dụ/bài, chủ yếu từ domain tự nhiên (`'như cây rụng lá'`, `'trôi như sông'`), kết hợp câu hỏi tu từ ở giữa bài."

**Nguyên tắc**: mọi mô tả phải **định lượng** hoặc **có bằng chứng cụ thể**. Cấm các từ đánh giá cảm tính không có số liệu backing: "sâu sắc", "lôi cuốn", "cuốn hút", "ấn tượng", "tài hoa", "tinh tế", "đặc sắc".

### C2. Khen/chê tác giả

- **Sai**: "Tác giả viết rất hay, đặc biệt là câu kết."
- **Đúng**: "Pattern kết bài: câu cụt tuyên bố (60% bài) hoặc câu hỏi mở (30% bài)."

**Nguyên tắc**: không đánh giá hay/dở. Bạn là nhà phân tích khách quan, không phải critic. Mô tả — không phán xét.

---

## D. Lỗi về so sánh

### D1. So sánh với tác giả khác tự phát

- **Sai**: "Tác giả này viết giống Nguyễn Ngọc Tư nhưng ít ẩn dụ hơn."
- **Đúng**: chỉ phân tích tác giả được đưa vào corpus. Không so sánh trừ khi user yêu cầu rõ.

### D2. So sánh với "phong cách nói chung" mơ hồ

- **Sai**: "Tác giả ít formal hơn văn phong báo chí trung bình."
- **Đúng**: "Mức formal: 2/5 — dùng tiếng lóng (`'vãi'`, `'éo'` — bài 4), câu rút gọn thiếu chủ ngữ."

---

## E. Lỗi về cỡ mẫu và độ tin cậy

### E1. Phát biểu chắc nịch với corpus nhỏ

- **Sai (với 2 bài)**: "Tác giả LUÔN mở bài bằng anecdote."
- **Đúng**: "Cả 2 bài trong corpus đều mở bằng anecdote (`'...'`, `'...'`). Cần thêm bài để xác nhận đây là pattern cố định."

**Nguyên tắc**: cỡ mẫu nhỏ → hedging mạnh. Viết "trong corpus hiện tại" thay vì "tác giả luôn/không bao giờ".

### E2. Bỏ qua ghi chú độ tin cậy

- **Sai**: output metadata không có dòng "Độ tin cậy".
- **Đúng**: luôn điền độ tin cậy (Rất thấp / Trung bình / Khá / Cao) dựa trên bảng trong SKILL.md.

---

## F. Lỗi về template

### F1. Bỏ chiều không đủ data

- **Sai**: bỏ luôn mục "7. Tư duy & logic" vì không đủ data.
- **Đúng**: giữ heading, ghi nội dung: `> Không đủ dữ liệu để kết luận (cần corpus dài hơn).`

### F2. "Công thức tái tạo" chung chung

- **Sai**: "Viết giống tác giả, phong cách suồng sã, có ẩn dụ."
- **Đúng**:
  1. "Mở bài bằng 1 câu cụt ≤5 từ (VD dạng `'Nó xong rồi.'`)."
  2. "Đoạn 2 kể 1 anecdote đời thường 3-4 câu, ngôi `'tôi'`."
  3. "Chèn ít nhất 1 ẩn dụ từ domain thể thao giữa thân bài."
  4. ...

**Nguyên tắc**: mỗi bước phải có **yếu tố định lượng** (số từ/câu) hoặc **thao tác cụ thể** (loại nào, ở đâu). Test: đưa công thức cho một AI khác → nó có viết ra được bài đúng style không? Nếu không → công thức chưa đủ cụ thể.

### F3. Anti-patterns không có bằng chứng

- **Sai (trong mục Anti-patterns)**: "Không dùng từ sáo rỗng."
- **Đúng**: "Không dùng emoji (0 instance trong 10 bài corpus)." / "Không viết đoạn >5 câu (đoạn dài nhất: 4 câu, bài 2)."

**Nguyên tắc**: Anti-pattern = điều tác giả **không bao giờ làm trong corpus**, có bằng chứng đếm được.

---

## G. Lỗi về workflow

### G1. Bỏ qua self-check

- Sau khi draft style guide, **dừng lại 30 giây**, đọc từ đầu, check 5 câu hỏi trong SKILL.md.
- Nếu fail → sửa TRƯỚC khi ghi file. Không ghi file rồi hứa "sẽ sửa".

### G2. Không hỏi tên tác giả

- Thiếu tên → output file sẽ là `style-guides/tac-gia-x.md` — xấu và khó tra cứu.
- Luôn hỏi tên tác giả ngay khi bắt đầu, hoặc infer từ context nếu rõ ràng (VD user nói "phân tích cách viết của Haruki Murakami").

### G3. Không cảnh báo khi corpus quá nhỏ

- Corpus <3 bài → cảnh báo user trước khi phân tích. User có thể muốn bổ sung thêm trước.

---

## H. Checklist cuối cùng trước khi ghi file

Trước khi gọi `Write`, đi qua checklist này:

- [ ] Mỗi đặc điểm có trích dẫn nguyên văn trong ngoặc kép?
- [ ] Mỗi trích dẫn ≤30 từ, có ghi nguồn `(bài: X)`?
- [ ] Đủ 8 chiều (hoặc đánh dấu "không đủ dữ liệu" rõ ràng)?
- [ ] Signature phrases: mọi cụm ≥2 lần ở ≥2 bài?
- [ ] Công thức tái tạo: mỗi bước có định lượng hoặc thao tác cụ thể?
- [ ] Anti-patterns: mỗi điều có bằng chứng đếm được?
- [ ] Metadata đầu file: đủ 4 dòng (số bài / nguồn / ngày / độ tin cậy)?
- [ ] Tóm tắt 1 dòng ≤25 từ?
- [ ] Không có virtue word chung chung không định lượng?
- [ ] Không tóm tắt nội dung bài?
- [ ] Không so sánh với tác giả khác?
- [ ] Không đánh giá hay/dở?

Fail bất kỳ ô nào → sửa trước khi ghi file.
