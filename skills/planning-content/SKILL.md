---
name: planning-content
description: "Phân tích nội dung và lên kế hoạch outline chi tiết cho bài viết. Hỗ trợ mọi loại input: topic thuần, notes, URL, file (PDF/DOCX/EPUB), YouTube. Convert tài liệu sang markdown, research bổ sung khi cần, tạo content map và outline ý chính cho từng bài. CHỈ tập trung phân tích + outline, KHÔNG hướng dẫn cách viết, tone, style, hay cấu trúc trình bày."
disable-model-invocation: true
---

# Planning Content

Workflow: Detect & Convert Input → Interview → Research → Map Content → Generate Outlines → Save

**Nguyên tắc cốt lõi:**

- Skill CHỈ làm 2 việc: (1) phân tích nội dung input, (2) xác định các ý chính cần cover trong từng bài.
- KHÔNG can thiệp cách viết, tone, style, cách sắp xếp section, mở bài, kết bài. Đó là việc của skill viết bài.
- Outline = bản đồ ý tưởng, KHÔNG phải bản nháp.

## Quick Reference

| Reference | Mục đích | Load khi |
|---|---|---|
| [detail-levels.md](references/detail-levels.md) | Các mức chi tiết output | Phase 2 (Interview) |
| [context-optimization.md](references/context-optimization.md) | Anti-patterns khi đọc content.md | Phase 4 (nếu có structure.json) |
| [tier-processing.md](references/tier-processing.md) | Xử lý tài liệu lớn theo tier | Phase 4 (nếu input đã convert) |

## Phase 1: Detect & Convert Input

### 1.0 Resolve Skill Paths (khi cần convert)

Chỉ cần khi input là file hoặc URL cần convert. Tìm `wa-env` → chạy → dùng paths tuyệt đối.

```bash
Glob("**/planning-content/scripts/wa-env")
bash {path_to_wa-env}
# → SCRIPTS_DIR, SKILL_DIR, PROJECT_ROOT, OUTPUT_DIR, REFERENCES_DIR
```

> **FAIL CONDITION**: Không tìm thấy `wa-env` → dùng WebFetch cho URL, Read cho file text. Conversion scripts không bắt buộc.

### 1.1 Detect Input Type

| Input Type | Detection | Action |
|---|---|---|
| **Topic thuần** | Chỉ có chủ đề, không file/URL | → Phase 2 trực tiếp |
| **Notes/ý tưởng rời** | Bullet points, gạch đầu dòng | → Phase 2 trực tiếp |
| **File (PDF/DOCX/EPUB)** | Path + extension | `wa-convert {path}` → content.md + structure.json |
| **URL (web page)** | `http://` hoặc `https://` (không YouTube) | `wa-convert {url}` hoặc WebFetch |
| **YouTube URL** | `youtube.com` hoặc `youtu.be` | `wa-convert {url}` |
| **Plain text / .txt / .md** | Không extension phức tạp | Rewrite → `wa-paste-text` hoặc Read trực tiếp |

### 1.2 File/URL Conversion

```bash
{SCRIPTS_DIR}/wa-convert [/path/to/file.pdf or url]
```

**Output**: `planning-content/{slug}-{timestamp}/input-handling/content.md` + `structure.json`

### 1.3 Plain Text Processing

1. Read content (nếu là file)
2. Rewrite thành structured markdown (thêm headings, giữ nguyên nội dung)
3. Đề xuất title
4. Chạy:

```bash
echo "{rewritten_content}" | {SCRIPTS_DIR}/wa-paste-text - --title "{title}"
```

### 1.4 Fallback (không có scripts)

Nếu scripts không available (chưa setup, lỗi path):

- **URL**: dùng `WebFetch` trực tiếp
- **File text (.md/.txt)**: dùng `Read` trực tiếp
- **PDF/DOCX/EPUB**: báo user chạy `setup.sh` trước: `bash {SCRIPTS_DIR}/setup.sh`

### Error Handling

| Lỗi | Xử lý |
|---|---|
| File not found | Hỏi lại path |
| Unsupported format | Báo user, đề xuất convert thủ công |
| URL fetch failed | Báo lỗi, dừng |
| Empty content | Cảnh báo, xác nhận trước khi tiếp |
| Encrypted PDF | Hỏi bản giải mã |

## Phase 2: Interview

Hỏi tất cả câu hỏi trong 1 lượt:

1. **Audience**: Người đọc chính là ai? (founder, marketer, developer, sinh viên...)
2. **Goal**: Mục tiêu chính? (educate / engage / convert / thought leadership)
3. **Detail Level** *(chỉ khi input đã convert)*: Mức chi tiết output?
   - Concise (15-25%): tóm lược, giữ ý chính
   - **Standard (30-40%)**: cân bằng *(Default)*
   - Comprehensive (50-65%): chi tiết, giữ nhiều ví dụ
   - Faithful (75-90%): gần như đầy đủ nội dung gốc
4. *(Optional)* **Constraints**: Yêu cầu đặc biệt (deadline, topic cần tránh, kênh đăng)

Chi tiết Detail Level: xem [detail-levels.md](references/detail-levels.md).

*Fast-track: Nếu input đã đủ context hoặc user yêu cầu "làm luôn", giả định sensible defaults và sang Phase 3.*

### Edge Cases

- **Input quá ngắn (1-2 câu):** Hỏi user bổ sung context hoặc dùng web research mở rộng trước khi tạo outline.
- **Thiếu data cho 1 ý:** Note rõ "data gap" trong outline (field `Open questions`) để writer biết cần tìm thêm gì, hoặc đề xuất loại bỏ ý nếu không có cách tìm.
- **Topic quá rộng:** Narrow down qua Interview, yêu cầu user chọn góc cụ thể trước khi plan.

## Phase 3: Research (Conditional)

### Khi nào chạy

- **Chạy**: input là topic thuần, notes/ý tưởng rời, hoặc URL bài viết ngắn
- **Skip**: input là tài liệu đã convert (PDF/DOCX/EPUB/YouTube) vì nội dung đã đầy đủ

### Quy trình

- WebSearch 3-5 queries liên quan topic + audience + trends.
- Nếu input là URL → WebFetch phân tích nội dung.
- Nếu input là file → đọc và bóc ý chính.
- Thu thập: data, số liệu, góc nhìn mới, content gaps, ví dụ thực tế, case study.
- **Bắt buộc cite nguồn** cho mọi data point.

## Phase 4: Map Content & Generate Outlines

### 4.0 Tier-Aware Processing (chỉ khi input đã convert)

Nếu input đã convert (có `structure.json`):

1. **Đọc structure.json ONLY** cho outline, stats, tier. KHÔNG đọc content.md ở bước này. Xem [context-optimization.md](references/context-optimization.md).
2. Xác định tier xử lý. Xem [tier-processing.md](references/tier-processing.md).

| Tier | Điều kiện | Strategy |
|---|---|---|
| Standard | < 50K words | Xử lý 1 lượt, tạo tất cả outline cùng lúc |
| Tier 2 | 50K-100K | Content map trước, batch ~10 outline/lượt |
| Tier 3 | >= 100K | Fast path, minimal analysis, batch ~10 outline/lượt |

### 4.1 Content Map

**Cho topic thuần/notes:**
- Liệt kê toàn bộ concept/ý lớn từ input + research.
- Group các ý liên quan thành cluster theo chủ đề.
- Đánh dấu ưu tiên (must-have / nice-to-have).

**Cho tài liệu đã convert:**
- Dùng `outline` từ `structure.json`: section titles, word counts, critical markers.
- Group sections thành clusters theo heading hierarchy.
- Đánh dấu critical sections (đã có từ structure.json).
- KHÔNG đọc content.md cho bước này.

### 4.2 Generate Outlines

Đề xuất số lượng bài bao phủ toàn bộ nội dung input:

- **Topic thuần** → 3-10 bài (tùy scope).
- **Notes/ý tưởng rời** → theo số ý tưởng có sẵn.
- **URL/article** → 5-15 bài (tùy độ dài + density).
- **Tài liệu đã convert** → tính từ word count và detail level:

```python
if user_specified_article_count:
    target = user_specified_count
else:
    detail_ratio = 0.35  # Standard default
    total_output = word_count * detail_ratio
    target = max(3, min(10, round(total_output / 2500)))
```

- **Sách/tài liệu dài** → bao phủ toàn bộ giá trị cốt lõi. Chia thành **batches** (mỗi batch ~10 bài).

**Nguyên tắc lên outline:**

- **1 bài = 1 chủ đề duy nhất.** Mỗi outline tập trung đúng 1 ý chính (concept, bài học, góc nhìn, câu chuyện).
- Outline = liệt kê **ý chính** bài cần cover. KHÔNG quy định cấu trúc trình bày, KHÔNG đề xuất framework viết.
- Mỗi ý chính phải có data/ví dụ hỗ trợ rõ ràng. Ý không có data → đánh dấu "cần tìm thêm" hoặc loại.
- Outline phải đủ rõ để writer hiểu **bài nói về cái gì** mà không cần đoán thêm ý chính. Cách trình bày là việc của writer.
- KHÔNG viết câu mở bài, câu kết, hay bất kỳ phần draft nào của bài hoàn chỉnh.
- **Cho tài liệu đã convert**: khi cần chi tiết cho outline, đọc content.md theo section cụ thể (dùng `line`/`line_end` từ structure.json), KHÔNG đọc toàn bộ file.

**Format mỗi outline:**

```
### Bài [N]: [Tiêu đề đề xuất]

- **Audience:** [Người đọc cụ thể của bài này]
- **Goal:** [Sau khi đọc, reader hiểu hoặc làm được gì]
- **Angle:** [Góc tiếp cận, bài này nhìn vấn đề từ hướng nào]
- **Thesis (ý cốt lõi):** [1 câu, ý duy nhất bài muốn truyền tải]
- **Key points cần cover:**
  - [Ý chính 1] | data/ví dụ: [...] | nguồn: [...]
  - [Ý chính 2] | data/ví dụ: [...] | nguồn: [...]
  - [Ý chính 3] | data/ví dụ: [...] | nguồn: [...]
- **Takeaway / insight chính:** [Reader rút ra điều gì]
- **Open questions:** [Data hoặc câu hỏi còn thiếu, writer cần tìm thêm. Nếu không có, ghi "Không"]
```

## Phase 5: Save Output

Lưu thành nhiều file để dễ quản lý:

**Cho tài liệu đã convert (có input-handling/):**

```
{CWD}/planning-content/{topic-slug}/
├── input-handling/
│   ├── content.md              # Markdown source (từ scripts)
│   └── structure.json          # Document structure (từ scripts)
├── index.md                    # Overview + danh sách link
├── outline-[NN]-[slug].md     # Mỗi bài 1 file
├── research.md                 # Data đã research (nếu Phase 3 chạy)
└── content-map.md              # Content map (nếu input dài)
```

**Cho topic thuần/notes (không convert):**

```
{CWD}/planning-content/{topic-slug}/
├── index.md
├── outline-[NN]-[slug].md
├── research.md
└── content-map.md              # Nếu input dài
```

**Xử lý input dài theo batch:**

- Tạo content map trước, lưu vào `content-map.md`.
- Chia thành batches ~10 bài/batch, làm batch đầu tiên trước.
- **Checklist tiến độ** dạng markdown trong `index.md`:
  ```
  - [x] Batch 1 (Chương 1-3): 10/10 outlines
  - [ ] Batch 2 (Chương 4-6): 0/10
  ```
- **Coverage check (BẮT BUỘC):** Sau mỗi batch, đối chiếu content map. Liệt kê concept ĐÃ cover vs CHƯA cover. Lặp đến khi 100% content map có outline.
- Cập nhật `index.md` sau mỗi batch.
- Hỏi user confirm trước khi làm batch tiếp.

Cuối cùng hỏi: "Đã hoàn thành outline cho [N] bài. Bạn muốn điều chỉnh outline nào trước khi chuyển cho skill viết bài không?"

## Constraints

- Output tiếng Việt (trừ khi user yêu cầu khác).
- Mọi data point phải cite nguồn (khi có research).
- KHÔNG đề xuất tone, style, cách trình bày, cấu trúc section, framework viết, độ dài bài.
- KHÔNG viết draft câu mở bài, câu kết, hay bất kỳ phần nào của bài hoàn chỉnh.
- Outline phải đủ rõ ý để writer không cần tự suy luận thêm ý chính.
- Default output dir: `{CWD}/planning-content/[topic-slug]/` nếu user không chỉ định.

## Output Format

**1. `index.md`:**

```
# Content Plan: [Topic]

## Overview
- Audience: [...]
- Goal: [...]
- Detail Level: [...] (nếu có)
- Tổng số bài: [N]
- Nguồn input: [URL/file/topic]
- Word count gốc: [N] (nếu có structure.json)

## Danh sách Outlines
1. [Bài 1: Tiêu đề](outline-01-slug.md)
2. [Bài 2: Tiêu đề](outline-02-slug.md)
...

## Coverage Checklist (nếu input dài)
- [x] Batch 1 — 10/10
- [ ] Batch 2 — 0/10
```

**2. `outline-[NN]-[slug].md`:** chi tiết từng bài theo format ở Phase 4.2.

**3. `research.md`:** data + sources thu thập được (nếu Phase 3 chạy).

**4. `content-map.md`** (input dài): toàn bộ concept map + cluster + ưu tiên.
