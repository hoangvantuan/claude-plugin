# Direct Path Workflow (<20K words OR <50K AND ≤3 articles)

> **GUARD**: Tier đã xác định là Direct Path từ Step 2.6. Nếu chưa → **STOP, quay lại SKILL.md Step 2.6**.

Main agent writes ALL articles directly — không spawn subagents.

## Step 3: Analyze

### 3.0 Processing Path Confirmation

Read `structure.json` → verify `direct_path.eligible == true AND direct_path.capacity_ok == true`.

```
structure.json → direct_path.eligible?
├─ YES AND capacity_ok → DIRECT PATH (proceed)
├─ YES BUT NOT capacity_ok → WARN, recommend Tier 1
└─ NO → STOP, load tier-1 or tier-2 or tier-3 workflow instead
```

### 3.3 Article Plan (`analysis/_plan.md`)

**Check user request first:**

```python
if user_specified_article_count:
    target_articles = user_specified_count
    skip_auto_split = True
else:
    target_articles = calculate_optimal_articles(total_words, detail_ratio)
    skip_auto_split = False
```

Group sections into articles (default 3-7, or user-specified count):

```markdown
| #   | Slug  | Title         | Sections      | Est. Words | Reading Time |
| --- | ----- | ------------- | ------------- | ---------- | ------------ |
| 1   | intro | Introduction  | S01, S02      | 2000       | ~13 min      |
| 2   | core  | Core Concepts | S03, S04, S05 | 2500       | ~13-15 min   |
```

**Rules**: All sections mapped. Target reading time per detail level. Target 2000-3000 words/bài (tham khảo).

**Content-Type Detection**: Xác định `content_type` cho mỗi article (`tutorial`, `conceptual`, `narrative`, `analysis`, `mixed`).

**Series Context** (tạo cùng lúc với plan):

```markdown
## Series Context

Core message: "{1-2 câu thông điệp cốt lõi}"

| # | Title | Role | Opening | Reader Enters | Reader Exits | Transformation Moment | Misconception | Bridge to Next |
| 1 | Intro | foundation | scene-setting | Chưa biết X | Hiểu X cơ bản | "Aha: X không phải Y" | "Nghĩ X là Z" | "Nhưng X trong thực tế...?" |
```

**Opening Diversity Rule**: KHÔNG 2 bài liên tiếp dùng cùng opening technique. Dùng ít nhất ceil(N/2) techniques khác nhau.

### 3.4 Shared Context (Inline Glossary)

Direct Path: inline glossary ~200 words, embed trực tiếp khi viết.

### 3.6 Quality Gate: Analysis Complete

- [ ] All sections have IDs (from structure.json)
- [ ] Critical sections marked
- [ ] Article plan covers 100% sections

## Step 4: Write Articles (Main Agent)

### 4.1 Overview Article (Phase 1)

Write `00-overview.md`:
- Template: `templates/overview-template.md`
- Target: 300-400 words (initial)
- Include placeholders for Key Takeaways and Article Index

### 4.2 Content Articles (Direct Path)

Main agent writes all articles directly:
- Đọc voice file + structure file
- Đọc source content.md trực tiếp (full hoặc theo line ranges từ structure.json)
- Apply tất cả shared rules: WRITING_RULES, ANTI-AI WRITING
- KHÔNG cần return format (vì không có subagent)
- Viết từng article theo `_plan.md`, save vào `articles/XX-{slug}.md`
- Mỗi article MUST end with "## Các bài viết trong series"

### 4.4 Coverage Tracking

Main agent tự tạo `_coverage.md` sau khi viết xong tất cả.

**IMPORTANT**: PASS/FAIL chỉ dựa trên section coverage, không phải word count.

**Load [steps-5-6-synthesize-verify.md](steps-5-6-synthesize-verify.md) for Steps 5-6.**
