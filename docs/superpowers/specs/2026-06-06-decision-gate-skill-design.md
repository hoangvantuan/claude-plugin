# Decision Gate — Skill Design

Ngày: 2026-06-06
Trạng thái: Đã duyệt thiết kế, chờ review spec

## 1. Mục tiêu

Skill `decision-gate` đóng vai trò trợ lý ra quyết định cho một hạng mục công việc kỹ thuật bất kỳ: Bug, Feature, Techdebt, hoặc Task thường. Input thường mơ hồ (chưa chắc là bug thật, chưa chắc đáng làm), nên skill phải xác minh trước khi kết luận, rồi đưa ra khuyến nghị go/no-go kèm ưu tiên và thời điểm.

Skill dừng ở **bản khuyến nghị** (decision brief). Không tự tạo issue, không tự lập kế hoạch, không bàn giao sang skill khác.

## 2. Tư thế cốt lõi: không phán xét vội

Nguyên tắc đặt ngay đầu SKILL.md như một anti-pattern guard:

- Input mơ hồ là mặc định. Chưa chắc là bug, chưa chắc đáng làm.
- Cấm kết luận go/no-go trước khi có bằng chứng từ pha xác minh.
- Mọi verdict phải gắn với bằng chứng cụ thể hoặc giả định được ghi rõ.

## 3. Quyết định thiết kế (đã chốt với user)

| # | Vấn đề | Quyết định |
|---|--------|-----------|
| 1 | Bản chất pha Research | Lai: mặc định tự đào dữ liệu thật (codebase, git, test, issue); thiếu nguồn thì hỏi user |
| 2 | Điểm kết thúc | Dừng ở khuyến nghị (decision brief). Không tạo issue/plan |
| 3 | Khung chấm điểm | Khung chuẩn có tên: RICE/ICE cho ưu tiên, Eisenhower/WSJF cho thời điểm. Điểm số minh bạch |
| 4 | Xử lý theo loại | Một luồng thống nhất cho mọi loại; Claude tự điều chỉnh câu hỏi theo ngữ cảnh |
| 5 | Cách tương tác | Tự động chạy research + scoring, dừng đúng 1 lần ở ranh giới go/no-go để user xác nhận giả định |

## 4. Luồng 3 pha

Một luồng thống nhất áp cho Bug/Feature/Techdebt/Task. Phân loại hạng mục chỉ để đặt đúng câu hỏi, không rẽ nhánh thành playbook riêng.

### Pha 1 — Xác minh (research)

Chế độ lai: tự đào trước, bí thì hỏi.

- Thu bằng chứng thật: đọc codebase, `git log` / `git blame`, grep, chạy test hoặc reproduce, tìm issue/PR liên quan.
- Khi thiếu nguồn (không trong repo, không có issue tracker, cần context sản phẩm): chuyển sang hỏi user.
- Kết quả pha là **Reality check**, nội dung tùy bản chất hạng mục:
  - Bug: reproduce được không? Root cause ở đâu?
  - Feature / Task: nhu cầu gốc có thật không? Có align mục tiêu không?
  - Techdebt: thực sự gây đau không? Đo được cost-of-delay không?
- Ghi rõ **giả định** và **khoảng trống thông tin**.

### Pha 2 — Cổng Go/No-Go (điểm chốt xác nhận duy nhất)

- Tổng hợp bằng chứng thành verdict: **Go / No-Go / Cần thêm thông tin**, kèm lý do gắn bằng chứng.
- Đây là lần dừng duy nhất: trình reality-check + danh sách giả định cho user xác nhận hoặc sửa, trước khi sang scoring.
- Nếu No-Go hoặc Cần thêm thông tin: dừng, không scoring.

### Pha 3 — Ưu tiên & Thời điểm (chỉ khi Go)

- **Ưu tiên:** RICE (Reach, Impact, Confidence, Effort); case nhẹ dùng ICE. Bảng minh bạch từng yếu tố kèm cơ sở (bằng chứng hay giả định) → điểm số → mức **P0-P3**.
- **Thời điểm:** Eisenhower (urgent × important) và/hoặc WSJF (cost-of-delay / effort) → **now / next / later**.
- Claude ước lượng từ bằng chứng. Yếu tố cần context sản phẩm (Reach, business Impact) thì hỏi hoặc đánh dấu là giả định.

## 5. Output: Decision Brief

Artifact cuối cùng, định dạng markdown theo template. Các phần:

1. Hạng mục + loại (bug/feature/techdebt/task)
2. Reality check: verified hay chưa, bằng chứng, reproduction/root-cause hoặc need-alignment
3. Verdict: Go / No-Go / Cần thêm thông tin + lý do
4. (nếu Go) Priority: bảng framework + điểm số + P-level
5. (nếu Go) Timing: now/next/later + lý do
6. Giả định & khoảng trống thông tin

Không có phần "bước kế tiếp tự động". Skill dừng tại đây.

## 6. Cấu trúc file

Theo phương án B (khớp convention repo: `deep-insight`, `systems-thinking`).

```
skills/decision-gate/
  SKILL.md                            # 3 pha + tư thế "không phán xét vội" + checkpoint go/no-go
  references/frameworks.md            # RICE/ICE/Eisenhower/WSJF: công thức, cách map score→P-level và →timing
  references/verification-tactics.md  # mẹo đào bằng chứng theo bản chất hạng mục (reproduce, root-cause, đo techdebt, validate need)
  templates/decision-brief.md         # template output
```

SKILL.md giữ gọn, điều phối luồng. Công thức khung và mẹo xác minh tách references để load khi cần. Template brief tách riêng.

## 7. Phạm vi (YAGNI)

Trong phạm vi:
- Xử lý một hạng mục mỗi lần.
- Output là decision brief văn bản.

Ngoài phạm vi (loại bỏ):
- Triage hàng loạt nhiều hạng mục cùng lúc.
- Tự tạo issue, lập kế hoạch, bàn giao sang skill khác.
- Playbook riêng từng loại hạng mục.
- Tích hợp issue tracker bên ngoài (chỉ đọc nếu có sẵn trong repo).

## 8. Việc cập nhật tài liệu khi hoàn thành

Sau khi tạo skill, cập nhật `CLAUDE.md` (phần Structure + bảng chi tiết skill) và `README.md` theo quy tắc Auto-update Documentation của repo.
