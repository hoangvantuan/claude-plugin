---
name: content-planner
description: Plan and write full content for Facebook posts and blog articles from any input (topic, notes, URL, documents). Two-phase workflow - Phase 1 creates content plan with briefs, Phase 2 writes full articles with advanced writing style (3-archetype system, anti-AI writing, self-critique process). Auto-researches via web search. Use when user wants to "plan content", "write blog post", "create Facebook posts", "content calendar", "lên kế hoạch viết bài", "viết bài cho Facebook/blog", or "lập content plan".
---

# Content Planner

Lên kế hoạch và viết bài đầy đủ cho Facebook + Blog từ bất kỳ input nào. 2-phase workflow: Plan trước, Write sau.

## Phase 1: Plan

### Step 1: Detect Input

Xác định loại input từ user:

- **Topic thuần** — chỉ có chủ đề, cần research từ đầu
- **Notes/outline** — có sẵn ý tưởng, cần structure lại
- **URL** — bài viết/tài liệu online, cần phân tích + mở rộng
- **File/document** — tài liệu đã có, cần extract ideas

### Step 2: Interview

Ask one at a time, conversational:

1. **Audience**: "Ai là người đọc chính? (VD: startup founders, marketer, developer...)"
2. **Tone**: "Tone bạn muốn? (chuyên gia / thân thiện / provocative / storytelling)"
3. **Goals**: "Mục tiêu chính? (educate / engage / convert / thought leadership)"
4. **Platform priority**: "Ưu tiên platform nào trước? (blog trước rồi derive FB, hay FB trước?)"
5. *(Optional)* **Constraints**: "Có yêu cầu đặc biệt nào không? (deadline, brand guidelines, topics to avoid)"

### Step 3: Research

- WebSearch 3-5 queries liên quan topic + audience + trends
- Nếu input là URL → WebFetch phân tích nội dung
- Thu thập: data, số liệu, góc nhìn mới, content gaps
- Ghi nguồn cho mọi data point

### Step 4: Generate Content Plan

Đề xuất số lượng bài **không giới hạn**, tỷ lệ thuận với độ sâu/rộng của input:

- **Topic thuần** → 3-10 bài (tùy scope)
- **Notes/outline** → theo số ý tưởng có sẵn
- **URL/article** → 5-15 bài (tùy độ dài + density)
- **Sách/tài liệu dài** → **bao phủ toàn bộ giá trị cốt lõi** — có thể 20, 30, 50+ bài. Chia thành **batches** (mỗi batch ~10 bài) để quản lý. Đảm bảo không bỏ sót chapter/concept quan trọng nào.

**Nguyên tắc:** Số lượng bài phục vụ mục tiêu truyền tải đầy đủ nội dung gốc. Quality không đánh đổi quantity — mỗi bài vẫn phải self-contained và có giá trị độc lập.

Mỗi bài có brief:

```
### Bài [N]: [Tiêu đề đề xuất]
- **Platform:** Blog / Facebook
- **Type:** [Load từ references/blog-types.md hoặc references/facebook-types.md]
- **Framework:** [Chọn theo type — xem mapping trong references/blog-types.md]
- **Angle:** [Góc tiếp cận cụ thể]
- **Hook idea:** [1-2 câu hook]
- **Key points:** [3-5 bullet points]
- **CTA:** [Call to action]
- **Target reader:** [Ai sẽ đọc bài này]
- **Word count:** [Ước tính]
```

Gợi ý thứ tự đăng (thường: blog trước → derive Facebook posts từ content blog).

### Step 5: Save Output

- `{CWD}/{output-dir}/plan.md` — overview + tất cả briefs (nếu nhiều batch thì ghi rõ batch nào)
- `{CWD}/{output-dir}/research.md` — data đã research với sources

**Với input dài (sách, tài liệu lớn):**
- Trước tiên, tạo **content map** tổng quan: liệt kê tất cả chapters/concepts cốt lõi cần cover
- Chia thành batches, mỗi batch ~10 bài, plan batch đầu tiên chi tiết
- Hỏi user confirm trước khi plan batch tiếp theo

Hỏi user: "Plan đã xong. Bạn muốn viết bài nào? (VD: 'viết bài 1, 3, 5' hoặc 'viết tất cả')"

## Phase 2: Write

Trigger: User chỉ định bài cần viết (VD: "viết bài 1, 3" hoặc "write all articles from plan").

### Step 1: Read Plan

Đọc `plan.md` từ output dir để lấy briefs.

### Step 2: Write Each Article

Với mỗi bài được chọn:

1. Load type guidelines từ [references/blog-types.md](references/blog-types.md) hoặc [references/facebook-types.md](references/facebook-types.md)
2. Load [references/writing-system.md](references/writing-system.md) — áp dụng cho TẤT CẢ bài viết (cả Blog lẫn Facebook)
3. Load framework từ [references/content-frameworks.md](references/content-frameworks.md)
4. Viết full content theo brief + type structure + framework + writing system
5. **Blog** → markdown format, đúng structure template của type, headings viết như insight
6. **Facebook** → plain text, xuống dòng nhiều, hook 3 dòng đầu phải mạnh

### Step 3: Save Articles

Mỗi bài lưu file riêng:

- Blog: `{CWD}/{output-dir}/blog-[NN]-[type]-[slug].md`
- Facebook: `{CWD}/{output-dir}/fb-[NN]-[type]-[slug].md`

## Constraints

- Output tiếng Việt (trừ khi user yêu cầu khác)
- Blog phải đúng structure template theo type definition trong references
- Facebook post không dùng outbound links (giảm reach)
- Mỗi bài viết self-contained, đọc độc lập được
- Research data phải cite nguồn
- Không giới hạn số bài/plan — số lượng tỷ lệ với độ sâu input. Với input dài (sách, khóa học), chia thành batches ~10 bài, plan từng batch tuần tự để đảm bảo bao phủ toàn bộ giá trị cốt lõi
- Default output dir: `{CWD}/content-planner/[topic-slug]/` nếu user không chỉ định

## Output Format

Phase 1 output `plan.md`:

```
# Content Plan: [Topic]

## Overview
- Audience: [...]
- Tone: [...]
- Goals: [...]
- Tổng số bài: [N]

## Briefs
[Briefs theo format ở Step 4]

## Thứ tự đăng đề xuất
[Timeline/order]
```

Phase 2 output: Mỗi bài theo structure template của type tương ứng trong references/.

## References

- [references/writing-system.md](references/writing-system.md) — Writing system dùng chung (archetypes, anti-AI writing, self-critique, power techniques)
- [references/blog-types.md](references/blog-types.md) — 6 blog type guidelines
- [references/facebook-types.md](references/facebook-types.md) — 4 Facebook post types
- [references/content-frameworks.md](references/content-frameworks.md) — Writing frameworks (PAS, Inverted Pyramid, etc.)
