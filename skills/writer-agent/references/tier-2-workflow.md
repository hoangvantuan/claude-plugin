# Tier 2 Workflow (50K-100K words)

> **GUARD**: Tier đã xác định là Tier 2 từ Step 2.6. Nếu chưa → **STOP, quay lại SKILL.md Step 2.6**.

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

**Content-Type Detection**: `content_type` per article. Embed `CONTENT_TYPE: {type}` in subagent prompt.

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
- Template: `templates/context-file-template.md`
- Prompt: [context-extractor-prompt.md](context-extractor-prompt.md)
- Output: `analysis/XX-{slug}-context.md`

See [large-doc-processing.md](large-doc-processing.md) for context extraction strategy.

### 3.6 Quality Gate: Analysis Complete

- [ ] All sections have IDs
- [ ] Critical sections marked (>50% → auto-escalate Tier 3)
- [ ] Article plan covers 100% sections
- [ ] Context files created for all articles
- [ ] `_glossary.md` generated

## Step 4: Write Articles

### 4.0a Pre-read Voice & Structure (BẮT BUỘC)

```python
voice_content = Read(f"{VOICES_DIR}/{voice}-compact.md")
structure_content = Read(f"{STRUCTURES_DIR}/{structure}-compact.md")
```

### 4.0b Subagent Context Budget Rules

1. **CONTEXT RULES** — embed in prompt
2. **run_in_background: true** — cho ≥3 articles
3. **Summary files (.done)** — subagent ghi `{outputPath}.done`

### 4.0b.1 Result Collection Protocol (BẮT BUỘC)

```python
Bash("ls articles/*.done")
Read("articles/01-intro.md.done")
# KHÔNG dùng TaskOutput hay tail .output files
```

### 4.0c State Tracking

Create/update `analysis/_state.json`. See [retry-workflow.md](retry-workflow.md).

### 4.1 Overview Article (Phase 1)

Write `00-overview.md` in main context. Template: `templates/overview-template.md`. Target: 300-400 words.

### 4.2 Content Articles (Tier 2 — Context Files)

Spawn subagents using **Tier 2 template** from [article-writer-prompt.md](article-writer-prompt.md#standard-template---tier-2-variant-context-files).

```
Task tool:
- subagent_type: "general-purpose"
- description: "Write: {title}"
- run_in_background: true
- prompt: [Use Tier 2 template with contextFilePath, glossaryFilePath, {voiceContent}, {structureContent}]
```

### 4.3 SoT Pattern (Long Articles)

When output >2000 words AND >=5 subsections. See [article-writer-prompt.md#sot-pattern](article-writer-prompt.md#sot-pattern-long-articles-2000-words).

### 4.4 Coverage Tracking

Subagent returns inline: `COVERAGE: S01:ok S02*:faithful S03:ok`
Main agent enriches to 4-column.

### 4.5 Critical Sections

⭐ sections MUST be faithfully rewritten (100% meaning, Vietnamese, voice persona).

### 4.6 Quality Gate: Articles Complete

Verify từ `.done` files:
- [ ] All articles written
- [ ] All RESULT: PASS
- [ ] KEY_TAKEAWAY collected for Step 5.1

**Continuous Batching**: max_concurrent = 3.

**Load [steps-5-6-synthesize-verify.md](steps-5-6-synthesize-verify.md) for Steps 5-6.**
