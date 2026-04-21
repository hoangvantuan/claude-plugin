---
name: writing-structures
description: "Thư viện khung bài viết (structures) và content frameworks. Use this skill whenever the user asks 'có structure nào?', 'dùng khung Story Arc', 'viết theo PAS framework', 'apply BLUF-Evidence', 'cấu trúc 5 phần social', hoặc bất cứ khi nào task viết lách cần chọn/áp dụng một khung bài có sẵn. Cũng kích hoạt khi cần tra cứu catalog trước khi viết để chọn xương sống cho bài. Đây KHÔNG phải skill viết bài — skill này chỉ cung cấp structure/framework definitions làm nguyên liệu cho skill/AI khác áp dụng."
disable-model-invocation: true
---

# Writing Structures

Thư viện khung bài và content framework cho viết lách, chia 2 category:

- **Structures** — xương sống bài dài (blog article, essay). Mỗi structure định nghĩa cách tổ chức nội dung từ mở đến kết.
- **Frameworks** — công thức viết ngắn hơn (Problem-Agitate-Solution, Inverted Pyramid...) có thể áp dụng cho bài blog, bài social, hoặc section trong bài dài.

Mỗi file tài liệu độc lập để AI hoặc skill khác load khi cần.

## Structures có sẵn

Mỗi structure (trừ `social-5-parts`) có 2 variant: `main` (đầy đủ) và `compact` (rút gọn cho context budget hẹp).

| Structure       | Slug              | Tóm tắt 1 dòng                                                                             | Main file                                                                 |
| --------------- | ----------------- | ------------------------------------------------------------------------------------------ | ------------------------------------------------------------------------- |
| Story Arc       | `story-arc`       | Cung truyện: setup → rising action → climax → resolution. Hợp narrative, personal journey. | [structures/story-arc.md](references/structures/story-arc.md)             |
| BLUF-Evidence   | `bluf-evidence`   | Kết luận trước, chứng minh sau. Hợp data-driven, news-style, bài ngắn gọn.                 | [structures/bluf-evidence.md](references/structures/bluf-evidence.md)     |
| Building Blocks | `building-blocks` | Xây dựng từng bước: khái niệm đơn → lắp ghép → hệ thống đầy đủ. Hợp giáo dục.              | [structures/building-blocks.md](references/structures/building-blocks.md) |
| Depth-Practice  | `depth-practice`  | Chiều sâu trước, thực hành sau. Hợp bài giải thích triết lý kèm cách áp dụng.              | [structures/depth-practice.md](references/structures/depth-practice.md)   |
| Five Layers     | `five-layers`     | 5 tầng đào sâu từ bề mặt xuống gốc. Hợp phân tích đa chiều một hiện tượng.                 | [structures/five-layers.md](references/structures/five-layers.md)         |
| Master-Student  | `master-student`  | Đối thoại thầy-trò, format C:/T:. Hợp triết lý, chánh niệm qua hỏi-đáp.                    | [structures/master-student.md](references/structures/master-student.md)   |
| Spiral Return   | `spiral-return`   | Xoáy ốc: quay lại chủ đề nhiều lần, mỗi lần sâu hơn. Hợp reflective, meditative.           | [structures/spiral-return.md](references/structures/spiral-return.md)     |
| Adaptive        | `adaptive`        | Linh hoạt, không khung cố định. Dùng khi content mixed không fit structure nào.            | [structures/adaptive.md](references/structures/adaptive.md)               |
| Social 5-Parts  | `social-5-parts`  | Cấu trúc 5 phần cho social post: Tiêu đề → Hook → Tension → Escalation → Turn. 200-500 từ. | [structures/social-5-parts.md](references/structures/social-5-parts.md)   |


Compact variant nằm cùng thư mục với suffix `-compact.md` (VD: `structures/story-arc-compact.md`). File `structure-template.md` là template để soạn structure mới.

## Frameworks có sẵn

5 framework ngắn hơn trong 1 file duy nhất: [frameworks.md](references/frameworks.md).

| Framework        | Slug          | Công thức                                    | Best for                                                     |
| ---------------- | ------------- | -------------------------------------------- | ------------------------------------------------------------ |
| PAS              | `pas`         | Problem → Agitate → Solution                 | Opinion posts, bài cần drive action, Facebook Controversial. |
| Inverted Pyramid | `pyramid`     | Lead (kết luận) → Body (detail) → Background | Deep Analysis blog, data-driven, news-style.                 |
| Step-by-step     | `step`        | Setup → Step 1..N → Result → Troubleshooting | How-to Guide, tutorial.                                      |
| SAR              | `sar`         | Situation → Action → Result                  | Case Study blog, Hook + Story social post.                   |
| Progressive      | `progressive` | Simple → Intermediate → Advanced → Expert    | Explainer, bài giáo dục, technical cho non-technical.        |


## Cách dùng

### Tra cứu / chọn structure hoặc framework

Khi user hỏi "có structure/framework nào?":

1. Hiển thị bảng tương ứng.
2. Nếu user chưa chọn, hỏi user muốn load cái nào + mô tả ngắn khi nào dùng.

### Load structure

Khi user yêu cầu "dùng structure X" / "viết theo khung Y":

1. Tra slug trong bảng Structures → đường dẫn file.
2. `Read` file structure đó (main hoặc compact tùy context budget).
3. Nắm các phần chính: Khi nào dùng / Các phase / Ví dụ / Anti-patterns.
4. Áp dụng vào task viết.

### Load framework

Khi user yêu cầu "apply framework X":

1. `Read` file [frameworks.md](references/frameworks.md).
2. Tìm section tương ứng (PAS / Inverted Pyramid / Step-by-step / SAR / Progressive Disclosure).
3. Áp dụng các bước theo công thức.

### Thêm structure mới

1. Dùng [structures/structure-template.md](references/structures/structure-template.md) làm base.
2. Soạn 2 file: `<slug>.md` (main) và `<slug>-compact.md` (rút gọn).
3. Lưu vào `references/structures/`.
4. Thêm dòng mới vào bảng **Structures có sẵn**.

### Thêm framework mới

1. Thêm section mới vào [frameworks.md](references/frameworks.md) theo format hiện có: Giải thích / Steps / Best for / Example.
2. Thêm dòng mới vào bảng **Frameworks có sẵn**.

## Nguyên tắc

- **Thư viện, không phải writer**: skill này chỉ cung cấp structure/framework definitions. KHÔNG tự sinh ra bài viết.
- **Độc lập tuyệt đối**: skill này KHÔNG load/invoke/reference skill khác. Không có chuyện "load style-library rồi mới xuất". User (hoặc skill workflow khác) tự quyết compose gì với nhau.
- **Single source of truth**: mỗi structure/framework một định nghĩa duy nhất trong skill này.
- **Structure ≠ content**: structure chỉ định cách tổ chức, KHÔNG quyết định giọng, persona, hay đối tượng đọc. Những chiều đó thuộc về `style-library` và `writing-context` — user tự compose.
