---
name: van-tu-tu-training
description: >
  Xây dựng bộ tài liệu training theo mô hình Văn-Tư-Tu (Tam Tuệ Học). Sử dụng khi user muốn tạo khoá đào tạo,
  training materials, learning modules, tài liệu hướng dẫn nội bộ, onboarding, upskill cho cá nhân/team/công ty.
  Trigger khi user nói: "tạo tài liệu training", "xây dựng khoá học", "thiết kế chương trình đào tạo",
  "làm training module", "tạo bài tập thực hành", "xây dựng onboarding", hoặc bất kỳ yêu cầu liên quan
  đến việc tạo nội dung đào tạo có cấu trúc. Ưu tiên skill này khi user đề cập đến "Văn-Tư-Tu",
  "70% thực hành", "learning by doing", hoặc muốn training thực tế thay vì lý thuyết suông.
---

# Văn-Tư-Tu Training Builder

Skill xây dựng bộ tài liệu training theo mô hình **Văn-Tư-Tu** (Tam Tuệ Học / Śruta-Cintā-Bhāvanā) — framework 2.600 năm từ Phật giáo, ứng dụng vào đào tạo hiện đại.

## Nguyên tắc cốt lõi

**Mô hình Văn-Tư-Tu:**

| Giai đoạn | Tỷ lệ | Bản chất                                                          |
| --------- | ----- | ----------------------------------------------------------------- |
| **Văn**   | 10%   | Tiếp nhận kiến thức — tinh gọn, chỉ giữ cái cần thiết             |
| **Tư**    | 20%   | Tiêu hoá kiến thức — đặt câu hỏi, liên hệ bản thân                |
| **Tu**    | 70%   | Sống với kiến thức — thực hành, đúc kết, chuyển hoá thành hành vi |


**5 nguyên tắc vàng:**

1. **Tu > Tư > Văn** — 70% cho thực hành, không phải lý thuyết
2. **1 module = 1 chủ đề = 1 chu trình Văn-Tư-Tu hoàn chỉnh**
3. **Module độc lập** — bỏ bớt, thêm vào, đổi thứ tự đều không ảnh hưởng
4. **Phương pháp theo cấp độ** — Người mới cần yêu thương, người giỏi cần áp lực
5. **Đúc kết là bắt buộc** — Không đúc kết = không học

## Quick Start — Cá nhân, 1 chủ đề đơn

Nếu chỉ cần tạo **1 module cho cá nhân tự học**, bỏ qua quy trình 6 bước, tạo 1 file duy nhất:

```markdown
# [Tên Module] — Training Cá Nhân

## VĂN: Tôi cần biết gì? (10%)
- 3-5 ý chính, mỗi ý kèm 1 ví dụ thực tế
- 1 framework/mô hình tóm tắt

## TƯ: Điều này có ý nghĩa gì với tôi? (20%)
- Liên hệ với công việc hiện tại
- 1 tình huống cụ thể tôi sẽ áp dụng
- Kế hoạch thử nghiệm

## TU: Thực hành (70%)
- Tuần 1: Thử [hành động cụ thể] — ghi nhật ký mỗi ngày
- Tuần 2: Mở rộng + điều chỉnh
- Đúc kết: 3 bài học rút ra + 1 nguyên tắc giữ lại
```

Nếu cần **nhiều module, cho team/công ty** → dùng quy trình 6 bước bên dưới.

## Quy trình 6 bước

Khi user yêu cầu tạo tài liệu training, thực hiện theo 6 bước sau:

### Bước 1: Xác định mục tiêu tổng thể

Cần 5 thông tin sau. **Chỉ hỏi những câu mà user chưa cung cấp**, gộp thành 1 lần hỏi duy nhất:

1. **Chủ đề đào tạo là gì?** — Cụ thể, rõ ràng
2. **Sau khoá, người học CÓ THỂ LÀM GÌ?** — Viết dạng hành vi đo lường được
3. **Ai là người học?** — Kinh nghiệm, cấp độ (mới/có nền tảng/tiềm năng cao/expert)
4. **Áp dụng ở đâu?** — Bối cảnh công việc thực tế
5. **Đo lường thành công bằng gì?** — Chỉ số cụ thể

Nếu user đã cung cấp đủ 5 thông tin → bỏ qua, chuyển thẳng Bước 2.

### Bước 2: Phân tách thành modules

Đây là bước quyết định chất lượng toàn bộ khoá đào tạo.

**Quy trình:**

1. Brainstorm tất cả kiến thức/kỹ năng cần dạy
2. Nhóm thành clusters (mỗi cluster = 1 module tiềm năng)
3. Kiểm tra tính độc lập (3 câu hỏi):
  - Học xong cluster này, làm được ít nhất 1 việc cụ thể?
  - Bỏ cluster này, các cluster còn lại vẫn có giá trị?
  - Hoàn thành trong 1-5 ngày (cá nhân) / 1-2 tuần (team)?
4. Xác định tier: Foundation → Core → Advanced → Specialized
5. Vẽ prerequisite map (dùng Mermaid)
6. Tạo bảng tóm tắt module

**5 quy tắc phân tách:**

- 1 module = 1 chủ đề trọng tâm
- Độc lập tối đa (ghi rõ prerequisite nếu có)
- Đủ nhỏ để hoàn thành (1-5 ngày)
- Đủ lớn để có giá trị
- Cùng cấp độ trừu tượng

> Đọc `references/modular-architecture.md` để hiểu chi tiết về kiến trúc modular, tier system, và folder structure.

### Bước 3: Thiết kế từng module

Với mỗi module, xác định:

| Quyết định            | Lựa chọn                                       |
| --------------------- | ---------------------------------------------- |
| **Tỷ lệ Văn-Tư-Tu**   | Dựa vào loại kiến thức và cấp độ người học     |
| **Chiều đi**          | Văn→Tư→Tu (mặc định) hay Tu→Tư→Văn (kiến tạo)? |
| **Mức độ guided**     | Step-by-step / Semi-guided / Independent?      |
| **Deliverable chính** | Người học nộp/trình bày gì cuối module?        |

**Khi chọn chiều kiến tạo (Tu→Tư→Văn):**

Áp dụng khi người học có nền tảng hoặc chủ đề mang tính trải nghiệm (kỹ năng mềm, leadership, sáng tạo).

| Bước | Hoạt động | Facilitator làm gì |
|------|-----------|-------------------|
| **Tu trước** | Đặt người học vào tình huống thực tế / mô phỏng — CHƯA dạy lý thuyết | Tạo môi trường, quan sát, không can thiệp |
| **Tư giữa** | Người học tự đúc kết: "Mình vừa làm gì? Tại sao kết quả như vậy?" | Hỏi ngược, dẫn dắt phản tư |
| **Văn cuối** | Cung cấp framework/lý thuyết — người học đối chiếu với trải nghiệm | Bổ sung, hệ thống hoá |

> Lưu ý: Chiều kiến tạo **xuất phát chậm** nhưng **về đích trước** — hành vi thay đổi sâu và bền hơn. Đo sau 30-60-90 ngày, không chỉ quiz ngay sau buổi học.

> Đọc `references/ratio-adjustment.md` để tra cứu tỷ lệ phù hợp theo loại kiến thức và cấp độ.

### Bước 4: Xây dựng nội dung

**Thứ tự viết tối ưu cho MỖI module:**

```
1. Viết README.md (thẻ căn cước module)
2. Viết TU_THUC_HANH trước — bài thực hành, dự án (70% giá trị)
3. Viết TU_SUY_TU — câu hỏi phản chiếu, case study
4. Viết VAN — chỉ kiến thức CẦN CHO Tư và Tu
5. Viết DANH_GIA — rubric, After-Action Review template
```

**Quy tắc vàng:** Với mỗi đoạn trong Văn, tự hỏi: "Bỏ đoạn này, người học có làm được bài thực hành không?" Nếu có → bỏ.

> Templates chi tiết cho từng thành phần — chỉ load file cần dùng:
> - `references/template-van.md` — Template cho phần VĂN
> - `references/template-tu-suy-tu.md` — Template cho phần TƯ
> - `references/template-tu-thuc-hanh.md` — Template cho phần TU
> - `references/template-danh-gia.md` — Template cho phần ĐÁNH GIÁ

### Bước 5: Triển khai

Điều chỉnh theo quy mô:

| Quy mô          | Cách làm                                                  |
| --------------- | --------------------------------------------------------- |
| **Cá nhân**     | 1 file/module, đơn giản, tự học                           |
| **Team (5-15)** | Full folder structure, facilitator điều phối, buddy pairs |
| **Công ty**     | Module Library, facilitator training, rolling deployment  |

**Chi tiết triển khai theo quy mô:**

**Cá nhân:**
- 1 file/module là đủ (gộp Văn-Tư-Tu vào 1 file)
- Tự đặt deadline cho mỗi module (1-5 ngày)
- Dùng checklist hành động để duy trì kỷ luật

**Team (5-15 người):**
- **Buddy pairs:** Ghép chéo trình độ, trao đổi bài Tư + review deliverable của nhau
- **Facilitator:** 1 người dẫn dắt, không giảng bài — hỏi ngược + phản biện
- **Kick-off:** Giới thiệu khoá, chia buddy, gửi pre-work (Văn Module 1)
- **Check-in:** Giữa tuần (15-30 phút) — tiến độ + rào cản
- **Wrap-up:** Teach-back (mỗi người 5 phút) + After-Action Review

**Công ty (rolling deployment):**
- **Pilot:** 1 team đi trước (4-6 tuần) → thu feedback → điều chỉnh tài liệu
- **Train-the-trainer:** Alumni pilot trở thành facilitator cho đợt sau
- **Module Library:** Modules đã validate đưa vào thư viện chung — team tự chọn theo tier + prerequisite
- **Rolling:** Team mới bắt đầu mỗi 2-4 tuần, không cần đợi tất cả cùng lúc

> Đọc `references/template-facilitator-hub.md` để tra cứu chi tiết: hướng dẫn facilitation, module map, lịch trình gợi ý, và cách ghép buddy pairs.

### Bước 6: Đánh giá & cải tiến

**Cấp module:** After-Action Review sau mỗi module + Rubric đánh giá deliverable.
**Cấp khoá:** Survey cuối khoá + đo hành vi thay đổi sau 30-60-90 ngày.

| Thời điểm | Công cụ | Đo gì |
|-----------|---------|-------|
| Cuối mỗi module | After-Action Review + Rubric | Mức độ nắm kiến thức + chất lượng thực hành |
| Cuối khoá | Survey cuối khoá | Đánh giá tổng thể + mức độ hài lòng |
| Sau 30 ngày | Follow-up check-in | Đang thử áp dụng? Rào cản gì? |
| Sau 60 ngày | Check-in 1:1 | Hành vi đã thay đổi chưa? Kết quả cụ thể? |
| Sau 90 ngày | Follow-up + Meeting nhóm | Thói quen bền vững? Tác động đo lường được? |

**Phân tích & cải tiến:**
- Tỷ lệ áp dụng < 30% → Kiểm tra lại phần Tu (thiếu thực hành?)
- Tỷ lệ áp dụng 30-60% → Kiểm tra rào cản môi trường
- Tỷ lệ áp dụng > 60% → Khoá hiệu quả — đúc kết best practices

> Templates đánh giá cấp module (rubric, AAR) và cấp khoá (survey, follow-up 30-60-90): đọc `references/template-danh-gia.md`.

## Micro-cycle xuyên suốt

Mỗi hoạt động học đều đi qua 3 bước:

1. **Quan sát** → Nhìn, nghe, ghi nhận (không vội đánh giá)
2. **Phân tích** → Tại sao? Cơ chế gì? Liên hệ gì với mình?
3. **Đúc kết** → Bài học là gì? Tôi sẽ làm gì khác?

Đảm bảo micro-cycle này xuất hiện trong MỖI bài thực hành, MỖI case study.

## Facilitation — Cách dạy/dẫn dắt

**Nguyên tắc vàng:** Đừng trả lời — hãy hỏi ngược.

- Người học hỏi → Đưa tài liệu, cho tự nghiên cứu (Văn)
- Cho thời gian tự tìm hiểu (Tư)
- Người học nộp kế hoạch → Facilitator phản biện (Tư sâu hơn)
- Đạt → Triển khai (Tu)

> Chi tiết về mô hình Gà-Đại Bàng (phương pháp theo cấp độ), hai chiều đi của tam giác, và facilitation nâng cao: đọc `references/philosophy-foundation.md`.
> Tỷ lệ Văn-Tư-Tu gợi ý theo cấp độ người học: đọc `references/ratio-adjustment.md`.

## Output format

Tạo bộ tài liệu theo cấu trúc folder chuẩn trong `references/modular-architecture.md` (Section 4 + 5).

**Lưu ý:**

- Cá nhân: đơn giản hoá — 1 file/module là đủ
- Team: full structure
- Công ty: thêm Module Library

## References

Khi cần tra cứu chi tiết, đọc các file sau:

| File                                     | Khi nào đọc                                                                    |
| ---------------------------------------- | ------------------------------------------------------------------------------ |
| `references/philosophy-foundation.md`    | Triết lý Văn-Tư-Tu, facilitation, mô hình Gà-Đại Bàng, hai chiều             |
| `references/modular-architecture.md`     | Phân tách module, tier system, prerequisite map, template tổng quan khoá       |
| `references/ratio-adjustment.md`         | Tỷ lệ theo loại kiến thức, cấp độ, quy tắc ràng buộc, thời gian              |
| `references/template-van.md`             | Template phần VĂN (core_reading, knowledge_check)                             |
| `references/template-tu-suy-tu.md`       | Template phần TƯ (phản chiếu, case study, nhật ký)                            |
| `references/template-tu-thuc-hanh.md`    | Template phần TU (guided practice, dự án, checklist, teach-back)               |
| `references/template-danh-gia.md`        | Template ĐÁNH GIÁ (rubric, AAR, survey cuối khoá, follow-up 30-60-90)         |
| `references/template-facilitator-hub.md` | Template Facilitator Hub (hướng dẫn chung, module map, lịch trình, buddy pairs) |

