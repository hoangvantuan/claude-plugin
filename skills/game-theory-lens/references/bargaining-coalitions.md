# Mặc cả và liên minh (Bargaining & Coalitions)

## Khái niệm cốt lõi

Lý thuyết mặc cả (Bargaining Theory) phân tích cách hai hoặc nhiều bên **chia sẻ lợi ích từ hợp tác** — khi hợp tác có lợi hơn không hợp tác, nhưng ai cũng muốn phần lớn hơn. Lý thuyết liên minh (Coalition Theory) mở rộng sang 3+ người chơi: ai kết hợp với ai, chia lợi ích thế nào.

### Các thuật ngữ nền tảng

| Thuật ngữ                          | Định nghĩa                                                                            | Ví dụ                                      |
| ---------------------------------- | ------------------------------------------------------------------------------------- | ------------------------------------------ |
| Điểm bất đồng (Disagreement Point) | Payoff mỗi bên nhận nếu đàm phán thất bại                                             | Mức lương hiện tại khi đàm phán tăng lương |
| BATNA                              | Phương án thay thế tốt nhất ngoài đàm phán (Best Alternative To Negotiated Agreement) | Lời mời từ công ty khác                    |
| Thặng dư hợp tác (Surplus)         | Tổng lợi ích hợp tác − tổng lợi ích không hợp tác                                     | Giá trị tạo thêm khi hai công ty sáp nhập  |
| Lõi (Core)                         | Tập hợp phân chia mà không liên minh con nào muốn tách ra                             | Phân chia ổn định trong nhóm 3+ người      |
| Giá trị Shapley (Shapley Value)    | Phân chia "công bằng" dựa trên đóng góp biên trung bình                               | Chia lợi nhuận theo đóng góp thật sự       |


---

## Khi nào áp dụng

- **Hai bên đàm phán trực tiếp** về giá, lương, điều khoản hợp đồng
- **Nhiều bên cân nhắc hợp tác** và cần chia lợi ích công bằng
- **Sức mạnh đàm phán không đối xứng** — một bên có lựa chọn tốt hơn
- **Cần đánh giá BATNA** trước khi vào đàm phán
- **Phân chia chi phí chung** giữa nhiều bên (hạ tầng, dự án chung)

---

## Giải pháp mặc cả Nash (Nash Bargaining Solution)

### Nguyên tắc

> Tối đa hóa **tích** của phần thặng dư mỗi bên nhận được so với điểm bất đồng.

Công thức: max (u₁ − d₁) × (u₂ − d₂)

Trong đó:

- u₁, u₂: phần mỗi bên nhận
- d₁, d₂: payoff tại điểm bất đồng

### Trường hợp đối xứng

Nếu hai bên có cùng sức mạnh → **chia đôi thặng dư**:

- Thặng dư = Tổng giá trị − d₁ − d₂
- Mỗi bên nhận: dᵢ + Thặng dư/2

### Trường hợp bất đối xứng

Sức mạnh đàm phán khác nhau (tham số α cho bên 1, 1−α cho bên 2):

- max (u₁ − d₁)^α × (u₂ − d₂)^(1−α)
- α cao hơn → bên 1 nhận phần lớn hơn

**Trực giác**: Sức mạnh đàm phán đến từ đâu?

- Điểm bất đồng cao → mạnh hơn (ít cần thỏa thuận)
- Kiên nhẫn hơn → mạnh hơn (chịu được kéo dài)
- Ít sợ rủi ro hơn → mạnh hơn (dám mạo hiểm đổ vỡ)

---

## Mô hình đề nghị xen kẽ Rubinstein (Rubinstein Alternating Offers)

### Cơ chế

1. Người chơi 1 đề nghị cách chia
2. Người chơi 2 chấp nhận hoặc từ chối
3. Nếu từ chối: Người chơi 2 đề nghị (nhưng "bánh" co lại theo hệ số chiết khấu δ)
4. Lặp lại cho đến khi đồng ý

### Cân bằng hoàn hảo con trò chơi (Subgame Perfect Equilibrium)

Với hệ số chiết khấu δ₁, δ₂ (0 < δ < 1, càng gần 1 = càng kiên nhẫn):

- **Người đề nghị trước nhận**: 1/(1 + δ₁) phần (khi δ₁ = δ₂ = δ → 1/(1+δ))
- **Người đề nghị sau nhận**: δ/(1 + δ) phần

### Bài học chiến lược

| Yếu tố                  | Ảnh hưởng                           | Lý do                                                 |
| ----------------------- | ----------------------------------- | ----------------------------------------------------- |
| Kiên nhẫn (δ cao)       | Nhận phần lớn hơn                   | Chịu được kéo dài → đối phương nhượng bộ trước        |
| Đề nghị trước           | Lợi thế nhỏ (First-Mover Advantage) | Đặt khung tham chiếu, đối phương phải phản ứng        |
| Chi phí chậm trễ cao    | Nhận phần nhỏ hơn                   | Muốn kết thúc nhanh → chấp nhận ít hơn                |
| Cam kết không nhượng bộ | Lợi thế lớn — nếu đáng tin          | "Tôi không thể giảm thêm" → đối phương phải chấp nhận |


---

## Điểm bất đồng vs Lựa chọn bên ngoài — phân biệt quan trọng!

|                    | Điểm bất đồng (Disagreement Point)    | Lựa chọn bên ngoài (Outside Option)                    |
| ------------------ | ------------------------------------- | ------------------------------------------------------ |
| **Khi nào xảy ra** | Đàm phán thất bại hoàn toàn           | Bạn rời bàn đàm phán để chọn phương án khác            |
| **Ảnh hưởng**      | Luôn ảnh hưởng kết quả (nâng sàn)     | Chỉ ảnh hưởng nếu tốt hơn phần bạn sẽ nhận             |
| **Ví dụ**          | Công nhân đình công → cả hai mất      | Nhận offer từ công ty khác                             |
| **Chiến lược**     | Cải thiện điểm bất đồng → luôn có lợi | Cải thiện outside option → chỉ có lợi nếu nó ràng buộc |


**Ví dụ minh họa**: Đàm phán lương

- Lương hiện tại 20tr, đàm phán tăng lương
- Điểm bất đồng: vẫn nhận 20tr (không đàm phán được = giữ nguyên)
- Outside option: offer 25tr từ công ty khác
- Nếu kết quả đàm phán > 25tr → outside option không ảnh hưởng
- Nếu kết quả đàm phán < 25tr → bạn rời đi, outside option ràng buộc

→ **Sai lầm phổ biến**: Nghĩ rằng có offer bên ngoài tự động tăng kết quả. Thực tế: chỉ tăng nếu offer đó **tốt hơn** phần bạn sẽ nhận.

---

## Định lý Coase (Coase Theorem)

> Nếu chi phí giao dịch = 0 và quyền sở hữu rõ ràng → đàm phán hợp lý **luôn đạt kết quả hiệu quả**, bất kể quyền sở hữu ban đầu thuộc về ai.

### Ví dụ kinh điển

Nhà máy gây ô nhiễm, hàng xóm chịu thiệt hại:

- **Hàng xóm có quyền** không khí sạch → nhà máy trả tiền bồi thường để tiếp tục hoạt động
- **Nhà máy có quyền** thải → hàng xóm trả tiền để nhà máy giảm thải
- Cả hai trường hợp → mức thải **hiệu quả** giống nhau (chỉ phân phối tiền khác)

### Tại sao thực tế thường thất bại

| Rào cản                | Ví dụ                                                 |
| ---------------------- | ----------------------------------------------------- |
| Chi phí giao dịch cao  | Triệu người bị ô nhiễm không thể đàm phán cùng lúc    |
| Thông tin bất đối xứng | Nhà máy giấu mức thiệt hại thật                       |
| Quyền sở hữu không rõ  | Ai sở hữu không khí? Biển? Dữ liệu cá nhân?           |
| Số lượng bên quá lớn   | Free-rider problem: "người khác sẽ đàm phán thay tôi" |


→ Coase Theorem hữu ích nhất khi: **ít bên, chi phí giao dịch thấp, quyền rõ ràng**.

---

## Lý thuyết liên minh (Coalition Theory)

### Khi nào cần liên minh?

Với 3+ người chơi, câu hỏi không chỉ là "chia bao nhiêu" mà còn "liên minh với ai":

**Ví dụ**: Ba đảng chính trị (A: 45 ghế, B: 35 ghế, C: 20 ghế). Cần 51 ghế để nắm quyền.

- A+B = 80 ghế ✓
- A+C = 65 ghế ✓  
- B+C = 55 ghế ✓
- → Mọi cặp đều thắng → liên minh nào hình thành?

### Lõi (Core)

Phân chia nằm trong Core nếu **không liên minh con nào có thể tự làm tốt hơn**:

- Liên minh {A,B} nhận tổng ≥ giá trị {A,B} tự tạo
- Liên minh {A,C} nhận tổng ≥ giá trị {A,C} tự tạo
- Tương tự cho mọi liên minh con

**Vấn đề**: Core có thể rỗng — không có phân chia nào ổn định → luôn có liên minh muốn phá vỡ thỏa thuận.

### Giá trị Shapley (Shapley Value)

> Phân chia "công bằng" dựa trên **đóng góp biên trung bình** của mỗi người chơi.

**Cách tính** (trực giác):

1. Xếp ngẫu nhiên thứ tự N người chơi
2. Mỗi người nhận = giá trị liên minh sau khi họ vào − giá trị liên minh trước khi họ vào
3. Lấy trung bình trên **tất cả** thứ tự có thể

**Tính chất Shapley đảm bảo**:

- **Hiệu quả**: Chia hết tổng giá trị
- **Đối xứng**: Người đóng góp giống nhau → nhận giống nhau
- **Dummy**: Người không đóng góp → nhận 0
- **Cộng tính**: Shapley(game1 + game2) = Shapley(game1) + Shapley(game2)

### Ví dụ Shapley: Chia chi phí đường băng sân bay

3 loại máy bay cần đường băng dài khác nhau:

- Loại nhỏ: cần 1km
- Loại trung: cần 2km
- Loại lớn: cần 3km
- Chi phí: 1 triệu/km

**Chia đều 3 triệu/3 = 1 triệu mỗi loại?** Không công bằng — loại nhỏ chỉ cần 1km.

**Shapley Value**:

- 1km đầu: cả 3 dùng → chia 3 = 333K mỗi loại
- 1km thứ hai: chỉ trung + lớn dùng → chia 2 = 500K mỗi loại
- 1km thứ ba: chỉ lớn dùng → 1 triệu cho lớn

| Loại  | Shapley | % tổng |
| ----- | ------- | ------ |
| Nhỏ   | 333K    | 11%    |
| Trung | 833K    | 28%    |
| Lớn   | 1.833K  | 61%    |


→ Nguyên tắc: Người gây chi phí nhiều hơn → trả nhiều hơn, nhưng vẫn được giảm nhờ phần dùng chung.

---

## Nghịch lý Condorcet (Condorcet Paradox)

### Bỏ phiếu theo đa số có thể tạo vòng lặp

3 cử tri, 3 phương án (A, B, C):

| Cử tri | Thứ tự ưa thích |
| ------ | --------------- |
| 1      | A > B > C       |
| 2      | B > C > A       |
| 3      | C > A > B       |


Kết quả bỏ phiếu theo cặp:

- A vs B: A thắng (cử tri 1, 3) → A > B
- B vs C: B thắng (cử tri 1, 2) → B > C
- C vs A: C thắng (cử tri 2, 3) → C > A
- → **A > B > C > A** — vòng lặp!

**Hệ quả**: Không có "ý chí đa số" rõ ràng. Người kiểm soát **chương trình nghị sự** (chọn cặp nào bỏ phiếu trước) kiểm soát kết quả.

→ Trong doanh nghiệp: Khi ban giám đốc bỏ phiếu giữa 3+ phương án, **thứ tự bỏ phiếu có thể quyết định kết quả**, không phải sở thích thật sự.

---

## Phương pháp phân tích mặc cả

### Bước 1: Xác định BATNA của mỗi bên

Mỗi bên sẽ làm gì nếu đàm phán thất bại? Giá trị phương án đó?

### Bước 2: Tính thặng dư hợp tác

Tổng giá trị hợp tác − tổng BATNA = phần "bánh" có thể chia.

### Bước 3: Đánh giá sức mạnh đàm phán

Ai kiên nhẫn hơn? Ai sợ rủi ro ít hơn? Ai có cam kết đáng tin hơn?

### Bước 4: Dự đoán phân chia

Áp dụng Nash Bargaining hoặc Rubinstein tùy bối cảnh.

### Bước 5: Kiểm tra outside options

Outside option có ràng buộc không? Nếu có → điều chỉnh dự đoán.

### Bước 6: Xem xét yếu tố hành vi

Công bằng cảm tính (fairness), ego, cảm xúc — thực tế này thường quan trọng hơn lý thuyết.

---

## Ví dụ thực tế

### 1. Đàm phán lương — Rubinstein trong đời thật

**Bối cảnh**: Lập trình viên senior đàm phán lương với công ty tech.

| Yếu tố    | Lập trình viên                      | Công ty                                         |
| --------- | ----------------------------------- | ----------------------------------------------- |
| BATNA     | Offer 40tr từ công ty khác          | Tuyển ứng viên khác (mất 2 tháng, 50tr chi phí) |
| Kiên nhẫn | Trung bình (cần việc trong 1 tháng) | Thấp (dự án gấp, thiếu người)                   |
| Thông tin | Biết thị trường lương               | Biết budget team                                |


**Phân tích**:

- Thặng dư: Giá trị nhân sự cho công ty (say 60tr/tháng) − BATNA lập trình viên (40tr) = 20tr
- Công ty ít kiên nhẫn → lập trình viên có lợi thế
- Dự đoán: Lương 45-50tr (lập trình viên nhận >50% thặng dư nhờ kiên nhẫn hơn)

**Chiến lược cho lập trình viên**: Tăng BATNA (tìm thêm offer), thể hiện kiên nhẫn (không vội), cam kết đáng tin ("Dưới 45tr tôi chọn offer kia").

### 2. Mua bán nhà — bất đối xứng thông tin

**Bối cảnh**: Người bán biết nhà có vấn đề nền móng. Người mua không biết.

**Phân tích**:

- Người bán: Giá trị thật 2 tỷ (do vấn đề nền), muốn bán 3 tỷ
- Người mua: Đánh giá 3.5 tỷ (không biết vấn đề nền)
- Coase: Nếu thông tin đầy đủ → giá khoảng 2.5-3 tỷ (chia đôi thặng dư)
- Thực tế: Bất đối xứng thông tin → người mua có thể trả 3 tỷ → mua đắt 1 tỷ

**Giải pháp cơ chế**: Yêu cầu giám định độc lập, warranty, disclosure laws → giảm bất đối xứng thông tin.

### 3. Chia chi phí dự án chung — Shapley Value trong doanh nghiệp

**Bối cảnh**: 3 phòng ban dùng chung hệ thống IT.

- Phòng A dùng module cơ bản (500tr)
- Phòng B dùng module cơ bản + nâng cao (800tr)
- Phòng C dùng toàn bộ (1 tỷ)

**Chia đều**: 1 tỷ / 3 = 333tr mỗi phòng? Phòng A phản đối — họ chỉ cần module 500tr.

**Shapley Value** — nguyên tắc đóng góp biên:

- Module cơ bản (500tr): Cả 3 dùng → 167tr mỗi phòng
- Module nâng cao (300tr): B + C dùng → 150tr mỗi phòng
- Module đặc biệt (200tr): Chỉ C dùng → 200tr cho C

| Phòng | Shapley | So với chia đều |
| ----- | ------- | --------------- |
| A     | 167tr   | Giảm 166tr      |
| B     | 317tr   | Giảm 16tr       |
| C     | 517tr   | Tăng 184tr      |


→ Công bằng hơn, mỗi phòng trả tương xứng mức sử dụng, và không phòng nào muốn tách ra tự xây riêng.

---

## Bẫy thường gặp

1. **Nhầm BATNA với mong muốn**: BATNA là phương án thay thế **thật sự có**, không phải mức giá bạn **muốn**. "Tôi muốn 50tr" không phải BATNA. "Tôi có offer 45tr" mới là BATNA.
2. **Bỏ qua chi phí đàm phán**: Rubinstein giả định đàm phán kéo dài chỉ tốn thời gian. Thực tế: mỗi vòng đàm phán tốn luật sư, stress, thiện chí. Đôi khi chấp nhận ít hơn để kết thúc nhanh = tối ưu.
3. **Cam kết không đáng tin**: "Tôi sẽ không bao giờ chấp nhận dưới X" chỉ mạnh nếu đối phương **tin** bạn sẽ giữ lời. Cam kết đáng tin cần: công khai, không thể rút lại, có chi phí nếu nuốt lời.
4. **Shapley Value thiếu thực tế**: Tính Shapley cần biết giá trị mọi liên minh con — thường rất khó ước lượng. Với N người chơi cần tính 2^N giá trị liên minh. N = 20 → hơn 1 triệu giá trị.
5. **Giả định mọi người lý trí**: Ultimatum game cho thấy người ta **từ chối** offer bất công dù từ chối = mất tiền. Công bằng cảm tính (perceived fairness) ảnh hưởng lớn hơn lý thuyết dự đoán.
6. **Quên power dynamics**: Lý thuyết giả định "mọi bên có quyền rời bàn". Thực tế: nhân viên đàm phán với sếp, nước nhỏ đàm phán với nước lớn — sức mạnh bất đối xứng phá vỡ các dự đoán cân bằng.
