# Directory Structure

Standard directory structure for writer-planner output.

## Project Layout

```
writer-planner/{book-name}/
├── input-handling/              # Step 1: Input processing
│   ├── content.md               # Converted markdown source
│   └── structure.json           # Document structure analysis
│
├── analysis/                    # Step 3: Analysis artifacts
│   ├── _plan.md                 # Article grouping plan
│   ├── _glossary.md             # Shared terminology (Tier 2 only)
│   └── XX-{slug}-context.md     # Context files (Tier 2 only)
│
└── articles/                    # Created by writer-executor
    ├── 00-overview.md
    └── XX-{slug}.md
```

## Tier-Specific Files

| File | Tier 1 (<50K) | Tier 2 (50K-100K) | Tier 3 (>=100K) |
|------|:---:|:---:|:---:|
| `_plan.md` | Required | Required | Required (minimal) |
| `_glossary.md` | Skip (inline) | Required | Skip (inline) |
| Context files | Skip | Required | Skip |

## File Naming Conventions

| Type | Pattern | Example |
|------|---------|---------|
| Context file | `XX-{slug}-context.md` | `01-introduction-context.md` |
| Article | `XX-{slug}.md` | `01-introduction.md` |

## Variable Reference

| Variable | Source | Example |
|----------|--------|---------|
| `{book-name}` | From title slug + timestamp | `managing-to-learn-250127-1430` |
| `{slug}` | From article title | `core-concepts` |
| `XX` | Zero-padded number | `01`, `02`, `10` |

## Path Resolution

```
Base: writer-planner/{book-name}/

Input:      {base}/input-handling/content.md
Structure:  {base}/input-handling/structure.json
Analysis:   {base}/analysis/
Articles:   {base}/articles/
Overview:   {base}/articles/00-overview.md
```
