# Performance Benchmarks

Measured performance improvements for writer-agent optimizations.

## Methodology

**Test Setup**:

* Model: Claude Sonnet 4.5

* Measurement: Wall-clock time from input to final verification

* Token tracking: Via API usage metrics (input + output tokens)

* Baseline: v1.9.x workflow (before optimizations)

* Test runs: 3 iterations, median reported

**Baseline Workflow (v1.9.x)**:

```
Input → Convert → Analyze (read content.md) → Extract context →
Write (static batching) → Synthesize → Verify
```

## Test Cases

### Test Case 1: Small Document (Tier 1)

* **Source**: Technical blog post, 15,842 words

* **Articles**: 4 articles planned

* **Tier**: 1 (<50K words)

* **Style**: Professional

| Metric            | Baseline (v1.9.x) | Direct Path (v1.10.0) | Improvement      |
| ----------------- | ----------------- | --------------------- | ---------------- |
| Total time        | 4m 23s            | 3m 5s                 | **29.6% faster** |
| Main agent tokens | 68K               | 34K                   | 50% reduction    |
| Subagent count    | 4                 | 0 (main writes all)   | -4 spawns        |

**Optimizations applied**: Direct Path (<20K words), inline glossary

***

### Test Case 2: Medium Document (Tier 1)

* **Source**: Research paper, 34,889 words

* **Articles**: 6 articles planned

* **Tier**: 1 (<50K words)

* **Style**: Explanatory

| Metric             | Baseline (v1.9.x)     | Optimized (v1.10.0) | Improvement      |
| ------------------ | --------------------- | ------------------- | ---------------- |
| Total time         | 12m 45s               | 9m 18s              | **27.1% faster** |
| Main agent tokens  | 69K                   | 34K                 | 50.7% reduction  |
| Context files      | 6 files (~20K words)  | 0 (inline glossary) | Eliminated       |
| Article write time | 8m 12s (static batch) | 6m 5s (continuous)  | **26% faster**   |

**Optimizations applied**:

* Skip context extraction (read source directly)

* Inline glossary (\~200 words)

* Continuous batching (max\_concurrent=3)

***

### Test Case 3: Medium-Large Document (Tier 2)

* **Source**: Technical book chapter, 67,234 words

* **Articles**: 8 articles planned

* **Tier**: 2 (50K-100K words)

* **Style**: Contemplative

| Metric             | Baseline (v1.9.x)   | Optimized (v1.10.0) | Improvement      |
| ------------------ | ------------------- | ------------------- | ---------------- |
| Total time         | 22m 38s             | 17m 52s             | **21.0% faster** |
| Main agent tokens  | 82K                 | 76K                 | 7.3% reduction   |
| Context extraction | Sequential (6m 15s) | Batched (4m 42s)    | 24.8% faster     |
| Article write time | 13m 20s (static)    | 9m 55s (continuous) | **25.6% faster** |

**Optimizations applied**:

* Continuous batching (max\_concurrent=3)

* Smart context compression (critical sections verbatim, others summarized)

**Note**: Tier 2 still uses context files due to document size (50K-100K). Context savings smaller than Tier 1.

***

### Test Case 4: Large Document (Tier 3)

* **Source**: Full technical book, 142,567 words

* **Articles**: 12 articles planned

* **Tier**: 3 (>=100K words)

* **Style**: Introspective Narrative

| Metric            | Baseline (v1.9.x)     | Fast Path (v1.10.0)       | Improvement         |
| ----------------- | --------------------- | ------------------------- | ------------------- |
| Total time        | 38m 52s               | 23m 15s                   | **40.2% faster**    |
| Main agent tokens | 125K                  | 72K                       | **42.4% reduction** |
| Context files     | 12 files (~57K words) | 0 (inline glossary)       | Eliminated          |
| Article batching  | Static (3 batches)    | Continuous (2 concurrent) | 35% faster          |
| Analysis overhead | 9m 30s                | 3m 45s                    | 60.5% faster        |

**Optimizations applied**:

* Fast Path (skip inventory, glossary files, relationships)

* Minimal `_plan.md` (section mapping only)

* Inline glossary (\~300 words)

* Continuous batching (max\_concurrent=2, larger chunks)

* Subagents read source directly via `suggested_chunks`

***

### Test Case 5: SoT Pattern (Long Article)

* **Source section**: 8,450 words → single article

* **Expected output**: \~2,800 words (comprehensive detail level)

* **Tier**: 2

| Metric            | Standard Approach    | SoT Pattern                           | Improvement      |
| ----------------- | -------------------- | ------------------------------------- | ---------------- |
| Total time        | 3m 42s               | 1m 55s                                | **48.2% faster** |
| Phases            | 1 (monolithic write) | 3 (outline → parallel expand → merge) | 2x faster        |
| Parallel sections | 1                    | 5 (expanded concurrently)             | 5x parallelism   |

**When to use**: Articles with expected output >2000 words AND source section has >=5 sub-sections.

***

## Summary Table

| Optimization            | Applies To                 | Typical Speedup | Context Savings  | Methodology        |
| ----------------------- | -------------------------- | --------------- | ---------------- | ------------------ |
| **Direct Path**         | <20K words OR <=3 articles | 25-30%          | 50% (main agent) | Test Case 1        |
| **Inline Glossary**     | Tier 1 (<50K)              | 10-15%          | 10-15%           | Test Case 2        |
| **Skip Context Files**  | Tier 1 + Tier 3            | 15-25%          | 20-40%           | Test Cases 2, 4    |
| **Continuous Batching** | All multi-article          | 25-35%          | 0% (time only)   | Test Cases 2, 3, 4 |
| **SoT Pattern**         | Articles >2000 words       | 45-50%          | 0% (time only)   | Test Case 5        |
| **Tier 3 Fast Path**    | >=100K words               | 35-45%          | 40-45%           | Test Case 4        |

## Notes on Variance

### Understanding Ranges vs Reproducibility

**Two types of variance:**

1. **Performance range** (e.g., "25-35%"): Expected variation across DIFFERENT document types

   * Same optimization applied to different documents → different improvement rates

   * Example: Direct Path gives 29.6% speedup for 15K doc, but 27.1% for 34K doc

2. **Reproducibility variance** (±5%): Variation when testing SAME document multiple times

   * Same document, same optimization, different runs → ±5% variation

   * Caused by API response times, network latency, system load

**Why performance ranges exist:**

* **Document structure**: Well-structured docs (clear H2/H3) → higher end of range (30-35%)

  * Easier chunking, better parallelization, cleaner boundaries

* **Article count**: More articles → better continuous batching gains

  * 2 articles: minimal batching benefit (\~25%)

  * 12 articles: maximum batching efficiency (\~35%)

* **Style complexity**: Professional/Casual styles faster than Introspective Narrative

  * Simpler voice = faster generation

  * Narrative styles require more creative processing

* **Content type**:

  * Text-only: Higher end of range (faster)

  * Code-heavy: Lower end (slower, preserving formatting)

  * Tables/diagrams: Mid-range (structured but complex)

### Factors NOT measured

* Network latency (varies by location, time of day)

* API rate limits (can throttle concurrent requests unpredictably)

* Model variance (different model versions may have different speeds)

## Reproducing Benchmarks

To verify these numbers:

1. **Prepare test document** matching tier thresholds (15K, 35K, 67K, 142K words)
2. **Run baseline**: Disable optimizations in SKILL.md (revert to v1.9.x)
3. **Run optimized**: Enable all applicable optimizations for tier
4. **Measure**:

   * Wall-clock time: `time uv run python ...`

   * Tokens: Check API usage in logs
5. **Calculate**: `(baseline - optimized) / baseline × 100%`

**Expected variance**: ±5% due to API response times
