---
name: professional
category: analytical
best_for:
  - Technical reports
  - Business proposals
  - Research summaries
  - Case studies
  - White papers
reading_level: intermediate
formality: high
difficulty: medium
version: 1.1.0
---
# Professional (Chuyên Nghiệp)

## Philosophy

Viết như một chuyên gia đang trình bày cho đồng nghiệp. Mục tiêu: truyền tải thông tin chính xác, có cấu trúc, và đáng tin cậy.

**Nguyên tắc:** Chính xác > Cảm xúc | Bằng chứng > Ý kiến | Rõ ràng > Hoa mỹ

## Voice

Xưng **"tác giả"** hoặc **không xưng** (passive voice khi cần). Giọng điệu khách quan, trung lập, có thẩm quyền nhưng không kiêu ngạo.

## Structure

### 1. Opening (Executive Summary)

- Insight chính ngay câu đầu tiên (BLUF)
- Bối cảnh ngắn gọn nếu cần
- Roadmap: người đọc sẽ thu được gì?

### 2. Development (Evidence-Based)

- **Evidence**: Dữ liệu, nghiên cứu, case study
- **Analysis**: Phân tích ý nghĩa của evidence
- **Implications**: Hàm ý và ứng dụng

Mỗi phần có:
- Heading rõ ràng
- Transition logic giữa các ý
- Citations khi cần thiết

### 3. Closing (Action-Oriented)

- Tóm tắt các điểm chính
- Kết luận dựa trên evidence
- Recommendations cụ thể, actionable

## Language

### DO

- Thuật ngữ chính xác, định nghĩa khi cần
- Câu active voice rõ ràng: "Nghiên cứu cho thấy..." thay vì "Đã được cho thấy..."
- Quantify khi có thể: "47%" thay vì "gần một nửa"
- Hedging có kiểm soát: "suggests", "indicates" cho kết quả không chắc chắn
- Parallel structure trong danh sách
- Câu 10-25 từ, tránh quá dài

### DON'T

- Từ cảm xúc: "tuyệt vời", "đáng kinh ngạc"
- Hedging quá mức: "có thể", "hình như", "sort of"
- Colloquialisms và slang
- Anecdotes cá nhân làm bằng chứng chính
- Câu mơ hồ, không kiểm chứng được

## Example

> **Executive Summary**: Triển khai automated testing giảm 47% sự cố production trong 6 tháng.
>
> **Phân tích**: Dữ liệu từ deployment logs cho thấy việc phát hiện sớm integration failures đóng góp phần lớn vào việc ngăn ngừa sự cố. Cụ thể, 78% các issues được bắt tại CI/CD pipeline, trước khi đến môi trường staging.
>
> **Khuyến nghị**: Các tổ chức áp dụng practices tương tự có thể kỳ vọng cải thiện tương đương trong quý đầu tiên triển khai. Ưu tiên integration tests cho các API endpoints có traffic cao nhất.

## Core Techniques

### 1. BLUF (Bottom Line Up Front)

Kết luận đầu tiên, chi tiết sau:

```
[Kết luận chính]
↓
[Bằng chứng hỗ trợ]
↓
[Phân tích chi tiết]
↓
[Khuyến nghị]
```

> **Pattern**: "X tăng/giảm Y% do Z. Cụ thể, [evidence]. Do đó, [recommendation]."

### 2. Evidence Hierarchy

Sắp xếp evidence theo độ tin cậy:

| Tier | Loại Evidence | Khi nào dùng |
| ---- | ------------- | ------------ |
| **Tier 1** | Meta-analyses, systematic reviews | Khẳng định chắc chắn |
| **Tier 2** | Randomized controlled trials | Kết luận mạnh |
| **Tier 3** | Observational studies, surveys | Supporting evidence |
| **Tier 4** | Case studies, expert opinions | Minh họa, context |

### 3. Structured Argumentation

Minto Pyramid cho lập luận phức tạp:

```
         [Governing Thought]
              /    |    \
     [Key Point] [Key Point] [Key Point]
        /  \       /  \        /  \
   [Support] [Support] [Support] [Support]
```

### 4. Precision Language

| Thay vì | Dùng |
| ------- | ---- |
| "nhiều" | "67%" hoặc "majority (>50%)" |
| "gần đây" | "Q4 2024" hoặc "trong 6 tháng qua" |
| "cải thiện đáng kể" | "cải thiện 23% so với baseline" |
| "một số nghiên cứu" | "[Author, Year]" hoặc "N=3 studies" |

## Tone Calibration

| Ngữ cảnh | Tone | Ví dụ |
| -------- | ---- | ----- |
| **Technical report** | Formal, data-heavy | "Kết quả benchmark cho thấy throughput tăng 2.3x..." |
| **Business proposal** | Confident, benefit-focused | "Giải pháp này sẽ giảm operational costs 15%..." |
| **Analysis** | Balanced, evidence-based | "Dữ liệu suggest rằng... tuy nhiên, cần xem xét..." |
| **Recommendation** | Actionable, clear | "Khuyến nghị: Triển khai Phase 1 trong Q2..." |

## Transition Phrases

| Mục đích | Cụm từ |
| -------- | ------ |
| Giới thiệu evidence | "Dữ liệu cho thấy...", "Nghiên cứu indicates..." |
| Phân tích | "Điều này suggests...", "Phân tích reveals..." |
| Contrast | "Tuy nhiên,", "Ngược lại,", "Mặt khác," |
| Causation | "Do đó,", "Kết quả là,", "Dẫn đến," |
| Conclusion | "Tóm lại,", "Kết luận,", "Dựa trên analysis," |
| Recommendation | "Khuyến nghị:", "Đề xuất:", "Next steps:" |

## Citation & Reference

### In-text Citations

- **(Author, Year)**: "...cognitive load theory (Sweller, 1988)."
- **Author (Year)**: "Kahneman (2011) argues that..."
- **Multiple sources**: "(Smith, 2020; Jones, 2021)"

### Data Attribution

- Internal data: "Theo internal analytics (Q4 2024)..."
- Third-party: "Theo báo cáo của McKinsey (2024)..."
- Survey: "Khảo sát N=500 respondents cho thấy..."

## Document Patterns

### Technical Analysis

```
1. Executive Summary
2. Background / Context
3. Methodology
4. Findings
   - Finding 1: [Evidence + Analysis]
   - Finding 2: [Evidence + Analysis]
5. Discussion
6. Recommendations
7. Appendix (nếu cần)
```

### Business Case

```
1. Problem Statement
2. Proposed Solution
3. Cost-Benefit Analysis
4. Risk Assessment
5. Implementation Plan
6. Metrics & KPIs
```

## Pacing Rules

| Yếu tố | Quy tắc |
| ------ | ------- |
| Đoạn văn | 3-6 câu, focused on one idea |
| Câu | 10-25 từ, avoid >30 từ |
| Headings | H2 cho major sections, H3 cho subsections |
| Lists | Bullet cho items không có thứ tự, number cho steps/rankings |
| Structured data | Dùng bullet points cho so sánh, không dùng tables |
| Data points | Ít nhất 1/major claim |

## Quality Checklist

### Opening
- [ ] BLUF rõ ràng?
- [ ] Context đủ nhưng không thừa?
- [ ] Roadmap cho người đọc?

### Development
- [ ] Evidence-based cho mỗi claim?
- [ ] Analysis logic và consistent?
- [ ] Transitions smooth giữa sections?
- [ ] Technical terms được định nghĩa?

### Closing
- [ ] Summary cover key points?
- [ ] Conclusions dựa trên evidence?
- [ ] Recommendations actionable và specific?

### Overall
- [ ] Tone objective và professional?
- [ ] Không có emotional appeals?
- [ ] Citations đầy đủ?
- [ ] Format consistent?

## Inspiration

Barbara Minto (Pyramid Principle) • McKinsey Style • Harvard Business Review • The Economist • Nature/Science journals
