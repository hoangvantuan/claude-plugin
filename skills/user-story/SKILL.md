---
name: user-story
description: "Viết, rà soát và tách user story kèm acceptance criteria (Given/When/Then), kiểm tra INVEST và phân rã epic."
---

# User Story

Biến input thô thành user story có persona rõ, vấn đề đúng, outcome đo được, và acceptance criteria xác minh được.

## Khi Nào Dùng

Dùng khi user cần:

- Viết user story mới.
- Chuyển requirement, PRD, epic, hoặc ý tưởng thành user story.
- Viết acceptance criteria theo Given/When/Then.
- Rà soát story theo INVEST.
- Tách epic hoặc story lớn thành story nhỏ.
- Tìm persona hoặc problem statement trước khi viết story.

Không dùng khi việc không liên quan đến giá trị người dùng.

## Nguyên Tắc Lõi

User story tốt trả lời 5 câu:

1. Ai bị ảnh hưởng?
2. Họ đang cố đạt kết quả gì?
3. Điều gì đang chặn họ?
4. Họ muốn làm hành động nào?
5. Làm sao biết story đã xong?

**Không đề cập kỹ thuật.** Story mô tả giá trị và hành vi từ góc nhìn người dùng. Không nhắc đến công nghệ, kiến trúc, giải pháp cài đặt, hay cách triển khai. Ví dụ: viết "đăng nhập nhanh bằng tài khoản Google" thay vì "tích hợp OAuth 2.0 với Google Identity Platform".

Nếu thiếu dữ liệu, đừng bịa. Ghi rõ giả định và hỏi tối đa 3 câu nếu thiếu chặn việc viết.

## Workflow Chuẩn

### Bước 1: Xác Định Mode

- **Ý tưởng mỏng:** Discovery. Làm persona ngắn, problem statement, rồi story.
- **Requirement rõ:** Story. Viết story và acceptance criteria.
- **Epic lớn:** Epic. Viết hypothesis, rồi tách thành story.
- **Story có sẵn:** Review. Rà soát INVEST, acceptance criteria, scope.
- **Story quá to:** Split. Tách theo pattern phù hợp.

### Bước 2: Persona Tối Thiểu

Persona không cần dài. Nhưng "user" quá chung thường yếu.

Ghi ngắn:

```markdown
### Persona
- **Nhóm người dùng:** [persona cụ thể]
- **Bối cảnh:** [họ đang ở đâu, dùng sản phẩm lúc nào]
- **Mục tiêu:** [kết quả họ muốn]
- **Nỗi đau:** [điều đang cản họ]
- **Giả định cần kiểm chứng:** [nếu có]
```

Ưu tiên persona theo hành vi. Ví dụ: "trial user lần đầu đăng nhập" tốt hơn "người dùng".

### Bước 3: Problem Statement

Trước khi viết story, nêu vấn đề từ góc nhìn người dùng.

```markdown
### Problem Statement
[Persona] cần một cách để [kết quả mong muốn] vì [root cause], hiện khiến họ [tác động thực tế hoặc cảm xúc].
```

Tránh nhét sẵn giải pháp. Ví dụ yếu: "User cần nút Google login". Ví dụ tốt: "Trial user cần vào app nhanh vì tạo mật khẩu mới làm họ bỏ dở onboarding".

### Bước 4: Epic Hypothesis, Nếu Input Là Epic

Nếu input rộng hoặc rủi ro cao, viết hypothesis trước:

```markdown
### Epic Hypothesis
- **If we** [giải pháp hoặc hướng can thiệp]
- **for** [persona]
- **then we will** [outcome đo được]
- **We will test by:** [prototype, concierge test, landing page, A/B test, phỏng vấn]
- **Valid if:** [metric + timeframe]
```

Sau đó mới tách epic thành user story.

### Bước 5: Viết User Story

Dùng format Mike Cohn:

```markdown
### User Story [ID]

- **Summary:** [tiêu đề ngắn, tập trung vào giá trị]

#### Use Case
- **As a** [persona cụ thể]
- **I want to** [hành động người dùng thực hiện]
- **so that** [outcome người dùng nhận được]

#### Acceptance Criteria
- **Scenario:** [tình huống chính]
- **Given:** [tiền điều kiện]
- **When:** [hành động kích hoạt]
- **Then:** [kết quả quan sát được]
```

Quy tắc:

- Một story chỉ nên có một `When`.
- Một story chỉ nên có một `Then` chính.
- `When` phải khớp với `I want to`.
- `Then` phải chứng minh `so that`.
- Nếu cần nhiều `When/Then`, chuyển sang Split mode.

### Bước 6: Rà Soát INVEST

Chấm nhanh:

- **Independent:** Story có thể làm độc lập không?
- **Negotiable:** Story còn là điểm mở để thảo luận không?
- **Valuable:** User nhận giá trị thật không?
- **Estimable:** Team có đủ hiểu để ước lượng công sức không?
- **Small:** Hoàn thành và giao được trong 1 đến 5 ngày không?
- **Testable:** Có thể xác minh bằng tiêu chí cụ thể không?

Nếu trượt `Valuable`, quay lại problem statement. Nếu trượt `Small`, tách story.

## Tách Story

Khi story quá lớn, thử các pattern theo thứ tự:

1. **Workflow steps:** tách theo các bước trong hành trình người dùng.
2. **Business rule variations:** tách theo quy tắc nghiệp vụ, quyền, trạng thái.
3. **Data variations:** tách theo loại thông tin hoặc input khác nhau.
4. **Acceptance criteria complexity:** tách theo từng cặp When/Then.
5. **Milestone giá trị:** tách theo từng phần giao được giá trị cho người dùng.
6. **Phụ thuộc bên ngoài:** tách theo bên thứ ba, đối tác, dịch vụ liên kết.
7. **Tiny Acts of Discovery:** nếu còn mơ hồ, đề xuất thử nghiệm nhỏ trước.

Mỗi phần tách phải có giá trị riêng cho người dùng. Không tách theo tầng hệ thống.

## Output Mặc Định

Khi user yêu cầu viết story, trả về:

```markdown
## User Story

### Context
- **Persona:** ...
- **Problem:** ...
- **Assumptions:** ...

### Story
- **Summary:** ...
- **As a** ...
- **I want to** ...
- **so that** ...

### Acceptance Criteria
- **Scenario:** ...
- **Given:** ...
- **When:** ...
- **Then:** ...

### Quality Check
- **INVEST:** ...
- **Split needed:** Yes/No
- **Open questions:** ...
```

Nếu user yêu cầu nhiều story, dùng bảng tóm tắt trước, rồi viết chi tiết từng story.

## Ví Dụ

Input:

```text
trial user login Google để vào app không cần tạo password
```

Output:

```markdown
## User Story

### Context
- **Persona:** Trial user lần đầu vào app.
- **Problem:** Trial user cần vào app nhanh vì tạo mật khẩu mới làm tăng ma sát, hiện khiến họ dễ bỏ dở onboarding.
- **Assumptions:** App đã có trang đăng nhập và hỗ trợ đăng nhập qua Google.

### Story
- **Summary:** Đăng nhập Google để giảm ma sát onboarding.
- **As a** trial user
- **I want to** đăng nhập bằng tài khoản Google
- **so that** tôi vào app ngay mà không cần tạo mật khẩu mới

### Acceptance Criteria
- **Scenario:** Trial user đăng nhập lần đầu bằng Google.
- **Given:** Tôi đang ở trang đăng nhập.
- **Given:** Tôi có tài khoản Google hợp lệ.
- **When:** Tôi chọn "Đăng nhập bằng Google" và cho phép liên kết.
- **Then:** Tôi đã đăng nhập và được chuyển đến bước hướng dẫn sử dụng.

### Quality Check
- **INVEST:** Pass. Story nhỏ, có giá trị, xác minh được.
- **Split needed:** No.
- **Open questions:** Cần xác nhận trang đích sau đăng nhập và trải nghiệm khi đăng nhập Google thất bại.
```

## Script Hỗ Trợ

Dùng script để tạo stub Markdown ổn định, không gọi mạng:

```bash
python3 scripts/user-story-template.py --persona "trial user" --action "log in with Google" --outcome "access the app without creating a new password"
```

Script nằm tại `skills/user-story/scripts/user-story-template.py`.

## Chống Lỗi Thường Gặp

- Không viết "As a user" nếu có thể cụ thể hơn.
- Không để `so that` lặp lại `I want to`.
- Không dùng acceptance criteria mơ hồ như "better UX" hoặc "faster".
- Không viết story cho việc chỉ phục vụ nội bộ mà người dùng không nhận được giá trị.
- Không tách story theo tầng hệ thống (ví dụ: "phần lưu trữ" và "phần hiển thị").
- Không viết full PRD khi user chỉ cần story.
- Không đề cập chi tiết kỹ thuật, công nghệ, hay giải pháp cài đặt trong story.
