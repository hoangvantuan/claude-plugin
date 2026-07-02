# Patterns phân tích giao tiếp trong cuộc họp

## 1. Né tránh xung đột (Conflict Avoidance)

### Dấu hiệu cần tìm

- **Hedging language**: "có lẽ", "có thể", "hình như", "maybe", "kind of", "I think", "sort of"
- **Gián tiếp thay vì trực tiếp**: hỏi vòng vo thay vì nêu thẳng vấn đề
- **Đổi chủ đề khi căng thẳng**: chuyển sang topic khác khi bắt đầu có bất đồng
- **Đồng ý nửa vời**: "ừ, nhưng...", "cũng được", "yeah, but..."
- **Không đề cập vấn đề rõ ràng**: bỏ qua elephant in the room

### Ví dụ phân tích

```
**Tìm thấy**: Hedging khi cần đưa feedback quan trọng

**Transcript** (00:14:32):
> "Em nghĩ là... có lẽ mình nên xem lại timeline một chút? 
> Ý em là nếu anh thấy hợp lý thì mình thử, còn không 
> thì cũng được ạ."

**Vấn đề**: Dự án trễ 2 tuần, nhưng hedging language ("có lẽ", 
"nếu anh thấy hợp lý", "cũng được") khiến người nghe dễ bỏ qua 
mức độ nghiêm trọng.

**Cách tốt hơn**: 
"Dự án đang trễ 2 tuần so với kế hoạch. Em cần thảo luận 
với anh về nguyên nhân và điều chỉnh timeline hôm nay."
```

## 2. Tỉ lệ nói/nghe (Speaking Ratio)

### Metrics cần tính

- **% thời gian nói** so với tổng thời gian cuộc họp
- **Số lần ngắt lời** (bị ngắt và ngắt người khác)
- **Độ dài trung bình mỗi lượt nói**
- **Tỉ lệ câu hỏi vs. câu khẳng định**

### Cách tính

- Đếm số dòng/từ của mỗi speaker trong transcript
- Tính % theo từng người
- So sánh với benchmark: facilitator nên nói ~30-40%, để 60-70% cho team

### Benchmark tham khảo

| Vai trò                    | % nói khuyến nghị     |
| -------------------------- | --------------------- |
| Facilitator/PM             | 30-40%                |
| Presenter (phần trình bày) | 60-80%                |
| Participant bình thường    | chia đều phần còn lại |
| 1:1 meeting                | 40-60% mỗi người      |


## 3. Filler Words và Hedging Language

### Từ cần đếm

**Tiếng Việt**: "ờ", "à", "ừm", "kiểu", "kiểu như", "cơ bản là", "nói chung là", "thực ra", "đại loại"

**Tiếng Anh**: "um", "uh", "like", "you know", "actually", "basically", "literally", "I mean", "sort of", "kind of"

### Cách báo cáo

- Tần suất: X lần / phút hoặc X lần / lượt nói
- Ngữ cảnh tăng: khi nào filler words xuất hiện nhiều hơn (nervous, uncertain, bị hỏi bất ngờ)
- So sánh giữa các cuộc họp nếu có nhiều transcript

## 4. Kỹ năng lắng nghe chủ động (Active Listening)

### Dấu hiệu tích cực

- **Câu hỏi tham chiếu**: đặt câu hỏi liên quan đến ý kiến người trước ("Anh vừa nói X, vậy có nghĩa là...")
- **Paraphrase**: diễn đạt lại ý người khác để xác nhận hiểu đúng
- **Build on**: phát triển thêm từ ý kiến của người khác
- **Clarifying questions**: hỏi làm rõ thay vì giả định

### Dấu hiệu thiếu lắng nghe

- Lặp lại ý đã được nói mà không nhận ra
- Chuyển topic mà không acknowledge ý kiến trước
- Trả lời không liên quan đến câu hỏi
- Ngắt lời giữa chừng

## 5. Phong cách điều hành (Facilitation)

### Khía cạnh đánh giá

- **Quản lý thời gian**: có bám agenda không, có để topic kéo dài quá lâu không
- **Xử lý bất đồng**: directive (quyết nhanh) vs. collaborative (để team thảo luận)
- **Inclusive**: có kéo người ít nói vào không, có để 1 người dominate không
- **Action items**: có chốt rõ ràng ai làm gì khi nào không
- **Decision-making**: rõ ràng hay mơ hồ, có ghi nhận phản đối không

### Benchmark facilitation tốt

- Mở đầu: nêu mục tiêu và agenda trong 2 phút đầu
- Giữa: giữ thảo luận đúng topic, chuyển mục đúng thời gian
- Cuối: tóm tắt quyết định, chốt action items, hẹn follow-up
- Xuyên suốt: hỏi ý kiến người chưa phát biểu

## Cấu trúc báo cáo output

```markdown
# Phân tích giao tiếp trong cuộc họp

**Phạm vi phân tích**: [khoảng thời gian]
**Số cuộc họp**: [X cuộc]
**Tổng thời lượng**: [X giờ]
**Đối tượng phân tích**: [tên người]

## Tổng quan

[2-3 câu tóm tắt: nhận xét tổng thể về phong cách giao tiếp]

## Điểm mạnh

1. **[Điểm mạnh 1]**
   - Bằng chứng: [trích dẫn + cuộc họp + timestamp]
   - Tác động: [tại sao đây là điểm mạnh]

2. **[Điểm mạnh 2]**
   [cùng format]

3. **[Điểm mạnh 3]**
   [cùng format]

## Cơ hội cải thiện

1. **[Pattern 1]**
   - Tần suất: [X lần trong Y cuộc họp]
   - Ví dụ tiêu biểu:
     - **[Tên cuộc họp]** ([timestamp]):
       > [Trích dẫn nguyên văn]
     - Vấn đề: [giải thích tại sao cần cải thiện]
     - Cách tốt hơn: [đề xuất cụ thể, có thể kèm câu mẫu]
   
2. **[Pattern 2]**
   [cùng format]

## Thống kê giao tiếp

| Metric | Giá trị | Benchmark |
|--------|---------|-----------|
| % thời gian nói | X% | 30-40% (facilitator) |
| Câu hỏi / cuộc họp | X | - |
| Filler words / phút | X | - |
| Ngắt lời (gây ra) | X / cuộc | - |
| Ngắt lời (bị) | X / cuộc | - |

## Xu hướng theo thời gian

[Chỉ hiển thị khi phân tích nhiều cuộc họp]
- [Metric A]: tăng/giảm từ X → Y
- [Metric B]: ổn định ở mức X

## Hành động cụ thể

1. [Hành động 1]: mô tả ngắn, áp dụng ngay từ cuộc họp tiếp
2. [Hành động 2]: mô tả ngắn
3. [Hành động 3]: mô tả ngắn
```
