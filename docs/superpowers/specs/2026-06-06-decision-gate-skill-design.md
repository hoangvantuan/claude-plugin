# Decision Gate — Skill Design

Ngày: 2026-06-06
Cập nhật: 2026-06-06 (sau vòng grill, chốt 10 quyết định)
Trạng thái: Đã duyệt thiết kế, sẵn sàng tạo skill

## 1. Mục tiêu

Skill `decision-gate` đóng vai trò trợ lý ra quyết định cho một hạng mục công việc kỹ thuật bất kỳ: Bug, Feature, Techdebt, hoặc Task thường. Input thường mơ hồ (chưa chắc là bug thật, chưa chắc đáng làm), nên skill phải xác minh trước khi kết luận, rồi đưa ra khuyến nghị go/no-go kèm ưu tiên.

Skill dừng ở **bản khuyến nghị** (decision brief). Không tự tạo issue, không tự lập kế hoạch, không gọi skill khác, không gợi ý bước kế.

## 2. Tư thế cốt lõi: không phán xét vội

Nguyên tắc đặt ngay đầu SKILL.md như một anti-pattern guard:

- Input mơ hồ là mặc định. Chưa chắc là bug, chưa chắc đáng làm.
- Cấm kết luận go/no-go trước khi có bằng chứng từ pha xác minh.
- Mọi verdict phải gắn với bằng chứng cụ thể hoặc giả định được ghi rõ.
- Gate chỉ mở (Go) khi giả định **then chốt** đã thành bằng chứng. Giả định **phụ** được phép tồn tại (ghi rõ), nhưng đẩy vào Confidence thấp khi scoring.

## 3. Quyết định thiết kế (đã chốt qua grill)

| # | Vấn đề | Quyết định |
|---|--------|-----------|
| 1 | Trigger / `description` | Go/no-go + ưu tiên cho MỘT hạng mục mơ hồ; xác minh bằng chứng thật; chấm điểm theo loại; dừng ở brief. Không nối sang skill kế |
| 2 | Bản chất pha Research | Lai: cạn nguồn in-repo + runtime read-only trước; thiếu thì hỏi user hoặc ghi giả định |
| 2b | Độ sâu reproduce | Chỉ chạy **read-only**. Tuyệt đối cấm sửa code (skill chỉ phán quyết) |
| 3 | Điểm dừng | Tách 2 loại: hỏi-trong-pha-1 (thu fact, nhiều lần) ≠ checkpoint pha 2 (chốt diễn giải, một lần) |
| 4 | Khung chấm điểm | Map theo loại: Feature→RICE, Bug→ICE, Techdebt→WSJF, Task→ICE |
| 5 | Trục Timing | Bỏ hẳn. Pha 3 chỉ còn Priority → P-level |
| 6 | Output | Mặc định in ra chat; lưu file chỉ khi user yêu cầu |
| 7 | Phân loại | Claude tự gán, nêu tại checkpoint để sửa. Loại chọn khung scoring (vẫn 1 luồng) |
| 8 | Tiêu chí gate | Giả định then chốt chưa verify → không Go. Giả định phụ → Go được, Confidence thấp |
| 9 | Map P-level | P0-P3 neo tiêu chí định tính chung; điểm số chỉ hỗ trợ. Không hard-code ngưỡng |
| 10 | Kết thúc | Dừng tuyệt đối ở brief. Không gợi ý, không gọi skill, không tạo artifact ngoài brief |

## 4. Luồng 3 pha

Một luồng thống nhất áp cho Bug/Feature/Techdebt/Task. Phân loại hạng mục dùng để (a) đặt đúng câu hỏi xác minh và (b) chọn khung chấm điểm ở pha 3. Đây vẫn là **một luồng chung**, không có playbook hay file riêng từng loại: "rẽ nhánh" chỉ là chọn công thức trong cùng `frameworks.md`.

### Pha 1 — Xác minh (research)

Chế độ lai: tự đào trước, bí thì hỏi. Ranh giới đào/hỏi theo **bản chất thông tin**, không theo thời gian.

| Loại thông tin | Hành động |
|---|---|
| Có trong repo (code, `git log`/`git blame`, grep, test, issue/PR sẵn) | Tự đào, bắt buộc. Không hỏi thứ tự đào được |
| Hành vi runtime (reproduce bug) | Chạy test/lệnh **read-only** để verify. **Cấm sửa code.** Nếu reproduce cần sửa/cần env không có → ghi "chưa verify được" + hỏi user đã gặp chưa |
| Context sản phẩm (Reach thật, business impact, ưu tiên chiến lược) | Hỏi user, hoặc đánh dấu giả định. Không bịa |

Hỏi trong pha 1 có thể diễn ra **nhiều lần**, là việc thu thập fact tự nhiên, KHÔNG tính là checkpoint.

Kết quả pha là **Reality check**, nội dung tùy bản chất hạng mục:
- Bug: reproduce được không? Root cause ở đâu?
- Feature / Task: nhu cầu gốc có thật không? Có align mục tiêu không?
- Techdebt: thực sự gây đau không? Đo được cost-of-delay không?

Ghi rõ **giả định** (phân tầng then-chốt vs phụ) và **khoảng trống thông tin**.

### Pha 2 — Cổng Go/No-Go (checkpoint diễn giải, một lần)

Đây là **lần dừng-xác-nhận duy nhất**, khác với việc hỏi-thu-fact ở pha 1. Mục tiêu: chốt *diễn giải*, không phải gom thêm dữ liệu.

- Claude tự **gán loại hạng mục** (bug/feature/techdebt/task) từ bằng chứng pha 1, nêu ngay tại checkpoint để user sửa nếu sai (gộp vào checkpoint, không thêm lần dừng mới).
- Trình **reality-check + danh sách giả định** cho user xác nhận hoặc sửa.
- Verdict, dựa trên độ vững bằng chứng:

| Tình trạng bằng chứng | Verdict |
|---|---|
| Xác minh được (reproduce / nhu cầu gốc có thật / cost đo được) | **Go** → sang pha 3 |
| Phủ định rõ (không reproduce + không ai cần + không đau) | **No-Go** → dừng, xuất brief ghi lý do |
| Giả định **then chốt** chưa verify được | **Cần thêm thông tin** → refine tại cùng checkpoint (đào bổ sung đúng chỗ thiếu rồi trình lại), KHÔNG cho Go |

"Cần thêm thông tin" KHÔNG phải verdict thứ ba ngang hàng, mà là trạng thái refine tại cùng một cổng. Giữ nguyên tắc "checkpoint một lần về khái niệm".

### Pha 3 — Ưu tiên (chỉ khi Go)

Một trục duy nhất: **Priority → P-level**. Không có trục timing.

**Chọn khung theo loại:**

| Loại | Khung | Lý do |
|---|---|---|
| Feature (hướng user) | RICE (Reach × Impact × Confidence ÷ Effort) | Reach có nghĩa thật |
| Bug | ICE (Impact × Confidence × Ease) | Bỏ Reach; Impact = mức đau/tần suất |
| Techdebt | WSJF (Cost-of-Delay ÷ Effort) | Đo "càng để lâu càng đắt" |
| Task / khác | ICE | Nhẹ, đủ dùng |

Hạng mục **lai** (vd "API chậm" vừa bug vừa techdebt): chọn khung theo **quyết định cần ra**, không theo nhãn bề mặt. "Sửa ngay không" → bug → ICE. "Refactor kiến trúc không" → techdebt → WSJF. Ghi rõ đã chọn khung nào và vì sao.

**Map điểm → P-level:** P0-P3 neo vào **tiêu chí định tính chung**, điểm số chỉ là đầu vào hỗ trợ xếp hạng và minh bạch lý do. KHÔNG hard-code ngưỡng số kiểu "RICE>300 = P0".

| P-level | Nghĩa định tính (chung mọi khung) |
|---|---|
| P0 | Đang chảy máu / chặn việc khác / rủi ro nghiêm trọng. Làm ngay |
| P1 | Giá trị cao, rõ ràng đáng làm sớm |
| P2 | Đáng làm, chưa gấp |
| P3 | Biên, làm khi rảnh hoặc gộp dịp khác |

Claude diễn giải điểm + bối cảnh → chốt P-level, ghi rõ lý do (vd: "ICE=320, nhưng là bug chặn checkout của khách → P0 dù điểm chưa cao nhất"). Bảng từng yếu tố vẫn hiện đủ.

Yếu tố cần context sản phẩm (Reach, business Impact) thì hỏi hoặc đánh dấu là giả định (phụ → Confidence thấp).

## 5. Output: Decision Brief

Artifact cuối, markdown theo template. Mặc định **in ra chat**; chỉ lưu file khi user yêu cầu (khi đó: `{CWD}/decision-gate/{ten-hang-muc-slug}-{YYMMDD}.md`).

Các phần:

1. Hạng mục + loại (bug/feature/techdebt/task)
2. Reality check: verified hay chưa, bằng chứng, reproduction/root-cause hoặc need-alignment
3. Verdict: Go / No-Go / Cần thêm thông tin + lý do gắn bằng chứng
4. (nếu Go) Priority: bảng khung (RICE/ICE/WSJF theo loại) + điểm số + P-level + lý do diễn giải
5. Giả định (then chốt / phụ) & khoảng trống thông tin

Không có phần "bước kế tiếp". Skill dừng tại đây: không gợi ý skill khác, không gọi skill, không tạo artifact ngoài brief.

## 6. Cấu trúc file

Theo phương án B (khớp convention repo: `deep-insight`, `systems-thinking`).

```
skills/decision-gate/
  SKILL.md                            # 3 pha + tư thế "không phán xét vội" + checkpoint go/no-go + tiêu chí gate
  references/frameworks.md            # RICE/ICE/WSJF: công thức, map khung↔loại, map điểm→P-level định tính
  references/verification-tactics.md  # mẹo đào bằng chứng theo loại (reproduce read-only, root-cause, đo techdebt, validate need)
  templates/decision-brief.md         # template output
```

SKILL.md giữ gọn, điều phối luồng. Công thức khung và mẹo xác minh tách references để load khi cần. Template brief tách riêng. `frameworks.md` KHÔNG còn Eisenhower và KHÔNG dùng WSJF cho timing; WSJF chỉ dùng cho Priority của techdebt.

## 7. Phạm vi (YAGNI)

Trong phạm vi:
- Xử lý một hạng mục mỗi lần.
- Output là decision brief văn bản.

Ngoài phạm vi (loại bỏ):
- Triage hàng loạt nhiều hạng mục cùng lúc.
- Tự tạo issue, lập kế hoạch, gọi/gợi ý skill khác.
- Playbook riêng từng loại hạng mục.
- Tích hợp issue tracker bên ngoài (chỉ đọc nếu có sẵn trong repo).
- Trục timing (now/next/later) và Eisenhower.
- Sửa code để reproduce (chỉ read-only).

## 8. Việc cập nhật tài liệu khi hoàn thành

Sau khi tạo skill, cập nhật `CLAUDE.md` (phần Structure + bảng chi tiết skill) và `README.md` theo quy tắc Auto-update Documentation của repo.
