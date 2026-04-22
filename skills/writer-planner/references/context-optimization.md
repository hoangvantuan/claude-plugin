# Context Optimization Guide

> **📖 Tier Definitions**: See [SKILL.md Step 2.2](../SKILL.md#22-determine-tier) for canonical tier thresholds and strategies.

## Problem: Unnecessary content.md Reads

### Common Mistake

```
Step 3.1: Structure Scan
├─ Read structure.json (~1.3K words)      ✅
└─ Read content.md (~24K words)           ❌ WASTE!
    └─ Loses 94% of context on duplicate data
```

**Why this is wrong:**
- `structure.json` already contains ALL structural information
- `content.md` sẽ được đọc sau ở giai đoạn viết bài (theo line ranges)
- Reading both wastes 90%+ of context budget

### Correct Workflow

```
Step 3.1: Structure Scan
└─ ONLY read structure.json
    ├─ Extract outline (section titles, line ranges)
    ├─ Extract stats (word_count, heading_count)
    └─ Determine tier recommendation

Step 3.2-3.3: Planning
└─ Use data from structure.json
    └─ NO content.md read needed!

Giai đoạn viết bài (sau planning):
└─ Đọc content.md theo line ranges cụ thể từ _plan.md
    └─ Mỗi article chỉ đọc phần source liên quan
```

## Context Budget Comparison

### Example: 34,889-word document (Tier 1)

| Approach | Structure Scan | Planning | Article Writing | Total |
|----------|---------------|----------|-----------------|-------|
| ❌ **Wrong** | 37K (json + content) | 2K | 5K × 6 articles = 30K | **69K** |
| ✅ **Correct** | 2K (json only) | 2K | 5K × 6 articles = 30K | **34K** |

**Savings: 51% reduction in main agent context usage**

## What structure.json Contains

```json
{
  "stats": {
    "word_count": 34889,
    "heading_count": 82,
    "critical_count": 24,
    "estimated_articles": 6
  },
  "tier_recommendation": {
    "tier": 1,
    "reason": "Word count 34,889 < 50,000"
  },
  "direct_path": {
    "eligible": true,
    "capacity_ok": true,
    "capacity_limit": 38000,
    "warning": null
  },
  "outline": [
    {
      "level": 2,
      "text": "Section Title",
      "line": 3,              // ← Start line
      "line_end": 34,         // ← End line
      "word_count": 1571,
      "critical": true
    }
  ],
  "suggested_chunks": [...]   // For Tier 3
}
```

This is **SUFFICIENT** for:
- Determining tier
- Creating section registry (from structure.json)
- Creating _plan.md
- Planning article structure

## When to Read content.md

### ✅ CORRECT Times to Read

1. **Step 3.4 (Post-Planning)**: Extract inline glossary
   - **Only for Tier 1 (<50K) OR Tier 3 (>=100K)**
   - Tier 2 uses separate `_glossary.md` file created by context extractors
   - Execute AFTER completing Steps 3.1-3.3 planning
   - **Algorithm**: See "Glossary Extraction Algorithm" below
2. **Giai đoạn viết bài**: Đọc theo line ranges từ _plan.md
3. **Debug**: If structure.json is missing/corrupted

## Glossary Extraction Algorithm (Step 3.4)

**Input**: content.md first 300-500 lines (or until first major section ends)
**Output**:
- Tier 1: ~200 words total
- Tier 3: ~300 words total

**Process**:
```python
1. Read content.md (offset=1, limit=500)
   # Stop early if hit first H1 boundary after 300 lines

2. Extract terms using patterns:
   - Definition patterns: "X là", "X is", "X: ", "X - "
   - Bold/italic terms: **term**, *term*
   - First mention in parentheses: "term (definition)"
   - Technical terms in code blocks or tables

3. For each term found:
   - Keep definition to ~20 words max
   - Prioritize: foundational concepts > technical terms > examples

4. Score terms by importance:
   score = (frequency × 2) + (1 / position_weight)
   # Earlier terms weighted higher

5. Sort by score, take top N until hitting word budget:
   - Tier 1: ~200 words (10-12 terms)
   - Tier 3: ~300 words (15-18 terms)
   - Note: Word budget varies by language (use get_max_words):
     EN ~44K max, VI ~32K max, mixed ~38K max words

6. Format output:
   Term1: Brief definition (~20 words)
   Term2: Brief definition
   ...
```

**Example output** (Tier 1, ~200 words):
```markdown
Agent: An autonomous software component that can make decisions and take actions
Context window: The amount of text an LLM can process at once
Tier: Processing strategy based on document size
Critical section: Content that must preserve 100% meaning in output
Coverage: Percentage of source sections represented in output
```

**Validation (Relaxed - v1.13.0)**:
- Count words in generated glossary
- IF > target × 1.5: Trim to most important terms
- IF < target × 0.5: Accept as-is (đủ dùng)
- KHÔNG expand search thêm (tốn context)

**Lưu ý**: Glossary chỉ là reference, không cần chính xác. Ít terms vẫn OK.

### ❌ NEVER Read During

1. **Step 3.1**: Structure scan (use structure.json)
2. **Step 3.2**: Inventory creation (use outline from JSON)
3. **Step 3.3**: Planning (use outline from JSON)

**Step 3 Timeline** (visual clarification):
```
Step 3: Analyze
├─ 3.1: Structure Scan (read structure.json ONLY) ❌ NO content.md
├─ 3.2: Inventory (use outline from structure.json) ❌ NO content.md
├─ 3.3: Plan (use outline from structure.json) ❌ NO content.md
├─ [CHECKPOINT: Planning complete, outline ready]
├─ 3.4: Glossary Extraction (NOW read first chunk) ✅ Read content.md lines 1-500
├─ 3.5: Context Files (Tier 2 only)
└─ 3.6: Quality Gate
```

**Timing rule**: Steps 3.1-3.3 use structure.json exclusively. Step 3.4 (post-planning) is when first content.md read occurs for glossary extraction.

## Validation Checklist

- [ ] `structure.json` was read
- [ ] `content.md` was NOT read during Steps 3.1-3.3
- [ ] `_plan.md` created using outline from JSON
- [ ] Line ranges in plan match `structure.json` outline
- [ ] `content.md` first read at Step 3.4 (glossary extraction)

> **📖** Tier-specific context strategies: See [SKILL.md §2.2](../SKILL.md#22-determine-tier) and [tier-2-workflow.md §3.5](tier-2-workflow.md#35-context-files-tier-2-only).
