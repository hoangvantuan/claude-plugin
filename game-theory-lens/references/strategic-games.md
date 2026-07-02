# Các Nguyên mẫu Trò chơi Chiến lược

## Mục lục

1. [Thế lưỡng nan Tù nhân (Prisoner's Dilemma)](#thế-lưỡng-nan-tù-nhân-prisoners-dilemma)
2. [Trò chơi Gà (Chicken / Hawk-Dove)](#trò-chơi-gà-chicken--hawk-dove)
3. [Săn Hươu (Stag Hunt)](#săn-hươu-stag-hunt)
4. [Cuộc chiến Giới tính (Battle of the Sexes)](#cuộc-chiến-giới-tính-battle-of-the-sexes)
5. [Trò chơi Phối hợp (Coordination Game)](#trò-chơi-phối-hợp-coordination-game)
6. [Đồng xu Đối nghịch (Matching Pennies)](#đồng-xu-đối-nghịch-matching-pennies)
7. [Thế lưỡng nan Tình nguyện (Volunteer's Dilemma)](#thế-lưỡng-nan-tình-nguyện-volunteers-dilemma)
8. [Bảng Chẩn đoán Nguyên mẫu](#bảng-chẩn-đoán-nguyên-mẫu)

---

## Thế lưỡng nan Tù nhân (Prisoner's Dilemma)

### Cấu trúc

|                    | Bob: Hợp tác | Bob: Phản bội |
|--------------------|-------------|--------------|
| **Alice: Hợp tác** | (3, 3)      | (0, 5)       |
| **Alice: Phản bội** | (5, 0)      | (1, 1)       |

Thứ tự lợi ích: **Cám dỗ (T=5) > Phần thưởng (R=3) > Trừng phạt (P=1) > Bị lừa (S=0)**

Điều kiện: T > R > P > S và 2R > T + S (hợp tác thực sự tạo giá trị, không chỉ chuyển từ bên này sang bên kia).

### Phân tích

- **Nash duy nhất:** (Phản bội, Phản bội) — cả hai phản bội bất kể đối phương làm gì.
- **Phản bội là chiến lược trội** cho cả hai bên.
- **Nghịch lý:** Nash (1,1) bị Pareto trội bởi (3,3). Tính duy lý cá nhân dẫn đến kết quả tập thể tồi tệ.

### Tại sao hợp tác thất bại trong trò chơi một lần

Dù cả hai biết (Hợp tác, Hợp tác) tốt hơn, mỗi bên nghĩ: "Nếu đối phương hợp tác, tôi được 5 thay vì 3 khi phản bội. Nếu đối phương phản bội, tôi được 1 thay vì 0 khi phản bội. Dù thế nào, phản bội tốt hơn." Không có cơ chế cam kết → hợp tác sụp đổ.

### Hai phiên bản kinh điển

**Phiên bản Gangster (gốc):** Hai tội phạm bị bắt riêng. Im lặng = hợp tác. Khai = phản bội. Cảnh sát ép mỗi người bằng cách cho deal giảm án.

**Phiên bản Hawk-Dove (sinh học tiến hóa):** Hai con vật tranh lãnh thổ. Dove (nhường) = hợp tác. Hawk (đánh) = phản bội. Nhưng chú ý: Hawk-Dove game chuẩn có cấu trúc khác — xem mục Trò chơi Gà bên dưới.

### Ví dụ thực tế

**Chạy đua vũ trang (Arms Race):** Mỹ và Liên Xô. Giải trừ = hợp tác. Tăng vũ khí = phản bội. Cả hai muốn an ninh bằng vũ khí → cả hai tăng → cả hai kém an toàn hơn và tốn kém hơn. Nash: cả hai chạy đua.

**Chiến tranh giá (Price War):** Hai hãng hàng không trên cùng tuyến. Giữ giá cao = hợp tác. Hạ giá = phản bội. Hạ giá hút khách ngắn hạn nhưng nếu cả hai hạ → lợi nhuận bay hơi. Các hiệp hội ngành (IATA) cố gắng tạo cơ chế duy trì giá — bản chất là giải quyết PD.

**Thỏa thuận khí hậu (Environmental Agreements):** Mỗi quốc gia muốn người khác giảm phát thải trong khi mình tiếp tục công nghiệp hóa. Giảm phát thải = hợp tác. Tiếp tục xả thải = phản bội. Thỏa thuận Paris cố gắng chuyển từ one-shot sang repeated game với cơ chế giám sát.

---

## Trò chơi Gà (Chicken / Hawk-Dove)

### Cấu trúc

|                    | Bob: Nhường | Bob: Không nhường |
|--------------------|-----------|------------------|
| **Alice: Nhường**   | (3, 3)    | (1, 5)           |
| **Alice: Không nhường** | (5, 1)    | (0, 0)           |

Thứ tự: T > R > S > P (khác PD ở chỗ: bị lừa (S=1) vẫn tốt hơn cả hai đâm đầu (P=0)).

### Phân tích

- **2 Nash thuần túy:** (Nhường, Không nhường) và (Không nhường, Nhường) — một bên phải lùi.
- **1 Nash hỗn hợp:** Cả hai ngẫu nhiên hóa với xác suất tính từ payoff.
- **Không có chiến lược trội** — phản ứng tối ưu phụ thuộc đối phương.

### Chính sách Bên miệng Hố (Brinkmanship)

Chiến thuật: **cam kết không nhường trước** để buộc đối phương phải nhường. Cách thực hiện:
- Đốt cầu: loại bỏ lựa chọn nhường (ví dụ: công bố rộng rãi lập trường → mất mặt nếu lùi).
- Tăng rủi ro: không đe dọa trực tiếp mà tạo tình huống nguy hiểm leo thang (Thomas Schelling: "rủi ro vượt khỏi tầm kiểm soát").
- Nguy hiểm: nếu cả hai dùng brinkmanship → cả hai đâm đầu → thảm họa.

### Ví dụ thực tế

**Khủng hoảng Tên lửa Cuba (1962):** Mỹ và Liên Xô. Không nhường = duy trì tên lửa/phong tỏa. Nhường = rút tên lửa/bỏ phong tỏa. Kennedy tạo phong tỏa hải quân (leo thang có kiểm soát). Khrushchev nhường (rút tên lửa) — bù lại Mỹ cam kết không xâm lược Cuba. Kết quả: Nash (Liên Xô nhường, Mỹ không nhường).

**Đối đầu kinh doanh:** Hai công ty cùng tuyên bố ra sản phẩm cùng phân khúc. Thị trường chỉ đủ cho một. Nếu cả hai ra → cả hai lỗ. Ai rút trước → mất chi phí phát triển nhưng sống sót. Bên nào commit nguồn lực công khai hơn (đốt cầu) → bên kia có động cơ rút.

**Đàm phán lương:** Nhân viên đòi tăng hoặc nghỉ. Công ty từ chối hoặc chấp nhận. Nếu cả hai cứng → nhân viên nghỉ, công ty mất người → cả hai thiệt. Ai có BATNA (phương án thay thế) tốt hơn → bên đó "cam kết" đáng tin hơn.

---

## Săn Hươu (Stag Hunt)

### Cấu trúc

|                    | Bob: Hươu | Bob: Thỏ |
|--------------------|----------|---------|
| **Alice: Hươu**    | (5, 5)   | (0, 3)  |
| **Alice: Thỏ**     | (3, 0)   | (3, 3)  |

Thứ tự: R > T ≥ P > S. Hợp tác cho kết quả tốt nhất nhưng đòi hỏi **niềm tin** rằng đối phương cũng hợp tác.

### Phân tích

- **2 Nash thuần túy:** (Hươu, Hươu) — hiệu quả, và (Thỏ, Thỏ) — an toàn.
- **Vấn đề cốt lõi: niềm tin (trust).** Săn hươu cần cả hai cùng tham gia. Nếu nghi ngờ đối phương đi bắt thỏ → bạn cũng đi bắt thỏ để không về tay không.
- **Lưu vực hấp dẫn (Basin of Attraction):** Nash kém hiệu quả (Thỏ, Thỏ) thường có lưu vực hấp dẫn lớn hơn — cần ít hơn 50% quần thể chơi Thỏ để kéo mọi người về Nash này. Đây là lý do xã hội thường mắc kẹt ở cân bằng kém.

### Khác biệt quan trọng với Prisoner's Dilemma

| Tiêu chí | Prisoner's Dilemma | Stag Hunt |
|-----------|-------------------|-----------|
| Hợp tác là Nash? | **Không** | **Có** |
| Vấn đề chính | Động cơ phản bội | Thiếu niềm tin |
| Giải pháp | Cần cơ chế ép buộc | Cần xây dựng lòng tin |
| Chiến lược trội | Có (phản bội) | Không |

### Ví dụ thực tế

**Dự án nhóm:** 5 người cùng làm báo cáo. Nếu tất cả nỗ lực → kết quả xuất sắc (Hươu). Nếu ai đó lo người khác lười → cũng lười theo, làm vừa đủ qua (Thỏ). Một người "bắt thỏ" đủ phá vỡ niềm tin cả nhóm.

**Hợp tác quốc tế:** Các nước ASEAN cùng đầu tư hạ tầng khu vực. Nếu tất cả đầu tư → kết nối mạnh, mọi bên hưởng lợi (Hươu). Nếu nghi nước khác không đầu tư → tự đầu tư nội địa (Thỏ). Cần cơ chế cam kết (hiệp ước, quỹ chung) để chuyển kỳ vọng.

**Áp dụng công nghệ mới:** Chuyển đổi sang tiêu chuẩn mới (ví dụ: IPv6). Nếu tất cả chuyển → lợi ích mạng lớn. Nếu nghi người khác không chuyển → giữ cũ an toàn hơn. Kết quả: kẹt ở IPv4 hàng thập kỷ.

---

## Cuộc chiến Giới tính (Battle of the Sexes)

### Cấu trúc

|                   | Bob: Opera | Bob: Bóng đá |
|-------------------|-----------|-------------|
| **Alice: Opera**   | (3, 2)    | (0, 0)      |
| **Alice: Bóng đá** | (0, 0)    | (2, 3)      |

Cả hai muốn đi cùng nhau nhưng thích hoạt động khác nhau.

### Phân tích

- **2 Nash thuần túy:** (Opera, Opera) và (Bóng đá, Bóng đá).
- **1 Nash hỗn hợp:** Cả hai ngẫu nhiên hóa — nhưng kết quả hỗn hợp tệ hơn cả hai Nash thuần túy (xác suất cao đi lệch nhau).
- **Vấn đề: phối hợp khi sở thích khác nhau.** Ai nhường?

### Điểm tập trung (Focal Point / Schelling Point)

Khi giao tiếp bị hạn chế, các bên dựa vào **quy ước, tiền lệ, hoặc đặc điểm nổi bật** để phối hợp. Thomas Schelling: "Nếu bạn phải gặp ai đó ở New York mà không hẹn trước, bạn đến đâu?" → Grand Central Station lúc 12h trưa. Không có lý do logic — chỉ là điểm nổi bật.

### Ví dụ thực tế

**Cặp vợ chồng chọn nhà hàng.** Cả hai muốn ăn tối cùng nhau nhưng một người thích Nhật, một thích Ý. Tốt hơn là đi cùng nhau đến bất kỳ đâu hơn ăn riêng. Giải pháp: luân phiên, hoặc bên ít quan tâm hơn nhường.

**Hai công ty chọn tiêu chuẩn kỹ thuật.** Cả hai muốn tương thích nhưng mỗi bên muốn tiêu chuẩn mình → tận dụng lợi thế sẵn có. Kết quả: "standards war" (VHS vs Betamax, Blu-ray vs HD DVD).

---

## Trò chơi Phối hợp (Coordination Game / Driving Game)

### Cấu trúc

|                  | Bob: Trái | Bob: Phải |
|------------------|----------|----------|
| **Alice: Trái**   | (1, 1)   | (0, 0)   |
| **Alice: Phải**   | (0, 0)   | (1, 1)   |

Phối hợp thuần túy — không ai thích Trái hơn Phải, chỉ cần **cùng phía**.

### Phân tích

- **2 Nash thuần túy:** (Trái, Trái) và (Phải, Phải).
- Vấn đề duy nhất: **chọn quy ước nào?** Một khi quy ước được thiết lập, cực kỳ ổn định.
- **Chọn quy ước (Convention Selection):** Lịch sử, văn hóa, hoặc quyết định tùy ý ban đầu → quy ước kẹt (lock-in). Anh lái trái, đa số thế giới lái phải — không ai "đúng" hơn ai.

### Ví dụ: Tiêu chuẩn ổ cắm điện

Mỗi quốc gia chọn kiểu ổ cắm. Trong nước: chỉ cần thống nhất. Giữa các nước: thiếu phối hợp → du khách cần adapter. Chi phí chuyển đổi (switching cost) quá cao → kẹt ở quy ước cũ dù có tiêu chuẩn "tốt hơn".

---

## Đồng xu Đối nghịch (Matching Pennies)

### Cấu trúc

|                  | Bob: Ngửa | Bob: Sấp |
|------------------|----------|---------|
| **Alice: Ngửa**   | (1, -1)  | (-1, 1) |
| **Alice: Sấp**    | (-1, 1)  | (1, -1) |

Tổng-không thuần túy. Alice muốn khớp, Bob muốn lệch (hoặc ngược lại).

### Phân tích

- **Không có Nash thuần túy.** Bất kỳ cặp thuần túy nào → một bên có động cơ đổi.
- **Nash hỗn hợp duy nhất:** Cả hai chơi 50-50.
- Đây là mô hình nền tảng cho **tương tác đối đầu thuần túy**: bảo mật vs tấn công, kiểm tra vs gian lận.

### Ví dụ: Kiểm tra thuế ngẫu nhiên

Cơ quan thuế (Alice) muốn bắt trốn thuế. Người nộp thuế (Bob) muốn trốn nếu không bị kiểm tra. Nếu cơ quan kiểm tra tất cả → quá tốn kém. Nếu không kiểm tra → mọi người trốn. Nash hỗn hợp: kiểm tra ngẫu nhiên với tỷ lệ sao cho chi phí trốn thuế kỳ vọng = chi phí nộp thuế.

---

## Thế lưỡng nan Tình nguyện (Volunteer's Dilemma / Good Samaritan Game)

### Cấu trúc (3 người, đơn giản hóa)

Một người cần tình nguyện (chi phí c) để cả nhóm được lợi (giá trị v, v > c). Nếu không ai tình nguyện → tất cả được 0.

### Phân tích

- **Nhiều Nash thuần túy:** Mỗi Nash có đúng một người tình nguyện — nhưng ai?
- **1 Nash hỗn hợp:** Mỗi người tình nguyện với xác suất p. Khi nhóm lớn hơn → p giảm → xác suất **không ai** tình nguyện tăng.
- **Hiệu ứng người ngoài cuộc (Bystander Effect):** Quy mô nhóm tỷ lệ nghịch với xác suất giúp đỡ. Không phải vì người ta vô cảm — mà vì mỗi người nghĩ "chắc ai đó khác sẽ làm."

### Ví dụ thực tế

**Báo cáo sự cố:** Trong công ty 500 người, thấy lỗi bảo mật. Báo cáo mất thời gian (c) nhưng có lợi cho tất cả (v). Ai cũng nghĩ người khác sẽ báo → không ai báo. Giải pháp: chỉ định rõ trách nhiệm (xóa tính ẩn danh).

**Đóng góp mã nguồn mở (Open Source):** Ai cũng dùng, ít người đóng góp. Viết patch tốn công (c), cả cộng đồng hưởng lợi (v). Giải pháp: tài trợ doanh nghiệp, hệ thống credit/danh tiếng.

**Gọi cấp cứu:** Người bị nạn trên đường phố đông. 50 người thấy — mỗi người giả định ai đó đã gọi. Thực nghiệm: càng đông người chứng kiến, thời gian trung bình để ai đó hành động càng dài.

---

## Bảng Chẩn đoán Nguyên mẫu

Khi phân tích tình huống thực tế, dùng bảng sau để xác định nguyên mẫu phù hợp:

| Triệu chứng trong tình huống | Nguyên mẫu có thể | Câu hỏi xác nhận |
|-------------------------------|-------------------|-------------------|
| Mỗi bên có động cơ "ăn gian" dù hợp tác tốt hơn cho tất cả | **Prisoner's Dilemma** | Phản bội có phải chiến lược trội không? |
| Ai lùi trước sẽ "mất mặt" nhưng đâm đầu cả hai thì thảm họa | **Chicken** | Kết quả cả hai cứng đầu có tệ nhất không? |
| Hợp tác cho kết quả tốt nhất nhưng rủi ro nếu đối tác không hợp tác | **Stag Hunt** | Có tồn tại lựa chọn "an toàn" cho kết quả vừa phải không? |
| Cả hai muốn phối hợp nhưng thích phương án khác nhau | **Battle of the Sexes** | Đi riêng có tệ hơn đi cùng theo phương án mình không thích? |
| Chỉ cần thống nhất, không ai thích phương án nào hơn | **Coordination Game** | Lợi ích chỉ phụ thuộc vào "cùng phe" không? |
| Một bên muốn đoán đúng, bên kia muốn tránh bị đoán | **Matching Pennies** | Đây có phải đối đầu tổng-không thuần túy? |
| Ai đó cần hy sinh cho nhóm, nhưng không ai muốn là người đó | **Volunteer's Dilemma** | Nhóm càng lớn, ai cũng càng chờ đợi người khác? |

### Cạm bẫy chung khi chọn nguyên mẫu

- **Mọi thứ đều là Prisoner's Dilemma?** Không. Nhiều tình huống là Stag Hunt (vấn đề niềm tin, không phải động cơ phản bội) hoặc Chicken (vấn đề ai nhường, không phải ai phản bội). Kiểm tra: phản bội có phải chiến lược trội không? Nếu không → không phải PD.
- **Bỏ qua tính lặp lại.** Tình huống one-shot khác hoàn toàn với tương tác lặp. Cùng cấu trúc PD nhưng lặp vô hạn → hợp tác có thể là Nash (xem repeated-games-trust.md).
- **Giả định chỉ có 2 bên.** Nhiều tình huống có n bên → cấu trúc thay đổi đáng kể (Volunteer's Dilemma thay đổi theo n, PD nhiều bên = Bi kịch của Công hữu).
- **Lẫn lộn lợi ích với tiền.** Gán payoff sai vì chỉ tính tiền → chọn sai nguyên mẫu. Luôn hỏi: "Bên này thực sự muốn gì?" trước khi gán số.
