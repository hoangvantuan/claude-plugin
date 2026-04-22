# Tier 2 Workflow (50K-100K words)

> **GUARD**: Tier đã xác định là Tier 2 từ Step 2.2. Nếu chưa → **STOP, quay lại SKILL.md Step 2.2**.

## Step 3: Analyze

### 3.0 Processing Path Confirmation

Read `structure.json` → verify `tier_recommendation.tier == 2`.

### 3.1 Structure Scan

> **📖 READ FIRST**: [context-optimization.md](context-optimization.md) — anti-patterns that waste 50%+ context budget.

**Quick path**: ONLY read `structure.json` for outline, stats, tier recommendation. DO NOT read `content.md`.

### 3.2 Content Inventory

Use `structure.json` outline directly.

### 3.3 Article Plan (`analysis/_plan.md`)

```python
if user_specified_article_count:
    target_articles = user_specified_count
else:
    target_articles = calculate_optimal_articles(total_words, detail_ratio)
```

Group sections into articles (default 3-7). Rules: all sections mapped, target 2000-3000 words/bài.

**Content-Type Detection**: Xác định `content_type` cho mỗi article (`tutorial`, `conceptual`, `narrative`, `analysis`, `mixed`).

**Series Context** (tạo cùng lúc với plan):

```markdown
## Series Context
Core message: "{1-2 câu thông điệp cốt lõi}"
| # | Title | Role | Opening | Reader Enters | Reader Exits | Transformation Moment | Misconception | Bridge to Next |
```

**Opening Diversity Rule**: KHÔNG 2 bài liên tiếp dùng cùng opening technique.

### 3.3.1 Article Splitting (Auto)

Same as Tier 1: `MAX_OUTPUT_WORDS = 3000`, `TARGET_PART_WORDS = 2000`. Atomic unit = H2 block.

### 3.4 Shared Context (Seed Glossary)

Tier 2: seed glossary → context extractors produce `_glossary.md` (~600 words separate file).

Chi tiết: [context-optimization.md#glossary-extraction-algorithm](context-optimization.md#glossary-extraction-algorithm-step-34).

### 3.5 Context Files (Tier 2 Only)

Spawn context extractor subagents: batch min(3, article_count).
- Output: `analysis/XX-{slug}-context.md`
- Critical `*` sections: FULL verbatim. Other sections: summarize to ~30%.

See [large-doc-processing.md](large-doc-processing.md) for context extraction strategy.

### 3.6 Quality Gate: Analysis Complete

- [ ] All sections have IDs
- [ ] Critical sections marked (>50% → auto-escalate Tier 3)
- [ ] Article plan covers 100% sections
- [ ] Context files created for all articles
- [ ] `_glossary.md` generated


