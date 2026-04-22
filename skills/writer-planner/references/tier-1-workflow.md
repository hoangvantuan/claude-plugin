# Tier 1 Workflow (20K-50K words, fails Direct Path)

> **GUARD**: Tier đã xác định là Tier 1 từ Step 2.2. Nếu chưa → **STOP, quay lại SKILL.md Step 2.2**.

## Step 3: Analyze

### 3.0 Processing Path Confirmation

Read `structure.json` → verify `tier_recommendation.tier == 1` hoặc document fails Direct Path conditions.

### 3.1 Structure Scan

> **📖 READ FIRST**: [context-optimization.md](context-optimization.md) — anti-patterns that waste 50%+ context budget.

**Quick path** (if `structure.json` exists):
- **ONLY** read `structure.json` for outline, stats, tier recommendation
- **DO NOT** read `content.md` — wastes context budget
- Skip manual scanning

⚠️ **CRITICAL**: Do NOT read full `content.md` during structure scan!

### 3.2 Content Inventory

Use `structure.json` outline directly. Section IDs, line ranges, word counts, critical markers all available.

### 3.3 Article Plan (`analysis/_plan.md`)

```python
if user_specified_article_count:
    target_articles = user_specified_count
    skip_auto_split = True
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

**Opening Diversity Rule**: KHÔNG 2 bài liên tiếp dùng cùng opening technique. Dùng ít nhất ceil(N/2) techniques khác nhau.

### 3.3.1 Article Splitting (Auto)

**Priority**: User-specified count → tuân theo, KHÔNG auto-split. Auto-split chỉ khi user KHÔNG specify.

- `MAX_OUTPUT_WORDS = 3000`, `TARGET_PART_WORDS = 2000`
- Atomic unit = H2 block. NEVER split within paragraph/H3/critical section.

### 3.4 Shared Context (Inline Glossary)

Tier 1: inline glossary ~200 words. Article dependencies: 1-2 sentences.

### 3.6 Quality Gate: Analysis Complete

- [ ] All sections have IDs
- [ ] Critical sections marked (<=30% typical, >50% → auto-escalate Tier 3)
- [ ] Article plan covers 100% sections



