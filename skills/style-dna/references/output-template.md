# Output template — Style guide markdown

Template cố định để output style guide. Không thay đổi cấu trúc heading. Điền nội dung vào các chỗ `[...]`.

---

## Template chính xác (copy y nguyên khung)

```markdown
# Style Guide: [Tên tác giả]

> **Metadata**
> - Số bài phân tích: [N]
> - Nguồn corpus: [file / URL / paste]
> - Ngày tạo: [YYYY-MM-DD]
> - Độ tin cậy: [Rất thấp / Trung bình / Khá / Cao]

## Tóm tắt 1 dòng

[≤25 từ — bản chất văn phong, để người khác đọc xong hình dung được ngay. VD: "Suồng sã như bạn thân, câu cụt nhấn nhịp, ẩn dụ thể thao, hay đá xéo cuối đoạn, đóng bài bằng câu hỏi."]

## Chi tiết 8 chiều

### 1. Giọng điệu & persona

- **Mức formal**: [1-5] — [mô tả ngắn].
- **Tone chủ đạo**: [nghiêm/hài/châm biếm/nhiệt huyết/trầm/...] — "[trích dẫn thể hiện tone]" (bài: [tên/số]).
- **Ngôi xưng tác giả**: [tôi/mình/ta/...] — "[trích dẫn]" (bài: [tên/số]).
- **Cách gọi reader**: [bạn/anh em/...] — "[trích dẫn]" (bài: [tên/số]).
- **Thái độ với chủ đề**: [chuyên gia/bạn kể chuyện/...] — "[trích dẫn]" (bài: [tên/số]).

### 2. Cấu trúc bài

- **Pattern mở bài**: [câu hỏi / anecdote / tuyên bố / ...] — "[trích dẫn đoạn mở]" (bài: [tên/số]).
- **Xương sống triển khai**: [chronological/problem-solution/list-based/...] — ví dụ: [mô tả ngắn pattern trong bài X].
- **Pattern kết bài**: [call-to-action / circle back / reflection / ...] — "[trích dẫn đoạn kết]" (bài: [tên/số]).

### 3. Nhịp & độ dài câu

- **Độ dài câu trung bình**: [X-Y từ/câu].
- **Câu cụt 3-5 từ**: [có/không], chức năng [nhấn/chuyển/kết] — "[trích dẫn]" (bài: [tên/số]).
- **Tỷ lệ câu đơn/phức/ghép**: [X%] / [Y%] / [Z%] (ước lượng).
- **Thủ pháp nhịp**:
  - [Anaphora/song hành/đảo ngữ/câu hỏi tu từ]: "[trích dẫn]" (bài: [tên/số]).

### 4. Từ vựng đặc trưng (fingerprint)

- **Từ hiếm mà lặp**: [liệt kê] — ví dụ "[trích]" (bài: [tên/số]).
- **Slang/tiếng lóng**: [có/không] — "[trích]" (bài: [tên/số]).
- **Thuật ngữ chuyên ngành**: [domain] — "[trích]" (bài: [tên/số]).
- **Filler words cá nhân**: [liệt kê] — "[trích]" (bài: [tên/số]).

### 5. Kỹ thuật tu từ

- **Metaphor domain áp đảo**: [thể thao/ẩm thực/chiến tranh/...] — "[trích ẩn dụ tiêu biểu]" (bài: [tên/số]).
- **Nguồn ví dụ quen dùng**: [lịch sử/phim/đời thường/khoa học] — "[trích]" (bài: [tên/số]).
- **Cách chuyển đoạn**: [từ nối / câu cầu / whitespace / heading] — mô tả + ví dụ.
- **Cách dùng hài**: [tự trào / đá xéo / one-liner / không có] — "[trích]" (bài: [tên/số]).

### 6. Format & typography

- **Heading**: [có/không], tần suất [X/bài TB], cấp nào chủ yếu.
- **List**: [có/không], tần suất, dùng cho nội dung loại nào.
- **Bold/italic**: [có/không], cách dùng.
- **Blockquote/code block**: [có/không].
- **Độ dài đoạn TB**: [X-Y câu/đoạn].
- **Emoji**: [có/không], loại nào.
- **Dấu chấm lửng (…) / em-dash (—)**: [có/không], cách dùng.
- **Whitespace rhythm**: [đoạn ngắn xen dài / đều đều] — mô tả.

### 7. Tư duy & logic

- **Pattern lập luận chính**: [quy nạp/diễn dịch/phản biện/kể chuyện→bài học/...] — "[trích dẫn thể hiện pattern]" (bài: [tên/số]).
- **Xử lý counter-argument**: [né/đối diện/giễu cợt/steelman] — "[trích]" (bài: [tên/số]) hoặc "Không đủ dữ liệu".
- **Tuyệt đối vs. nuance**: [thiên cực đoan / có chừng mực] — tần suất từ tuyệt đối vs. hedging word.
- **Cấp độ trừu tượng**: [cao/thấp/linh hoạt] — mô tả.

### 8. Quirks cá nhân

- **[Quirk 1]**: mô tả — "[trích 1]" (bài X), "[trích 2]" (bài Y), "[trích 3]" (bài Z).
- **[Quirk 2]**: mô tả — 3 instances.
- ... (chỉ list quirk lặp ≥3 lần ở ≥2 bài).

## Signature phrases (top 15)

| Cụm từ | Tần suất | Ví dụ ngữ cảnh |
|--------|----------|----------------|
| "[cụm từ]" | [X lần / Y bài] | "[trích câu chứa cụm]" |
| ... | ... | ... |

## Công thức tái tạo

Hướng dẫn 5-8 bước cụ thể, thao tác được, để AI/người khác viết một bài mới giống giọng tác giả này:

1. [Bước 1 — rất cụ thể. VD: "Mở bài bằng câu cụt ≤7 từ dạng tuyên bố."]
2. [Bước 2 — VD: "Đoạn 1 giới thiệu ngữ cảnh đời thường, 2-3 câu, ngôi 'tôi'."]
3. [Bước 3 — VD: "Chen ít nhất 1 ẩn dụ từ domain thể thao trong thân bài."]
4. [Bước 4 — VD: "Mỗi đoạn 2-4 câu, không vượt 5 câu."]
5. [Bước 5 — VD: "Dùng ít nhất 1 câu hỏi tu từ giữa bài để ngắt nhịp."]
6. [Bước 6 — VD: "Kết bài bằng câu cụt tuyên bố hoặc câu hỏi mở cho reader."]
7. [Bước 7 — optional, nếu có quirk độc nhất cần nhắc riêng.]

## Anti-patterns (thứ KHÔNG được làm khi viết theo style này)

- [Điều tác giả không bao giờ làm, có bằng chứng từ corpus].
- VD: "Không dùng emoji (0 instance trong 10 bài)."
- VD: "Không viết đoạn >5 câu (đoạn dài nhất trong corpus: 4 câu)."
- VD: "Không dùng từ chuyên ngành kỹ thuật (corpus toàn từ đời thường)."
- VD: "Không tuyên bố tuyệt đối kiểu 'luôn luôn' / 'không bao giờ' (hedging word gấp 3 lần từ tuyệt đối)."
```

---

## Quy tắc điền template

1. **Không bỏ heading nào**. Nếu một chiều "không đủ dữ liệu", vẫn giữ heading, ghi nội dung: `> Không đủ dữ liệu để kết luận (cần thêm corpus).`
2. **Trích dẫn phải nguyên văn**, đặt trong `"..."`, kèm `(bài: [tên/số])`.
3. **Độ dài tóm tắt 1 dòng ≤25 từ**. Đếm cẩn thận.
4. **Bảng signature phrases**:
  - Tối đa 15 dòng, tối thiểu 5 dòng (nếu đủ data).
  - Sắp theo tần suất giảm dần.
  - Chỉ cụm xuất hiện ≥2 lần.
  - Cột "Tần suất" ghi dạng `X lần / Y bài` (số lần xuất hiện / số bài khác nhau có cụm).
5. **Công thức tái tạo** phải THAO TÁC ĐƯỢC:
  - Sai: "Viết giống tác giả, phong cách suồng sã."
  - Đúng: "Mở bài bằng 1 câu cụt ≤5 từ, xuống dòng, kế đến đoạn 3-4 câu kể ngữ cảnh đời thường, ngôi 'tôi'."
  - Mỗi bước phải có yếu tố định lượng (số từ, số câu, vị trí, loại cụ thể).
6. **Anti-patterns** phải có bằng chứng từ corpus (VD "0 emoji trong 10 bài"), không phát biểu chung chung ("không dùng từ sến").
7. **Metadata đầu file**: luôn có đủ 4 dòng số bài / nguồn / ngày / độ tin cậy.
