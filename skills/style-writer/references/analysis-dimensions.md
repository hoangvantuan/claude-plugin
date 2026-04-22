# 8 chiều phân tích văn phong — Chi tiết thao tác

File này hướng dẫn CỤ THỂ cần tìm gì, đo gì trong corpus để phân tích 8 chiều. Mỗi chiều có: mục tiêu, các câu hỏi khảo sát, ví dụ tín hiệu, cách trích bằng chứng.

---

## 1. Giọng điệu & persona

**Mục tiêu**: Xác định "người kể chuyện" là ai, nói với ai, thái độ ra sao.

**Khảo sát:**

- **Mức formal** — Scale 1-5:
  - 1: cực suồng sã, dùng "éo", "vl", tiếng lóng nặng.
  - 2: suồng sã có kiểm soát, "mình", "bọn mình", pha lóng nhẹ.
  - 3: trung tính, "tôi/mình", ngôn ngữ đời thường sạch.
  - 4: chuẩn mực, "tôi/chúng ta", tránh lóng, câu hoàn chỉnh.
  - 5: formal học thuật, "tác giả", passive voice, thuật ngữ nặng.
- **Tone chủ đạo** — Nghiêm / hài / châm biếm / nhiệt huyết / trầm / buồn / lạnh lùng / ấm áp. Có thể pha: "nghiêm + châm biếm nhẹ".
- **Ngôi xưng tác giả**: tôi / mình / ta / chúng ta / (ẩn ngôi). Đếm tần suất.
- **Cách gọi reader**: bạn / anh em / các bạn / (không gọi trực tiếp). Distance như nào — bạn bè / học trò / người xa lạ?
- **Thái độ với chủ đề**: chuyên gia giảng giải / bạn kể chuyện / người phê bình / người quan sát / người tâm sự.

**Cách trích bằng chứng**: chọn 1 câu ngắn (≤30 từ) thể hiện rõ tone. VD để chứng minh "suồng sã + châm biếm": `"Nó bảo tôi làm đi, tôi nhìn nó cười, ừ làm cái đầu mày."`

---

## 2. Cấu trúc bài

**Mục tiêu**: Phân tích khung xương bài viết — mở, thân, kết.

**Khảo sát:**

- **Pattern mở bài** — quét câu/đoạn đầu của mỗi bài:
  - Câu hỏi tu từ: `"Bạn có bao giờ nghĩ..."`
  - Thống kê/số liệu: `"Năm 2023, 87% người dùng..."`
  - Anecdote (kể chuyện nhỏ): `"Hôm qua tôi gặp anh bạn..."`
  - Tuyên bố mạnh: `"Mọi thứ bạn biết về X đều sai."`
  - Trích dẫn: `"'Blah blah' — Einstein từng nói..."`
  - Câu cụt độc lập: `"Thất bại."`
  - Đếm tỷ lệ từng kiểu qua các bài.
- **Xương sống thân bài**:
  - Chronological (theo dòng thời gian).
  - Problem-solution (nêu vấn đề → giải pháp).
  - Compare-contrast (so sánh 2 phía).
  - List-based (liệt kê có đánh số/heading).
  - Narrative (kể chuyện liền mạch).
  - Hybrid (ghi rõ cụ thể).
- **Pattern kết bài**:
  - Call-to-action ("Hãy thử...").
  - Circle back opening (quay lại ý mở bài).
  - Reflection (suy ngẫm).
  - Cliff-hanger (mở câu hỏi cho reader).
  - Câu cụt tuyên bố ("Chấm hết.").
  - Để lửng, không kết.

**Trích bằng chứng**: đoạn mở/kết ngắn ≤30 từ, đánh dấu bài nào.

---

## 3. Nhịp & độ dài câu

**Mục tiêu**: Đo nhịp thở của văn — tác giả có biến thiên độ dài câu không, dùng thủ pháp gì.

**Khảo sát:**

- **Độ dài câu trung bình** — đếm token (hoặc từ) của 50-100 câu mẫu. Tính mean. Ghi khoảng: "TB 14-18 từ/câu".
- **Câu cụt** (3-5 từ, thường là tuyên bố): có không, tần suất, chức năng (nhấn mạnh / chuyển đoạn / kết thúc):
  - VD: `"Thế thôi."`, `"Nó chết rồi."`, `"Không có gì cả."`
- **Tỷ lệ câu đơn / phức / ghép**:
  - Đơn: 1 chủ-vị.
  - Phức: 1 chủ-vị chính + mệnh đề phụ.
  - Ghép: 2+ chủ-vị ngang hàng (dấu phẩy, "và", "nhưng").
  - Ước lượng phần trăm từ mẫu 50 câu.
- **Thủ pháp nhịp**:
  - Anaphora (lặp đầu câu): `"Tôi đi. Tôi thấy. Tôi biết."`
  - Song hành (parallel): `"Sáng làm, chiều học, tối đọc."`
  - Đảo ngữ: `"Đẹp, cái váy đó."`
  - Câu hỏi tu từ: `"Ai mà không muốn thế?"`
  - Tam đoạn luận văn phong: 3 mệnh đề cân xứng.

**Trích bằng chứng**: 2-3 câu liên tiếp thể hiện nhịp.

---

## 4. Từ vựng đặc trưng (fingerprint)

**Mục tiêu**: Tìm 10-20 từ/cụm từ TÁC GIẢ NÀY hay dùng mà người khác ít dùng — chữ ký văn phong.

**Khảo sát:**

- Quét toàn corpus, đếm tần suất từ/cụm. Loại bỏ stopwords tiếng Việt (và, là, thì, mà, của, với, này, đó...).
- Tìm các loại:
  - **Từ "hiếm mà lặp"** — từ ít phổ thông nhưng tác giả dùng nhiều lần (VD: "trĩu nặng", "cồn cào", "bủn rủn").
  - **Cụm cố định đặc trưng** — cụm tác giả "đóng nhãn" (VD: "đi đến tận cùng", "chạm đáy bản thân").
  - **Slang/tiếng lóng** — nếu có (VD: "chuẩn chỉ", "vãi cả l", "đu trend").
  - **Neologism** — từ tác giả tự chế hoặc dùng theo cách riêng (VD: "sự vô thường hóa").
  - **Thuật ngữ chuyên ngành** — nếu tác giả có sở trường (tài chính, triết học, nhạc, nấu ăn...).
  - **Filler words cá nhân** — từ đệm vô thức: "thực ra", "kiểu", "về cơ bản", "nói chung", "cuối cùng thì".

**Format bảng top 15:**

| Cụm từ | Tần suất | Ví dụ ngữ cảnh |
|--------|----------|----------------|
| "kiểu gì" | 8 lần / 5 bài | `"Nó kiểu gì cũng sẽ về."` |

**Quy tắc**: cụm chỉ xuất hiện 1 lần → **không đưa vào bảng**.

---

## 5. Kỹ thuật tu từ

**Mục tiêu**: Identify công cụ tu từ và nguồn chất liệu tác giả hay dùng.

**Khảo sát:**

- **Metaphor/analogy** — quét các so sánh ("như", "giống", "là") hoặc ẩn dụ. Nhóm theo domain:
  - Thể thao (chạy/đua/bóng).
  - Ẩm thực (nấu/nêm/chín).
  - Chiến tranh (đánh/thủ/công).
  - Tự nhiên (cây/sông/mưa).
  - Cơ thể (tim/máu/hơi thở).
  - Máy móc (chạy/vận hành/hỏng).
  - Tôn giáo/tâm linh.
  - Domain khác — ghi cụ thể.
  - → Domain nào áp đảo?
- **Nguồn ví dụ quen dùng**:
  - Lịch sử (cổ kim Đông Tây).
  - Phim ảnh, sách, truyện.
  - Câu chuyện đời thường (của bản thân hoặc người quen).
  - Khoa học, thí nghiệm.
  - Quan sát xã hội.
- **Cách chuyển đoạn**:
  - Từ nối cứng: "Tuy nhiên", "Ngoài ra", "Thứ hai là".
  - Câu cầu (bridging sentence): câu tóm đoạn trước + mở đoạn sau.
  - Whitespace (dòng trắng giữa đoạn).
  - Heading / sub-heading.
  - Dấu "*** " phân chia block.
- **Hài hước**:
  - Tự trào (cười chính mình).
  - Đá xéo người khác / hiện tượng.
  - One-liner (câu hài đơn).
  - Tình huống (cười ngữ cảnh, không cần joke rõ).
  - Không có hài hước.

**Trích bằng chứng**: 1 metaphor tiêu biểu + 1 câu hài (nếu có).

---

## 6. Format & typography

**Mục tiêu**: Đo "body language" trực quan của bài viết.

**Khảo sát (đếm/tần suất):**

- **Heading** — có dùng không? H1/H2/H3? Bao nhiêu heading/bài TB?
- **Bullet/numbered list** — có không? Tần suất? Dùng cho loại nội dung nào (ví dụ / bước / luận điểm)?
- **Bold** — dùng nhấn mạnh từ khóa hay câu quan trọng? Tần suất (ít/vừa/dày đặc)?
- **Italic** — có không? Dùng để nhấn giọng / nêu tên riêng / trích dẫn / ngoại ngữ?
- **Blockquote** — có không? Dùng để trích người khác / tự trích / nhấn ý?
- **Code block / inline code** — chỉ nếu tác giả viết tech. Nếu không phải tech → skip.
- **Độ dài đoạn văn TB** — đếm số câu trong đoạn (đo 30 đoạn mẫu). Ghi khoảng: "2-4 câu/đoạn".
- **Emoji/emoticon** — có không? Loại nào? Đặt ở đâu (đầu heading / giữa câu / cuối)?
- **Dấu chấm lửng (…)** — có không? Để tạo lửng lơ / ngắt nhịp / bỏ ý?
- **Em-dash (—)** — có dùng không? Để mở rộng / chèn giải thích / thay ngoặc?
- **Whitespace rhythm** — đoạn ngắn xen dài có chủ đích? Hay đồng đều?

**Trích bằng chứng**: ghi rõ "bài X dùng 3 heading, 2 list, không emoji, đoạn TB 3 câu".

---

## 7. Tư duy & logic

**Mục tiêu**: Hiểu cách tác giả xây lập luận và xử lý phản biện.

**Khảo sát:**

- **Pattern lập luận**:
  - **Quy nạp** — từ nhiều ví dụ → rút quy luật.
  - **Diễn dịch** — từ nguyên tắc → áp dụng case.
  - **Phản biện** — nêu quan điểm đối lập → đả phá.
  - **Kể chuyện → rút bài học** — câu chuyện rồi moral.
  - **Socratic** — hỏi dồn để reader tự nhận ra.
  - **Analogy-based** — lập luận qua so sánh với case khác.
- **Xử lý counter-argument**:
  - **Né** — không nhắc tới phản biện.
  - **Đối diện** — nêu rõ phản biện → trả lời.
  - **Giễu cợt** — nêu phản biện để chế nhạo.
  - **Steelman** — trình bày phản biện mạnh nhất rồi vẫn bác.
- **Tuyệt đối vs. nuance**:
  - Tuyệt đối: "luôn", "không bao giờ", "mọi", "tất cả", "chắc chắn".
  - Nuance: "thường", "có thể", "tùy", "phần lớn", "đôi khi".
  - Đếm tỷ lệ → tác giả thiên về cực đoan hay có chừng mực?
- **Cấp độ trừu tượng** — tác giả ở tầng cao (lý thuyết, nguyên tắc) hay tầng thấp (case cụ thể, con số)? Có lên-xuống linh hoạt không?

**Trích bằng chứng**: 1 câu thể hiện pattern lập luận, 1 câu thể hiện cách xử lý đối lập (nếu có).

---

## 8. Quirks cá nhân

**Mục tiêu**: Bắt những pattern lặp ≥3 lần KHÔNG rơi vào 7 chiều trên — cái làm tác giả "độc nhất".

**Khảo sát cần tìm:**

- **Thói quen mở ngoặc** — hay chèn (ghi chú) giải thích giữa câu?
- **Viết hoa nhấn mạnh** — HAY VIẾT HOA hẳn một từ cho nhấn?
- **Tagline/catchphrase** — câu lặp qua nhiều bài (VD: "Thế thôi.", "Chấm hết.", "Bạn hiểu ý tôi chứ?").
- **Câu hỏi đóng bài** — có bài nào cũng kết bằng 1 câu hỏi không?
- **Mở bài bằng cùng 1 mô-tuýp** — VD 3 bài đều mở bằng thời tiết ("Hôm nay trời...").
- **Dùng tên riêng/nickname** — hay gọi cùng một nhân vật (vợ, bạn thân, con) làm "nhân vật phụ" lặp lại?
- **Số đặc biệt** — hay dùng một con số cụ thể không lý do (3 thứ, 7 điều...)?
- **Dấu câu độc đáo** — hay dùng ba chấm, gạch ngang dồn dập, chấm than liên tiếp?
- **Đi lạc đề có chủ đích** — hay ngắt mạch chính để kể một chuyện khác rồi quay lại?

**Quy tắc**: pattern chỉ ghi nhận khi **lặp ≥3 lần** qua ≥2 bài khác nhau.

**Trích bằng chứng**: 2-3 instance của cùng pattern từ các bài khác nhau, để chứng minh đó là pattern thật chứ không phải trùng hợp.

---

## Quy trình gợi ý khi phân tích

1. **Scan nhanh toàn corpus** lần 1 — nắm cảm nhận tổng thể (tone, persona, domain).
2. **Quét tuần tự từng bài** — ghi chú nhanh vào scratch pad cho 8 chiều.
3. **Tổng hợp pattern** — cái gì lặp ≥2 lần mới ghi nhận.
4. **Chọn bằng chứng đắt nhất** cho mỗi đặc điểm — ưu tiên câu ngắn, đặc trưng, dễ đọc.
5. **Tìm signature phrases** qua đếm tần suất cụm 2-4 từ phổ biến (bỏ stopwords).
6. **Soạn "công thức tái tạo"** — biến đặc điểm thành thao tác cụ thể, để AI khác đọc xong viết được.
7. **Self-check** theo checklist trong SKILL.md.
