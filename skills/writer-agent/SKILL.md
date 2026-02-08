---
name: writer-agent
description: Transform documents into styled article series. Analyze input (md, txt, pdf, docx, pptx, xlsx, html, epub, images, url), extract core ideas, decompose into logical sections, write articles with user-selectable styles (professional, casual, custom), synthesize into organized output. Uses Docling for high-quality document conversion. Handles large documents with hierarchical summarization. Output to docs/generated/.
disable-model-invocation: true
version: 1.16.0
license: MIT
---

# Writer Agent

Transform documents and URLs into styled article series.

## Quick Reference

| Reference                                                             | Purpose                            |
| --------------------------------------------------------------------- | ---------------------------------- |
| [directory-structure.md](references/directory-structure.md)           | Output folder layout               |
| [decision-trees.md](references/decision-trees.md)                     | Workflow decision guides           |
| [retry-workflow.md](references/retry-workflow.md)                     | Error recovery procedures          |
| [large-doc-processing.md](references/large-doc-processing.md)         | Handling documents >50K words      |
| [article-writer-prompt.md](references/article-writer-prompt.md)       | Subagent prompt templates          |
| [context-extractor-prompt.md](references/context-extractor-prompt.md) | Context extraction template        |
| [context-optimization.md](references/context-optimization.md)         | Context optimization anti-patterns |
| [performance-benchmarks.md](references/performance-benchmarks.md)     | Measured performance test cases    |
| [detail-levels.md](references/detail-levels.md)                       | Output detail level options        |

## Workflow Overview

**Direct Path (<20K words OR <50K words with <=3 articles):**

Main agent writes all articles directly without subagents.

```
Input → Convert → Plan → Write(main) → Synthesize → Verify
  1        1        3         4            5           6
```

**Standard (Tier 1-2, 20K-100K words):**

```
Input → Convert → Analyze → Extract → Write → Synthesize → Verify
  1        1         3         3        4         5           6
```

**Fast Path (Tier 3, >=100K words):**

```
Input → Convert → Plan → Write(parallel) → Synthesize → Verify
  1        1        3          4              5           6
```

## Step 0: Resolve Skill Paths

**PHẢI chạy trước mọi bước khác.** Resolve đường dẫn thực tế của skill để tương thích cả project-local và global install.

```bash
# Tìm wa-env script
WA_ENV=$(find ~/.claude -name wa-env -path "*/writer-agent/*" -type f 2>/dev/null | head -1)
[ -z "$WA_ENV" ] && WA_ENV=$(find .claude -name wa-env -path "*/writer-agent/*" -type f 2>/dev/null | head -1)

# Parse output → lấy các biến
eval "$($WA_ENV)"
```

**Kết quả**: Các biến `SCRIPTS_DIR`, `SKILL_DIR`, `STYLES_DIR` sẵn sàng dùng cho các bước sau.

**Fallback** (nếu wa-env không tìm thấy):

```bash
# Tìm bất kỳ wa-convert nào
WA_CONVERT=$(find ~/.claude .claude -name wa-convert -path "*/writer-agent/*" -type f 2>/dev/null | head -1)
SCRIPTS_DIR=$(dirname "$WA_CONVERT")
SKILL_DIR=$(dirname "$SCRIPTS_DIR")
STYLES_DIR="$SKILL_DIR/output_styles"
```

> **Lưu ý**: Tất cả commands trong các bước sau dùng `$SCRIPTS_DIR`, `$SKILL_DIR`, `$STYLES_DIR` thay vì hardcoded paths.

## Step 1: Input Handling

Detect input type and convert to markdown.

| Input Type               | Detection               | Action                    |
| ------------------------ | ----------------------- | ------------------------- |
| File (PDF/DOCX/EPUB/etc) | Path + extension        | `wa-convert {path}`       |
| URL                      | `http://` or `https://` | `wa-convert {url}`        |
| Plain text / .txt / .md  | No complex extension    | Rewrite → `wa-paste-text` |

### File/URL Conversion

```bash
$SCRIPTS_DIR/wa-convert [/path/to/file.pdf or url]
```

**Output**: `docs/generated/{slug}-{timestamp}/input-handling/content.md`

### Plain Text Processing

1. Read content (if file)
2. Rewrite to structured markdown (add headings, preserve content)
3. Propose title
4. Execute:

```bash
echo "{rewritten_content}" | $SCRIPTS_DIR/wa-paste-text - --title "{title}"
```

### Error Handling

| Error              | Action                         |
| ------------------ | ------------------------------ |
| File not found     | Ask for correct path           |
| Unsupported format | Try Docling, confirm with user |
| URL fetch failed   | Report and stop                |
| Empty content      | Warn, confirm before continue  |
| Encrypted PDF      | Ask for decrypted version      |

## Step 2: Select Style

Use `AskUserQuestion` to confirm output style.

| Style                   | File                         | Voice                                |
| ----------------------- | ---------------------------- | ------------------------------------ |
| Professional            | `professional.md`            | Formal, data-driven, 3rd person      |
| Explanatory             | `explanatory.md`             | Teaching, "we" together              |
| Mindful Educator        | `mindful-educator.md`        | Depth + practice + mindfulness       |
| Introspective Narrative | `introspective-narrative.md` | Personal journey, "I"                |
| Mindful Dialogue        | `mindful-dialogue.md`        | Master-student dialogue              |
| Mindful Storytelling    | `mindful-storytelling.md`    | First person storytelling            |
| Deep Dive               | `deep-dive.md`               | Investigative, assumption-challenging |

Style files: `$STYLES_DIR/{style}.md`

## Step 2.5: Select Detail Level

Use `AskUserQuestion` to confirm output detail level.

| Level         | Ratio  | Description                         |
| ------------- | ------ | ----------------------------------- |
| Concise       | 15-25% | Tóm lược, giữ ý chính               |
| **Standard**  | 30-40% | Cân bằng (Recommended)              |
| Comprehensive | 50-65% | Chi tiết, giữ nhiều ví dụ           |
| Faithful      | 75-90% | Gần như đầy đủ, viết lại theo style |

**Default**: Standard (if user skips or unclear)

### Calculate Target Words (Tham khảo)

**LƯU Ý**: Target words chỉ mang tính tham khảo. PASS/FAIL dựa trên section coverage, không phải word count.

```
target_ratio = midpoint of selected level
total_target = source_words × target_ratio

Per article (reference only):
article_target = (article_source_words / source_words) × total_target
# Word count để định hướng, không bắt buộc đạt chính xác
```

### Understanding Detail Level Parameters

**Two complementary concepts:**

1. **`target_ratio`**: Controls total article length relative to source

   * Standard level: 30-40% (midpoint 35%)

   * This ratio applies to the entire article wordcount

2. **`example_percentage`**: Controls retention of examples within kept content

   * Standard level: 60% of examples

   * This percentage applies only to example sections

**Worked example (Standard level, 35% target ratio, 60% examples):**

* Source section: 5,000 words total

  * Main explanatory content: 4,000 words

  * Examples (10 examples): 1,000 words

* Target article length: 5,000 × 0.35 = 1,750 words

* Keep 60% of examples: 6 examples ≈ 600 words

* Remaining budget for main content: 1,750 - 600 = 1,150 words

* Main content compression: 1,150 / 4,000 = 28.75% (summarized)

**Key insight:** Higher `example_percentage` (60%) than overall `target_ratio` (35%) means examples are preserved more than prose, reflecting their teaching value.

See [detail-levels.md](references/detail-levels.md) for full specification.

## Step 2.6: Tier Reference Table

**Canonical tier definitions** (referenced throughout documentation):

| Tier            | Word Count                     | Strategy                       | Context Approach   | Glossary                    | max\_concurrent |
| --------------- | ------------------------------ | ------------------------------ | ------------------ | --------------------------- | --------------- |
| **Direct Path** | <20K OR (<50K AND ≤3 articles) | Main agent writes all          | N/A (no subagents) | Inline (\~200 words)        | N/A             |
| **Tier 1**      | 20K-50K                        | Subagents read source directly | No context files   | Inline (\~200 words)        | 3               |
| **Tier 2**      | 50K-100K                       | Smart compression              | Context extractors | Separate file (\~600 words) | 3               |
| **Tier 3**      | >=100K                         | Fast Path, minimal overhead    | No context files   | Inline (\~300 words)        | 2               |

**Priority rules:**

* Direct Path conditions are checked FIRST and override tier boundaries

* Documents 20K-50K with ≤3 articles use Direct Path (not Tier 1)

* Only documents failing Direct Path conditions fall through to tier selection

**Key differences:**

* Direct Path: Main agent handles everything (no subagents)

* Tier 1: Lightweight subagents, read source via line ranges

* Tier 2: Context extraction for compression (only tier with separate glossary file)

* Tier 3: Like Tier 1 but larger chunks, more selective glossary, lower concurrency

## Step 3: Analyze

**Goal**: Create analysis artifacts for article generation.

### 3.0 Processing Path Selection

Read `structure.json` → use `direct_path` field (computed by `wa-convert` v1.2+):

```
structure.json → direct_path.eligible?
├─ YES AND direct_path.capacity_ok?
│   └─ DIRECT PATH
│       └─ Skip context extraction
│       └─ Main agent writes ALL articles
│       └─ ~30% faster for small documents
│
├─ YES BUT NOT direct_path.capacity_ok?
│   └─ WARN: direct_path.warning
│   └─ RECOMMEND: Use Tier 1 with subagents instead
│
├─ NO AND tier_recommendation.tier <= 2?
│   └─ STANDARD PATH (3.1-3.5)
│
└─ NO AND tier_recommendation.tier == 3?
    └─ FAST PATH (Tier 3)
```

> **Note**: `direct_path` fields in structure.json (since v1.2) include `eligible`, `capacity_ok`, `capacity_limit`, and `warning`. These are pre-computed based on word count, estimated article count, and detected language. Main agent does NOT need to recalculate these values.

**Examples:**

| Document     | Words | Articles | Path            | Reason                                        |
| ------------ | ----- | -------- | --------------- | --------------------------------------------- |
| Blog post    | 15K   | 5        | Direct          | <20K words (first condition) ✓                |
| Tutorial     | 45K   | 3        | Direct          | <50K AND ≤3 articles (second condition) ✓     |
| Long guide   | 48K   | 3        | Direct → Tier 1 | Exceeds max\_words for mixed (38K) ⚠️         |
| Paper        | 45K   | 4        | Standard        | Fails both conditions (4 > 3) → use subagents |
| Book chapter | 67K   | 8        | Standard        | Tier 2: smart compression                     |
| Full book    | 142K  | 12       | Fast            | Tier 3: reference-based                       |

> **Note**: Direct Path capacity limit depends on language: EN ~44K, VI ~32K, mixed ~38K words. Use `structure.json → language` field for accurate limit.

### 3.1 Structure Scan

> **📖 READ FIRST**: [context-optimization.md](references/context-optimization.md) explains anti-patterns that waste 50%+ context budget. Review before proceeding.

**Quick path** (if `structure.json` exists):

* **ONLY** read `structure.json` for outline, stats, tier recommendation

* **DO NOT** read `content.md` - it wastes context budget

* Skip manual scanning (outline already in JSON)

**Fallback** (if `structure.json` missing):

⚠️ **WARNING**: Fallback mode loses 51% context optimization. Re-run `wa-convert` to generate `structure.json` if possible.

Manual scan using efficient commands:

```bash
# Extract heading structure without reading full file
grep -n "^#" docs/generated/{slug}/input-handling/content.md | head -100

# Or use line-based sampling (first 100 lines for overview)
Read(file_path, offset=1, limit=100)  # Only to extract headings
```

⚠️ **CRITICAL**: Do NOT read full `content.md` during structure scan! For all tiers, subagents will read source content directly when writing articles. Reading it now wastes 90%+ context budget. See [context-optimization.md](references/context-optimization.md) for budget examples and common mistakes.

### 3.1.1 Tier 3 Fast Path (>=100K words)

For very large documents, minimize analysis overhead:

| Action | Detail                                                            |
| ------ | ----------------------------------------------------------------- |
| SKIP   | `_glossary.md`, context files                                     |
| CREATE | Minimal `_plan.md` (section-to-article mapping + line ranges)     |
| EMBED  | Key terms (\~300 words) + dependencies inline in subagent prompts |
| SPAWN  | Subagents immediately after `_plan.md` (continuous batching)      |

**Context savings**: \~40% reduction in main agent context.

See [large-doc-processing.md](references/large-doc-processing.md#tier-3-fast-path) for `_plan.md` format, subagent prompt template, and workflow details.

### 3.2 Content Inventory

Use `structure.json` outline directly. Section IDs, line ranges, word counts, and critical markers are all available in `structure.json`.

### 3.3 Article Plan (`analysis/_plan.md`)

**Check user request first:**

```python
# Priority: User request > Auto-split
if user_specified_article_count:
    # User yêu cầu số bài cụ thể (ví dụ: "chia thành 5 bài")
    target_articles = user_specified_count
    skip_auto_split = True
    # Phân bổ sections đều cho các bài, không chia nhỏ thêm
else:
    # Auto mode: chia thành 3-7 bài, mỗi bài ~10 phút đọc
    target_articles = calculate_optimal_articles(total_words, detail_ratio)
    skip_auto_split = False
```

Group sections into articles (default 3-7, or user-specified count):

```markdown
| #   | Slug  | Title         | Sections      | Est. Words | Reading Time |
| --- | ----- | ------------- | ------------- | ---------- | ------------ |
| 1   | intro | Introduction  | S01, S02      | 2000       | ~13 min      |
| 2   | core  | Core Concepts | S03, S04, S05 | 2500       | ~13-15 min   |
```

**Rules**:

* All sections must be mapped. Coverage check at end.

* Target \~13-15 phút đọc/bài (2000-3000 từ)

* Nếu user chỉ định số bài → tuân theo, không auto-split thêm

**Content-Type Detection (tạo cùng lúc với plan):**

Khi tạo `_plan.md`, xác định `content_type` cho mỗi article:

| Content Type | Suggested Structure | Khi nào |
|-------------|-------------------|---------|
| `tutorial` | Problem → Solution → Steps → Practice | Hướng dẫn, how-to |
| `conceptual` | Question → Exploration → Framework → Implications | Lý thuyết, triết học |
| `narrative` | Scene → Conflict → Journey → Resolution | Câu chuyện, memoir |
| `analysis` | Finding → Evidence → Discussion → Application | Nghiên cứu, report |
| `mixed` | Follow output style's default Structure | Nội dung hỗn hợp |

Detection signals:

| Signal | Content Type |
|--------|-------------|
| Step-by-step headings, numbered lists, "how to" | `tutorial` |
| Questions as headings, thesis statements, arguments | `conceptual` |
| Narrative structure, characters, timeline | `narrative` |
| Data tables, methodology, findings | `analysis` |
| Mix of above | `mixed` (use dominant) |

Ghi vào plan table:

```markdown
| #   | Slug  | Title         | Sections      | Est. Words | Content Type |
| --- | ----- | ------------- | ------------- | ---------- | ------------ |
| 1   | intro | Introduction  | S01, S02      | 2000       | conceptual   |
| 2   | core  | Core Concepts | S03, S04, S05 | 2500       | tutorial     |
```

Subagent sử dụng: Embed `CONTENT_TYPE: {type}` vào prompt. Subagent ưu tiên:
1. Output style's Structure (primary)
2. Content-type hint (secondary, nếu style không có structure cụ thể cho loại này)

**Series Context (QUAN TRỌNG - tạo cùng lúc với plan):**

Khi tạo `_plan.md`, đồng thời xác định:

```markdown
## Series Context

Core message: "{1-2 câu thông điệp cốt lõi}"

| # | Title | Role | Reader Enters | Reader Exits | Bridge to Next |
| 1 | Intro | foundation | Chưa biết X | Hiểu X cơ bản | "Nhưng X trong thực tế...?" |
| 2 | Core | development | Hiểu X cơ bản | Nắm vững Y | "Y mở ra câu hỏi về Z..." |
| 3 | Adv | climax | Nắm vững Y | Kết nối Y với Z | N/A (last) |
```

**Cách tạo Reader Enters/Exits/Bridge:**
- `Reader Enters`: Kiến thức người đọc có khi bắt đầu bài (từ bài trước hoặc kiến thức nền)
- `Reader Exits`: Kiến thức người đọc đạt được sau bài (dẫn tới bài sau)
- `Bridge to Next`: 1 câu gợi tò mò kết nối bài này với bài tiếp (KHÔNG dùng "Trong phần tiếp theo...")

Thông tin này sẽ được embed vào `SERIES_CONTEXT` block trong mỗi subagent prompt (xem [article-writer-prompt.md](references/article-writer-prompt.md#series-context-block)).

### 3.3.1 Article Splitting (Auto)

**Trigger**: After Step 3.3, before Step 3.4. Check each planned article.

**Priority rules:**

1. **User-specified count**: Nếu user yêu cầu số bài cụ thể → tuân theo, KHÔNG auto-split
2. **Auto-split**: Chỉ áp dụng khi user KHÔNG yêu cầu số bài cụ thể

**Key constants:**

* `MAX_OUTPUT_WORDS = 3000` (\~15 min reading time)

* `TARGET_PART_WORDS = 2000` (\~13 min reading time)

* Atomic unit = H2 block (H2 + H3 children). NEVER split within paragraph, H3, or critical section.

**When to split**: `estimated_output = source_words × detail_ratio > MAX_OUTPUT_WORDS`

**Algorithm**: Greedy grouping of H2 blocks, no minimum. See [large-doc-processing.md#article-splitting-strategy](references/large-doc-processing.md#article-splitting-strategy) for full algorithm and validation matrix.

**Validate after split:**

```bash
$SCRIPTS_DIR/wa-validate-split docs/generated/{book}/analysis/_plan.md
```

**Part naming**: `02-core.md` → `02-core-part1.md`, `02-core-part2.md`

**Context bridging**: For Part N > 1, provide prev part topics, last paragraph, key concepts. See [article-writer-prompt.md#multi-part-article-template](references/article-writer-prompt.md#multi-part-article-template).

### 3.4 Shared Context (Inline Glossary)

⚠️ **TIMING**: Execute AFTER Steps 3.1-3.3 complete, BEFORE Step 3.5.

**Strategy by tier:**

```
word_count < 50,000 (Tier 1)?
├─ YES → Extract inline glossary (~200 words) from first ~300 lines
│   └─ Embed in each subagent prompt
│   └─ Skip separate _glossary.md
│   └─ Saves 1 Read call per subagent (~400 words saved)
│
├─ 50,000 <= word_count < 100,000 (Tier 2)?
│   └─ SKIP inline extraction (context extractors in Step 3.5 will create _glossary.md)
│       └─ Article writers (Step 4) will read shared _glossary.md file (~600 words)
│       └─ More comprehensive terminology than inline approach
│
└─ word_count >= 100,000 (Tier 3)?
    └─ Extract inline glossary (~300 words) from first ~500 lines
        └─ Embed in each subagent prompt
        └─ Skip separate _glossary.md
        └─ Larger than Tier 1 due to more technical terminology
```

**Extraction algorithm**: See [context-optimization.md#glossary-extraction-algorithm](references/context-optimization.md#glossary-extraction-algorithm) for detailed process.

**Quick process**:

1. Read content.md first 300-500 lines (tier-dependent)
2. Extract terms using definition patterns
3. Score by importance (frequency + position)
4. Take top N terms until hitting word budget
5. Format: `Term: definition (~20 words each)`

**Tier 3 inline rationale:**

* Avoids 1 Read call per subagent (saves \~400 words/subagent)

* Trade-off: More selective terms (300 vs 1000) but faster execution

* Larger than Tier 1 (300 vs 200 words) because large documents have more technical terminology

* Combined with reading source directly via line ranges = maximum efficiency

**Inline glossary format**:

```markdown
## Terms

Term1: definition (~20 words)
Term2: definition
Term3: definition
```

Article dependencies: Embed 1-2 sentences in prompt, not separate file.

### 3.5 Context Files

**Skip for**:

* Tier 1 (<50K words): Subagents read source directly via line ranges

* Tier 3 (>=100K words): Subagents read source directly via line ranges

* Direct Path (<20K words): Main agent writes directly

**Decision** (see [decision-trees.md#3](references/decision-trees.md#3-context-extraction-strategy) for full tree):

* Tier 1/3 or <20K words: Skip context files (subagents read source directly via line ranges)

* Tier 2 (50K-100K): Spawn context extractor subagents (batch: min(3, article\_count))

* Template: `templates/_context-file-template.md`

Each context file: `analysis/XX-{slug}-context.md`

### 3.6 Quality Gate: Analysis Complete

Before proceeding to Step 4, verify:

* [ ] All sections have IDs (from structure.json)

* [ ] Critical sections marked (\* auto-detected in structure.json)
  * **Guideline**: Thường <=30% sections là critical

  * **If >30%**: Tự động ghi nhận trong `_plan.md`, KHÔNG cần user confirmation

    * Document: "High critical ratio: {ratio}% - technical content"

    * Tiếp tục workflow bình thường

  * **If >50%**: Tự động chuyển sang Tier 3 strategy (read source directly)

    * KHÔNG cần STOP hoặc ask user

    * Tier 3 xử lý được high critical ratio vì đọc source trực tiếp

    * Ghi log: "Auto-escalated to Tier 3 due to high critical ratio"

  * **Rationale**: Tự động xử lý thay vì blocking workflow để hỏi user

* [ ] Article plan covers 100% sections

* [ ] For Tier 3: \_plan.md created with line ranges

## Step 4: Write Articles

### 4.0 State Tracking (Recommended)

For resume and retry support, create/update `analysis/_state.json`. Required if retry-workflow is needed (see [retry-workflow.md](references/retry-workflow.md)):

```json
{
  "status": "in_progress",
  "current_step": 4,
  "completed_articles": ["00-overview.md"],
  "pending_articles": ["01-intro.md", "02-core.md"]
}
```

See [retry-workflow.md](references/retry-workflow.md#state-persistence) for details.

For selective re-runs (style change or single article rewrite), see [retry-workflow.md#selective-re-run](references/retry-workflow.md#selective-re-run).

### 4.1 Overview Article (Phase 1)

Write `00-overview.md` in **main context**:

* Requires full series knowledge

* Template: `templates/_overview-template.md`

* Target: 300-400 words (initial)

* Include placeholders for Key Takeaways and Article Index

**Phase 1 content**:

* Surprising insight + Micro-story + Core questions + Why It Matters

* Placeholder sections for Điểm chính and Mục lục

### 4.2 Content Articles

**Direct Path** (<20K words): Main agent writes all articles directly.

**Standard/Fast Path**: Spawn subagents for articles 01+:

```
Task tool:
- subagent_type: "general-purpose"
- description: "Write: {title}"
- prompt: [Use references/article-writer-prompt.md]
```

**Multi-Part Articles** (from Step 3.3.1):

For split articles, spawn each part sequentially within the article:

```
# Article 2 was split into 3 parts
1. Spawn 02-core-part1.md
2. Wait for completion → extract context bridge
3. Spawn 02-core-part2.md (with context from part1)
4. Wait → extract context bridge
5. Spawn 02-core-part3.md (with context from part2)

# Other articles can run in parallel
# e.g., 01-intro.md and 03-advanced.md can run while part2 waits
```

**Context bridge extraction:**

```python
def extract_context_bridge(completed_part):
    """Extract context for next part from completed part"""
    article_content = read(completed_part.output_path)
    return {
        'prevPartTopics': extract_h2_titles(article_content),
        'prevPartEnding': get_last_paragraph(article_content, max_words=50),
        'keyConceptsFromPrev': extract_bold_terms(article_content)
    }
```

**Prompt validation (optional, for debugging):**

```bash
echo "{prompt_text}" | $SCRIPTS_DIR/wa-validate-prompt --tier {1|2|3} --stdin
```

Validates all required template variables are present. Exit code 0 = PASS, 1 = missing variables.

**Continuous Batching** (preferred over static batching):

* Tier 1-2: `max_concurrent = 3` (smaller chunks \~3.5K words)

* Tier 3: `max_concurrent = 2` (larger chunks \~10K words)

* Dynamic adjustment: large chunks (>8K) → reduce to 2, all small (<2K) → increase to 5

* On any completion → spawn next immediately (no batch waiting)

* **Benefits**: 25-35% faster than static batching

See [large-doc-processing.md#continuous-batching-vs-static](references/large-doc-processing.md#continuous-batching-vs-static) for full algorithm and [performance-benchmarks.md](references/performance-benchmarks.md) for benchmarks.

**Progress Reporting**:

After each article completes, update TaskUpdate:

* Format: `"Writing articles: {completed}/{total} completed"`

* Example: `"Writing articles: 3/7 completed"`

* Do NOT include time estimates

### 4.3 SoT Pattern (Long Articles)

**When to use** Skeleton-of-Thought: estimated output >2000 words AND >=5 subsections (H3 preferred, fallback to H2).

**Quick decision**: `h3_count >= 5` → SoT. `h3 == 0 AND h2 >= 5` → SoT. Otherwise → standard write.

**Workflow**: Phase 1 (skeleton) → Phase 2 (expand ALL sections parallel) → Phase 3 (merge + transitions)

**Benefits**: 45-50% faster for long articles. See [article-writer-prompt.md#sot-pattern](references/article-writer-prompt.md#sot-pattern) for template and [performance-benchmarks.md#test-case-5](references/performance-benchmarks.md#test-case-5-sot-pattern-long-article) for benchmarks.

**Limitations**: Priority 3 (paragraph breaks) not implemented. Ambiguous structure → default to standard write.

### 4.4 Coverage Tracking

Subagent reports coverage in **return message** (not in article file) using **table format**. See [Step 5.2](#52-coverage-aggregation) for aggregation details.

**IMPORTANT**: PASS/FAIL chỉ dựa trên section coverage, không phải word count. Word count chỉ mang tính thống kê.

**Subagent return format** (2-column, see article-writer-prompt.md):

```markdown
DONE: {filename} | {N} words (stats)
COVERAGE (determines PASS/FAIL):
| Section | Status |
|---------|--------|
| S01 | ✅ quoted |
| S02 ⭐ | ✅ faithful |
RESULT: PASS # PASS nếu all sections covered
```

**Tiêu chí PASS/FAIL:**

* **PASS**: Tất cả sections được assigned đều được covered (100% section coverage)

* **FAIL**: Có section bị missing hoặc skipped không hợp lệ

* **Word count**: Chỉ thống kê, KHÔNG ảnh hưởng PASS/FAIL

Main agent enriches with "Assigned To" and "Used In" columns → aggregates into `_coverage.md` (4-column format, see [Step 5.2](#52-coverage-aggregation)).

### 4.5 Critical Sections

**⭐ sections MUST be faithfully rewritten** (không tóm tắt, không bỏ ý):

* Giữ 100% ý nghĩa và thông tin gốc — KHÔNG được tóm tắt hay lược bỏ

* PHẢI viết lại bằng tiếng Việt theo voice của output style đã chọn

* KHÔNG copy nguyên văn từ source

* If unable to include fully → flag for review

### 4.6 Quality Gate: Articles Complete

Before proceeding to Step 5, verify:

* [ ] All articles written (check pending list)

* [ ] **Each article has "## Các bài viết trong series" at end** (check `SERIES_LIST: YES` in subagent return)
  * If `SERIES_LIST: NO` → Append series list to article file before continuing

* [ ] Coverage reports collected from all subagents

* [ ] No placeholder text in articles

* [ ] Source verification quotes provided

* [ ] Opening of each article is NOT mechanical ("Trong bài này...")

## Step 5: Synthesize

### 5.1 Update Overview (Phase 2)

Update `00-overview.md` with actual content for placeholder sections:

**Điểm chính** (Key Takeaways):

```markdown
## Điểm chính

1. **[Concept 1]**: [Brief explanation from series]
2. **[Concept 2]**: [Brief explanation from series]
3. **[Concept 3]**: [Brief explanation from series]
```

**Các bài viết trong series** (Series List):

```markdown
## Các bài viết trong series

1. **Tổng quan - Brief description** _(đang xem)_
2. [Article 1 Title](./01-slug.md) - Brief description
3. [Article 2 Title](./02-slug.md) - Brief description
```

**Final overview target**: 400-600 words

### 5.2 Coverage Aggregation

Collect subagent coverage tables → aggregate into `analysis/_coverage.md`

**Process**:

1. Each subagent returns a 2-column COVERAGE TABLE (`| Section | Status |`) in their return message
2. Main agent enriches each row with "Assigned To" and "Used In" columns (from `_plan.md`)
3. Concatenate all enriched tables into single `_coverage.md` file (4-column format)
4. Add summary statistics at bottom

**Column enrichment**: Main agent knows which article each subagent wrote, so it adds:

* `Assigned To`: article filename (from `_plan.md`)

* `Used In`: same as Assigned To (or different if reassigned during writing)

**Coverage file format** (required by `validate_coverage.py`):

```markdown
## Section Coverage Matrix

| Section | Assigned To   | Used In       | Status        |
| ------- | ------------- | ------------- | ------------- |
| S01     | 01-article.md | 01-article.md | ✅ summarized |
| S02 ⭐  | 01-article.md | 01-article.md | ✅ faithful   |

- Total: {N} | Used: {N} | Missing: {N}
```

**Format rules**:

* Column 1: `S{NN}` with optional `⭐` for critical sections

* Column 4:

  * For used sections: `✅` followed by one of: `used`, `faithful`, `quoted`, `summarized`

  * For skipped sections: `⚠️ skipped` (requires Notes column with reason)

* Summary line at bottom: `- Total: {N} | Used: {N} | Missing: {N}`

**Edge case examples**:

```markdown
| Section | Assigned To | Used In               | Status        | Notes                      |
| ------- | ----------- | --------------------- | ------------- | -------------------------- |
| S05     | 01-intro.md | 02-core.md            | ✅ summarized | Reassigned during planning |
| S08     | 02-core.md  | 02-core.md, 03-adv.md | ✅ quoted     | Shared across articles     |
| S12     | 03-adv.md   | -                     | ⚠️ skipped    | Redundant with S08         |
```

**Multi-Part Article Coverage:** For split articles, track by part in `_coverage.md`. Each section row should sum to ~100%. See [large-doc-processing.md#coverage-tracking](references/large-doc-processing.md#coverage-tracking) for format and validation rules.

**Edge case rules:**

1. **Reassignment**: Section moved to different article (common when planning adjusts)

   * "Assigned To" shows original plan

   * "Used In" shows actual article that included it

   * Validate coverage in "Used In" article

2. **Shared sections** (one section used in multiple articles):

   * Format: `Used In` = comma-separated list (e.g., `02-core.md, 03-adv.md`)

   * Validation: Each article in the list MUST contain \[Sxx] reference

   * Check both articles include the section (quoted, summarized, or paraphrased)

   * Status reflects how primary article used it

3. **Skipped**: Must document reason (redundant, off-topic, user instruction)

   * Status: `⚠️ skipped` (not `✅`)

   * Notes column required with explicit reason

Run validation:

```bash
$SCRIPTS_DIR/wa-validate docs/generated/{book}/analysis/_coverage.md
```

## Step 6: Verify

### 6.1 Coverage Check

**Soft target**: Coverage nên đạt >=95% (không bắt buộc retry)

```
Coverage results:
├─ >= 95% → PASS (tiếp tục)
├─ 90-94% → WARNING (ghi nhận, không retry tự động)
│   └─ Chỉ retry nếu user yêu cầu
├─ < 90% → ASK USER
│   └─ Option 1: Accept as-is
│   └─ Option 2: Retry specific articles
│   └─ Option 3: Create supplementary
```

**QUAN TRỌNG**: Không tự động retry để đạt coverage target. Việc retry tốn token và thời gian, thường không cải thiện đáng kể.

### 6.2 Quality Checklist

* [ ] All articles written, reader-ready (no metadata)

* [ ] Overview updated with Key Takeaways and Series List

* [ ] **All articles have "## Các bài viết trong series" at the end** (MANDATORY)

* [ ] All links in series lists verified

* [ ] \_coverage.md reported (>=95% target, >=90% acceptable)

* [ ] Critical ⭐ sections included (faithful rewrite — 100% meaning, Vietnamese, style voice)

* [ ] Warnings logged for any skipped sections

* [ ] **No mechanical openings** ("Trong bài này...", "Bài viết sẽ trình bày...")

* [ ] **No mechanical closings** ("Tóm lại, bài viết đã...", "Trong phần tiếp theo...")

### 6.3 Error Recovery (User-Driven)

| Error               | Action                         | Auto-retry? |
| ------------------- | ------------------------------ | ----------- |
| Subagent timeout    | Report to user, ask what to do | ❌ NO        |
| Missing output      | Log warning, continue          | ❌ NO        |
| Style mismatch      | Report, user decides           | ❌ NO        |
| Content fabrication | Flag for user review           | ❌ NO        |
| Coverage < 90%      | Ask user for decision          | ❌ NO        |

**Nguyên tắc**: Không tự động retry. User có toàn quyền quyết định.

See [retry-workflow.md](references/retry-workflow.md) for user decision flow.

## Content Guidelines

### Source Fidelity

* Use ONLY source material, no fabrication

* **REWRITE ALL content in output style voice** — Source defines WHAT to say, Style defines HOW to say it

* DO NOT copy-paste sentences from source (bao gồm cả ⭐ critical sections)

* Maintain original terminology (thuật ngữ giữ nguyên, nhưng câu văn phải được viết lại)

* ⭐ Critical sections: faithful rewrite — giữ 100% ý nghĩa, KHÔNG tóm tắt, viết lại bằng tiếng Việt + style voice

* Non-critical sections: MUST be rewritten in the selected output style's voice, structure, and language patterns

* VERIFY quotes prove source origin, but article content must be rewritten (not copied)

### Writing Quality

**Narrative Coherence:**

* Mỗi bài viết phải có mạch logic riêng, KHÔNG phải tóm tắt tuần tự từng section

* Sections phải nối với nhau bằng bridges (logical hoặc emotional), không phải "Tiếp theo..."

* Draw connections giữa các ý trong bài VÀ với thông điệp cốt lõi của series

**Opening & Closing (quyết định ấn tượng):**

* Opening: Hook compelling (câu hỏi, hình ảnh, khoảnh khắc). TRÁNH: "Trong bài này chúng ta sẽ..."

* Closing: Kết resonant (câu hỏi mở, hình ảnh, lời mời). TRÁNH: "Tóm lại, bài viết đã trình bày..."

* Mechanical phrases BLACKLIST: "Trong phần tiếp theo", "Như đã đề cập ở trên", "Bài viết này sẽ", "Tóm lại"

**Depth vs Breadth:**

* Khi một ý quan trọng: đi SÂU (ví dụ, implications, câu hỏi) thay vì liệt kê

* Khi nhiều ý nhỏ: nhóm lại thành pattern/theme, không liệt kê từng ý riêng lẻ

* Priority: 2-3 key insights explored deeply > 10 points listed superficially

**Reader Engagement:**

* Đặt câu hỏi cho người đọc (rhetorical hoặc reflective)

* Dùng ví dụ cụ thể, relatable thay vì abstract

* Tạo tension/curiosity trước khi giải đáp

* Vary sentence length: xen kẽ câu ngắn và dài

### Formatting

* Link between articles with relative paths

* Track all sections with \[Sxx] IDs

* NO markdown tables in article output - use bullet points instead

* NO diagrams (mermaid, ASCII, flowcharts) - describe in prose or bullets

### Series List (MANDATORY)

* **MỖI bài viết PHẢI có "## Các bài viết trong series" ở cuối** - Thiếu = FAIL

* Mark current article with _(đang xem)_

* Validation: Subagent return format includes `SERIES_LIST: YES/NO`

* Main agent MUST check `SERIES_LIST: YES` trước khi accept article

## Cài đặt thư viện mới

Skill sử dụng virtual environment tại `$SCRIPTS_DIR/.venv`. Khi cần cài thêm thư viện, **PHẢI activate venv trước**:

```bash
# 1. Activate venv (dùng SCRIPTS_DIR từ Step 0)
source $SCRIPTS_DIR/.venv/bin/activate

# 2. Cài package
uv pip install <package>

# 3. Cập nhật requirements.txt
uv pip freeze > $SCRIPTS_DIR/requirements.txt
```

**KHÔNG dùng:**

* `uv pip install <package>` khi chưa activate venv → lỗi "No virtual environment found"

* `uv pip install <package> --system` → lỗi "externally managed" (Python Homebrew)

* `uv add <package>` → cần pyproject.toml, skill dùng requirements.txt

