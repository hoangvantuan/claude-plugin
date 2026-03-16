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
  opening_technique: "{technique từ Opening Palette, e.g. in-medias-res}"
  prev_opening_used: "{technique bài trước dùng, e.g. scene-setting | N/A nếu bài đầu}"
```

**Cách main agent tạo Series Context:**

1. Từ `_plan.md`, xác định article_role dựa trên vị trí trong series
2. core_message: trích từ thông điệp cốt lõi trong plan hoặc structure.json
3. prev/next: tóm tắt 1 câu từ article titles trong plan
4. reader_journey: mô tả progression logic
5. reader_enters: mô tả kiến thức người đọc có khi bắt đầu bài (từ bài trước)
6. reader_exits: mô tả kiến thức người đọc đạt được sau bài (dẫn tới bài sau)
7. opening_technique: lấy từ cột `Opening` trong `_plan.md` Series Context table
8. prev_opening_used: technique bài trước dùng (N/A nếu bài đầu tiên)

## Shared Rules (Referenced by All Tier Templates)

All tier templates include these identical blocks. Defined once here to avoid duplication.

### WRITING_RULES Block

```
WRITING_RULES (CRITICAL):
- Write ENTIRE article in Vietnamese. Technical terms in English + Vietnamese explanation on first use.
- NO markdown tables (use bullet lists). NO diagrams (mermaid/ASCII/flowcharts, describe in prose).
- MUST rewrite ALL content in selected voice. Source = WHAT, Voice = HOW.
- DO NOT copy-paste from source. If paragraph matches source word-for-word → FAIL.
- Critical [Sxx]*: faithful rewrite (100% meaning, Vietnamese, voice persona, NO summary).
- Non-critical: rewrite freely per detail level.
- FIRST cover ALL source ideas → THEN rewrite in voice → THEN write naturally.
- Quality coverage + voice compliance > word count targets.
```

### WRITER PROFILE Block (Bắt buộc, luôn include)

```
WRITER_PROFILE:
  IDENTITY: {role} với chuyên môn {expertise}. Credibility: {credibility}. Unique angle: {unique_angle}
  PHILOSOPHY: Worldview: {worldview}. Core beliefs: {core_beliefs}
  AUDIENCE: Người đọc {knows}, cảm thấy {feels}, muốn {wants}, sợ {fears}. Objections: {objections}
  EMOTIONAL_MAP: Primary: {primary}. Avoid: {avoid}. Arc: {emotional_arc}

  DIMENSION BOUNDARIES:
  Voice controls (KHÔNG bị override):
  - Persona, ngôi xưng, giọng điệu cơ bản
  - Language DO/DON'T list
  - Core techniques và sentence-level pacing
  
  Profile controls:
  - Identity → authority, expertise, evidence type
  - Audience → addressing level, complexity, examples
  - Emotion → emotional arc, guardrails, intensity

  CONFLICT RESOLUTION:
  - TONE: Voice sets BASE tone, Emotion ADJUSTS intensity within voice's range
  - CLOSING: Voice sets FORMAT (summary/question/open), Emotion sets FEELING (empower/reflect/provoke)
  - If conflict: Adapt emotion's GOAL using voice's TOOLS
    Example: Teacher + Provoke → dùng analogy (Teacher tool) để challenge assumption (Provoke goal)
    Example: Objective + Reflect → dùng data (Objective tool) để mở câu hỏi (Reflect goal)
    Example: Dialogue + Empower → dùng câu hỏi Zen (Dialogue tool) để trao sức (Empower goal)
```

### How to Compose 5 Dimensions into Subagent Prompt

```
Dimension mapping (tất cả mandatory):
  Voice      → VOICE section: paste compact voice file content ({voice}-compact.md)
  Structure  → STRUCTURE section: paste compact structure file content ({structure}-compact.md)
  Identity   → WRITER_PROFILE.IDENTITY field
  Audience   → WRITER_PROFILE.AUDIENCE field
  Emotion    → WRITER_PROFILE.EMOTIONAL_MAP field

Rules:
  - Tất cả 5 dimensions BẮT BUỘC, luôn include đầy đủ
  - Voice and Structure are always separate sections, never merged into WRITER PROFILE
  - WRITER PROFILE luôn có đủ 3 fields: IDENTITY, AUDIENCE, EMOTIONAL_MAP
  - Use compact versions for subagent injection (75% smaller, retains all essential sections)
  - Full voice/structure files available for main agent reference during Step 2
```

**Ví dụ compose** (Teacher + Building Blocks + Tech Builder + Curious Beginners + Empower & Challenge):

```
VOICE: [paste nội dung voices/teacher.md]

STRUCTURE: [paste nội dung structures/building-blocks.md]

WRITER_PROFILE:
  IDENTITY: Tech Builder - practitioner, pragmatic builder. Credibility: hands-on experience. Unique angle: real-world application
  AUDIENCE: Curious Beginners - mới bắt đầu, cần clarity, muốn hiểu cơ bản, sợ chủ đề quá khó
  EMOTIONAL_MAP: Primary: Empower & Challenge - growth qua discomfort. Avoid: condescending tone. Arc: curiosity → confidence → motivation
```

### WRITING QUALITY Block

```
WRITING QUALITY (CRITICAL):
- Opening: MUST use SERIES_CONTEXT.opening_technique (see Opening Palette in structure file)
  - DO NOT default to scene-setting if a different technique is assigned
  - DO NOT use the same opening pattern as prev_opening_used
- Closing: Follow the structure file's Closing guidelines
- Narrative flow: Each section leads naturally to the next
- Depth over breadth: Go deep on 2-3 key ideas
- Draw connections: Link ideas to SERIES_CONTEXT.core_message
- BLACKLIST phrases: "Trong phần tiếp theo...", "Tóm lại,...", "Bài viết đã trình bày..."
- Micro-story: Nếu có thể, dùng ví dụ cụ thể (người thật, tình huống thật, kết quả thật) thay vì giải thích trừu tượng. Không cần format story, có thể chỉ là 1-2 câu nhắc kinh nghiệm lồng trong đoạn.

INSIGHT_TECHNIQUES (minimum 2 per article):
- Tạo insight bằng cách: tìm mâu thuẫn, liên hệ ngoài ngành, rút hệ quả source không nói, hoặc đặt lại câu hỏi
- KHÔNG dùng cấu trúc câu cố định cho insight. Để nó xuất hiện tự nhiên trong dòng chảy bài viết
- Mỗi insight phải earned: build up context trước, không drop in bất ngờ
- Cho phép 1-2 đoạn/bài CHỈ kể/mô tả mà KHÔNG rút insight. Đôi khi chi tiết chỉ cần ở đó.
```

### ANTI-AI WRITING Block

```
ANTI-AI WRITING (CRITICAL, output PHẢI đọc như người viết, KHÔNG như AI):

PUNCTUATION:
- TUYỆT ĐỐI KHÔNG dùng em dash (—). Thay bằng dấu phẩy, dấu hai chấm, hoặc tách câu
  SAI: "Giải pháp này — vốn đã được thử nghiệm — mang lại kết quả tốt"
  ĐÚNG: "Giải pháp này đã được thử nghiệm và mang lại kết quả tốt"
  ĐÚNG: "Giải pháp này, vốn đã được thử nghiệm, mang lại kết quả tốt"
- Hạn chế dấu chấm phẩy (;). Tách thành 2 câu nếu cần
- Không lạm dụng dấu phẩy nối (comma splice)

VOCABULARY BLACKLIST (KHÔNG dùng các từ/cụm sau):
- VI: "bức tranh toàn cảnh", "hệ sinh thái", "bối cảnh không ngừng", "mở ra cánh cửa",
      "hành trình chuyển đổi", "đa chiều", "đa diện", "toàn diện và sâu sắc",
      "không thể phủ nhận", "đáng kinh ngạc", "tuyệt vời", "mang tính cách mạng",
      "thay đổi cuộc chơi", "đột phá", "mang tính bước ngoặt"
- EN: "delve", "tapestry", "landscape", "leverage", "nuanced", "multifaceted",
      "paradigm shift", "transformative", "game-changer", "holistic", "robust"
- Thay bằng từ đơn giản, cụ thể, gần gũi đời thường

SENTENCE STRUCTURE (VOICE-DEPENDENT — xem Pacing Rules trong voice file):
- Mỗi voice có chiến lược câu riêng. TUÂN THEO voice's Pacing Rules, không áp dụng 1 pattern cho tất cả
- KHÔNG viết câu đều tăm tắp cùng độ dài. 3 câu trung bình liên tiếp = OK và tự nhiên
- KHÔNG alternating ngắn-dài-ngắn đều đặn (AI pattern dễ nhận ra)
- KHÔNG lặp cấu trúc song song liên tục ("Thứ nhất... Thứ hai... Thứ ba...")
- KHÔNG stack nhiều mệnh đề phụ trong 1 câu
- Bắt đầu câu bằng "Và", "Nhưng", "Vì" khi cần nhịp tự nhiên

STACCATO BAN (CRITICAL — vi phạm = output giống AI ngay lập tức):
- KHÔNG viết 2+ câu dưới 6 từ liên tiếp. "Không phải buồn. Không phải mệt. Chỉ là nặng." = FAIL
- KHÔNG dùng nominal phrases đứng riêng: "Mùi trà sen. Tiếng gió qua rặng tre." = FAIL
  → Lồng vào câu có động từ: "Mùi trà sen trộn lẫn tiếng gió lùa qua rặng tre"
- KHÔNG kết đoạn bằng fragment "triết lý": "Đơn giản vậy thôi." "Chỉ có vậy." = FAIL
  → Nếu cần kết ngắn, dùng câu có chủ-vị: "Chuyện chỉ có vậy thôi."
- Câu ngắn (<8 từ): tối đa 2-3 lần/bài, PHẢI có chủ ngữ + vị ngữ, đứng sau buildup

TONE & PERSONALITY:
- Có ý kiến rõ ràng, dám nói thẳng. Hạn chế hedging — không dùng "có thể/có lẽ/dường như" liên tiếp trong cùng đoạn
- Nếu cần provisional, dùng nhiều cách: "tôi đoán...", "chưa chắc nhưng...", "nghe thì...", "xem ra..."
- Không enthusiasm giả tạo ("tuyệt vời!", "đáng kinh ngạc!")
- Không corporate neutral vô vị. Nếu điều gì tốt, nói tốt. Nếu xấu, nói xấu.
- Cho phép 1-2 câu/bài lệch tone nhẹ (bình luận cá nhân bất ngờ, aside ngắn) — dấu hiệu người viết thật
- Self-contradict: khoảng 1/3 bài, không phải mọi bài. Không dùng cùng cấu trúc câu mỗi lần

VIETNAMESE-SPECIFIC:
- Ưu tiên từ thuần Việt hơn Hán-Việt khi nghĩa tương đương
  SAI: "tối ưu hóa hiệu suất hoạt động" → ĐÚNG: "chạy nhanh hơn"
  SAI: "cung cấp khả năng" → ĐÚNG: "giúp", "cho phép"
- Không lặp "chúng ta" quá nhiều (tối đa 3-4 lần/đoạn)
- Cấu trúc câu Việt tự nhiên, KHÔNG dịch từ English
  SAI: "Bằng cách sử dụng X, chúng ta có thể đạt được Y"
  ĐÚNG: "Dùng X thì đạt được Y"
- Dùng particles khi phù hợp với style (nhỉ, nhé, ấy, đấy)

STRUCTURAL:
- KHÔNG liệt kê 3 items mọi lúc (triple-listing). Dùng 2, 4, 5 items tự nhiên
- KHÔNG mở bài bằng "Trong bối cảnh...", "Trong thế giới hiện đại...", "Với sự phát triển..."
- KHÔNG tóm tắt lại điều vừa nói (summary redundancy)
- Nối ý bằng logic tự nhiên. Nếu ý tiếp hiển nhiên, không cần transition. Nếu cần, dùng từ phù hợp context chứ không theo template
- KHÔNG dùng "Hơn nữa", "Ngoài ra", "Bên cạnh đó" trong 2 đoạn liên tiếp

PATTERN BLACKLIST (AI tells — phát hiện ngay bởi người đọc):
- Opening: NEVER "Trong bối cảnh...", "Với sự phát triển...", "Bạn đã bao giờ tự hỏi..." dạng rhetorical
- Uniformity: Vary paragraph length (2-7 câu). KHÔNG để mọi đoạn cùng độ dài
- Mirror: KHÔNG kết đoạn cùng cấu trúc với câu mở đoạn sau
- Triple-list: KHÔNG dùng pattern "X, Y, và Z" liên tiếp >2 lần/bài
- Fragment closers: KHÔNG kết đoạn bằng fragment triết lý: "Đơn giản vậy thôi." "Chỉ có vậy."
```


### READER_TRANSFORMATION Block

```
READER_TRANSFORMATION:
  reader_before: "{what reader believes/knows before this article}"
  reader_after: "{what reader understands/can do after}"
  transformation_moment: "{the key 'aha' moment in this article}"
  common_misconception: "{what reader likely gets wrong about this topic}"
```

Main agent populates from SERIES_CONTEXT.reader_enters/exits + plan analysis. Subagent uses this to: give transformation_moment most depth, address common_misconception explicitly.

### SELF_CRITIQUE Block

```
SELF_CRITIQUE (after writing article, before .done):
Re-read your article. Fix these 3 things:
1. Find the most AI-sounding sentence -> rewrite with shorter words, specific detail
2. Find a paragraph that just summarizes source -> add insight using INSIGHT_TECHNIQUES
3. Check: does opening hook reader in 2 sentences? If not, sharpen it
Save revised article to {outputPath} (overwrite). Then proceed to .done.
```

### CONTEXT RULES Block

```
CONTEXT RULES (CRITICAL - minimize subagent context usage):
- Voice and Structure content are EMBEDDED in this prompt. DO NOT read them from files.
- DO NOT glob or search for other article files
- DO NOT read existing articles for format reference
- DO NOT explore the directory structure
- ONLY read the SOURCE file at specified line range
- Workflow: Read SOURCE → Write article to OUTPUT → Write .done summary → Return summary. Nothing else.
```

### RETURN FORMAT Block

```
RETURN FORMAT (CRITICAL):
- Save article to {outputPath} using Write tool
- Save summary to {outputPath}.done using Write tool (same path + ".done" extension)
- Your FINAL response MUST contain ONLY the summary below
- DO NOT include explanations, thinking process, or commentary in final message
- DO NOT return article content in message

Summary content (write to BOTH .done file AND final message):

DONE: {filename} | {N} words
KEY_TAKEAWAY: {1-2 câu tóm tắt insight/ý chính quan trọng nhất của bài viết}
COVERAGE: S01:ok S02*:faithful S03:ok
RESULT: {PASS/FAIL}
```

## Tier 3 Compact Template (>=100K words)

Streamlined prompt for large documents (~40% context reduction):

```
Task tool:
- subagent_type: "general-purpose"
- description: "Write: {title}"

- prompt: |
    TASK: Write "{title}" for {seriesTitle}

    SOURCE: {sourcePath} L{start}-{end}
    OUTPUT: {outputPath}

    VOICE:
    {voiceContent}

    STRUCTURE:
    {structureContent}

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
      opening_technique: "{openingTechnique}"
      prev_opening_used: "{prevOpeningUsed}"

    SERIES_LIST:
    {seriesList}

    [Include READER_TRANSFORMATION block from Shared Rules above]
    [Include CONTEXT RULES block from Shared Rules above]
    [Include WRITING_RULES block from Shared Rules above]

    ARTICLE_STRUCTURE:
    - Follow the STRUCTURE section above for article organization
    - The structure defines phases (Opening/Development/Closing or equivalent)
    - MANDATORY constraints (override structure):
      1. Title (H1) - descriptive, evocative
      2. Opening: MUST use opening_technique "{openingTechnique}" from SERIES_CONTEXT.
         DO NOT default to scene-setting. DO NOT repeat prev_opening_used pattern.
      3. Before "## Các bài viết trong series", add a brief narrative bridge (1-2 sentences)
         that creates natural curiosity for the next article.
         Format: A question, image, or thought connecting this article's conclusion to the next.
         DO NOT use: "Trong phần tiếp theo...", "Bài tiếp theo sẽ..."
      4. Must end with "## Các bài viết trong series" (mark current with _(đang xem)_)
    - The structure defines HOW to organize content
    - The source sections [Sxx] define WHAT content to include

    CONTENT_TYPE: {contentType}

    [Include WRITER PROFILE block from Shared Rules above]
    [Include WRITING QUALITY block from Shared Rules above]
    [Include ANTI-AI WRITING block from Shared Rules above]

    RULES:
    - Source ONLY, no fabrication
    - [Sxx]* sections = faithful rewrite (100% meaning, Vietnamese, selected voice, KHÔNG tóm tắt)
    - Non-critical sections = MUST rewrite in selected voice
    - MUST end with "## Các bài viết trong series" section (MANDATORY - article FAILS without this)
    - Mark current article with _(đang xem)_
    - Focus on content coverage, word count is reference only

    [Include SELF_CRITIQUE block from Shared Rules above]
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
    OUTPUT: {outputPath}

    VOICE:
    {voiceContent}

    STRUCTURE:
    {structureContent}

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
      opening_technique: "{openingTechnique}"
      prev_opening_used: "{prevOpeningUsed}"

    SERIES_LIST:
    {seriesList}

    [Include READER_TRANSFORMATION block from Shared Rules above]
    [Include CONTEXT RULES block from Shared Rules above]
    [Include WRITING_RULES block from Shared Rules above]

    ARTICLE_STRUCTURE:
    - Follow the STRUCTURE section above for article organization
    - The structure defines phases (Opening/Development/Closing or equivalent)
    - MANDATORY constraints (override structure):
      1. Title (H1) - descriptive, evocative
      2. Opening: MUST use opening_technique "{openingTechnique}" from SERIES_CONTEXT.
         DO NOT default to scene-setting. DO NOT repeat prev_opening_used pattern.
      3. Before "## Các bài viết trong series", add a brief narrative bridge (1-2 sentences)
         that creates natural curiosity for the next article.
         Format: A question, image, or thought connecting this article's conclusion to the next.
         DO NOT use: "Trong phần tiếp theo...", "Bài tiếp theo sẽ..."
      4. Must end with "## Các bài viết trong series" (mark current with _(đang xem)_)
    - The structure defines HOW to organize content
    - The source sections [Sxx] define WHAT content to include

    CONTENT_TYPE: {contentType}

    [Include WRITER PROFILE block from Shared Rules above]
    [Include WRITING QUALITY block from Shared Rules above]
    [Include ANTI-AI WRITING block from Shared Rules above]

    RULES:
    - Source content ONLY
    - [Sxx]* = faithful rewrite (100% meaning, Vietnamese, selected voice, KHÔNG tóm tắt)
    - Non-critical sections = MUST rewrite in selected voice
    - Preserve terminology
    - 100% reader-facing, no metadata in output
    - Focus on content coverage, word count is reference only
    - MUST end with "## Các bài viết trong series" (MANDATORY - article FAILS without this)

    [Include SELF_CRITIQUE block from Shared Rules above]
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

    OUTPUT: {outputPath}

    VOICE:
    {voiceContent}

    STRUCTURE:
    {structureContent}

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
      opening_technique: "{openingTechnique}"
      prev_opening_used: "{prevOpeningUsed}"

    SERIES_LIST:
    {seriesList}

    [Include READER_TRANSFORMATION block from Shared Rules above]
    [Include CONTEXT RULES block from Shared Rules above]
    [Include WRITING_RULES block from Shared Rules above]

    ARTICLE_STRUCTURE:
    - Follow the STRUCTURE section above for article organization
    - The structure defines phases (Opening/Development/Closing or equivalent)
    - MANDATORY constraints (override structure):
      1. Title (H1) - descriptive, evocative
      2. Opening: MUST use opening_technique "{openingTechnique}" from SERIES_CONTEXT.
         DO NOT default to scene-setting. DO NOT repeat prev_opening_used pattern.
      3. Before "## Các bài viết trong series", add a brief narrative bridge (1-2 sentences)
         that creates natural curiosity for the next article.
         Format: A question, image, or thought connecting this article's conclusion to the next.
         DO NOT use: "Trong phần tiếp theo...", "Bài tiếp theo sẽ..."
      4. Must end with "## Các bài viết trong series" (mark current with _(đang xem)_)
    - The structure defines HOW to organize content
    - The source sections [Sxx] define WHAT content to include

    CONTENT_TYPE: {contentType}

    [Include WRITER PROFILE block from Shared Rules above]
    [Include WRITING QUALITY block from Shared Rules above]
    [Include ANTI-AI WRITING block from Shared Rules above]

    RULES:
    - Source content ONLY
    - [Sxx]* = faithful rewrite (100% meaning, Vietnamese, selected voice, KHÔNG tóm tắt)
    - Non-critical sections = MUST rewrite in selected voice
    - Preserve terminology
    - 100% reader-facing, no metadata in output
    - Focus on content coverage, word count is reference only
    - MUST end with "## Các bài viết trong series" (MANDATORY - article FAILS without this)

    [Include SELF_CRITIQUE block from Shared Rules above]
    [Include RETURN FORMAT block from Shared Rules above]
```

### Detail Level Parameters

| Level         | critical_handling                    | non_critical_handling    | example_percentage | Target Reading Time |
| ------------- | ------------------------------------ | ------------------------ | ------------------ | ------------------- |
| Concise       | Full faithful rewrite (100% meaning) | 1-2 sentences each       | 30%                | ~5 min              |
| Standard      | Full faithful rewrite (100% meaning) | Summarize + key examples | 60%                | ~10 min             |
| Comprehensive | Full faithful rewrite (100% meaning) | Most content             | 85%                | ~13 min             |
| Faithful      | Full faithful rewrite (100% meaning) | Full content             | 100%               | ~15 min             |


**Reading Time Targets (~13-15 minutes per article):**

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

- Priority 3 (paragraph breaks) is not implemented. Documents with no headings will skip SoT.
- Mixed structure logic uses simple addition, which may not capture complexity of deeply nested hierarchies.

**Note:** "Total source content" = combined content from ALL sections ([Sxx]) mapped to this article.

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

    VOICE:
    {voiceContent}

    LANGUAGE: Write in Vietnamese. Keep technical terms in English with Vietnamese explanation.
    DO NOT read any files. All context is provided above.

    Return: markdown content only

Task[1]:
- description: "Write section: {H2_title}"

- prompt: |
    Write "{H2_title}" (~{word_target} words)
    Context: {section_content}

    VOICE:
    {voiceContent}

    REWRITE RULE: Rewrite content in voice persona. DO NOT copy-paste from source. Source = WHAT, Voice = HOW.
    FORMATTING: NO markdown tables, NO diagrams (mermaid, ASCII art, flowcharts) - use bullet points instead.
    QUALITY: Write with narrative flow, not as summary. Go deep on key ideas. End section with bridge to next.
    ANTI-AI: NO em dash (—). Vary sentence length. No AI vocabulary. Natural Vietnamese structure.
    LANGUAGE: Write in Vietnamese. Keep technical terms in English with Vietnamese explanation.
    DO NOT read any files. All context is provided above.

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
- Match transition tone to selected voice

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

**SoT Error Handling**: Section fails → log it, continue with successful sections → report to user at end with options: accept partial (recommended), retry failed section, or fallback to monolithic write. Phase 3 merge fails → save sections separately. **Không tự động retry — user quyết định.**

**Benefits**: ~45-50% faster for long articles via parallel expansion

## Variable Reference

| Variable             | Tier 1                          | Tier 2                          | Tier 3                                 |
| -------------------- | ------------------------------- | ------------------------------- | -------------------------------------- |
| `{contextFilePath}`  | N/A                             | `analysis/XX-{slug}-context.md` | N/A                                    |
| `{glossaryFilePath}` | N/A                             | `analysis/_glossary.md`         | N/A                                    |
| `{sourcePath}`       | `input-handling/content.md`     | N/A                             | `input-handling/content.md`            |
| `{start}`, `{end}`   | From `structure.json` outline   | N/A                             | From `structure.json` suggested_chunks |
| `{inlineGlossary}`   | ~200 words (embedded in prompt) | N/A                             | ~300 words (embedded in prompt)        |
| `{voiceContent}`     | Pre-read by main agent          | Pre-read by main agent          | Pre-read by main agent                 |
| `{structureContent}` | Pre-read by main agent          | Pre-read by main agent          | Pre-read by main agent                 |
| `{seriesList}`       | From `_plan.md`                 | From `_plan.md`                 | From `_plan.md`                        |
| `{contentType}`      | From `_plan.md` content type    | From `_plan.md` content type    | From `_plan.md` content type           |
| `{readerEnters}`     | From `_plan.md` Series Context  | From `_plan.md` Series Context  | From `_plan.md` Series Context         |
| `{readerExits}`      | From `_plan.md` Series Context  | From `_plan.md` Series Context  | From `_plan.md` Series Context         |
| `{openingTechnique}` | From `_plan.md` Opening column  | From `_plan.md` Opening column  | From `_plan.md` Opening column         |
| `{prevOpeningUsed}`  | Technique of prev article (N/A if first) | Same | Same                            |

**Note**: `{voiceContent}` and `{structureContent}` are pre-read by the main agent and embedded directly in the prompt. Subagents do NOT read these files themselves - this saves 2+ tool calls per subagent, significantly reducing conversation transcript size.

**Note**: Tier 1 and Tier 3 both read source directly via line ranges, but Tier 3 uses larger inline glossary (~300 words) because larger documents have more technical terminology and subagents need more context without access to the full document.

## Series List Format

```markdown
## Các bài viết trong series

1. [Tổng quan](./00-overview.md) - Giới thiệu series
2. [Article 1 Title](./01-slug.md) - Brief description
3. **Article 2 Title** _(đang xem)_
4. [Article 3 Title](./03-slug.md) - Brief description
```

Current article: Use **bold** + *(đang xem)* instead of link.

## Skip Validation

See [decision-trees.md#6](decision-trees.md#6-skip-validation-relaxed---v1130) for the full validation rules.

> **v1.13.0**: Không tự động retry. Log warnings và report cho user quyết định.

## Error Recovery (User-Driven - v1.13.0)

> See [retry-workflow.md](retry-workflow.md) for full error recovery procedures and user decision points.

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
    OUTPUT: {outputPath}

    VOICE:
    {voiceContent}

    STRUCTURE:
    {structureContent}

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

    [Include WRITING_RULES block from Shared Rules above]

    SERIES_LIST (Multi-Part Format):
    1. [Tổng quan](./00-overview.md) - Giới thiệu series
    2a. [Core Concepts - Phần 1](./02-core-part1.md)
    2b. **Core Concepts - Phần 2** _(đang xem)_
    2c. [Core Concepts - Phần 3](./02-core-part3.md)
    3. [Next Topic](./03-next.md)

    [Include WRITING QUALITY block from Shared Rules above]
    - Opening (Part 2+): Brief recap then dive in, NOT mechanical "Ở phần trước..."
    - Closing (not last part): Create anticipation for next part naturally

    [Include ANTI-AI WRITING block from Shared Rules above]

    RULES:
    - Source content ONLY, no fabrication
    - [Sxx]* = faithful rewrite (100% meaning, Vietnamese, selected voice, KHÔNG tóm tắt)
    - Non-critical sections = MUST rewrite in selected voice
    - Do NOT repeat content from previous parts
    - Reference previous parts naturally, not mechanically
    - Include navigation links between parts
    - Focus on content coverage, word count is reference only
    - MUST end with "## Các bài viết trong series" (MANDATORY)

    SELF_CRITIQUE: Re-read. Fix most AI-sounding sentence. Add >=1 insight per INSIGHT_TECHNIQUES. Check: Part 1 opening hooks in 2 sentences? Part 2+ recap is brief then dives in?

    RETURN FORMAT (CRITICAL):
    - Save article to {outputPath} using Write tool
    - Save summary to {outputPath}.done using Write tool
    - DO NOT return article content in message

    Summary content (write to BOTH .done file AND final message):

    DONE: {filename} | {N} words
    PART: {partNumber}/{totalParts}
    KEY_TAKEAWAY: {1-2 câu tóm tắt insight chính của phần này}
    COVERAGE: S01:ok S02*:faithful S03:ok
    RESULT: {PASS/FAIL}
```

### Part Naming & Context Bridge

> See [large-doc-processing.md §Article Splitting](large-doc-processing.md#article-splitting-strategy) for part naming conventions, context bridge generation, and multi-part series list format.

### Coverage Tracking for Split Articles

Each part reports coverage for its assigned sections only (same status label format as standard coverage).
Main agent aggregates into `_coverage.md`:

```markdown
| Section | Assigned To | Status |
|---------|-------------|--------|
| S03 | 02-core-part1 | ✅ summarized |
| S04 | 02-core-part1, 02-core-part2 | ✅ faithful (split across parts) |
| S05 | 02-core-part2 | ✅ summarized |
| S06 ⭐ | 02-core-part3 | ✅ faithful |
```

**Validation rules:**

- Each section MUST be covered by at least one part
- No line can appear in multiple parts (no overlap)
- All source lines must be covered (no miss)
- Critical sections ⭐ MUST be 100% in single part
