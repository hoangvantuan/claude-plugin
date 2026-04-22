---
name: planning-content
description: "Lên dàn ý, lập kế hoạch nội dung chi tiết cho bài viết Blog. Kích hoạt khi user muốn lên dàn ý, tạo outline, lập plan viết. KHÔNG dùng để trực tiếp viết bài hoàn chỉnh."
disable-model-invocation: true
---

# Planning Content

Workflow: Phân tích Input → Research → Xây dựng hệ thống Khung bài viết (Framework/Outline).

**Nguyên tắc cốt lõi:**

- Skill này CHỈ tập trung vào việc tạo ra các bản thiết kế (outline/framework) nội dung chi tiết.
- Không viết bài hoàn chỉnh. Việc viết bài sẽ do skill khác phụ trách.

## Phase 1: Plan & Structure

### Step 1: Detect Input

Xác định loại input từ user:

- **Topic thuần** — chỉ có chủ đề, cần research từ đầu.
- **Notes/outline** — có sẵn ý tưởng, cần structure lại.
- **URL** — bài viết/tài liệu online, cần phân tích + mở rộng.
- **File/document** — tài liệu đã có, cần extract ideas.

### Step 2: Interview

Hỏi tất cả câu hỏi trong 1 lượt để tiết kiệm thời gian:

1. **Audience**: Ai là người đọc chính? (VD: startup founders, marketer, developer...).
2. **Goals**: Mục tiêu chính? (educate / engage / convert / thought leadership).
3. *(Optional)* **Constraints**: Có yêu cầu đặc biệt nào không? (deadline, brand guidelines, topics to avoid).

*Ngoại lệ (Fast-track): Nếu input ban đầu đã cung cấp đủ ngữ cảnh (Audience, Goal) hoặc user yêu cầu "làm luôn", hãy tự động giả định các sensible defaults và bỏ qua Step 2 để sang thẳng Step 3.*

### Edge Cases

- **Input quá ngắn (1-2 câu, không có detail):** Hỏi user bổ sung context hoặc dùng web research mở rộng. Giới hạn blog types khả dụng: How-to Guide, Quick Insight, Listicle.
- **Thiếu data cho Deep Analysis / Case Study:** Nếu web research không đủ data/số liệu → chuyển sang type phù hợp hơn (Opinion, Explainer) thay vì tạo khung với data thiếu.
- **Input là chủ đề quá rộng:** Narrow down bằng Interview (Step 2) — yêu cầu user chọn góc cụ thể trước khi plan.

### Step 3: Research

- WebSearch 3-5 queries liên quan topic + audience + trends.
- Nếu input là URL → WebFetch phân tích nội dung.
- Thu thập: data, số liệu, góc nhìn mới, content gaps.
- Ghi nguồn cho mọi data point.

### Step 4: Generate Content Frameworks

Đề xuất số lượng **khung bài viết (framework/outline)** bao phủ toàn bộ nội dung input:

- **Topic thuần** → 3-10 khung bài (tùy scope).
- **Notes/outline** → theo số ý tưởng có sẵn.
- **URL/article** → 5-15 khung bài (tùy độ dài + density).
- **Sách/tài liệu dài** → **Bao phủ toàn bộ giá trị cốt lõi**. Chia thành **batches** (mỗi batch ~10 khung bài) để quản lý. Đảm bảo không bỏ sót chapter/concept quan trọng nào.

**Nguyên tắc xây dựng dàn ý:**

- **1 bài = 1 chủ đề duy nhất.** Mỗi khung bài tập trung vào đúng 1 ý chính (concept, framework, câu chuyện, bài học).
- Xây dựng outline chi tiết tuân thủ chặt chẽ theo các structure trong `content-frameworks.md` (PAS, Tháp ngược, Step-by-step...).
- Dàn ý phải đủ chi tiết để skill viết bài sau này có thể bám sát 100% không cần tự suy luận thêm ý chính.

Mỗi khung bài viết có cấu trúc như sau:

```
### Bài [N]: [Tiêu đề đề xuất]

- **Type:** [Load từ references/blog-types.md]
- **Framework:** [Chọn cấu trúc theo references/content-frameworks.md, vd: PAS, Inverted Pyramid...]
- **Angle:** [Góc tiếp cận cụ thể]
- **Outline Chi tiết:**
  - [Phần 1 của Framework]: Điểm chính 1, data hỗ trợ, ví dụ.
  - [Phần 2 của Framework]: Điểm chính 2, data hỗ trợ, ví dụ.
  - [Phần 3 của Framework]: Điểm chính 3, conclusion/takeaway.
- **Word count target:** [Ước tính]
```

### Step 5: Save Output

Lưu kết quả thành nhiều file để dễ quản lý:

- Sinh ra file `{CWD}/{output-dir}/index.md` — chứa Overview chiến dịch và danh sách các link tới file dàn ý.
- Mỗi khung bài viết được lưu thành file riêng: `{CWD}/{output-dir}/framework-[NN]-[slug].md`.
- Sinh ra file `{CWD}/{output-dir}/research.md` — data đã research với sources.

**Với input dài (sách, tài liệu lớn) xử lý theo batch:**

- Trước tiên, tạo **content map** tổng quan: liệt kê tất cả chapters/concepts cốt lõi cần cover.
- Chia thành batches, mỗi batch ~10 khung bài, tạo framework cho batch đầu tiên.
- **Tạo Checklist Quản lý:** Thêm checklist tiến độ dạng markdown block (vd: `- [x] Batch 1 (Chương 1-3) \n - [ ] Batch 2 (Chương 4-6)`) vào `index.md` hoặc in ra console để tránh lạc bước.
- **Coverage check (BẮT BUỘC):** Sau mỗi batch, đối chiếu content map — liệt kê rõ concepts nào ĐÃ cover, concepts nào CHƯA cover. Tiếp tục tạo khung batch mới cho đến khi 100% content map được cover.
- Cập nhật lại file `index.md` sau mỗi batch.
- Hỏi user confirm trước khi làm batch tiếp theo.

Hỏi user: "Đã hoàn thành bộ khung dàn ý cho [N] bài. Bạn có muốn điều chỉnh khung bài nào trước khi chuyển cho skill viết bài xử lý không?"

## Constraints

- Output tiếng Việt (trừ khi user yêu cầu khác).
- Outline bắt buộc phải đúng structure template theo type definition trong references.
- Outline phải đủ chi tiết, có ví dụ mồi và data cụ thể.
- Research data phải cite nguồn.
- Default output dir: `{CWD}/content-planner/[topic-slug]/` nếu user không chỉ định.

## Output Format

Quy trình này sẽ sinh ra nhiều file được quản lý bởi một file index:

**1. File `index.md`:**

```
# Content Frameworks: [Topic]

## Overview
- Audience: [...]
- Goals: [...]
- Tổng số khung bài: [N]

## Danh sách Frameworks
1. [Bài 1: Tiêu đề](framework-01-slug.md)
2. [Bài 2: Tiêu đề](framework-02-slug.md)
...
```

**2. Các file `framework-[NN]-[slug].md`:**
Chứa nội dung chi tiết của từng khung bài (tuân theo format ở Step 4).

## References

- [references/blog-types.md](references/blog-types.md) — 6 blog type guidelines
- [references/content-frameworks.md](references/content-frameworks.md) — Writing frameworks (PAS, Inverted Pyramid, etc.)
