# Article Writer Subagent Prompt

## Quality Philosophy

Subagent không chỉ tóm tắt source material. Subagent phải **biến đổi** source thành bài viết engaging, có chiều sâu, có mạch logic riêng. Mỗi bài viết phải đứng độc lập như một bài hoàn chỉnh, đồng thời kết nối với series.

**Nguyên tắc cốt lõi:**
- **Narrative > Summary**: Viết bài có mạch kể, không phải liệt kê ý
- **Insight > Information**: Tạo connections giữa các ý, rút ra insight
- **Engagement > Coverage**: Một bài viết hay mà cover 90% tốt hơn bài nhàm chán cover 100%
- **Opening & Closing matter most**: Đầu tư nhiều nhất vào mở bài và kết bài

## Series Context Block

**QUAN TRỌNG**: Mỗi subagent prompt PHẢI include Series Context block để subagent hiểu vai trò bài viết trong toàn bộ series.

```
SERIES_CONTEXT:
  core_message: "{1-2 câu tóm tắt thông điệp cốt lõi của toàn bộ tài liệu}"
  article_role: "{Vai trò bài này trong series: mở đầu/nền tảng/phát triển/cao trào/kết luận}"
  prev_article: "{Tên bài trước} - {1 câu tóm tắt nội dung chính}"
  next_article: "{Tên bài sau} - {1 câu tóm tắt nội dung chính}"
  reader_journey: "{Đến bài này, người đọc đã hiểu X, bài này sẽ đưa họ đến Y}"
  reader_enters: "{Người đọc biết X nhưng chưa hiểu Y}"
  reader_exits: "{Người đọc hiểu Y và muốn biết Z}"
```

**Cách main agent tạo Series Context:**
1. Từ `_plan.md`, xác định article_role dựa trên vị trí trong series
2. core_message: trích từ thông điệp cốt lõi trong plan hoặc structure.json
3. prev/next: tóm tắt 1 câu từ article titles trong plan
4. reader_journey: mô tả progression logic
5. reader_enters: mô tả kiến thức người đọc có khi bắt đầu bài (từ bài trước)
6. reader_exits: mô tả kiến thức người đọc đạt được sau bài (dẫn tới bài sau)

## Shared Rules (Referenced by All Tier Templates)

All tier templates include these identical blocks. Defined once here to avoid duplication.

### LANGUAGE Block
```
LANGUAGE:
- Write ENTIRE article in Vietnamese — NO exceptions, including ⭐ critical sections
- Keep technical terms in English with Vietnamese explanation when first introduced
- Example: "user role modeling (mô hình hóa vai trò người dùng)"
- ALL prose, explanations, transitions MUST be in Vietnamese
- DO NOT keep any section in source's original language — everything must be rewritten in Vietnamese
```

### FORMATTING Block
```
FORMATTING (CRITICAL):
- NO markdown tables - convert to bullet lists
- NO diagrams (mermaid, ASCII art, flowcharts) - describe in prose or bullets
- Use bullet points for comparisons, lists, and structured data
```

### REWRITE RULE Block
```
REWRITE RULE (CRITICAL):
- MUST rewrite ALL content in YOUR voice following the output style — INCLUDING ⭐ critical sections
- DO NOT copy-paste sentences or paragraphs from source (no exceptions)
- Source = WHAT ideas to express, Style = HOW to express them
- Transform source ideas into the style's voice, structure, and language patterns
- ⭐ critical sections: faithful rewrite — giữ 100% ý nghĩa, KHÔNG tóm tắt, viết lại bằng tiếng Việt + style voice
- Non-critical sections: rewrite freely (có thể tóm tắt theo detail level)
- If a paragraph matches source word-for-word → FAIL (no exceptions)
```

### WRITING QUALITY Block
```
WRITING QUALITY (CRITICAL):
- Opening/Closing: Follow the style's Opening and Closing guidelines
- Narrative flow: Each section leads naturally to the next
- Depth over breadth: Go deep on 2-3 key ideas
- Draw connections: Link ideas to SERIES_CONTEXT.core_message
- BLACKLIST phrases: "Trong phần tiếp theo...", "Tóm lại,...", "Bài viết đã trình bày..."
```

### CONTENT PRIORITY Block
```
CONTENT PRIORITY:
- FIRST: Cover ALL ideas from source sections completely
- SECOND: Rewrite in output style voice (NOT copy source text)
- THIRD: Write naturally, word count is for statistics only
- If all sections covered AND rewritten in style → PASS
- DO NOT rewrite to hit word count targets
- Quality content coverage + style compliance > arbitrary word targets
```

### RETURN FORMAT Block
```
RETURN FORMAT (CRITICAL - Table format):
- Article content ALREADY saved to {outputPath}
- DO NOT return article content in message
- Return ONLY this summary:

DONE: {filename} | {N} words (stats)
COVERAGE (determines PASS/FAIL):
| Section | Status |
|---------|--------|
| S01 | ✅ {how_used} |
| S02 ⭐ | ✅ faithful |
RESULT: {PASS if all sections covered, FAIL if missing}
SERIES_LIST: {YES/NO}
VERIFY: "quote..." (L45), "quote..." (L128)
[Max 3 quotes, each ≤30 chars]
[Mark critical with ⭐, skipped with ⚠️]
```

## Tier 3 Compact Template (>=100K words)

Streamlined prompt for large documents (\~40% context reduction):

```
Task tool:
- subagent_type: "general-purpose"
- description: "Write: {title}"
- prompt: |
    TASK: Write "{title}" for {seriesTitle}

    SOURCE: {sourcePath} L{start}-{end}
    STYLE: .claude/skills/writer-agent/output_styles/{style}.md
    OUTPUT: {outputPath}

    TARGET: ~{target_words} words (reference only) | MODE: {detail_level}

    TERMS: {inlineGlossary}

    SERIES_CONTEXT:
      core_message: "{coreMessage}"
      article_role: "{articleRole}"
      prev_article: "{prevArticleSummary}"
      next_article: "{nextArticleSummary}"
      reader_journey: "{readerJourney}"
      reader_enters: "{readerEnters}"
      reader_exits: "{readerExits}"

    SERIES_LIST:
    {seriesList}

    [Include LANGUAGE block from Shared Rules above]
    [Include FORMATTING block from Shared Rules above]

    STRUCTURE:
    - Follow the Structure section in the output style file for article organization
    - If style has Opening/Development/Closing → use that pattern
    - If style has Scene/Encounter/Deepening/Transformation → use that pattern
    - MANDATORY constraints (override style):
      1. Title (H1) - descriptive, evocative
      2. Before "## Các bài viết trong series", add a brief narrative bridge (1-2 sentences)
         that creates natural curiosity for the next article.
         Format: A question, image, or thought connecting this article's conclusion to the next.
         DO NOT use: "Trong phần tiếp theo...", "Bài tiếp theo sẽ..."
      3. Must end with "## Các bài viết trong series" (mark current with _(đang xem)_)
    - The style's Structure section defines HOW to organize content
    - The source sections [Sxx] define WHAT content to include

    CONTENT_TYPE: {contentType}
    # Hint: Use this to adapt structure if the style's Structure section is generic.
    # tutorial → include practical steps/examples
    # conceptual → include thought experiments/frameworks
    # narrative → include scenes/character development
    # analysis → include evidence hierarchy/methodology

    [Include REWRITE RULE block from Shared Rules above]
    [Include WRITING QUALITY block from Shared Rules above]

    RULES:
    - Source ONLY, no fabrication
    - [Sxx]* sections = faithful rewrite (100% meaning, Vietnamese, style voice — KHÔNG tóm tắt)
    - Non-critical sections = MUST rewrite in style voice
    - MUST end with "## Các bài viết trong series" section (MANDATORY - article FAILS without this)
    - Mark current article with _(đang xem)_
    - Focus on content coverage, word count is reference only

    [Include CONTENT PRIORITY block from Shared Rules above]
    [Include RETURN FORMAT block from Shared Rules above]
```

## Standard Template - Tier 1 Variant (Inline Glossary)

For Tier 1 documents (<50K words) - subagents read source directly with inline glossary.

```
Task tool:
- subagent_type: "general-purpose"
- description: "Write: {title}"
- prompt: |
    TASK: Write article #{articleNumber} "{title}"

    SOURCE: {sourcePath} L{start}-{end}
    STYLE: .claude/skills/writer-agent/output_styles/{style}.md
    OUTPUT: {outputPath}

    TARGET: ~{target_words} words (reference only, source: {source_words} words)
    MODE: {detail_level}

    TERMS (Key Glossary):
    {inlineGlossary}

    DEPTH RULES ({detail_level}):
    - Critical [Sxx]*: {critical_handling}
    - Non-critical: {non_critical_handling}
    - Examples: Keep {example_percentage}%

    SERIES_CONTEXT:
      core_message: "{coreMessage}"
      article_role: "{articleRole}"
      prev_article: "{prevArticleSummary}"
      next_article: "{nextArticleSummary}"
      reader_journey: "{readerJourney}"
      reader_enters: "{readerEnters}"
      reader_exits: "{readerExits}"

    SERIES_LIST:
    {seriesList}

    [Include LANGUAGE block from Shared Rules above]
    [Include FORMATTING block from Shared Rules above]

    STRUCTURE:
    - Follow the Structure section in the output style file for article organization
    - If style has Opening/Development/Closing → use that pattern
    - If style has Scene/Encounter/Deepening/Transformation → use that pattern
    - MANDATORY constraints (override style):
      1. Title (H1) - descriptive, evocative
      2. Before "## Các bài viết trong series", add a brief narrative bridge (1-2 sentences)
         that creates natural curiosity for the next article.
         Format: A question, image, or thought connecting this article's conclusion to the next.
         DO NOT use: "Trong phần tiếp theo...", "Bài tiếp theo sẽ..."
      3. Must end with "## Các bài viết trong series" (mark current with _(đang xem)_)
    - The style's Structure section defines HOW to organize content
    - The source sections [Sxx] define WHAT content to include

    CONTENT_TYPE: {contentType}
    # Hint: Use this to adapt structure if the style's Structure section is generic.
    # tutorial → include practical steps/examples
    # conceptual → include thought experiments/frameworks
    # narrative → include scenes/character development
    # analysis → include evidence hierarchy/methodology

    [Include REWRITE RULE block from Shared Rules above]
    [Include WRITING QUALITY block from Shared Rules above]

    RULES:
    - Source content ONLY
    - [Sxx]* = faithful rewrite (100% meaning, Vietnamese, style voice — KHÔNG tóm tắt)
    - Non-critical sections = MUST rewrite in style voice
    - Preserve terminology
    - 100% reader-facing, no metadata in output
    - Focus on content coverage, word count is reference only
    - MUST end with "## Các bài viết trong series" (MANDATORY - article FAILS without this)

    [Include CONTENT PRIORITY block from Shared Rules above]
    [Include RETURN FORMAT block from Shared Rules above]
```

## Standard Template - Tier 2 Variant (Context Files)

For Tier 2 documents (50K-100K words) - subagents read compressed context files.

```
Task tool:
- subagent_type: "general-purpose"
- description: "Write: {title}"
- prompt: |
    TASK: Write article #{articleNumber} "{title}"

    READ:
    1. Context: {contextFilePath}
    2. Glossary: {glossaryFilePath}
    3. Style: .claude/skills/writer-agent/output_styles/{style}.md

    OUTPUT: {outputPath}

    TARGET: ~{target_words} words (reference only, source: {source_words} words)
    MODE: {detail_level}

    DEPTH RULES ({detail_level}):
    - Critical [Sxx]*: {critical_handling}
    - Non-critical: {non_critical_handling}
    - Examples: Keep {example_percentage}%

    SERIES_CONTEXT:
      core_message: "{coreMessage}"
      article_role: "{articleRole}"
      prev_article: "{prevArticleSummary}"
      next_article: "{nextArticleSummary}"
      reader_journey: "{readerJourney}"
      reader_enters: "{readerEnters}"
      reader_exits: "{readerExits}"

    SERIES_LIST:
    {seriesList}

    [Include LANGUAGE block from Shared Rules above]
    [Include FORMATTING block from Shared Rules above]

    STRUCTURE:
    - Follow the Structure section in the output style file for article organization
    - If style has Opening/Development/Closing → use that pattern
    - If style has Scene/Encounter/Deepening/Transformation → use that pattern
    - MANDATORY constraints (override style):
      1. Title (H1) - descriptive, evocative
      2. Before "## Các bài viết trong series", add a brief narrative bridge (1-2 sentences)
         that creates natural curiosity for the next article.
         Format: A question, image, or thought connecting this article's conclusion to the next.
         DO NOT use: "Trong phần tiếp theo...", "Bài tiếp theo sẽ..."
      3. Must end with "## Các bài viết trong series" (mark current with _(đang xem)_)
    - The style's Structure section defines HOW to organize content
    - The source sections [Sxx] define WHAT content to include

    CONTENT_TYPE: {contentType}
    # Hint: Use this to adapt structure if the style's Structure section is generic.
    # tutorial → include practical steps/examples
    # conceptual → include thought experiments/frameworks
    # narrative → include scenes/character development
    # analysis → include evidence hierarchy/methodology

    [Include REWRITE RULE block from Shared Rules above]
    [Include WRITING QUALITY block from Shared Rules above]

    RULES:
    - Source content ONLY
    - [Sxx]* = faithful rewrite (100% meaning, Vietnamese, style voice — KHÔNG tóm tắt)
    - Non-critical sections = MUST rewrite in style voice
    - Preserve terminology
    - 100% reader-facing, no metadata in output
    - Focus on content coverage, word count is reference only
    - MUST end with "## Các bài viết trong series" (MANDATORY - article FAILS without this)

    [Include CONTENT PRIORITY block from Shared Rules above]
    [Include RETURN FORMAT block from Shared Rules above]
```

### Detail Level Parameters

| Level         | critical\_handling                    | non\_critical\_handling  | example\_percentage | Target Reading Time |
| ------------- | ------------------------------------- | ------------------------ | ------------------- | ------------------- |
| Concise       | Full faithful rewrite (100% meaning)  | 1-2 sentences each       | 30%                 | \~5 min             |
| Standard      | Full faithful rewrite (100% meaning)  | Summarize + key examples | 60%                 | \~10 min            |
| Comprehensive | Full faithful rewrite (100% meaning)  | Most content             | 85%                 | \~13 min            |
| Faithful      | Full faithful rewrite (100% meaning)  | Full content             | 100%                | \~15 min            |

**Reading Time Targets (\~13-15 minutes per article):**

```python
MAX_OUTPUT_WORDS = 3000      # ~15 min for general content (200 wpm)
TARGET_PART_WORDS = 2000     # ~13 min for technical content (150 wpm)

# Formula: reading_time = word_count / words_per_minute
# Technical: 150 wpm | General: 200 wpm
```

## SoT Pattern (Long Articles >2000 words)

**When to use:** Articles with estimated output >2000 words AND total source content has >=5 subsections.

**Subsection definition** (priority order):

1. **Priority 1**: H3+ headings (if available)
2. **Priority 2**: H2 headings (if no H3 exists)
3. **Priority 3**: Major paragraph breaks (if flat structure) ⚠️ **NOT IMPLEMENTED**

**Algorithm**:

```python
h3_count = count_headings(sections, level=3)
if h3_count >= 5:
    use_sot = True
elif h3_count == 0:  # Flat structure (no H3)
    h2_count = count_headings(sections, level=2)
    use_sot = (h2_count >= 5)
    # NOTE: If H2=0 too, skip SoT (Priority 3 not implemented)
else:  # Mixed (some H3, but <5)
    total = h3_count + count_headings(sections, level=2)
    use_sot = (total >= 5)
    # NOTE: Simple additive count may not reflect true hierarchy
```

**Limitations:**

* Priority 3 (paragraph breaks) is not implemented. Documents with no headings will skip SoT.

* Mixed structure logic uses simple addition, which may not capture complexity of deeply nested hierarchies.

**Note:** "Total source content" = combined content from ALL sections (\[Sxx]) mapped to this article.

For articles meeting criteria, use Skeleton-of-Thought:

```
# Phase 1: Generate skeleton (spawn first)
Task:
- description: "Outline: {title}"
- prompt: |
    Generate H2/H3 outline for "{title}"
    Source: {contextPath} or {sourcePath} L{start}-{end}
    Return: Headers only, ~50 words

# Phase 2: Expand sections (spawn ALL in parallel)
Task[0]:
- description: "Write section: Introduction"
- prompt: |
    Write Introduction (~300 words) for "{title}"
    Context: {intro_content}
    Style: {style}.md

    LANGUAGE: Write in Vietnamese. Keep technical terms in English with Vietnamese explanation.

    Return: markdown content only

Task[1]:
- description: "Write section: {H2_title}"
- prompt: |
    Write "{H2_title}" (~{word_target} words)
    Context: {section_content}
    Style: {style}.md

    REWRITE RULE: Rewrite content in style voice. DO NOT copy-paste from source. Source = WHAT, Style = HOW.
    FORMATTING: NO markdown tables, NO diagrams (mermaid, ASCII art, flowcharts) - use bullet points instead.
    QUALITY: Write with narrative flow, not as summary. Go deep on key ideas. End section with bridge to next.

    LANGUAGE: Write in Vietnamese. Keep technical terms in English with Vietnamese explanation.

    Return: markdown content only

# Phase 3: Merge (main agent)

## 3a. Combine sections
- Concatenate expanded sections in outline order (Phase 1 skeleton)
- Remove duplicate H2/H3 headers if sections overlap

## 3b. Add transitions between H2 sections
- Insert 1-2 bridge sentences between each H2 section
- Write organic bridge sentences (question, insight, or image that connects sections naturally)
- Avoid mechanical transitions: "Từ X, chuyển sang Y", "Dựa trên phần trên", "Tiếp nối"
- Transitions must NOT introduce new factual claims (style/flow only)
- Match transition tone to selected output style

## 3c. Terminology consistency check
- Scan all sections for variant spellings of key terms from glossary
- Unify to the form used in the source document
- Check person/voice consistency across sections (must match style)

## 3d. Handle overlapping content
- If two parallel sections cover the same [Sxx]:
  - Keep the longer/richer version
  - Delete the duplicate, add a brief cross-reference sentence
  - Never merge by averaging -- pick one, discard the other

## 3e. Final pass
- Verify content coverage is complete (all source ideas included)
- Add "Các bài viết trong series" section at end
- Mark current article with **bold** + _(đang xem)_
- Save to {outputPath}
```

**SoT Error Handling (User-Driven - v1.13.0)**:

```
Phase 2 section fails (timeout or error)?
├─ Log which section failed
├─ Continue with successful sections
├─ Report to user at end:
│   "Section {X} failed. Options:
│    1. Accept partial article (recommended)
│    2. Retry failed section
│    3. Fallback to monolithic write"
│
└─ Phase 3 merge fails?
    └─ Save sections as separate files
    └─ Report: "Merge failed. Sections saved separately."
    └─ User can manually merge or request retry

QUAN TRỌNG: Không tự động retry. User quyết định.
```

**Benefits**: \~45-50% faster for long articles via parallel expansion

## Variable Reference

| Variable             | Tier 1                           | Tier 2                          | Tier 3                                  |
| -------------------- | -------------------------------- | ------------------------------- | --------------------------------------- |
| `{contextFilePath}`  | N/A                              | `analysis/XX-{slug}-context.md` | N/A                                     |
| `{glossaryFilePath}` | N/A                              | `analysis/_glossary.md`         | N/A                                     |
| `{sourcePath}`       | `input-handling/content.md`      | N/A                             | `input-handling/content.md`             |
| `{start}`, `{end}`   | From `structure.json` outline    | N/A                             | From `structure.json` suggested\_chunks |
| `{inlineGlossary}`   | \~200 words (embedded in prompt) | N/A                             | \~300 words (embedded in prompt)        |
| `{style}`            | User selection                   | User selection                  | User selection                          |
| `{seriesList}`       | From `_plan.md`                  | From `_plan.md`                 | From `_plan.md`                         |
| `{contentType}`      | From `_plan.md` content type     | From `_plan.md` content type    | From `_plan.md` content type            |
| `{readerEnters}`     | From `_plan.md` Series Context   | From `_plan.md` Series Context  | From `_plan.md` Series Context          |
| `{readerExits}`      | From `_plan.md` Series Context   | From `_plan.md` Series Context  | From `_plan.md` Series Context          |

**Note**: Tier 1 and Tier 3 both read source directly via line ranges, but Tier 3 uses larger inline glossary (\~300 words) because larger documents have more technical terminology and subagents need more context without access to the full document.

## Series List Format

```markdown
## Các bài viết trong series

1. [Tổng quan](./00-overview.md) - Giới thiệu series
2. [Article 1 Title](./01-slug.md) - Brief description
3. **Article 2 Title** _(đang xem)_
4. [Article 3 Title](./03-slug.md) - Brief description
```

Current article: Use **bold** + _(đang xem)_ instead of link.

## Skip Validation

See [decision-trees.md#7](references/decision-trees.md#7-skip-validation) for the full validation rules.

Invalid skip → Retry with instruction to summarize or include specific \[Sxx].

## Error Recovery (User-Driven - v1.13.0)

| Error          | Action                | Auto-retry? |
| -------------- | --------------------- | ----------- |
| Timeout        | Report to user        | ❌ NO        |
| Missing output | Log warning, continue | ❌ NO        |
| Style mismatch | Report, user decides  | ❌ NO        |
| Fabrication    | Flag for user review  | ❌ NO        |

**Nguyên tắc**: Log và report, không tự động retry.

## Multi-Part Article Template

For articles that have been split due to length (see SKILL.md Step 3.3.1).

```
Task tool:
- subagent_type: "general-purpose"
- description: "Write: {title} (Part {N}/{total})"
- prompt: |
    TASK: Write "{title} (Phần {partNumber}/{totalParts})"

    SOURCE: {sourcePath} L{start}-{end}
    STYLE: .claude/skills/writer-agent/output_styles/{style}.md
    OUTPUT: {outputPath}

    TARGET: ~{target_words} words (reference only)

    TERMS: {inlineGlossary}

    CONTEXT BRIDGE (for Part 2+):
    - Previous part: {prevPartSlug}.md
    - Prev topics: {prevPartTopics}
    - Prev ended with: "{prevPartEnding}"
    - Key concepts introduced: {keyConceptsFromPrev}

    CONTINUATION RULES:
    - Part 1: Start normally with hook intro
    - Part 2+: Begin with visual recap block, then dive into new content
      Format:
      > **Từ phần trước:**
      > - [Key point 1 from previous part]
      > - [Key point 2 from previous part]
      > - [Key point 3 from previous part]

      Then continue with a hook into new content (NOT "Tiếp tục từ...")
    - Not last part: End with: "Xem tiếp Phần {N+1}..."
    - Last part: End with conclusion

    LANGUAGE:
    - Write ENTIRE article in Vietnamese
    - Keep technical terms in English with Vietnamese explanation

    FORMATTING (CRITICAL):
    - NO markdown tables - convert to bullet lists
    - NO diagrams (mermaid, ASCII art, flowcharts) - describe in prose or bullets
    - Use bullet points for comparisons, lists, and structured data

    SERIES_LIST (Multi-Part Format):
    1. [Tổng quan](./00-overview.md) - Giới thiệu series
    2a. [Core Concepts - Phần 1](./02-core-part1.md)
    2b. **Core Concepts - Phần 2** _(đang xem)_
    2c. [Core Concepts - Phần 3](./02-core-part3.md)
    3. [Next Topic](./03-next.md)

    REWRITE RULE (CRITICAL):
    - MUST rewrite ALL content in YOUR voice following the output style — INCLUDING ⭐ critical sections
    - DO NOT copy-paste sentences or paragraphs from source (no exceptions)
    - Source = WHAT ideas to express, Style = HOW to express them
    - Transform source ideas into the style's voice, structure, and language patterns
    - ⭐ critical sections: faithful rewrite — giữ 100% ý nghĩa, KHÔNG tóm tắt, viết lại bằng tiếng Việt + style voice
    - If a paragraph matches source word-for-word → FAIL (no exceptions)

    WRITING QUALITY (CRITICAL):
    - Opening (Part 1): Compelling hook, NOT "Trong bài này..."
    - Opening (Part 2+): Brief recap then dive in, NOT mechanical "Ở phần trước..."
    - Narrative flow: Sections lead naturally to each other
    - Closing (not last part): Create anticipation for next part naturally
    - Closing (last part): Resonant ending that ties back to article theme

    RULES:
    - Source content ONLY, no fabrication
    - [Sxx]* = faithful rewrite (100% meaning, Vietnamese, style voice — KHÔNG tóm tắt)
    - Non-critical sections = MUST rewrite in style voice
    - Do NOT repeat content from previous parts
    - Reference previous parts naturally, not mechanically
    - Include navigation links between parts
    - Focus on content coverage, word count is reference only
    - MUST end with "## Các bài viết trong series" (MANDATORY)

    RETURN FORMAT (CRITICAL - Table format):
    - Article content ALREADY saved to {outputPath}
    - DO NOT return article content in message

    DONE: {filename} | {N} words (stats)
    PART: {partNumber}/{totalParts}
    COVERAGE (determines PASS/FAIL):
    | Section | Status |
    |---------|--------|
    | S01 | ✅ {how_used} |
    | S02 ⭐ | ✅ faithful |
    RESULT: {PASS if all sections covered, FAIL if missing}
    SERIES_LIST: {YES/NO}
    VERIFY: "quote..." (L45), "quote..." (L128)
```

### Context Bridge Generation

Main agent generates context bridge for Part N based on Part N-1:

```python
def generate_context_bridge(prev_part, current_part):
    return {
        'prevPartSlug': prev_part['slug'],
        'prevPartTopics': extract_h2_titles(prev_part),  # List of H2s
        'prevPartEnding': get_last_paragraph(prev_part, max_words=50),
        'keyConceptsFromPrev': extract_defined_terms(prev_part)
    }
```

### Part Naming Convention

| Original         | Split Into                                                 |
| ---------------- | ---------------------------------------------------------- |
| `02-core.md`     | `02-core-part1.md`, `02-core-part2.md`, `02-core-part3.md` |
| `03-advanced.md` | `03-advanced-part1.md`, `03-advanced-part2.md`             |

### Coverage Tracking for Split Articles

Each part reports coverage for its assigned sections only.
Main agent aggregates into `_coverage.md`:

```markdown
| Section | Part 1 | Part 2 | Part 3 | Total |
|---------|--------|--------|--------|-------|
| S03 | 100% | - | - | 100% ✅ |
| S04 | 60% | 40% | - | 100% ✅ |
| S05 | - | 100% | - | 100% ✅ |
| S06 | - | 50% | 50% | 100% ✅ |
```

**Validation rules:**

* Each section MUST have Total = 100%

* No line can appear in multiple parts (no overlap)

* All source lines must be covered (no miss)

