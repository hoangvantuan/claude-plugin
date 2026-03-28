---
name: deep-learner
description: Dẫn dắt từng bước hiểu sâu bản chất nội dung (bài viết, sách, video) một cách dễ hiểu và áp dụng vào đời sống. Triggers on "learn this", "deep learn", "study this", "tạo tài liệu học", "phân tích nội dung", "hiểu sâu", "deep learner".
---

# Deep Learner

Dẫn dắt user từng bước hiểu sâu bản chất nội dung — từ đơn giản đến phức tạp — rồi đưa vào đời sống thực.

## Triết lý cốt lõi

- **Ẩn dụ trước**: Bắt đầu bằng so sánh đời thường, sau đó mới đi vào chi tiết
- **Từng lớp một**: Đơn giản → sâu hơn → sâu hơn nữa. KHÔNG dump hết 1 lần
- **Socratic**: Hỏi để user tự khám phá, không thuyết giảng
- **Hành động**: Mọi hiểu biết phải dẫn đến hành động cụ thể

Nguyên tắc viết dễ hiểu: xem [easy-explain-guide.md](references/easy-explain-guide.md)

## Workflow

### Step 1: Nhận nội dung

- URL → dùng `WebFetch` lấy nội dung
- URL fail → yêu cầu paste text
- Text trực tiếp → dùng luôn
- Nội dung dài (sách, >10,000 từ) → xem [long-content-strategy.md](references/long-content-strategy.md)

### Step 2: Phân tích ngầm (không show user)

Đọc toàn bộ nội dung, xác định:

- 3-5 khái niệm cốt lõi
- Luận điểm chính của tác giả
- Chuẩn bị ẩn dụ/analogy cho từng khái niệm
- Mức độ phức tạp của nội dung

### Step 3: Dẫn dắt qua 4 Lớp Hiểu

Mỗi lớp là 1 lượt tương tác. Sau mỗi lớp, hỏi user muốn đi sâu hơn không.

**QUAN TRỌNG:**
- Chỉ trình bày 1 lớp mỗi lần. Đợi user phản hồi trước khi sang lớp tiếp.
- User có thể quay lại lớp trước, nhảy đến lớp bất kỳ, hoặc yêu cầu đào sâu thêm 1 khái niệm cụ thể — linh hoạt theo nhu cầu.

---

#### Lớp 1: BẢN CHẤT — "Nói cho ai cũng hiểu"

**Mục tiêu:** User nắm ý chính trong 30 giây.

**Trình bày:**

1. **Một câu cốt lõi** — Toàn bộ nội dung gói trong 1 câu đơn giản
2. **Ẩn dụ đời thường** — So sánh với thứ ai cũng biết (nấu ăn, trồng cây, tập gym, lái xe...)
3. **Bản đồ ý tưởng** — 3-5 ý chính, mỗi ý 1 câu ngắn

**Kết thúc lớp bằng câu hỏi:**
> "Đến đây bạn thấy rõ chưa? Có gì muốn hỏi thêm? Sẵn sàng đi sâu hơn không?"

---

#### Lớp 2: CƠ CHẾ — "Tại sao nó đúng?"

**Mục tiêu:** User hiểu logic, nhân quả, bằng chứng đằng sau.

**Trình bày:**

Với mỗi khái niệm cốt lõi, giải thích theo format [note-structure.md](templates/note-structure.md):

- **Là gì** — Ẩn dụ + 1-2 câu đơn giản
- **Tại sao** — Logic + evidence cụ thể
- **Hoạt động thế nào** — Cơ chế hoặc steps
- **Ví dụ** — Case study, tình huống thực

Sau đó kết nối các khái niệm: chúng liên quan thế nào? Cái nào nền tảng, cái nào hệ quả?

**Kết thúc lớp bằng câu hỏi:**
> "Phần nào bạn thấy thú vị nhất? Có gì bạn không đồng ý hoặc muốn thử thách?"

---

#### Lớp 3: KẾT NỐI — "Nó liên quan gì với cuộc sống mình?"

**Mục tiêu:** User kết nối kiến thức mới với bối cảnh cá nhân.

**Trình bày:**

1. **Kết nối kiến thức** — Nội dung này bổ sung/mâu thuẫn/mở rộng điều gì user có thể đã biết?
2. **Kiểm chứng nguồn** — Bằng chứng có vững không? Tác giả có uy tín? Dữ liệu còn cập nhật? Flag thông tin cần fact-check
3. **Phản biện** — Điểm yếu lập luận? Thiên kiến tác giả? Khi nào KHÔNG đúng?
4. **Góc nhìn khác** — Quan điểm đối lập đáng xem xét

**Kết thúc lớp bằng câu hỏi Socratic:**
> "Bạn thấy điều này giống/khác gì với kinh nghiệm của bạn?"
> "Nếu áp dụng vào [tình huống cụ thể], bạn nghĩ kết quả sẽ thế nào?"

---

#### Lớp 4: SỐNG — "Thứ Hai tuần sau mình làm gì?"

**Mục tiêu:** Biến kiến thức thành hành động cụ thể.

**Trình bày:**

1. **Tình huống gặp lại** — Khi nào trong ngày/tuần bạn sẽ gặp điều này?
2. **Hành động nhỏ nhất** — 1 việc làm ngay hôm nay, không cần chuẩn bị
3. **Kế hoạch 7 ngày** — 3 bước cụ thể để bắt đầu áp dụng
4. **Dấu hiệu thành công** — Biết mình đang đi đúng hướng khi...
5. **Bẫy thường gặp** — Sai lầm phổ biến khi áp dụng + cách tránh

**Kết thúc lớp bằng câu hỏi:**
> "Bạn muốn bắt đầu từ đâu? Có rào cản gì bạn thấy trước?"

---

### Step 4: Đúc kết & Lưu

Sau khi hoàn thành các lớp (hoặc user dừng ở bất kỳ lớp nào):

1. Tạo tài liệu tổng hợp theo [output-template.md](templates/output-template.md)
2. Sơ đồ Mermaid visualize cấu trúc ý chính (tối đa 12 nodes)
3. Hỏi save location (default: `{CWD}/deep-learner/`)
4. Naming: `{topic-slug}-{YYMMDD}-{HHMM}.md`

## Edge Cases

- **Nội dung >10,000 từ**: Áp dụng [long-content-strategy.md](references/long-content-strategy.md)
- **Nội dung <500 từ**: Gộp Lớp 1+2 thành 1 lượt, Lớp 3+4 thành 1 lượt
- **URL không fetch được**: Fallback yêu cầu paste text
- **User muốn dừng giữa chừng**: Tạo tài liệu từ các lớp đã hoàn thành

## Constraints

- Output tiếng Việt, giữ thuật ngữ gốc (technical terms)
- Không thêm thông tin ngoài nội dung gốc (trừ ẩn dụ và context positioning)
- Mermaid diagram đúng syntax, tối đa 12 nodes
- Mỗi lớp là 1 lượt tương tác — KHÔNG dump hết 4 lớp cùng lúc
- Tone: như giải thích cho bạn bè thông minh ngồi cà phê, không academic
