# Trò chơi Lặp lại và Niềm tin

## Mục lục

1. [Phân loại Trò chơi Lặp lại](#phân-loại-trò-chơi-lặp-lại)
2. [Nghịch lý Lặp hữu hạn (Finite Repetition Paradox)](#nghịch-lý-lặp-hữu-hạn)
3. [Định lý Dân gian (Folk Theorem)](#định-lý-dân-gian-folk-theorem)
4. [Các Chiến lược Lặp Kinh điển](#các-chiến-lược-lặp-kinh-điển)
5. [Giải đấu Axelrod](#giải-đấu-axelrod)
6. [Trừng phạt Tỷ lệ vs Bất tỷ lệ](#trừng-phạt-tỷ-lệ-vs-bất-tỷ-lệ)
7. [Danh tiếng và Niềm tin như Hiện tượng Cân bằng](#danh-tiếng-và-niềm-tin)
8. [Khi nào Hợp tác Sụp đổ](#khi-nào-hợp-tác-sụp-đổ)
9. [Thỏa thuận Tự kiểm soát (Self-policing Agreements)](#thỏa-thuận-tự-kiểm-soát)
10. [Ví dụ Thực tế](#ví-dụ-thực-tế)

---

## Phân loại Trò chơi Lặp lại

### Ba loại

| Loại | Mô tả | Hợp tác bền vững? |
|------|--------|-------------------|
| Một lần (One-shot) | Chơi đúng 1 lần, không gặp lại | Rất khó — không có "bóng của tương lai" |
| Lặp hữu hạn (Finitely repeated) | Biết chính xác số vòng (ví dụ: 10 vòng) | Nghịch lý: lý thuyết nói không, thực tế thì có |
| Lặp vô hạn/bất định (Indefinitely repeated) | Không biết khi nào kết thúc, xác suất tiếp tục δ | Có — nếu δ đủ lớn (đủ kiên nhẫn) |

### Hệ số Chiết khấu (Discount Factor) δ

δ = xác suất trò chơi tiếp tục sau mỗi vòng (hoặc mức kiên nhẫn). δ = 0.9 → 90% khả năng gặp lại. δ càng cao → "bóng của tương lai" càng dài → hợp tác càng dễ duy trì.

### Khi nào dùng

- Khi tương tác không phải one-shot: đồng nghiệp, đối tác kinh doanh, láng giềng, quốc gia.
- Khi cần đánh giá: "Tình huống này có đủ 'tương lai' để hợp tác bền vững không?"

---

## Nghịch lý Lặp hữu hạn

### Backward Induction (Quy nạp Ngược)

Xét Thế lưỡng nan Tù nhân lặp 10 vòng, cả hai biết đúng 10 vòng:

1. **Vòng 10 (cuối):** Không có vòng sau → giống one-shot → cả hai phản bội.
2. **Vòng 9:** Biết vòng 10 sẽ phản bội → không lý do hợp tác vòng 9 → phản bội.
3. **Vòng 8:** Biết vòng 9-10 phản bội → phản bội...
4. **Suy ngược đến vòng 1:** Phản bội ngay từ đầu.

### Kết luận lý thuyết

Trong PD lặp hữu hạn với bên chơi hoàn toàn duy lý và hiểu biết chung về tính duy lý → **hợp tác không bao giờ xảy ra**. Backward induction "tháo rời" hợp tác từ cuối ngược lên.

### Thực tế khác lý thuyết

Thí nghiệm cho thấy: con người **vẫn hợp tác** trong PD lặp hữu hạn, đặc biệt ở các vòng đầu. Hợp tác giảm dần khi gần vòng cuối. Giải thích:
- Không chắc đối phương hoàn toàn duy lý → duy trì hợp tác "đề phòng".
- Tư duy "reputation" (danh tiếng) — dù lý thuyết nói không cần.
- Bounded rationality (tính duy lý giới hạn) — không ai thực sự suy ngược 100 vòng.

### Khi nào dùng

- Khi tình huống có **điểm kết thúc rõ ràng** → cảnh giác với hiệu ứng endgame (xem bên dưới).
- Khi ai đó lập luận "chúng ta sẽ gặp lại" → kiểm tra: có biết chính xác bao nhiêu lần không?

---

## Định lý Dân gian (Folk Theorem)

### Phát biểu (đơn giản hóa)

Trong trò chơi lặp vô hạn, **bất kỳ kết quả nào cho mỗi bên lợi ích ≥ mức tối thiểu đảm bảo (minimax)** đều có thể là Nash Equilibrium — miễn là δ đủ lớn (bên chơi đủ kiên nhẫn).

### Minimax là gì?

Mức minimax = lợi ích tối thiểu mà bên A đảm bảo được **dù đối phương cố gắng hại A nhất**. Trong PD: minimax = P (lợi ích khi cả hai phản bội), vì nếu bạn phản bội, tệ nhất bạn được P.

### Hàm ý thực tế

- **Tin tốt:** Hợp tác (R, R) có thể bền vững trong trò chơi lặp — thậm chí trong PD!
- **Tin xấu:** Rất nhiều kết quả khác cũng có thể bền vững → Folk Theorem dự đoán quá nhiều, không đủ sắc để chỉ ra kết quả "đúng".
- **Tin thực dụng:** Folk Theorem nói "hợp tác **có thể** bền vững" — nhưng không nói "hợp tác **sẽ** xảy ra". Cần chiến lược cụ thể để duy trì.

### Khi nào dùng

- Khi cần lập luận: "Liệu hợp tác có thể duy trì trong tương tác dài hạn này?" → Kiểm tra δ và minimax.
- Khi đánh giá cơ chế: "Phạt có đủ nặng để ngăn phản bội không?" → So sánh lợi ích phản bội ngắn hạn vs chi phí bị phạt dài hạn.

---

## Các Chiến lược Lặp Kinh điển

### GRIM (Trừng phạt Vĩnh viễn / Grim Trigger)

**Quy tắc:** Hợp tác cho đến khi đối phương phản bội lần đầu. Sau đó phản bội **vĩnh viễn**.

| Ưu điểm | Nhược điểm |
|----------|------------|
| Đe dọa mạnh nhất — trừng phạt tối đa | Không tha thứ — 1 lỗi phá vỡ vĩnh viễn |
| Đơn giản, dễ hiểu | Nếu có "nhiễu" (lỡ tay phản bội) → hợp tác chết |
| Nash Equilibrium (nếu δ đủ lớn) | Trong thực tế quá cứng nhắc — không ai dùng |

### TIT-FOR-TAT (Ăn Miếng Trả Miếng)

**Quy tắc:** Bắt đầu hợp tác. Sau đó **sao chép nước đi cuối** của đối phương.

| Ưu điểm | Nhược điểm |
|----------|------------|
| Tốt bụng (nice) — không phản bội trước | Bị khai thác bởi chiến lược luân phiên (Hợp tác/Phản bội xen kẽ) |
| Trả đũa (retaliatory) — phạt ngay khi bị phản bội | "Echo effect" — 1 lần phản bội tạo vòng lặp trả đũa |
| Tha thứ (forgiving) — quay lại hợp tác ngay khi đối phương hợp tác | Không khoan dung với nhiễu — sai 1 bước → chuỗi Phản bội-Hợp tác-Phản bội |
| Rõ ràng (clear) — đối phương dễ hiểu pattern | |

### TIT-FOR-TWO-TATS (Nhẫn nhịn hơn)

**Quy tắc:** Chỉ phản bội sau khi đối phương phản bội **2 lần liên tiếp**. Tha thứ hơn TFT, chống nhiễu tốt hơn, nhưng dễ bị khai thác hơn.

### TAT-FOR-TIT (Phản trước, Sửa sau)

**Quy tắc:** Bắt đầu phản bội. Sau đó sao chép nước đi cuối đối phương. Kiểm tra đối phương trước — nếu đối phương "mạnh" (trả đũa) → chuyển sang hợp tác. Nếu yếu → tiếp tục khai thác.

### Win-Stay, Lose-Shift (Pavlov)

**Quy tắc:** Nếu kết quả vòng trước "tốt" (R hoặc T) → giữ nguyên. Nếu "xấu" (P hoặc S) → đổi. Tự sửa lỗi — nếu cả hai phản bội (P) → cả hai đổi → cả hai hợp tác (R) → ổn định.

---

## Giải đấu Axelrod

### Bối cảnh

Robert Axelrod (1984) tổ chức giải đấu: mời các nhà lý thuyết trò chơi gửi chiến lược cho PD lặp lại. Mỗi chiến lược đấu với mọi chiến lược khác qua nhiều vòng. Tổng điểm xác định thứ hạng.

### Kết quả đáng kinh ngạc

**TIT-FOR-TAT thắng** — chiến lược đơn giản nhất trong số được gửi. Axelrod tổ chức giải lần 2, mọi người biết kết quả lần 1 → TIT-FOR-TAT **lại thắng**.

### Bốn tính chất của chiến lược thành công

| Tính chất | Mô tả | Tại sao quan trọng |
|-----------|--------|---------------------|
| **Tốt bụng (Nice)** | Không bao giờ phản bội trước | Tránh vòng xoáy trả đũa không cần thiết |
| **Trả đũa (Retaliatory)** | Phạt ngay khi bị phản bội | Ngăn bị khai thác |
| **Tha thứ (Forgiving)** | Quay lại hợp tác khi đối phương quay lại | Thoát vòng xoáy trả đũa |
| **Rõ ràng (Clear)** | Đối phương dễ hiểu pattern | Đối phương nhanh chóng học: hợp tác với TFT là tốt nhất |

### Bài học

- Chiến lược "ranh mãnh" (cố khai thác, lợi dụng) thua dài hạn.
- Chiến lược "quá hiền" (luôn hợp tác bất kể) cũng thua — bị khai thác.
- **Chiến lược tốt nhất: tốt bụng nhưng không ngây thơ.**

---

## Trừng phạt Tỷ lệ vs Bất tỷ lệ

### Trừng phạt Tỷ lệ (Proportional Punishment)

Phạt **vừa đủ** để ngăn vi phạm. Ví dụ: TIT-FOR-TAT — phản bội 1 vòng cho mỗi lần bị phản bội.

### Trừng phạt Bất tỷ lệ (Disproportionate Punishment)

Phạt **nặng hơn** vi phạm. Ví dụ: GRIM — phản bội vĩnh viễn cho 1 lần vi phạm.

### So sánh

| Tiêu chí | Tỷ lệ | Bất tỷ lệ |
|----------|--------|-----------|
| Sức đe dọa | Vừa đủ | Rất mạnh |
| Khoan dung với sai lầm | Cao — phục hồi nhanh | Thấp — 1 lỗi = thảm họa |
| Đáng tin (credible)? | Có — phạt không tốn nhiều | Đôi khi không — phạt nặng cũng hại người phạt |
| Chống nhiễu | Tốt | Rất kém |

### Khi nào dùng

- **Tỷ lệ:** Khi tương tác dài hạn, có khả năng sai lầm/nhiễu, quan hệ đáng duy trì.
- **Bất tỷ lệ:** Khi cần răn đe mạnh, hành vi dễ quan sát (ít nhiễu), quan hệ có thể hy sinh.

### Cạm bẫy

- **"Bắn chim sẻ bằng đại bác" (Nuclear option cho vi phạm nhỏ).** Nếu phạt không đáng tin (vì quá tốn kém để thực hiện) → đe dọa suông → không có tác dụng răn đe.
- **Không phạt đủ.** Nếu lợi ích phản bội > chi phí bị phạt tỷ lệ → phạt tỷ lệ không đủ → cần tăng.

---

## Danh tiếng và Niềm tin

### Danh tiếng như Hiện tượng Cân bằng

Danh tiếng không phải "tài sản" trừu tượng — nó là **niềm tin của đối phương về kiểu (type) của bạn**, được cập nhật qua hành vi quan sát được. Trong cân bằng:

- Bên có danh tiếng tốt → đối phương hợp tác → lợi ích dài hạn.
- Chi phí duy trì danh tiếng = lợi ích ngắn hạn bị mất do không phản bội.
- Danh tiếng có giá trị **vì** người khác phạt bạn khi mất danh tiếng (ngừng hợp tác).

### Xây dựng Niềm tin

| Phương pháp | Cơ chế | Ví dụ |
|-------------|--------|-------|
| Cam kết nhỏ trước, lớn sau | Rủi ro tăng dần, mỗi bước xác minh | Đối tác kinh doanh bắt đầu từ đơn hàng nhỏ |
| Đầu tư không thu hồi (Sunk cost) | "Đốt cầu" — cam kết đáng tin vì đã trả chi phí | Xây nhà máy gần nhà cung cấp |
| Minh bạch | Giảm bất đối xứng thông tin → giảm nhu cầu niềm tin | Mã nguồn mở, sổ sách công khai |
| Con tin (Hostage) | Gửi tài sản có giá trị cho bên kia giữ | Deposit, collateral, escrow |

---

## Khi nào Hợp tác Sụp đổ

### Hiệu ứng Vịt què (Lame Duck Effect)

Khi biết tương tác sắp kết thúc → mất động cơ duy trì danh tiếng. Ví dụ: tổng thống nhiệm kỳ cuối, CEO sắp nghỉ hưu, nhân viên đã nộp đơn từ chức. Đối phương biết → ngừng hợp tác trước → backward induction bắt đầu.

### Ẩn danh (Anonymity)

Nếu không ai biết bạn là ai → danh tiếng vô giá trị → không có cơ chế phạt → hợp tác sụp đổ. Đây là lý do:
- Giao dịch ẩn danh trên internet cần cơ chế bên thứ ba (escrow, đánh giá).
- Mạng xã hội ẩn danh toxic hơn mạng thật danh.
- Tội phạm có tổ chức hoạt động trong cộng đồng nhỏ (không ẩn danh) → duy trì "danh tiếng" nội bộ.

### Hiệu ứng Cuối trò (Endgame Effect)

Rộng hơn lame duck: bất kỳ khi nào xác suất tương tác tương lai giảm đáng kể (δ giảm), hợp tác lung lay. Ví dụ:
- Công ty sắp phá sản → nhà cung cấp đòi thanh toán ngay (không tin tương lai).
- Ngành hàng suy thoái → doanh nghiệp cạnh tranh quyết liệt hơn (ít tương lai để bảo vệ).

### Thay đổi Bên chơi (Player Turnover)

Nếu "bên chơi" thay đổi (nhân viên mới, lãnh đạo mới, thế hệ mới) → danh tiếng tích lũy bị reset. Bên mới có thể không cảm thấy ràng buộc bởi thỏa thuận cũ → cần cơ chế chuyển giao danh tiếng (thương hiệu tổ chức, hợp đồng pháp lý).

---

## Thỏa thuận Tự kiểm soát (Self-policing Agreements)

### Định nghĩa

Thỏa thuận mà **mỗi bên tự nguyện tuân thủ** vì vi phạm dẫn đến mất lợi ích tương lai — không cần bên thứ ba (tòa án, cảnh sát) cưỡng chế.

### Điều kiện cần

1. **Tương tác lặp lại** với δ đủ lớn.
2. **Hành vi quan sát được** — phải biết ai vi phạm.
3. **Cơ chế phạt đáng tin** — bên phạt thực sự sẵn sàng phạt (phạt không quá tốn kém cho người phạt).
4. **Lợi ích tuân thủ dài hạn > lợi ích vi phạm ngắn hạn.**

### Khi nào dùng

- Khi không có cơ chế cưỡng chế bên ngoài (hợp đồng quốc tế, thỏa thuận phi chính thức).
- Khi cần đánh giá: "Thỏa thuận này có tự bền vững không?" → Kiểm tra 4 điều kiện.

### Thiết kế thỏa thuận tự kiểm soát

**Bước 1:** Xác định Nash Equilibrium của trò chơi one-shot (kết quả nếu không có thỏa thuận).

**Bước 2:** Xác định kết quả mong muốn (thường Pareto tốt hơn Nash one-shot).

**Bước 3:** Thiết kế cơ chế phạt — gì xảy ra khi ai đó vi phạm? Quay về Nash one-shot bao nhiêu vòng?

**Bước 4:** Tính δ tối thiểu — δ phải đủ lớn để: giá trị hiện tại của tuân thủ vĩnh viễn > giá trị phản bội 1 lần + bị phạt sau đó.

**Bước 5:** Kiểm tra tính khả quan — δ thực tế có đủ lớn không? Hành vi có quan sát được không?

---

## Ví dụ Thực tế

### Thị trường Kim cương Antwerp

**Bối cảnh:** Trung tâm giao dịch kim cương Antwerp (Bỉ). Các thương gia giao dịch kim cương trị giá hàng triệu đô — thường bằng **cái bắt tay**, không hợp đồng văn bản.

**Cơ chế:**
- Cộng đồng nhỏ, khép kín (chủ yếu người Do Thái Orthodox) → không ẩn danh.
- Danh tiếng lan truyền tức thì trong cộng đồng → gian lận 1 lần = mất sự nghiệp.
- Tương tác lặp vô hạn (gia đình truyền nghề nhiều thế hệ) → δ rất cao.
- Cơ chế phạt: tẩy chay tập thể (multilateral punishment) → chi phí gian lận cực cao.

**Phân tích:** Thỏa thuận tự kiểm soát hoàn hảo. Điều kiện: cộng đồng nhỏ + thông tin minh bạch + tương lai dài. Khi cộng đồng mở rộng cho người ngoài → niềm tin giảm → cần hợp đồng pháp lý.

### Quan hệ Chủ - Nhân viên

**Bối cảnh:** Chủ trả lương, nhân viên nỗ lực. Nỗ lực khó đo lường chính xác (moral hazard).

**Cơ chế lặp lại:**
- Nhân viên nỗ lực → thăng tiến, tăng lương → tiếp tục nỗ lực (cân bằng hợp tác).
- Nhân viên lười → không thăng tiến, có thể bị sa thải → chi phí mất việc ngăn lười.
- Chủ công bằng → giữ nhân viên giỏi → lợi ích dài hạn.
- Chủ bóc lột → nhân viên giỏi nghỉ → mất nhân tài.

**Khi hợp tác sụp đổ:**
- Nhân viên biết sắp bị layoff → lame duck → nỗ lực giảm.
- Công ty sắp phá sản → không có tương lai → nhân viên tìm việc mới, không đầu tư.
- Ngành hot, nhiều cơ hội → nhân viên ít sợ mất việc (δ thấp vì dễ tìm việc khác) → cần tăng lương/phúc lợi để duy trì.

### Nghĩa vụ Liên thế hệ (Intergenerational Duties)

**Bối cảnh:** Thế hệ hiện tại dùng tài nguyên, thế hệ tương lai chịu hậu quả. Đây là PD liên thế hệ.

**Vấn đề:**
- Thế hệ tương lai **không thể phạt** thế hệ hiện tại → không có cơ chế tự kiểm soát.
- δ giữa các thế hệ thấp — người sống hôm nay ít quan tâm lợi ích người 100 năm sau.
- Backward induction: thế hệ cuối cùng (nếu có) không cần quan tâm → thế hệ trước đó cũng không → ... sụp đổ.

**Giải pháp thực tế:**
- Thể chế dài hạn (hiến pháp, quỹ tín thác) — ràng buộc hành vi hiện tại.
- Giá trị văn hóa (đạo hiếu, legacy) — tạo utility cho việc "để lại di sản".
- Tổ chức đại diện thế hệ tương lai (environmental agencies, endowment funds).

### Tuân thủ Thuế (Tax Compliance)

**Bối cảnh:** Nộp thuế là PD nhiều bên — mỗi cá nhân muốn trốn trong khi người khác nộp.

**Cơ chế lặp lại:**
- Kiểm tra ngẫu nhiên (mixed strategy của cơ quan thuế) → xác suất bị phát hiện > 0.
- Phạt nặng nếu bị bắt → tăng chi phí kỳ vọng của gian lận.
- Danh tiếng xã hội: ở xã hội nhỏ, trốn thuế bị xem thường → phạt xã hội bổ sung.

**Khi tuân thủ sụp đổ:**
- Nếu mọi người tin "ai cũng trốn" → tâm lý "mình trốn cũng không sao" → vòng xoáy xuống.
- Nếu chính phủ dùng thuế lãng phí → người dân cảm thấy bị lừa → giảm tuân thủ tự nguyện.
- Nếu xác suất kiểm tra quá thấp (ngân sách cơ quan thuế bị cắt) → chi phí kỳ vọng gian lận giảm → trốn thuế tăng.

**Bài học:** Tuân thủ thuế là cân bằng xã hội (social equilibrium) — cần duy trì cả cơ chế phạt lẫn niềm tin rằng "hầu hết mọi người tuân thủ". Mất một trong hai → equilibrium chuyển.

---

## Cạm bẫy Thường gặp trong Phân tích Trò chơi Lặp

### 1. Giả định δ cao khi thực tế thấp
Mối quan hệ "dài hạn" trên danh nghĩa có thể có δ thấp vì: thay đổi nhân sự, thay đổi thị trường, hoặc một bên có nhiều lựa chọn thay thế. Luôn hỏi: "Khả năng tương tác tiếp theo thực sự là bao nhiêu?"

### 2. Bỏ qua vấn đề quan sát
Folk Theorem giả định **hành vi quan sát được**. Nếu không thể biết ai vi phạm → không thể phạt ai → hợp tác sụp đổ dù δ = 1. Trong thực tế: đo lường hiệu quả không hoàn hảo, hành vi có noise.

### 3. Phạt không đáng tin (Not Credible Punishment)
Tuyên bố "sẽ phạt nặng" nhưng phạt cũng gây hại cho người phạt → đối phương biết bạn sẽ không phạt → đe dọa suông. GRIM trong thực tế thường không đáng tin: "Bạn thực sự sẽ hủy quan hệ triệu đô vì lỗi nhỏ?"

### 4. Nhầm hợp tác trong PD lặp với hợp tác trong one-shot
Hợp tác bền vững trong PD lặp **không** có nghĩa là hợp tác tốt trong one-shot. Tình huống one-shot thực sự (gặp người lạ, giao dịch 1 lần) → vẫn nên kỳ vọng phản bội.

### 5. Quên hiệu ứng endgame
Dù tương tác "dài hạn", nếu ai đó **biết** mình sắp rời (nghỉ hưu, chuyển công ty, di cư) → δ cá nhân giảm → hành vi thay đổi trong giai đoạn cuối. Thiết kế cơ chế cần tính đến điều này (ví dụ: vesting schedule, deferred compensation).
