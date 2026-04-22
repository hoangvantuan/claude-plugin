# Large Document Processing

Load this reference when document word count > 20K.

> **📖 Tier Definitions**: See [SKILL.md Step 2.2](../SKILL.md#22-determine-tier) for tier table with thresholds and strategies.
> [Decision Trees](decision-trees.md#2-context-tier-selection) for tier selection flow.

## Quick Path (Structure JSON)

If `structure.json` exists (from wa-convert):

```python
structure = read("{book}/input-handling/structure.json")
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
* `overlap_from_prev`: Start line for ~10 lines overlap from previous chunk (None for first chunk)
* `word_count`: Actual word count (not estimate)
* `heading_path`: Hierarchical path like `["Chapter 1", "Section A"]`

**Skip manual chunking** when structure.json available.

## Context Tiers

> **Tier thresholds & strategies**: Xem [SKILL.md Step 2.2](../SKILL.md#22-determine-tier). Chi tiết workflow từng tier: [tier-direct-path.md](tier-direct-path.md), [tier-1-workflow.md](tier-1-workflow.md), [tier-2-workflow.md](tier-2-workflow.md), [tier-3-workflow.md](tier-3-workflow.md).

**Direct Path selection** (từ `structure.json`):

```
direct_path.eligible AND direct_path.capacity_ok?
├─ YES → DIRECT PATH (proceed)
├─ eligible BUT NOT capacity_ok → WARN, recommend Tier 1
└─ NOT eligible → Use tier_recommendation.tier
```

## Tier 3 Fast Path

For documents >=100K words, reduce main agent overhead by ~40%.

### What to Skip

| Standard Step | Fast Path Action |
|---------------|------------------|
| Analysis artifacts | SKIP - use `structure.json` outline |
| `_glossary.md` | SKIP - embed ~300 words inline |
| Article dependencies | SKIP - embed 1-2 sentences per article |
| Context files | SKIP - not needed for Tier 3 |
| Context extractors | SKIP - not needed for Tier 3 |

### What to Create

1. **Minimal `_plan.md`** - Section→article mapping only:

```markdown
# Article Plan
Source: content.md (111K words)

| # | Slug | Outline Indices | Lines | Chunks |
|---|------|-----------------|-------|--------|
| 0 | overview | - | - | - |
| 1 | intro | 0-2 | 1-258 | 0 |
| 2 | core | 3-5 | 259-574 | 1 |
```

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

def split_article(article, detail_ratio=0.35):
    source_words = sum(s.word_count for s in article.sections)
    estimated = source_words * detail_ratio

    if estimated <= MAX_OUTPUT:
        return [article]  # No split needed

    h2_blocks = extract_h2_blocks(article.sections)

    parts = []
    current = {'blocks': [], 'words': 0}

    for block in h2_blocks:
        block_output = block.word_count * detail_ratio

        if current['words'] + block_output > MAX_OUTPUT:
            if current['blocks']:
                parts.append(current)
                current = {'blocks': [], 'words': 0}

        current['blocks'].append(block)
        current['words'] += block_output

    if current['blocks']:
        parts.append(current)

    return parts
```

### Validation

| Check | Pass Condition |
|-------|----------------|
| No overlap | Each line in exactly 1 part |
| No miss | All source lines covered |
| Critical intact | [Sxx]* 100% in single part |

### Part Naming Convention

| Original | Split Parts |
|----------|-------------|
| `02-core.md` | `02-core-part1.md`, `02-core-part2.md`, `02-core-part3.md` |
| `03-advanced.md` | `03-advanced-part1.md`, `03-advanced-part2.md` |
