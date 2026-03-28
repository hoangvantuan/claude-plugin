# Patterns Phân tích

## 1. Tách lớp (Layer Decomposition)

### Nguyên lý

Mọi vấn đề đều có nhiều lớp. Lớp ngoài = hiện tượng dễ thấy. Lớp trong = cơ chế ẩn.

### 4 lớp chuẩn

```
Hiện tượng (Surface)     ← Cái thấy được
    ↓
Cơ chế (Mechanism)       ← Cái vận hành
    ↓
Nguyên nhân (Cause)      ← Cái sinh ra cơ chế
    ↓
Gốc rễ (Root)            ← Cái chi phối tất cả
```

### Cách tách lớp thực tế

1. Bắt đầu từ **hiện tượng** — cái dễ thấy nhất
2. Hỏi **"Tại sao?"** → lộ ra cơ chế
3. Hỏi tiếp **"Tại sao cơ chế này tồn tại?"** → lộ ra nguyên nhân
4. Hỏi tiếp **"Cái gì tạo ra nguyên nhân đó?"** → chạm gốc rễ

### Ví dụ: Giáo dục

| Lớp | Nội dung |
|-----|----------|
| Hiện tượng | Học sinh chán học, điểm thấp |
| Cơ chế | Phương pháp dạy nhồi nhét, thi cử áp lực |
| Nguyên nhân | Hệ thống đánh giá chỉ dựa vào điểm số |
| Gốc rễ | Triết lý giáo dục coi trọng kiến thức hơn phát triển con người |

### Ví dụ: Y tế

| Lớp | Nội dung |
|-----|----------|
| Hiện tượng | Bệnh nhân ngày càng đông |
| Cơ chế | Lối sống không lành mạnh phổ biến |
| Nguyên nhân | Ngành y tập trung chữa bệnh thay vì phòng ngừa |
| Gốc rễ | Mô hình kinh tế y tế = càng nhiều bệnh nhân càng có lợi nhuận |

## 2. Phân tích Nhân quả

### Công thức: Nhân + Duyên = Quả

Không chỉ tìm nguyên nhân — phải tìm cả **điều kiện** (duyên) mới hiểu đầy đủ.

### Kỹ thuật chuỗi nhân quả

```
Nhân 1 + Duyên A → Quả 1
Quả 1 + Duyên B → Quả 2 (Quả 1 trở thành Nhân cho Quả 2)
Quả 2 + Duyên C → Quả 3
...
```

### Phân biệt nhân quả gần vs. xa

Khi phân tích, LUÔN xét cả hai:

**Nhân quả gần:**
- Hiệu ứng trực tiếp, dễ thấy
- Thường là lý do mọi người hành động

**Nhân quả xa:**
- Hiệu ứng tích lũy, khó thấy
- Thường là lý do thực sự nên/không nên hành động
- Kiểm tra bằng câu hỏi: "Nếu nhân bản & duy trì lâu dài?"

## 3. Phân tích Tương tác

### Mục đích

Hiểu các thành phần **ảnh hưởng lẫn nhau** thế nào — không phải chỉ liệt kê chúng.

### Kỹ thuật

**Sơ đồ tương tác:**
- Vẽ các thành phần chính
- Vẽ mũi tên chỉ hướng tác động
- Ghi chú: tác động tích cực (+) hay tiêu cực (-)

**Tìm feedback loops:**
- **Vòng tăng cường** (reinforcing): A→B→C→A (càng lúc càng mạnh)
  - Ví dụ: Tự tin → Dám thử → Thành công → Tự tin hơn
- **Vòng triệt tiêu** (balancing): A→B→C→~A (tự điều chỉnh)
  - Ví dụ: Nóng → Bật quạt → Mát → Tắt quạt → Nóng lại

**Tìm điểm leverage:**
- Điểm mà can thiệp nhỏ → ảnh hưởng lớn toàn hệ thống
- Thường nằm ở nơi nhiều mũi tên hội tụ hoặc phân tán

## 4. Quan sát liên đới (Cross-domain Analysis)

### Nguyên lý

Nhiều vấn đề tưởng khác nhau nhưng **vận hành cùng nguyên lý**. Nhận ra pattern chung = hiểu sâu hơn.

### Cách thực hiện

1. Xác định **đặc điểm cốt lõi** của vấn đề đang phân tích
2. Tìm **vấn đề tương tự** ở lĩnh vực khác có cùng đặc điểm
3. So sánh: cùng nguyên lý hay khác?
4. Nếu cùng → đúc kết pattern chung

### Ví dụ

Động cơ xe máy ↔ Động cơ ô tô ↔ Động cơ máy bay:
- Cùng nguyên lý: chuyển hóa năng lượng → chuyển động
- Khác: quy mô, nhiên liệu, cơ chế cụ thể
- Pattern chung: **Mọi hệ thống vận động đều cần nguồn chuyển hóa năng lượng**

## 5. Logic & Phản biện

### Phản biện = Lật ngược nhìn

- Phản biện KHÔNG phải cãi lại
- Phản biện = **nhìn từ góc đối diện** để kiểm tra kết luận

### Kỹ thuật phản biện

1. **Lật ngược giả định**: "Nếu điều ngược lại đúng thì sao?"
2. **Tìm phản ví dụ**: "Có trường hợp nào kết luận này sai không?"
3. **Thay đổi duyên**: "Nếu điều kiện khác, kết quả có thay đổi?"
4. **Nhân quả xa**: "Nếu nhân bản lâu dài, hậu quả là gì?"

### Lưu ý

Phải **thấy logic trước** mới phản biện được. Nếu chưa hiểu vấn đề → không nên vội phản biện.
