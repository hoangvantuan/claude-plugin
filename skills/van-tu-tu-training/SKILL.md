---
name: van-tu-tu-training
description: "Xây dựng bộ tài liệu training theo mô hình Văn-Tư-Tu (Tam Tuệ Học)."
disable-model-invocation: true
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

## Chuẩn đặt tên & liên kết

**Tuyệt đối tuân thủ** chuẩn trong `references/naming-convention.md` khi tạo bộ tài liệu:

- **Folder/file**: kebab-case, tiếng Việt không dấu, zero-pad 2 chữ số (`01-`, `02-`). Ví dụ: `module-01-nen-tang-feedback/`, `cau-hoi-phan-chieu.md`.
- **Phase folder cố định**: `01-van/`, `02-tu-suy-tu/`, `03-tu-thuc-hanh/`, `04-danh-gia/`.
- **Folder meta prefix `_`**: `_facilitator-hub/`, `_danh-gia-khoa/`.
- **Link**: luôn markdown + relative path — `[Module 2](../module-02-slug/README.md)`. Không đường dẫn tuyệt đối, không text trần.
- **README mỗi module** bắt buộc link: tổng quan khoá, 4 phase, prerequisite (nếu có), module tiếp theo.

> Đọc `references/naming-convention.md` để biết chi tiết tên chuẩn theo vị trí, cách tạo slug, bản đồ link bắt buộc, và checklist kiểm tra cuối.

## Google Docs Compatibility — BẮT BUỘC

Output của skill này là file `.md`, thường được upload lên Google Drive và **auto-convert sang Google Docs**. Để không vỡ layout:

**6 cấm kỵ tuyệt đối:**

1. **Không ASCII art box** — cấm ký tự `┌ ┐ └ ┘ │ ─ ├ ┤ ┬ ┴ ┼`. Docs đổi font → lệch hàng thê thảm.
2. **Không multi-column bằng khoảng trắng** — dùng table markdown 2+ cột thay thế.
3. **Không ASCII tree folder** (`├── └──`) ngoài code block — chuyển nested bullet list.
4. **Không Mermaid diagram** trong deliverable — export ảnh PNG hoặc thay bằng bảng quan hệ "Từ → Đến".
5. **Không `---` horizontal rule** trong content — Docs convert thành đường kẻ mảnh phá nhịp. Dùng heading mới hoặc blank line thay thế. (Ngoại lệ: YAML frontmatter ở đầu file giữ nguyên.)
6. **Không link relative path chéo file** khi upload Drive — thay bằng Docs URL sau convert. Naming-convention relative link chỉ dùng cho Git/local.

**Element OK (đã verify):** heading, bullet, numbered list, **task list `- [ ]` / `- [x]` → render thành checkbox native tick được**, table, bold/italic, blockquote, inline code, code block, link, ảnh URL public.

**Element né:** HTML tags (trừ `<br>` trong cell bảng OK), footnote `[^1]`.

**Khi cần diagram/layout phức tạp:**

| Ý định | Thay bằng |
|---|---|
| Hộp so sánh A vs B | Table markdown 2 cột |
| Folder tree | Nested bullet list (hoặc code block nếu buộc) |
| Flow chart | Ảnh PNG (export từ mermaid.live) hoặc bảng "Bước → Hành động" |
| Prerequisite map | Bảng "Module → Prerequisite" |
| 2x2 matrix | Table markdown 2 cột × 2 row |

> Đọc `references/gdocs-compatibility.md` để biết chi tiết: whitelist/blacklist element, rules bảng, ký tự Unicode an toàn, và checklist test convert cuối cùng.

## Quick Start — Cá nhân, 1 chủ đề đơn

Nếu chỉ cần tạo **1 module cho cá nhân tự học**, bỏ qua quy trình 6 bước, tạo 1 file duy nhất. Đặt tên file theo chuẩn: `module-01-<slug-chu-de>.md` (kebab-case, VN không dấu). Ví dụ: `module-01-ky-thuat-sbi.md`.

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

### Bước 2: Trích xuất nội dung & Phân tách modules

Đây là bước quyết định chất lượng toàn bộ khoá đào tạo.

**Rẽ nhánh:** Nếu user KHÔNG cung cấp tài liệu gốc (chỉ có topic/mục tiêu) → bỏ qua 2A, chuyển thẳng 2B — xây dựng modules từ mục tiêu Bước 1 và kiến thức chuyên môn. Nếu CÓ tài liệu → thực hiện đầy đủ 2A-2B-2C để không sót nội dung.

#### 2A. Trích xuất nội dung gốc (Content Extraction)

Nếu user cung cấp tài liệu (sách, bài viết, video transcript, notes, slide...), **BẮT BUỘC** trích xuất trước khi phân module:

1. **Đọc/phân tích toàn bộ tài liệu gốc** — không bỏ sót phần nào
2. **Liệt kê tất cả ý chính** (key ideas) — mỗi ý 1 dòng, giữ nguyên ngữ nghĩa gốc
3. **Phân loại từng ý** theo bản chất:

| Ký hiệu | Loại | Ví dụ |
|----------|------|-------|
| **K** | Kiến thức (khái niệm, định nghĩa, framework) | "SBI gồm 3 bước: Situation-Behavior-Impact" |
| **N** | Nguyên tắc (quy tắc, mindset, giá trị) | "Feedback phải kịp thời, không để qua 48h" |
| **T** | Kỹ thuật (cách làm, quy trình, tool) | "Dùng câu hỏi mở thay vì phán xét" |
| **V** | Ví dụ/Câu chuyện (case, minh hoạ) | Câu chuyện CEO nhận feedback từ intern |
| **C** | Cảnh báo/Sai lầm (anti-pattern, trap) | "Đừng feedback khi đang tức giận" |

4. **Tạo bảng Content Inventory:**

```markdown
## Content Inventory — [Tên tài liệu gốc]

| # | Ý chính | Loại | Nguồn (trang/phút/đoạn) | → Module |
|---|---------|------|-------------------------|----------|
| 1 | [Ý chính 1] | K | Trang 12 | M1 |
| 2 | [Ý chính 2] | N | Video 05:30 | M2 |
| 3 | [Ý chính 3] | T | Chương 3 | M2 |
| ... | ... | ... | ... | ... |
```

Cột "→ Module" để trống lúc đầu, điền sau khi phân module ở bước 2B.

#### 2B. Phân tách modules

**Quy trình:**

1. Từ Content Inventory, nhóm các ý chính thành clusters (mỗi cluster = 1 module tiềm năng)
2. Kiểm tra tính độc lập (3 câu hỏi):
  - Học xong cluster này, làm được ít nhất 1 việc cụ thể?
  - Bỏ cluster này, các cluster còn lại vẫn có giá trị?
  - Hoàn thành trong 1-5 ngày (cá nhân) / 1-2 tuần (team)?
3. Xác định tier: Foundation → Core → Advanced → Specialized
4. Vẽ prerequisite map (dùng Mermaid)
5. Tạo bảng tóm tắt module

#### 2C. Đối chiếu Content Coverage (BẮT BUỘC)

Sau khi phân module xong, **điền cột "→ Module"** trong Content Inventory và kiểm tra:

```markdown
## Content Coverage Check

| Kiểm tra | Kết quả |
|----------|---------|
| Tổng ý chính trích xuất | ___ ý |
| Đã gán vào module | ___ ý |
| CHƯA gán (orphan) | ___ ý |
| Loại bỏ có lý do | ___ ý |

### Ý chưa được gán (nếu có)
| # | Ý chính | Lý do chưa gán | Quyết định |
|---|---------|----------------|-----------|
| _ | ___ | ___ | Thêm vào Module X / Tạo module mới / Loại bỏ (lý do) |
```

**Quy tắc:**
- **0 ý orphan** = đạt — mọi nội dung quan trọng đều có chỗ
- Nếu có ý orphan → quyết định: gán vào module phù hợp, tạo module mới, hoặc loại bỏ (phải ghi rõ lý do)
- **Trình bày Content Coverage Check cho user xác nhận** trước khi chuyển Bước 3
- Nếu user bổ sung tài liệu mới giữa chừng → lặp lại 2A-2C cho phần bổ sung

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

**Thứ tự viết tối ưu cho MỖI module** (tên phase folder theo chuẩn `naming-convention.md`):

```
1. Viết README.md (thẻ căn cước module)
2. Viết 03-tu-thuc-hanh/ trước — bài thực hành, dự án (70% giá trị)
3. Viết 02-tu-suy-tu/ — câu hỏi phản chiếu, case study
4. Viết 01-van/ — chỉ kiến thức CẦN CHO Tư và Tu
5. Viết 04-danh-gia/ — rubric, After-Action Review template
6. Đối chiếu với Content Inventory — đảm bảo mọi ý chính gán cho module này đều xuất hiện trong nội dung
```

**Quy tắc vàng:** Với mỗi đoạn trong Văn, tự hỏi: "Bỏ đoạn này, người học có làm được bài thực hành không?" Nếu có → bỏ.

**Quy tắc đối chiếu:** Sau khi viết xong module, check lại Content Inventory — mọi ý có ký hiệu K/N/T/V/C gán cho module này phải xuất hiện trong ít nhất 1 thành phần (Văn, Tư, hoặc Tu). Nếu thiếu → bổ sung hoặc ghi lý do loại bỏ.

**Micro-cycle trong mỗi hoạt động:** Mỗi bài thực hành và case study phải đi qua 3 bước: Quan sát (nhìn, ghi nhận, không vội đánh giá) → Phân tích (tại sao? cơ chế gì? liên hệ gì với mình?) → Đúc kết (bài học là gì? tôi sẽ làm gì khác?). Thiếu đúc kết = không học.

> Templates chi tiết cho từng thành phần — chỉ load file cần dùng:
> - `references/template-van.md` — Template cho phần VĂN
> - `references/template-tu-suy-tu.md` — Template cho phần TƯ
> - `references/template-tu-thuc-hanh.md` — Template cho phần TU
> - `references/template-danh-gia.md` — Template cho phần ĐÁNH GIÁ

### Bước 5: Triển khai

Điều chỉnh theo quy mô:

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

## Facilitation

**Nguyên tắc vàng:** Đừng trả lời — hãy hỏi ngược. Facilitator dẫn dắt bằng câu hỏi, không giảng bài.

> Chi tiết facilitation (mô hình Gà-Đại Bàng, hai chiều đi, phương pháp theo cấp độ): đọc `references/philosophy-foundation.md`.
> Tỷ lệ Văn-Tư-Tu theo cấp độ người học: đọc `references/ratio-adjustment.md`.

## Output format

Tạo bộ tài liệu theo cấu trúc folder chuẩn trong `references/modular-architecture.md` (Section 4 + 5). Mọi tên folder, tên file, và link **bắt buộc** tuân thủ `references/naming-convention.md`.

**Trước khi bàn giao**, chạy **cả hai** checklist:

1. **Naming & liên kết** — cuối file `references/naming-convention.md` (Section 5):
   - Mọi folder/file kebab-case, VN không dấu, zero-pad số.
   - Đủ 4 phase folder mỗi module.
   - Mọi link bắt buộc (tổng quan ↔ module ↔ phase ↔ facilitator) có mặt, không link placeholder.

2. **Google Docs compatibility** — cuối file `references/gdocs-compatibility.md` (Section 8):
   - Không ASCII box-drawing ngoài code block.
   - Không multi-column bằng space.
   - Folder tree đã trong code block hoặc nested bullet.
   - Mermaid đã thay bằng ảnh/table.
   - **Không `---` horizontal rule** trong content (YAML frontmatter được miễn).
   - Không HTML tags (trừ `<br>` trong cell bảng).
   - Không footnote `[^1]` — chuyển "Ghi chú" cuối file.
   - Link chéo file đã plan theo mục tiêu (Git giữ relative, Drive thay Docs URL).
   - Bảng ≤ 6 cột, không merge cell, có blank line trước và sau.
   - Heading không nhảy cóc, không in đậm.
   - Không 2+ blank line liên tiếp.
   - (Khuyến khích) test 1 file đại diện: upload Drive → mở Docs → kiểm tra.

**Lưu ý theo quy mô:**

- Cá nhân: đơn giản hoá — 1 file/module là đủ (tên file vẫn theo chuẩn kebab-case).
- Team: full structure.
- Công ty: thêm Module Library.


