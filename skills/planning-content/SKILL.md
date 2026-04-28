---
name: planning-content
description: "Phân tích nội dung và lên outline ý chính cho từng bài. Hỗ trợ mọi loại input: topic thuần, notes, URL, file (PDF/DOCX/EPUB/XLSX/PPTX), YouTube. Convert tài liệu sang markdown, research bổ sung khi cần, tạo content map và outline ý chính cho từng bài. CHỈ tập trung phân tích + outline, KHÔNG hướng dẫn cách viết, tone, style, hay cấu trúc trình bày."
disable-model-invocation: true
---

# Planning Content

Workflow: Detect & Convert → Interview → Research → Content Map → Outlines → Save → Adjust (nếu cần)

**Nguyên tắc cốt lõi:**

- Skill CHỈ làm 2 việc: (1) phân tích nội dung input, (2) xác định các ý chính cần cover trong từng bài.
- KHÔNG can thiệp cách viết, tone, style, cách sắp xếp section, mở bài, kết bài. Đó là việc của skill viết bài.
- Outline = bản đồ ý tưởng, KHÔNG phải bản nháp.

## Quick Reference

| Reference | Mục đích | Load khi |
|---|---|---|
| [tier-processing.md](references/tier-processing.md) | Tier detection, context rule, batch, subagent, quality gate, fallback | Phase 4 (nếu input đã convert) |

## Phase 1: Detect & Convert Input

### 1.0 Resolve Skill Paths (khi cần convert)

Chỉ cần khi input là file hoặc URL cần convert.

1. Dùng tool **Glob** tìm `wa-env`:
   ```
   Glob("**/planning-content/scripts/wa-env")
   ```
2. Chạy bằng **Bash**:
   ```bash
   bash {path_to_wa-env}
   ```
3. Parse output lấy: `SCRIPTS_DIR`, `SKILL_DIR`, `PROJECT_ROOT`, `OUTPUT_DIR`, `REFERENCES_DIR`

> **FAIL CONDITION**: Không tìm thấy `wa-env` → dùng WebFetch cho URL, Read cho file text. Conversion scripts không bắt buộc.

### 1.1 Detect Input Type

| Input Type | Detection | Action |
|---|---|---|
| **Topic thuần** | Chỉ có chủ đề, không file/URL | → Phase 2 trực tiếp |
| **Notes/ý tưởng rời** | Bullet points, gạch đầu dòng | → Phase 2 trực tiếp |
| **File (PDF/DOCX/EPUB)** | Path + extension | `wa-convert {path}` → content.md + structure.json |
| **File (XLSX/PPTX)** | Path + extension | `wa-convert {path}` (qua Docling). Kiểm tra chất lượng conversion, xem [tier-processing.md](references/tier-processing.md) mục "Lưu ý chất lượng conversion" |
| **File (HTML/AsciiDoc)** | Path + extension | `wa-convert {path}` (qua Docling) |
| **Image (PNG/JPEG/TIFF/BMP/WEBP)** | Path + extension | Dùng Read tool (multimodal) để đọc ảnh trực tiếp. Nếu cần text extraction: `wa-convert {path}` (OCR qua Docling) |
| **URL (web page)** | `http://` hoặc `https://` (không YouTube) | Ưu tiên `WebFetch` (nhanh, xử lý JavaScript). Dùng `wa-convert {url}` khi WebFetch trả về nội dung rác hoặc user yêu cầu convert offline |
| **YouTube URL** | `youtube.com` hoặc `youtu.be` | `wa-convert {url}` |
| **Plain text / .txt / .md** | Không extension phức tạp | Rewrite → `wa-paste-text` hoặc Read trực tiếp |

### 1.2 File/URL Conversion

```bash
# Auto-generate output dir
{SCRIPTS_DIR}/wa-convert /path/to/file.pdf

# Custom output dir (khi user chỉ định)
{SCRIPTS_DIR}/wa-convert /path/to/file.pdf my-project/input-handling
```

**Output**: `content.md` + `structure.json` trong output dir.
- Mặc định: `planning-content/{slug}-{timestamp}/input-handling/`
- Custom: thư mục user chỉ định (argument thứ 2)

> **Lưu ý venv**: Scripts dùng venv riêng tại `{SCRIPTS_DIR}/.venv/` (tách biệt với venv hệ thống). Nếu chưa setup, chạy `bash {SCRIPTS_DIR}/setup.sh` trước.

### 1.3 Plain Text Processing

1. Read content (nếu là file)
2. Rewrite thành structured markdown (thêm headings, giữ nguyên nội dung)
3. Đề xuất title
4. Ghi rewritten content vào file tạm, rồi chạy:

```bash
# Ghi content vào file tạm (tránh lỗi shell escape với echo)
Write("/tmp/planning-content-input.md", rewritten_content)

{SCRIPTS_DIR}/wa-paste-text /tmp/planning-content-input.md --title "{title}"
```

### 1.4 Multi-Input

Khi user đưa nhiều file/URL cùng lúc:

- Xử lý **tuần tự**, mỗi input tạo thư mục riêng.
- Sau khi convert xong tất cả, hỏi user: gộp thành 1 content map chung hay tách riêng từng bộ outline?
- Nếu gộp: tạo 1 thư mục chung, content map reference đến nhiều source.

### 1.5 Fallback (không có scripts)

Nếu scripts không available (chưa setup, lỗi path):

- **URL**: dùng `WebFetch` trực tiếp
- **File text (.md/.txt)**: dùng `Read` trực tiếp
- **PDF/DOCX/EPUB/XLSX/PPTX**: báo user chạy `setup.sh` trước: `bash {SCRIPTS_DIR}/setup.sh`

### Error Handling

| Lỗi | Xử lý |
|---|---|
| File not found | Hỏi lại path |
| Unsupported format | Báo user, đề xuất convert thủ công |
| URL fetch failed | Báo lỗi, dừng |
| Empty content | Cảnh báo, xác nhận trước khi tiếp |
| Encrypted PDF | Hỏi bản giải mã |
| YouTube không có transcript | Script tạo warning page (không có nội dung thật). Báo user, hỏi có muốn dùng WebSearch research topic thay thế không. Nếu không, dừng |

## Phase 2: Interview

Hỏi tất cả câu hỏi trong 1 lượt:

1. **Audience**: Người đọc chính là ai? (founder, marketer, developer, sinh viên...)
2. **Goal**: Mục tiêu chính? (educate / engage / convert / thought leadership)
3. **Scope**: Bao phủ toàn bộ nội dung hay chọn lọc phần cụ thể?
4. *(Optional)* **Số bài**: User muốn bao nhiêu bài? (mặc định: tự tính từ word count)
5. *(Optional)* **Ngôn ngữ output**: Tiếng Việt (mặc định) hay ngôn ngữ khác?
6. *(Optional)* **Constraints**: Yêu cầu đặc biệt (deadline, topic cần tránh, kênh đăng)

*Fast-track: Nếu input đã đủ context hoặc user yêu cầu "làm luôn", giả định sensible defaults và sang Phase 3.*

### Edge Cases

- **Input quá ngắn (1-2 câu):** Hỏi user bổ sung context hoặc dùng web research mở rộng trước khi tạo outline.
- **Thiếu data cho 1 ý:** Note rõ "data gap" trong outline (field `Open questions`) để writer biết cần tìm thêm gì, hoặc đề xuất loại bỏ ý nếu không có cách tìm.
- **Topic quá rộng:** Narrow down qua Interview, yêu cầu user chọn góc cụ thể trước khi plan.

## Phase 3: Research (Conditional)

### Khi nào chạy

- **Luôn chạy**: input là topic thuần, notes/ý tưởng rời
- **Chạy nếu cần**: tài liệu convert nhưng nội dung mỏng (ít data, ít ví dụ), YouTube transcript ngắn/thiếu context
- **Skip**: tài liệu đã convert có nội dung đầy đủ (sách, report dài, tài liệu chuyên sâu)

Tiêu chí "đầy đủ": tài liệu tự cung cấp đủ data, ví dụ, evidence cho các ý chính. Nếu outline có nhiều `Open questions`, cân nhắc chạy research.

### Quy trình

- WebSearch 3-5 queries liên quan topic + audience + trends.
- Thu thập: data, số liệu, góc nhìn mới, content gaps, ví dụ thực tế, case study.
- **Bắt buộc cite nguồn** cho mọi data point.

> **Lưu ý**: Nếu input đã qua Phase 1 convert (URL hay file), nội dung gốc đã nằm trong content.md. Research ở Phase 3 là tìm **bổ sung** (trend mới, góc nhìn khác, data gap), KHÔNG phải fetch lại nội dung đã có.

## Phase 4: Map Content & Generate Outlines

### 4.0 Tier-Aware Processing (chỉ khi input đã convert)

Nếu input đã convert (có `structure.json`):

1. **Đọc structure.json ONLY** (không đọc content.md). Chỉ đọc content.md theo section khi cần chi tiết cho outline cụ thể.
2. Xác định tier và Direct Path. Chi tiết workflow, fallback, subagent: xem [tier-processing.md](references/tier-processing.md).
3. Nếu structure.json không tạo được (script báo `structure_error`): xem mục "Fallback" trong [tier-processing.md](references/tier-processing.md).

### 4.1 Content Map

**Cho topic thuần/notes:**
- Liệt kê toàn bộ concept/ý lớn từ input + research.
- Group các ý liên quan thành cluster theo chủ đề.
- Đánh dấu ưu tiên (must-have / nice-to-have).

**Cho tài liệu đã convert:**
- Dùng `outline` từ `structure.json`: section titles, word counts, critical markers.
- Group sections thành clusters theo heading hierarchy.
- Đánh dấu critical sections (đã có từ structure.json).

### 4.2 Generate Outlines

Đề xuất số lượng bài bao phủ toàn bộ nội dung input:

- **Topic thuần** → 3-10 bài (tùy scope).
- **Notes/ý tưởng rời** → theo số ý tưởng có sẵn.
- **URL/article** → 5-15 bài (tùy độ dài + density).
- **Tài liệu đã convert** → tính từ word count:

```python
if user_specified_article_count:
    target = user_specified_count
else:
    target = max(3, round(word_count / 2500))
```

> `structure.json.stats.estimated_articles` là ước lượng sơ bộ (dựa trên heading count), dùng làm tham khảo. Formula trên chính xác hơn.

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
{CWD}/planning-content/{topic-slug}-{YYMMDD-HHMM}/
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
{CWD}/planning-content/{topic-slug}-{YYMMDD-HHMM}/
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

## Phase 6: Adjust Outlines (nếu user yêu cầu)

Khi user muốn điều chỉnh sau Phase 5:

| Yêu cầu | Xử lý |
|---|---|
| **Sửa 1 outline** | Đọc file outline cụ thể, chỉnh theo feedback, ghi đè |
| **Merge 2+ outlines** | Gộp key points, chọn thesis mới, xoá file thừa, cập nhật index.md |
| **Tách 1 outline thành nhiều** | Chia key points thành groups, tạo file mới cho mỗi group, cập nhật index.md |
| **Thêm outline mới** | Tạo file outline mới theo format Phase 4.2, thêm vào index.md |
| **Xoá outline** | Xoá file, cập nhật index.md, chạy coverage check nếu input đã convert |
| **Đổi thứ tự** | Rename file numbers (outline-01, 02...), cập nhật index.md |

Sau mỗi lần điều chỉnh, chạy coverage check (nếu input đã convert) để đảm bảo không bỏ sót nội dung.

## Constraints

- Output tiếng Việt (trừ khi user yêu cầu khác). Khi source khác ngôn ngữ (ví dụ sách tiếng Anh): outline viết tiếng Việt, giữ nguyên thuật ngữ chuyên ngành gốc trong ngoặc.
- Mọi data point phải cite nguồn (khi có research).
- KHÔNG đề xuất tone, style, cách trình bày, cấu trúc section, framework viết, độ dài bài.
- KHÔNG viết draft câu mở bài, câu kết, hay bất kỳ phần nào của bài hoàn chỉnh.
- Outline phải đủ rõ ý để writer không cần tự suy luận thêm ý chính.
- Default output dir: `{CWD}/planning-content/{topic-slug}-{YYMMDD-HHMM}/` nếu user không chỉ định.

## Output Format

**1. `index.md`:**

```
# Content Plan: [Topic]

## Overview
- Audience: [...]
- Goal: [...]
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
