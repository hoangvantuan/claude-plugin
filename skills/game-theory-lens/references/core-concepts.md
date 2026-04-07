# Khái niệm cốt lõi của Lý thuyết Trò chơi

## Mục lục

1. [Ma trận Lợi ích (Payoff Matrix)](#ma-trận-lợi-ích-payoff-matrix)
2. [Lý thuyết Hữu dụng (Utility Theory)](#lý-thuyết-hữu-dụng-utility-theory)
3. [Phản hồi Tối ưu (Best Reply)](#phản-hồi-tối-ưu-best-reply)
4. [Chiến lược Trội và Bị trội (Dominant / Dominated Strategy)](#chiến-lược-trội-và-bị-trội)
5. [Cân bằng Nash (Nash Equilibrium)](#cân-bằng-nash-nash-equilibrium)
6. [Chiến lược Hỗn hợp (Mixed Strategy)](#chiến-lược-hỗn-hợp-mixed-strategy)
7. [Hiệu quả Pareto (Pareto Efficiency)](#hiệu-quả-pareto-pareto-efficiency)
8. [Trò chơi Tổng-không và Tổng-khác-không (Zero-sum vs Non-zero-sum)](#trò-chơi-tổng-không-và-tổng-khác-không)
9. [Hiểu biết Chung (Common Knowledge)](#hiểu-biết-chung-common-knowledge)
10. [Hướng dẫn từng bước](#hướng-dẫn-từng-bước)

---

## Ma trận Lợi ích (Payoff Matrix)

### Định nghĩa

Ma trận lợi ích là bảng mô tả kết quả của mọi tổ hợp hành động giữa các bên chơi. Quy ước chuẩn: **hàng = bên A (Alice)**, **cột = bên B (Bob)**. Mỗi ô chứa cặp số `(lợi ích A, lợi ích B)`.

### Cách đọc

|               | Bob: Trái | Bob: Phải |
|---------------|-----------|-----------|
| **Alice: Trên** | (3, 2)    | (1, 4)    |
| **Alice: Dưới** | (2, 1)    | (4, 3)    |

- Ô (Trên, Trái) → Alice được 3, Bob được 2.
- Số đầu tiên **luôn** là của bên chơi hàng (Alice).
- Số thứ hai **luôn** là của bên chơi cột (Bob).

### Khi nào dùng

- Khi tình huống có ≥ 2 bên ra quyết định đồng thời (hoặc không biết quyết định của nhau).
- Khi mỗi bên có tập hành động rời rạc, đếm được.
- Khi kết quả phụ thuộc vào tổ hợp hành động của tất cả các bên.

### Hướng dẫn: Xây dựng Ma trận Lợi ích cho bất kỳ tình huống nào

**Bước 1 — Xác định các bên chơi.** Ai là người ra quyết định thực sự? Loại bỏ bên không có quyền chọn.

**Bước 2 — Liệt kê hành động khả thi của mỗi bên.** Giữ ≤ 3-4 hành động/bên để ma trận không bùng nổ. Gộp các hành động tương tự.

**Bước 3 — Xác định thứ tự thời gian.** Các bên quyết định đồng thời hay tuần tự? Nếu đồng thời → ma trận chuẩn. Nếu tuần tự → cây trò chơi (game tree) phù hợp hơn, nhưng vẫn có thể chuyển về ma trận.

**Bước 4 — Gán giá trị lợi ích.** Không cần con số chính xác — chỉ cần **thứ hạng** đúng. Hỏi: "Bên A thích kết quả X hơn Y không?" Nếu có, gán X > Y.

**Bước 5 — Kiểm tra tính nhất quán.** Đọc lại từng ô: "Nếu Alice làm X và Bob làm Y, kết quả này có hợp lý không?"

**Bước 6 — Xác nhận giả định.** Ma trận giả định các bên duy lý (rational) và biết cấu trúc trò chơi. Nếu không đúng, ghi rõ giới hạn.

### Ví dụ thực tế: Hai quán cà phê cạnh nhau

Hai quán cà phê quyết định giá: Cao hoặc Thấp.

|                   | Quán B: Giá Cao | Quán B: Giá Thấp |
|-------------------|-----------------|-------------------|
| **Quán A: Giá Cao**  | (50, 50)        | (10, 70)          |
| **Quán A: Giá Thấp** | (70, 10)        | (30, 30)          |

- Cả hai giá cao → chia đều thị trường, lợi nhuận tốt.
- Một bên hạ giá → hút khách, bên kia mất khách.
- Cả hai hạ giá → cạnh tranh đáy, ai cũng thiệt.

---

## Lý thuyết Hữu dụng (Utility Theory)

### Định nghĩa

Hữu dụng (utility) là con số đại diện cho mức độ ưa thích của một bên đối với một kết quả. Không phải tiền — mà là **thước đo sự ưa thích** bao gồm cả yếu tố phi tài chính (danh tiếng, thời gian, cảm xúc).

### Sở thích Bộc lộ (Revealed Preference)

Không cần hỏi ai thích gì — quan sát **hành vi thực tế**. Nếu ai đó chọn A khi có thể chọn B, ta suy ra họ thích A hơn B. Đây là cách gán giá trị utility thực tế nhất.

### Thái độ Rủi ro (Risk Attitudes)

| Thái độ | Mô tả | Ví dụ |
|---------|--------|-------|
| Ưa rủi ro (Risk-seeking) | Thích cơ hội lớn dù xác suất thấp | Đầu tư startup, mua vé số |
| Trung lập rủi ro (Risk-neutral) | Chỉ quan tâm kỳ vọng trung bình | Quỹ đầu tư lớn, bảo hiểm |
| Tránh rủi ro (Risk-averse) | Thích chắc chắn hơn kỳ vọng cao | Mua bảo hiểm, gửi tiết kiệm |

### Khi nào dùng

- Khi cần so sánh các kết quả có bản chất khác nhau (tiền vs thời gian vs danh tiếng).
- Khi kết quả liên quan đến xác suất và cần tính đến thái độ rủi ro.
- Khi hành vi quan sát được mâu thuẫn với lợi ích tài chính thuần túy.

### Cạm bẫy thường gặp

- **Đồng nhất utility với tiền.** Người ta từ chối tăng lương 20% để giữ work-life balance — utility của họ không chỉ là tiền.
- **Giả định mọi người có cùng hàm utility.** Bên A ưa rủi ro, bên B tránh rủi ro → cùng trò chơi nhưng hành vi hoàn toàn khác.

---

## Phản hồi Tối ưu (Best Reply)

### Định nghĩa

Phản hồi tối ưu của bên A với hành động X của bên B là hành động mang lại lợi ích cao nhất cho A, **giả định B chơi X**. Ký hiệu: BR_A(X).

### Cách tìm

1. Cố định một cột (hành động của Bob).
2. So sánh lợi ích của Alice trong các hàng.
3. Hàng có lợi ích Alice cao nhất = Best Reply của Alice.
4. Lặp lại cho mỗi cột.
5. Làm tương tự cho Bob (cố định hàng, so sánh cột).

### Ví dụ

|               | Bob: X | Bob: Y |
|---------------|--------|--------|
| **Alice: A**  | (3, 1) | (0, 2) |
| **Alice: B**  | (2, 3) | (1, 0) |

- Bob chơi X → Alice so 3 vs 2 → BR_Alice(X) = A
- Bob chơi Y → Alice so 0 vs 1 → BR_Alice(Y) = B
- Alice chơi A → Bob so 1 vs 2 → BR_Bob(A) = Y
- Alice chơi B → Bob so 3 vs 0 → BR_Bob(B) = X

---

## Chiến lược Trội và Bị trội

### Chiến lược Trội (Dominant Strategy)

Hành động tốt nhất **bất kể đối phương làm gì**. Nếu tồn tại, chọn nó là lựa chọn duy lý hiển nhiên.

### Chiến lược Bị trội (Dominated Strategy)

Hành động **luôn tệ hơn** một hành động khác bất kể đối phương làm gì. Bên duy lý không bao giờ chọn chiến lược bị trội.

### Loại bỏ Lặp (Iterated Elimination of Dominated Strategies - IEDS)

1. Tìm chiến lược bị trội của bất kỳ bên nào → loại bỏ.
2. Trong ma trận rút gọn, tìm tiếp chiến lược bị trội → loại bỏ.
3. Lặp cho đến khi không còn chiến lược bị trội.
4. Nếu còn đúng 1 ô → đó là nghiệm duy nhất.

### Khi nào dùng

- IEDS là bước đầu tiên trước khi tìm Nash — đơn giản hóa ma trận.
- Nếu một bên có chiến lược trội, phân tích trở nên đơn giản: bên đó luôn chơi chiến lược trội, bên còn lại best-reply theo.

### Cạm bẫy

- **Trội yếu vs trội mạnh (Weak vs Strict dominance).** Trội yếu: ≥ trong mọi trường hợp, > trong ít nhất một. Loại bỏ trội yếu có thể thay đổi tập Nash — cần cẩn thận.

---

## Cân bằng Nash (Nash Equilibrium)

### Định nghĩa

Tổ hợp chiến lược mà **không bên nào có lợi khi đơn phương đổi chiến lược**, giả định các bên khác giữ nguyên. Nói cách khác: mỗi bên đang chơi Best Reply với chiến lược của bên kia.

### Hai cách hiểu

| Góc nhìn | Mô tả | Hàm ý |
|-----------|--------|-------|
| Duy lý (Rational) | Mỗi bên suy luận logic và chọn tối ưu | Cần giả định về hiểu biết chung, tính duy lý |
| Tiến hóa (Evolutionary) | Chiến lược sống sót qua thử-và-sai trong quần thể lớn | Không cần bên chơi "thông minh" — chọn lọc tự nhiên đủ |

### Hướng dẫn: Tìm Cân bằng Nash (phương pháp Best Reply)

**Bước 1 — Đánh dấu Best Reply của Alice.** Với mỗi cột (hành động Bob), gạch chân lợi ích cao nhất của Alice trong cột đó.

**Bước 2 — Đánh dấu Best Reply của Bob.** Với mỗi hàng (hành động Alice), gạch chân lợi ích cao nhất của Bob trong hàng đó.

**Bước 3 — Tìm ô có cả hai gạch chân.** Ô nào cả lợi ích Alice lẫn Bob đều được gạch chân → đó là Nash Equilibrium.

### Ví dụ hoàn chỉnh

|               | Bob: L   | Bob: R   |
|---------------|----------|----------|
| **Alice: U**  | (**3**, 1) | (0, **2**) |
| **Alice: D**  | (2, **3**) | (**1**, 0) |

Best Reply Alice: cột L → U (3>2), cột R → D (1>0) → gạch chân **3** và **1**.
Best Reply Bob: hàng U → R (2>1), hàng D → L (3>0) → gạch chân **2** và **3**.

Ô có cả hai gạch chân: **không có** → trò chơi này không có Nash thuần túy → cần tìm Mixed Strategy Nash.

### Khi nào dùng

- Sau khi đã loại bỏ chiến lược bị trội (IEDS).
- Để dự đoán kết quả "ổn định" của tương tác chiến lược.
- Để kiểm tra: "Liệu thỏa thuận/kế hoạch hiện tại có bền vững không?" — nếu ai đó có động cơ lệch → không phải Nash → sẽ sụp đổ.

### Cạm bẫy thường gặp

- **Nash ≠ kết quả tốt nhất.** Trong Thế lưỡng nan Tù nhân (Prisoner's Dilemma), Nash là (Phản bội, Phản bội) — tệ cho cả hai.
- **Nhiều Nash.** Một trò chơi có thể có 0, 1, hoặc nhiều Nash thuần túy. Nhiều Nash → vấn đề phối hợp (ai chọn cái nào?).
- **Nash không nói ai "nên" làm gì.** Nó dự đoán kết quả ổn định, không phải kết quả mong muốn.

---

## Chiến lược Hỗn hợp (Mixed Strategy)

### Định nghĩa

Thay vì chọn chắc chắn một hành động, bên chơi **ngẫu nhiên hóa** giữa các hành động với xác suất cụ thể. Ví dụ: chơi Trái với xác suất 0.7, Phải với xác suất 0.3.

### Nguyên lý Vô hiệu hóa (Indifference Principle)

Trong Nash hỗn hợp, xác suất của bên A được chọn sao cho **bên B vô hiệu giữa các hành động của mình** (kỳ vọng bằng nhau). Nghịch lý: xác suất của bạn được xác định bởi lợi ích của đối phương, không phải của bạn.

### Khi nào dùng

- Khi không có Nash thuần túy (ví dụ: Oẳn tù tì / Matching Pennies).
- Khi cần tránh bị đoán trước (thể thao, đàm phán, an ninh).
- Khi trò chơi lặp lại và đối phương có thể học pattern của bạn.

### Ví dụ: Penalty Kick

Thủ môn chọn Trái/Phải. Cầu thủ sút Trái/Phải. Nếu cùng hướng → thủ môn cản. Khác hướng → bàn thắng.

|               | Thủ môn: Trái | Thủ môn: Phải |
|---------------|--------------|---------------|
| **Sút: Trái**  | (0, 1)       | (1, 0)        |
| **Sút: Phải**  | (1, 0)       | (0, 1)        |

Nash hỗn hợp: cả hai chơi 50-50. Dữ liệu thực tế từ bóng đá chuyên nghiệp xác nhận tỷ lệ gần 50-50.

### Cạm bẫy

- **Hỗn hợp không có nghĩa là "lung tung".** Xác suất được tính toán chính xác từ cấu trúc lợi ích.
- **Trong thực tế, ít ai ngẫu nhiên hóa hoàn hảo.** Con người có thiên kiến pattern — đối thủ tinh ý sẽ khai thác.

---

## Hiệu quả Pareto (Pareto Efficiency)

### Định nghĩa

Kết quả Pareto hiệu quả là kết quả mà **không thể cải thiện cho bất kỳ bên nào mà không làm tệ hơn cho bên khác**. Kết quả Pareto bị trội (Pareto dominated) là kết quả tồn tại phương án tốt hơn cho mọi bên (hoặc tốt hơn cho một bên mà không hại bên nào).

### So sánh Nash và Pareto

| Tiêu chí | Nash | Pareto |
|-----------|------|--------|
| Câu hỏi | Ai có động cơ lệch? | Có thể cải thiện cho mọi người? |
| Ổn định | Có — không ai muốn đổi | Không nhất thiết — có thể không ổn định |
| Tối ưu xã hội | Không nhất thiết | Có — không lãng phí |
| Số lượng | Thường ít (1-3) | Thường nhiều |

### Khi nào dùng

- Để đánh giá: "Kết quả hiện tại có lãng phí không?" Nếu Pareto bị trội → tồn tại cải thiện win-win.
- Để phân biệt vấn đề phối hợp (cần thỏa thuận) vs xung đột thực sự (lợi ích đối lập).

### Ví dụ

Trong bài toán hai quán cà phê ở trên: (Cao, Cao) = (50, 50) là Pareto hiệu quả. (Thấp, Thấp) = (30, 30) là Pareto bị trội bởi (Cao, Cao). Nhưng (Thấp, Thấp) lại là Nash. Đây chính là bi kịch của Thế lưỡng nan Tù nhân.

---

## Trò chơi Tổng-không và Tổng-khác-không

### Tổng-không (Zero-sum)

Lợi ích một bên = tổn thất bên kia. Tổng lợi ích mọi ô = hằng số. Đây là trò chơi **đối đầu thuần túy** — không có win-win.

### Tổng-khác-không (Non-zero-sum)

Tổng lợi ích thay đổi tùy ô. Có thể win-win hoặc lose-lose. **Hầu hết tình huống thực tế** là tổng-khác-không.

### Tại sao phân biệt quan trọng

| Loại | Đàm phán | Chiến lược tối ưu |
|------|----------|-------------------|
| Tổng-không | Phân chia miếng bánh cố định | Tối đa lợi mình = tối thiểu lợi đối phương |
| Tổng-khác-không | Có thể làm bánh lớn hơn | Hợp tác có thể tốt hơn cho tất cả |

### Cạm bẫy

- **Nhầm tổng-khác-không thành tổng-không.** Đa số xung đột kinh doanh, chính trị không phải tổng-không — nhưng người ta thường nghĩ vậy → bỏ lỡ cơ hội hợp tác.

---

## Hiểu biết Chung (Common Knowledge)

### Định nghĩa

Sự kiện E là hiểu biết chung nếu: mọi người biết E, mọi người biết rằng mọi người biết E, mọi người biết rằng mọi người biết rằng mọi người biết E... lặp vô hạn.

### Tại sao quan trọng

Nash Equilibrium giả định cấu trúc trò chơi (ma trận, hành động, lợi ích) là hiểu biết chung. Nếu không:
- Bên A không biết lợi ích của B → không tính được Best Reply.
- Bên A biết lợi ích B nhưng B không biết A biết → B hành xử khác.

### Ví dụ: Bài toán Hai tướng (Two Generals Problem)

Hai tướng cần phối hợp tấn công. Gửi tin qua liên lạc không đáng tin cậy. Tướng A gửi "tấn công lúc rạng sáng" — không chắc B nhận được. B xác nhận — không chắc A nhận xác nhận. A xác nhận xác nhận — không chắc B nhận... Không bao giờ đạt hiểu biết chung → phối hợp bất khả.

### Khi nào dùng

- Khi phân tích tình huống mà thông tin không đối xứng hoặc kênh truyền không đáng tin cậy.
- Khi đánh giá liệu một thỏa thuận/quy ước có thực sự được tất cả các bên hiểu giống nhau.

---

## Hướng dẫn từng bước: Phân tích tình huống bằng Lý thuyết Trò chơi

### Bước 1 — Nhận diện cấu trúc trò chơi
- Ai là bên chơi?
- Mỗi bên có những lựa chọn nào?
- Quyết định đồng thời hay tuần tự?
- Thông tin đối xứng hay bất đối xứng?

### Bước 2 — Xây dựng Ma trận Lợi ích
- Gán giá trị (thứ hạng hoặc con số) cho mỗi kết quả.
- Xác nhận: giá trị phản ánh đúng sở thích thực tế?

### Bước 3 — Phân tích chiến lược
- Loại bỏ chiến lược bị trội (IEDS).
- Tìm Best Reply cho mỗi bên.
- Xác định Nash Equilibrium (thuần túy và/hoặc hỗn hợp).

### Bước 4 — Đánh giá kết quả
- Nash có Pareto hiệu quả không?
- Nếu không → tồn tại cơ hội cải thiện nhưng cần cơ chế (cam kết, lặp lại, bên thứ ba).

### Bước 5 — So khớp với Nguyên mẫu (Archetype)
- Cấu trúc giống Thế lưỡng nan Tù nhân, Trò chơi Gà, Săn Hươu, hay loại nào?
- Nguyên mẫu gợi ý giải pháp đã biết.

### Bước 6 — Xem xét yếu tố mở rộng
- Trò chơi lặp lại? → Hợp tác có thể bền vững.
- Thông tin bất đối xứng? → Cần xem xét tín hiệu, sàng lọc.
- Nhiều bên chơi? → Cần liên minh, cơ chế phiếu bầu.
