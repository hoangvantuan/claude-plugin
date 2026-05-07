# Training Engine: Framework Xây dựng Tài liệu Training

**Ngày**: 2026-05-07
**Repo**: `/Users/tuanhv/Desktop/git_projects/training-engine`
**Loại**: Claude Code plugin độc lập
**Tiền thân**: skill `van-tu-tu-training` trong `shun-claude-plugin`

## Tổng quan

Training Engine là plugin Claude Code chuyên xây dựng tài liệu training. Thay vì gộp mọi thứ vào 1 skill, Training Engine tách thành **pipeline 6 phase**, mỗi phase là 1 skill độc lập. Phương pháp sư phạm (Văn-Tư-Tu, ADDIE, 4Cs, ...) là **plugin** cắm vào pipeline, không hardcode.

### Vấn đề với skill hiện tại

- 1 SKILL.md 320 dòng, chạy tuần tự 4 bước, không tách được
- Phương pháp Văn-Tư-Tu gắn cứng, không thay bằng method khác
- Không có state management, user phải chạy lại từ đầu nếu muốn sửa 1 phase
- Templates và rules trộn lẫn method-specific với method-agnostic

### Giải pháp

Plugin riêng biệt với kiến trúc Skill Family:
- 7 skills (1 conductor + 6 pipeline phases)
- Method plugin system (Văn-Tư-Tu là method đầu tiên, hướng dẫn tạo method mới)
- Project state folder cho mỗi dự án training
- Conductor điều phối + cho phép gọi riêng từng skill

## Kiến trúc

### Cấu trúc thư mục plugin

```
training-engine/
  .claude-plugin/
    plugin.json
  CLAUDE.md
  skills/
    training/                    ← CONDUCTOR
      SKILL.md
    training-init/               ← Phase 1: Khởi tạo dự án
      SKILL.md
      references/
        brief-template.md        ← Template brief (phần generic)
        validation-rules.md      ← Rules validate câu trả lời brief
    training-research/           ← Phase 2: Nghiên cứu nội dung
      SKILL.md
      references/
        extraction-guide.md      ← Hướng dẫn trích xuất & phân loại
        source-formats.md        ← Hỗ trợ PDF, DOCX, URL, YouTube, text
    training-analyze/            ← Phase 3: Phân tích & tách module
      SKILL.md
      references/
        modular-architecture.md  ← Tiêu chí tách module (method-agnostic)
        tier-system.md           ← Foundation/Core/Advanced/Specialized
    training-plan/               ← Phase 4: Thiết kế từng module
      SKILL.md
      references/
        design-decisions.md      ← 4 quyết định per module
    training-build/              ← Phase 5: Sinh nội dung
      SKILL.md
      references/
        naming-convention.md     ← Quy tắc đặt tên file/folder
        gdocs-compatibility.md   ← Rules tương thích Google Docs
        build-order.md           ← Thứ tự viết tối ưu
    training-review/             ← Phase 6: Review & validation
      SKILL.md
      references/
        quality-checklist.md     ← Checklist chất lượng (generic)
        trap-detection.md        ← Failure mode patterns (generic)
    training-methods/            ← Thư viện phương pháp sư phạm
      SKILL.md                   ← Hướng dẫn chọn/tạo method
      van-tu-tu/                 ← Method: Văn-Tư-Tu (default)
        method.md
        references/
        templates/
      _template/                 ← Template tạo method mới
        method.md
        README.md
```

### State: Project Folder

Mỗi dự án training tạo thư mục riêng chứa output mỗi phase:

```
training-projects/<slug>/
  project.json                 ← Metadata dự án
  00-brief.md                  ← Output: training-init
  01-content-inventory.md      ← Output: training-research
  02-module-map.md             ← Output: training-analyze
  03-module-designs/           ← Output: training-plan
    module-01-<slug>.md
    module-02-<slug>.md
  04-modules/                  ← Output: training-build
    module-01-<slug>/
      README.md
      ...phase folders...
    module-02-<slug>/
      ...
    _facilitator-hub/
    _danh-gia-khoa/
  05-review-report.md          ← Output: training-review
```

`training-projects/` nằm tại **thư mục làm việc của user** (CWD), không nằm trong plugin.

### project.json

```json
{
  "name": "feedback-cho-leader",
  "method": "van-tu-tu",
  "current_phase": "init",
  "phases": {
    "init": { "status": "done", "output": "00-brief.md" },
    "research": { "status": "pending" },
    "analyze": { "status": "pending" },
    "plan": { "status": "pending" },
    "build": { "status": "pending" },
    "review": { "status": "pending" }
  },
  "config": {
    "default_ratio": [10, 20, 70],
    "default_direction": "traditional"
  },
  "created_at": "2026-05-07",
  "updated_at": "2026-05-07"
}
```

## Pipeline: 6 Phase Skills

### Phase 1: `/training-init` (Khởi tạo)

**Input**: Tên chủ đề + mô tả sơ bộ
**Output**: `00-brief.md` + `project.json`

Workflow:
1. Tạo thư mục `training-projects/<slug>/`
2. Hỏi user chọn method (liệt kê methods có trong `training-methods/`, mặc định Văn-Tư-Tu)
3. Load method manifest → lấy brief questions đặc thù method
4. Hỏi 5 câu hỏi bắt buộc (generic) + câu hỏi method-specific
5. Validate: mỗi câu trả lời phải có số cụ thể, danh từ cụ thể, chứng cứ kiểm chứng
6. Hỏi 3 câu hỏi bối cảnh (trigger-based, không bắt buộc)
7. Ghi `00-brief.md` + `project.json`

5 câu hỏi generic (mọi method):
1. Training này dạy gì? (1-2 câu, không dùng từ mơ hồ)
2. Sau khoá, bao nhiêu % học viên làm được gì? (công thức: "Sau [thời gian], [X]% [nhóm] có thể [hành động] [tần suất], kiểm chứng bằng [bằng chứng]")
3. Học viên là ai? (level + tự đánh giá 1-10 + kiến thức hiện có + pain point lớn nhất)
4. Họ áp dụng ở đâu? (tình huống cụ thể + tần suất)
5. Đo thành công bằng gì? (công thức: "[chỉ số] đo bằng [công cụ], tại [thời điểm], đạt khi [ngưỡng]")

### Phase 2: `/training-research` (Nghiên cứu)

**Input**: `00-brief.md` + tài liệu nguồn (file, URL, text)
**Output**: `01-content-inventory.md`

Workflow:
1. Đọc `project.json` → kiểm tra phase init đã done
2. Đọc `00-brief.md` để hiểu scope
3. Nhận tài liệu nguồn từ user (hỗ trợ: PDF, DOCX, URL, YouTube transcript, text trực tiếp)
4. Trích xuất mọi ý chính từ tài liệu
5. Phân loại theo taxonomy của method (Văn-Tư-Tu dùng: K=Khái niệm, N=Nguyên lý, T=Kỹ thuật, V=Ví dụ, C=Cảnh báo)
6. So sánh inventory với brief → xác định khoảng trống
7. Bổ sung research cho khoảng trống (web search, deep research)
8. Ghi `01-content-inventory.md`

Format output:

```markdown
| # | Ý chính | Loại | Nguồn | Ghi chú |
|---|---------|------|-------|---------|
| 1 | SBI framework... | T | source-1.pdf p.12 | Core technique |
| 2 | Feedback loop... | K | research | Bổ sung |
```

### Phase 3: `/training-analyze` (Phân tích & tách module)

**Input**: `00-brief.md` + `01-content-inventory.md`
**Output**: `02-module-map.md`

Workflow:
1. Đọc brief + content inventory
2. Nhóm ý chính thành cụm độc lập (module candidates)
3. Kiểm tra 5 tiêu chí tách module:
   - 1 module = 1 chủ đề (nói được trong 1 câu)
   - Bỏ module A không làm vỡ module B
   - Hoàn thành được trong 1-5 ngày
   - Đủ lớn để sau module, học viên làm được ≥1 việc cụ thể
   - Cùng mức trừu tượng trong 1 tier
4. Xếp tier: Foundation → Core → Advanced → Specialized
5. Vẽ prerequisite map (Mermaid flowchart)
6. Content coverage check: mỗi ý trong inventory phải thuộc ≥1 module
7. Brief coverage check: mỗi outcome (brief Q2) + metric (brief Q5) phải có module phục vụ
8. Ghi `02-module-map.md`

### Phase 4: `/training-plan` (Thiết kế module)

**Input**: `00-brief.md` + `02-module-map.md` + method config
**Output**: `03-module-designs/module-XX-<slug>.md`

Workflow:
1. Cho mỗi module trong module map, quyết định 4 điều:
   - Ratio giữa các phase (method cung cấp lookup table theo content type + learner level)
   - Direction (thứ tự các phase trong module)
   - Guidance level: step-by-step / semi-guided / independent
   - Primary deliverable: học viên nộp/trình bày gì (phải verify metric từ brief)
2. Liên kết mỗi module với outcome (brief Q2) + metric (brief Q5) cụ thể
3. Ghi 1 file design per module vào `03-module-designs/`

### Phase 5: `/training-build` (Sinh nội dung)

**Input**: `03-module-designs/` + method templates
**Output**: `04-modules/` (toàn bộ cấu trúc khoá học)

Workflow:
1. Cho mỗi module design:
   - Load templates từ method plugin
   - Sinh nội dung theo thứ tự tối ưu (method quyết định, vd Văn-Tư-Tu: README → Tu → Tư → Văn → Đánh giá)
   - Áp dụng naming convention
   - Áp dụng GDocs compatibility rules
2. Sinh facilitator hub (`_facilitator-hub/`):
   - Hướng dẫn chung
   - Module map với links
   - Lịch trình gợi ý
3. Sinh đánh giá khoá (`_danh-gia-khoa/`):
   - Survey cuối khoá
   - Follow-up 30/60/90 ngày
4. Sinh `00-tong-quan.md` (overview với links tới mọi module)

### Phase 6: `/training-review` (Review)

**Input**: `04-modules/` + `00-brief.md`
**Output**: `05-review-report.md`

Workflow:
1. Quality checklist per module (method cung cấp tiêu chí)
2. Naming & linking check (theo naming-convention.md)
3. GDocs compatibility check (theo gdocs-compatibility.md)
4. Failure mode scan (method cung cấp danh sách bẫy)
5. Brief alignment: output cuối có phủ hết outcome + metric từ brief?
6. Ghi `05-review-report.md` với pass/fail per module + issues + gợi ý sửa

## Conductor: `/training`

Entry point chính. Đọc state, gợi ý bước tiếp.

Workflow:
1. Tìm `training-projects/` trong CWD
2. Nếu không có project nào: hỏi tạo mới → gọi `training-init`
3. Nếu có 1 project: đọc `project.json`, hiển thị dashboard
4. Nếu có nhiều project: hỏi chọn project nào
5. Gợi ý phase tiếp theo dựa trên `current_phase`
6. User có thể yêu cầu chạy bất kỳ phase nào (conductor kiểm tra prerequisite)

Dashboard:

```
╔═══════════════════════════════════════╗
║  Training: Feedback cho Leader        ║
║  Method: Văn-Tư-Tu                    ║
╠═══════════════════════════════════════╣
║  ✅ Init        → 00-brief.md        ║
║  ✅ Research    → 01-content-inv.md   ║
║  ▶️ Analyze     (gợi ý chạy tiếp)    ║
║  ⬜ Plan                              ║
║  ⬜ Build                             ║
║  ⬜ Review                            ║
╚═══════════════════════════════════════╝
```

## Method Plugin System

### Method manifest: `method.md`

Mỗi method plugin bắt buộc có file `method.md` với cấu trúc sau:

```markdown
# Method: [Tên method]

## Metadata
- id: [kebab-case identifier]
- version: [semver]
- origin: [xuất xứ]

## Philosophy
[Mô tả ngắn triết lý sư phạm, 3-5 câu]

## Module Phases
Định nghĩa các phase bên trong 1 module:
- [phase-id] ([tên]): [% mặc định]
  - Mô tả: [phase này dạy/làm gì]
  - Template: templates/[file].md

## Directions
Thứ tự các phase có thể chạy:
- [direction-id]: [phase-1] → [phase-2] → ... (cho [đối tượng nào])

## Ratio Adjustments
Bảng điều chỉnh ratio theo:
- Content type
- Learner level
- Duration
(Hoặc reference đến file: references/ratio-table.md)

## Brief Questions (Hook: init)
Câu hỏi bổ sung khi khởi tạo dự án (ngoài 5 câu generic):
- [câu hỏi method-specific]

## Content Taxonomy (Hook: research)
Phân loại nội dung:
- [code]: [mô tả]

## Module Criteria (Hook: analyze)
Tiêu chí bổ sung khi tách module (ngoài 5 tiêu chí generic):
- [tiêu chí method-specific]

## Quality Criteria (Hook: review)
Tiêu chí chất lượng per module:
| # | Tiêu chí | Loại | Mô tả |
|---|----------|------|-------|

## Failure Modes (Hook: review)
| Bẫy | Triệu chứng | Cách thoát |
|-----|-------------|------------|

## Build Order (Hook: build)
Thứ tự viết nội dung tối ưu cho 1 module:
1. [file đầu tiên] (lý do)
2. [file tiếp] (lý do)
```

### Method Văn-Tư-Tu (default)

Nội dung chuyển từ skill hiện tại:

```
training-methods/van-tu-tu/
  method.md                    ← Manifest (tổng hợp từ SKILL.md hiện tại)
  references/
    philosophy.md              ← Từ philosophy-foundation.md
    ratio-table.md             ← Từ ratio-adjustment.md
    facilitation.md            ← Phần facilitation từ philosophy-foundation.md
    failure-modes.md           ← 5 bẫy từ SKILL.md
  templates/
    module-structure.md        ← Cấu trúc: 01-van/, 02-tu-suy-tu/, 03-tu-thuc-hanh/, 04-danh-gia/
    van.md                     ← Từ template-van.md
    tu-suy-tu.md               ← Từ template-tu-suy-tu.md
    tu-thuc-hanh.md            ← Từ template-tu-thuc-hanh.md
    danh-gia.md                ← Từ template-danh-gia.md
    facilitator-hub.md         ← Từ template-facilitator-hub.md
```

### Template tạo method mới

```
training-methods/_template/
  method.md                    ← Template trống, mọi section có placeholder + hướng dẫn
  README.md                    ← Step-by-step: copy → rename → điền → test
```

README.md hướng dẫn:
1. Copy thư mục `_template/` → rename theo method id
2. Điền `method.md`: bắt buộc mọi section, không để TBD
3. Tạo `references/` nếu method có tài liệu tham khảo
4. Tạo `templates/` với 1 template per module phase
5. Test: chạy `training-init` chọn method mới, verify brief questions load đúng

## Migration từ skill hiện tại

### Bảng mapping file

| File hiện tại (van-tu-tu-training) | Đích mới | Phân loại |
|---|---|---|
| `philosophy-foundation.md` | `training-methods/van-tu-tu/references/philosophy.md` | Method-specific |
| `ratio-adjustment.md` | `training-methods/van-tu-tu/references/ratio-table.md` | Method-specific |
| `template-van.md` | `training-methods/van-tu-tu/templates/van.md` | Method-specific |
| `template-tu-suy-tu.md` | `training-methods/van-tu-tu/templates/tu-suy-tu.md` | Method-specific |
| `template-tu-thuc-hanh.md` | `training-methods/van-tu-tu/templates/tu-thuc-hanh.md` | Method-specific |
| `template-danh-gia.md` | `training-methods/van-tu-tu/templates/danh-gia.md` | Method-specific |
| `template-facilitator-hub.md` | `training-methods/van-tu-tu/templates/facilitator-hub.md` | Method-specific |
| `modular-architecture.md` | `skills/training-analyze/references/modular-architecture.md` | Method-agnostic |
| `naming-convention.md` | `skills/training-build/references/naming-convention.md` | Method-agnostic |
| `gdocs-compatibility.md` | `skills/training-build/references/gdocs-compatibility.md` | Method-agnostic |
| `template-training-brief.md` | Tách: generic → `training-init/references/brief-template.md`, Văn-Tư-Tu questions → `method.md` | Hybrid |

### Nội dung cần viết mới

| File | Mô tả |
|---|---|
| `plugin.json` | Plugin manifest cho training-engine |
| `CLAUDE.md` | Project instructions |
| 7 `SKILL.md` files | Prompt chính cho conductor + 6 phase skills |
| `training-methods/SKILL.md` | Hướng dẫn chọn/tạo method |
| `training-methods/van-tu-tu/method.md` | Method manifest (tổng hợp từ SKILL.md cũ) |
| `training-methods/_template/method.md` | Template method trống |
| `training-methods/_template/README.md` | Hướng dẫn tạo method mới |
| `training-init/references/validation-rules.md` | Rules validate brief |
| `training-research/references/extraction-guide.md` | Hướng dẫn trích xuất |
| `training-research/references/source-formats.md` | Formats hỗ trợ |
| `training-analyze/references/tier-system.md` | Hệ thống xếp tier |
| `training-plan/references/design-decisions.md` | 4 quyết định per module |
| `training-build/references/build-order.md` | Thứ tự viết |
| `training-review/references/quality-checklist.md` | Checklist generic |
| `training-review/references/trap-detection.md` | Failure patterns generic |
| `training-methods/van-tu-tu/references/facilitation.md` | Tách từ philosophy-foundation |
| `training-methods/van-tu-tu/references/failure-modes.md` | 5 bẫy từ SKILL.md |
| `training-methods/van-tu-tu/templates/module-structure.md` | Cấu trúc module Văn-Tư-Tu |

### Sau migration

Xoá `skills/van-tu-tu-training/` trong `shun-claude-plugin`. Cập nhật CLAUDE.md và README.md của shun-claude-plugin.

## Quy tắc thiết kế xuyên suốt

1. **Method-agnostic vs method-specific**: Pipeline skills không chứa logic đặc thù 1 method. Mọi thứ method-specific nằm trong `training-methods/<method-id>/`.
2. **State rõ ràng**: Mỗi skill ghi output vào file cố định. Skill sau đọc file trước, không truyền qua biến.
3. **Fail fast**: Nếu thiếu prerequisite, thông báo ngay. Không đoán.
4. **Idempotent**: Chạy lại 1 phase sẽ ghi đè output cũ. Không tạo bản sao.
5. **YAGNI**: Build Văn-Tư-Tu method đầu tiên. Chỉ thêm method mới khi có nhu cầu thực.

## plugin.json

```json
{
  "name": "training-engine",
  "description": "Framework xây dựng tài liệu training với phương pháp sư phạm pluggable",
  "version": "1.0.0",
  "skills": [
    {
      "name": "training",
      "description": "Conductor: quản lý pipeline xây dựng training từ init đến review. Entry point chính."
    },
    {
      "name": "training-init",
      "description": "Khởi tạo dự án training: chọn method, trả lời brief questions, tạo project folder."
    },
    {
      "name": "training-research",
      "description": "Nghiên cứu & trích xuất nội dung từ tài liệu nguồn (PDF, DOCX, URL, YouTube, text). Output: content inventory."
    },
    {
      "name": "training-analyze",
      "description": "Phân tích content inventory, tách module độc lập, xếp tier, vẽ prerequisite map, kiểm tra coverage."
    },
    {
      "name": "training-plan",
      "description": "Thiết kế từng module: chọn ratio, direction, guidance level, deliverable theo method config."
    },
    {
      "name": "training-build",
      "description": "Sinh nội dung từng module theo templates, kèm facilitator hub và đánh giá khoá."
    },
    {
      "name": "training-review",
      "description": "Review chất lượng toàn bộ khoá: quality checklist, naming, GDocs compat, failure modes, brief alignment."
    },
    {
      "name": "training-methods",
      "description": "Thư viện phương pháp sư phạm. Xem danh sách methods có sẵn hoặc hướng dẫn tạo method mới."
    }
  ]
}
```
