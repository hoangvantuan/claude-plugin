# Tier 1 Workflow (20K-50K words, fails Direct Path)

> **GUARD**: Tier đã xác định là Tier 1 từ Step 2.6. Nếu chưa → **STOP, quay lại SKILL.md Step 2.6**.

## Step 3: Analyze

### 3.0 Processing Path Confirmation

Read `structure.json` → verify `tier_recommendation.tier == 1` hoặc document fails Direct Path conditions.

### 3.1 Structure Scan

> **📖 READ FIRST**: [context-optimization.md](context-optimization.md) — anti-patterns that waste 50%+ context budget.

**Quick path** (if `structure.json` exists):
- **ONLY** read `structure.json` for outline, stats, tier recommendation
- **DO NOT** read `content.md` — wastes context budget
- Skip manual scanning

⚠️ **CRITICAL**: Do NOT read full `content.md` during structure scan! Subagents read source directly when writing.

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

**Content-Type Detection**: `content_type` per article (`tutorial`, `conceptual`, `narrative`, `analysis`, `mixed`). Embed `CONTENT_TYPE: {type}` in subagent prompt.

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
- Validate: `{SCRIPTS_DIR}/wa-validate-split docs/generated/{book}/analysis/_plan.md`

### 3.4 Shared Context (Inline Glossary)

Tier 1: inline glossary ~200 words embed trong prompt. Article dependencies: 1-2 sentences inline.

### 3.6 Quality Gate: Analysis Complete

- [ ] All sections have IDs
- [ ] Critical sections marked (<=30% typical, >50% → auto-escalate Tier 3)
- [ ] Article plan covers 100% sections

## Step 4: Write Articles

### 4.0a Pre-read Voice & Structure (BẮT BUỘC)

```python
voice_content = Read(f"{VOICES_DIR}/{voice}-compact.md")
structure_content = Read(f"{STRUCTURES_DIR}/{structure}-compact.md")
# Embed vào prompt, subagent KHÔNG tự đọc files
```

### 4.0b Subagent Context Budget Rules

1. **CONTEXT RULES** — embed in prompt, cấm subagent glob/read files thừa
2. **run_in_background: true** — dùng cho ≥3 articles
3. **Summary files (.done)** — subagent ghi `{outputPath}.done`, main agent đọc `.done`

```python
tasks = []
for article in articles:
    task = Task(
        subagent_type="general-purpose",
        description=f"Write: {article.title}",
        run_in_background=True,
        prompt=compose_prompt(article, voice_content, structure_content)
    )
    tasks.append(task)
```

### 4.0b.1 Result Collection Protocol (BẮT BUỘC)

```python
Bash("ls articles/*.done")           # Check completion
Read("articles/01-intro.md.done")    # Read summary (~200 bytes)
Bash("wc -w articles/01-intro.md")   # Validate word count
# KHÔNG dùng TaskOutput hay tail .output files
```

### 4.0c State Tracking

Create/update `analysis/_state.json` for resume support. See [retry-workflow.md](retry-workflow.md).

### 4.1 Overview Article (Phase 1)

Write `00-overview.md` in main context. Template: `templates/overview-template.md`. Target: 300-400 words.

### 4.2 Content Articles (Tier 1 — Standard Path)

Spawn subagents using **Tier 1 template** from [article-writer-prompt.md](article-writer-prompt.md#standard-template---tier-1-variant-inline-glossary).

```
Task tool:
- subagent_type: "general-purpose"
- description: "Write: {title}"
- run_in_background: true
- prompt: [Use Tier 1 template with {voiceContent}, {structureContent} from 4.0a]
```

### 4.3 SoT Pattern (Long Articles)

Use Skeleton-of-Thought when: output >2000 words AND >=5 subsections. See [article-writer-prompt.md#sot-pattern](article-writer-prompt.md#sot-pattern-long-articles-2000-words).

### 4.4 Coverage Tracking

Subagent returns inline coverage: `COVERAGE: S01:ok S02*:faithful S03:ok`
Main agent enriches to 4-column. See [§5.2](steps-5-6-synthesize-verify.md#52-coverage-aggregation).

### 4.5 Critical Sections

⭐ sections MUST be faithfully rewritten (100% meaning, Vietnamese, voice persona, KHÔNG tóm tắt).

### 4.6 Quality Gate: Articles Complete

Verify từ `.done` files:
- [ ] All articles written (`.done` files vs pending list)
- [ ] All RESULT: PASS
- [ ] KEY_TAKEAWAY collected for Step 5.1

**Continuous Batching**: max_concurrent = 3, on completion → spawn next immediately.

**Load [steps-5-6-synthesize-verify.md](steps-5-6-synthesize-verify.md) for Steps 5-6.**
