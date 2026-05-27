# Quy Tắc Chung

Tài liệu này chứa quy tắc MẶC ĐỊNH cho mọi voice và structure.

**Override rule:** Voice file có quyền override bất kỳ mục nào dưới đây (ghi rõ mục override). Analyzed voices (tạo từ Workflow Analyze) ưu tiên data corpus, chỉ bắt buộc tuân thủ phần "Từ Cấm (Anti-AI)" và "Dấu Câu".

---

## Nhịp Thở (Breath Rhythm)

### Xương sống

- Câu flowing 12-25 từ, nhiều mệnh đề nối dấu phẩy. Đây là nhịp tự nhiên tiếng Việt.
- Đoạn văn 2-5 câu, có nhịp thở (xen kẽ dài/ngắn).

### Câu ngắn

Hai chuẩn tùy nhóm voice:

| Nhóm | Voices | Câu ngắn | Ghi chú |
|---|---|---|---|
| **Contemplative** | Personal, Storyteller, Dialogue, Guide | ≤8 từ, có chủ-vị | Tạo khoảng lặng, chiêm nghiệm |
| **Analytical** | Investigator, Objective, Teacher | ≤10 từ | Tạo punch, nhấn mạnh luận điểm |

**Quy tắc chung cho cả hai nhóm:**
- Tối đa 2-3 câu ngắn/bài
- Luôn đứng SAU buildup (đoạn dài trước, ngắn sau)
- KHÔNG viết 2+ câu ngắn liên tiếp
- Đoạn một câu = điểm nhấn (hiếm, bất ngờ)

### Cấm

- KHÔNG xếp nominal phrases liên tiếp: "Mùi X. Tiếng Y." → Lồng vào câu có động từ
- Lặp cấu trúc = mantra (dùng có chủ đích, không lạm dụng)

---

## Dấu Câu

- **Cấm em-dash (—) và en-dash (–)** ở mọi vị trí. Thay bằng dấu phẩy, dấu hai chấm, hoặc tách câu.
- Dùng dấu ba chấm (...) cho khoảng lặng (contemplative voices).
- Hạn chế dấu chấm phẩy. Tách thành 2 câu đọc tự nhiên hơn.

---

## Từ Cấm (Anti-AI Blacklist)

Áp dụng MỌI voice, KỂ CẢ analyzed voices. Không ngoại lệ.

### Từ cấm tuyệt đối

- **"Có lẽ"**: marker phổ biến nhất của văn AI tiếng Việt. Thay bằng: viết thẳng quan điểm, "tôi chưa chắc", "không biết nữa", câu hỏi mở.

### Cụm mở bài sáo (Nhóm A)

Cấm mở bài bằng các cụm sau hoặc biến thể gần nghĩa:

- "Hãy cùng khám phá..."
- "Trong thế giới ngày nay..."
- "Bạn đã bao giờ tự hỏi..."
- "Đây là một hành trình..."

### Cụm chuyển đoạn máy (Nhóm B)

Cấm dùng làm transition giữa đoạn:

- "Không chỉ... mà còn..."
- "Bên cạnh đó..."
- "Hơn nữa..."
- "Điều đáng chú ý là..."
- "Thật thú vị là..."

### Cụm kết bài template (Nhóm C)

Cấm kết bài bằng:

- "Cuối cùng, điều quan trọng nhất là..."
- "Hãy bắt đầu ngay hôm nay..."
- "Mỗi người đều có thể..."

### Triple adjective / virtue words rỗng (Nhóm D)

- Cấm xếp 3 tính từ liên tiếp bằng phẩy + "và": "sâu sắc, tinh tế, và đầy ý nghĩa"
- Cấm virtue words không định lượng: "tuyệt vời", "đáng kinh ngạc", "vô cùng"

### Hedging rỗng (Nhóm E)

- "một cách nào đó"
- "ở một mức độ nào đó"

---

## Quality Checklist (gộp)

Checklist DUY NHẤT cho mọi bài viết. Voice/structure file BỔ SUNG tối đa 2-3 ô riêng, không lặp lại ô dưới đây.

### MUST (bài ngắn + dài đều chạy)

- [ ] Không có từ/cụm trong Anti-AI Blacklist?
- [ ] Không có em-dash (— –)?
- [ ] Giọng nhất quán xuyên suốt bài?
- [ ] Đọc to: nghe tự nhiên, không vấp?
- [ ] Insight cốt lõi rõ (nói được trong 1 câu)?

### SHOULD (bài dài ≥800 từ)

- [ ] "Vậy thì sao?" — mỗi đoạn trả lời được?
- [ ] Ít nhất 1 khoảnh khắc khiến người đọc dừng lại?
- [ ] Ẩn dụ nhất quán (không trộn nhiều hệ)?
- [ ] Nhịp thở: xen kẽ câu dài/ngắn đúng quy tắc?
- [ ] Kết bài phù hợp voice category?

### NICE (hướng đến xuất sắc)

- [ ] Cognitive dissonance: thách thức giả định cũ của người đọc?
- [ ] Đáng share: tôi có share bài này lên trang cá nhân không?
- [ ] "Kể lại test": người đọc kể lại cho bạn trong 1 câu, câu đó có thú vị không?

---

## Opening Palette Master

Tất cả technique mở bài có sẵn. Mỗi structure chọn 4-5 technique phù hợp. Quy tắc: KHÔNG lặp technique giữa 2 bài liên tiếp trong series.

| Slug | Tên | Mô tả | Phù hợp với |
|---|---|---|---|
| `scene-setting` | Khoảnh khắc giác quan | Thời gian, không gian, chi tiết giác quan cụ thể | Narrative, contemplative |
| `question-first` | Câu hỏi trước | Câu hỏi khiến dừng lại, bối cảnh sau | Universal |
| `contrast` | Tương phản | Nghịch lý, phản trực giác, hai vế đối lập | Universal |
| `provocation` | Nhận định bất ngờ | Phá giả định, đảo kỳ vọng | Analytical, educational |
| `memory-flash` | Hồi ức mảnh ghép | Ký ức rời rạc, chi tiết giác quan mạnh | Narrative, reflective |
| `in-medias-res` | Giữa hành động | Nhảy vào giữa cảnh/đối thoại | Narrative, dialogue |
| `assumption-challenge` | Thách thức giả định | Giả định phổ biến bị lật | Analytical, investigative |
| `experiment` | Thử nghiệm | Trải nghiệm/experiment cụ thể mở đầu | Educational, guide |
| `scenario` | Tình huống thực tế | Tình huống người đọc relate | Tutorial, educational |
| `bold-claim` | Kết luận mạnh | BLUF: insight quan trọng nhất ngay đầu | Business, technical |

---

## Kết Bài: Phân Loại Theo Voice Category

| Category | Voices | Kết bài |
|---|---|---|
| **Contemplative** | Personal, Storyteller, Dialogue | Kết mở CÓ SỨC NẶNG: câu hỏi/hình ảnh liên quan trực tiếp đến đời sống người đọc. Không phải triết lý chung chung. |
| **Action-oriented** | Teacher, Guide | Hành động cụ thể + câu hỏi gợi mở. Người đọc biết bước tiếp theo. |
| **Analytical** | Investigator | Câu hỏi mở + honest limitation. Mời tư duy tiếp. |
| **Professional** | Objective | Summary + recommendations actionable + next steps. |

**Override rule:** Structure có thể override voice khi cần. Ví dụ: Depth-Practice luôn có invitation to practice, kể cả khi dùng với contemplative voice.

Phân biệt "kết mở có sức nặng" vs "kết mở trống":
- **Có sức nặng**: câu hỏi mà người đọc PHẢI mang theo vì liên quan trực tiếp đến cuộc sống họ
- **Trống**: câu hỏi triết lý chung chung, gật đầu rồi quên
