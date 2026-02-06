# Context File Template

> **Applies to Tier 2 only (50K-100K words)**. Tier 1 and Tier 3 skip context files entirely — subagents read source directly via line ranges.

## Compact Format

Use this compact format for `XX-{slug}-context.md`:

```markdown
# {Article Title}
TIER:2 | LINES:{start}-{end} | WORDS:{count} | CRIT:{S02,S05}

## Sections
[S01] Title (L{x}-{y})
[S02]* Core Argument (L{x}-{y}) ← verbatim required
[S03] Supporting (L{x}-{y})

## Terms
Term1: definition (~20 words)
Term2: definition

## Nav
Prev: [00-overview](./00-overview.md)
Next: [02-core](./02-core.md)

## Content

### [S01] {Title}
{Verbatim text}

### [S02]* {Critical Title}
{FULL verbatim text - never summarize}

### [S03] {Title} [SUMMARIZED]
Key points:
- Point 1
- Point 2
Full content: content.md L200-350
```

**Context savings**: ~20% vs verbose format

## Format Rules

| Element | Format | Example |
|---------|--------|---------|
| Header | Single line metadata | `TIER:2 \| LINES:1-500 \| WORDS:8500` |
| Critical | Asterisk suffix | `[S02]*` |
| Lines | Compact | `L1-50` not `lines 1-50` |
| Terms | Inline, no table | `Term: definition` |
| Nav | Minimal | `Prev: [title](path)` |

## Tier 2 Content Handling

- Critical sections `*`: FULL verbatim — never summarize
- Other sections: Summarize to ~30% length
- Add `[SUMMARIZED]` tag for non-verbatim sections
- Include `Full: content.md L{start}-{end}` reference for summarized sections

## Content Rules

1. **COPY verbatim** for `*` sections — no paraphrasing
2. **PRESERVE** formatting (code blocks, lists, emphasis)
3. **COMPRESS** non-critical via summary
4. **SKIP** boilerplate, repeated content

## Subagent Return Format

```
EXTRACTED: S01,S02,S03
WORDS: ~1700
ISSUES: none
NEW_TERMS: term_x (suggest add to glossary)
```
