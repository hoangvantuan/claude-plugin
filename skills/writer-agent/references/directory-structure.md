# Directory Structure

Standard directory structure for writer-agent output.

## Project Layout

```
docs/generated/{book-name}/
├── input-handling/              # Step 1: Input processing
│   ├── content.md               # Converted markdown source
│   └── structure.json           # Document structure analysis
│
├── analysis/                    # Step 3: Analysis artifacts
│   ├── _inventory.md            # Section registry (Optional Tier 1-2, consider using structure.json directly)
│   ├── _plan.md                 # Article grouping plan
│   ├── _glossary.md             # Shared terminology (Tier 2 only)
│   ├── _coverage.md             # Aggregated coverage report
│   ├── _state.json              # Resume state (recommended for retry support)
│   ├── 01-{slug}-context.md     # Context file (Tier 2 only)
│   └── 02-{slug}-context.md     # Context file (Tier 2 only)
│
└── articles/                    # Step 4-5: Generated articles
    ├── 00-overview.md           # Series entry point
    ├── 01-{slug}.md             # Article 1
    ├── 02-{slug}.md             # Article 2
    └── ...
```

## Tier-Specific Files

| File | Tier 1 (<50K) | Tier 2 (50K-100K) | Tier 3 (>=100K) |
|------|:---:|:---:|:---:|
| `_plan.md` | Required | Required | Required (minimal) |
| `_inventory.md` | Optional | Optional | Skip (use structure.json) |
| `_glossary.md` | Skip (inline) | Required | Skip (inline) |
| Context files | Skip | Required | Skip |
| `_coverage.md` | Required | Required | Required |

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
Base: docs/generated/{book-name}/

Input:      {base}/input-handling/content.md
Structure:  {base}/input-handling/structure.json
Analysis:   {base}/analysis/
Articles:   {base}/articles/
Overview:   {base}/articles/00-overview.md
```
