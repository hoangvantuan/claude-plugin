# Phương pháp Đúc kết

## Tại sao đúc kết khó nhất?

Quan sát = thu thập (passive). Phân tích = chia nhỏ (systematic). Đúc kết = **tác ý** (intentional) — phải chủ động đặt câu hỏi: "Cốt lõi là cái gì?"

Không ai đúc kết được bằng cách bị động đọc thật nhiều rồi tự nhiên "ngộ ra". Phải **chủ động tìm kiếm** cái lõi.

## Kỹ thuật tìm Lõi

### Phương pháp "Bỏ đi thử"

1. Liệt kê tất cả thành phần/yếu tố của vấn đề
2. Thử bỏ từng cái: bỏ cái này đi, hệ thống có sụp không?
3. Cái nào bỏ đi mà hệ thống sụp = **lõi**
4. Kiểm tra ngược: từ lõi có thể phát sinh những cái khác không?

### Phương pháp "Giao nhau"

1. Quan sát **nhiều hiện tượng tương tự** (≥3)
2. Tìm **điểm chung** xuất hiện ở tất cả
3. Điểm chung đó = ứng viên cho lõi
4. Kiểm tra: Bỏ điểm chung đi, các hiện tượng có còn tồn tại?

### Phương pháp "Câu hỏi đệ quy"

1. "Cái quan trọng nhất là gì?" → Trả lời A
2. "Tại sao A quan trọng?" → Vì B
3. "Tại sao B quan trọng?" → Vì C
4. Lặp cho đến khi không thể hỏi tiếp → C là lõi

## Nguyên lý hóa

### Từ insight → Nguyên lý

Sau khi tìm được lõi, cần **diễn đạt** thành nguyên lý:

**Tiêu chí nguyên lý tốt:**
- **Ngắn gọn**: 1-2 câu, ai cũng nhớ được
- **Tổng quát**: Đúng với hầu hết trường hợp, không chỉ 1 ví dụ
- **Kiểm chứng được**: Có thể test bằng ví dụ mới
- **Hành động được**: Biết nguyên lý → biết phải làm gì

**Ví dụ nguyên lý hóa:**
- Quan sát: xe máy, ô tô, máy bay đều cần động cơ
- Nguyên lý: "Mọi phương tiện di chuyển đều cần nguồn chuyển hóa năng lượng thành chuyển động"
- Test: Xe đạp? → Nguồn = sức người. Đúng!

## Sơ đồ hóa

### Tại sao sơ đồ quan trọng?

- Sơ đồ thể hiện **sự vận hành** — không chỉ liệt kê
- Mind map chỉ là mục lục đẹp — không cho thấy nhân quả, tương tác
- Sơ đồ tốt = người khác nhìn vào **hiểu cơ chế trong vài giây**

### Loại sơ đồ phù hợp cho từng mục đích

| Mục đích | Loại sơ đồ | Mermaid type |
|----------|------------|--------------|
| Chuỗi nhân quả | Flowchart | `flowchart TD` |
| Cấu trúc phân tầng | Tree/Mindmap | `mindmap` |
| Tương tác hai chiều | Flowchart + bidirectional | `flowchart LR` |
| Feedback loop | Flowchart vòng tròn | `flowchart TD` |
| Tiến trình theo thời gian | Timeline | `timeline` |
| So sánh | Table | Markdown table |

### Nguyên tắc sơ đồ

1. **Thể hiện vận hành**: Mũi tên = "dẫn đến", "tạo ra", "ảnh hưởng"
2. **Tối giản**: Chỉ giữ yếu tố cốt lõi, bỏ chi tiết phụ
3. **Có hướng**: Đọc từ trên xuống hoặc trái sang phải
4. **Đánh dấu lõi**: Highlight yếu tố cốt lõi (bold, màu khác)

## 4 cấp độ chất lượng đúc kết

| Cấp | Mô tả | Tiêu chí |
|-----|--------|----------|
| **1 — Đủ ý** | Đầy đủ nội dung, không thiếu sót | Liệt kê đúng, đủ |
| **2 — Có sơ đồ** | Sơ đồ hóa, bổ sung minh họa | Có hình, có bảng, dễ nhìn |
| **3 — Tối ưu** | Làm đi làm lại, cải thiện liên tục | Ngắn gọn hơn, rõ ràng hơn |
| **4 — Dạy được** | Truyền đạt cho người khác vỡ ra ngay | Ai đọc cũng hiểu, không cần giải thích thêm |

Mục tiêu tối thiểu: **Cấp 2**. Mục tiêu lý tưởng: **Cấp 4**.

## Kiểm tra chất lượng đúc kết

5 tiêu chí đánh giá:

| # | Tiêu chí | Câu hỏi | Thang |
|---|----------|---------|-------|
| 1 | **Cốt lõi** | Đã tìm được cái chi phối tất cả? | Có/Không |
| 2 | **Giải thích lực** | Nguyên lý giải thích được bao nhiêu % hiện tượng? | 1-5 |
| 3 | **Dự đoán lực** | Dùng nguyên lý dự đoán được điều mới? | 1-5 |
| 4 | **Truyền đạt** | Người khác đọc hiểu trong 2 phút? | 1-5 |
| 5 | **Hành động** | Biết phải làm gì tiếp từ đúc kết? | Có/Không |

Nếu tiêu chí 1 hoặc 5 = "Không" → Quay lại phân tích, chưa đúc kết xong.
