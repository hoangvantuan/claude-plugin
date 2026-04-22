---
name: style-writer
description: "Skill viết lách có 2 workflow: (1) Analyze — bóc tách DNA văn phong từ corpus bài viết để tạo style guide markdown, (2) Library — tra cứu/load style guide có sẵn (personas, archetypes, voices) để áp dụng khi viết. Kích hoạt khi user nhắc: 'phân tích văn phong', 'clone giọng văn', 'tạo style guide', 'stylometry', 'fingerprint viết lách', 'phân tích cách viết của X', 'có style/persona/archetype/voice nào?', 'liệt kê style guide', 'load style X', 'dùng văn phong Y', 'apply archetype Z', 'viết theo giọng W', hoặc bất cứ task viết lách nào cần chọn/phân tích style."
disable-model-invocation: true
---

# Style Writer

Skill quản lý văn phong viết lách, gồm 2 workflow:

| Workflow | Mục đích | Khi nào dùng |
|----------|----------|-------------|
| **Analyze** | Bóc tách DNA văn phong từ corpus → tạo style guide | User muốn phân tích cách viết, tạo style guide mới |
| **Library** | Tra cứu/load style guide có sẵn | User muốn xem catalog, load style, áp dụng khi viết |

Khi user gọi skill này, xác định workflow phù hợp dựa trên ngữ cảnh. Nếu không rõ, hỏi user.

---

## Workflow 1: Analyze

Bóc tách DNA văn phong từ tập bài viết của MỘT tác giả, trả về style guide markdown theo template cố định.

### Vai trò

Chuyên gia phân tích văn phong (stylometry & literary analysis) 15 năm kinh nghiệm. Mỗi đặc điểm phát biểu phải có trích dẫn nguyên văn từ corpus. Không bằng chứng → không ghi nhận.

**Bạn KHÔNG generate bài mới, KHÔNG so sánh tác giả, KHÔNG đánh giá hay/dở. Chỉ mô tả khách quan hình thức cách viết, có bằng chứng.**

### Bước 1. Thu thập corpus (Văn)

User có thể cung cấp corpus theo 3 cách. Detect và xử lý tương ứng:

**a. File/folder local** — user cho path `.txt`/`.md` hoặc folder.
- File đơn: `Read` file.
- Folder: `Glob` pattern `**/*.{md,txt}`, `Read` từng file, nối lại phân tách bởi `---`.

**b. Paste trực tiếp** — user dán nội dung vào chat, bài phân tách bởi `---`.
- Không cần load file, dùng luôn nội dung trong tin nhắn.

**c. URL (Substack/blog)** — user cho URL newsletter hoặc bài riêng lẻ.
- Nếu là Substack: ưu tiên dùng skill `substack-tools` (có `substack_crawl.py`).
- Nếu là blog khác: dùng `WebFetch` từng URL, extract nội dung main article.
- Nếu là URL mục lục (archive page): fetch trước để lấy danh sách URL bài, rồi fetch từng bài.

**Kiểm tra cỡ corpus**: tối thiểu 3 bài để có pattern đáng tin. Dưới 3 bài → báo user biết giới hạn, vẫn làm nhưng ghi rõ "dữ liệu hạn chế" trong output.

**Hỏi tên tác giả** nếu user chưa cung cấp — dùng cho tên file output và heading.

### Bước 2. Phân tích 8 chiều (Tư)

Đọc `references/analysis-dimensions.md` để có guide chi tiết từng chiều với ví dụ cụ thể cần tìm gì.

Tóm tắt 8 chiều:

1. **Giọng điệu & persona** — Formal level (1-5), tone, ngôi xưng, distance với reader, thái độ.
2. **Cấu trúc bài** — Pattern mở bài, xương sống triển khai, pattern kết bài.
3. **Nhịp & độ dài câu** — Độ dài TB, câu cụt, tỷ lệ đơn/phức/ghép, thủ pháp nhịp.
4. **Từ vựng đặc trưng (fingerprint)** — 10-20 từ/cụm tác giả hay dùng, slang, thuật ngữ, filler.
5. **Kỹ thuật tu từ** — Metaphor domain, nguồn ví dụ, cách chuyển đoạn, cách dùng hài.
6. **Format & typography** — Heading, list, bold, đoạn dài, emoji, em-dash, whitespace.
7. **Tư duy & logic** — Pattern lập luận, xử lý counter-argument, tuyệt đối vs. nuance.
8. **Quirks cá nhân** — Thói quen riêng, tagline, cách đặt câu hỏi, pattern lặp ≥3 lần.

**Nguyên tắc cốt lõi**: không bằng chứng → không ghi nhận. Pattern phải lặp ≥2 lần ở ≥2 bài. Thiếu data → ghi "Không đủ dữ liệu", không bịa. Chi tiết evidence rules (trích dẫn nguyên văn ≤30 từ, tham chiếu bài, v.v.) xem `references/anti-patterns.md` mục A.

### Bước 3. Xuất style guide (Tu)

Đọc `references/output-template.md` để lấy template chính xác.

**Tên file output**: `references/personas/<ten-tac-gia-kebab-case>.md`
- VD tác giả "Nguyễn Văn A" → `references/personas/nguyen-van-a.md`.
- Nếu file đã tồn tại, hỏi user: ghi đè, đổi tên (thêm date suffix), hay skip.

**Sau khi ghi file**, cập nhật bảng **Personas có sẵn** trong SKILL.md này (thêm dòng mới), rồi báo user:

```
Đã tạo: [path file]
- Bản chất: [1 câu ≤25 từ mô tả văn phong]
- Signature phrases: "[cụm 1]", "[cụm 2]", "[cụm 3]"
- Độ tin cậy: [Rất thấp / Trung bình / Khá / Cao] — [N bài]
```

### Ràng buộc và self-check (Analyze)

Mọi ràng buộc (must NOT) và checklist verify cuối nằm trong `references/anti-patterns.md`:

- **Mục A-F**: anti-patterns phân nhóm (bằng chứng, form vs content, đánh giá, so sánh, cỡ mẫu, template). Đọc khi cần hiểu lỗi cụ thể.
- **Mục H**: checklist 12 ô cuối cùng trước khi ghi file. Đi qua từng ô, fail bất kỳ ô nào → sửa trước khi `Write`. Không ghi draft cẩu thả rồi hứa "sẽ sửa sau".

### Cỡ corpus và độ tin cậy

| Số bài | Độ tin cậy | Ghi chú khi xuất |
|--------|------------|-------------------|
| 1-2    | Rất thấp   | Ghi rõ "style guide sơ bộ, cần thêm corpus" |
| 3-5    | Trung bình | Đủ pattern cơ bản, một số chiều có thể thiếu |
| 6-10   | Khá       | Đủ cho hầu hết chiều |
| 10+    | Cao       | Đáng tin, có thể dùng để training |

Luôn ghi số bài đã phân tích vào phần metadata đầu style guide.

---

## Workflow 2: Library

Thư viện style guide viết lách, chia 3 category:

- **Personas** — bản sắc tác giả cụ thể (1 con người thật, có tên, có quirks, có signature phrases).
- **Archetypes** — kiểu viết có pattern cố định (reusable cho nhiều tác giả / nhiều bài).
- **Voices** — giọng điệu generic (teacher/storyteller/objective... không gắn người cụ thể).

### Personas có sẵn

| Persona | Slug   | Tóm tắt 1 dòng | File |
| ------- | ------ | --------------- | ---- |
| Tuấn    | `tuan` | Xưng "Tuấn" ngôi 3, "Cậu" khi dạy dỗ, "tôi" khi tâm sự; giọng Nam Bộ, anecdote có tên nhân vật, bold-CAPS dồn dập, metaphor nông nghiệp/đồng quê. | [personas/tuan.md](references/personas/tuan.md) |

### Archetypes có sẵn

| Archetype        | Slug               | Khi nào dùng | File |
| ---------------- | ------------------ | ------------ | ---- |
| Patient Observer | `patient-observer` | Bài về hành trình, quá trình, kiên nhẫn, growth, học hỏi dài hạn. | [archetypes/patient-observer.md](references/archetypes/patient-observer.md) |
| Dramatic Prophet | `dramatic-prophet` | Bài về reset, phá bỏ cái cũ, transformation, chuyển paradigm. | [archetypes/dramatic-prophet.md](references/archetypes/dramatic-prophet.md) |
| Quiet Devastator | `quiet-devastator` | Bài insight sắc, nghịch lý, observation tinh tế, irony, phê phán ngầm. | [archetypes/quiet-devastator.md](references/archetypes/quiet-devastator.md) |

### Voices có sẵn

Mỗi voice có 3 variant: `main` (đầy đủ), `compact` (rút gọn cho context budget hẹp), `exemplars` (ví dụ cụ thể).

| Voice        | Slug           | Tóm tắt 1 dòng | Main file |
| ------------ | -------------- | --------------- | --------- |
| Teacher      | `teacher`      | Dạy bài bản, giải thích khái niệm từng bước, scaffolding cho người mới. | [voices/teacher.md](references/voices/teacher.md) |
| Storyteller  | `storyteller`  | Kể chuyện chánh niệm, hành trình ngôi "tôi", trải nghiệm > lý thuyết. | [voices/storyteller.md](references/voices/storyteller.md) |
| Objective    | `objective`    | Trung lập, dữ liệu, phân tích, giọng báo chí nghiêm túc. | [voices/objective.md](references/voices/objective.md) |
| Investigator | `investigator` | Điều tra, đặt câu hỏi, dẫn dắt người đọc tự khám phá qua manh mối. | [voices/investigator.md](references/voices/investigator.md) |
| Guide        | `guide`        | Hướng dẫn cụ thể, actionable, đi kèm người đọc như một mentor đồng hành. | [voices/guide.md](references/voices/guide.md) |
| Personal     | `personal`     | Cá nhân, tự sự, reflective; kể chuyện mình để reader chiếu vào. | [voices/personal.md](references/voices/personal.md) |
| Dialogue     | `dialogue`     | Đối thoại thầy-trò (format C:/T:), triết lý qua hỏi-đáp. | [voices/dialogue.md](references/voices/dialogue.md) |

Compact và exemplars variant nằm cùng thư mục với suffix `-compact.md` và `-exemplars.md` (VD: `voices/storyteller-compact.md`, `voices/storyteller-exemplars.md`).

### Tra cứu / chọn style

Khi user hỏi "có style/persona/archetype/voice nào?":

1. Hiển thị bảng tương ứng (Personas / Archetypes / Voices).
2. Nếu user chưa chọn, hỏi user muốn load cái nào.

### Load style guide

Khi user yêu cầu "dùng persona X" / "viết theo archetype Y" / "apply voice Z":

1. Tra slug trong bảng → đường dẫn file.
2. `Read` toàn bộ file đó.
3. Nắm các phần chính của file:
  - **Persona**: 8 chiều + signature phrases + công thức tái tạo + anti-patterns.
  - **Archetype**: khi nào dùng + kỹ thuật cốt lõi + emotional arc + pattern mẫu.
  - **Voice**: philosophy + giọng + cấu trúc đặc thù.
4. Áp dụng vào task viết. Tuân thủ mọi anti-pattern trong file.

### Thêm persona mới

Dùng **Workflow 1: Analyze** để bóc tách DNA từ corpus. Output tự động lưu vào `references/personas/` và cập nhật bảng.

### Thêm archetype mới

1. Soạn file mô tả archetype theo cấu trúc chuẩn: "Khi nào phù hợp" + "Kỹ thuật cốt lõi" + "Emotional Arc" + "Pattern mẫu" + (optional) "Lưu ý" / "Phong cách bổ sung".
2. Lưu vào `references/archetypes/<slug>.md`.
3. Thêm dòng mới vào bảng **Archetypes có sẵn**.

### Thêm voice mới

1. Soạn 3 file: `<slug>.md` (main), `<slug>-compact.md`, `<slug>-exemplars.md`.
2. File main tối thiểu cần: Philosophy, Voice (ngôi kể/giọng), đặc trưng structure khuyến nghị, anti-patterns.
3. Lưu vào `references/voices/`.
4. Thêm dòng mới vào bảng **Voices có sẵn**.

---

## Quy ước file style guide

- **Persona**: theo output chuẩn của Workflow Analyze — 8 chiều + signature phrases + công thức + anti-patterns + AI anti-patterns.
- **Archetype**: 4-5 section cố định (khi nào dùng / kỹ thuật / emotional arc / pattern mẫu / lưu ý).
- **Voice**: philosophy + voice + structure preference + anti-patterns. Có 3 variant (main/compact/exemplars) để chọn theo context budget.

## Nguyên tắc

- **Thư viện + phân tích, không phải writer**: skill này cung cấp style guide và phân tích văn phong. KHÔNG tự sinh ra bài viết hoàn chỉnh.
- **Single source of truth**: mỗi style một file duy nhất trong skill này. Skill/AI khác reference bằng path, không copy nội dung đi nơi khác.
- **Fingerprint > generic**: style guide tốt phải có nét nhận dạng mạnh (tên xưng, signature phrase, quirks), đủ để phân biệt qua 3 câu đầu. Voice/archetype thì có pattern rõ ràng, dễ nhận.
