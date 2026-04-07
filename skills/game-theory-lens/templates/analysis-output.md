# [Chủ đề] — Phân tích qua Lý thuyết Trò chơi

> Ngày phân tích: [YYYY-MM-DD]

## Tổng quan tình huống

[Mô tả ngắn gọn tình huống, bối cảnh, và lý do cần phân tích. 3-5 câu.]

**Các bên tham gia (Players):**
- Player 1: [Tên] — [Mục tiêu/lợi ích chính]
- Player 2: [Tên] — [Mục tiêu/lợi ích chính]
- [Thêm nếu có]

**Mục đích phân tích:** [hiểu bản chất / ra quyết định / tư vấn chiến lược / dự đoán kết quả]

---

## 1. Nhận diện Trò chơi

### Game Archetype

Tình huống này gần nhất với: **[Tên trò chơi mẫu]** (ví dụ: Prisoner's Dilemma, Chicken, Stag Hunt...)

**Vì sao:** [Giải thích ngắn vì sao map sang archetype này]

### Bảng Payoff (Payoff Matrix)

[Bảng 2x2 hoặc lớn hơn, với giá trị ước lượng]

|  | Player 2: Chiến lược A | Player 2: Chiến lược B |
|---|---|---|
| **Player 1: Chiến lược A** | (payoff1, payoff2) | (payoff1, payoff2) |
| **Player 1: Chiến lược B** | (payoff1, payoff2) | (payoff1, payoff2) |

*Ghi chú: Giá trị payoff ước lượng dựa trên [cơ sở nào].*

### Game Tree (nếu là trò chơi tuần tự)

```mermaid
[Game tree flowchart nếu áp dụng]
```

---

## 2. Phân tích Cấu trúc Chiến lược

### Chiến lược trội (Dominant Strategy)
[Có/không? Giải thích]

### Nash Equilibrium
- **Equilibrium dự đoán:** [Mô tả tổ hợp chiến lược]
- **Ý nghĩa:** [Kết quả này nghĩa là gì cho các bên?]
- **Hiệu quả Pareto:** [Kết quả có hiệu quả không? Có tổ hợp nào tốt hơn cho cả hai?]

### Yếu tố thông tin
- **Ai biết gì:** [Mô tả phân bổ thông tin]
- **Signaling:** [Tín hiệu nào đang được gửi? Đáng tin không?]
- **Thông tin bất đối xứng:** [Ảnh hưởng thế nào đến chiến lược?]

---

## 3. Phân tích Động lực

### Tính chất thời gian
- **Loại trò chơi:** [Một lần / Lặp lại hữu hạn / Lặp lại vô hạn]
- **Hệ quả:** [Ảnh hưởng thế nào đến khả năng hợp tác?]

### Tiến hoá chiến lược
[Theo thời gian, chiến lược nào có xu hướng lan rộng? Chiến lược nào bị đào thải?]

### Thiết kế cơ chế (nếu có thể thay đổi luật chơi)
[Gợi ý cách thay đổi incentive/luật chơi để đạt kết quả tốt hơn]

---

## 4. Đàm phán & Liên minh

*(Bỏ qua nếu không áp dụng)*

### Vị thế đàm phán
| Player | BATNA | Mức kiên nhẫn | Sợ rủi ro | Vị thế |
|---|---|---|---|---|
| [Tên] | [Phương án B] | [Cao/Thấp] | [Cao/Thấp] | [Mạnh/Yếu] |

### Dự đoán kết quả đàm phán
[Nash bargaining solution dự đoán phân chia như thế nào?]

### Liên minh (3+ players)
[Liên minh nào khả thi? Liên minh nào ổn định?]

---

## 5. Đúc kết

### Insight chính

1. **[Insight 1]** — Vì sao: [reasoning]. Nghĩa là: [implication].
2. **[Insight 2]** — Vì sao: [reasoning]. Nghĩa là: [implication].
3. **[Insight 3]** — Vì sao: [reasoning]. Nghĩa là: [implication].

### Cảnh báo ngụy biện

[Liệt kê ngụy biện cần tránh khi suy nghĩ về tình huống này]

### Khuyến nghị chiến lược

**Cho [Player 1]:**
- [Khuyến nghị cụ thể + lý do]

**Cho [Player 2]:**
- [Khuyến nghị cụ thể + lý do]

**Cho người thiết kế luật chơi (nếu áp dụng):**
- [Đề xuất thay đổi cơ chế]

### Sơ đồ tổng hợp

```mermaid
[Flowchart hoặc mindmap tổng hợp logic chiến lược]
```

---

*Phân tích dựa trên framework Game Theory Lens, tham khảo lý thuyết của Ken Binmore, John Nash, và John von Neumann.*
