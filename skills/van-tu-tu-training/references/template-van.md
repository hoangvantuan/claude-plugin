# Template VĂN — Kiến Thức Nền Tảng (10%)

**Mục đích:** Cung cấp đúng và đủ kiến thức cho module này để người học có thể suy tư và thực hành.

## 4 nguyên tắc giải thích sâu — Bắt buộc áp dụng khi viết Văn

Văn tốt không phải Văn đẹp, mà Văn người học **tiêu hoá được**. Phần lớn tài liệu training fail vì viết Văn theo kiểu sách giáo khoa — tóm tắt đúng nhưng không ai hiểu. 4 nguyên tắc dưới đây để tránh bẫy đó.

| Nguyên tắc | Yêu cầu | Ví dụ sai | Ví dụ đúng |
|---|---|---|---|
| **1. Từ quen → lạ** | Mỗi khái niệm mới phải neo vào thứ người học đã biết | "Feedback loop là cơ chế tự điều chỉnh..." | "Bạn biết điều hoà không? Nóng lên → máy chạy → lạnh xuống → máy tắt. Đó là feedback loop." |
| **2. Ẩn dụ bắt buộc** | Mỗi khái niệm trừu tượng cần ít nhất 1 ẩn dụ cụ thể | "SBI gồm Situation, Behavior, Impact." | "SBI như chụp X-quang: Situation là vị trí chụp, Behavior là hình ảnh thấy, Impact là chẩn đoán ý nghĩa." |
| **3. "Tại sao" trước "là gì"** | Dẫn người học qua vấn đề → manh mối → kết luận, không nhảy thẳng vào định nghĩa | Bắt đầu module bằng "Định nghĩa SBI là..." | Bắt đầu bằng "Bạn từng feedback cho nhân viên mà họ phản ứng tiêu cực chưa? Vì sao? Vì bạn nói 'Em làm không tốt' thay vì chỉ ra cụ thể. Đây là nơi SBI xuất hiện..." |
| **4. Đa góc nhìn** | Trình bày khái niệm từ nhiều vai để người học tự xây mental model đa diện | Chỉ giải thích từ góc sếp | "Nếu bạn là sếp đang feedback: ... Nếu bạn là nhân viên nhận feedback: ... Nếu bạn là đồng nghiệp chứng kiến: ..." |

**Rule kiểm tra:** Mỗi khái niệm trong Văn đã đi qua đủ 4 nguyên tắc chưa? Đọc lại đoạn đó và tự hỏi:

- Có neo vào thứ quen thuộc không? (Từ quen → lạ)
- Có ẩn dụ cụ thể không? (Ẩn dụ bắt buộc)
- Có dẫn dắt từ vấn đề không, hay nhảy thẳng định nghĩa? (Tại sao trước)
- Có nhiều góc nhìn không? (Đa góc nhìn)

Thiếu 1 → bổ sung. Thiếu 2+ → viết lại khái niệm đó.

## Template `core_reading.md`

```markdown
# [Tên Module] — Kiến Thức Nền Tảng

## Tại sao chủ đề này quan trọng?
[2-3 câu — nêu vấn đề thực tế mà người học đang gặp]

## Khái niệm cốt lõi

### 1. [Khái niệm A]
**Định nghĩa:** [1 câu rõ ràng]
**Ví dụ thực tế:** [Tình huống gần gũi với công việc người học]
**Áp dụng:** Bạn sẽ dùng khái niệm này trong [Bài thực hành cụ thể của module này]

### 2. [Khái niệm B]
[Cùng cấu trúc — tối đa 3-5 khái niệm/module]

## Framework/Mô hình chính
[1 sơ đồ hoặc bảng tóm tắt — nắm toàn bộ module trong 1 hình]

## Tóm tắt 1 phút
- Ý chính 1: ___
- Ý chính 2: ___
- Ý chính 3: ___

→ Tiếp theo: Chuyển sang phần TƯ để suy tư về module này.
```

## Template `knowledge_check.md`

```markdown
# Knowledge Check — [Tên Module]

Trả lời nhanh để kiểm tra mức độ nắm kiến thức. Không cần hoàn hảo.
Nếu sai 3+ câu, đọc lại phần tương ứng trong core_reading.

## Câu 1: [Khái niệm A]
[Câu hỏi trắc nghiệm hoặc đúng/sai]

## Câu 2: [Tình huống]
Trong tình huống sau, bạn nên áp dụng gì?
"[Mô tả ngắn — liên quan đến bài thực hành sắp làm]"

[... 5-10 câu tổng cộng ...]

## Đáp án
[Liệt kê + giải thích ngắn]
```

## Checklist chất lượng Module Văn

**Dung lượng & kết nối:**
- [ ] Dưới 10 trang / 20 phút đọc cho module này?
- [ ] Không trùng lặp kiến thức với module khác?
- [ ] Mọi thứ đều dẫn đến phần Tư hoặc Tu của chính module này?
- [ ] Có tóm tắt cuối?

**4 nguyên tắc giải thích sâu (mỗi khái niệm phải đạt đủ):**
- [ ] Từ quen → lạ: khái niệm neo vào thứ người học đã biết?
- [ ] Ẩn dụ bắt buộc: mỗi khái niệm trừu tượng có ít nhất 1 ẩn dụ cụ thể?
- [ ] "Tại sao" trước "là gì": dẫn dắt từ vấn đề thực → kết luận, không nhảy thẳng định nghĩa?
- [ ] Đa góc nhìn: trình bày từ nhiều vai (người hành động / người nhận / người quan sát)?
