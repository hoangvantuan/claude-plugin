# Report & Output Format

Templates cho Coverage Report, Quality Report, và Outline file format. Load khi cần generate reports (Step 4).

## Coverage Report Format

Lưu tại `{output_folder}/coverage-report.md`.

```markdown
# Coverage Report — [Tên presentation]

## Tổng quan
- **Source**: [tên file hoặc mô tả input]
- **Detail level**: L[x]
- **Topics trong source**: [N]
- **Topics covered**: [M] ([percentage]%)
- **Topics omitted**: [K]

## Source → Slide Mapping

| # | Source Topic | Priority | Slide(s) | Status |
|---|---|---|---|---|
| 1 | Topic A | must | 3, 4 | ✅ Covered |
| 2 | Topic B | must | 5 | ✅ Covered |
| 3 | Topic C | should | 6 | ✅ Merged with Topic B |
| 4 | Topic D | should | — | ⚠️ Omitted |
| 5 | Topic E | nice | — | ➖ Skipped (L2) |
| 6 | [R] Researched stat | should | 7 | ✅ Covered (research) |

## Omitted Topics & Justification

| Topic | Priority | Lý do bỏ |
|---|---|---|
| Topic D | should | Trùng lặp nội dung với Topic B (slide 5) |
| Topic E | nice | Edge case, vượt scope L2 |

## Key Data Check
- ✅ [Metric/data point] → slide [N]
- ✅ [Example] → slide [N]
- ⚠️ [Table/data] → simplified thành bullets (slide [N])
```

### Coverage Report Rules

- Mọi topic trong Content Analysis Map PHẢI xuất hiện trong report (covered hoặc omitted)
- Mọi topic omitted PHẢI có justification cụ thể (không generic)
- Justification hợp lệ: "trùng lặp với Topic X", "vượt scope L[n]", "gộp vào slide [N]", "quá chi tiết/edge case cho level này"
- Justification KHÔNG hợp lệ: "không quan trọng", "bỏ qua", "không cần thiết"
- Nếu coverage < threshold → PHẢI thêm topics vào outline cho đến khi đạt threshold

## Quality Report Format

Append vào cuối file `coverage-report.md`:

```markdown
---

# Quality Report

## Thesis Clarity
- **Core message**: [1 câu thesis]
- **Xuất hiện rõ ràng trong outline?** ✅/❌
- **Vị trí**: [Slide/Section X]
- **Intended transformation**: [educate/persuade/activate] — [mô tả]

## Argument Strength
| # | Key Argument | Evidence? | Evidence cụ thể? | Counter/Nuance? |
|---|---|---|---|---|
| 1 | [Argument 1] | ✅/❌ | ✅/❌ | ✅/❌ |
| 2 | [Argument 2] | ✅/❌ | ✅/❌ | ✅/❌ |
| 3 | [Argument 3] | ✅/❌ | ✅/❌ | ✅/❌ |

## Coherence Flow
- **Mỗi section có liên kết logic với section trước?** ✅/❌
- **Logic gaps**: [Liệt kê nếu có]
- **Narrative arc rõ ràng?** ✅/❌ [mô tả tension → release]

## Depth Score
| Score | Mô tả | Đạt? |
|---|---|---|
| 1 | Chỉ liệt kê facts, không có insight | |
| 2 | Có giải thích WHY/HOW | |
| 3 | Có insight/nguyên lý rút ra | |
| 4 | Có thể thay đổi cách thinking của audience | |
**Depth Score hiện tại**: [X/4]

## Content Principles Check
- [ ] Mọi slide/section title là assertion, không phải topic label?
- [ ] Mọi data point có implication kèm theo? ("So What?" test)
- [ ] Outline phục vụ đúng 1 transformation?
- [ ] Có tension-release pattern trong body?
- [ ] Ví dụ concrete xuất hiện trước khái niệm abstract?
```

### Quality Report Rules

- Quality Report BẮT BUỘC cho mọi output type (presentation, blog, doc)
- **Tiêu chí đạt tối thiểu**: Thesis Clarity = ✅, Depth Score ≥ 2, Content Principles ≥ 3/5
- Nếu Depth Score = 1 → CẢNH BÁO: outline chỉ là danh sách facts, cần bổ sung insight
- Nếu Thesis Clarity = ❌ → CẢNH BÁO: outline thiếu core message
- Nếu có Logic gaps → CẢNH BÁO: thêm section/transition để lấp gap
- Nếu Content Principles < 3/5 → xem lại và cải thiện trước khi show user

## Outline File Format (outline.md)

BẮT BUỘC có YAML frontmatter. Metadata cho phép reuse outline mà không cần hỏi lại config.

```yaml
---
title: "Tên outline"
slug: "ten-outline"
output_type: "presentation" | "blog" | "doc"
content_type: "..." # chỉ khi presentation
framework: "..." # chỉ khi presentation
audience: "..." # chỉ khi presentation
detail_level: "L1" | "L2" | "L3"
language: "vi" | "en" | "bilingual"
source: "mô tả source input"
thesis: "core message 1 câu"
intended_transformation: "educate" | "persuade" | "activate"
created: "YYYY-MM-DD HH:mm"
total_slides: N # hoặc total_sections cho blog/doc
---
```

## Outline Display Format

### L1 Format

```
=== OUTLINE (L1) ===

[Opening]
1. [title] Title chính
   Subtitle ngắn gọn
2. [content] Hook/Problem statement
   1 câu mô tả hook

[Body]
3. [content] Assertion sentence (section gộp)
   - Bullet ngắn <8 words
   - Bullet ngắn <8 words
   - Bullet ngắn <8 words

[Closing]
N. [summary] Key Takeaways
   - Point 1
   - Point 2

=== END OUTLINE ===
```

### L2/L3 Format

```
=== OUTLINE (L2/L3) ===

[Opening]
1. [title] Title chính của presentation
   Subtitle mô tả
2. [content] Hook/Problem statement
   Brief description of hook content
3. [agenda] Agenda
   List of sections

[Body - Section 1: Tên section]
4. [content] Assertion sentence as title
   - Main bullet 1
     · Sub-detail hoặc ví dụ
   - Main bullet 2
     · Sub-detail hoặc ví dụ
   - Main bullet 3
     · Sub-detail
5. [content] Next assertion
   - Main bullet with detail
     · Code example hoặc config snippet
   - Main bullet 2
     · Giải thích ngắn

[Body - Section 2: Tên section]
6. [transition] Section divider
7. [comparison] So sánh A vs B
   Left: Option A - key characteristics
   Right: Option B - key characteristics

[Closing]
N. [summary] Key Takeaways
   - Point 1
   - Point 2
   - Point 3
N+1. [cta] Call to Action
   Action description

=== END OUTLINE ===
```
