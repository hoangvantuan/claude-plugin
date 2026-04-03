---
name: deep-insight
description: >
  Quan sát đa chiều → Phân tích tách lớp → Đúc kết cốt lõi để hiểu sâu bất kỳ vấn đề nào.
  Sử dụng khi user muốn nghiên cứu sâu một chủ đề, phân tích tài liệu, tìm bản chất vấn đề,
  hoặc đúc kết kiến thức từ nhiều nguồn. Trigger khi user nói: "phân tích sâu", "tìm hiểu sâu",
  "đúc kết", "tách lớp", "tìm cốt lõi", "quan sát phân tích", "hiểu bản chất", "deep insight",
  "nghiên cứu vấn đề", hoặc khi cần hiểu thấu đáo một chủ đề phức tạp trước khi hành động.
  Ưu tiên skill này khi user cung cấp tài liệu/chủ đề và muốn output dạng phân tích sâu,
  không chỉ tóm tắt. Cũng nên dùng khi user đề cập "quan sát - phân tích - đúc kết",
  "nhân quả", "tìm lõi", hoặc bất kỳ yêu cầu nào đòi hỏi tư duy sâu hơn mức tóm tắt thông thường.
---

# Deep Insight — Quan sát · Phân tích · Đúc kết

Skill giúp hiểu sâu bất kỳ vấn đề nào thông qua chu trình **ba bước tư duy**:

| Bước          | Bản chất                   | Mục tiêu                  |
| ------------- | -------------------------- | ------------------------- |
| **Quan sát**  | Thu thập đa chiều          | Thấy đủ — không bỏ sót    |
| **Phân tích** | Tách lớp, tìm liên kết     | Thấy rõ — cơ chế vận hành |
| **Đúc kết**   | Rút cốt lõi, nguyên lý hóa | Thấy sâu — nắm bản chất   |

Ba bước này là **chu trình lặp**, không tuyến tính. Mỗi vòng lặp đi sâu hơn vòng trước.

> **Nguyên tắc vàng**: Đúc kết không phải tóm tắt. Tóm tắt là rút gọn thông tin. Đúc kết là tìm ra **cái lõi chi phối tất cả những cái khác** — thứ mà khi nắm được, mọi thứ còn lại tự sáng tỏ.

**Failure modes cần tránh:**
- **Tóm tắt giả đúc kết** — Liệt kê ý chính rồi gọi là "cốt lõi". Nếu bỏ 1 ý mà hệ thống không sụp → chưa tìm được lõi.
- **Phân tích thiếu dữ liệu** — Vào phân tích khi chưa quan sát đủ rộng → kết luận phiến diện.
- **Sơ đồ mục lục** — Mind map chỉ liệt kê, không thể hiện nhân quả hay tương tác → không giúp hiểu vận hành.
- **Đúc kết bị động** — Đọc nhiều rồi chờ "ngộ" thay vì chủ động hỏi "cái gì chi phối tất cả?"
- **Thiếu hành động** — Hiểu sâu mà không biết phải làm gì tiếp = chưa đúc kết xong.

## Khi nào đọc references

- Cần hiểu nền tảng triết học (ba gốc, nhân-duyên-quả): đọc `references/framework-foundation.md`
- Cần kỹ thuật quan sát đa chiều chi tiết: đọc `references/observation-guide.md`
- Cần patterns phân tích (tách lớp, nhân quả, tương tác): đọc `references/analysis-patterns.md`
- Cần phương pháp đúc kết & sơ đồ hóa: đọc `references/synthesis-methods.md`
- Cần template output: đọc `references/output-template.md`

## Quy trình thực hiện

### Bước 0: Xác định đầu vào

Cần 3 thông tin. **Chỉ hỏi những gì user chưa cung cấp**, gộp 1 lần hỏi:

1. **Chủ đề / vấn đề cần hiểu sâu là gì?**
2. **Tài liệu đầu vào?** — files, URLs, hoặc kiến thức user đã có
3. **Mục đích hiểu sâu để làm gì?** — ra quyết định, dạy người khác, viết bài, giải quyết vấn đề...

Nếu user đã cung cấp đủ → bỏ qua, vào thẳng Bước 1.

**Khi user không có tài liệu** (chỉ đưa chủ đề): Dùng research (WebSearch, deep-research) làm nguồn chính. Quan sát đa chiều dựa trên kết quả research thay vì documents.

### Bước 1: QUAN SÁT — Thu thập đa chiều

Mục tiêu: **Thấy đủ** — nhìn vấn đề từ nhiều góc, không bỏ sót chiều quan trọng.

**1.1. Đọc & tiêu hóa tài liệu đầu vào**

- Đọc toàn bộ tài liệu user cung cấp
- Ghi nhận: ý chính, thuật ngữ, mâu thuẫn, khoảng trống thông tin

**1.2. Quan sát đa chiều** — Nhìn vấn đề từ ≥5 góc:

| Chiều quan sát          | Câu hỏi dẫn đường                                        |
| ----------------------- | -------------------------------------------------------- |
| **Từ trên** (tổng quan) | Vấn đề này nằm trong hệ thống lớn nào?                   |
| **Từ dưới** (nền tảng)  | Cái gì làm nền, làm gốc cho vấn đề này?                  |
| **Từ trong** (cơ chế)   | Bên trong nó vận hành như thế nào?                       |
| **Từ ngoài** (bối cảnh) | Môi trường, điều kiện xung quanh ảnh hưởng ra sao?       |
| **Theo thời gian**      | Nó thay đổi thế nào theo thời gian? Nhân quả gần vs. xa? |
| **Liên đới**            | Những vấn đề tương tự vận hành cùng nguyên lý không?     |

**1.3. Research bổ sung** (nếu cần)

- Khi phát hiện khoảng trống thông tin → research thêm từ nguồn uy tín
- Có thể sử dụng skill `deep-research` nếu cần nghiên cứu chuyên sâu
- Có thể dùng `WebSearch` / `WebFetch` cho tra cứu nhanh
- Ưu tiên: sách, nghiên cứu học thuật, chuyên gia uy tín trong lĩnh vực

**Output Bước 1:** Bản ghi quan sát — liệt kê các phát hiện theo từng chiều, đánh dấu mâu thuẫn và khoảng trống.

### Bước 2: PHÂN TÍCH — Tách lớp, tìm liên kết

Mục tiêu: **Thấy rõ** — hiểu cơ chế vận hành, mối quan hệ nhân quả.

**2.1. Tách lớp** — 4 tầng: Hiện tượng → Cơ chế → Nguyên nhân → Gốc rễ. Chi tiết & ví dụ: đọc `references/analysis-patterns.md` mục "Tách lớp".

**2.2. Phân tích nhân quả** — Theo chuỗi Nhân + Duyên = Quả. Luôn phân biệt **nhân quả gần** vs. **nhân quả xa**. Chi tiết: đọc `references/analysis-patterns.md` mục "Phân tích Nhân quả" và `references/framework-foundation.md` mục "Nhân - Duyên - Quả".

**2.3. Phân tích tương tác** — Các thành phần ảnh hưởng lẫn nhau thế nào:

- Vẽ sơ đồ tương tác (dùng Mermaid nếu phù hợp)
- Tìm feedback loops (vòng lặp tự tăng cường hoặc tự triệt tiêu)
- Nhận diện điểm leverage (can thiệp ít nhưng ảnh hưởng lớn)

**2.4. Quan sát liên đới** — So sánh với vấn đề tương tự:

- Lĩnh vực khác có vấn đề tương tự không?
- Cùng nguyên lý hay khác?
- Rút ra pattern chung

**Output Bước 2:** Bản phân tích — sơ đồ tách lớp, chuỗi nhân quả, sơ đồ tương tác.

### Bước 3: ĐÚC KẾT — Rút cốt lõi, nguyên lý hóa

Mục tiêu: **Thấy sâu** — nắm bản chất, biến thành nguyên lý có thể truyền đạt.

Đây là bước **khó nhất** — đòi hỏi **tác ý** (chủ động đặt câu hỏi), không thể làm bị động.

**3.1. Tìm LÕI** — Trả lời câu hỏi trung tâm:

> "Trong tất cả những gì đã quan sát và phân tích, **cái gì chi phối những cái khác**?"

Chi tiết 3 phương pháp tìm lõi ("Bỏ đi thử", "Giao nhau", "Câu hỏi đệ quy"): đọc `references/synthesis-methods.md`.

**3.2. Nguyên lý hóa** — Biến insight thành 1-3 câu ngắn gọn, tổng quát, kiểm chứng được, hành động được. Test bằng 3 câu hỏi kiểm tra nhân quả (đọc `references/framework-foundation.md` mục "Ba câu hỏi kiểm tra nhân quả").

**3.3. Sơ đồ hóa** — Sơ đồ phải thể hiện **sự vận hành** (cái gì dẫn đến cái gì), không chỉ liệt kê. Dùng Mermaid flowchart/mindmap. Chi tiết: đọc `references/synthesis-methods.md` mục "Sơ đồ hóa".

**3.4. Kiểm tra chất lượng đúc kết** — 5 tiêu chí (chi tiết: `references/synthesis-methods.md` mục "Kiểm tra chất lượng"):

- **Cốt lõi**: Đã tìm được cái chi phối tất cả?
- **Giải thích lực**: Nguyên lý giải thích được bao nhiêu hiện tượng? (1-5)
- **Dự đoán lực**: Dự đoán được điều mới? (1-5)
- **Truyền đạt**: Người khác hiểu trong 2 phút? (1-5)
- **Hành động**: Biết phải làm gì tiếp?

**Tiêu chí dừng**: Nếu Cốt lõi = Có, Hành động = Có, và trung bình Giải thích + Dự đoán + Truyền đạt ≥ 3/5 → đúc kết đạt. Nếu chưa → quay lại Bước 1 hoặc 2 bổ sung, tối đa 2 vòng lặp.

## Format output

Dùng template mặc định từ `references/output-template.md`. Tuỳ mục đích user có thể điều chỉnh cấu trúc, nhưng giữ nguyên 3 phần chính: Quan sát → Phân tích → Đúc kết.

## Lưu report

Sau khi hoàn thành, lưu output vào:

```
{CWD}/deep-insight/{topic-slug}-{YYMMDD}.md
```

Tạo thư mục `{CWD}/deep-insight/` nếu chưa tồn tại. Thông báo đường dẫn file cho user.

## Lưu ý quan trọng

1. **Quan sát phải đủ rộng trước khi phân tích** — Phân tích sớm trên dữ liệu thiếu → kết luận sai. Nếu thiếu thông tin, research thêm trước.
2. **Sơ đồ phải thể hiện vận hành** — Mũi tên = "dẫn đến", "tạo ra". Mind map chỉ liệt kê → không đủ.
3. **Ngôn ngữ output** — Viết bằng tiếng Việt có dấu đầy đủ, trừ khi user yêu cầu khác. Thuật ngữ chuyên ngành giữ tiếng Anh nếu phổ biến hơn.
