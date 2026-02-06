---
name: proslide
description: "Tạo slide PowerPoint chuyên nghiệp từ nội dung đầu vào. Sử dụng khi user yêu cầu tạo presentation, slide deck, hoặc gọi /proslide. Hỗ trợ 3 mức độ chi tiết và style tùy chọn. Reuse outline để generate nhiều variants."
---

# ProSlide - Professional Slide Generator

Tạo professional text-only PowerPoint slides từ content input. Vietnamese default. Activate `pptx` skill (built-in, cùng context) cho HTML-to-PPTX conversion.

## Output Folder Structure

Mỗi lần tạo presentation, output được lưu trong folder có cấu trúc:

```
output/
└── {slug}-{YYMMDD-HHmm}/          # VD: ai-trends-260206-0840/
    ├── outline.md                   # Outline có thể reuse
    ├── content-map.md               # Content map (từ phân tích source)
    ├── coverage-report.md           # Coverage report
    ├── research-notes.md            # Research bổ sung (nếu có)
    └── slides/
        └── {slug}-{style-name}.pptx # VD: ai-trends-clean-minimal.pptx
```

**Naming rules:**

* `{slug}`: kebab-case từ topic chính (max 30 chars)

* `{YYMMDD-HHmm}`: timestamp lúc tạo folder

* `{style-name}`: kebab-case tên style (VD: clean-minimal, bold-impact)

* Khi reuse outline để generate thêm PPTX mới, file mới được thêm vào `slides/` của folder đã có

## Step 0: Detect Mode (New / Reuse)

1. Kiểm tra input từ user:

   * Nếu user chỉ vào **folder output đã có** (chứa `outline.md`) → **Reuse mode**

   * Nếu user cung cấp **nội dung mới** (text, file path) → **New mode**

   * Nếu user nói "dùng lại outline", "reuse", "tạo thêm slide" + chỉ folder → **Reuse mode**

2. **Reuse mode** → nhảy thẳng tới **Step 2.5** (skip Step 1 & 2)

3. **New mode** → tiếp tục Step 1

## Step 1: Tiếp nhận nội dung & Cấu hình

1. Đọc input từ user: text trực tiếp hoặc file path (.md, .txt, .pdf)
2. Nếu input là file path, đọc nội dung file
3. Phân tích sơ bộ: topic, length, complexity
4. Hỏi user bằng AskUserQuestion (3 câu hỏi trong 1 lần):

**Câu hỏi 1 - Loại nội dung** (header: "Content type"):

* "Hướng dẫn/Giáo dục" - Giải thích khái niệm, tutorial, hướng dẫn học (Gagné + scaffolding)

* "Business/Báo cáo" - Phân tích, đề xuất, báo cáo kết quả (Pyramid Principle)

* "Thuyết phục/Pitch" - Bán ý tưởng, pitch sản phẩm, proposal (PAS + Sparkline)

* "Technical/Process" - Quy trình, kiến trúc, hệ thống, so sánh kỹ thuật (SCR + step-by-step)

**Câu hỏi 2 - Mức độ chi tiết** (header: "Detail level"):

* "L1 - Tổng quan" - Chỉ ý chính, bullet ngắn gọn (5+ slides)

* "L2 - Cân bằng" - Ý chính + giải thích + ví dụ minh họa (10+ slides)

* "L3 - Chi tiết" - Đầy đủ nội dung, deep dive, code examples (18+ slides)

**Câu hỏi 3 - Ngôn ngữ** (header: "Language"):

* "Tiếng Việt" - Toàn bộ nội dung tiếng Việt (Recommended)

* "English" - Toàn bộ nội dung tiếng Anh

* "Song ngữ" - Title tiếng Anh, body tiếng Việt (phù hợp technical/academic)

**Câu hỏi 4 - Research bổ sung** (header: "Research"):

* "Chỉ dùng source" - Tạo slide 100% từ nội dung đầu vào, không tìm thêm

* "Research thêm" - Tìm thêm data, statistics, examples từ web để bổ sung slide

* "Auto" - Tự động: research nếu source ít thông tin (<500 words hoặc thiếu data/metrics), skip nếu đủ

**Logic đánh dấu Recommended cho câu hỏi 4:**

* Nếu source < 500 words HOẶC source chỉ có bullet points không context HOẶC thiếu data/metrics/examples → đánh dấu "Research thêm" là (Recommended)

* Nếu source >= 500 words VÀ có đầy đủ data/context → đánh dấu "Chỉ dùng source" là (Recommended)

## Step 1.5: Research bổ sung (Optional)

Chạy sau Step 1, trước Step 2. Quyết định dựa trên câu hỏi 4 ở Step 1.

**Khi nào chạy:**

* User chọn "Research thêm" → luôn chạy

* User chọn "Auto" → chạy NẾU source < 500 words HOẶC source thiếu data/metrics/examples cụ thể

* User chọn "Chỉ dùng source" → SKIP hoàn toàn, nhảy tới Step 2

**Process:**

1. Extract 3-5 topic keywords từ source input (dựa trên content type đã chọn)
2. Tạo 2-3 search queries phù hợp:

   * Query 1: `"{topic chính}" statistics data {năm hiện tại}` (tìm số liệu mới nhất)

   * Query 2: `"{topic chính}" trends insights` (tìm xu hướng, insights)

   * Query 3: `"{topic chính}" examples best practices` (tìm ví dụ, case studies)
3. Chạy WebSearch cho mỗi query
4. Extract findings relevant: statistics, data points, examples, quotes, trends
5. Lưu kết quả vào `{output_folder}/research-notes.md` theo format:

```markdown
# Research Notes — [Topic]

## Search Queries
1. [query 1]
2. [query 2]
3. [query 3]

## Findings

### Statistics & Data
- [stat 1] — Source: [url/name]
- [stat 2] — Source: [url/name]

### Trends & Insights
- [insight 1]
- [insight 2]

### Examples & Case Studies
- [example 1]
- [example 2]

## Selected for Slides
Items below sẽ được đưa vào Content Map với tag [R]:
1. [item] — lý do chọn
2. [item] — lý do chọn
```

1. Append selected items vào Content Map (Step 2) với prefix `[R]` để phân biệt source gốc vs researched
2. Thông báo user: "Research xong: tìm thấy X data points, Y insights. Đã lưu tại research-notes.md"

**Quy tắc research:**

* Chỉ lấy thông tin factual, có nguồn rõ ràng

* Ưu tiên: số liệu cụ thể > xu hướng > ví dụ > quotes

* KHÔNG thay thế nội dung source, chỉ BỔ SUNG

* Max 10 items đưa vào Content Map (tránh overwhelming)

* Research items trong outline phải ghi rõ "(Nguồn: research)" trong speaker notes hoặc content

## Visual Patterns per Content Type

Khi tạo slides, áp dụng visual patterns phù hợp với content type đã chọn:

| Content Type       | Visual Patterns                                                     | Recommended Slide Types                           |
| ------------------ | ------------------------------------------------------------------- | ------------------------------------------------- |
| Hướng dẫn/Giáo dục | Numbered step indicators, before/after comparison, warm decorations | content, comparison, statement (cho key concepts) |
| Business/Báo cáo   | Accent bars, data callout slides, conservative decorations          | content, metric (cho KPIs), comparison, summary   |
| Thuyết phục/Pitch  | Bold statement slides, high contrast, CTA emphasis                  | statement (30%+), metric, content, cta            |
| Technical/Process  | Code blocks, process flow indicators, comparison tables             | content, comparison, code, transition             |

## Auto Style Recommendation

Dựa trên content type, gợi ý style (user có quyền chọn khác):

| Content Type       | Primary Recommendation | Secondary         |
| ------------------ | ---------------------- | ----------------- |
| Hướng dẫn/Giáo dục | Warm Earth             | Clean Minimal     |
| Business/Báo cáo   | Clean Minimal          | Soft Professional |
| Thuyết phục/Pitch  | Bold Impact            | Corporate Dark    |
| Technical/Process  | Clean Minimal          | Corporate Dark    |

Khi hiển thị style choices, đánh dấu recommended style bằng "(Recommended)" dựa trên bảng trên.

## Step 2: Phân tích nội dung & Tạo outline (New mode)

1. Tạo output folder: `output/{slug}-{YYMMDD-HHmm}/` và subfolder `slides/`
2. Đọc `references/outline-rules.md` (relative to this skill folder) để nắm quy tắc outline
3. Áp dụng framework tương ứng với content type đã chọn ở Step 1 (xem Content Type → Framework Mapping trong outline-rules.md)
4. **Content Map** (xem "Content Map Rules" trong outline-rules.md):

   * Parse source → extract topics → assign priority (`must`/`should`/`nice`) theo detail level

   * Nếu Step 1.5 đã chạy → append research items vào Content Map với prefix `[R]` (xem outline-rules.md)

   * Lưu Content Map ra file `{output_folder}/content-map.md`
5. Phân tích nội dung theo detail level đã chọn (xem Detail Level Mapping + Content Selection Criteria trong outline-rules.md)
6. Tạo outline theo cấu trúc bắt buộc: Opening > Body > Closing. **Cross-check** với Content Map: mọi `must` topics phải xuất hiện, `should`/`nice` theo threshold
7. **Lưu outline** ra file `{output_folder}/outline.md` với metadata header (xem Outline File Format trong outline-rules.md)
8. Hiển thị outline cho user review (numbered list với slide titles + brief content description)
9. **Coverage Report** (xem "Coverage Report Rules" trong outline-rules.md):

   * Generate file `{output_folder}/coverage-report.md` mapping source topics → slides + omission justification

   * Thông báo cho user: tóm tắt 1 dòng coverage % + mention report file path
10. **Feedback loop**: Hỏi user "Outline OK? Bạn có muốn chỉnh sửa gì không?" bằng AskUserQuestion (header: "Outline review"):

* "OK, tiếp tục" - Chấp nhận outline, chuyển sang chọn style

* "Chỉnh sửa" - User sẽ mô tả thay đổi → cập nhật outline file + re-check coverage → show lại → hỏi lại

## Step 2.5: Reuse mode (khi đã có outline)

1. Đọc `{output_folder}/outline.md` — parse metadata header để lấy: content\_type, detail\_level, language, slug
2. Hiển thị tóm tắt cho user: "Reuse outline: {title}, {detail\_level}, {language}, {N} slides"
3. Tiếp tục chọn style ở Step 2.6

## Step 2.6: Chọn style (cả New và Reuse mode)

1. Scan `.claude/skills/proslide/styles/*.yaml` (exclude `_template.yaml`) để liệt kê styles
2. Kiểm tra `{output_folder}/slides/` xem đã có PPTX nào chưa → show user "(đã tạo)" bên cạnh style đã dùng
3. Nếu chỉ có 1 style → tự động chọn, thông báo cho user. Nếu 2+ styles → hỏi user bằng AskUserQuestion (header: "Style"): "Chọn style:" + list style names + đánh dấu styles đã tạo

## Step 3: Tạo slide

1. Đọc file YAML style đã chọn từ `styles/` folder (relative to this skill folder)
2. Đọc `references/slide-templates.md` (relative to this skill folder) để nắm HTML patterns cho từng slide type
3. Đọc outline từ `{output_folder}/outline.md` (nếu Reuse mode) hoặc từ context (nếu vừa tạo)
4. Chuẩn bị design brief dựa trên outline + style YAML:

   * Slide dimensions: `layout.width` x `layout.height` (default 720x405 for 16:9)

   * Font families: `fonts.heading` cho titles, `fonts.body` cho body text

   * Font sizes: từ `fonts.*` và `slide_styles.*` (slide\_styles override global fonts)

   * Colors: tất cả values từ `colors.*` và `slide_styles.*`

   * Spacing: `layout.margin`, `layout.line_spacing`, `layout.bullet_spacing`
5. **Activate** **`pptx`** **skill** trong cùng agent context. Cung cấp:

   * Design brief (colors, fonts, dimensions, **decorations** từ bước 4)

   * HTML templates cho từng slide type (từ `references/slide-templates.md`)

   * Nội dung từng slide theo outline (title, body content, slide type)

   * Ngôn ngữ từ outline metadata

   * Visual patterns phù hợp content type (xem bảng Visual Patterns ở trên)

   * Yêu cầu: text-only slides, không hình ảnh, không chart

   * **HTML constraints** (xem section bên dưới) - pptx skill PHẢI tuân thủ khi tạo HTML

   * **Output path**: `{output_folder}/slides/{slug}-{style-name}.pptx`
6. Sau khi pptx skill tạo xong PPTX, validate bằng python-pptx: kiểm tra số slides, nội dung text, font sizes. Sửa nếu có lỗi.
7. Thông báo output:

   * File PPTX path

   * Output folder path (nhắc user có thể reuse outline: `/proslide` + chỉ folder path)

## HTML Constraints cho pptx skill (CRITICAL)

Khi activate pptx skill, PHẢI truyền các constraints sau. pptx skill tạo HTML và convert sang PPTX, nên rules này áp dụng cho HTML mà pptx skill generate:

* **KHÔNG dùng nested** **`<ul>`/`<ol>`**: html2pptx render mỗi `<ul>` thành shape riêng biệt → nested lists gây overlap text. Thay vào đó:

  * Flatten list: gộp sub-items vào main bullet dùng " — " hoặc inline text

  * Hoặc dùng `<p>` với margin-left cho sub-items thay vì nested `<ul>`

  * SAI: `<ul><li>Main</li><ul><li>Sub</li></ul></ul>` → OVERLAP

  * ĐÚNG: `<ul><li><b>Main:</b> sub-detail 1, sub-detail 2</li></ul>`

  * ĐÚNG: `<ul><li>Main</li></ul><p style="margin-left:44pt; color:#7F8C8D;">— Sub detail</p>`

* **Heading + 1 list per slide**: Mỗi slide nên có 1 heading element + tối đa 1 `<ul>` hoặc `<ol>`. Nhiều list elements cùng level sẽ tạo nhiều shapes chồng nhau.

* **Sub-items trong L2/L3**: Dùng inline formatting thay nested list

  * Pattern: `<li><b>Label:</b> detail text (VD: example)</li>`

  * Hoặc: `<li>Main point — sub-detail</li>`

## Important Notes

* Chỉ tạo text-only slides, không hình ảnh

* Chỉ dùng web-safe fonts hỗ trợ Vietnamese: Arial, Tahoma, Verdana

* KHÔNG dùng: Impact, Courier New (Vietnamese rendering kém)

* Chi tiết quy tắc outline: xem `references/outline-rules.md`

* HTML templates cho slide types: xem `references/slide-templates.md`

* Style YAML files nằm trong `styles/` folder, template ở `styles/_template.yaml`

* Font size priority: `slide_styles.*` override `fonts.*` global values

* **Decorations**: Mỗi style có section `decorations` định nghĩa accent elements (underline, topbar, left bar, etc.). pptx skill PHẢI đọc và áp dụng decorations khi tạo HTML

* **Projector contrast**: Đảm bảo text/background contrast ratio >= 4.5:1 (WCAG AA). Accent colors trên background phải readable trên projector chất lượng thấp. Nếu phát hiện contrast kém, điều chỉnh shade sáng/tối hơn

* **5 styles available**: Clean Minimal, Corporate Dark, Warm Earth, Bold Impact, Soft Professional

