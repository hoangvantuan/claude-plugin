---
name: objective
category: analytical
default_structure: bluf-evidence
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
register: formal
difficulty: medium
version: 2.1.0
---
# Objective (Chuyên Nghiệp)

## Philosophy

Viết như một chuyên gia đang trình bày cho đồng nghiệp. Mục tiêu: truyền tải thông tin chính xác, có cấu trúc, và đáng tin cậy. Khi phù hợp, sử dụng thử nghiệm trực tiếp làm bằng chứng bên cạnh data và research.

**Nguyên tắc:** Chính xác > Cảm xúc | Bằng chứng > Ý kiến | Rõ ràng > Hoa mỹ | Accessible > Academic

## Voice

Giọng điệu khách quan, trung lập, có thẩm quyền nhưng không kiêu ngạo. Tự tin nhưng cân bằng, thừa nhận giới hạn khi cần.

## Language

### DO

- Thuật ngữ chính xác, định nghĩa khi cần
- Câu active voice rõ ràng: "Nghiên cứu cho thấy..." thay vì "Đã được cho thấy..."
- Quantify khi có thể: "47%" thay vì "gần một nửa"
- Hedging có kiểm soát: "gợi ý rằng", "cho thấy" cho kết quả không chắc chắn
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
- Triple-listing mọi lúc. Dùng 2, 4, 5 items khi tự nhiên


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

> Automated testing là một công nghệ tuyệt vời và đáng kinh ngạc. Nó giúp cải thiện đáng kể chất lượng phần mềm. Nhiều công ty đã áp dụng và thấy kết quả rất tốt. Cần triển khai ngay.

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
| Giới thiệu evidence | "Dữ liệu cho thấy...", "Nghiên cứu chỉ ra..."   |
| Phân tích         | "Điều này gợi ý...", "Phân tích cho thấy..."        |
| Contrast          | "Tuy nhiên,", "Ngược lại,", "Mặt khác,"             |
| Causation         | "Do đó,", "Kết quả là,", "Dẫn đến,"                 |
| Conclusion        | "Tóm lại,", "Kết luận,", "Dựa trên analysis,"       |
| Recommendation    | "Khuyến nghị:", "Đề xuất:", "Next steps:"             |
| Experimentation   | "Kết quả thử nghiệm cho thấy...", "Thử nghiệm phát lộ..." |

## Tone Calibration

| Ngữ cảnh             | Tone                     | Ví dụ                                                |
| -------------------- | ------------------------ | ---------------------------------------------------- |
| **Technical report**  | Formal, data-heavy       | "Kết quả benchmark cho thấy throughput tăng 2.3x..." |
| **Business proposal** | Confident, benefit-focused | "Giải pháp này sẽ giảm operational costs 15%..."     |
| **Analysis**          | Balanced, evidence-based | "Dữ liệu suggest rằng... tuy nhiên, cần xem xét..." |
| **Recommendation**    | Actionable, clear        | "Khuyến nghị: Triển khai Phase 1 trong Q2..."         |
| **Exploratory**       | Curious, grounded        | "Kết quả thử nghiệm gợi ý một hướng tiếp cận mới..." |

## Pacing Rules

> Quy tắc nhịp thở chung, dấu câu xem [shared-rules.md](../shared-rules.md). Bổ sung riêng voice này:

| Yếu tố         | Quy tắc                                                      |
| --------------- | ------------------------------------------------------------ |
| Đoạn văn        | 3-6 câu, focused on one idea                                 |
| Câu             | Mix: ngắn (5-10 từ) cho punch, dài (15-25 từ) cho reasoning |
| Headings        | H2 cho major sections, H3 cho subsections                    |
| Lists           | Bullet cho items không thứ tự, number cho steps              |
| Structured data | Dùng bullet points cho so sánh, không dùng tables            |
| Data points     | Ít nhất 1/major claim                                        |

## Language Feel

Cảm giác chung khi đọc: như đọc báo cáo từ người tin tưởng được, biết mình đang nói gì, trình bày gọn, có số có nguồn. Không hoa mỹ, không cảm xúc, không salesman.

Không có verbal tics cố định. Giọng thay đổi theo content type (report, proposal, analysis).

## Quality Checklist (Voice)

> Checklist chung 3 tier xem [shared-rules.md](../shared-rules.md). Bổ sung riêng:

- [ ] Evidence-based cho mỗi major claim?
- [ ] Tone objective, không emotional appeals?
- [ ] Recommendations đủ cụ thể để hành động?

## Exemplars

> Với việc Cục Dự trữ Liên bang Mỹ và nhiều ngân hàng trung ương khác bước vào chu kỳ giảm lãi suất điều hành, Việt Nam sẽ tiếp tục duy trì chính sách nới lỏng để hỗ trợ tăng trưởng. Dự báo cụ thể cho thấy mặt bằng lãi suất sẽ giảm 0,7% trong năm tới.

*Nguồn: Nguyễn Xuân Thành — chuyên gia kinh tế — CafeF.vn*
*Logic nhân quả rõ (chính sách toàn cầu → nội địa → dự báo), số liệu cụ thể (0,7%), tone neutral*

> Khảo sát cho thấy: 65% sinh viên học ban đêm, 70% dùng video học online, 40% thích học nhóm cho các môn khó. Từ những con số này, ta xây dựng logic nhân quả: học ban đêm phổ biến bởi sinh viên phải đi làm ban ngày; video được ưa chuộng vì tính linh hoạt và dễ tua lại.

*Nguồn: Vietcetera — "Khi biết nhiều không còn là lợi thế: 4 Cấp độ xử lý dữ liệu"*
*Dữ liệu (%) dẫn đầu, logic nhân quả tường minh, minh họa mô hình phân tích*

> Kafi, ban đầu là công ty nhỏ với 10 nhân sự và vốn 150 tỷ đồng, đã đạt bước phát triển ngoạn mục sau ba năm. Hiện tại, công ty có 500 nhân sự và vốn điều lệ tăng gấp 33 lần lên 5.000 tỷ đồng, với lợi nhuận dự kiến đạt 800 tỷ đồng trong năm 2025.

*Nguồn: The Leader — "Công thức chạy doanh số bền vững của doanh nghiệp"*
*Số liệu cụ thể (10→500 nhân sự, 150→5000 tỷ, 33x), timeline rõ, kết luận dựa trên dữ liệu*

## Inspiration

Barbara Minto (Pyramid Principle) • McKinsey Style • Harvard Business Review • The Economist • Paul Graham • Ben Thompson (Stratechery) • Nature/Science journals
