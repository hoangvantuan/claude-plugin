---
name: professional
category: analytical
best_for:
  - Technical reports
  - Business proposals
  - Research summaries
  - Case studies
  - White papers
  - Technology analysis
  - Experiment reports
reading_level: intermediate
formality: high
difficulty: medium
version: 2.0.0
---
# Professional (Chuyên Nghiệp)

## Philosophy

Viết như một chuyên gia đang trình bày cho đồng nghiệp. Mục tiêu: truyền tải thông tin chính xác, có cấu trúc, và đáng tin cậy. Khi phù hợp, sử dụng thử nghiệm trực tiếp làm bằng chứng bên cạnh data và research.

**Nguyên tắc:** Chính xác > Cảm xúc | Bằng chứng > Ý kiến | Rõ ràng > Hoa mỹ | Accessible > Academic

## Voice

Xưng **"tác giả"** hoặc **không xưng** (passive voice khi cần). Giọng điệu khách quan, trung lập, có thẩm quyền nhưng không kiêu ngạo. Tự tin nhưng cân bằng, thừa nhận giới hạn khi cần.

## Structure

### 1. Opening (Executive Summary)

- Insight chính ngay câu đầu tiên (BLUF)
- Bối cảnh ngắn gọn nếu cần
- Roadmap: người đọc sẽ thu được gì?

### 2. Development (Evidence-Based)

- **Evidence**: Dữ liệu, nghiên cứu, case study, kết quả thử nghiệm
- **Analysis**: Phân tích ý nghĩa của evidence
- **Implications**: Hàm ý và ứng dụng

Mỗi phần có:
- Heading rõ ràng
- Transition logic giữa các ý
- Citations khi cần thiết
- Balance: cả cơ hội và giới hạn

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
- Mix câu ngắn mạnh (5-10 từ) và câu chi tiết (15-25 từ) tạo rhythm
- Giải thích thuật ngữ phức tạp bằng ngôn ngữ đơn giản khi cần

### DON'T

- Từ cảm xúc: "tuyệt vời", "đáng kinh ngạc"
- Hedging quá mức: "có thể", "hình như", "sort of"
- Colloquialisms và slang
- Anecdotes cá nhân làm bằng chứng chính
- Câu mơ hồ, không kiểm chứng được
- Chỉ lạc quan hoặc chỉ bi quan, cần balance
- Em dash (—), thay bằng dấu phẩy, dấu hai chấm, hoặc tách câu
- AI vocabulary: "bức tranh toàn cảnh", "hệ sinh thái", "đa chiều", "toàn diện và sâu sắc", "delve", "tapestry", "landscape", "leverage"
- Câu đều tăm tắp cùng độ dài. Xen kẽ câu ngắn mạnh (5-10 từ) và câu phân tích dài (15-25 từ)
- Triple-listing mọi lúc. Dùng 2, 4, 5 items khi tự nhiên
- Từ Hán-Việt khi có từ thuần Việt tương đương: "tối ưu hóa" thay vì "chạy tốt hơn", "cung cấp khả năng" thay vì "giúp"

## Example

> **Executive Summary**: Triển khai automated testing giảm 47% sự cố production trong 6 tháng.
>
> **Phân tích**: Dữ liệu từ deployment logs cho thấy việc phát hiện sớm integration failures đóng góp phần lớn vào việc ngăn ngừa sự cố. Cụ thể, 78% các issues được bắt tại CI/CD pipeline, trước khi đến môi trường staging.
>
> Tuy nhiên, automated testing không thay thế hoàn toàn manual QA. Kết quả thử nghiệm trên 3 teams cho thấy: teams kết hợp cả hai phương pháp giảm 62% sự cố, trong khi teams chỉ dùng automated testing giảm 47%.
>
> **Khuyến nghị**: Triển khai hybrid approach: automated cho regression, manual cho UX và edge cases. Ưu tiên integration tests cho API endpoints có traffic cao nhất.

## Common Mistakes

### Wrong

> Automated testing là một công nghệ tuyệt vời và đáng kinh ngạc. Nó giúp cải thiện đáng kể chất lượng phần mềm. Nhiều công ty đã áp dụng và thấy kết quả rất tốt. Chúng ta nên triển khai ngay.

**Why wrong:** Từ cảm xúc ("tuyệt vời", "đáng kinh ngạc"), vague claims ("đáng kể", "rất tốt"), không có data, không có nuance.

### Correct

> [Xem Example: mỗi claim có data, có nuance, có recommendation cụ thể]

## Core Techniques

### 1. BLUF (Bottom Line Up Front)

Kết luận đầu tiên, chi tiết sau:

> **Pattern**: "[Kết luận chính + metric]. Cụ thể, [evidence]. Do đó, [recommendation]."

### 2. Evidence Hierarchy

Sắp xếp evidence theo độ tin cậy:

| Tier       | Loại Evidence                       | Khi nào dùng               |
| ---------- | ----------------------------------- | -------------------------- |
| **Tier 1** | Meta-analyses, systematic reviews   | Khẳng định chắc chắn       |
| **Tier 2** | Controlled trials, A/B tests        | Kết luận mạnh              |
| **Tier 3** | Observational studies, experiments  | Supporting evidence         |
| **Tier 4** | Case studies, expert opinions       | Minh họa, context          |

### 3. Structured Argumentation (Minto Pyramid)

Governing Thought → Key Points → Supporting Evidence. Mỗi layer phải support layer trên.

### 4. Precision Language

| Thay vì               | Dùng                                    |
| ---------------------- | --------------------------------------- |
| "nhiều"               | "67%" hoặc "majority (>50%)"           |
| "gần đây"             | "Q4 2024" hoặc "trong 6 tháng qua"    |
| "cải thiện đáng kể"    | "cải thiện 23% so với baseline"         |
| "một số nghiên cứu"    | "[Author, Year]" hoặc "N=3 studies"    |

### 5. Experimentation as Evidence

Khi có kết quả thử nghiệm trực tiếp, trình bày như evidence:

> **Pattern**: "[Mô tả thử nghiệm] → [Kết quả quan sát] → [Implications] → [Giới hạn]"

Luôn kèm giới hạn: sample size, điều kiện, reproducibility.

### 6. Balance Optimism with Caution

| Aspect       | Cách thể hiện                            |
| ------------ | ---------------------------------------- |
| **Tiềm năng** | "Kết quả cho thấy tiềm năng đáng kể..." |
| **Giới hạn**  | "...tuy nhiên, cần xem xét [factors]"    |
| **Rủi ro**    | "Rủi ro chính bao gồm..."               |
| **Cơ hội**    | "Cơ hội áp dụng nếu [điều kiện]"        |

## Transition Phrases

| Mục đích          | Cụm từ                                              |
| ----------------- | ---------------------------------------------------- |
| Giới thiệu evidence | "Dữ liệu cho thấy...", "Nghiên cứu indicates..."   |
| Phân tích         | "Điều này suggests...", "Phân tích reveals..."        |
| Contrast          | "Tuy nhiên,", "Ngược lại,", "Mặt khác,"             |
| Causation         | "Do đó,", "Kết quả là,", "Dẫn đến,"                 |
| Conclusion        | "Tóm lại,", "Kết luận,", "Dựa trên analysis,"       |
| Recommendation    | "Khuyến nghị:", "Đề xuất:", "Next steps:"             |
| Experimentation   | "Kết quả thử nghiệm cho thấy...", "Testing reveals..." |

## Tone Calibration

| Ngữ cảnh             | Tone                     | Ví dụ                                                |
| -------------------- | ------------------------ | ---------------------------------------------------- |
| **Technical report**  | Formal, data-heavy       | "Kết quả benchmark cho thấy throughput tăng 2.3x..." |
| **Business proposal** | Confident, benefit-focused | "Giải pháp này sẽ giảm operational costs 15%..."     |
| **Analysis**          | Balanced, evidence-based | "Dữ liệu suggest rằng... tuy nhiên, cần xem xét..." |
| **Recommendation**    | Actionable, clear        | "Khuyến nghị: Triển khai Phase 1 trong Q2..."         |
| **Exploratory**       | Curious, grounded        | "Kết quả thử nghiệm gợi ý một hướng tiếp cận mới..." |

## Pacing Rules

| Yếu tố         | Quy tắc                                                      |
| --------------- | ------------------------------------------------------------ |
| Đoạn văn        | 3-6 câu, focused on one idea                                 |
| Câu             | Mix: ngắn (5-10 từ) cho punch, dài (15-25 từ) cho reasoning |
| Headings        | H2 cho major sections, H3 cho subsections                    |
| Lists           | Bullet cho items không thứ tự, number cho steps              |
| Structured data | Dùng bullet points cho so sánh, không dùng tables            |
| Data points     | Ít nhất 1/major claim                                        |

## Prompt Context (For AI)

When using this style, provide:

- **Audience**: Decision makers, professionals, technical teams cần thông tin chính xác
- **Purpose**: Inform, analyze, recommend: dựa trên evidence
- **Success criteria**: Mỗi claim có evidence, mỗi section có value, người đọc có thể action
- **Constraints**: Không emotional appeals, không vague claims, luôn có data hoặc evidence

## Quality Checklist

### Opening
- [ ] BLUF rõ ràng?
- [ ] Context đủ nhưng không thừa?
- [ ] Roadmap cho người đọc?

### Development
- [ ] Evidence-based cho mỗi claim?
- [ ] Analysis logic và consistent?
- [ ] Balance giữa opportunities và limitations?
- [ ] Technical terms được định nghĩa?

### Closing
- [ ] Summary cover key points?
- [ ] Conclusions dựa trên evidence?
- [ ] Recommendations actionable và specific?

### Overall
- [ ] Tone objective và professional?
- [ ] Không có emotional appeals?
- [ ] Mix câu ngắn + dài tạo rhythm?
- [ ] Format consistent?

## Inspiration

Barbara Minto (Pyramid Principle) • McKinsey Style • Harvard Business Review • The Economist • Paul Graham • Ben Thompson (Stratechery) • Nature/Science journals
