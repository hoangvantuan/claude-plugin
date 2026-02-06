# Glossary Template

## Usage by Tier

| Tier | Format | Word Budget |
|------|--------|-------------|
| Direct Path | Inline in main agent context | ~200 words |
| Tier 1 (<50K) | Inline in subagent prompts | ~200 words |
| Tier 2 (50K-100K) | Separate `_glossary.md` file | ~300-600 words |
| Tier 3 (>=100K) | Inline in subagent prompts | ~300 words |

## Inline Format (Tier 1, 3, Direct Path)

Embedded directly in subagent prompts:

```markdown
TERMS:
Term1: Brief definition (~20 words)
Term2: Brief definition
Term3: Brief definition
```

## Separate File Format (Tier 2 only)

File: `analysis/_glossary.md`

```markdown
# Glossary

Source: {source_path}
Generated: {timestamp}

## Key Terms

Term1: Brief definition (~20-30 words)
Term2: Brief definition
Term3: Brief definition

## Language Notes

- **Original terms to keep**: {list Hán-Việt terms, technical jargon}
- **Translation approach**: {how to handle foreign terms}
```

## Guidelines

1. Max 10-15 key terms for inline, up to 25 for separate file
2. Each definition ~20-30 words max
3. Prioritize: foundational concepts > technical terms > examples
4. Preserve original terminology (Hán-Việt, technical jargon)
5. Use consistent term names across all articles
