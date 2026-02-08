# Context Extractor Subagent Prompt

> **Tier 3 (>=100K words)**: SKIP this step entirely.
> Subagents read source directly via line ranges. See [large-doc-processing.md](large-doc-processing.md#tier-3-fast-path).

> **Direct Path (<20K words)**: SKIP this step.
> Main agent writes articles directly without context extraction.

## When to Use

```
word_count >= 50,000 AND word_count < 100,000?
├─ YES → Use context extractors (Tier 2 only)
└─ NO → Skip
    ├─ <50K: Tier 1 or Direct Path (subagents read source directly)
    └─ >=100K: Tier 3 Fast Path (subagents read source directly)
```

## Compact Template (Tier 2 only)

> **Note**: Tier 1 skips context extraction entirely. Subagents read source directly via line ranges. This template applies to Tier 2 (50K-100K words) only.

```
Task tool:
- subagent_type: "general-purpose"
- description: "Extract: {article_title}"
- prompt: |
    TASK: Create context file for article #{article_number} "{title}"

    SOURCE: {source_path} L{start}-{end}
    OUTPUT: {context_file_path}

    SECTIONS: {section_ids}

    TERMS (embed in output):
    {inline_glossary}

    NAV:
    - Prev: {prev_article}
    - Next: {next_article}

    FORMAT:
    # {title}
    TIER:{tier} | LINES:{start}-{end} | WORDS:{count} | CRIT:{critical_ids}

    ## Sections
    [S01] Title (L{x}-{y})
    [S02]* Critical (L{x}-{y})

    ## Terms
    Term1: definition
    Term2: definition

    ## Nav
    Prev: [{prev}](./{prev}.md)
    Next: [{next}](./{next}.md)

    ## Content
    ### [S01] {Title}
    {Verbatim text}

    ### [S02]* {Critical}
    {FULL verbatim - never summarize}

    RULES:
    - COPY verbatim, no paraphrasing
    - PRESERVE formatting (code, lists, emphasis)
    - [Sxx]* = FULL text, never summarize
    - Mark critical with asterisk

    RETURN:
    EXTRACTED: S01,S02,S03
    WORDS: ~{N}
    ISSUES: {any problems}
    NEW_TERMS: {terms not in glossary}
```

## Tier-Specific Handling

> **Note**: Only Tier 2 uses context extraction. Tier 1 and Tier 3 subagents read source directly via line ranges.

### Tier 2 (50K-100K words)
- Critical `*` sections: FULL verbatim
- Other sections: Summarize to ~30%
- Add `[SUMMARIZED]` tag

```markdown
### [S03] Supporting [SUMMARIZED]
Key points:
- Point 1
- Point 2
Full: content.md L200-350
```

## Parallel Execution (Continuous Batching)

```python
max_concurrent = 3
pending = [context_files...]

while pending:
    # Fill slots
    while running < max_concurrent and pending:
        spawn(pending.pop(0))

    # On any complete → spawn next immediately
    completed = wait_any()
    if pending:
        spawn(pending.pop(0))
```

## Variable Reference

| Variable | Source |
|----------|--------|
| `{context_file_path}` | `analysis/XX-{slug}-context.md` |
| `{source_path}` | `input-handling/content.md` |
| `{start}`, `{end}` | From `_plan.md` or `structure.json` |
| `{section_ids}` | From `structure.json` |
| `{inline_glossary}` | ~200 words initial key terms (input to extractor; extractor outputs comprehensive `_glossary.md` ~600 words) |

## Error Handling

| Error | Action |
|-------|--------|
| Source not found | Report, don't create empty |
| Context overflow | Apply Tier 2 summarization |
| New terms found | Report in return message |
| Missing sections | Report gap to main agent |

## Return Format

```
EXTRACTED: S01,S02,S03
WORDS: ~1700
ISSUES: none
NEW_TERMS: term_x (suggest add)
```
