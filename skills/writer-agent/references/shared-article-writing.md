# Shared Article Writing Steps (Steps 4.0-4.6)

> Shared across Tier 1, Tier 2, and Tier 3 workflows. Each tier file imports this reference and only defines tier-specific differences.

## Step 4.0a: Pre-read Voice & Structure (BẮT BUỘC)

```python
voice_content = Read(f"{VOICES_DIR}/{voice}-compact.md")
structure_content = Read(f"{STRUCTURES_DIR}/{structure}-compact.md")
# Embed vào prompt, subagent KHÔNG tự đọc files
```

## Step 4.0b: Subagent Context Budget Rules

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

## Step 4.0b.1: Result Collection Protocol (BẮT BUỘC)

```python
Bash("ls articles/*.done")           # Check completion
Read("articles/01-intro.md.done")    # Read summary (~200 bytes)
Bash("wc -w articles/01-intro.md")   # Validate word count
# KHÔNG dùng TaskOutput hay tail .output files
```

## Step 4.0c: State Tracking

Create/update `analysis/_state.json` for resume support. See [retry-workflow.md](retry-workflow.md).

## Step 4.1: Overview Article (Phase 1)

Write `00-overview.md` in main context. Template: `templates/overview-template.md`. Target: 300-400 words.

## Step 4.3: SoT Pattern (Long Articles)

Use Skeleton-of-Thought when: output >2000 words AND >=5 subsections. See [article-writer-prompt.md#sot-pattern](article-writer-prompt.md#sot-pattern-long-articles-2000-words).

## Step 4.4: Coverage Tracking

Subagent returns inline coverage: `COVERAGE: S01:ok S02*:faithful S03:ok`
Main agent enriches to 4-column. See [steps-5-6-synthesize-verify.md §5.2](steps-5-6-synthesize-verify.md#52-coverage-aggregation).

## Step 4.5: Critical Sections

⭐ sections MUST be faithfully rewritten (100% meaning, Vietnamese, voice persona, KHÔNG tóm tắt).

## Step 4.6: Quality Gate: Articles Complete

Verify từ `.done` files:
- [ ] All articles written (`.done` files vs pending list)
- [ ] All RESULT: PASS
- [ ] KEY_TAKEAWAY collected for Step 5.1

**Load [steps-5-6-synthesize-verify.md](steps-5-6-synthesize-verify.md) for Steps 5-6.**
