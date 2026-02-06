# Retry Workflow (v1.13.0 - Relaxed)

Quy trình retry được đơn giản hóa để tiết kiệm token và thời gian.

## Nguyên tắc mới (v1.13.0)

**QUAN TRỌNG**: Không tự động retry. Mọi retry đều do user yêu cầu.

```
Lý do thay đổi:
- Retry tự động tốn nhiều token (mỗi lần = 1 subagent spawn)
- Coverage 90-95% thường đủ tốt, không cần đạt 98%
- User có quyền quyết định trade-off giữa quality và cost
```

## State Tracking (Đơn giản hóa)

```json
{
  "version": "1.1",
  "status": "in_progress",
  "current_step": 4,
  "completed_articles": ["00-overview.md", "01-introduction.md"],
  "pending_articles": ["02-core-concepts.md", "03-advanced.md"],
  "warnings": ["02-core-concepts: skip S05 (no reason)"]
}
```

**Lưu ý**: Không còn `retries` tracking vì không retry tự động.

## Retry Policy (User-Driven)

| Situation           | Action                    | Auto-retry? |
| ------------------- | ------------------------- | ----------- |
| Subagent timeout    | Report to user            | ❌ NO       |
| Coverage 90-94%     | Log warning, continue     | ❌ NO       |
| Coverage < 90%      | Ask user what to do       | ❌ NO       |
| Style mismatch      | Report, user decides      | ❌ NO       |
| Content fabrication | Flag for user review      | ❌ NO       |

## Coverage Recovery Procedure (User-Driven)

### Step 1: Collect và Report

Sau khi tất cả articles hoàn thành, tổng hợp coverage:

```
=== COVERAGE SUMMARY ===
Total sections: 12
Sections covered: 11
Sections skipped: 1 (S06)
Coverage: 91.7%

Warnings:
- S06 skipped in 02-core.md (reason: "too long")

Result: WARNING (90-95% range)
```

### Step 2: Report to User (Không tự động retry)

```
Báo cáo cho user:
"Coverage đạt 91.7% (11/12 sections).
Section S06 bị skip với lý do 'too long'.

Bạn muốn:
1. Accept as-is (recommended - 91.7% là đủ tốt)
2. Retry article 02-core.md để include S06
3. Tạo supplementary article cho S06"
```

### Step 3: Execute User Decision (Nếu user yêu cầu retry)

CHỈ KHI user chọn retry:

```
Task tool call:
- subagent_type: "general-purpose"
- description: "Retry article: {title}"
- prompt: |
    RETRY (user requested): Include missing section.

    ## Missing Section
    - [S06] Section Title - SUMMARIZE, do NOT skip

    ## Instructions
    1. Read source: {sourcePath} L{start}-{end}
    2. Focus on section [S06]
    3. Integrate naturally into article

    [Standard article writer prompt...]
```

### Step 4: Finalize

```
IF user chose "Accept as-is":
    → Mark complete with current coverage
    → Log: "Accepted 91.7% coverage per user decision"

IF user requested retry AND retry successful:
    → Update coverage
    → Mark complete

IF user requested supplementary:
    → Create supplementary article
    → Update overview
```

## Supplementary Article Creation

When retries exhausted but content important:

```markdown
# Supplementary: {Topic}

This article covers additional content from the source document.

## Sections Covered
- [S06] {Section Title}
- [S12] {Section Title}

## Content

{Extract content from context files}
```

Add to overview's Article Index (Mục lục):

```markdown
| S | [Supplementary: {Topic}](./supplementary-{slug}.md) | Additional coverage |
```

## Timeout Recovery (User-Driven)

### Subagent Timeout Detection

Task tool returns with timeout indicator:

```
Subagent timed out after 120 seconds.
Partial output saved to: {output_path}
```

### Recovery Steps

1. **Check partial output và Report**:

   ```
   Read {output_path}
   IF has meaningful content (>50% expected):
       → Save partial as draft
       → Report: "Article {title} timeout với ~{percent}% content"
   ELSE:
       → Report: "Article {title} timeout, no usable content"
   ```

2. **Ask user** (không tự động retry):

   ```
   "Article '{title}' bị timeout.

   Bạn muốn:
   1. Accept partial content (nếu có)
   2. Retry article này
   3. Skip article này"
   ```

3. **Execute user decision**:
   - Nếu retry → spawn lại với shorter timeout hoặc smaller chunk
   - Nếu accept partial → mark as complete với warning
   - Nếu skip → log và continue

## State Persistence

> **Note**: `_state.json` is **recommended** (required for retry and resume support). Without it, recovery from failures requires re-running from the beginning. See [SKILL.md Step 4.0](../SKILL.md#40-state-tracking-recommended).

### Save State After Each Step

```python
def save_state(step, articles_done, articles_pending, retries):
    state = {
        "version": "1.0",
        "status": "in_progress",
        "current_step": step,
        "timestamp": datetime.now().isoformat(),
        "completed_articles": articles_done,
        "pending_articles": articles_pending,
        "retries": retries
    }
    write("analysis/_state.json", json.dumps(state))
```

### Resume From State

```python
def resume_from_state():
    state = read("analysis/_state.json")

    if state["status"] == "completed":
        print("Already completed")
        return

    # Resume from last step
    step = state["current_step"]
    pending = state["pending_articles"]

    if step == 4:  # Article writing
        for article in pending:
            spawn_article_writer(article)
    elif step == 5:  # Synthesis
        run_synthesis()
    elif step == 6:  # Verify
        run_verification()
```

## Direct Path Recovery

When the main agent fails during Direct Path (no subagents):

```
Main agent fails during article writing?
├─ Check _state.json for progress
│   └─ IF _state.json exists:
│       └─ Resume from last completed article
│       └─ Re-write only pending articles
│   └─ ELSE:
│       └─ Re-run from Step 4 (all articles)
│
├─ Main agent context overflow?
│   └─ Switch to Tier 1 (use subagents instead)
│   └─ Reuse existing _plan.md and structure.json
│
└─ Partial article written?
    └─ Save as draft
    └─ Resume from last H2 heading boundary
```

**Important**: Direct Path has no subagent retry mechanism. Recovery relies on `_state.json` for tracking progress. This is why state tracking is **recommended** (not optional).

## User Decision Points

Các điểm cần user quyết định (không còn "escalation" vì không có auto-retry):

### Coverage < 90%

```
AskUserQuestion:
  question: "Coverage đạt {coverage}%. Bạn muốn làm gì?"
  options:
    - label: "Accept as-is"
      description: "Tiếp tục với {coverage}% (recommended nếu >85%)"
    - label: "Retry specific articles"
      description: "Chọn articles để retry"
    - label: "Create supplementary"
      description: "Tạo bài bổ sung cho sections bị skip"
```

### Timeout

```
AskUserQuestion:
  question: "Article '{title}' bị timeout. Bạn muốn làm gì?"
  options:
    - label: "Retry"
      description: "Thử lại article này"
    - label: "Accept partial"
      description: "Giữ phần đã viết được"
    - label: "Skip"
      description: "Bỏ qua article này"
```

## Selective Re-run

When `_state.json` exists AND user requests partial changes (style change, single article rewrite, content correction):

### Prerequisites

- `analysis/_state.json` exists with `status: "completed"`
- `analysis/structure.json`, `_plan.md`, context files all present
- Previous run completed successfully

### Scope Detection

| Request | Scope | Reuse |
|---------|-------|-------|
| Change style | ALL articles | structure.json, _plan.md |
| Rewrite 1 article | Single article | All analysis artifacts |
| Content correction | Affected article(s) | All analysis artifacts |

### Workflow

1. **Identify scope**: Which articles need regeneration?
2. **Reuse artifacts**: Keep structure.json, _plan.md, _inventory.md, context files
3. **Update state**:
   - Set `status: "in_progress"`
   - Move target articles from `completed_articles` to `pending_articles`
   - Preserve retry counts for unchanged articles
4. **Execute**: Spawn subagent(s) for target article(s) only
5. **Always re-run**: Synthesis (Step 5) and Verification (Step 6)
6. **Collect coverage**: Update `_coverage.md` with new results

### State Update Example

```json
{
  "status": "in_progress",
  "current_step": 4,
  "completed_articles": ["00-overview.md", "01-intro.md"],
  "pending_articles": ["02-core.md"],
  "selective_rerun": true,
  "rerun_reason": "style_change"
}
```

