---
name: planning-content
description: "Phân tích nội dung và lập outline ý chính. Input: topic, notes, URL, PDF/DOCX/EPUB/XLSX/PPTX, YouTube. Không viết bài."
---

# Planning Content

Workflow: Detect & Convert → Interview → Research → Content Map → Outlines → Save → Adjust (nếu cần)

**Nguyên tắc cốt lõi:**

- Skill CHỈ làm 2 việc: (1) phân tích nội dung input, (2) xác định các ý chính cần cover trong từng bài.
- KHÔNG can thiệp cách viết, tone, style, cách sắp xếp section, mở bài, kết bài, framework viết, độ dài bài. Đó là việc của skill viết bài.
- KHÔNG viết draft câu mở bài, câu kết, hay bất kỳ phần nào của bài hoàn chỉnh.
- Outline = bản đồ ý tưởng, KHÔNG phải bản nháp.
- Mọi data point phải cite nguồn (khi có research).
- Output tiếng Việt (trừ khi user yêu cầu khác). Thuật ngữ chuyên ngành giữ nguyên gốc trong ngoặc.

## Quick Reference

| Reference | Mục đích | Load khi |
|---|---|---|
| [tier-processing.md](references/tier-processing.md) | Tier detection, batch, subagent, quality gate | Phase 4 (nếu input đã convert) |

## Phase 1: Detect & Convert Input

### 1.0 Resolve Skill Paths

Chỉ cần khi input là file hoặc URL cần convert:

1. Dùng Glob tìm `**/planning-content/scripts/wa-env`
2. Chạy: `bash {path_to_wa-env}`
3. Parse output lấy: `SCRIPTS_DIR`, `SKILL_DIR`, `PROJECT_ROOT`, `OUTPUT_DIR`, `REFERENCES_DIR`

Nếu không tìm thấy `wa-env`: dùng WebFetch cho URL, Read cho file text. Scripts không bắt buộc.

### 1.1 Detect Input Type

| Input Type | Detection | Action |
|---|---|---|
| **Topic thuần** | Chỉ có chủ đề, không file/URL | → Phase 2 trực tiếp |
| **Notes/ý tưởng rời** | Bullet points, gạch đầu dòng | → Phase 2 trực tiếp |
| **File (PDF/DOCX/EPUB)** | Path + extension | `wa-convert {path}` → content.md + structure.json |
| **File (XLSX/PPTX)** | Path + extension | `wa-convert {path}` (qua Docling). Kiểm tra chất lượng, xem [tier-processing.md](references/tier-processing.md) mục "Lưu ý chất lượng conversion" |
| **File (HTML/AsciiDoc)** | Path + extension | `wa-convert {path}` (qua Docling) |
| **Image (PNG/JPEG/TIFF/BMP/WEBP)** | Path + extension | Dùng Read tool (multimodal) để đọc ảnh trực tiếp. Nếu cần text extraction: `wa-convert {path}` (OCR qua Docling) |
| **URL (web page)** | `http://` hoặc `https://` (không YouTube) | Ưu tiên `WebFetch`. Dùng `wa-convert {url}` khi WebFetch trả nội dung rác |
| **YouTube URL** | `youtube.com` hoặc `youtu.be` | `wa-convert {url}` |
| **Plain text / .txt / .md** | Không extension phức tạp | Read trực tiếp, hoặc `wa-paste-text` nếu cần lưu vào output dir |

### 1.2 File/URL Conversion

```bash
# Auto-generate output dir
{SCRIPTS_DIR}/wa-convert /path/to/file.pdf

# Custom output dir
{SCRIPTS_DIR}/wa-convert /path/to/file.pdf my-project/input-handling
```

**Output**: `content.md` + `structure.json` trong output dir.

> **Lưu ý venv**: Scripts dùng venv riêng tại `{SCRIPTS_DIR}/.venv/`. Nếu chưa setup, chạy `bash {SCRIPTS_DIR}/setup.sh` trước.

### 1.3 Multi-Input

Khi user đưa nhiều file/URL cùng lúc:

- Xử lý tuần tự, mỗi input tạo thư mục riêng.
- Sau khi convert xong, hỏi user: gộp thành 1 content map chung hay tách riêng từng bộ outline?

### 1.4 Fallback (không có scripts)

- **URL**: dùng `WebFetch` trực tiếp
- **File text (.md/.txt)**: dùng `Read` trực tiếp
- **PDF/DOCX/EPUB/XLSX/PPTX**: báo user chạy `bash {SCRIPTS_DIR}/setup.sh`

### Error Handling

| Lỗi | Xử lý |
|---|---|
| File not found | Hỏi lại path |
| Unsupported format | Báo user, đề xuất convert thủ công |
| URL fetch failed | Báo lỗi, dừng |
| Empty content | Cảnh báo, xác nhận trước khi tiếp |
| Encrypted PDF | Hỏi bản giải mã |
| YouTube không có transcript | Báo user, hỏi có muốn dùng WebSearch research topic thay thế không |

## Phase 2: Interview

Hỏi tất cả câu hỏi trong 1 lượt:

1. **Audience**: Người đọc chính là ai?
2. **Goal**: Mục tiêu chính? (educate / engage / convert / thought leadership)
3. **Scope**: Góc cụ thể nào của chủ đề? (mặc định: bao phủ toàn bộ nội dung input)
4. *(Optional)* **Số bài**: User muốn bao nhiêu bài? (mặc định: tự tính)
5. *(Optional)* **Constraints**: Yêu cầu đặc biệt (deadline, topic cần tránh, kênh đăng, ngôn ngữ output)

*Fast-track: Nếu input đã đủ context hoặc user yêu cầu "làm luôn", giả định sensible defaults và sang Phase 3.*

### Edge Cases

- **Input quá ngắn (1-2 câu):** Hỏi user bổ sung context hoặc dùng web research mở rộng.
- **Thiếu data cho 1 ý:** Note "Open questions" trong outline để writer biết cần tìm thêm.
- **Topic quá rộng:** Yêu cầu user chọn góc cụ thể trước khi plan.

## Phase 3: Research (Conditional)

### Khi nào chạy

- **Luôn chạy**: input là topic thuần, notes/ý tưởng rời
- **Chạy nếu cần**: tài liệu convert nhưng nội dung mỏng, YouTube transcript ngắn/thiếu context
- **Skip**: tài liệu đã convert có nội dung đầy đủ (sách, report dài, tài liệu chuyên sâu)

Tiêu chí "đầy đủ": tài liệu tự cung cấp đủ data, ví dụ, evidence cho các ý chính.

### Quy trình

- WebSearch 3-5 queries liên quan topic + audience + trends.
- Thu thập: data, số liệu, góc nhìn mới, ví dụ thực tế, case study.
- **Bắt buộc cite nguồn** cho mọi data point.

> Research ở Phase 3 là tìm **bổ sung** (trend mới, góc nhìn khác, data gap), KHÔNG phải fetch lại nội dung đã có từ Phase 1.

## Phase 4: Map Content & Generate Outlines

### 4.0 Tier-Aware Processing (chỉ khi input đã convert)

Nếu input đã convert (có `structure.json`):

1. Đọc `structure.json` ONLY (không đọc content.md toàn bộ). Chỉ đọc content.md theo section cụ thể khi cần chi tiết.
2. Xác định tier. Chi tiết workflow, batch, subagent: xem [tier-processing.md](references/tier-processing.md).
3. Nếu structure.json lỗi: xem mục "Fallback" trong [tier-processing.md](references/tier-processing.md).

### 4.1 Content Map

**Cho topic thuần/notes:**
- Liệt kê toàn bộ concept/ý lớn từ input + research.
- Group các ý liên quan thành cluster theo chủ đề.
- Đánh dấu ưu tiên (must-have / nice-to-have).

**Cho tài liệu đã convert:**
- Dùng `outline` từ `structure.json`: section titles, word counts, critical markers.
- Group sections thành clusters theo heading hierarchy.

### 4.2 Generate Outlines

**Tính số bài:**

```python
if user_specified_article_count:
    target = user_specified_count
else:
    target = max(3, round(word_count / 2500))
```

Ước lượng theo loại input khi không có word count:
- Topic thuần → 3-10 bài (tùy scope)
- Notes/ý tưởng rời → theo số ý tưởng có sẵn
- URL/article → 5-15 bài (tùy độ dài + density)
- Sách/tài liệu dài → chia thành batches (~10 bài/batch)

**Nguyên tắc lên outline:**

- **1 bài = 1 chủ đề duy nhất.** Mỗi outline tập trung đúng 1 ý chính.
- Outline = liệt kê **ý chính** bài cần cover, KHÔNG quy định cấu trúc trình bày.
- Mỗi ý chính phải có data/ví dụ hỗ trợ. Ý không có data → đánh dấu "cần tìm thêm" hoặc loại.
- Outline phải đủ rõ để writer hiểu **bài nói về cái gì** mà không cần đoán.
- **Cho tài liệu đã convert**: đọc content.md theo section cụ thể (`offset`/`limit` từ structure.json), KHÔNG đọc toàn bộ.

**Format mỗi outline:**

```
### Bài [N]: [Tiêu đề đề xuất]

- **Audience:** [Người đọc cụ thể của bài này]
- **Goal:** [Sau khi đọc, reader hiểu hoặc làm được gì]
- **Angle:** [Góc tiếp cận]
- **Thesis (ý cốt lõi):** [1 câu]
- **Key points cần cover:**
  - [Ý chính 1] | data/ví dụ: [...] | nguồn: [...]
  - [Ý chính 2] | data/ví dụ: [...] | nguồn: [...]
  - [Ý chính 3] | data/ví dụ: [...] | nguồn: [...]
- **Takeaway / insight chính:** [Reader rút ra điều gì]
- **Open questions:** [Data còn thiếu. Nếu không có, ghi "Không"]
```

## Phase 5: Save Output

**Cấu trúc thư mục:**

```
{CWD}/planning-content/{topic-slug}-{YYMMDD-HHMM}/
├── input-handling/              # Chỉ khi có convert
│   ├── content.md
│   └── structure.json
├── index.md                     # Overview + danh sách link
├── outline-[NN]-[slug].md      # Mỗi bài 1 file
├── research.md                  # Nếu Phase 3 chạy
└── content-map.md               # Nếu input dài hoặc nhiều concepts
```

**index.md format:**

```markdown
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

## Coverage Checklist (nếu batch)
- [x] Batch 1 — 10/10
- [ ] Batch 2 — 0/10
```

**Xử lý input dài (batch):**

- Tạo content map trước, lưu vào `content-map.md`.
- Batch ~10 bài/batch, làm batch đầu trước.
- **Coverage check (BẮT BUỘC) sau mỗi batch:** đối chiếu content map, liệt kê concept ĐÃ cover vs CHƯA cover. Lặp đến 100%.
- Cập nhật `index.md` sau mỗi batch.
- Hỏi user confirm trước batch tiếp.

Cuối cùng hỏi: "Đã hoàn thành outline cho [N] bài. Bạn muốn điều chỉnh outline nào không?"

## Phase 6: Adjust Outlines (nếu user yêu cầu)

| Yêu cầu | Xử lý |
|---|---|
| **Sửa 1 outline** | Đọc file, chỉnh theo feedback, ghi đè |
| **Merge 2+ outlines** | Gộp key points, chọn thesis mới, xoá file thừa, cập nhật index.md |
| **Tách 1 outline** | Chia key points thành groups, tạo file mới, cập nhật index.md |
| **Thêm outline mới** | Tạo file theo format Phase 4.2, thêm vào index.md |
| **Xoá outline** | Xoá file, cập nhật index.md, chạy coverage check nếu input đã convert |
| **Đổi thứ tự** | Rename file numbers, cập nhật index.md |

Sau mỗi điều chỉnh, chạy coverage check (nếu input đã convert) để đảm bảo không bỏ sót.
