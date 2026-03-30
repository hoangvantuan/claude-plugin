---
name: outline-writer
description: "Phân tích nội dung và tạo outline chuyên nghiệp. Sử dụng khi user yêu cầu tạo outline, phân tích content, lập dàn ý cho presentation/blog/document, hoặc gọi /outline-writer. Output: outline.md với YAML frontmatter."
disable-model-invocation: true
---

# Outline Writer — Content Analysis & Outline Generator

Tạo professional outline từ content input. Hỗ trợ nhiều output types: presentation slides, blog post, documentation. Vietnamese default.

## Output Folder Structure

```
{CWD}/outline-writer/
└── {slug}-{YYMMDD-HHmm}/
    ├── outline.md
    ├── content-map.md
    ├── coverage-report.md
    └── research-notes.md (nếu có research)
```

**Naming rules:**

- `{slug}`: kebab-case từ topic chính (max 30 chars)
- `{YYMMDD-HHmm}`: timestamp lúc tạo folder

## Step 1: Tiếp nhận nội dung & Cấu hình

1. Đọc input từ user: text trực tiếp hoặc file path (.md, .txt, .pdf)
2. Nếu input là file path, đọc nội dung file
3. Phân tích sơ bộ: topic, length, complexity
4. Hỏi user bằng AskUserQuestion (4 câu hỏi trong 1 lần):

**Câu hỏi 1 - Output type** (header: "Output type"):

- "Presentation slides" - Outline cho slide deck (tiếp tục hỏi audience & framework ở Step 1.1)
- "Blog post" - Outline cho bài viết blog
- "Documentation/Report" - Outline cho tài liệu/báo cáo

**Câu hỏi 2 - Mức độ chi tiết** (header: "Detail level"):

- "L1 - Tổng quan" - Chỉ ý chính, bullet ngắn gọn (5+ items)
- "L2 - Cân bằng" - Ý chính + giải thích + ví dụ minh họa (10+ items)
- "L3 - Chi tiết" - Đầy đủ nội dung, deep dive, code examples (18+ items)

**Câu hỏi 3 - Ngôn ngữ** (header: "Language"):

- "Tiếng Việt" - Toàn bộ nội dung tiếng Việt (Recommended)
- "English" - Toàn bộ nội dung tiếng Anh
- "Song ngữ" - Title tiếng Anh, body tiếng Việt

**Câu hỏi 4 - Research bổ sung** (header: "Research"):

- "Chỉ dùng source" - 100% từ nội dung đầu vào, không tìm thêm
- "Research thêm" - Tìm thêm data, statistics, examples từ web
- "Auto" - Tự động: research nếu source ít thông tin, skip nếu đủ

**Logic Recommended cho câu hỏi 4:** Source < 500 words HOẶC thiếu data/metrics → recommend "Research thêm". Source >= 500 words VÀ đủ data → recommend "Chỉ dùng source".

5. Nếu output_type = "Presentation slides" → hỏi thêm content type (AskUserQuestion, header: "Content type"):
  - "Hướng dẫn/Giáo dục" - Giải thích khái niệm, tutorial (Gagné + scaffolding)
  - "Business/Báo cáo" - Phân tích, đề xuất, báo cáo (Pyramid Principle)
  - "Thuyết phục/Pitch" - Bán ý tưởng, pitch sản phẩm (PAS + Sparkline)
  - "Technical/Process" - Quy trình, kiến trúc, so sánh kỹ thuật (SCR + step-by-step)

## Step 1.1: Audience & Framework Selection (Chỉ khi output_type = "Presentation slides")

Hỏi user bằng AskUserQuestion (1-2 câu hỏi tùy content type):

**Câu hỏi 1 — Audience** (header: "Audience", luôn hỏi):

- "Executive/Decision maker" - C-level, cần bottom-line upfront, metrics, ngắn gọn
- "Technical team" - Engineers, developers — jargon OK, chi tiết kỹ thuật
- "Mixed/General" - Đa dạng trình độ — cần giải thích thuật ngữ, ví dụ cụ thể
- "Workshop/Hands-on" - Đào tạo thực hành — interactive, knowledge checks

**Câu hỏi 2 — Framework** (header: "Framework", chỉ hỏi khi content type = "Business/Báo cáo"):

- "Pyramid Principle" - Kết luận trước, supporting arguments sau (Recommended khi audience = Mixed)
- "SCQA" - Situation → Complication → Question → Answer (Recommended khi audience = Executive)

**Audience ảnh hưởng outline:**

| Audience  | Ảnh hưởng                                              |
| --------- | ------------------------------------------------------ |
| Executive | Ưu tiên metrics, bottom-line upfront, max 12-15 slides |
| Technical | Sequential IA, jargon OK, code examples, L2-L3 phù hợp |
| Mixed     | Thêm definition cho thuật ngữ, ví dụ concrete bắt buộc |
| Workshop  | Force Gagné framework, thêm knowledge check items      |

## Step 1.2: Audience Mental Model (Silent — không hỏi user)

Áp dụng cho mọi output type. Với blog/doc: suy luận từ topic + context. Với presentation: suy luận từ audience type đã chọn ở Step 1.1.

Sau khi biết audience type, **tự suy luận** (KHÔNG hỏi user) Audience Mental Model và giữ trong context:

```
AUDIENCE MENTAL MODEL:
- Prior knowledge: [Audience đã biết gì về topic này?]
- Existing beliefs: [Họ đang tin gì? — có thể đúng hoặc sai]
- Knowledge gap: [Họ cần biết thêm gì?]
- Belief shift: [Sau outline, họ cần thay đổi suy nghĩ gì?]
- Resistance point: [Rào cản lớn nhất khi tiếp nhận nội dung?]
```

**Cách Mental Model ảnh hưởng outline:**

- Nếu audience đã tin X (sai) → cần section phá vỡ giả định trước khi trình bày thesis
- Nếu audience thiếu kiến thức Y → cần scaffolding từ cái đã biết sang cái mới
- Nếu audience kháng cự thay đổi → cần evidence mạnh trước kết luận, không kết luận trước
- Nếu knowledge gap nhỏ → có thể dùng L1, gap lớn → cần L2-L3

**Nguyên lý**: Truyền đạt hiệu quả = nói đúng thứ audience cần nghe, theo đúng thứ tự họ sẵn sàng tiếp nhận. Mental Model định hướng NỘI DUNG, không chỉ FORMAT.


## Step 1.5: Research bổ sung (Optional)

Chạy sau Step 1, trước Step 2. Quyết định dựa trên câu hỏi Research ở Step 1.

**Khi nào chạy:**

- User chọn "Research thêm" → luôn chạy
- User chọn "Auto" → chạy NẾU source < 500 words HOẶC thiếu data/metrics
- User chọn "Chỉ dùng source" → SKIP hoàn toàn

**Process:**

1. Extract 3-5 topic keywords từ source
2. Tạo 2-3 search queries: `"{topic}" statistics data {năm}`, `"{topic}" trends insights`, `"{topic}" examples best practices`
3. Chạy WebSearch cho mỗi query
4. Extract findings relevant: statistics, data points, examples, quotes
5. Lưu kết quả vào `{CWD}/{output_folder}/research-notes.md`
6. Append selected items vào Content Analysis Map với prefix `[R]`
7. Thông báo user: "Research xong: X data points, Y insights. Đã lưu tại research-notes.md"

**Quy tắc:** Chỉ thông tin factual có nguồn. Ưu tiên: số liệu > xu hướng > ví dụ. KHÔNG thay thế source, chỉ BỔ SUNG. Max 10 items.

## Step 1.7: Thesis Extraction (Bắt buộc cho mọi output type)

Chạy sau Research (nếu có), trước Step 2. Đây là bước **quan trọng nhất** — xác định core message trước khi tạo outline.

**Process:**

1. Đọc toàn bộ source (và research notes nếu có)
2. Trả lời: **"Nếu audience chỉ nhớ 1 điều duy nhất từ nội dung này, đó là gì?"** → Đây là **Thesis** (core message)
3. Trả lời: **"3 arguments/evidence nào mạnh nhất chứng minh thesis?"** → Đây là **Key Arguments**
4. Trả lời: **"Audience cần thay đổi gì sau khi tiếp nhận nội dung?"** → Đây là **Intended Transformation**:
   - "không biết X" → "hiểu X" (educate)
   - "tin X sai" → "tin X đúng" (persuade)
   - "không hành động" → "hành động Y" (activate)
5. Giữ trong context, KHÔNG show cho user riêng — thesis sẽ xuất hiện trong outline và quality report

**Thesis format (internal):**

```
=== THESIS ===
Core message: [1 câu assertion — KHÔNG phải topic label]
Key arguments:
  1. [Argument 1]
  2. [Argument 2]
  3. [Argument 3]
Intended transformation: [educate/persuade/activate] — [mô tả cụ thể]
=== END THESIS ===
```

**Quy tắc Thesis:**

- Thesis PHẢI là assertion (nhận định có thể đúng/sai), KHÔNG phải topic label
  - SAI: "Phương pháp Agile trong phát triển phần mềm"
  - ĐÚNG: "Agile giúp giảm 60% thời gian delivery nhưng đòi hỏi thay đổi văn hóa toàn tổ chức"
- Thesis phải kiểm chứng được bằng evidence từ source
- Key arguments PHẢI có evidence trong source hoặc research
- Nếu source không có thesis rõ ràng (VD: tài liệu kỹ thuật thuần túy) → thesis = mục tiêu chính mà audience cần đạt được

## Visual Patterns per Content Type (Chỉ khi output_type = "Presentation slides")

| Content Type       | Visual Patterns                         | Recommended Slide Types                     |
| ------------------ | --------------------------------------- | ------------------------------------------- |
| Hướng dẫn/Giáo dục | Numbered steps, before/after comparison | content, comparison, statement, quote       |
| Business/Báo cáo   | Accent bars, data callout               | content, metric, comparison, table, summary |
| Thuyết phục/Pitch  | Bold statements, high contrast, CTA     | statement (30%+), metric, quote, cta        |
| Technical/Process  | Code blocks, process flow, Mermaid      | content, comparison, code, diagram, table   |


## Step 2: Phân tích nội dung & Tạo outline

1. Tạo output folder: `{CWD}/outline-writer/{slug}-{YYMMDD-HHmm}/`
2. Đọc `references/outline-rules.md` (relative to this skill folder) để nắm quy tắc outline
3. **Framework selection:**
  - Presentation: áp dụng framework tương ứng content type (xem Content Type → Framework Mapping trong outline-rules.md). Nếu audience = "Workshop", override sang Gagné
  - Blog/Doc: sắp xếp logic — Introduction → Body sections (clustered) → Conclusion
4. **Content Analysis Map**: Parse source → extract topics → **map relationships** → assign priority (`must`/`should`/`nice`) theo detail level → **link topics to Key Arguments từ Thesis**. Nếu Step 1.5 đã chạy → append items `[R]`. Lưu `{CWD}/{output_folder}/content-map.md`. Chi tiết format: xem Content Analysis Map Rules trong outline-rules.md
5. Phân tích nội dung theo detail level + audience-aware adjustments (nếu presentation) + **Audience Mental Model** (nếu có). Xem Detail Level Mapping + Audience-Aware Adjustments + Content Principles trong outline-rules.md
6. Tạo outline **xây quanh Thesis**: Opening giới thiệu core message > Body chứng minh bằng Key Arguments > Closing khẳng định thesis + CTA. Áp dụng Cognitive Sequencing + Narrative Arc + **Content Principles** (xem outline-rules.md). Cross-check Content Analysis Map: mọi `must` topics phải xuất hiện, mọi Key Arguments phải có evidence
7. **Lưu outline** ra `{CWD}/{output_folder}/outline.md` với YAML frontmatter:
  ```yaml
   ---
   title: "Tên outline"
   slug: "ten-outline"
   output_type: "presentation" | "blog" | "doc"
   content_type: "..." # chỉ khi presentation
   framework: "..." # chỉ khi presentation
   audience: "..." # chỉ khi presentation
   detail_level: "L1" | "L2" | "L3"
   language: "vi" | "en" | "bilingual"
   source: "mô tả source input"
   thesis: "core message 1 câu"
   intended_transformation: "educate" | "persuade" | "activate"
   created: "YYYY-MM-DD HH:mm"
   total_slides: N # hoặc total_sections cho blog/doc
   ---
  ```
8. Hiển thị outline cho user review
9. **Coverage & Quality Report**: Generate `{CWD}/{output_folder}/coverage-report.md` bao gồm cả Coverage Report VÀ Quality Report (xem Coverage Report Rules + Quality Report Rules trong outline-rules.md)
10. **Feedback loop**: Hỏi "Outline OK?" (AskUserQuestion, header: "Outline review"):
  - "OK, tiếp tục" - Chấp nhận outline
    - "Chỉnh sửa" - User mô tả thay đổi → cập nhật → hỏi lại
11. Khi approved, thông báo tùy output_type:
  - Blog/Doc: "Outline xong tại `{CWD}/{output_folder}/outline.md`."

## Important Notes

- Chi tiết quy tắc outline: xem `references/outline-rules.md`
- Outline rules áp dụng chủ yếu cho presentation. Blog/doc dùng subset rules phù hợp (Content Analysis Map, Coverage & Quality Report, Cognitive Sequencing, Content Principles)
- **Thesis Extraction**, Content Analysis Map, Coverage & Quality Report bắt buộc cho mọi output type
- **Nguyên lý cốt lõi**: Outline tốt = tấm bản đồ đi từ điểm A (audience chưa biết) đến điểm B (insight cốt lõi), KHÔNG phải danh mục liệt kê tất cả những gì source nói
