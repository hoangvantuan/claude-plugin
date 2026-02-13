# Large Document Processing

Load this reference when document word count > 20K.

> **📖 Tier Definitions**: See [SKILL.md Step 2.6](../SKILL.md#step-26-tier-reference-table) for canonical tier table with thresholds, strategies, and parameters.
> [Decision Trees](decision-trees.md#2-context-tier-selection) for tier selection flow.

## Quick Path (Structure JSON)

If `structure.json` exists (from wa-convert):

```python
structure = read("docs/generated/book/input-handling/structure.json")
tier = structure["tier_recommendation"]["tier"]

for chunk in structure["suggested_chunks"]:
    # Include overlap from previous chunk if available
    if chunk.get("overlap_from_prev"):
        start = chunk["overlap_from_prev"]
    else:
        start = chunk["line_start"]

    Read(file, offset=start, limit=chunk["line_end"] - start + 1)
```

**Chunk fields**:

* `line_start`, `line_end`: Main content boundaries

* `overlap_from_prev`: Start line for \~10 lines overlap from previous chunk (None for first chunk)

* `word_count`: Actual word count (not estimate)

* `heading_path`: Hierarchical path like `["Chapter 1", "Section A"]`

**Skip manual chunking** when structure.json available.

## Context Tiers

### Direct Path (<20K words OR <50K with ≤3 articles)

Main agent writes all articles directly. No context extraction needed.

**Rationale:** Main agent can handle up to ~50K words when article count is low (≤3), as the overhead of spawning subagents outweighs benefits for simple structures.

```
# Use pre-computed fields from structure.json (v1.2+)
direct_path.eligible AND direct_path.capacity_ok?
├─ YES → Main agent writes ALL articles
│   └─ Embed inline glossary in prompts
│   └─ ~30% faster than subagent workflow
│
├─ eligible BUT NOT capacity_ok?
│   └─ WARN: direct_path.warning
│   └─ Recommend Tier 1 instead
│
└─ NOT eligible → Use tier_recommendation.tier
```

**Examples:** See [SKILL.md §3.0](../SKILL.md#30-processing-path-selection) for detailed examples.

### Tier 1: Direct Source Read (20K-50K words)

Subagents đọc source trực tiếp qua line ranges từ `structure.json`. Inline glossary (~200 words) embed trong prompt.

```
Subagent workflow:
1. Read voice file
2. Read source content.md L{start}-{end} (from structure.json outline)
3. Write article (rewrite in voice persona)
4. Return coverage report
```

### Tier 2: Smart Compression (50K-100K words)

1. Critical sections (*): Keep FULL source in context file (article writer sẽ faithful rewrite)
2. Supporting sections: Summarize

```markdown
# {Article Title}
TIER:2 | LINES:1-1500 | WORDS:25K | CRIT:S02,S05

## Content
[S01] {Title}
{Source text}

[S02]* {Critical Title}
{FULL source text, article writer sẽ faithful rewrite}

[S03] {Supporting} [SUMMARIZED]
Key points:
- Point 1
- Point 2
Full: content.md L200-350
```

### Tier 3: Fast Path (>=100K words)

Subagents read source directly via line ranges. No context files.

```
1. wa-convert → structure.json
2. Read structure.json → extract key terms
3. Create minimal _plan.md
4. Spawn article writers (continuous batching)
   └─ Each reads source directly via L{start}-{end}
5. Collect coverage → synthesize
```

## Tier 3 Fast Path

For documents >=100K words, reduce main agent overhead by ~40%.

### What to Skip

| Standard Step | Fast Path Action |
|---------------|------------------|
| Analysis artifacts | SKIP - use `structure.json` outline |
| `_glossary.md` | SKIP - embed ~300 words in subagent prompt |
| Article dependencies | SKIP - embed 1-2 sentences per article in prompt |
| Context files | SKIP - subagents read source directly |
| Context extractors | SKIP - combine with article writers |

### What to Create

1. **Minimal `_plan.md`** - Section→article mapping only:

```markdown
# Article Plan
Voice: personal | Source: content.md (111K words)

| # | Slug | Outline Indices | Lines | Chunks |
|---|------|-----------------|-------|--------|
| 0 | overview | - | - | - |
| 1 | intro | 0-2 | 1-258 | 0 |
| 2 | core | 3-5 | 259-574 | 1 |
```

2. **Inline context in subagent prompts**:

```markdown
TASK: Write "{title}" for {seriesTitle}

SOURCE: {sourcePath} L{start}-{end}
STYLE: {VOICES_DIR}/{voice}.md
OUTPUT: {outputPath}

TERMS:
- Term1: Definition (~20 words)
- Term2: Definition

NAV: [Prev](./{prev}.md) | [Next](./{next}.md)
```

### Workflow (Continuous Batching)

```
1. wa-convert → structure.json
2. Hỏi user → style
3. Read structure.json → extract key terms from first chunk
4. Create minimal _plan.md
5. Write 00-overview.md (main agent)
6. Spawn article writers (continuous batching):
   ├─ max_concurrent = 2
   ├─ Spawn immediately when slot available
   ├─ On complete → spawn next (no batch waiting)
   └─ Each: Read source chunk → Write → Return coverage
7. Collect coverage reports → _coverage.md
8. Update 00-overview.md (Key Takeaways + Article Index)
9. Verify >=95% coverage
```

### Subagent Efficiency

Each subagent receives:
- Source file path + exact line range
- Style file path (not content)
- Inline key terms (~300 words)
- Article dependencies (2-3 sentences)

Subagent workflow:
1. Read style file (~350 words)
2. Read source chunk (~10K words from suggested_chunks)
3. Write article
4. Return coverage report

**No separate context extraction step** = fewer subagent calls.

## Article Splitting Strategy

When a single article would exceed 3000 words output, automatically split into multiple parts.

### When Applied

| Condition | Action |
|-----------|--------|
| Estimated output > 3000 words | Split into parts |
| Most common in Tier 2-3 | Large source chunks |
| Applies after _plan.md created | Step 3.3.1 |

### Atomic Units

```
H2 block = smallest unsplittable unit
         = 1 H2 heading + all H3 children + content

NEVER split:
├── Within a paragraph
├── Between H3 and parent H2
├── A critical section [Sxx]*
└── Inside code blocks or tables
```

### Splitting Algorithm

```python
MAX_OUTPUT = 3000   # words per article
TARGET = 2000       # ideal words per part
# NOTE: No MIN_PART - prioritize content coverage over word count

def split_article(article, detail_ratio=0.35):
    source_words = sum(s.word_count for s in article.sections)
    estimated = source_words * detail_ratio

    if estimated <= MAX_OUTPUT:
        return [article]  # No split needed

    # Extract H2 blocks
    h2_blocks = extract_h2_blocks(article.sections)

    # Greedy grouping (prioritize content coverage)
    parts = []
    current = {'blocks': [], 'words': 0}

    for block in h2_blocks:
        block_output = block.word_count * detail_ratio

        if current['words'] + block_output > MAX_OUTPUT:
            if current['blocks']:  # Has content = start new part
                parts.append(current)
                current = {'blocks': [], 'words': 0}

        current['blocks'].append(block)
        current['words'] += block_output

    if current['blocks']:
        parts.append(current)

    # No merge step - small parts OK if content complete
    return parts
```

### Validation Matrix

Before spawning subagents, validate split coverage:

| Check | Pass Condition | Error |
|-------|----------------|-------|
| No overlap | Each line in exactly 1 part | `OverlapError` |
| No miss | All source lines covered | `MissError` |
| Content coverage | No min - prioritize content coverage | Small parts OK if complete |
| Critical intact | [Sxx]* 100% in single part | Cannot split critical |

**Validation pseudocode:**

```python
def validate_split(article, parts):
    covered_lines = set()

    for part in parts:
        for block in part['blocks']:
            for line in range(block.line_start, block.line_end + 1):
                if line in covered_lines:
                    raise OverlapError(f"Line {line} duplicated")
                covered_lines.add(line)

    expected = set()
    for section in article.sections:
        expected.update(range(section.line_start, section.line_end + 1))

    missing = expected - covered_lines
    if missing:
        raise MissError(f"Lines {sorted(missing)} not covered")

    return True
```

### Context Bridging

For Part N > 1, provide context from Part N-1:

```markdown
CONTEXT BRIDGE:
- Previous part: 02-core-part1.md
- Prev topics: Fundamentals, Architecture
- Prev ended with: "...đó là nền tảng cho phần tiếp theo."
- Key concepts: authentication, token-based auth, session
```

**Extraction:**

```python
def extract_context_bridge(completed_part):
    content = read(completed_part.output_path)
    return {
        'prevPartSlug': completed_part.slug,
        'prevPartTopics': extract_h2_titles(content),
        'prevPartEnding': get_last_paragraph(content, max_words=50),
        'keyConceptsFromPrev': extract_bold_terms(content)
    }
```

### Part Naming Convention

| Original | Split Parts |
|----------|-------------|
| `02-core.md` | `02-core-part1.md`, `02-core-part2.md`, `02-core-part3.md` |
| `03-advanced.md` | `03-advanced-part1.md`, `03-advanced-part2.md` |

### Series List Format (Multi-Part)

```markdown
## Các bài viết trong series

1. [Tổng quan](./00-overview.md) - Giới thiệu series
2. [Introduction](./01-intro.md) - Khái niệm cơ bản
3a. [Core Concepts - Phần 1](./02-core-part1.md) - Fundamentals
3b. **Core Concepts - Phần 2** _(đang xem)_
3c. [Core Concepts - Phần 3](./02-core-part3.md) - Best Practices
4. [Advanced Topics](./03-advanced.md) - Nâng cao
```

### Coverage Tracking

Each part reports its sections. Main agent aggregates:

```markdown
## Multi-Part Coverage: 02-core (3 parts)

| Section | Part 1 | Part 2 | Part 3 | Total |
|---------|--------|--------|--------|-------|
| S03 | 100% | - | - | 100% ✅ |
| S04 | 60% | 40% | - | 100% ✅ |
| S05 | - | 100% | - | 100% ✅ |
| S06 ⭐ | - | - | 100% | 100% ✅ |
```

**Rules:**
- Each row MUST sum to 100%
- Critical sections [Sxx]* MUST be 100% in single part
- No line overlap between parts

## Prefetch Strategy

> **📖 Referenced from**: [SKILL.md Step 3.1.1](../SKILL.md#311-tier-3-fast-path-100k-words) - Tier 3 Fast Path uses prefetch to parallelize analysis.

Parallelize analysis to reduce wait time:

```
wa-convert completes
    │
    ├─ structure.json ready
    │
    └─ IMMEDIATELY start (parallel):
        ├─ Extract key terms (first 300 lines)
        ├─ Prepare minimal _plan.md
        ├─ Pre-generate subagent prompts
        └─ Write 00-overview.md

Result: ~15-20% faster than sequential
```

## Chunking Algorithm

### Chunk Parameters

| Parameter   | Value         | Notes                       |
| ----------- | ------------- | --------------------------- |
| Target size | 11.5K words   | Safe margin for subagent    |
| Overlap     | 10 lines      | ~100-150 words continuity   |
| Minimum     | 3K words      | Merge smaller chunks        |

### Boundary Detection (priority high → low)

1. H1 headings (`#`) → Chapter-level
2. H2 headings (`##`) → Section chunks
3. Horizontal rules (`---`) → Topic breaks
4. H3 headings (`###`) → If section > 10K words
5. Empty lines + paragraph → Fallback

### Semantic Boundary Rules

- Never split inside code blocks (```)
- Never split inside tables
- Prefer splitting at blank lines (paragraph boundaries)
- Keep bulleted/numbered lists together

### Algorithm

```
1. SCAN: grep -n "^#" file.md → [(line, level, title), ...]
2. BUILD: H1 contains H2 contains H3
3. CALCULATE: words = actual word count per section
4. SPLIT: If section > 11.5K words → split at next heading level
5. OVERLAP: Include last 10 lines of prev chunk
6. TAG: Add section path as metadata
```

## Format-Specific Handling

### Text/Markdown Large Files

```bash
# Read in chunks (~1500 lines, ~13K words safe)
Read(file_path, offset=1, limit=1500)     # Chunk 1
Read(file_path, offset=1501, limit=1500)  # Chunk 2
```

### PDF Large Documents

**Text-based PDF:**

```bash
pdftotext -layout input.pdf output.txt
```

**Scanned PDFs (OCR):**

```bash
pdftoppm -png -r 150 -f 1 -l 10 input.pdf /tmp/pages/page
# Process with ai-multimodal skill
```

## Word Budget Distribution

| Component          | Main Agent | Sub-agent  |
| ------------------ | ---------- | ---------- |
| structure.json     | ~350 words | -          |
| Inline glossary    | -          | ~300 words |
| \_plan.md          | ~1000 words| -          |
| Source content     | 0          | 10-13K words|
| **Total**          | **~1.5K**  | **10-13K** |

## Continuous Batching vs Static

| Approach | Behavior | Speed |
|----------|----------|-------|
| Static (old) | Wait for batch N to complete → spawn batch N+1 | Baseline |
| Continuous | Spawn next immediately when any slot frees | +25-40% |

> See [SKILL.md §4.2](../SKILL.md#42-content-articles) for continuous batching pseudocode with dynamic concurrency adjustment.
