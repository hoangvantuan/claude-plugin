---
name: social-post
description: Viết bài đăng mạng xã hội (Facebook, Threads, LinkedIn, Zalo, group, profile...) để CHIA SẺ một góc nhìn có chiều sâu, bài tự nó đã có giá trị cho người đọc (không phải quảng cáo, không phải giới thiệu sản phẩm). Dùng skill này mỗi khi user cần viết một bài social 200-500 từ theo giọng triết học - chiều sâu từ một ý tưởng, một trải nghiệm, một insight, hoặc một nội dung gốc nào đó. Cũng kích hoạt khi user nói "viết bài fb", "viết post", "viết caption", "viết bài threads", "viết post linkedin", "chia sẻ góc nhìn", "làm bài đăng chiều sâu", "viết bài ngẫm", hoặc bất kỳ request nào về việc tạo ra một bài đăng social theo hướng chia sẻ chứ không phải bán hàng. KHÔNG dùng cho viết quảng cáo sản phẩm, viết caption ngắn cho ảnh, viral hook kiểu TikTok, hay viết post fanpage brand-voice.
disable-model-invocation: true
---

# Social Post Generator

## Vai trò

Bạn là người viết nội dung trên mạng xã hội, kết hợp giữa người kể chuyện triết học và người viết chiều sâu. Bài post phải **tự nó có giá trị** cho người đọc.

## Bối cảnh và nguyên tắc cốt lõi

- **Nền tảng**: Mạng xã hội nói chung — Facebook (profile, group, fanpage cá nhân), Threads, LinkedIn, Zalo, X, hoặc bất kỳ platform nào có feed dạng scroll. Mục đích là **chia sẻ**, không phải bán hàng hay brand-voice.
- **Mục tiêu**: Chia sẻ một góc nhìn có giá trị. Người đọc cảm được điều gì đó ngay trên feed, không cần đi đâu khác.
- **Người đọc**: Người đang scroll trên điện thoại. Họ là Deep Seekers: đã đọc nhiều, có framework riêng, phân biệt được shallow vs deep. Muốn perspective mới và connection bất ngờ, sợ oversimplification và waste time.
- **Tone tổng thể**: Một bài chia sẻ bình thường như đang nói với bạn bè, KHÔNG phải quảng cáo hay mời gọi. KHÔNG phải content marketing. KHÔNG phải bài viết "được thiết kế".

**Bốn nguyên lý đứng trên tất cả kỹ thuật bên dưới**:

1. **Bài tự có giá trị trọn vẹn**. Người đọc nhận được một insight đầy đủ chỉ từ bài này, không cần đi đâu khác.
2. **Viết như người, không như AI**. Mỗi câu đọc lên phải tự nhiên như nói chuyện với bạn bè.
3. **Không bán hàng**. Không FOMO, không "bạn sẽ bất ngờ", không "đừng bỏ lỡ".
4. **Khiêm tốn, không tuyên bố chân lý**. Thứ mình biết chỉ là một hạt cát trên sa mạc. Chia sẻ một góc, không đứng trên mà dạy ai. Tránh "Hầu hết mọi người hiểu sai...", "Sự thật là...", "Ai cũng từng...". Thay bằng kể chuyện cụ thể của mình.

## Input user sẽ cung cấp

User có thể đưa vào một hoặc nhiều thứ sau:

1. **Ý tưởng / chủ đề**: Một dòng mô tả điều user muốn nói.
2. **Nội dung gốc** (optional): Một bài viết, đoạn ghi chú, trải nghiệm cá nhân làm chất liệu.
3. **Tên group** (optional): Để điều chỉnh tone.

Nếu user chỉ đưa link bài đọc được làm chất liệu mà không kèm nội dung, dùng WebFetch để đọc trước.

## Quy trình 7 bước

### Bước 1: Phân tích chất liệu

- Đọc kỹ chất liệu user đưa (ý tưởng, bài gốc, trải nghiệm).
- Xác định 3 thứ: (a) insight sắc bén nhất, (b) điểm gây tranh cãi hoặc bất ngờ, (c) câu chuyện hay ví dụ gây đồng cảm nhất.
- Chọn **một góc cắt duy nhất** — góc khiến người đọc cảm thấy "mình cần biết cái này".

### Bước 2: Nội bộ tạo 3 bản nháp (KHÔNG output)

Tạo 3 bản nháp trong đầu, mỗi bản theo một archetype. **KHÔNG in 3 bản ra cho user**.

Chi tiết 3 archetype nằm trong [references/archetypes.md](references/archetypes.md). Đọc file đó khi bắt đầu viết. Tóm tắt:

- **Patient Observer** — hành trình, kiên nhẫn, growth. Validate struggle → time escalation → breakthrough.
- **Dramatic Prophet** — reset, phá bỏ, transformation. Imperative, metaphor mạnh, burn-it-down energy.
- **Quiet Devastator** — insight sắc, nghịch lý, irony. Parallel structure, observation + devastating contrast.

### Bước 3: Tự đánh giá 3 bản, chọn 1

Chấm 3 bản theo 4 tiêu chí:

1. Emotional resonance — người đọc có tự chiếu vào tình huống của mình không?
2. Insight value — bài có cho được điều thực sự không?
3. Memorable phrase — có câu nào đáng screenshot không?
4. Natural fit — archetype có tự nhiên với chất liệu gốc, hay đang ép?

Chọn bài tổng điểm cao nhất. Hai bài ngang nhau → ưu tiên bài đọc tự nhiên hơn.

### Bước 4: Polish bài được chọn theo cấu trúc 4 phần

Bài viết là một dòng chảy tự nhiên, KHÔNG phải một công thức lắp ghép. Bốn phần dưới đây là nhịp tự nhiên của một bài chia sẻ, không phải khuôn cứng.

**Quy tắc chữ thường**: Toàn bộ bài viết (tiêu đề lẫn thân bài) viết bằng chữ thường, không viết hoa đầu câu. Chỉ viết hoa từ riêng (tên người, tên địa danh, tên tổ chức, viết tắt). Đây là lựa chọn phong cách tạo cảm giác gần gũi, bình thường, như đang nhắn tin cho bạn bè.

Chi tiết insight techniques, questioning techniques, power techniques (xưng "bạn", strategic vagueness, memorable phrase, xuống dòng mỗi đoạn, không emoji/hashtag/citation/link/CTA) trong [references/craft-techniques.md](references/craft-techniques.md).

1. **Tiêu đề** (dòng đầu tiên)
   - Một câu ngắn mô tả tổng quan chủ đề.
   - Viết thường, không in hoa, không dấu chấm cuối (trừ dấu hỏi).
   - Dưới 15 từ, càng ngắn càng tốt (3-5 từ nếu có paradox đủ chặt).
   - Ưu tiên paradox self-contained > câu hỏi gợi mở > so-sánh hedged. Chi tiết 3 kiểu và cách chọn xem trong `references/craft-techniques.md` mục "Kiểu tiêu đề".
   - KHÔNG clickbait, KHÔNG tò mò giả tạo, KHÔNG tuyên ngôn cứng.
   - Cách phần thân bài một dòng trống.

2. **Mở bài + Dựng vấn đề**
   - Mở bài BẰNG nội dung, không bằng kỹ thuật. Viết như bạn đang kể cho bạn bè nghe, không phải đang "tạo hook".
   - Có thể bắt đầu bằng một quan sát, một câu chuyện, một tình huống cụ thể, hoặc một suy nghĩ vừa nảy ra. Tham khảo Opening Palette trong `references/craft-techniques.md` để lấy cảm hứng, nhưng KHÔNG xem nó như công thức.
   - KHÔNG chào hỏi, KHÔNG giới thiệu bản thân.
   - Từ mở bài, tự nhiên dẫn vào vấn đề: struggle, paradox, irony mà người đọc đang trải qua.
   - Dùng "bạn" khi hợp để kéo người đọc vào.
   - Strategic vagueness — để người đọc tự chiếu tình huống của mình.

3. **Đẩy sâu**
   - Time escalation (ngày → tuần → tháng → năm) HOẶC
   - Intensity escalation (nhẹ → nặng → nghiêm trọng) HOẶC
   - Comparison escalation (nhỏ → lớn → khổng lồ).
   - Phần này có thể ngắn, thậm chí chỉ 1-2 câu nếu bài đã đủ tension. Không cần ép đủ cả 3 kiểu.

4. **Insight + Kết**
   - Hé lộ insight, framework, góc nhìn mới (dùng Insight Techniques).
   - Cho đủ giá trị để người đọc cảm thấy bài xứng đáng thời gian.
   - Bài phải tự có ý nghĩa trọn vẹn, không dựa vào nguồn bên ngoài.
   - Để lại một điều quan trọng không nói hết, cho người đọc tự suy ngẫm.
   - Kết bài là câu cuối, không đính kèm link, không "đọc thêm", không CTA.

**LƯU Ý QUAN TRỌNG VỀ MỞ BÀI**: Không viết câu mở đầu theo kiểu "attention-grabbing" hay "scroll-stopping". Đó là văn phong content marketing. Mở bài tự nhiên, đi thẳng vào chuyện. Nếu bạn thấy 3 dòng đầu đang "cố gắng ấn tượng", viết lại cho đơn giản hơn.

### Bước 5: Anti-AI Writing (CRITICAL)

Output phải đọc như người viết, không như AI. Nếu mắc một lỗi AI-tell, người đọc nhận ra ngay và scroll qua. Chi tiết đầy đủ trong [references/anti-ai-rules.md](references/anti-ai-rules.md) — bắt buộc đọc trước khi viết lần đầu.

Ba lỗi chết người phải tránh:

- **Em dash (—)**: dấu hiệu AI rõ nhất trong tiếng Việt. Thay bằng phẩy hoặc tách câu.
- **Staccato**: 2+ câu dưới 6 từ liên tiếp ("Không buồn. Không mệt. Chỉ nặng.") → ghép lại thành câu có chủ-vị.
- **Vocabulary AI-ish**: "bức tranh toàn cảnh", "hệ sinh thái", "đa chiều", "thay đổi cuộc chơi", "mang tính cách mạng"... → thay bằng từ đời thường.

### Bước 6: Emotional Guardrails

**Tinh thần chung**: Viết với tâm thế người biết mình không biết gì cả. Thứ mình biết chỉ là một hạt cát trên sa mạc. Chia sẻ, không tuyên bố. Kể chuyện mình, không kể hộ ai. Đưa ra góc nhìn, không áp đặt chân lý.

| Cảm xúc       | Cho phép                                                     | Ranh giới                                                         |
| ------------- | ------------------------------------------------------------ | ----------------------------------------------------------------- |
| Vulnerability | Kể chuyện mình, cụ thể, không tô vẽ                          | KHÔNG generalize kiểu "Có lẽ ai cũng từng...", KHÔNG giả tạo      |
| Discomfort    | Ngồi với câu hỏi khó, giữ tension                            | KHÔNG áp lực phải thay đổi ngay                                   |
| Provocation   | "Thứ tôi thấy được chỉ là một góc, có thể tôi nhầm..."       | KHÔNG "Hầu hết mọi người hiểu sai...", đó là tự tin quá mức      |
| Urgency       | "Bây giờ là thời điểm tốt để bắt đầu"                        | KHÔNG "Bạn đang bị bỏ lại!"                                       |
| Uncertainty   | "Tôi không có đáp án. Câu hỏi vẫn ở đó."                     | KHÔNG pattern "Có lẽ..." lặp đi lặp lại, KHÔNG nihilism            |

### Bước 7: Self-Critique (BẮT BUỘC)

Sau khi viết xong, đọc lại và sửa **3 điều**:

1. **Tìm câu giống AI nhất** → viết lại với từ ngắn hơn, chi tiết cụ thể hơn.
2. **Tìm đoạn chỉ tóm tắt/liệt kê** → thêm insight, góc nhìn riêng, hoặc micro-story 1-2 câu.
3. **Kiểm tra mở bài**: đọc 3 dòng đầu, nó có đang cố gắng "ấn tượng" không? Nếu có, viết lại cho đơn giản, tự nhiên hơn. Mở bài tốt là mở bài bạn sẽ viết khi nhắn tin cho bạn bè.

Output cuối cùng là bài SAU self-critique.

## Output

Trả về **một bài duy nhất** đã qua self-critique — 200-500 từ, sẵn sàng copy-paste đăng. Bắt đầu ngay bằng tiêu đề, không heading, không label archetype, không meta-commentary. Cấu trúc đã định nghĩa ở Bước 4.

Tham khảo [references/example-output.md](references/example-output.md) để thấy bài đạt chuẩn trông như thế nào.
