# Thiết kế cơ chế (Mechanism Design)

## Khái niệm cốt lõi

Thiết kế cơ chế (Mechanism Design) là **lý thuyết trò chơi ngược** — thay vì phân tích trò chơi đã có, ta **thiết kế luật chơi** sao cho kết quả mong muốn chính là trạng thái cân bằng.

> Câu hỏi trung tâm: "Tôi muốn kết quả X. Tôi cần thiết kế luật chơi nào để mọi người tự nguyện hành động dẫn đến X?"

### Các thuật ngữ nền tảng

| Thuật ngữ | Định nghĩa | Ví dụ |
|---|---|---|
| Cơ chế (Mechanism) | Bộ luật chơi: ai được nói gì, kết quả tính thế nào | Phiên đấu giá, quy trình tuyển dụng |
| Tương thích khuyến khích (Incentive Compatibility) | Nói thật là chiến lược tối ưu cho mỗi người chơi | Đấu giá Vickrey — trả giá thật không bao giờ thiệt |
| Hiệu quả phân bổ (Allocative Efficiency) | Hàng đến tay người đánh giá cao nhất | Người trả giá cao nhất thắng |
| Ràng buộc tham gia (Participation Constraint) | Người chơi phải được lợi hơn so với không tham gia | Không ai bị ép mua giá cao hơn giá trị họ đánh giá |
| Giá sàn (Reserve Price) | Giá tối thiểu người bán chấp nhận | Shopee đặt giá khởi điểm 1.000đ |

---

## Khi nào áp dụng

- **Bạn là người thiết kế luật**, không phải người chơi — bạn quyết định quy trình
- **Người tham gia có thông tin riêng** mà bạn muốn họ tiết lộ trung thực
- **Kết quả hiện tại không tối ưu** vì luật chơi tạo khuyến khích sai
- **Cần phân bổ nguồn lực khan hiếm** giữa nhiều bên có nhu cầu khác nhau
- **Muốn ngăn gian lận** bằng cách khiến gian lận trở nên bất lợi

---

## Các loại đấu giá (Auction Types)

| Loại | Cách hoạt động | Chiến lược tối ưu | Điểm yếu |
|---|---|---|---|
| Anh (English / Ascending) | Giá tăng dần, người cuối cùng thắng | Trả đến giá trị thật rồi dừng | Lộ thông tin cho đối thủ |
| Hà Lan (Dutch / Descending) | Giá giảm dần, người đầu tiên chấp nhận thắng | Dừng sớm hơn giá trị thật | Rủi ro mất hàng nếu chờ quá lâu |
| Kín giá cao nhất (First-Price Sealed-Bid) | Nộp giá kín, giá cao nhất thắng và trả đúng giá đó | Trả **thấp hơn** giá trị thật (shade bid) | Không ai biết nên shade bao nhiêu |
| Vickrey (Second-Price Sealed-Bid) | Nộp giá kín, giá cao nhất thắng nhưng trả giá **người thứ hai** | **Trả đúng giá trị thật** — chiến lược trội | Dễ bị thông đồng nếu ít người |

### Tại sao đấu giá Vickrey khuyến khích nói thật?

Phân tích 3 trường hợp khi giá trị thật của bạn là V:

1. **Trả đúng V**: Nếu thắng, bạn trả giá người thứ hai (< V) → có lời. Nếu thua, người khác đánh giá cao hơn → hợp lý.
2. **Trả cao hơn V**: Rủi ro thắng nhưng trả giá > V → lỗ.
3. **Trả thấp hơn V**: Rủi ro thua dù giá người thứ hai < V → bỏ lỡ cơ hội có lời.

→ Trả đúng V luôn tối ưu bất kể đối thủ làm gì = **chiến lược trội** (Dominant Strategy).

### Định lý tương đương doanh thu (Revenue Equivalence Theorem)

> Với cùng số người tham gia, cùng phân phối giá trị, và người đánh giá thấp nhất trả 0 → **mọi loại đấu giá cho cùng doanh thu kỳ vọng**.

Điều kiện: người chơi trung lập rủi ro (Risk-Neutral), giá trị độc lập (Independent Private Values).

**Khi nào định lý bị phá vỡ** — và đây mới là chỗ thú vị:
- Người chơi sợ rủi ro → đấu giá kín giá cao nhất cho doanh thu cao hơn
- Giá trị tương quan → đấu giá Anh cho doanh thu cao hơn (giảm Lời nguyền người thắng)

### Lời nguyền người thắng (Winner's Curse)

Trong đấu giá giá trị chung (Common Value) — ví dụ đấu giá quyền khai thác dầu:
- Mỗi công ty ước lượng trữ lượng khác nhau
- Người thắng là người **ước lượng lạc quan nhất**
- → Trung bình, người thắng **trả quá cao** so với giá trị thật

**Cách phòng tránh**: Shade bid xuống, đặc biệt khi nhiều đối thủ tham gia.

---

## Phương pháp phân tích thiết kế cơ chế

### Bước 1: Xác định kết quả mong muốn
Bạn muốn đạt được gì? Hiệu quả phân bổ? Tối đa doanh thu? Công bằng?

### Bước 2: Liệt kê thông tin riêng tư
Ai biết gì mà người khác không biết? Giá trị thật? Năng lực thật? Chi phí thật?

### Bước 3: Xác định hành vi gian lận có thể
Nếu luật chơi hiện tại cho phép nói dối → nói dối có lợi không? Lợi bao nhiêu?

### Bước 4: Thiết kế luật khiến nói thật là tối ưu
Tách phần thưởng khỏi lời khai: giống Vickrey — thắng nhờ giá cao, nhưng trả theo giá người khác.

### Bước 5: Kiểm tra ràng buộc tham gia
Liệu mọi người vẫn muốn tham gia? Cơ chế có quá phức tạp không?

### Bước 6: Kiểm tra chống thông đồng
Hai hoặc nhiều người có thể hợp tác phá luật không?

---

## Ví dụ thực tế

### 1. Phán xử Solomon — cơ chế 3.000 năm tuổi

**Bối cảnh**: Hai người mẹ tranh một đứa bé. Vua Solomon ra lệnh: "Chẻ đứa bé làm đôi."

**Phân tích cơ chế**:
- Mẹ thật: Từ bỏ quyền nuôi con để con sống → bộc lộ giá trị thật (con > quyền sở hữu)
- Mẹ giả: Đồng ý chẻ → bộc lộ giá trị thật (quyền sở hữu > sống chết đứa bé)
- Solomon dùng cơ chế khiến **nói thật là phản ứng tự nhiên**

**Hạn chế**: Chỉ hoạt động nếu mẹ giả không biết trước luật chơi. Nếu biết → cả hai đều nói "Đừng chẻ" → cơ chế thất bại.

### 2. Đấu giá phổ tần số Anh Quốc (2000) — 35 tỷ USD

**Bối cảnh**: Chính phủ Anh bán giấy phép 3G. Thiết kế bởi nhà kinh tế Ken Binmore.

**Thiết kế cơ chế**:
- Đấu giá đồng thời nhiều giấy phép (Simultaneous Ascending Auction)
- Số giấy phép > số nhà mạng lớn → đảm bảo cạnh tranh từ người mới
- Giá sàn đủ cao để loại người chơi không nghiêm túc
- Quy tắc chống thông đồng: cấm liên lạc giữa các nhà thầu

**Kết quả**: Thu về 22,5 tỷ bảng (~35 tỷ USD) — gấp 4 lần dự kiến.

**So sánh**: Hà Lan dùng thiết kế kém hơn (số giấy phép = số nhà mạng lớn) → thu chỉ 2,7 tỷ USD.

### 3. eBay/Shopee — Vickrey trong thực tế

**Cơ chế proxy bidding của eBay**:
- Bạn nhập giá tối đa (Maximum Bid)
- Hệ thống tự động trả giá tối thiểu để bạn dẫn đầu
- Người thắng trả = giá cao thứ hai + bước giá tối thiểu
- → Gần giống Vickrey → khuyến khích nhập giá thật

**Vấn đề thực tế**: Sniping (trả giá phút cuối) phá vỡ lý thuyết vì đấu giá có thời hạn cố định, không phải vô hạn như mô hình.

---

## Khi nào cần thiết kế lại trò chơi

| Dấu hiệu | Giải pháp thiết kế |
|---|---|
| Mọi người nói dối về năng lực/giá trị | Tách phần thưởng khỏi lời khai (revelation principle) |
| Không ai muốn đi trước | Tạo cam kết bắt buộc (commitment device) |
| Thông đồng phổ biến | Tăng số người chơi, giám sát chéo |
| Kết quả không hiệu quả | Cho phép giao dịch phụ (side payments) |
| Người mạnh luôn thắng | Đặt giá sàn, handicap, affirmative action |

---

## Bẫy thường gặp

1. **Giả định mọi người tuân luật**: Cơ chế tốt phải hoạt động khi mọi người **cố gắng phá luật** — đó mới là stress test thật sự.

2. **Quên ràng buộc tham gia**: Cơ chế hoàn hảo nhưng không ai thèm tham gia = vô nghĩa. Luôn hỏi: "Nếu tôi là người chơi, tôi có tham gia không?"

3. **Bỏ qua chi phí phức tạp**: Cơ chế VCG (Vickrey-Clarke-Groves) tối ưu về lý thuyết nhưng quá phức tạp để con người hiểu → không ai tin → không ai tham gia.

4. **Tối ưu một mục tiêu, phá hỏng mục tiêu khác**: Tối đa doanh thu thường mâu thuẫn với hiệu quả phân bổ. Phải chọn — không thể có cả hai (trừ trường hợp đặc biệt).

5. **Thiết kế cho một lần chơi**: Trong thực tế, trò chơi lặp lại → người chơi học cách khai thác cơ chế. Phải dự đoán hành vi dài hạn, không chỉ lần đầu.

---

## Giá sàn — công cụ đơn giản nhưng mạnh mẽ

**Tại sao giá sàn quan trọng**:
- Không có giá sàn: người bán có thể bị ép bán giá thấp khi ít người tham gia
- Giá sàn quá cao: không ai mua → hàng ế
- Giá sàn tối ưu (Myerson): phụ thuộc vào phân phối giá trị của người mua

**Ví dụ thực tế**: Đấu giá bất động sản
- Giá sàn = 80% giá thị trường → đủ hấp dẫn để người mua tham gia, đủ cao để bảo vệ người bán
- Không công bố giá sàn → tạo sự không chắc chắn → người mua trả cao hơn

---

## Tóm tắt quyết định

> Khi bạn là **người chơi** → dùng lý thuyết trò chơi để tìm chiến lược tối ưu.
> Khi bạn là **người thiết kế luật** → dùng thiết kế cơ chế để tạo trò chơi mới.
> Câu hỏi chuyển đổi: "Tôi có thể thay đổi luật chơi không? Nếu có → thiết kế cơ chế."
