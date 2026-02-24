---
name: writer-agent
description: Transform documents into styled article series. Analyze input (md, txt, pdf, docx, pptx, xlsx, html, epub, images, url), extract core ideas, decompose into logical sections, write articles with user-selectable styles (professional, casual, custom), synthesize into organized output. Uses Docling for high-quality document conversion. Handles large documents with hierarchical summarization. Output to docs/generated/.
disable-model-invocation: true
version: 2.0.0
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

**Tier Workflow Files** (loaded at Step 2.7 after tier determination):

| Tier | File | When |
| --- | --- | --- |
| Direct Path | [tier-direct-path.md](references/tier-direct-path.md) | <20K OR (<50K AND ≤3 articles) |
| Tier 1 | [tier-1-workflow.md](references/tier-1-workflow.md) | 20K-50K (fails Direct Path) |
| Tier 2 | [tier-2-workflow.md](references/tier-2-workflow.md) | 50K-100K |
| Tier 3 | [tier-3-workflow.md](references/tier-3-workflow.md) | >=100K |

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

**PHẢI thực hiện TRƯỚC mọi bước khác.** Skill có thể nằm ở thư mục thường hoặc thư mục ẩn (dotdir).

> **LƯU Ý**: Glob mặc định **bỏ qua thư mục ẩn** (bắt đầu bằng `.`). Khi skill được cài qua plugin, nó nằm trong `.agents/skills/` — Glob với `**/` sẽ KHÔNG tìm được.

**Bước 1**: Tìm `wa-convert` theo thứ tự ưu tiên (dừng ngay khi tìm thấy):

```
# 1a. Glob thư mục thường (nhanh nhất)
Glob("**/writer-agent/scripts/wa-convert")

# 1b. Nếu 1a không có kết quả → tìm trong các dotdir phổ biến
Glob(".agent/**/wa-convert")
Glob(".agents/**/wa-convert")
Glob(".claude/**/wa-convert")

# 1c. Nếu 1b vẫn không có → dùng find (tìm cả dotdir)
Bash: find . -path "*/writer-agent/scripts/wa-convert" -not -path "*/.venv/*" 2>/dev/null | head -1
```

**Bước 2**: Từ kết quả, xác định các đường dẫn:

```
SCRIPTS_DIR    = directory chứa wa-convert  (ví dụ: /Users/x/.agents/skills/writer-agent/scripts)
SKILL_DIR      = parent của SCRIPTS_DIR     (ví dụ: /Users/x/.agents/skills/writer-agent)
VOICES_DIR     = SKILL_DIR/voices
STRUCTURES_DIR = SKILL_DIR/structures
IDENTITIES_DIR = SKILL_DIR/identities
AUDIENCES_DIR  = SKILL_DIR/audiences
EMOTIONS_DIR   = SKILL_DIR/emotional_maps
TEMPLATES_DIR  = SKILL_DIR/templates
```

**Bước 3**: Ghi nhớ các đường dẫn này. Tất cả commands trong các bước sau PHẢI dùng đường dẫn đã resolve, KHÔNG dùng relative path.

**Ví dụ**: Nếu tìm thấy `/Users/x/.agents/skills/writer-agent/scripts/wa-convert`:
- Gọi convert: `/Users/x/.agents/skills/writer-agent/scripts/wa-convert file.pdf`
- Đọc voice: `/Users/x/.agents/skills/writer-agent/voices/teacher.md`
- Đọc structure: `/Users/x/.agents/skills/writer-agent/structures/building-blocks.md`

> **QUAN TRỌNG**: KHÔNG BAO GIỜ hardcode path cố định, luôn dùng đường dẫn tuyệt đối từ Bước 1.

**Bước 4 (Validation)**: Verify paths đã resolve:

```python
# PHẢI verify trước khi tiếp tục Step 1
assert Glob(f"{SCRIPTS_DIR}/wa-convert")   # Script chính
assert Glob(f"{VOICES_DIR}/*.md")          # Voice files
assert Glob(f"{STRUCTURES_DIR}/*.md")      # Structure files
assert Glob(f"{TEMPLATES_DIR}/*.md")       # Templates
# Nếu BẤT KỲ assert nào fail → STOP, kiểm tra lại Bước 1-2
```

> **FAIL CONDITION**: Nếu cả 3 cách tìm (1a, 1b, 1c) đều không tìm thấy `wa-convert` → STOP workflow hoàn toàn. KHÔNG tự suy đoán paths.

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


## Step 2: Select Writing Dimensions

Hệ thống 5 chiều độc lập. User chọn preset combo hoặc Custom để mix-match tự do.

### Preset Combos (Recommended)

Show bảng sau cho user, hỏi chọn preset hoặc "Custom":

| Preset | Voice | Structure | Identity | Audience | Emotion |
|--------|-------|-----------|----------|----------|---------|
| Educator | Teacher | Building Blocks | Tech Builder | Curious Beginners | Empower & Challenge |
| Storyteller | Storyteller | Story Arc | Contemplative Thinker | Deep Seekers | Reflect & Discover |
| Analyst | Objective | BLUF-Evidence | Knowledge Curator | Busy Professionals | Empower & Challenge |
| Explorer | Investigator | Five Layers | Knowledge Curator | Deep Seekers | Provoke & Transform |
| Mentor | Guide | Depth-Practice | Contemplative Thinker | Curious Beginners | Reflect & Discover |
| Reflector | Personal | Spiral Return | Contemplative Thinker | Deep Seekers | Reflect & Discover |
| Zen Master | Dialogue | Master-Student | Contemplative Thinker | Deep Seekers | Reflect & Discover |

**Cách dùng**: Hiển thị bảng trên → Hỏi user gõ tên preset (e.g. "Educator") hoặc "Custom".

- **Nếu chọn preset**: Tất cả 5 dimensions đã set, skip đến Step 2.5
- **Nếu chọn Custom**: Chuyển sang Step 2a-2f bên dưới (chọn từng chiều)
- **Adaptive structure**: Dùng khi content mixed/không fit structures cố định. Chỉ available qua Custom mode hoặc user yêu cầu trực tiếp.

### Step 2a-2f: Custom Mode (chọn từng chiều)

**Flow:** Voice → Structure → Identity → Audience → Emotion (tất cả bắt buộc)

Mỗi chiều có default mapping dựa trên voice. Suggest defaults, user PHẢI confirm hoặc chọn khác.

**Step 2a: Voice** — Hỏi user confirm voice (giọng văn, tone, persona).

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

Voice files: `voices/{voice}.md`. Xem `references/dimension-comparison.md` để so sánh.

**Step 2b: Structure** — Hỏi user confirm structure. Mỗi voice có `default_structure` trong frontmatter.

| Structure | File | Organization | Default cho |
| --- | --- | --- | --- |
| BLUF-Evidence | `bluf-evidence.md` | Executive Summary → Evidence → Action | Objective |
| Building Blocks | `building-blocks.md` | Hook → Intuition → Concept → Example → Apply | Teacher |
| Five Layers | `five-layers.md` | Surface → Structure → Tension → Connection → Synth | Investigator |
| Spiral Return | `spiral-return.md` | Moment → Spiral deeper → Open ending | Personal |
| Master-Student | `master-student.md` | Experience → Dialogue → Silence | Dialogue |
| Story Arc | `story-arc.md` | Scene → Encounter → Deepening → Transformation | Storyteller |
| Depth-Practice | `depth-practice.md` | Present moment → Layers → Practice invitation | Guide |
| Adaptive | `adaptive.md` | Content-driven, flexible | Mixed content |

Structure files: `structures/{structure}.md`

**Step 2c: Identity** — Hỏi user chọn writer identity.

| Identity | File | Mô tả | Default cho |
| --- | --- | --- | --- |
| Tech Builder | `tech-builder.md` | Practitioner, pragmatic builder | Teacher |
| Contemplative Thinker | `contemplative-thinker.md` | Hành giả, tìm ý nghĩa | Personal, Guide, Dialogue, Storyteller |
| Knowledge Curator | `knowledge-curator.md` | Cross-domain connector | Objective, Investigator |
| **Custom** | User tạo mới | Theo `templates/identity-template.md` | - |

**Step 2d: Audience** — Hỏi user viết cho ai.

| Audience | File | Mô tả | Default cho |
| --- | --- | --- | --- |
| Busy Professionals | `busy-professionals.md` | Bận, cần actionable | Objective |
| Curious Beginners | `curious-beginners.md` | Mới, cần clarity | Teacher, Guide |
| Deep Seekers | `deep-seekers.md` | Muốn chiều sâu | Personal, Investigator, Dialogue, Storyteller |
| **Custom** | User tạo mới | Theo `templates/audience-template.md` | - |

**Step 2e: Emotion** — Hỏi user muốn người đọc cảm thấy gì.

| Emotion | File | Mô tả | Default cho |
| --- | --- | --- | --- |
| Empower & Challenge | `empower-challenge.md` | Growth qua discomfort | Teacher, Objective |
| Reflect & Discover | `reflect-discover.md` | Stillness, wonder | Personal, Guide, Dialogue, Storyteller |
| Provoke & Transform | `provoke-transform.md` | Challenge assumptions | Investigator |
| **Custom** | User tạo mới | Theo `templates/emotion-template.md` | - |

### Step 2f: Compatibility Check (Custom mode only)

Sau khi chọn xong 5 dimensions, kiểm tra compatibility:

```python
pairs_to_check = [(identity, voice), (audience, voice), (emotion, voice)]
low_compat = [pair for pair in pairs_to_check if compatibility(pair) == "★"]
if low_compat:
    warn(f"Combo {low_compat} có compatibility thấp (★)")
    # Hỏi user: tiếp tục hay chọn khác?
```

**Conflict Resolution**: Voice quyết định HOW (style/tone), Profile (Identity/Audience/Emotion) bổ sung WHAT (authority, đối tượng, cảm xúc).

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
```

### Understanding Detail Level Parameters

**Two complementary concepts:**

1. `**target_ratio**`: Controls total article length relative to source
  - Standard level: 30-40% (midpoint 35%)
2. `**example_percentage**`: Controls retention of examples within kept content
  - Standard level: 60% of examples

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

## Step 2.7: Load Tier Workflow (BẮT BUỘC)

**Sau khi xác định tier từ Step 2.6**, đọc file workflow tương ứng:

```python
tier = determine_tier(structure_json)  # Từ structure.json

if tier == "direct_path":
    Read(f"{SKILL_DIR}/references/tier-direct-path.md")
elif tier == 1:
    Read(f"{SKILL_DIR}/references/tier-1-workflow.md")
elif tier == 2:
    Read(f"{SKILL_DIR}/references/tier-2-workflow.md")
elif tier == 3:
    Read(f"{SKILL_DIR}/references/tier-3-workflow.md")
```

**Tier workflow file chứa Steps 3-4.** Sau khi hoàn thành Step 4, load `references/steps-5-6-synthesize-verify.md` cho Steps 5-6.

> **FAIL CONDITION**: Nếu không load tier workflow file → KHÔNG biết cách xử lý Steps 3-4 cho tier đó. STOP và load file đúng.

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
