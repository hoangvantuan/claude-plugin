# Decision Trees

Quick reference for workflow decisions.

> **📖 Tier Definitions**: See [SKILL.md Step 2.6](../SKILL.md#step-26-tier-reference-table) for canonical tier table with word count thresholds, strategies, and parameters.

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

> **📖 Tier Thresholds**: See [SKILL.md Step 2.6](../SKILL.md#step-26-tier-reference-table) for canonical word count ranges.

⚠️ **IMPORTANT**: At this step, ONLY read `structure.json`. Do NOT read `content.md`.

```
Check structure.json → direct_path + tier_recommendation (pre-computed by wa-convert v1.2+)

direct_path.eligible?
├─ YES AND capacity_ok? → DIRECT PATH (main agent writes all, skip to Step 4)
├─ YES BUT NOT capacity_ok? → WARN → Proceed to Tier 1
└─ NO → Use tier_recommendation.tier
    ├─ Tier 1 → Skip context files, inline glossary (~200 words), subagents read source via line ranges
    ├─ Tier 2 → Context files + _glossary.md, smart compression
    └─ Tier 3 → FAST PATH, skip context files, inline glossary (~300 words), subagents read source via line ranges
```

## 3. Context Extraction Strategy (UPDATED v1.11.0)

> **📖 Direct Path & Tier details**: See [tier-direct-path.md](tier-direct-path.md#step-3-analyze) and tier workflow files

```
Starting Step 3.5 (Context Files)

Direct Path eligible + capacity_ok? → SKIP context extraction (main agent writes all)
Tier 1 or Tier 3? → SKIP context files (subagents read source directly + inline glossary)
Tier 2? → Spawn context extractors (see references/context-extractor-prompt.md)
  ├─ Create _glossary.md (shared file)
  └─ Batch size: min(3, article_count)
```

## 3.1 Tier 3 Fast Path Workflow

> **📖 Full details**: See [large-doc-processing.md](large-doc-processing.md#tier-3-fast-path)

```
Tier 3 detected (>=100K words)

1. Minimal Analysis: structure.json + first ~300 lines → minimal _plan.md
2. Write Overview: 00-overview.md
3. Spawn writers: max_concurrent=2, continuous batching, inline glossary
4. Synthesize & Verify
```

## 4. Article Writing Strategy

```
Starting Step 4 (Write Articles)

Overview article (00-overview.md)?
├─ YES → Write in MAIN context
│   └─ Needs full series knowledge
│   └─ Template: templates/overview-template.md
│
└─ NO → Estimate article length
    estimated_words = (source_words × detail_ratio) / article_count

    estimated_words > 2000 AND total_subsections >= 5?
    ├─ YES → Use SoT Pattern
    │   ├─ "total_subsections" = H3 headings (priority) OR H2 if no H3 OR paragraph breaks
    │   ├─ Algorithm: if h3_count >= 5 → use SoT
    │   │            elif h3_count == 0 → check h2_count >= 5
    │   │            else → h3 + h2 >= 5
    │   ├─ Phase 1: Generate skeleton
    │   ├─ Phase 2: Expand sections in parallel (spawn all)
    │   ├─ Phase 3: Merge + add transitions
    │   └─ See article-writer-prompt.md#sot-pattern
    │   └─ Benefits: 45-50% faster vs monolithic write
    │   └─ Example 1: S01(3 H3) + S02(4 H3) = 7 H3 total ✓
    │   └─ Example 2: S03(8K words, 7 H2, 0 H3) → fallback to H2 count ✓
    │
    └─ NO → Standard subagent
        ├─ Use references/article-writer-prompt.md
        └─ Continuous batching (max 3 concurrent for Tier 1-2)
```

## 5. Parallel Execution (Continuous Batching)

```
Ready to spawn subagents?

CONTINUOUS BATCHING (preferred):
├─ Set max_concurrent:
│   ├─ Tier 1-2: max_concurrent = 3 (smaller chunks ~3.5K words)
│   └─ Tier 3: max_concurrent = 2 (larger chunks ~10K words, avoid memory pressure)
├─ Spawn articles immediately up to max_concurrent
├─ On ANY completion:
│   ├─ Collect coverage report
│   ├─ If pending articles remain → spawn next immediately
│   └─ Continue until all done
└─ Benefits: ~25-40% faster than static batching

STATIC BATCHING (legacy, avoid):
├─ Spawn batch of N articles
├─ Wait for ALL to complete
├─ Spawn next batch
└─ Wastes time waiting for slowest

SEQUENTIAL (only when required):
├─ Content dependencies between articles
├─ System resource constraints
└─ Spawn 1 at a time
```

## 6. Skip Validation (Relaxed)

> **Policy**: User-driven retry only. See [retry-workflow.md](retry-workflow.md).

```
Subagent reports skipped section [Sxx]

Check skip reason (for logging only):
├─ "Redundant" with specific [Syy] reference?
│   └─ VALID → Log và tiếp tục
├─ "Off-topic" for this article?
│   └─ VALID → Log và tiếp tục
├─ "User instruction" to skip?
│   └─ VALID → Log và tiếp tục
├─ "Too long" / "Already covered" without ref / No reason?
│   └─ WARNING → Log

Tổng hợp tất cả warnings → Báo cáo cuối cùng cho user
```

## 7. Coverage Resolution (Relaxed)

```
coverage >= 95%?
├─ YES → PASS → Hoàn thành
├─ 90-94%?
│   └─ WARNING → Báo cáo cho user → Tiếp tục hoàn thành workflow
└─ < 90%?
    └─ ASK USER:
        ├─ Option 1: Accept as-is (recommended nếu >85%)
        ├─ Option 2: Retry specific articles (user chọn)
        └─ Option 3: Create supplementary article
```

## 8. Error Recovery (User-Driven)

```
Error type?
├─ Subagent timeout → Log, save partial, continue, report cuối
├─ Missing output file → Log, continue, report cuối
├─ Voice mismatch → Accept as-is, note trong report
├─ Content fabrication → Flag cho user review
└─ Context overflow → Tự động switch tier + re-chunk

Sau khi tất cả articles xong:
└─ Tổng hợp errors → Report cho user → User quyết định
```

## 9. Inline Glossary Strategy

> See tier workflow files for glossary strategy by tier (Tier 1: inline ~200 words, Tier 2: `_glossary.md` ~600 words, Tier 3: inline ~300 words) and [context-optimization.md](context-optimization.md#glossary-extraction-algorithm-step-34) for extraction algorithm.
