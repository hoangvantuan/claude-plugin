---
name: outline-writer
description: "Phân tích nội dung và tạo outline thuần nội dung (sequence of sections; thesis, key arguments, evidence). KHÔNG quyết định media (slide/blog/doc), KHÔNG quy định cách viết/tone/style — đó là việc của writer. Output: outline.md."
disable-model-invocation: true
---

# Outline Writer — Content Analysis & Outline Generator

Tạo outline từ content input. Outline là cấu trúc nội dung trừu tượng (sequence of sections, mỗi section = 1 ý/insight); writer sau này chuyển thành slide deck, blog post, hoặc documentation tùy media. Vietnamese default.

## Scope

Outline-writer chịu trách nhiệm **CẤU TRÚC NỘI DUNG**: thesis, key arguments, topics, mối quan hệ giữa topics, priority, sequencing, framework cấu trúc.

Outline-writer KHÔNG chịu trách nhiệm về **CÁCH VIẾT / TONE / STYLE**: font size, layout, độ dài câu/bullet, anti-filler, voice, từ ngữ. Cũng KHÔNG quyết định **MEDIA**: outline không nói "đây là slide deck" hay "đây là blog post" — đó là decision của writer.

Nguyên tắc: **outline đưa ra ý gì, không đưa ra cách viết ý đó.**

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
4. Hỏi user bằng AskUserQuestion (3 câu hỏi trong 1 lần):

**Câu hỏi 1 - Mức độ chi tiết** (header: "Detail level"):

- "L1 - Tổng quan" - Chỉ ý chính
- "L2 - Cân bằng" - Ý chính + giải thích + ví dụ minh họa
- "L3 - Chi tiết" - Đầy đủ nội dung, deep dive, code examples

**Câu hỏi 2 - Ngôn ngữ** (header: "Language"):

- "Tiếng Việt" - Toàn bộ nội dung tiếng Việt (Recommended)
- "English" - Toàn bộ nội dung tiếng Anh
- "Song ngữ" - Title tiếng Anh, body tiếng Việt

**Câu hỏi 3 - Research bổ sung** (header: "Research"):

- "Chỉ dùng source" - 100% từ nội dung đầu vào, không tìm thêm
- "Research thêm" - Tìm thêm data, statistics, examples từ web
- "Auto" - Tự động: research nếu source ít thông tin, skip nếu đủ

**Logic Recommended cho câu hỏi 3:** Source < 500 words HOẶC thiếu data/metrics → recommend "Research thêm". Source >= 500 words VÀ đủ data → recommend "Chỉ dùng source".

5. Tiếp Step 1B.

### Step 1B: Audience Mental Model (Tự động — không hỏi user)

Auto-suy luận từ topic + context của source.

Tự suy luận và giữ trong context:

```
AUDIENCE MENTAL MODEL:
- Prior knowledge: [Audience đã biết gì về topic này?]
- Existing beliefs: [Họ đang tin gì? — có thể đúng hoặc sai]
- Knowledge gap: [Họ cần biết thêm gì?]
- Belief shift: [Sau outline, họ cần thay đổi suy nghĩ gì?]
- Resistance point: [Rào cản lớn nhất khi tiếp nhận nội dung?]
```

**Cách Mental Model ảnh hưởng outline:**

- Audience đã tin X (sai) → cần section phá vỡ giả định trước khi trình bày thesis
- Audience thiếu kiến thức Y → cần scaffolding từ cái đã biết sang cái mới
- Audience kháng cự thay đổi → cần evidence mạnh trước kết luận, không kết luận trước
- Knowledge gap nhỏ → có thể dùng L1, gap lớn → cần L2-L3

## Step 2: Research bổ sung (Optional)

Quyết định dựa trên câu hỏi Research ở Step 1:

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

## Step 3: Thesis Extraction (Bắt buộc)

Bước quan trọng nhất — xác định core message trước khi tạo outline.

1. Đọc toàn bộ source (và research notes nếu có)
2. Trả lời: **"Nếu audience chỉ nhớ 1 điều duy nhất từ nội dung này, đó là gì?"** → **Thesis**
3. Trả lời: **"3 arguments/evidence nào mạnh nhất chứng minh thesis?"** → **Key Arguments**
4. Trả lời: **"Audience cần thay đổi gì sau khi tiếp nhận nội dung?"** → **Intended Transformation**:
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

## Step 4: Phân tích nội dung & Tạo outline

1. Tạo output folder: `{CWD}/outline-writer/{slug}-{YYMMDD-HHmm}/`
2. Đọc references: [content-map-rules](references/content-map-rules.md), [outline-structure](references/outline-structure.md), [detail-levels](references/detail-levels.md), [framework-mapping](references/framework-mapping.md), [report-format](references/report-format.md)
3. **Framework auto-selection**: đọc source + Mental Model → suy luận content nature (giáo dục / business / pitch / technical) → chọn framework tương ứng (xem [framework-mapping](references/framework-mapping.md)). Ghi framework đã chọn vào YAML frontmatter
4. **Content Analysis Map**: Parse source → extract topics → map relationships → assign priority → link to Thesis. Lưu `{CWD}/{output_folder}/content-map.md`
5. Phân tích nội dung theo [detail-levels](references/detail-levels.md) + Audience Mental Model
6. Tạo outline **xây quanh Thesis**: Opening giới thiệu core message > Body chứng minh bằng Key Arguments > Closing khẳng định thesis + CTA. Áp dụng Cognitive Sequencing + Narrative Arc + Content Principles. Cross-check Content Analysis Map: mọi `must` topics phải xuất hiện, mọi Key Arguments phải có evidence. **Không quy định cách viết** (font, độ dài bullet, layout) và **không quy định media** (slide/blog/doc) trong outline.
7. **Lưu outline** ra `{CWD}/{output_folder}/outline.md` với YAML frontmatter (xem format trong [report-format](references/report-format.md))
8. Hiển thị outline cho user review
9. **Coverage & Quality Report**: Generate `{CWD}/{output_folder}/coverage-report.md`
10. **Feedback loop**: Hỏi "Outline OK?" (AskUserQuestion, header: "Outline review"):
  - "OK, tiếp tục" - Chấp nhận outline
    - "Chỉnh sửa" - User mô tả thay đổi → cập nhật → hỏi lại
11. Khi approved, thông báo: "Outline xong tại `{CWD}/{output_folder}/outline.md`."

**Nguyên lý cốt lõi**: Outline tốt = tấm bản đồ đi từ điểm A (audience chưa biết) đến điểm B (insight cốt lõi), KHÔNG phải danh mục liệt kê tất cả những gì source nói.