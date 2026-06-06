# Decision Brief — {Tên hạng mục}

> Template output cuối của skill. Mặc định in thẳng ra chat. Bỏ phần 4 nếu verdict là No-Go hoặc Cần thêm thông tin. Giữ giọng gọn, mỗi tuyên bố gắn bằng chứng hoặc nhãn giả định.

## 1. Hạng mục

- **Mô tả**: {một dòng tóm tắt hạng mục}
- **Loại**: {bug | feature | techdebt | task} — {một câu vì sao gán loại này}

## 2. Reality check

- **Trạng thái xác minh**: {verified | một phần | chưa verify được}
- **Bằng chứng**:
  - {bằng chứng 1 — vd "test `X` fail tại commit abc123, git blame chỉ tới PR #42"}
  - {bằng chứng 2}
- **{Reproduction & root-cause (bug) | Need & alignment (feature/task) | Đau & cost-of-delay (techdebt)}**:
  - {nội dung tùy loại — bug: reproduce thế nào, root cause ở đâu; feature: nhu cầu gốc & mức align; techdebt: đau đo được ra sao}

## 3. Verdict

**{Go | No-Go | Cần thêm thông tin}**

- **Lý do** (gắn bằng chứng): {vì sao verdict này, trỏ về mục 2}
- {Nếu No-Go: ghi rõ điều kiện nào thay đổi thì nên xem lại}
- {Nếu Cần thêm thông tin: ghi rõ giả định then chốt nào đang treo, cần đào/hỏi gì để gỡ}

## 4. Priority _(chỉ khi Go)_

- **Khung áp dụng**: {RICE | ICE | WSJF} — {một câu vì sao chọn khung này cho hạng mục này}

**Bảng điểm:**

| Yếu tố | Giá trị | Ghi chú |
|---|---|---|
| {Reach / Impact / ...} | {...} | {cơ sở ước lượng hoặc nhãn giả định} |
| ... | ... | ... |
| **Điểm tổng** | **{...}** | {công thức đã dùng} |

- **P-level**: **{P0 | P1 | P2 | P3}**
- **Lý do diễn giải**: {một câu nối điểm + bối cảnh → P-level, vd "ICE=320 nhưng là bug chặn checkout của khách đang trả tiền → P0"}

## 5. Giả định & khoảng trống

**Giả định:**

- _Then chốt_: {giả định mà nếu sai thì verdict đảo chiều — nên đã thành bằng chứng trước khi Go}
- _Phụ_: {giả định ảnh hưởng độ chính xác điểm số, kéo Confidence xuống thấp}

**Khoảng trống thông tin:**

- {điều chưa biết, chưa đào/hỏi ra được — để user tự cân nhắc}
