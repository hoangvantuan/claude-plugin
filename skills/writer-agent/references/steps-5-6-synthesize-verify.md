# Steps 5-6: Synthesize & Verify

> **GUARD**: Step 4 hoàn thành (tất cả articles written, `.done` files exist). Nếu chưa → **STOP, quay lại Step 4**.

## Step 5: Synthesize

### 5.1 Update Overview (Phase 2)

Update `00-overview.md` with actual content for placeholder sections.

**KHÔNG đọc lại articles.** Dùng dữ liệu từ `.done` files:

```python
# Nguồn dữ liệu cho overview (KHÔNG cần đọc article files hay transcript):
key_takeaways = []  # Từ KEY_TAKEAWAY trong .done files (Step 4.6)
series_list = []    # Từ _plan.md (đã có titles + descriptions từ Step 3)
core_message = ""   # Từ _plan.md Series Context
```

**Multi-part articles**: Gom KEY_TAKEAWAYs của các parts thành 1 takeaway cho bài đó. Ví dụ: article 02 có 3 parts → chọn takeaway đại diện nhất hoặc tổng hợp thành 1 câu.

**Điểm chính** (Key Takeaways) - compose từ KEY_TAKEAWAYs:

```markdown
## Điểm chính

1. **[Concept từ article 1 KEY_TAKEAWAY]**: [Expand từ takeaway]
2. **[Concept từ article 2 KEY_TAKEAWAY]**: [Expand từ takeaway]
3. **[Concept từ article 3 KEY_TAKEAWAY]**: [Expand từ takeaway]
```

**Các bài viết trong series** (Series List) - compose từ `_plan.md`:

```markdown
## Các bài viết trong series

1. **Tổng quan - Brief description** _(đang xem)_
2. [Article 1 Title](./01-slug.md) - Brief description
3. [Article 2 Title](./02-slug.md) - Brief description
```

**Final overview target**: 400-600 words (overview đặc biệt, dùng word target thay vì section coverage)

**Fallback nếu KEY_TAKEAWAY kém**: Nếu takeaway quá generic hoặc trống, dùng article title + plan description từ `_plan.md` thay thế. KHÔNG đọc article file chỉ để cải thiện takeaway.

### 5.2 Coverage Aggregation

Collect subagent coverage tables → aggregate into `analysis/_coverage.md`

**Process**: Subagent returns inline coverage (`COVERAGE: S01:ok S02*:faithful`) → Main agent enriches to 4-column (`Section | Assigned To | Used In | Status`) → Concatenate into `_coverage.md` → Add summary stats.

**Coverage file format**:

```markdown
## Section Coverage Matrix

| Section | Assigned To   | Used In       | Status        |
| ------- | ------------- | ------------- | ------------- |
| S01     | 01-article.md | 01-article.md | ✅ summarized |
| S02 ⭐  | 01-article.md | 01-article.md | ✅ faithful   |

- Total: {N} | Used: {N} | Missing: {N}
```

**Edge cases** (reassignment, shared sections, skipped): See [large-doc-processing.md#coverage-tracking](large-doc-processing.md#coverage-tracking).

Run validation:

```bash
{SCRIPTS_DIR}/wa-validate {book}/analysis/_coverage.md
```

## Step 6: Verify

### 6.1 Coverage Check

**Soft target**: Coverage nên đạt >=95% (không bắt buộc retry)

```
Coverage results:
├─ >= 95% → PASS (tiếp tục)
├─ 90-94% → WARNING (ghi nhận, không retry tự động)
│   └─ Chỉ retry nếu user yêu cầu
├─ < 90% → ASK USER
│   └─ Option 1: Accept as-is
│   └─ Option 2: Retry specific articles
│   └─ Option 3: Create supplementary
```

**QUAN TRỌNG**: Không tự động retry để đạt coverage target. Việc retry tốn token và thời gian, thường không cải thiện đáng kể.

### 6.2 Quality Checklist

Verify từ subagent returns + overview file (KHÔNG cần đọc article files):

- [ ] All RESULT: PASS (từ subagent returns)
- [ ] Overview updated with Key Takeaways and Series List (đọc `00-overview.md` ~600 words)
- [ ] All links in series lists verified (trong overview file)
- [ ] _coverage.md reported (>=95% target, >=90% acceptable)
- [ ] Critical ⭐ sections: spot-check source fidelity từ coverage
- [ ] Warnings logged for any skipped sections
- [ ] Anti-AI writing rules passed (xem [article-writer-prompt.md](article-writer-prompt.md))

### 6.3 Error Recovery (User-Driven)

> **Policy**: Không tự động retry. Mọi lỗi đều report cho user và chờ quyết định. See [retry-workflow.md](retry-workflow.md).

## Content Guidelines

**Key rules**: Source fidelity (rewrite, don't copy), ⭐ critical sections = faithful rewrite 100%, Anti-AI writing (no em dash, no AI vocabulary), NO tables/diagrams in output, MỖI article PHẢI có "## Các bài viết trong series" ở cuối. Full details: [article-writer-prompt.md](article-writer-prompt.md).
