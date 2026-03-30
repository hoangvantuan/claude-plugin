# Template Facilitator Hub

**Mục đích:** Cung cấp công cụ cho người dẫn dắt (facilitator) điều phối khoá đào tạo theo Văn-Tư-Tu.

## Template `huong_dan_chung.md`

```markdown
# Hướng Dẫn Facilitation — [Tên Khoá]

## Vai trò Facilitator trong Văn-Tư-Tu

Facilitator KHÔNG PHẢI giảng viên. Bạn là người **tạo điều kiện** để người học tự chuyển hoá.

| Giai đoạn | Vai trò Facilitator | KHÔNG làm |
|-----------|--------------------|-----------|
| **Văn** | Cung cấp tài liệu, định hướng đọc | Giảng bài dài, đọc slide |
| **Tư** | Đặt câu hỏi, phản biện, dẫn dắt thảo luận | Đưa đáp án, phán xét |
| **Tu** | Quan sát, coaching khi cần, tạo môi trường an toàn | Làm thay, kiểm soát quá mức |

## Nguyên tắc vàng

1. **Đừng trả lời — hỏi ngược**
   - Người học hỏi → "Em quan sát thấy gì?" / "Em nghĩ tại sao?"
   - Chỉ trả lời khi người học đã thử tự tìm nhưng thực sự bí

2. **70% thời gian cho Tu**
   - Nếu buổi học > 50% là bạn nói → đang sai
   - Người học phải ĐANG LÀM phần lớn thời gian

3. **Tạo không gian an toàn**
   - Sai là bình thường — miễn là đúc kết được bài học
   - Không ai bị chê trước nhóm

4. **Đúc kết là bắt buộc**
   - Mỗi hoạt động PHẢI kết thúc bằng đúc kết
   - Nếu hết giờ → cắt hoạt động, giữ đúc kết

## Checklist trước mỗi module

- [ ] Đọc README module — nắm mục tiêu + tỷ lệ VTT
- [ ] Chuẩn bị tài liệu Văn (đã in/share?)
- [ ] Đọc trước case study + câu hỏi phản chiếu (phần Tư)
- [ ] Kiểm tra bài thực hành — có đủ tài nguyên/công cụ?
- [ ] Chuẩn bị rubric đánh giá
- [ ] Chia buddy pairs (nếu team)

## Xử lý tình huống thường gặp

| Tình huống | Cách xử lý |
|-----------|------------|
| Người học im lặng, không tham gia | Bắt đầu bằng viết (1 phút viết trước khi chia sẻ) |
| 1 người nói quá nhiều | "Cảm ơn, mời người khác bổ sung góc nhìn khác" |
| Tranh luận đi xa chủ đề | "Ý hay — ghi lại, quay về [chủ đề module]" |
| Người học muốn thêm lý thuyết | "Đủ để thực hành — làm thử rồi thiếu gì bổ sung" |
| Người học nộp deliverable sơ sài | Phản biện bằng câu hỏi, không phán xét. Cho làm lại |
| Khoảng cách trình độ lớn | Buddy pairs: ghép người giỏi + người mới |
```

## Template `module_map.md`

```markdown
# Module Map — [Tên Khoá]

## Prerequisite Map

[Chèn Mermaid flowchart từ 00_TỔNG_QUAN.md]

## Chi tiết từng module

### Module 1: [Tên]
- **Tier:** [Foundation / Core / Advanced / Specialized]
- **Thời lượng:** [X]
- **Tỷ lệ VTT:** [V-T-T]%
- **Mục tiêu:** [1 câu]
- **Deliverable:** [Người học nộp gì?]
- **Lưu ý facilitation:** [Điểm cần chú ý riêng cho module này]

### Module 2: [Tên]
[Cùng cấu trúc]

## Kết nối giữa các module

| Từ module | Đến module | Kiến thức chuyển tiếp |
|-----------|-----------|----------------------|
| 1 | 2 | [Kiến thức nào từ M1 cần cho M2] |
| 1 | 3 | [Kiến thức nào từ M1 cần cho M3] |
```

## Template `lich_trinh_goi_y.md`

```markdown
# Lịch Trình Gợi Ý — [Tên Khoá]

## A. Cá nhân tự học

| Ngày/Tuần | Module | Hoạt động | Thời lượng |
|-----------|--------|-----------|-----------|
| Ngày 1-2 | M1 | Văn: Đọc tài liệu | 1-2 giờ |
| Ngày 3 | M1 | Tư: Phản chiếu + Case study | 1-2 giờ |
| Ngày 4-7 | M1 | Tu: Thực hành + Đúc kết | 3-5 giờ |
| ... | M2 | ... | ... |

## B. Team (5-15 người)

### Tuần 0: Chuẩn bị
- [ ] Facilitator đọc toàn bộ tài liệu khoá
- [ ] Chia buddy pairs
- [ ] Gửi tài liệu Văn Module 1 cho team đọc trước (pre-work)
- [ ] Setup kênh trao đổi (Slack/Teams channel)

### Tuần 1: Module 1 — [Tên]

| Ngày | Hoạt động | Hình thức | Thời lượng | Ghi chú |
|------|-----------|-----------|-----------|---------|
| T2 | Kick-off khoá + Văn M1 | Meeting nhóm | 1 giờ | Giới thiệu khoá, review Văn |
| T3-T4 | Tư M1: Phản chiếu cá nhân | Tự học | 1-2 giờ | Buddy pairs trao đổi |
| T5 | Tư M1: Case study nhóm | Meeting nhóm | 1 giờ | Facilitator dẫn dắt |
| T6-CN | Tu M1: Bắt đầu thực hành | Tự thực hành | 2-3 giờ | |

### Tuần 2: Module 1 (tiếp) + Module 2 (bắt đầu)
| Ngày | Hoạt động | Hình thức | Thời lượng |
|------|-----------|-----------|-----------|
| T2 | Tu M1: Check-in tiến độ | Meeting nhóm | 30 phút |
| T3-T5 | Tu M1: Tiếp tục thực hành | Tự thực hành | |
| T6 | M1 Wrap-up + Đúc kết + Gửi Văn M2 | Meeting nhóm | 1 giờ |

[Tiếp tục theo pattern cho các module sau...]

### Tuần cuối: Wrap-up khoá
| Ngày | Hoạt động | Thời lượng |
|------|-----------|-----------|
| T2-T4 | Teach-back: Mỗi người/buddy pair trình bày 5 phút | 1-2 giờ |
| T5 | After-Action Review khoá | 1 giờ |
| T6 | Survey cuối khoá | 15 phút |

## C. Công ty (rolling deployment)

### Giai đoạn 1: Pilot (4-6 tuần)
- Chọn 1 team (5-10 người) làm pilot
- Facilitator là người thiết kế khoá hoặc được training riêng
- Thu thập feedback, điều chỉnh tài liệu

### Giai đoạn 2: Mở rộng (sau pilot)
- Training facilitator mới từ alumni pilot (train-the-trainer)
- Mỗi facilitator phụ trách tối đa 15 người
- Rolling deployment: team mới bắt đầu mỗi 2-4 tuần

### Giai đoạn 3: Module Library
- Đưa modules đã validate vào thư viện chung
- Team tự chọn module phù hợp (theo tier + prerequisite)
- Facilitator chỉ hỗ trợ khi cần, không cần dẫn toàn bộ

### Buddy Pairs — Hướng dẫn

**Cách ghép:**
- Ghép chéo trình độ (người có kinh nghiệm + người mới)
- Hoặc ghép chéo phòng ban (góc nhìn đa dạng)
- KHÔNG ghép theo sở thích cá nhân

**Vai trò buddy:**
- Trao đổi bài Tư (câu hỏi phản chiếu) với nhau
- Review deliverable của nhau trước khi nộp
- Check-in nhau 2-3 lần/tuần (5-10 phút)
- Không phải dạy nhau — mà cùng HỌC
```
