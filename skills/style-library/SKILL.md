---
name: style-library
description: "Thư viện style guide viết lách với 3 catalog: personas (bản sắc tác giả cụ thể), archetypes (kiểu viết có pattern cố định), voices (giọng điệu generic). Use this skill whenever the user asks 'có style/persona/archetype/voice nào?', 'liệt kê style guide', 'load style X', 'dùng văn phong Y', 'apply archetype Z', 'viết theo giọng W', hoặc bất cứ khi nào task viết lách cần chọn/áp dụng một style guide có sẵn. Cũng kích hoạt khi cần tra cứu catalog trước khi viết bài. Đây KHÔNG phải skill viết bài — skill này chỉ cung cấp style guide đã có sẵn làm nguyên liệu cho skill/AI khác áp dụng."
disable-model-invocation: true
---

# Style Library

Thư viện style guide viết lách, chia 3 category:

- **Personas** — bản sắc tác giả cụ thể (1 con người thật, có tên, có quirks, có signature phrases).
- **Archetypes** — kiểu viết có pattern cố định (reusable cho nhiều tác giả / nhiều bài).
- **Voices** — giọng điệu generic (teacher/storyteller/objective... — không gắn người cụ thể).

Mỗi file là tài liệu độc lập để AI hoặc skill khác load khi cần viết bài theo style tương ứng.

## Personas có sẵn

| Persona | Slug   | Tóm tắt 1 dòng                                                                                                                                    | File                                            |
| ------- | ------ | ------------------------------------------------------------------------------------------------------------------------------------------------- | ----------------------------------------------- |
| Tuấn    | `tuan` | Xưng "Tuấn" ngôi 3, "Cậu" khi dạy dỗ, "tôi" khi tâm sự; giọng Nam Bộ, anecdote có tên nhân vật, bold-CAPS dồn dập, metaphor nông nghiệp/đồng quê. | [personas/tuan.md](references/personas/tuan.md) |


## Archetypes có sẵn

| Archetype        | Slug               | Khi nào dùng                                                           | File                                                                        |
| ---------------- | ------------------ | ---------------------------------------------------------------------- | --------------------------------------------------------------------------- |
| Patient Observer | `patient-observer` | Bài về hành trình, quá trình, kiên nhẫn, growth, học hỏi dài hạn.      | [archetypes/patient-observer.md](references/archetypes/patient-observer.md) |
| Dramatic Prophet | `dramatic-prophet` | Bài về reset, phá bỏ cái cũ, transformation, chuyển paradigm.          | [archetypes/dramatic-prophet.md](references/archetypes/dramatic-prophet.md) |
| Quiet Devastator | `quiet-devastator` | Bài insight sắc, nghịch lý, observation tinh tế, irony, phê phán ngầm. | [archetypes/quiet-devastator.md](references/archetypes/quiet-devastator.md) |


## Voices có sẵn

Mỗi voice có 3 variant: `main` (đầy đủ), `compact` (rút gọn cho context budget hẹp), `exemplars` (ví dụ cụ thể).

| Voice        | Slug           | Tóm tắt 1 dòng                                                           | Main file                                                   |
| ------------ | -------------- | ------------------------------------------------------------------------ | ----------------------------------------------------------- |
| Teacher      | `teacher`      | Dạy bài bản, giải thích khái niệm từng bước, scaffolding cho người mới.  | [voices/teacher.md](references/voices/teacher.md)           |
| Storyteller  | `storyteller`  | Kể chuyện chánh niệm, hành trình ngôi "tôi", trải nghiệm > lý thuyết.    | [voices/storyteller.md](references/voices/storyteller.md)   |
| Objective    | `objective`    | Trung lập, dữ liệu, phân tích, giọng báo chí nghiêm túc.                 | [voices/objective.md](references/voices/objective.md)       |
| Investigator | `investigator` | Điều tra, đặt câu hỏi, dẫn dắt người đọc tự khám phá qua manh mối.       | [voices/investigator.md](references/voices/investigator.md) |
| Guide        | `guide`        | Hướng dẫn cụ thể, actionable, đi kèm người đọc như một mentor đồng hành. | [voices/guide.md](references/voices/guide.md)               |
| Personal     | `personal`     | Cá nhân, tự sự, reflective; kể chuyện mình để reader chiếu vào.          | [voices/personal.md](references/voices/personal.md)         |
| Dialogue     | `dialogue`     | Đối thoại thầy-trò (format C:/T:), triết lý qua hỏi-đáp.                 | [voices/dialogue.md](references/voices/dialogue.md)         |


Compact và exemplars variant nằm cùng thư mục với suffix `-compact.md` và `-exemplars.md` (VD: `voices/storyteller-compact.md`, `voices/storyteller-exemplars.md`).

## Cách dùng

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

1. Bóc tách DNA văn phong từ corpus bằng skill [style-dna](../style-dna/SKILL.md).
2. Lưu output vào `references/personas/<slug>.md` (slug kebab-case, không dấu tiếng Việt).
3. Thêm một dòng mới vào bảng **Personas có sẵn** ở trên (tên hiển thị, slug, tóm tắt 1 dòng, link file).

### Thêm archetype mới

1. Soạn file mô tả archetype theo cấu trúc chuẩn: "Khi nào phù hợp" + "Kỹ thuật cốt lõi" + "Emotional Arc" + "Pattern mẫu" + (optional) "Lưu ý" / "Phong cách bổ sung".
2. Lưu vào `references/archetypes/<slug>.md`.
3. Thêm dòng mới vào bảng **Archetypes có sẵn**.

### Thêm voice mới

1. Soạn 3 file: `<slug>.md` (main), `<slug>-compact.md`, `<slug>-exemplars.md`.
2. File main tối thiểu cần: Philosophy, Voice (ngôi kể/giọng), đặc trưng structure khuyến nghị, anti-patterns.
3. Lưu vào `references/voices/`.
4. Thêm dòng mới vào bảng **Voices có sẵn**.

## Quy ước file style guide

- **Persona**: theo output chuẩn của skill [style-dna](../style-dna/SKILL.md) — 8 chiều + signature phrases + công thức + anti-patterns + AI anti-patterns.
- **Archetype**: 4-5 section cố định (khi nào dùng / kỹ thuật / emotional arc / pattern mẫu / lưu ý).
- **Voice**: philosophy + voice + structure preference + anti-patterns. Có 3 variant (main/compact/exemplars) để chọn theo context budget.

## Nguyên tắc

- **Thư viện, không phải writer**: skill này chỉ cung cấp style guide. KHÔNG tự sinh ra bài viết.
- **Độc lập tuyệt đối**: skill này KHÔNG load/invoke/reference skill khác. Không có chuyện "load anti-ai-writing rồi mới xuất". User (hoặc skill workflow khác) tự quyết compose gì với nhau.
- **Single source of truth**: mỗi style một file duy nhất trong skill này. Skill/AI khác reference bằng path, không copy nội dung đi nơi khác.
- **Fingerprint > generic**: style guide tốt phải có nét nhận dạng mạnh (tên xưng, signature phrase, quirks) — đủ để phân biệt qua 3 câu đầu. Voice/archetype thì có pattern rõ ràng, dễ nhận.
