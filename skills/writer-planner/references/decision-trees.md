# Decision Trees

Quick reference for workflow decisions.

> **📖 Tier Definitions**: See [SKILL.md Step 2.2](../SKILL.md#22-determine-tier) for canonical tier table.

## 1. Input Type Detection

```
Input received
├─ Starts with "http://" or "https://"?
│   └─ YES → URL input → Run wa-convert
├─ Has file extension (.pdf, .docx, .xlsx, .pptx, .html)?
│   └─ YES → File input → Run wa-convert
├─ Has extension .txt or .md?
│   └─ YES → Plain text file → Read file → Rewrite → Run wa-paste-text
└─ NO extension (pasted text)?
    └─ Plain text → Rewrite → Run wa-paste-text
```

## 2. Context Tier Selection

> **📖 Tier Thresholds**: See [SKILL.md Step 2.2](../SKILL.md#22-determine-tier) for canonical word count ranges.

⚠️ **IMPORTANT**: At this step, ONLY read `structure.json`. Do NOT read `content.md`.

```
Check structure.json → direct_path + tier_recommendation (pre-computed by wa-convert v1.2+)

direct_path.eligible?
├─ YES AND capacity_ok? → DIRECT PATH (proceed)
├─ YES BUT NOT capacity_ok? → WARN → Proceed to Tier 1
└─ NO → Use tier_recommendation.tier
    ├─ Tier 1 → Skip context files, inline glossary (~200 words)
    ├─ Tier 2 → Context files + _glossary.md
    └─ Tier 3 → FAST PATH, skip context files, inline glossary (~300 words)
```

## 3. Context Extraction Strategy (UPDATED v1.11.0)

> **📖 Direct Path & Tier details**: See [tier-direct-path.md](tier-direct-path.md#step-3-analyze) and tier workflow files

```
Starting Step 3.5 (Context Files)

Direct Path eligible + capacity_ok? → SKIP context extraction
Tier 1 or Tier 3? → SKIP context files (inline glossary only)
Tier 2? → Spawn context extractors
  ├─ Create _glossary.md (shared file)
  └─ Batch size: min(3, article_count)
```

## 3.1 Tier 3 Fast Path Workflow

> **📖 Full details**: See [large-doc-processing.md](large-doc-processing.md#tier-3-fast-path)

```
Tier 3 detected (>=100K words)

1. Minimal Analysis: structure.json + first ~300 lines → minimal _plan.md
2. Inline glossary ~300 words
```

## 4. Inline Glossary Strategy

> See tier workflow files for glossary strategy by tier (Tier 1: inline ~200 words, Tier 2: `_glossary.md` ~600 words, Tier 3: inline ~300 words) and [context-optimization.md](context-optimization.md#glossary-extraction-algorithm-step-34) for extraction algorithm.

