# Thông tin và Tín hiệu trong Lý thuyết Trò chơi

## Mục lục

1. [Phân loại Thông tin](#phân-loại-thông-tin)
2. [Tập Thông tin (Information Sets)](#tập-thông-tin-information-sets)
3. [Nói suông vs Tín hiệu Tốn kém (Cheap Talk vs Costly Signaling)](#nói-suông-vs-tín-hiệu-tốn-kém)
4. [Lừa phỉnh (Bluffing)](#lừa-phỉnh-bluffing)
5. [Sàng lọc (Screening)](#sàng-lọc-screening)
6. [Ví dụ Tín hiệu Kinh điển](#ví-dụ-tín-hiệu-kinh-điển)
7. [Khi Bất đối xứng Thông tin Thay đổi Cấu trúc Trò chơi](#khi-bất-đối-xứng-thông-tin-thay-đổi-cấu-trúc-trò-chơi)
8. [Ví dụ Thực tế](#ví-dụ-thực-tế)

---

## Phân loại Thông tin

### Bốn loại cơ bản

| | Biết hành động đã chơi (Thông tin Hoàn hảo - Perfect) | Không biết hành động đã chơi (Thông tin Không hoàn hảo - Imperfect) |
|---|---|---|
| **Biết loại/lợi ích đối phương (Thông tin Đầy đủ - Complete)** | Cờ vua: thấy mọi nước đi, biết mục tiêu đối thủ | Oẳn tù tì: biết lợi ích nhưng không biết đối phương sẽ ra gì |
| **Không biết loại/lợi ích đối phương (Thông tin Không đầy đủ - Incomplete)** | Hiếm trong thực tế | Đấu thầu kín: không biết giá trị đối thủ gán cho hợp đồng, không biết họ đấu bao nhiêu |

### Cách phân biệt

- **Hoàn hảo vs Không hoàn hảo (Perfect vs Imperfect):** Có biết lịch sử nước đi trước đó không?
- **Đầy đủ vs Không đầy đủ (Complete vs Incomplete):** Có biết "kiểu" (type) của đối phương không — tức là lợi ích, sở thích, năng lực?

### Chuyển đổi Harsanyi (Harsanyi's Typecasting)

Trò chơi thông tin không đầy đủ có thể chuyển thành thông tin không hoàn hảo bằng cách thêm **"Thiên nhiên" (Nature)** là bên chơi đầu tiên — Thiên nhiên ngẫu nhiên gán "kiểu" cho mỗi bên, mỗi bên chỉ biết kiểu mình. Kỹ thuật này biến bất kỳ trò chơi nào thành dạng phân tích được.

### Khi nào dùng

- Khi cần xác định: "Tình huống này có cấu trúc thông tin nào?" → Quyết định công cụ phân tích phù hợp.
- Thông tin đầy đủ + hoàn hảo → phân tích backward induction (quy nạp ngược).
- Thông tin không đầy đủ → cần Bayesian Nash Equilibrium (cân bằng Bayes-Nash).

---

## Tập Thông tin (Information Sets)

### Định nghĩa

Tập thông tin là nhóm các nút trong cây trò chơi mà bên chơi **không phân biệt được** khi đến lượt ra quyết định. Nếu bạn đang ở nút A hoặc B nhưng không biết ở đâu → A và B thuộc cùng tập thông tin → bạn phải chọn cùng hành động tại cả hai nút.

### Ý nghĩa thực tế

- Nếu mọi tập thông tin chỉ có 1 nút → trò chơi thông tin hoàn hảo (bạn luôn biết mình đang ở đâu).
- Nếu tập thông tin có nhiều nút → bạn đang hành động trong **sương mù** — phải xét xác suất từng nút.

### Ví dụ

Đàm phán mua nhà: Bạn không biết mức giá tối thiểu người bán chấp nhận. Tập thông tin của bạn bao gồm tất cả các nút tương ứng với các mức giá tối thiểu khác nhau → bạn phải chọn mức trả giá **mà không biết** mình đang ở nút nào.

---

## Nói suông vs Tín hiệu Tốn kém

### Nói suông (Cheap Talk)

Tuyên bố không có chi phí, không thể xác minh, không có hậu quả nếu nói dối. Trong lý thuyết trò chơi chuẩn: cheap talk **không mang thông tin** trong trò chơi có xung đột lợi ích thuần túy — vì bên nào cũng có động cơ nói điều có lợi cho mình.

**Nhưng:** Khi lợi ích phần lớn trùng nhau, cheap talk vẫn hữu ích. Ví dụ: hai bạn cùng muốn gặp nhau, tin nhắn "gặp ở quán A" đáng tin vì không ai có động cơ nói dối.

### Tín hiệu Tốn kém (Costly Signaling)

Hành động có chi phí thực, khó giả mạo, và chi phí **khác nhau** tùy "kiểu" bên gửi. Chìa khóa: bên "kém" không thể bắt chước vì chi phí quá cao so với lợi ích.

### Nguyên lý Nhược điểm của Zahavi (Zahavi's Handicap Principle)

Tín hiệu đáng tin **vì** nó tốn kém. Đuôi công nặng nề, dễ bị săn → chỉ con công khỏe mạnh mới "dám" mang → đuôi công = tín hiệu trung thực về sức khỏe gene. Nếu đuôi công miễn phí → mọi con đều có → mất giá trị tín hiệu.

### So sánh

| Tiêu chí | Nói suông (Cheap Talk) | Tín hiệu Tốn kém (Costly Signal) |
|----------|----------------------|----------------------------------|
| Chi phí | Không/rất thấp | Đáng kể |
| Có thể giả mạo? | Dễ dàng | Khó — chi phí cản trở |
| Đáng tin? | Chỉ khi lợi ích trùng | Đáng tin **vì** tốn kém |
| Ví dụ | "Sản phẩm chúng tôi tốt nhất" | Bảo hành 10 năm |
| Khi nào hữu ích? | Lợi ích gần trùng nhau | Xung đột lợi ích, bất đối xứng thông tin |

### Khi nào dùng

- Khi cần đánh giá: "Tuyên bố này đáng tin không?" → Hỏi: chi phí nói dối là gì? Nếu zero → coi là cheap talk.
- Khi thiết kế cơ chế: muốn tín hiệu đáng tin → **buộc chi phí phải gắn với kiểu** — bên "tốt" trả ít, bên "xấu" trả đắt.

---

## Lừa phỉnh (Bluffing)

### Mô hình Poker của Von Neumann

Von Neumann chứng minh: **lừa phỉnh tối ưu là toán học, không phải tâm lý**. Trong poker đơn giản:

- Bạn có bài tốt → đặt cược lớn (hiển nhiên).
- Bạn có bài xấu → **đôi khi** đặt cược lớn (bluff).
- Tỷ lệ bluff tối ưu phụ thuộc vào cấu trúc pot odds — không phải "đọc mặt đối thủ".

### Tại sao bluff là cần thiết

Nếu chỉ đặt lớn khi bài tốt → đối phương luôn bỏ khi bạn đặt lớn → bạn không bao giờ thắng lớn. Bluff ép đối phương phải **trả tiền để xác minh** → tăng giá trị khi bạn thực sự có bài tốt.

### Ứng dụng ngoài poker

- **Đàm phán:** Đôi khi phải "ra giá" quyết liệt dù vị thế yếu để đối phương không biết khi nào bạn thực sự mạnh.
- **Kinh doanh:** Startup "giả vờ" lớn hơn thực tế (văn phòng đẹp, sự kiện hoành tráng) để thu hút khách hàng lớn. Chi phí bluff = tiền thuê văn phòng. Nếu thành công → doanh thu bù đủ. Nếu thất bại → mất chi phí.
- **Quân sự:** Nghi binh (deception) — giả tạo dấu hiệu tấn công ở hướng khác. Chi phí: phân tán lực lượng. Lợi ích: đối phương phải bố phòng rải → yếu ở hướng chính.

### Cạm bẫy

- **Bluff quá nhiều → mất uy tín.** Đối phương học pattern → gọi mọi bluff.
- **Bluff khi chi phí bị lộ quá cao.** Nếu bluff thất bại mà hậu quả thảm khốc → tỷ lệ bluff tối ưu phải rất thấp.

---

## Sàng lọc (Screening)

### Định nghĩa

Bên **thiếu thông tin** thiết kế bài test/cơ chế để buộc bên **có thông tin** tự bộc lộ kiểu (type). Khác với tín hiệu (signaling) — ở đó bên có thông tin chủ động gửi.

### Cách thiết kế Sàng lọc

1. Tạo menu lựa chọn (ví dụ: 2 gói sản phẩm).
2. Đảm bảo **tự chọn (self-selection):** kiểu A thích gói 1, kiểu B thích gói 2.
3. Ràng buộc: mỗi kiểu phải thích gói "dành cho mình" hơn gói kia (incentive compatibility).

### Ví dụ: Bảo hiểm

Công ty bảo hiểm không biết ai rủi ro cao, ai rủi ro thấp. Thiết kế 2 gói:
- Gói A: phí thấp, đền bù ít, tự trả phần lớn (high deductible).
- Gói B: phí cao, đền bù nhiều, tự trả ít (low deductible).

Người rủi ro thấp chọn A (ít cần bảo hiểm, tiết kiệm phí). Người rủi ro cao chọn B (cần đền bù, sẵn sàng trả phí cao). Sàng lọc thành công: kiểu tự bộc lộ qua lựa chọn.

---

## Ví dụ Tín hiệu Kinh điển

### Giáo dục như Tín hiệu (Spence, 1973)

**Mô hình:** Bằng đại học có thể không dạy kỹ năng hữu ích — nhưng vẫn có giá trị vì nó là **tín hiệu tốn kém**. Người năng lực cao hoàn thành đại học dễ hơn (chi phí thấp). Người năng lực thấp bỏ cuộc hoặc mất nhiều năm hơn (chi phí cao). Nhà tuyển dụng biết điều này → dùng bằng cấp để sàng lọc.

**Hàm ý gây sốc:** Ngay cả khi đại học dạy **zero** kỹ năng, nó vẫn có giá trị kinh tế thuần túy như thiết bị sàng lọc. Đây là "mô hình tín hiệu" (signaling model) — đối lập với "mô hình vốn nhân lực" (human capital model) cho rằng giáo dục thực sự tăng năng suất.

### Đuôi Công (Peacock Tails)

Đuôi công dài, rực rỡ = gánh nặng sinh tồn. Chỉ con đực khỏe mạnh mới sống sót dù mang đuôi nặng → tín hiệu trung thực về chất lượng gene. Con cái chọn đuôi dài → gene "đuôi dài + khỏe" được truyền lại.

### Chim Chiền chiện Hót (Skylark Singing)

Chiền chiện hót to khi bay lên cao — ngay trước mặt kẻ săn mồi. Tín hiệu cho kẻ săn: "Tôi khỏe đến mức dám lộ vị trí — đừng phí công đuổi." Kẻ săn yếu hơn → bỏ đi → chiền chiện tiết kiệm năng lượng chạy trốn.

### Khi nào dùng

- Khi thấy hành vi "phi lý" trên bề mặt (tốn kém, không cần thiết) → hỏi: "Đây có phải tín hiệu tốn kém?" Nếu chi phí khác nhau theo kiểu → có thể là tín hiệu cân bằng.

---

## Khi Bất đối xứng Thông tin Thay đổi Cấu trúc Trò chơi

### Hiện tượng

Bất đối xứng thông tin không chỉ là "biết ít hơn" — nó có thể **phá hủy thị trường** hoặc **thay đổi hoàn toàn cấu trúc chiến lược**.

### Cơ chế

1. **Chọn lọc Ngược (Adverse Selection):** Bên thiếu thông tin đưa ra mức giá trung bình → bên "tốt" rút lui (giá quá thấp cho họ) → chỉ còn bên "xấu" → giá giảm tiếp → bên "trung bình" rút → vòng xoáy xuống.

2. **Rủi ro Đạo đức (Moral Hazard):** Sau khi ký hợp đồng, bên được bảo hiểm/bảo vệ thay đổi hành vi → rủi ro hơn. Bảo hiểm tạo ra chính rủi ro mà nó bảo vệ.

3. **Thay đổi tập chiến lược:** Khi thêm thông tin bất đối xứng, một trò chơi đơn giản (như phối hợp) có thể trở thành trò chơi tín hiệu phức tạp với nhiều Nash mới.

### Khi nào dùng

- Khi thấy "thị trường không hoạt động" hoặc "không ai muốn giao dịch" → nghi ngờ adverse selection.
- Khi thấy hành vi thay đổi sau khi ký hợp đồng → nghi ngờ moral hazard.

---

## Ví dụ Thực tế

### Phỏng vấn Xin việc

- **Bất đối xứng:** Ứng viên biết năng lực mình, nhà tuyển dụng không.
- **Cheap talk:** "Tôi rất chăm chỉ" → không có chi phí nói dối → kém đáng tin.
- **Costly signal:** Portfolio 10 dự án hoàn chỉnh trên GitHub → tốn hàng trăm giờ → chỉ người thực sự có năng lực mới tạo được.
- **Screening:** Bài test kỹ thuật 3 giờ — người giỏi giải nhanh (chi phí thấp), người kém bỏ cuộc (chi phí cao = mất mặt + thời gian).

### Thị trường Xe cũ (Lemons Problem — Akerlof, 1970)

- **Bất đối xứng:** Người bán biết xe tốt hay xấu, người mua không biết.
- **Adverse selection:** Người mua trả giá trung bình → chủ xe tốt không bán (giá quá thấp) → chỉ xe xấu (lemons) trên thị trường → người mua biết → trả giá thấp hơn → thị trường sụp đổ.
- **Giải pháp thực tế:** Bảo hành (costly signal từ người bán tốt), kiểm định độc lập (screening bởi bên thứ ba), đánh giá trực tuyến (giảm bất đối xứng).

### Thị trường Bảo hiểm

- **Bất đối xứng:** Khách hàng biết rủi ro mình, công ty bảo hiểm không.
- **Adverse selection:** Phí trung bình → người ít rủi ro không mua → pool rủi ro tăng → phí tăng → thêm người rời → death spiral.
- **Screening:** Menu gói bảo hiểm khác nhau (deductible cao/thấp) buộc tự bộc lộ.
- **Moral hazard:** Sau khi mua bảo hiểm, lái xe liều hơn, ít bảo trì hơn.

### Cạm bẫy thường gặp

- **Tin cheap talk khi có xung đột lợi ích.** "Chúng tôi cam kết chất lượng" từ bên bán → không chi phí → không đáng tin. Hỏi: hậu quả nếu nói dối là gì?
- **Nhầm correlation với signaling.** Người giàu mặc đồ hiệu — nhưng đồ hiệu có phải tín hiệu không? Chỉ khi chi phí (giá) khác nhau theo kiểu (giàu vs giả vờ giàu). Nếu đồ giả dễ mua → tín hiệu mất giá trị.
- **Bỏ qua chi phí sàng lọc.** Sàng lọc quá nghiêm → loại cả bên tốt (false negative). Bài test phỏng vấn 8 giờ → ứng viên giỏi có nhiều lựa chọn → bỏ qua công ty bạn.
- **Giả định thông tin là cố định.** Thông tin có thể thu thập, chia sẻ, hoặc che giấu — đây là hành động chiến lược, không phải dữ kiện tĩnh.
