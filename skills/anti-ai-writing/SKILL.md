---
name: anti-ai-writing
description: "Rules viết tiếng Việt KHÔNG giống AI — blacklist từ/cụm/chấm câu, quy tắc cấu trúc câu Việt, self-critique bắt buộc, insight techniques. Use this skill whenever writing or rewriting Vietnamese content (blog, social post, newsletter, essay, script, article) để output đọc như người viết thật, tránh smell AI-generated. Kích hoạt khi user yêu cầu 'viết bài', 'rewrite', 'edit', 'proofread', 'check AI smell', 'viết như người thật', 'đừng giống AI', 'humanize', hoặc bất cứ khi nào cần review văn bản tiếng Việt xem có mùi AI không. Là rule CHUNG áp dụng cho mọi văn phong, dùng độc lập — không phụ thuộc skill khác."
---

# Anti-AI Writing Rules

Rule chung để output viết tiếng Việt đọc như **người viết**, không giống **AI generated**. Áp dụng cho mọi văn phong, mọi platform. Dùng độc lập hoặc làm baseline cho bất kỳ task viết nào.

Một số văn phong cá nhân có signature **vi phạm** rule trong file này có chủ đích (câu cụt staccato, anaphora, câu hỏi tu từ dồn, liệt kê 4+ items...). Khi task yêu cầu viết theo một văn phong có signature vi phạm rule chung, ưu tiên signature đó — rule ở file này chỉ là baseline mặc định, không phải luật cứng.

## Blacklist từ vựng (cấm tuyệt đối)

**Tiếng Việt** — cụm AI hay phun ra, cấm dùng trong mọi context:

- "bức tranh toàn cảnh", "hệ sinh thái", "bối cảnh không ngừng"
- "mở ra cánh cửa", "hành trình chuyển đổi"
- "đa chiều", "đa diện", "toàn diện và sâu sắc"
- "không thể phủ nhận", "đáng kinh ngạc", "tuyệt vời"
- "mang tính cách mạng", "thay đổi cuộc chơi", "đột phá", "mang tính bước ngoặt"

**Tiếng Anh chèn** — từ buzzword AI hay nhét:

- "delve", "tapestry", "landscape", "leverage"
- "nuanced", "multifaceted", "paradigm shift"
- "transformative", "game-changer", "holistic", "robust"

Thay bằng từ đơn giản, cụ thể. Nếu đang viết theo văn phong miệt vườn/đời thường, metaphor cụ thể ("cá mập", "gà què", "con diều") tốt hơn buzzword trừu tượng.

## Blacklist cụm chuyển đoạn & mở bài

**Kết bài** — cấm:

- "Tóm lại,…"
- "Bài viết đã trình bày…"
- "Trong phần tiếp theo…"

**Mở bài** — cấm:

- "Trong bối cảnh…"
- "Trong thế giới hiện đại…"
- "Với sự phát triển…"
- "Bạn đã bao giờ tự hỏi…" (rhetorical kiểu AI)

**Nối đoạn** — cấm "Hơn nữa", "Ngoài ra", "Bên cạnh đó" xuất hiện trong 2 đoạn liên tiếp. Thay bằng "Rồi", "Thật ra", "Trở lại…" hoặc không cần connector (tách đoạn tự nhiên).

## Cấu trúc câu Việt

KHÔNG dịch sát từ cấu trúc tiếng Anh:

- Sai: "Bằng cách sử dụng X, chúng ta có thể đạt được Y" → Đúng: "Dùng X thì đạt được Y"
- Sai: "cung cấp khả năng" → Đúng: "giúp" / "cho phép"

Ưu tiên thuần Việt khi nghĩa tương đương với Hán-Việt:

- Sai: "tối ưu hóa hiệu suất hoạt động" → Đúng: "chạy nhanh hơn"
- Sai: "triển khai giải pháp" → Đúng: "làm" / "áp dụng"

KHÔNG stack nhiều mệnh đề phụ trong 1 câu. Bắt đầu câu bằng "Và / Nhưng / Vì" khi cần nhịp tự nhiên — hợp văn nói tiếng Việt.

## Chấm câu

- **Cấm hoàn toàn em-dash (—) và en-dash (–)** trong mọi vị trí, kể cả title. Dùng dấu phẩy, dấu hai chấm, hoặc tách thành 2 câu.
- Hạn chế dấu chấm phẩy (;) — đa số tách thành 2 câu đọc tự nhiên hơn.
- Không lạm dụng dấu phẩy nối (comma splice) — 2 mệnh đề độc lập thì tách câu.

## Tone

- KHÔNG corporate neutral vô vị. Tốt thì nói tốt, xấu thì nói xấu. Có ý kiến rõ, không đứng giữa kiểu tròn trịa.
- KHÔNG enthusiasm giả tạo: "tuyệt vời!", "đáng kinh ngạc!", "thật là tuyệt!"
- Nuance OK khi phân tích, nhưng KHÔNG dùng "có thể / có lẽ / dường như" liên tiếp trong cùng đoạn. Provisional thật thì đổi: "tôi đoán…", "chưa chắc nhưng…", "nghe thì…", "xem ra…".

## Đa dạng độ dài đoạn

- Đoạn vary 2-7 câu trong bài. Xen đoạn ngắn và đoạn dài có chủ đích.
- KHÔNG để mọi đoạn cùng độ dài (nhịp đều đều = AI).
- KHÔNG kết đoạn cùng cấu trúc câu với câu mở đoạn kế tiếp (mirror pattern là AI smell).
