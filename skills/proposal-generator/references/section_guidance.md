# Hướng dẫn viết theo từng section

Ví dụ tốt/xấu cụ thể cho từng section. Đọc subsection liên quan trước khi draft.

---

## Tóm tắt điều hành (Executive Summary)

**Mục tiêu**: Một reader cấp C đọc duy nhất trang này quyết định được có đọc tiếp hay không.

**Ví dụ tệ**:
> Trong thời đại số phát triển nhanh chóng ngày nay, doanh nghiệp cần ứng dụng công nghệ tiên tiến để duy trì lợi thế cạnh tranh. Chúng tôi đề xuất một giải pháp toàn diện sẽ chuyển đổi vận hành và thúc đẩy đổi mới sáng tạo trên toàn doanh nghiệp.

**Vì sao tệ**: không có chi tiết cụ thể, văn phong AI, không nói lên điều gì.

**Ví dụ tốt**:
> ACME hiện chi khoảng 2,4 tỷ VND/năm cho việc xử lý hóa đơn thủ công với 14 nhân sự kế toán. Chúng tôi đề xuất dự án 6 tháng triển khai nền tảng tự động hóa hóa đơn có hỗ trợ AI, dự kiến giảm 75% công việc thủ công, tiết kiệm khoảng 1,8 tỷ VND/năm và rút ngắn chu kỳ invoice-to-payment từ 9 ngày xuống dưới 3 ngày. Đầu tư: 480 triệu VND. Payback dự kiến: dưới 4 tháng.

**Vì sao tốt**: số cụ thể, vấn đề cụ thể, kết quả cụ thể, ROI gói gọn trong một câu.

---

## Vấn đề (Problem Statement)

**Mục tiêu**: Khiến reader cảm nhận được vấn đề một cách trực quan trước khi đưa giải pháp.

**Ví dụ tệ**:
> Công ty đang gặp những thách thức với hệ thống và quy trình hiện tại làm hạn chế hiệu quả vận hành.

**Ví dụ tốt**:
> Hệ thống order management hiện tại được build từ 2014 trên PHP 5.6, đã end-of-life từ 2018. Team báo cáo trung bình 3 production incident/tuần liên quan đến hệ thống, mỗi lần tốn 4-6 giờ của senior engineer để xử lý. Lead time cho feature request mới là 8-12 tuần vì thay đổi ở một module thường làm vỡ module khác. Tác động phía khách hàng: 17% đơn online thất bại tại bước checkout trong giờ cao điểm.

---

## Bối cảnh thị trường

**Mục tiêu**: Thể hiện rằng proposal được informed bởi bối cảnh thị trường, không phải nghĩ trong chân không.

Cần có:
- 1-2 câu về xu hướng thị trường, có số liệu cite
- 2-3 ví dụ giải pháp tương đương (gọi tên nếu là public)
- 1 câu về điểm khác biệt của approach trong proposal này

Bỏ qua nếu là proposal nội bộ thuần và market context không ảnh hưởng quyết định.

---

## Phương pháp đề xuất (Business View)

**Mục tiêu**: Reader phi kỹ thuật hiểu được đang build cái gì mà không cần thấy code hay jargon.

Test: đọc section này cho một project sponsor không viết code. Họ có hiểu không? Nếu không, viết lại.

**Ví dụ tệ**:
> Chúng tôi sẽ implement microservices-based event-driven architecture với Kafka, deploy trên Kubernetes với service mesh.

**Ví dụ tốt**:
> Chúng tôi sẽ thay hệ thống order monolithic hiện tại bằng cấu trúc module hóa, mỗi chức năng chính (catalog, cart, checkout, fulfillment) chạy độc lập. Điều này có nghĩa là sự cố ở một khu vực không còn kéo sập toàn site, và team có thể release cập nhật cho từng khu vực mà không cần re-test toàn bộ. Hệ thống mới sẽ host trên môi trường AWS hiện có của bạn.

Phần technical detail dành cho section sau.

---

## Solution Architecture

**Mục tiêu**: Senior engineer review xong và tin rằng team đề xuất biết họ đang làm gì.

Yêu cầu bắt buộc:
- Danh sách component kèm trách nhiệm mỗi component
- Mô tả data flow (ai gọi cái gì, theo thứ tự nào)
- Integration points (hệ thống ngoài, kèm protocol: REST, gRPC, event bus, file drop, v.v.)
- Deployment model

Nếu có diagram, prose vẫn phải mô tả diagram thể hiện gì. Nếu không có diagram, prose phải đủ structured để reader tự vẽ được diagram.

**Format mô tả diagram khi không có ảnh**:
```
Components:
  - API Gateway (entry point, authentication, rate limiting)
  - Order Service (REST + Kafka producer)
  - Payment Service (REST, talks to Stripe)
  - Notification Service (Kafka consumer, gửi email/SMS)
  - PostgreSQL (orders, payments)
  - Redis (session cache, rate limit counters)

Flow (đặt order):
  1. Client → API Gateway → Order Service (REST POST /orders)
  2. Order Service ghi PostgreSQL, publish order.created lên Kafka
  3. Payment Service consume order.created, gọi Stripe, publish payment.completed
  4. Notification Service consume payment.completed, gửi xác nhận
```

---

## Technology Stack

**Mục tiêu**: Lựa chọn cụ thể, có thể bảo vệ được. Không hand-wave kiểu "công nghệ hiện đại, scalable".

Mỗi dòng trong stack table phải pass test này: "Engineer ngồi cạnh tôi giải thích được vì sao chọn cái này thay vì alternative hiển nhiên không?"

**Dòng tệ**:
| Backend | Node.js | Hiện đại và scalable |

**Dòng tốt**:
| Backend | Node.js 22 LTS + Fastify | Team có 3+ năm kinh nghiệm Node; Fastify chọn thay Express vì native schema validation và throughput tốt hơn ~30% trên workload JSON-heavy mà chúng tôi dự kiến ở đây |

---

## Yêu cầu phi chức năng (NFR)

**Mục tiêu**: Target đo được, không phải nguyện vọng.

**Tệ**: "Hệ thống sẽ nhanh và scalable."

**Tốt**:
- p95 read latency < 300ms, p95 write latency < 800ms dưới load 500 RPS
- Horizontally scalable lên 5,000 RPS không cần đổi architecture
- 99.9% monthly uptime SLA (tương đương 43 phút downtime/tháng)
- Toàn bộ PII encrypt at rest (AES-256) và in transit (TLS 1.3)
- Mọi access auditable trong 90 ngày; lưu 1 năm cho compliance event

---

## Kế hoạch delivery

**Mục tiêu**: Plan thực tế, có phase, một PM đọc là chạy được.

Pitfall thường gặp:
- Underestimate UAT và bug-fix cycle (luôn pad)
- Quên environment setup, security review, data migration
- Chỉ liệt kê milestone "happy path"

Phải có rõ ràng:
- Phase discovery / kickoff
- Setup environment và tooling
- Build phase (chia thành các increment shippable)
- Phase integration / system test
- Phase UAT với khách hàng
- Production cutover
- Hypercare / warranty period

---

## Cấu trúc team

**Mục tiêu**: Khách hàng nhìn được chính xác ai đang làm dự án, role gì, allocation bao nhiêu.

Format:
| Vai trò | FTE | Phase | Ghi chú |
|---|---|---|---|
| Project Manager | 0,5 | Tất cả | Single point of contact |
| Tech Lead | 1,0 | Tất cả | Architecture decision, code review |
| Backend Engineers | 2,0 | Build phase | 1 senior, 1 mid |
| ... | ... | ... | ... |

State mix onshore/offshore nếu liên quan. Khách hàng thường quan tâm.

---

## QA Approach

**Mục tiêu**: Thể hiện chất lượng được build-in từ đầu, không phải bolt-on.

Lean vào test pyramid (70% unit, 20% integration, 10% E2E): điều chỉnh tỷ lệ theo loại dự án nhưng nói rõ lý do.

Yêu cầu bắt buộc:
- Target unit test coverage (ví dụ: 80% line coverage trên business logic, 60% tổng thể)
- Phạm vi integration test (boundary nào được test)
- Phạm vi E2E test (user journey nào)
- Plan performance test (load test trước mỗi major release)
- Plan security test (SAST trong CI, DAST trước production, penetration test trước go-live)
- Tooling (framework cụ thể, không phải "tool chuẩn ngành")

Nếu QA là win theme, đây là section để thể hiện. Dành cho nó độ dài thật sự.

---

## Rủi ro & giảm thiểu

**Mục tiêu**: Thể hiện sự chín chắn. Proposal không liệt kê rủi ro trông ngây thơ.

Mỗi dòng phải có biện pháp cụ thể, hành động được: không phải "sẽ giám sát chặt".

**Dòng tệ**:
| Trượt deadline | Trung bình | Cao | Sẽ giám sát chặt |

**Dòng tốt**:
| Rate limit của 3rd-party API gây fail data sync | Trung bình | Cao | Implement queueing + retry với exponential backoff ở Phase 1; thương lượng tier rate cao hơn với vendor trước Phase 2; build fallback sang nightly batch sync |

Hướng tới 5-8 dòng. Nhiều hơn trông như filler; ít hơn trông như chối bỏ rủi ro.

---

## Business Case / ROI

**Mục tiêu**: Diễn giải dự án thành ngôn ngữ tài chính mà CFO ký được.

Cấu trúc:
1. **Đầu tư**: tổng chi phí (project + N năm run cost), tách capex/opex nếu liên quan
2. **Lợi ích định lượng**: tiết kiệm chi phí, tăng doanh thu, giảm rủi ro: kèm assumption
3. **Payback period**: số tháng hoàn vốn
4. **Sensitivity**: kết quả thay đổi sao nếu lợi ích thấp hơn kỳ vọng 30%

Nếu chưa có số chính xác, đưa ra khoảng và state assumption đầu vào nào dẫn dắt kết quả. Tốt hơn nói "tiết kiệm 1,2-1,8 tỷ VND tùy tỷ lệ adoption" thay vì bịa "đúng 1,5 tỷ VND".

---

## Pricing

**Mục tiêu**: Rõ ràng, dễ scan, không có surprise.

Format tốt nhất: bảng tóm tắt ở đầu, line item ở dưới.

Luôn nói rõ:
- Mô hình giá nào (fixed, T&M, milestone)
- Cái gì IN scope ở giá này
- Cái gì OUT scope (sẽ là change request)
- Lịch thanh toán
- Đơn vị tiền và đã bao gồm thuế hay chưa

Cẩn thận khi đưa con số chính xác mà chưa confirm với finance/sales: khi generate, dùng khoảng hoặc placeholder kiểu `[XXX triệu VND: sẽ confirm]` nếu user chưa cung cấp giá.

---

## Why Us

**Mục tiêu**: 3-5 lý do, mỗi lý do có evidence backup.

**Tệ**: "Chúng tôi đam mê công nghệ và customer success."

**Tốt**:
- "Đã deliver 3 dự án invoice automation tương tự trong 2 năm qua cho khách [ngành], bao gồm [reference cụ thể nếu được phép]; trung bình go-live sớm 2 tuần so với plan."
- "Practice QA in-house với automation engineer riêng: dự án điển hình ship với 80%+ test coverage và zero P1 defect trong 90 ngày đầu post-launch."
- "[Accelerator/framework cụ thể] giảm thời gian setup khoảng 40% cho lớp dự án này."

---

## Giả định & Phụ thuộc

**Mục tiêu**: Bảo vệ scope và timeline. Mọi thứ proposal giả định là đúng phải nằm ở đây. Khi giả định sai, đây là cơ sở cho change request.

**Ví dụ giả định tệ**:
> Mọi thứ sẽ suôn sẻ.

**Ví dụ giả định tốt**:
> - Hệ thống CRM hiện tại có REST API documentation cập nhật, cho phép integration không cần reverse-engineer
> - Volume dữ liệu xử lý không vượt 500K records/ngày trong 12 tháng đầu
> - Khách hàng cung cấp test account cho tất cả third-party system trong vòng 2 tuần từ kickoff
> - Không phát sinh yêu cầu compliance mới ngoài GDPR và Nghị định 13/2023 đã nêu

**Phụ thuộc từ phía khách hàng**: liệt kê cụ thể cái gì cần, khi nào, hậu quả nếu trễ. Đừng viết "cần hỗ trợ từ khách hàng" chung chung. Viết "Key stakeholder (tên hoặc vai trò) available tối thiểu 4 giờ/tuần cho sprint review và UAT feedback. Nếu không available, quyết định bị trì hoãn, timeline dịch tương ứng."

---

## Business Case / ROI (phiên bản nâng cao)

**Mục tiêu**: Section quyết định dự án có được duyệt hay không. CFO đọc section này đầu tiên (sau Executive Summary).

### Cost of Inaction (chi phí không hành động)

Luôn bắt đầu ROI bằng câu hỏi: "Nếu không làm gì, tổ chức mất bao nhiêu?"

**Ví dụ tệ**:
> Nếu không triển khai, công ty sẽ tiếp tục gặp khó khăn.

**Ví dụ tốt**:
> Mỗi tháng delay, ACME tiếp tục chi 200 triệu VND cho 14 nhân sự xử lý hóa đơn thủ công. Trong 12 tháng tới, tổng chi phí không hành động ước tính 2,4 tỷ VND, chưa tính rủi ro sai sót (hiện 3,2% error rate trên invoices) và chi phí cơ hội khi 14 nhân sự không thể chuyển sang công việc giá trị cao hơn. Ngoài ra, quy định hóa đơn điện tử bắt buộc từ Q3/2026 đặt deadline cứng: không tuân thủ = phạt hành chính.

### TCO Comparison

So sánh tổng chi phí sở hữu 3-5 năm giữa "giữ nguyên" và "triển khai". Bao gồm cả chi phí ẩn: nhân sự vận hành, license, hạ tầng, opportunity cost.

### Sensitivity Analysis

Trình bày 3 kịch bản (lạc quan, cơ sở, bi quan). Thay đổi 1-2 biến đầu vào chính (tỷ lệ adoption, mức tiết kiệm). Nếu kịch bản bi quan vẫn có ROI dương, proposal rất mạnh. Nếu bi quan cho ROI âm, thẳng thắn nói và đề xuất phasing nhỏ hơn để giảm rủi ro.

---

## Mô hình quản trị dự án (Governance Model)

**Mục tiêu**: Khách hàng enterprise cần thấy cấu trúc quản trị rõ ràng. Thiếu section này cho dự án 6+ tháng trông không chuyên nghiệp.

**Ví dụ tệ**:
> Chúng tôi sẽ họp định kỳ và báo cáo tiến độ.

**Ví dụ tốt**:
> **Steering Committee** (Sponsor + PM + Tech Lead cả hai phía): họp 2 tuần/lần, 60 phút. Phê duyệt scope change, unblock quyết định chiến lược, review tiến độ tổng quan.
>
> **Weekly Status** (PM + Team leads): 30 phút mỗi thứ Hai. Review sprint progress, highlight blocker, plan tuần tới.
>
> **Escalation**: Cấp 1 (Team lead, 24h) → Cấp 2 (PM + Steering Committee, 48h) → Cấp 3 (Sponsor/C-level, 1 tuần).

Bao gồm RACI matrix cho 5-7 quyết định chính (scope change, tech decision, UAT sign-off, go-live approval). RACI đầy đủ đặt ở phụ lục.

Cho POC hoặc dự án dưới 3 tháng: ghi 1-2 dòng "Weekly sync với [vai trò], escalation qua [kênh]" là đủ.

---

## Quản lý thay đổi (Change Management)

**Mục tiêu**: Thể hiện hiểu rằng dự án thành công không chỉ về code mà về adoption. 70% dự án transformation thất bại vì con người, không phải kỹ thuật.

**Khi nào cần section này**: Dự án thay đổi workflow người dùng cuối, hoặc ảnh hưởng cách hàng chục người làm việc hàng ngày. Bỏ qua cho dự án backend thuần, API integration, hoặc internal tooling cho dev team.

**Ví dụ tệ**:
> Chúng tôi sẽ training user trước go-live.

**Ví dụ tốt**:
> **Training Plan**: 3 nhóm user với nội dung và hình thức khác nhau.
> - Admin (5 người): workshop 2 ngày hands-on, 2 tuần trước go-live. Bao gồm troubleshooting guide.
> - End user (120 người): 4 giờ video training + lab thực hành, 1 tuần trước go-live. Material bằng tiếng Việt, quay screen recording trên data thật (đã anonymize).
> - IT Support (3 người): 1 ngày technical workshop về monitoring, log analysis, common issues.
>
> **Adoption Metrics**: Track % login tuần 1 (target >80%), % giao dịch qua hệ thống mới tháng 1 (target >60%), trend support ticket tháng 1-3 (kỳ vọng giảm 50%).
>
> **Fallback**: Hệ thống cũ vẫn hoạt động song song trong 30 ngày đầu. Nếu adoption dưới 40% sau tháng 1, kích hoạt plan B: on-site champion program với 1 super-user mỗi phòng ban.

---

## Phasing Strategy (Chiến lược phân kỳ)

**Mục tiêu**: Cho dự án lớn, giải thích vì sao chia phase như vậy, không chỉ liệt kê phase.

3 nguyên tắc phân kỳ:

1. **Quick win trước**: Phase 1 phải deliver giá trị đo được sớm nhất có thể. Stakeholder cần thấy kết quả để tiếp tục invest. Ví dụ: Phase 1 tự động hóa quy trình tốn thời gian nhất, Phase 2 mở rộng ra các quy trình còn lại.

2. **Rủi ro kỹ thuật cao đẩy sớm**: Nếu integration với hệ thống legacy là phần khó nhất, đặt ở Phase 1. Thất bại sớm rẻ hơn thất bại muộn. Đừng để phần khó nhất ở cuối rồi phát hiện infeasible khi đã tốn 80% budget.

3. **Phase sau tự chứng minh bằng kết quả Phase trước**: Mỗi phase end là checkpoint. Stakeholder quyết định tiếp tục dựa trên kết quả thực tế, không chỉ promise.

**Ví dụ phân kỳ xấu**:
> Phase 1: Thiết kế. Phase 2: Development. Phase 3: Testing. Phase 4: Go-live.

Vì sao xấu: phase theo hoạt động, không theo giá trị. Phase 1 không deliver gì cho user. Nếu budget bị cắt sau Phase 2, không có gì chạy được.

**Ví dụ phân kỳ tốt**:
> Phase 1 (3 tháng): Tự động hóa invoice processing, module tốn nhất hiện tại (14 nhân sự, 200M/tháng). Deliver: hệ thống xử lý 80% invoice tự động, dashboard tracking. Quick win: tiết kiệm ngay 100M/tháng.
>
> Phase 2 (2 tháng): Mở rộng sang purchase order và expense report. Leverage platform Phase 1. Deliver: end-to-end procurement automation.
>
> Phase 3 (2 tháng): Analytics dashboard cho CFO, predictive cash flow. Deliver: executive visibility.

Mỗi phase có deliverable độc lập, có giá trị riêng, không phụ thuộc phase sau mới chạy được.

---

## Style note xuyên suốt

- Dùng ngôi thứ nhất số nhiều ("chúng tôi sẽ deliver") nhất quán cho team đề xuất
- Dùng ngôi thứ hai ("bạn", "team của bạn") tiết kiệm khi nói với khách hàng
- Không đổi thì lung tung: thì tương lai cho plan, hiện tại cho current state, quá khứ cho evidence
- Bảng rất tốt cho stack, team, risks, pricing, NFR, milestone: đừng ngại dùng
- Heading phải informative, không cute: "Solution Architecture" thay vì "Bí mật bên trong"

### Lưu ý về cách viết tiếng Việt cho proposal

- **Số liệu**: dùng dấu phẩy cho thập phân (1,5 tỷ thay vì 1.5 tỷ); có thể giữ format quốc tế nếu khách hàng quốc tế
- **Tiền tệ**: VND, USD viết tắt; nếu mix hai loại trong proposal thì state tỷ giá assumption ở đầu Pricing section
- **Anglicism**: chấp nhận thuật ngữ tech tiếng Anh khi đó là từ ngữ chuẩn trong industry (API, microservices, deployment); dịch khi từ tiếng Việt tự nhiên hơn (rủi ro, lợi ích, nhân sự, ngân sách)
- **Câu**: tránh câu quá dài kiểu dịch máy. Nếu một câu vượt 3 dòng, tách ra