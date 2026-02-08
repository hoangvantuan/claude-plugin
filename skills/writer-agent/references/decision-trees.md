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

⚠️ **IMPORTANT**: At this step, ONLY read `structure.json`. Do NOT read `content.md` - it will be read later by subagents via line ranges.

```
Check structure.json → direct_path + tier_recommendation (pre-computed by wa-convert v1.2+)

# STEP 1: Check Direct Path first (uses pre-computed fields)
direct_path.eligible?
├─ YES AND direct_path.capacity_ok?
│   └─ DIRECT PATH
│       └─ Main agent writes all articles
│       └─ Skip to Step 4 (Write Articles)
│
├─ YES BUT NOT direct_path.capacity_ok?
│   └─ WARN: direct_path.warning
│   └─ RECOMMEND: Proceed to Tier 1 instead
│
└─ NO → STEP 2: Use tier_recommendation.tier

tier == 1 (< 50K)?
├─ YES → Tier 1: Lightweight
│   └─ Skip context files, skip _glossary.md
│   └─ Subagents read source directly via line ranges
│   └─ Embed inline glossary (~200 words) in prompts
│   └─ ⚠️ Main agent does NOT read content.md during analysis
│
├─ tier == 2 (50K-100K)?
│   └─ Tier 2: Smart Compression
│       ├─ * Critical sections → Full source in context file (article writer faithful rewrites)
│       └─ Supporting sections → Summarize
│       └─ Create context files + _glossary.md
│       └─ RECOMMEND: Use subagents
│
└─ tier == 3 (>= 100K)?
    └─ Tier 3: Reference-Based → USE FAST PATH
        ├─ SKIP: _glossary.md, context files
        ├─ CREATE: minimal _plan.md only
        ├─ Subagents read source DIRECTLY via line ranges
        └─ See large-doc-processing.md#tier-3-fast-path
```

## 3. Context Extraction Strategy (UPDATED v1.11.0)

```
Starting Step 3.5 (Context Files)

# Use pre-computed direct_path from structure.json (v1.2+)
direct_path.eligible AND direct_path.capacity_ok?
├─ YES → DIRECT PATH (skip context extraction)
│   └─ Main agent writes ALL articles directly
│   └─ Embed inline glossary in each article prompt
│   └─ ~30% faster for small documents
│
├─ direct_path.eligible BUT NOT capacity_ok?
│   └─ WARN: direct_path.warning
│   └─ Proceed to Tier 1 instead
│
└─ NO → Check tier_recommendation.tier
    tier == 1 (< 50K) OR tier == 3 (>= 100K)?
    ├─ YES → SKIP context files
    │   └─ Subagents read source directly via line ranges
    │   └─ Embed inline glossary (~200 words Tier 1, ~300 words Tier 3) in prompts
    │   └─ Tier 1: ~20% faster than context extraction
    │   └─ Tier 3: ~40% context savings
    │
    └─ NO (Tier 2: 50K-100K) → Spawn context extractor subagents
        ├─ Create _glossary.md (shared file)
        ├─ Batch size: min(3, article_count)
        └─ Use references/context-extractor-prompt.md
```

**Examples:**
- 15K words, 5 articles → Direct Path (structure.json: eligible=true, capacity_ok=true) ✓
- 45K words, 3 articles → Direct Path for EN (capacity_ok=true), Warning for VI (capacity_ok=false) ⚠️
- 48K words, 3 articles → Warning (exceeds mixed limit 38K) → Recommend Tier 1 ⚠️
- 45K words, 4 articles → Standard Path (eligible=false → Tier 1, skip context files)

**v1.10.0 change**: Tier 1 documents (20K-50K) now skip context files. Subagents read source directly via line ranges with inline glossary, same as Tier 3. Only Tier 2 (50K-100K) uses context extraction.

**v1.11.0 change**: Direct Path eligibility and capacity limits now pre-computed in structure.json (`direct_path` field). Main agent no longer needs to calculate these manually.

## 3.1 Tier 3 Fast Path Workflow

```
Tier 3 detected (>=100K words)

Step 1: Minimal Analysis
├─ Read structure.json
├─ Read first chunk (~300 lines) for key terms
├─ Create minimal _plan.md (mapping only)
└─ SKIP: _glossary.md, context files

Step 2: Write Overview
└─ Main agent writes 00-overview.md

Step 3: Spawn Article Writers (Continuous Batching)
├─ max_concurrent = 2  # Tier 3: Larger chunks (~10K words) → limit to 2
├─ Spawn immediately when slot available
├─ On complete → spawn next (no batch waiting)
├─ Each subagent receives:
│   ├─ Source path + line range (from suggested_chunks)
│   ├─ Style file path
│   ├─ Key terms inline (~300 words)
│   └─ Article dependencies (1-2 sentences)
└─ Subagent: Read source → Write article → Return coverage

Step 4: Synthesize & Verify
├─ Collect coverage reports
├─ Update overview (Key Takeaways + Article Index)
└─ Report coverage (target >=95%, accept >=90%)
```

## 4. Article Writing Strategy

```
Starting Step 4 (Write Articles)

Overview article (00-overview.md)?
├─ YES → Write in MAIN context
│   └─ Needs full series knowledge
│   └─ Template: templates/_overview-template.md
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

## 6. Skip Validation (Relaxed - v1.13.0)

```
Subagent reports skipped section [Sxx]

QUAN TRỌNG: Không tự động retry. Chỉ ghi nhận và tiếp tục.

Check skip reason (for logging only):
├─ "Redundant" with specific [Syy] reference?
│   └─ VALID → Log và tiếp tục
│
├─ "Off-topic" for this article?
│   └─ VALID → Log và tiếp tục
│
├─ "User instruction" to skip?
│   └─ VALID → Log và tiếp tục
│
├─ "Too long"?
│   └─ WARNING → Log "consider summarizing"
│   └─ KHÔNG retry tự động
│
├─ "Already covered" without [Sxx] reference?
│   └─ WARNING → Log "missing reference"
│   └─ KHÔNG retry tự động
│
└─ No reason provided?
    └─ WARNING → Log "no reason"
    └─ KHÔNG retry tự động

Tổng hợp tất cả warnings → Báo cáo cuối cùng cho user
User quyết định có cần retry hay không
```

## 7. Coverage Resolution (Relaxed - v1.13.0)

```
Step 6: Verify coverage

QUAN TRỌNG: Không tự động retry. Báo cáo kết quả và để user quyết định.

coverage >= 95%?
├─ YES → PASS → Hoàn thành
│
├─ 90-94%?
│   └─ WARNING → Báo cáo cho user
│   └─ KHÔNG tự động retry
│   └─ Tiếp tục hoàn thành workflow
│
└─ < 90%?
    └─ ASK USER (chỉ khi thực sự thấp)
        ├─ Option 1: Accept as-is (recommended nếu >85%)
        ├─ Option 2: Retry specific articles (user chọn)
        └─ Option 3: Create supplementary article

LƯU Ý:
- KHÔNG có retry tự động
- KHÔNG có retry_count tracking
- User có toàn quyền quyết định
- Mục tiêu: tiết kiệm token và thời gian
```

## 8. Error Recovery (User-Driven - v1.13.0)

```
Error occurred during subagent execution

QUAN TRỌNG: Không tự động retry. Log và report cho user.

Error type?
├─ Subagent timeout
│   └─ Log: "Article {X} timeout"
│   └─ Save partial output (nếu có)
│   └─ Continue với các articles khác
│   └─ Report cho user ở cuối
│
├─ Missing output file
│   └─ Log: "Article {X} no output"
│   └─ Continue với các articles khác
│   └─ Report cho user ở cuối
│
├─ Style mismatch
│   └─ Log: "Article {X} style mismatch"
│   └─ Accept as-is (style không critical)
│   └─ Note trong report
│
├─ Content fabrication detected
│   └─ Log: "Article {X} possible fabrication"
│   └─ Flag cho user review
│   └─ KHÔNG tự động retry
│
└─ Context overflow
    └─ Log: "Context overflow, switching to higher tier"
    └─ Tự động switch (không cần user confirm)
    └─ Re-chunk và continue

Sau khi tất cả articles xong:
└─ Tổng hợp errors và warnings
└─ Report cho user
└─ User quyết định actions (nếu cần)
```

## 9. Inline Glossary Strategy

> See [SKILL.md §3.4](../SKILL.md#34-shared-context-inline-glossary) for full glossary strategy by tier and [context-optimization.md](context-optimization.md#glossary-extraction-algorithm-step-34) for extraction algorithm.
