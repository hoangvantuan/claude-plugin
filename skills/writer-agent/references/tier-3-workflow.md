# Tier 3 Workflow (>=100K words — Fast Path)

> **GUARD**: Tier đã xác định là Tier 3 từ Step 2.6. Nếu chưa → **STOP, quay lại SKILL.md Step 2.6**.

## Step 3: Analyze

### 3.0 Processing Path Confirmation

Read `structure.json` → verify `tier_recommendation.tier == 3`.

### 3.1 Structure Scan

> **📖 READ FIRST**: [context-optimization.md](context-optimization.md)

**Quick path**: ONLY read `structure.json`. DO NOT read `content.md`.

### 3.1.1 Tier 3 Fast Path

Minimize analysis overhead:

| Action | Detail                                                           |
| ------ | ---------------------------------------------------------------- |
| SKIP   | `_glossary.md`, context files                                    |
| CREATE | Minimal `_plan.md` (section-to-article mapping + line ranges)    |
| EMBED  | Key terms (~300 words) + dependencies inline in subagent prompts |
| SPAWN  | Subagents immediately after `_plan.md` (continuous batching)     |

**Context savings**: ~40% reduction in main agent context.

See [large-doc-processing.md#tier-3-fast-path](large-doc-processing.md#tier-3-fast-path) for `_plan.md` format.

### 3.2 Content Inventory

Use `structure.json` outline directly.

### 3.3 Article Plan (`analysis/_plan.md`)

Minimal plan: section-to-article mapping + line ranges. Target 3-7 articles.

**Series Context** (tạo cùng lúc):

```markdown
## Series Context
Core message: "{1-2 câu thông điệp cốt lõi}"
| # | Title | Role | Opening | Reader Enters | Reader Exits | Transformation Moment | Misconception | Bridge to Next |
```

**Opening Diversity Rule**: KHÔNG 2 bài liên tiếp dùng cùng opening technique.

### 3.4 Shared Context (Inline Glossary)

Tier 3: inline glossary ~300 words (larger than T1 due to bigger documents). Embed in prompt.

### 3.6 Quality Gate: Analysis Complete

- [ ] All sections have IDs
- [ ] Critical sections marked
- [ ] `_plan.md` created with line ranges
- [ ] Article plan covers 100% sections

## Step 4: Write Articles

> **📖 Shared steps 4.0a-4.0c, 4.1, 4.3-4.6**: See [shared-article-writing.md](shared-article-writing.md). Below is Tier 3-specific content only.

### 4.2 Content Articles (Tier 3 — Fast Path)

Spawn subagents using **Tier 3 Compact template** from [article-writer-prompt.md](article-writer-prompt.md#tier-3-compact-template-100k-words).

```
Task tool:
- subagent_type: "general-purpose"
- description: "Write: {title}"
- run_in_background: true
- prompt: [Use Tier 3 Compact template with {voiceContent}, {structureContent}, inlineGlossary ~300 words]
```

**Continuous Batching**: max_concurrent = 2 (larger chunks ~10K words). Dynamic: >8K → 2, <2K → 5.
