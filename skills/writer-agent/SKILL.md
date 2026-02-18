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


| Reference                                                             | Purpose                            | Load at Step       | DP | T1 | T2 | T3 |
| --------------------------------------------------------------------- | ---------------------------------- | ------------------ | -- | -- | -- | -- |
| [directory-structure.md](references/directory-structure.md)           | Output folder layout               | Step 1             | ✓  | ✓  | ✓  | ✓  |
| [decision-trees.md](references/decision-trees.md)                     | Workflow decision guides           | On confusion only  | ✓  | ✓  | ✓  | ✓  |
| [retry-workflow.md](references/retry-workflow.md)                     | Error recovery procedures          | On error only      | -  | ✓  | ✓  | ✓  |
| [large-doc-processing.md](references/large-doc-processing.md)         | Handling documents >50K words      | Step 3 (if >20K)   | -  | -  | ✓  | ✓  |
| [article-writer-prompt.md](references/article-writer-prompt.md)       | Subagent prompt templates          | Step 4             | -  | ✓  | ✓  | ✓  |
| [context-extractor-prompt.md](references/context-extractor-prompt.md) | Context extraction template        | Step 3 (Tier 2)    | -  | -  | ✓  | -  |
| [context-optimization.md](references/context-optimization.md)         | Context optimization anti-patterns | Step 3.1           | -  | ✓  | ✓  | ✓  |
| [detail-levels.md](references/detail-levels.md)                       | Output detail level options        | Step 2.5           | ✓  | ✓  | ✓  | ✓  |

**DP** = Direct Path | **T1-T3** = Tier 1-3 | **✓** = Load | **-** = Skip

**Dimension files** (loaded at Step 2): `voices/{voice}.md`, `structures/{structure}.md`, `identities/{identity}.md`, `audiences/{audience}.md`, `emotional_maps/{emotion}.md`


## Workflow Overview

**Direct Path (<20K words OR <50K words with <=3 articles):**

Main agent writes all articles directly without subagents.

```
Input → Convert → Style/Structure → Plan → Write(main) → Synthesize → Verify
  1        1           2               3        4            5           6
```

**Standard (Tier 1-2, 20K-100K words):**

```
Input → Convert → Style/Structure → Analyze → Extract → Write → Synthesize → Verify
  1        1           2               3         3         4        5           6
```

**Fast Path (Tier 3, >=100K words):**

```
Input → Convert → Style/Structure → Plan → Write(parallel) → Synthesize → Verify
  1        1           2              3          4              5           6
```

## Step 0: Resolve Skill Paths (BẮT BUỘC)

**PHẢI thực hiện TRƯỚC mọi bước khác.** Skill có thể được cài ở nhiều vị trí khác nhau.

**Bước 1**: Dùng Glob tìm `wa-convert`:

```
Glob("**/writer-agent/scripts/wa-convert")
```

**Bước 2**: Từ kết quả, xác định 4 đường dẫn:

```
SCRIPTS_DIR    = directory chứa wa-convert  (ví dụ: /Users/x/.claude/skills/writer-agent/scripts)
SKILL_DIR      = parent của SCRIPTS_DIR     (ví dụ: /Users/x/.claude/skills/writer-agent)
VOICES_DIR     = SKILL_DIR/voices           (ví dụ: /Users/x/.claude/skills/writer-agent/voices)
STRUCTURES_DIR = SKILL_DIR/structures       (ví dụ: /Users/x/.claude/skills/writer-agent/structures)
IDENTITIES_DIR = SKILL_DIR/identities       (ví dụ: /Users/x/.claude/skills/writer-agent/identities)
AUDIENCES_DIR  = SKILL_DIR/audiences        (ví dụ: /Users/x/.claude/skills/writer-agent/audiences)
EMOTIONS_DIR   = SKILL_DIR/emotional_maps   (ví dụ: /Users/x/.claude/skills/writer-agent/emotional_maps)
TEMPLATES_DIR  = SKILL_DIR/templates        (ví dụ: /Users/x/.claude/skills/writer-agent/templates)
```

**Bước 3**: Ghi nhớ các đường dẫn này. Tất cả commands trong các bước sau PHẢI dùng đường dẫn đã resolve, KHÔNG dùng relative path.

**Ví dụ**: Nếu Glob trả về `/Users/x/.claude/skills/writer-agent/scripts/wa-convert`:
- Gọi convert: `/Users/x/.claude/skills/writer-agent/scripts/wa-convert file.pdf`
- Đọc voice: `/Users/x/.claude/skills/writer-agent/voices/teacher.md`
- Đọc structure: `/Users/x/.claude/skills/writer-agent/structures/building-blocks.md`
- Đọc identity: `/Users/x/.claude/skills/writer-agent/identities/tech-builder.md`
- Đọc template: `/Users/x/.claude/skills/writer-agent/templates/overview-template.md`

> **QUAN TRỌNG**: KHÔNG BAO GIỜ hardcode `.claude/skills/writer-agent/...`, luôn dùng đường dẫn tuyệt đối từ Glob.

**Bước 4 (Validation)**: Verify các paths đã resolve bằng cách kiểm tra file tồn tại:

```python
# PHẢI verify trước khi tiếp tục Step 1
assert Glob(f"{SCRIPTS_DIR}/wa-convert")   # Script chính
assert Glob(f"{VOICES_DIR}/*.md")          # Voice files
assert Glob(f"{STRUCTURES_DIR}/*.md")      # Structure files
assert Glob(f"{TEMPLATES_DIR}/*.md")  # Templates
# Nếu BẤT KỲ assert nào fail → STOP, kiểm tra lại Bước 1-2
```

> **FAIL CONDITION**: Nếu không tìm thấy `wa-convert` → STOP workflow hoàn toàn. KHÔNG tự suy đoán paths.

## Step 1: Input Handling

> **GUARD**: `SCRIPTS_DIR` đã resolve từ Step 0. Nếu chưa → **STOP, quay lại Step 0**.

Detect input type and convert to markdown.

**Output language**: Luôn là tiếng Việt, bất kể source language.


| Input Type               | Detection                        | Action                    |
| ------------------------ | -------------------------------- | ------------------------- |
| File (PDF/DOCX/EPUB/etc) | Path + extension                 | `wa-convert {path}`       |
| URL (web page)           | `http://` or `https://`          | `wa-convert {url}`        |
| YouTube URL              | `youtube.com` or `youtu.be`      | `wa-convert {url}`        |
| Plain text / .txt / .md  | No complex extension             | Rewrite → `wa-paste-text` |


### File/URL Conversion

```bash
{SCRIPTS_DIR}/wa-convert [/path/to/file.pdf or url]
```

**Output**: `docs/generated/{slug}-{timestamp}/input-handling/content.md`

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


## Step 2: Select Writing Dimensions (5 Dimensions)

Hệ thống 5 chiều độc lập. User chọn từng chiều, mix-match tự do.

**Flow:** Voice → Structure → Identity → Audience → Emotion (tất cả bắt buộc)

Mỗi chiều có default mapping dựa trên voice. Hệ thống suggest defaults, user PHẢI confirm hoặc chọn khác cho mỗi chiều.

**Skip dimension**: Nếu user nói "không biết" hoặc skip → dùng default mapping → ghi nhận → tiếp tục. Không hỏi lại.

### Step 2a: Select Voice

Hỏi user để confirm voice (giọng văn, tone, persona).

| Voice | File | Mô tả |
| --- | --- | --- |
| Teacher | `teacher.md` | "Chúng ta" đồng hành, teaching, ấm áp |
| Personal | `personal.md` | "Tôi" personal journey, vulnerable |
| Objective | `objective.md` | Neutral, data-driven, formal |
| Guide | `guide.md` | Đồng hành mindful, Đông-Tây |
| Investigator | `investigator.md` | Tìm hiểu, đặt câu hỏi, challenge |
| Dialogue | `dialogue.md` | Thầy-trò đối thoại, Zen |
| Storyteller | `storyteller.md` | Kể chuyện ngôi thứ nhất, chánh niệm |
| **Custom** | User tạo mới | Theo `templates/voice-template.md` |

Voice files: `voices/{voice}.md`

Xem `references/dimension-comparison.md` để so sánh tất cả dimensions.

**Custom voice**: Nếu user muốn tạo voice riêng, copy `templates/voice-template.md` → `voices/{custom-name}.md`, điền theo template. Tương tự cho custom structure: `structures/structure-template.md` → `structures/{custom-name}.md`.

### Step 2b: Select Structure

Hỏi user để confirm structure (tổ chức bài viết).

Mỗi voice có `default_structure` trong frontmatter. Suggest default, user có thể override.

| Structure | File | Organization | Default cho |
| --- | --- | --- | --- |
| BLUF-Evidence | `bluf-evidence.md` | Executive Summary → Evidence → Action | Objective |
| Building Blocks | `building-blocks.md` | Hook → Intuition → Concept → Example → Apply | Teacher |
| Five Layers | `five-layers.md` | Surface → Structure → Tension → Connection → Synth | Investigator |
| Spiral Return | `spiral-return.md` | Moment → Spiral deeper → Open ending | Personal |
| Master-Student | `master-student.md` | Experience → Dialogue → Silence | Dialogue |
| Story Arc | `story-arc.md` | Scene → Encounter → Deepening → Transformation | Storyteller |
| Depth-Practice | `depth-practice.md` | Present moment → Layers → Practice invitation | Guide |

Structure files: `structures/{structure}.md`

Xem `references/dimension-comparison.md` để so sánh và mix-match.

### Step 2c: Select Writer Identity

Hỏi user chọn writer identity. Suggest default dựa trên voice, user confirm hoặc chọn khác.

| Identity | File | Mô tả | Default cho |
| --- | --- | --- | --- |
| Tech Builder | `tech-builder.md` | Practitioner, pragmatic builder | Teacher |
| Contemplative Thinker | `contemplative-thinker.md` | Hành giả, tìm ý nghĩa | Personal, Guide, Dialogue, Storyteller |
| Knowledge Curator | `knowledge-curator.md` | Cross-domain connector | Objective, Investigator |
| **Custom** | User tạo mới | Theo `templates/identity-template.md` | - |

Identity files: `identities/{identity}.md`

### Step 2d: Select Audience Profile

Hỏi user viết cho ai. Suggest default dựa trên voice, user confirm hoặc chọn khác.

| Audience | File | Mô tả | Default cho |
| --- | --- | --- | --- |
| Busy Professionals | `busy-professionals.md` | Bận, cần actionable | Objective |
| Curious Beginners | `curious-beginners.md` | Mới, cần clarity | Teacher, Guide |
| Deep Seekers | `deep-seekers.md` | Muốn chiều sâu | Personal, Investigator, Dialogue, Storyteller |
| **Custom** | User tạo mới | Theo `templates/audience-template.md` | - |

Audience files: `audiences/{audience}.md`

### Step 2e: Select Emotional Map

Hỏi user muốn người đọc cảm thấy gì. Suggest default dựa trên voice, user confirm hoặc chọn khác.

| Emotion | File | Mô tả | Default cho |
| --- | --- | --- | --- |
| Empower & Challenge | `empower-challenge.md` | Growth qua discomfort | Teacher, Objective |
| Reflect & Discover | `reflect-discover.md` | Stillness, wonder | Personal, Guide, Dialogue, Storyteller |
| Provoke & Transform | `provoke-transform.md` | Challenge assumptions | Investigator |
| **Custom** | User tạo mới | Theo `templates/emotion-template.md` | - |

Emotion files: `emotional_maps/{emotion}.md`

**Flow:** Chọn voice → Hệ thống suggest defaults cho tất cả → User confirm hoặc chọn khác từng cái

### Default Mapping Table

> **📖 See**: [`references/dimension-comparison.md`](references/dimension-comparison.md) for full default mapping table, compatibility matrix, and mixing guidelines.

Mỗi dimension table ở trên đã ghi "Default cho" column. Dùng bảng so sánh chi tiết khi cần xác nhận compatibility.

### Step 2f: Compatibility Check (BẮT BUỘC sau khi chọn xong 5 dimensions)

Sau khi user confirm tất cả 5 dimensions, **PHẢI kiểm tra compatibility** trước khi tiếp tục:

```python
# Đọc dimension-comparison.md section 7 (Cross-dimension Compatibility)
# Kiểm tra 3 cặp: Identity×Voice, Audience×Voice, Emotion×Voice
pairs_to_check = [
    (identity, voice),   # Identity × Voice table
    (audience, voice),   # Audience × Voice table
    (emotion, voice),    # Emotion × Voice table
]
low_compat = [pair for pair in pairs_to_check if compatibility(pair) == "★"]

if low_compat:
    # PHẢI thông báo user trước khi tiếp tục
    warn(f"Combo {low_compat} có compatibility thấp (★), có thể tạo tension trong giọng văn.")
    # Hỏi: "Bạn muốn tiếp tục hay chọn khác?"
    # Nếu user confirm → proceed
    # Nếu user chọn khác → quay lại step tương ứng
```

> **FAIL CONDITION**: Nếu có combo ★ mà KHÔNG cảnh báo user → vi phạm workflow.

**Conflict Resolution**: Khi dimensions tạo tension (vd: Provoke & Transform + Teacher voice), Voice luôn quyết định HOW (giọng văn, tone, persona). Profile (Identity/Audience/Emotion) bổ sung WHAT (authority, đối tượng, cảm xúc). Nếu conflict: Voice wins về style/tone, Profile wins về content framing.

## Step 2.5: Select Detail Level

Hỏi user để confirm output detail level.


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

1. `**target_ratio**`: Controls total article length relative to source
  - Standard level: 30-40% (midpoint 35%)
  - This ratio applies to the entire article wordcount
2. `**example_percentage**`: Controls retention of examples within kept content
  - Standard level: 60% of examples
  - This percentage applies only to example sections

> See [detail-levels.md](references/detail-levels.md) for worked examples and full specification.

## Step 2.6: Tier Reference Table

**Canonical tier definitions** (referenced throughout documentation):


| Tier            | Word Count                     | Strategy                       | Context Approach   | Glossary                   | max_concurrent |
| --------------- | ------------------------------ | ------------------------------ | ------------------ | -------------------------- | -------------- |
| **Direct Path** | <20K OR (<50K AND ≤3 articles) | Main agent writes all          | N/A (no subagents) | Inline (~200 words)        | N/A            |
| **Tier 1**      | 20K-50K (fails Direct Path)    | Subagents read source directly | No context files   | Inline (~200 words)        | 3              |
| **Tier 2**      | 50K-100K                       | Smart compression              | Context extractors | Separate file (~600 words) | 3              |
| **Tier 3**      | >=100K                         | Fast Path, minimal overhead    | No context files   | Inline (~300 words)        | 2              |


**Priority rules:**

- Direct Path conditions are checked FIRST and override tier boundaries
- Documents 20K-50K with ≤3 articles use Direct Path (not Tier 1)
- Only documents failing Direct Path conditions fall through to tier selection

> **Note**: Direct Path `<50K` condition is further limited by language: EN ~44K, VI ~32K, mixed ~38K words. These limits are pre-computed in `structure.json → direct_path.capacity_ok`. If capacity exceeded, fallback to Tier 1.

**Key differences:**

- Direct Path: Main agent handles everything (no subagents)
- Tier 1: Lightweight subagents, read source via line ranges
- Tier 2: Context extraction for compression (only tier with separate glossary file)
- Tier 3: Like Tier 1 but larger chunks, more selective glossary, lower concurrency

## Step 3: Analyze

> **GUARD**: Step 1 hoàn thành (`content.md` + `structure.json` tồn tại). Nếu thiếu → **STOP, quay lại Step 1**.

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
| Long guide   | 48K   | 3        | Direct → Tier 1 | Exceeds max_words for mixed (38K) ⚠️          |
| Paper        | 45K   | 4        | Standard        | Fails both conditions (4 > 3) → use subagents |
| Book chapter | 67K   | 8        | Standard        | Tier 2: smart compression                     |
| Full book    | 142K  | 12       | Fast            | Tier 3: reference-based                       |


> **Note**: Direct Path capacity limit depends on language: EN ~44K, VI ~32K, mixed ~38K words. Use `structure.json → language` field for accurate limit.

### 3.1 Structure Scan

> **📖 READ FIRST**: [context-optimization.md](references/context-optimization.md) explains anti-patterns that waste 50%+ context budget. Review before proceeding.

**Quick path** (if `structure.json` exists):

- **ONLY** read `structure.json` for outline, stats, tier recommendation
- **DO NOT** read `content.md` - it wastes context budget
- Skip manual scanning (outline already in JSON)

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


| Action | Detail                                                           |
| ------ | ---------------------------------------------------------------- |
| SKIP   | `_glossary.md`, context files                                    |
| CREATE | Minimal `_plan.md` (section-to-article mapping + line ranges)    |
| EMBED  | Key terms (~300 words) + dependencies inline in subagent prompts |
| SPAWN  | Subagents immediately after `_plan.md` (continuous batching)     |


**Context savings**: ~40% reduction in main agent context.

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

- All sections must be mapped. Coverage check at end.
- Target reading time phụ thuộc detail level: Concise ~5min, Standard ~10min, Comprehensive ~13min, Faithful ~15min
- Target words/bài: 2000-3000 từ (tham khảo, không bắt buộc)
- Nếu user chỉ định số bài → tuân theo, không auto-split thêm

**Content-Type Detection**: Khi tạo plan, xác định `content_type` cho mỗi article (`tutorial`, `conceptual`, `narrative`, `analysis`, `mixed`). Embed `CONTENT_TYPE: {type}` vào subagent prompt. Subagent ưu tiên structure file (primary), content-type hint (secondary).

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

- `MAX_OUTPUT_WORDS = 3000` (~15 min reading time)
- `TARGET_PART_WORDS = 2000` (~13 min reading time)
- Atomic unit = H2 block (H2 + H3 children). NEVER split within paragraph, H3, or critical section.

**When to split**: `estimated_output = source_words × detail_ratio > MAX_OUTPUT_WORDS`

**Algorithm**: Greedy grouping of H2 blocks, no minimum. See [large-doc-processing.md#article-splitting-strategy](references/large-doc-processing.md#article-splitting-strategy) for full algorithm and validation matrix.

**Validate after split:**

```bash
{SCRIPTS_DIR}/wa-validate-split docs/generated/{book}/analysis/_plan.md
```

**Part naming**: `02-core.md` → `02-core-part1.md`, `02-core-part2.md`

**Context bridging**: For Part N > 1, provide prev part topics, last paragraph, key concepts. See [article-writer-prompt.md#multi-part-article-template](references/article-writer-prompt.md#multi-part-article-template).

### 3.4 Shared Context (Inline Glossary)

⚠️ **TIMING**: Execute AFTER Steps 3.1-3.3, BEFORE Step 3.5.

**Strategy**: Tier 1/3 → inline glossary (~200-300 words) embed trong prompt. Tier 2 → seed glossary → context extractors produce `_glossary.md`. Chi tiết: [context-optimization.md#glossary-extraction-algorithm](references/context-optimization.md#glossary-extraction-algorithm-step-34).

Article dependencies: Embed 1-2 sentences in prompt, not separate file.

### 3.5 Context Files

**Skip for**:

- Tier 1 (<50K words): Subagents read source directly via line ranges
- Tier 3 (>=100K words): Subagents read source directly via line ranges
- Direct Path (<20K words): Main agent writes directly

**Decision** (see [decision-trees.md#3](references/decision-trees.md#3-context-extraction-strategy-updated-v1110) for full tree):

- Tier 1/3 or <20K words: Skip context files (subagents read source directly via line ranges)
- Tier 2 (50K-100K): Spawn context extractor subagents (batch: min(3, article_count))
- Template: `templates/_context-file-template.md`

Each context file: `analysis/XX-{slug}-context.md`

### 3.6 Quality Gate: Analysis Complete

Before proceeding to Step 4, verify:

- [ ] All sections have IDs (from structure.json)

- [ ] Critical sections marked (* auto-detected in structure.json)
  - **Guideline**: Thường <=30% sections là critical
  - **If >30%**: Tự động ghi nhận trong `_plan.md`, KHÔNG cần user confirmation
    - Document: "High critical ratio: {ratio}% - technical content"
    - Tiếp tục workflow bình thường
  - **If >50%**: Tự động chuyển sang Tier 3 strategy (read source directly)
    - KHÔNG cần STOP hoặc ask user
    - Tier 3 xử lý được high critical ratio vì đọc source trực tiếp
    - Ghi log: "Auto-escalated to Tier 3 due to high critical ratio"
  - **Rationale**: Tự động xử lý thay vì blocking workflow để hỏi user

- [ ] Article plan covers 100% sections

- [ ] For Tier 3: _plan.md created with line ranges

## Step 4: Write Articles

> **GUARD**: Verify trước khi bắt đầu:
> 1. `_plan.md` đã tạo (Step 3.3) → Nếu chưa → **STOP, quay lại Step 3**
> 2. Tier đã xác định (Direct Path / Tier 1-3) → Nếu chưa → **STOP, đọc structure.json**
> 3. `voice_content` + `structure_content` đã pre-read (Step 4.0a) → Nếu chưa → đọc ngay bên dưới

### 4.0a Pre-read Voice & Structure (BẮT BUỘC)

**PHẢI thực hiện TRƯỚC khi spawn subagents.** Main agent đọc sẵn voice và structure files, embed nội dung vào subagent prompt. Subagent KHÔNG tự đọc các file này.

```python
# Main agent đọc 1 lần, dùng cho tất cả subagents
voice_content = Read(f"{VOICES_DIR}/{voice}.md")
structure_content = Read(f"{STRUCTURES_DIR}/{structure}.md")

# Embed vào prompt thay vì truyền file path
# ĐÚNG: VOICE:\n{voice_content}
# SAI:  STYLE: {VOICES_DIR}/{voice}.md  (subagent phải tự đọc → lãng phí context)
```

**Lý do**: Mỗi file read trong subagent tạo ~4-6 JSON messages trong conversation transcript. Với 2 file reads (voice + structure), mỗi subagent tiết kiệm ~8-12 messages + ~300 lines content trong transcript trả về cho main agent.

### 4.0b Subagent Context Budget Rules

**Giảm output trả về main agent:**

1. **CONTEXT RULES** - Đã embed trong prompt template, cấm subagent glob/read files thừa
2. **run_in_background: true** - Dùng cho parallel article writing (≥3 articles). Main agent không nhận full transcript vào context.
3. **Summary files (.done)** - Subagent ghi summary ra `{outputPath}.done` bên cạnh article file. Main agent đọc `.done` files thay vì transcript.

```python
# Parallel writing với run_in_background
tasks = []
for article in articles:
    task = Task(
        subagent_type="general-purpose",
        description=f"Write: {article.title}",
        run_in_background=True,  # QUAN TRỌNG: tránh prompt too long
        prompt=compose_prompt(article, voice_content, structure_content)
    )
    tasks.append(task)
```

### 4.0b.1 Result Collection Protocol (BẮT BUỘC)

**Subagent ghi 2 files:**
- `articles/{slug}.md` — bài viết (article content)
- `articles/{slug}.md.done` — summary (~200 bytes: DONE, KEY_TAKEAWAY, COVERAGE, RESULT, VERIFY)

**Main agent thu thập kết quả:**

```python
# 1. Check completion: list .done files
Bash("ls articles/*.done")  # Biết bài nào đã xong

# 2. Read summary: đọc từng .done file (~200 bytes mỗi file)
Read("articles/01-intro.md.done")  # DONE, KEY_TAKEAWAY, COVERAGE, RESULT, VERIFY

# 3. Validate word count (nếu cần)
Bash("wc -w articles/01-intro.md")
```

**KHÔNG BAO GIỜ dùng các cách sau (gây bloat context):**

```python
# ❌ SAI: TaskOutput trả full transcript (50-100KB mỗi subagent)
TaskOutput(task_id="xxx")

# ❌ SAI: tail trên .output file trả raw JSONL (mỗi dòng hàng nghìn ký tự)
Bash("tail -5 /tmp/.../tasks/xxx.output")

# ❌ SAI: đọc article file chỉ để lấy summary
Read("articles/01-intro.md")  # 3000+ words vào context không cần thiết
```

**Lý do**: File `.output` là JSONL event stream, chứa toàn bộ Read/Write tool results (source content + article content). Dù chỉ `tail -5`, mỗi dòng JSONL có thể chứa hàng nghìn ký tự. TaskOutput cũng trả full transcript tương tự.

### 4.0c State Tracking (Recommended)

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

- Requires full series knowledge
- Template: `templates/overview-template.md`
- Target: 300-400 words (initial)
- Include placeholders for Key Takeaways and Article Index

**Phase 1 content**:

- Surprising insight + Micro-story + Core questions + Why It Matters
- Placeholder sections for Điểm chính and Mục lục

### 4.2 Content Articles

**Direct Path** (<20K words): Main agent writes all articles directly.

Direct Path guidelines — main agent follows cùng shared rules như subagent:
- Đọc voice file + structure file
- Đọc source content.md trực tiếp (full hoặc theo line ranges từ structure.json)
- Apply tất cả shared rules: LANGUAGE, FORMATTING, REWRITE RULE, ANTI-AI WRITING
- KHÔNG cần return format (vì không có subagent)
- Viết từng article theo `_plan.md`, save vào `articles/XX-{slug}.md`
- Mỗi article MUST end with "## Các bài viết trong series"
- Coverage tracking: main agent tự tạo `_coverage.md` sau khi viết xong tất cả

**Standard/Fast Path**: Spawn subagents for articles 01+:

```
Task tool:
- subagent_type: "general-purpose"
- description: "Write: {title}"
- run_in_background: true  # Dùng cho ≥3 articles
- prompt: [Use references/article-writer-prompt.md]
# QUAN TRỌNG: Dùng {voiceContent} và {structureContent} đã pre-read ở Step 4.0a
# KHÔNG truyền file paths cho subagent tự đọc
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

> See [large-doc-processing.md §Context Bridge](references/large-doc-processing.md#context-bridge) for the `extract_context_bridge()` function used between multi-part articles.

**Prompt validation (optional, for debugging):**

```bash
echo "{prompt_text}" | {SCRIPTS_DIR}/wa-validate-prompt --tier {1|2|3} --stdin
```

Validates all required template variables are present. Exit code 0 = PASS, 1 = missing variables.

**Continuous Batching** (preferred over static batching):

- Tier 1-2: `max_concurrent = 3` (smaller chunks ~3.5K words)
- Tier 3: `max_concurrent = 2` (larger chunks ~10K words)
- Dynamic adjustment: large chunks (>8K) → reduce to 2, all small (<2K) → increase to 5
- On any completion → spawn next immediately (no batch waiting)
- **Benefits**: 25-35% faster than static batching

See [large-doc-processing.md#continuous-batching-vs-static](references/large-doc-processing.md#continuous-batching-vs-static) for full algorithm.

**Progress Reporting**:

After each article completes, update TaskUpdate:

- Format: `"Writing articles: {completed}/{total} completed"`
- Example: `"Writing articles: 3/7 completed"`
- Do NOT include time estimates

### 4.3 SoT Pattern (Long Articles)

**When to use** Skeleton-of-Thought: estimated output >2000 words AND >=5 subsections (H3 preferred, fallback to H2).

**Quick decision**: `h3_count >= 5` → SoT. `h3 == 0 AND h2 >= 5` → SoT. `h3 + h2 >= 5` → SoT. Otherwise → standard write.

**Workflow**: Phase 1 (skeleton) → Phase 2 (expand ALL sections parallel) → Phase 3 (merge + transitions)

**Benefits**: 45-50% faster for long articles. See [article-writer-prompt.md#sot-pattern](references/article-writer-prompt.md#sot-pattern-long-articles-2000-words) for template.

**Limitations**: Priority 3 (paragraph breaks) not implemented. Ambiguous structure → default to standard write.

### 4.4 Coverage Tracking

**Coverage Format Pipeline**: Subagent returns 2-column (`Section | Status`) → Main agent enriches to 4-column (`Section | Assigned To | Used In | Status`) → Aggregate into `_coverage.md`. See [§5.2](#52-coverage-aggregation) for aggregation.

**IMPORTANT**: PASS/FAIL chỉ dựa trên section coverage, không phải word count. Word count chỉ mang tính thống kê.

**Subagent return format** (see article-writer-prompt.md):

```markdown
DONE: {filename} | {N} words
KEY_TAKEAWAY: Sinh lực bùng lên khi có mục đích rõ ràng và hành động mỗi ngày
COVERAGE:
| Section | Status |
|---------|--------|
| S01 | ✅ quoted |
| S02 ⭐ | ✅ faithful |
RESULT: PASS
SERIES_LIST: YES
VERIFY: "Vita Nova" (L21)
```

**Tiêu chí PASS/FAIL:**

- **PASS**: Tất cả assigned sections được covered HOẶC skipped với lý do hợp lệ (redundant, off-topic, user instruction)
- **FAIL**: Có section bị missing hoặc skipped không hợp lệ (không có lý do, hoặc "too long" / "already covered" thiếu reference)
- **Word count**: Chỉ thống kê, KHÔNG ảnh hưởng PASS/FAIL

Main agent enriches with "Assigned To" and "Used In" columns → aggregates into `_coverage.md` (4-column format, see [Step 5.2](#52-coverage-aggregation)).

### 4.5 Critical Sections

**⭐ sections MUST be faithfully rewritten** (không tóm tắt, không bỏ ý):

- Giữ 100% ý nghĩa và thông tin gốc, KHÔNG được tóm tắt hay lược bỏ
- PHẢI viết lại bằng tiếng Việt theo voice đã chọn
- KHÔNG copy nguyên văn từ source
- If unable to include fully → flag for review

### 4.6 Quality Gate: Articles Complete

Before proceeding to Step 5, verify từ `.done` files (KHÔNG cần đọc article files hay transcript):

```python
# Đọc tất cả .done files để verify
for done_file in Glob("articles/*.done"):
    summary = Read(done_file)  # ~200 bytes mỗi file
    # Parse: DONE, KEY_TAKEAWAY, COVERAGE, RESULT, SERIES_LIST, VERIFY
```

- [ ] All articles written (check `.done` files vs pending list)
- [ ] All RESULT: PASS (coverage đầy đủ)
- [ ] All SERIES_LIST: YES
- [ ] KEY_TAKEAWAY collected từ `.done` files (dùng cho Step 5.1)
- [ ] VERIFY quotes provided (spot-check source fidelity)

## Step 5: Synthesize

### 5.1 Update Overview (Phase 2)

Update `00-overview.md` with actual content for placeholder sections.

**KHÔNG đọc lại articles.** Dùng dữ liệu từ `.done` files:

```python
# Nguồn dữ liệu cho overview (KHÔNG cần đọc article files hay transcript):
key_takeaways = []  # Từ KEY_TAKEAWAY trong .done files (Step 4.6)
series_list = []    # Từ _plan.md (đã có titles + descriptions từ Step 3)
core_message = ""   # Từ _plan.md Series Context
```

**Multi-part articles**: Gom KEY_TAKEAWAYs của các parts thành 1 takeaway cho bài đó. Ví dụ: article 02 có 3 parts → chọn takeaway đại diện nhất hoặc tổng hợp thành 1 câu.

**Điểm chính** (Key Takeaways) - compose từ KEY_TAKEAWAYs:

```markdown
## Điểm chính

1. **[Concept từ article 1 KEY_TAKEAWAY]**: [Expand từ takeaway]
2. **[Concept từ article 2 KEY_TAKEAWAY]**: [Expand từ takeaway]
3. **[Concept từ article 3 KEY_TAKEAWAY]**: [Expand từ takeaway]
```

**Các bài viết trong series** (Series List) - compose từ `_plan.md`:

```markdown
## Các bài viết trong series

1. **Tổng quan - Brief description** _(đang xem)_
2. [Article 1 Title](./01-slug.md) - Brief description
3. [Article 2 Title](./02-slug.md) - Brief description
```

**Final overview target**: 400-600 words (overview đặc biệt, dùng word target thay vì section coverage)

**Fallback nếu KEY_TAKEAWAY kém**: Nếu takeaway quá generic hoặc trống, dùng article title + plan description từ `_plan.md` thay thế. KHÔNG đọc article file chỉ để cải thiện takeaway.

### 5.2 Coverage Aggregation

Collect subagent coverage tables → aggregate into `analysis/_coverage.md`

**Process**: Subagent returns 2-column (`Section | Status`) → Main agent enriches to 4-column (`Section | Assigned To | Used In | Status`) → Concatenate into `_coverage.md` → Add summary stats.

**Coverage file format**:

```markdown
## Section Coverage Matrix

| Section | Assigned To   | Used In       | Status        |
| ------- | ------------- | ------------- | ------------- |
| S01     | 01-article.md | 01-article.md | ✅ summarized |
| S02 ⭐  | 01-article.md | 01-article.md | ✅ faithful   |

- Total: {N} | Used: {N} | Missing: {N}
```

**Edge cases** (reassignment, shared sections, skipped): See [large-doc-processing.md#coverage-tracking](references/large-doc-processing.md#coverage-tracking).

Run validation:

```bash
{SCRIPTS_DIR}/wa-validate docs/generated/{book}/analysis/_coverage.md
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

Verify từ subagent returns + overview file (KHÔNG cần đọc article files):

- [ ] All RESULT: PASS (từ subagent returns)

- [ ] Overview updated with Key Takeaways and Series List (đọc `00-overview.md` ~600 words)

- [ ] All SERIES_LIST: YES (từ returns, append nếu NO)

- [ ] All links in series lists verified (trong overview file)

- [ ] _coverage.md reported (>=95% target, >=90% acceptable)

- [ ] Critical ⭐ sections: VERIFY quotes match source (spot-check từ returns)

- [ ] Warnings logged for any skipped sections

- [ ] Anti-AI writing rules passed (xem [article-writer-prompt.md#anti-ai-writing](references/article-writer-prompt.md))

### 6.3 Error Recovery (User-Driven)

> **Policy**: Không tự động retry. Mọi lỗi đều report cho user và chờ quyết định. See [retry-workflow.md](references/retry-workflow.md).

## Content Guidelines

**Key rules**: Source fidelity (rewrite, don't copy), ⭐ critical sections = faithful rewrite 100%, Anti-AI writing (no em dash, no AI vocabulary), NO tables/diagrams in output, MỖI article PHẢI có "## Các bài viết trong series" ở cuối. Full details: [article-writer-prompt.md](references/article-writer-prompt.md).

## Cài đặt thư viện mới

Skill sử dụng virtual environment tại `{SCRIPTS_DIR}/.venv`. Khi cần cài thêm thư viện, **PHẢI activate venv trước**:

```bash
# 1. Activate venv (dùng SCRIPTS_DIR từ Step 0)
source {SCRIPTS_DIR}/.venv/bin/activate

# 2. Cài package
uv pip install <package>

# 3. Cập nhật requirements.txt
uv pip freeze > {SCRIPTS_DIR}/requirements.txt
```

**KHÔNG dùng:**

- `uv pip install <package>` khi chưa activate venv → lỗi "No virtual environment found"
- `uv pip install <package> --system` → lỗi "externally managed" (Python Homebrew)
- `uv add <package>` → cần pyproject.toml, skill dùng requirements.txt

<br>