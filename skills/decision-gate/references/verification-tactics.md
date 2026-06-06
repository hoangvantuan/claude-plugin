# Verification Tactics — Mẹo đào bằng chứng theo loại

Tài liệu này dùng ở **pha 1**. Mục tiêu: biến giả định thành bằng chứng bằng những gì đào được trong repo và runtime read-only, trước khi phải hỏi user.

Nguyên tắc đỏ xuyên suốt: **chỉ read-only.** Skill này phán quyết, không sửa. Tuyệt đối không edit code, không chạy lệnh thay đổi state (migration, ghi DB, deploy). Nếu xác minh đòi hỏi thay đổi → dừng đào, ghi "chưa verify được" + hỏi user.

## Thứ tự chung: đào repo → thử runtime read-only → hỏi user

1. **Đào repo trước** (bắt buộc, đừng hỏi thứ tự đào được).
2. **Thử runtime read-only** nếu cần xác minh hành vi.
3. **Hỏi user** chỉ cho thứ không nằm trong repo/runtime: context sản phẩm, Reach thật, đã từng gặp lỗi chưa.

## Bug — reproduce được không? Root cause ở đâu?

**Đào repo:**

- `git log` / `git blame` quanh vùng nghi ngờ: thay đổi gần đây nào có thể gây lỗi? Ai sửa, vì sao (đọc commit message, PR)?
- grep thông điệp lỗi, tên hàm, mã lỗi để định vị code path.
- Tìm test sẵn có liên quan: có test nào đang fail/skip/xfail mô tả đúng lỗi này không?
- Tìm issue/PR đã mở trong repo nói về cùng triệu chứng.

**Thử runtime (read-only):**

- Chạy test suite hoặc test đơn lẻ liên quan để xem lỗi có tái hiện không.
- Chạy lệnh quan sát: log, trace, health-check, dry-run flag nếu có.
- **Nếu reproduce cần sửa code, dựng env không có, hoặc cần dữ liệu production** → ghi "chưa verify được", hỏi user: "Bạn đã gặp lỗi này chưa? Trong tình huống/bước nào, môi trường nào?"

**Phân biệt triệu chứng vs root cause:** lỗi hiện ở A không có nghĩa nguyên nhân ở A. Lần ngược chuỗi gọi tới nơi state bắt đầu sai. Root cause là chỗ mà sửa vào đó thì lớp triệu chứng biến mất, không phải chỗ exception nổ ra.

**Giả định then chốt điển hình của bug:** "lỗi này thật sự xảy ra (không phải hiểu nhầm)". Treo giả định này thì không được Go.

## Feature / Task — nhu cầu gốc có thật không? Có align không?

**Đào repo:**

- Có code/feature flag/TODO cũ cho thấy việc này từng được cân nhắc không?
- Tài liệu trong repo (README, docs, ADR) có nêu mục tiêu sản phẩm để đối chiếu align không?

**Hỏi user (context sản phẩm không đào được):**

- Nhu cầu gốc là gì? Ai cần, cần để giải quyết vấn đề nào? (Phân biệt "user xin tính năng X" vs "user thật sự cần giải quyết Y").
- Đã có cách workaround nào chưa? Nếu có rồi thì nhu cầu thật sự cấp tới đâu?
- Reach thật (bao nhiêu người dùng tới) — số liệu hay phỏng đoán?

**Bẫy thường gặp:** nhầm giải pháp được đề xuất với nhu cầu gốc. Hỏi "vấn đề thật phía sau yêu cầu này là gì?" trước khi đánh giá đáng làm hay không.

**Giả định then chốt điển hình:** "có người thật sự cần cái này" và "nó align mục tiêu hiện tại". Treo thì không Go.

## Techdebt — thực sự gây đau không? Đo được cost-of-delay không?

**Đào repo:**

- `git log` vùng debt: tần suất phải đụng vào đó (churn). Code đụng càng nhiều, debt càng đau.
- Dấu vết đau: số lần bug lặp quanh vùng này, số TODO/FIXME/HACK, độ phức tạp.
- Có chỗ nào đang phải workaround vì debt này không?

**Đo cost-of-delay (cho WSJF):**

- Để nguyên thì cái gì bị bào mòn (tốc độ dev, độ ổn định, rủi ro bảo mật)?
- Có ngưỡng vỡ không (vd thư viện sắp hết hỗ trợ, giới hạn scale sắp chạm)?
- Trả debt này có mở khóa việc khác không?

**Bẫy thường gặp:** "code xấu" không tự động là debt đáng trả. Debt chỉ đáng khi nó **đang gây đau đo được** hoặc **sắp gây đau**. Code xấu trong góc không ai đụng tới = ưu tiên thấp dù nhìn gai mắt.

**Giả định then chốt điển hình:** "debt này đang/sắp gây đau thật". Nếu chỉ là "trông xấu" mà không đo được đau → giả định then chốt treo → không Go (hoặc No-Go nếu rõ ràng không đau).

## Ghi nhận giả định và khoảng trống

Sau khi đào, mọi thứ chưa thành bằng chứng phải vào một trong hai sổ:

- **Giả định** (gắn nhãn then chốt / phụ): điều đang tạm coi là đúng để tiếp tục. Then chốt = sai thì đảo verdict. Phụ = ảnh hưởng độ chính xác điểm số.
- **Khoảng trống thông tin**: điều chưa biết và chưa đào/hỏi ra được, cần nêu rõ trong brief để user tự cân nhắc.

Không bao giờ lấp khoảng trống bằng phỏng đoán trình bày như sự thật.
