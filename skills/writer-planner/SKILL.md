---
name: writer-planner
description: Xử lý input (PDF, DOCX, EPUB, URL, YouTube, text) và tạo kế hoạch chia bài viết. Convert tài liệu sang markdown, phân tích cấu trúc, chia sections thành articles, tạo article plan với line ranges và series context. Output tại CWD/writer-planner/ sẵn sàng cho writer-executor viết bài.
disable-model-invocation: true
version: 2.0.0
license: MIT
---

# Writer Planner

Xử lý input và tạo kế hoạch chia bài. Không chọn style, không viết bài.

**Nhiệm vụ duy nhất**: Input → Convert → Analyze → Plan

## Quick Reference

| Reference                                                     | Purpose                            | Load at Step      |
| ------------------------------------------------------------- | ---------------------------------- | ----------------- |
| [directory-structure.md](references/directory-structure.md)   | Output folder layout               | Step 1            |
| [decision-trees.md](references/decision-trees.md)             | Workflow decision guides           | On confusion only |
| [detail-levels.md](references/detail-levels.md)               | Output detail level options        | Step 2            |
| [context-optimization.md](references/context-optimization.md) | Context optimization anti-patterns | Step 3.1          |
| [large-doc-processing.md](references/large-doc-processing.md) | Handling documents >50K words      | Step 3 (if >20K)  |


**Tier Workflow Files** (loaded at Step 2.2, chỉ đọc phần Step 3):

| Tier        | File                                                  | When                           |
| ----------- | ----------------------------------------------------- | ------------------------------ |
| Direct Path | [tier-direct-path.md](references/tier-direct-path.md) | <20K OR (<50K AND ≤3 articles) |
| Tier 1      | [tier-1-workflow.md](references/tier-1-workflow.md)   | 20K-50K (fails Direct Path)    |
| Tier 2      | [tier-2-workflow.md](references/tier-2-workflow.md)   | 50K-100K                       |
| Tier 3      | [tier-3-workflow.md](references/tier-3-workflow.md)   | >=100K                         |


## Workflow

```
Input → Convert → Tier + Detail Level → Analyze → Plan
  0        1              2                3         3
```

## Step 0: Resolve Skill Paths (BẮT BUỘC)

Tìm `wa-env` → chạy → dùng paths tuyệt đối.

```bash
Glob("**/writer-planner/scripts/wa-env")
bash {path_to_wa-env}
# → SCRIPTS_DIR, SKILL_DIR, REFERENCES_DIR
```

> **FAIL CONDITION**: Không tìm thấy `wa-env` → STOP.

## Step 1: Input Handling

> **GUARD**: `SCRIPTS_DIR` đã resolve từ Step 0. Nếu chưa → **STOP, quay lại Step 0**.

Detect input type và convert sang markdown.

| Input Type               | Detection                   | Action                    |
| ------------------------ | --------------------------- | ------------------------- |
| File (PDF/DOCX/EPUB/etc) | Path + extension            | `wa-convert {path}`       |
| URL (web page)           | `http://` or `https://`     | `wa-convert {url}`        |
| YouTube URL              | `youtube.com` or `youtu.be` | `wa-convert {url}`        |
| Plain text / .txt / .md  | No complex extension        | Rewrite → `wa-paste-text` |


### File/URL Conversion

```bash
{SCRIPTS_DIR}/wa-convert [/path/to/file.pdf or url]
```

**Output**: `writer-planner/{slug}-{timestamp}/input-handling/content.md` + `structure.json`

### Plain Text Processing

1. Read content (if file)
2. Rewrite to structured markdown (add headings, preserve content)
3. Propose title
4. Execute:

```bash
echo "{rewritten_content}" | {SCRIPTS_DIR}/wa-paste-text - --title "{title}"
```

### Error Handling

| Error              | Action                         |
| ------------------ | ------------------------------ |
| File not found     | Ask for correct path           |
| Unsupported format | Try Docling, confirm with user |
| URL fetch failed   | Report and stop                |
| Empty content      | Warn, confirm before continue  |
| Encrypted PDF      | Ask for decrypted version      |


## Step 2: Determine Tier & Detail Level

### 2.1 Select Detail Level

Hỏi user mức độ chi tiết cho output:

| Level         | Ratio  | Description                         |
| ------------- | ------ | ----------------------------------- |
| Concise       | 15-25% | Tóm lược, giữ ý chính               |
| **Standard**  | 30-40% | Cân bằng (Recommended)              |
| Comprehensive | 50-65% | Chi tiết, giữ nhiều ví dụ           |
| Faithful      | 75-90% | Gần như đầy đủ nội dung gốc       |


**Default**: Standard. Chi tiết → [detail-levels.md](references/detail-levels.md).

### 2.2 Determine Tier

Đọc `structure.json` → xác định tier:

| Tier            | Word Count                     | Strategy                      |
| --------------- | ------------------------------ | ----------------------------- |
| **Direct Path** | <20K OR (<50K AND ≤3 articles) | Main agent writes all         |
| **Tier 1**      | 20K-50K (fails Direct Path)    | Subagents, inline glossary    |
| **Tier 2**      | 50K-100K                       | Context extractors + glossary |
| **Tier 3**      | >=100K                         | Fast Path, minimal overhead   |


**Priority**: Direct Path checked FIRST, override tier boundaries.

Load tier workflow file tương ứng (chỉ phần Step 3):

```python
tier = determine_tier(structure_json)
Read(f"{SKILL_DIR}/references/tier-{tier}-workflow.md")  # Step 3 only
```

## Step 3: Analyze & Plan

Thực hiện theo tier workflow file đã load. Mỗi tier file chứa:

### 3.0 Processing Path Confirmation

Verify tier từ `structure.json`.

### 3.1 Structure Scan

> **📖 READ FIRST**: [context-optimization.md](references/context-optimization.md)

**CHỈ đọc `structure.json**` cho outline, stats, tier recommendation. **KHÔNG đọc `content.md**` ở bước này.

### 3.2 Content Inventory

Dùng `structure.json` outline trực tiếp. Section IDs, line ranges, word counts, critical markers đã có sẵn.

### 3.3 Article Plan (`analysis/_plan.md`)

```python
if user_specified_article_count:
    target_articles = user_specified_count
else:
    target_articles = calculate_optimal_articles(total_words, detail_ratio)
```

Group sections into articles (default 3-7):

```markdown
| #   | Slug  | Title         | Sections      | Est. Words | Reading Time |
| --- | ----- | ------------- | ------------- | ---------- | ------------ |
| 1   | intro | Introduction  | S01, S02      | 2000       | ~13 min      |
| 2   | core  | Core Concepts | S03, S04, S05 | 2500       | ~13-15 min   |
```

**Rules**: All sections mapped. Target 2000-3000 words/bài (tham khảo).

**Content-Type Detection**: Xác định `content_type` cho mỗi article (`tutorial`, `conceptual`, `narrative`, `analysis`, `mixed`).

**Series Context** (tạo cùng lúc với plan):

```markdown
## Series Context

Core message: "{1-2 câu thông điệp cốt lõi}"

| # | Title | Role | Opening | Reader Enters | Reader Exits | Transformation Moment | Misconception | Bridge to Next |
```

**Opening Diversity Rule**: KHÔNG 2 bài liên tiếp dùng cùng opening technique. Dùng ít nhất ceil(N/2) techniques khác nhau.

### 3.3.1 Article Splitting (Auto)

Khi estimated output > 3000 words:

- `MAX_OUTPUT_WORDS = 3000`, `TARGET_PART_WORDS = 2000`
- Atomic unit = H2 block. NEVER split within paragraph/H3/critical section.

### 3.4 Glossary Extraction

Đọc `content.md` first 300-500 lines, extract key terms:

- Tier 1/Direct Path: ~200 words inline glossary
- Tier 2: seed glossary → context extractors produce `_glossary.md`
- Tier 3: ~300 words inline glossary

### 3.5 Context Files (Tier 2 Only)

Spawn context extractor subagents. Output: `analysis/XX-{slug}-context.md`.

### 3.6 Quality Gate

- [ ] All sections have IDs (from structure.json)
- [ ] Critical sections marked
- [ ] Article plan covers 100% sections
- [ ] Context files created (Tier 2)

## Output

Sau khi hoàn thành, thư mục `writer-planner/{book}/` chứa:

```
writer-planner/{book}/
├── input-handling/
│   ├── content.md          # Markdown source
│   └── structure.json      # Document structure
└── analysis/
    ├── _plan.md            # Article plan (BẮT BUỘC)
    ├── _glossary.md        # Shared terminology (Tier 2 only)
    └── XX-{slug}-context.md # Context files (Tier 2 only)
```

### Completion Message

```
Kế hoạch bài viết sẵn sàng tại: {book_dir}/
- {N} articles planned
- Tier: {tier}
- Detail: {detail_level}
- Total words: {total_words}
```
