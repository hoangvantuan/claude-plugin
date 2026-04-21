---
name: writing-context
description: "Thư viện context dimensions cho viết lách — 3 trục: identities (góc nhìn người viết), audiences (đối tượng đọc), emotions (bản đồ cảm xúc bài). Use this skill whenever the user asks 'có identity/audience/emotion nào?', 'viết cho deep seekers', 'góc nhìn knowledge curator', 'emotional arc reflect-discover', hoặc bất cứ khi nào task viết lách cần chọn/áp dụng một trục ngữ cảnh có sẵn. Đây KHÔNG phải skill viết bài — skill này chỉ cung cấp context dimension definitions làm nguyên liệu cho skill/AI khác áp dụng."
disable-model-invocation: true
---

# Writing Context

Thư viện context dimensions cho viết lách, chia 3 trục:

- **Identities** — góc nhìn, vai trò người viết khi tiếp cận chủ đề (không phải persona cụ thể, mà là "lăng kính" tư duy).
- **Audiences** — đối tượng đọc mục tiêu, quyết định độ sâu, mật độ thuật ngữ, nhịp bài.
- **Emotions** — bản đồ cảm xúc bài mong muốn tạo ra ở người đọc (emotional arc).

3 trục này độc lập với nhau và độc lập với Style / Structure. User (hoặc workflow skill) compose 3 trục này với style + structure để viết bài.

## Identities có sẵn

| Identity              | Slug                    | Góc nhìn                                                                  | File                                                                                  |
| --------------------- | ----------------------- | ------------------------------------------------------------------------- | ------------------------------------------------------------------------------------- |
| Contemplative Thinker | `contemplative-thinker` | Người suy tư — tiếp cận chủ đề qua chiêm nghiệm, đặt câu hỏi existential. | [identities/contemplative-thinker.md](references/identities/contemplative-thinker.md) |
| Knowledge Curator     | `knowledge-curator`     | Người tổng hợp — gom-kết nối-trình bày tri thức từ nhiều nguồn.           | [identities/knowledge-curator.md](references/identities/knowledge-curator.md)         |
| Tech Builder          | `tech-builder`          | Người xây dựng — hands-on, thực chiến, thiên về cách làm hơn lý thuyết.   | [identities/tech-builder.md](references/identities/tech-builder.md)                   |


## Audiences có sẵn

| Audience           | Slug                 | Đặc trưng                                                                              | File                                                                          |
| ------------------ | -------------------- | -------------------------------------------------------------------------------------- | ----------------------------------------------------------------------------- |
| Busy Professionals | `busy-professionals` | Ít thời gian, cần kết luận nhanh, bullet points, skim-friendly.                        | [audiences/busy-professionals.md](references/audiences/busy-professionals.md) |
| Curious Beginners  | `curious-beginners`  | Mới tiếp cận, cần scaffold, giải thích từng bước, friendly tone.                       | [audiences/curious-beginners.md](references/audiences/curious-beginners.md)   |
| Deep Seekers       | `deep-seekers`       | Đã đọc nhiều, có framework riêng, muốn nuance + góc nhìn mới, ghét oversimplification. | [audiences/deep-seekers.md](references/audiences/deep-seekers.md)             |


## Emotions có sẵn

| Emotion             | Slug                | Emotional Arc                                                              | File                                                                      |
| ------------------- | ------------------- | -------------------------------------------------------------------------- | ------------------------------------------------------------------------- |
| Empower & Challenge | `empower-challenge` | Trao sức + thử thách — người đọc kết bài thấy được tiếp năng lượng + thúc. | [emotions/empower-challenge.md](references/emotions/empower-challenge.md) |
| Provoke & Transform | `provoke-transform` | Kích thích + chuyển hóa — phá assumption, buộc reset góc nhìn.             | [emotions/provoke-transform.md](references/emotions/provoke-transform.md) |
| Reflect & Discover  | `reflect-discover`  | Chiêm nghiệm + khám phá — dẫn người đọc ngồi im với câu hỏi, tự tìm ra.    | [emotions/reflect-discover.md](references/emotions/reflect-discover.md)   |


## Cách dùng

### Tra cứu / chọn

Khi user hỏi "có identity/audience/emotion nào?":

1. Hiển thị bảng tương ứng.
2. Nếu user chưa chọn, hỏi user muốn load cái nào.

### Load context dimension

Khi user yêu cầu "viết cho audience X" / "góc nhìn identity Y" / "emotional arc Z":

1. Tra slug trong bảng → đường dẫn file.
2. `Read` file tương ứng.
3. Áp dụng đặc trưng vào task viết.

### Compose 3 trục

3 trục độc lập, chọn 1 mỗi trục:

- Identity (góc nhìn người viết) — ảnh hưởng cách tiếp cận chủ đề, loại evidence đưa ra.
- Audience (đối tượng đọc) — ảnh hưởng độ sâu, thuật ngữ, mật độ ví dụ.
- Emotion (cảm xúc mục tiêu) — ảnh hưởng pacing, kết bài, loại câu hỏi.

Ví dụ compose: `Contemplative Thinker + Deep Seekers + Reflect & Discover` → bài triết lý sâu cho người đọc từng trải, kết mở cho họ tự ngẫm.

### Thêm dimension mới

1. Chọn trục phù hợp (identity / audience / emotion).
2. Soạn file theo format hiện có trong thư mục tương ứng.
3. Lưu vào `references/<trục>/<slug>.md`.
4. Thêm dòng mới vào bảng **... có sẵn** tương ứng trong SKILL.md.

## Nguyên tắc

- **Thư viện, không phải writer**: skill này chỉ cung cấp context dimension definitions. KHÔNG tự sinh ra bài viết.
- **Độc lập tuyệt đối**: skill này KHÔNG load/invoke/reference skill khác. Không có chuyện "load style-library rồi mới trả audience". User (hoặc skill workflow khác) tự quyết compose gì với nhau.
- **Single source of truth**: mỗi dimension một định nghĩa duy nhất trong skill này.
- **3 trục độc lập với nhau**: identity không auto-imply audience, emotion không auto-imply structure. Mọi combo đều hợp lệ, user tự chọn.
- **Context ≠ style ≠ structure**: context chỉ định "viết cho ai, cảm xúc gì, góc nhìn nào" — KHÔNG quyết định giọng (voice/persona) hay xương sống bài (structure). Những chiều đó ở `style-library` và `writing-structures`.
