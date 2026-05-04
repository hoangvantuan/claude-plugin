# Proposal Template (Mẫu cấu trúc proposal)

Đây là cấu trúc chuẩn. Dùng tất cả section trừ khi input chỉ rõ một section nào đó không liên quan (ví dụ: proposal nội bộ thì không cần section Commercial Terms).

Heading dùng tiếng Việt; thuật ngữ tech giữ nguyên tiếng Anh khi cần thiết để chính xác.

---

## 1. Trang bìa (Cover Page)

- Tên dự án
- Gửi đến: [khách hàng / phòng ban]
- Lập bởi: [team / công ty]
- Ngày và version
- Mức độ bảo mật (nếu có)

## 2. Tóm tắt điều hành (Executive Summary), tối đa 1 trang

Trang quan trọng nhất. Một executive bận rộn chỉ đọc trang này phải hiểu được:

- Đang giải quyết vấn đề gì
- Đề xuất làm gì
- Chi phí bao nhiêu (cho khoảng cũng được)
- Tác động kinh doanh là gì (định lượng)
- Bao giờ deliver xong

Viết section này CUỐI CÙNG, sau khi các phần khác đã xong.

## 3. Bối cảnh & Vấn đề (Background & Problem Statement)

- Bối cảnh: chuyện gì đang xảy ra ở phía khách hàng khiến đề tài này đáng làm bây giờ
- Vấn đề cụ thể, mô tả bằng số liệu cụ thể (không "cải thiện hiệu quả": đưa ra con số, ví dụ, pain point thực tế)
- Hậu quả nếu không làm gì (cost of inaction)

## 4. Bối cảnh thị trường & cạnh tranh (Market & Competitive Context)

- Quy mô / xu hướng thị trường nếu liên quan (cite nguồn)
- Các tổ chức tương đương đang làm gì
- Điều gì khác biệt của approach này

Bỏ qua section này nếu là proposal nội bộ thuần và market context không ảnh hưởng quyết định.

## 5. Phương pháp đề xuất: góc nhìn business (Proposed Approach: Business View)

Tóm tắt 1-2 trang **không kỹ thuật** về CÁI GÌ sẽ được build và CÁCH dự án vận hành. Reader là decision maker business, không phải engineer. Cover:

- Giải pháp nói bằng ngôn ngữ thông thường
- Các capability chính mà người dùng cuối thấy được
- Phasing (ví dụ: "Phase 1 deliver X vào Q3, Phase 2 thêm Y vào Q4")
- Cái gì giữ nguyên vs cái gì thay đổi đối với user/business

## 6. Solution Architecture: góc nhìn kỹ thuật

Section architecture thực sự, có diagram hoặc mô tả textual rõ ràng. Cover:

- Architecture high-level (component và cách kết nối)
- Data flow
- Integration points với hệ thống hiện tại
- Deployment model (cloud, on-prem, hybrid; gọi tên cloud service cụ thể nếu biết)
- Mô tả diagram inline nếu không có ảnh: mô tả component và mũi tên bằng prose

Cho .docx output, cố gắng có ít nhất 1 diagram nếu được. Nếu không generate được, mô tả bằng structured text và note rằng cần thêm diagram.

## 7. Technology Stack

Một stack cụ thể, có chính kiến, kèm lý do chọn. Tránh hand-waving kiểu "chúng tôi dùng công nghệ hiện đại". Format dưới dạng bảng:

| Tầng     | Lựa chọn                     | Lý do                         |
| -------- | ---------------------------- | ----------------------------- |
| Frontend | [framework + version cụ thể] | [lý do gắn với nhu cầu dự án] |
| Backend  | [framework cụ thể]           | [lý do]                       |
| Data     | [DB lựa chọn]                | [lý do]                       |
| Infra    | [cloud + service chính]      | [lý do]                       |
| ...      | ...                          | ...                           |


Chỉ liệt kê tầng liên quan đến dự án. Dự án data-heavy → mở rộng tầng data; mobile app → mở rộng tầng client.

## 8. Yêu cầu phi chức năng (Non-functional Requirements)

Mục tiêu cụ thể, đo được:

- Performance (ví dụ: p95 latency < 300ms cho read, < 800ms cho write)
- Scalability (ví dụ: hỗ trợ 10k concurrent users, 1M transaction/ngày)
- Availability (ví dụ: 99.9% uptime SLA)
- Security (model auth, encryption at rest/in transit, audit logging)
- Compliance (GDPR, HIPAA, PCI-DSS, Nghị định 13/2023, các quy định địa phương khác tùy domain)
- Observability (logging, metrics, alerting)

Nếu có mục chưa định nghĩa, đề xuất target và đánh dấu "for confirmation".

## 9. Kế hoạch delivery & timeline

- Phase hoặc sprint với deliverable cụ thể mỗi phase
- Milestone chính với ngày target (relative tới kickoff nếu chưa có ngày tuyệt đối)
- Phụ thuộc và critical path
- Acceptance criteria mỗi phase

Format dưới dạng bảng hoặc Gantt-style. Trung thực với timeline: pad cho integration testing và UAT.

## 10. Team & mô hình delivery

- Vai trò cần (PM, Tech Lead, BE, FE, QA, DevOps, v.v.) kèm mức FTE
- Mix onshore/offshore nếu liên quan
- Cadence giao tiếp (daily standup, weekly demo, monthly steering committee)
- Đường escalation

Nếu QA là một trong các win themes, đây là section để nhấn mạnh cấu trúc team QA và vai trò testing như differentiator.

## 11. Phương pháp QA (Quality Assurance Approach)

Section này xứng đáng có mục riêng cho mọi proposal kỹ thuật.

- Test strategy (tỷ lệ unit / integration / E2E: reference test pyramid)
- Approach và tooling cho test automation
- Performance testing và security testing
- Quy trình UAT và acceptance criteria
- Defect management

## 12. Rủi ro & biện pháp giảm thiểu (Risks & Mitigation)

Bảng top 5-8 rủi ro. Trung thực, proposal không có rủi ro trông ngây thơ.

| Rủi ro          | Khả năng | Tác động | Biện pháp          |
| --------------- | -------- | -------- | ------------------ |
| [rủi ro cụ thể] | C/T/T    | C/T/T    | [hành động cụ thể] |


Nhóm cần cân nhắc: technical risk, integration risk, data quality risk, schedule risk, vendor/dependency risk, change management risk.

## 13. Giả định & Phụ thuộc (Assumptions & Dependencies)

Section bảo vệ cả hai phía. Ghi rõ những gì proposal giả định là đúng, và những gì cần từ phía khách hàng.

### Giả định

Liệt kê các giả định đầu vào ảnh hưởng đến scope, timeline, pricing. Ví dụ:

- Hệ thống hiện tại có API documentation đầy đủ
- Data volume không vượt quá X records/ngày
- Team khách hàng có engineer hỗ trợ integration trong Phase 2
- Không có yêu cầu regulatory đặc biệt ngoài các quy định đã nêu

Mỗi giả định sai có thể dẫn đến change request. Nêu rõ để tránh dispute sau này.

### Phụ thuộc từ phía khách hàng

| Phụ thuộc                         | Cần trước phase | Deadline | Hậu quả nếu trễ               |
| --------------------------------- | --------------- | -------- | ----------------------------- |
| Cung cấp API credentials          | Phase 2         | Tuần 3   | Trễ 1 tuần/tuần trễ           |
| Staging environment sẵn sàng      | Phase 2         | Tuần 4   | Block integration testing     |
| Key stakeholder available 4h/tuần | Tất cả          | Ongoing  | Delay decision, trễ milestone |
| Sign-off UAT                      | Phase 4         | Tuần N   | Block go-live                 |


### Phụ thuộc bên thứ ba

Liệt kê vendor, API, service bên ngoài mà dự án phụ thuộc, kèm risk nếu vendor thay đổi terms hoặc downtime.

## 14. Business Case / ROI

Lập luận tài chính. Đây là section quyết định dự án có được duyệt hay không.

### Chi phí không hành động (Cost of Inaction)

Bắt đầu bằng câu hỏi: "Nếu không làm gì, mất bao nhiêu?" Ví dụ:

- Mỗi tháng delay mất X triệu do vận hành thủ công
- Rủi ro compliance penalty Y tỷ nếu không đáp ứng quy định trước deadline Z
- Mất cơ hội thị trường: đối thủ đã triển khai, mỗi quý chậm mất N% market share

Cost of inaction là đòn bẩy thuyết phục mạnh nhất. Không làm gì KHÔNG phải miễn phí.

### Tổng chi phí sở hữu (TCO Comparison)

So sánh tổng chi phí 3-5 năm giữa các phương án:

| Hạng mục                     | Giữ nguyên (as-is) | Phương án đề xuất | Ghi chú |
| ---------------------------- | ------------------ | ----------------- | ------- |
| Chi phí nhân sự vận hành/năm |                    |                   |         |
| Chi phí hạ tầng/năm          |                    |                   |         |
| Chi phí license/năm          |                    |                   |         |
| Chi phí triển khai (1 lần)   | 0                  |                   |         |
| Chi phí bảo trì/năm          |                    |                   |         |
| **Tổng 3 năm**               |                    |                   |         |


### Lợi ích kỳ vọng

- Lợi ích định lượng: tiết kiệm chi phí, tăng doanh thu, giảm rủi ro, tiết kiệm thời gian (kèm số cụ thể hoặc khoảng)
- Lợi ích phi tài chính: vị thế chiến lược, lợi thế cạnh tranh, năng lực mới, employee satisfaction

### Phân tích tài chính

- **Payback period**: số tháng hoàn vốn
- **ROI**: (lợi ích ròng / đầu tư) × 100%
- **NPV** (nếu đủ số liệu): dùng discount rate phù hợp với industry

### Sensitivity Analysis

Kết quả thay đổi thế nào nếu giả định không đúng:

| Kịch bản          | Thay đổi giả định                    | Payback | ROI |
| ----------------- | ------------------------------------ | ------- | --- |
| Lạc quan          | Adoption 90%, tiết kiệm cao          | X tháng | Y%  |
| Cơ sở (base case) | Adoption 70%, tiết kiệm trung bình   | X tháng | Y%  |
| Bi quan           | Adoption 50%, tiết kiệm thấp hơn 30% | X tháng | Y%  |


Nếu chưa có số chính xác, đưa ra khoảng và state assumption rõ ràng. "Tiết kiệm 1,2-1,8 tỷ VND tùy tỷ lệ adoption" tốt hơn bịa "đúng 1,5 tỷ VND".

## 15. Mô hình quản trị dự án (Governance Model)

Cho dự án mid-size trở lên. Bỏ qua cho POC hoặc dự án dưới 3 tháng / 5 người.

### Cấu trúc quản trị

| Cơ chế             | Thành phần                       | Tần suất               | Chức năng                                     |
| ------------------ | -------------------------------- | ---------------------- | --------------------------------------------- |
| Steering Committee | Sponsor + PM + Tech Lead (2 bên) | 2 tuần hoặc hàng tháng | Quyết định chiến lược, phê duyệt scope change |
| Weekly Status      | PM + Team leads (2 bên)          | Hàng tuần              | Theo dõi tiến độ, tháo gỡ blocker             |
| Daily Standup      | Dev team                         | Hàng ngày              | Đồng bộ công việc ngắn hạn                    |


### RACI cho quyết định chính

| Quyết định            | R (thực hiện)    | A (phê duyệt)      | C (tham vấn) | I (thông báo) |
| --------------------- | ---------------- | ------------------ | ------------ | ------------- |
| Thay đổi scope        | PM               | Steering Committee | Tech Lead    | Team          |
| Lựa chọn công nghệ    | Tech Lead        | CTO khách hàng     | Architect    | PM            |
| Nghiệm thu phase      | QA Lead          | Sponsor            | PM           | Team          |
| Escalation production | On-call engineer | Tech Lead          | PM           | Sponsor       |


### Quy trình escalation

3 cấp rõ ràng:

1. **Cấp 1**: Team lead giải quyết trong 24h làm việc
2. **Cấp 2**: PM escalation lên Steering Committee, giải quyết trong 48h
3. **Cấp 3**: Sponsor/C-level, giải quyết trong 1 tuần

## 16. Quản lý thay đổi (Change Management)

Cho dự án có ảnh hưởng đến người dùng cuối hoặc quy trình vận hành. Bỏ qua cho dự án backend thuần không thay đổi workflow người dùng.

### Training Plan

| Nhóm người dùng    | Nội dung training                 | Hình thức             | Thời lượng | Thời điểm            |
| ------------------ | --------------------------------- | --------------------- | ---------- | -------------------- |
| Admin / Super user | Quản trị hệ thống, cấu hình       | Hands-on workshop     | 2 ngày     | 2 tuần trước go-live |
| End user           | Quy trình mới, thao tác hàng ngày | Video + lab thực hành | 4 giờ      | 1 tuần trước go-live |
| IT Support         | Troubleshooting, monitoring       | Technical workshop    | 1 ngày     | Trước go-live        |


### Communication Plan

| Thời điểm            | Đối tượng              | Nội dung                             | Kênh              |
| -------------------- | ---------------------- | ------------------------------------ | ----------------- |
| Kickoff              | Toàn bộ bên liên quan  | Giới thiệu dự án, timeline, tác động | Town hall / email |
| Mỗi phase end        | Management + key users | Tiến độ, demo, preview thay đổi      | Demo session      |
| 2 tuần trước go-live | End user               | Hướng dẫn cụ thể, FAQ                | Email + training  |
| Go-live              | Tất cả                 | Hướng dẫn chuyển đổi, kênh support   | Email + chat      |


### Adoption Metrics

Đo lường mức độ sử dụng hệ thống mới sau go-live:

- **Tuần 1-2**: % user đã login ít nhất 1 lần (target: >80%)
- **Tháng 1**: % giao dịch xử lý qua hệ thống mới vs cũ (target: >60%)
- **Tháng 3**: Số support ticket liên quan hệ thống mới (trend giảm)
- **Tháng 6**: So sánh KPI trước/sau (thời gian xử lý, error rate, satisfaction)

## 17. Pricing & điều khoản thương mại

- Mô hình giá (fixed price, T&M, milestone-based, retainer, hybrid)
- Tổng chi phí ước lượng kèm breakdown theo phase / workstream
- Lịch thanh toán
- Cái gì IN scope vs OUT scope ở mức giá này
- Quy trình change request
- Điều khoản IP (mặc định: khách hàng sở hữu deliverable, vendor giữ reusable IP)
- Thời hạn bảo hành

Cho proposal nội bộ, thay section này bằng "Đề xuất ngân sách" (Budget Request).

## 18. Vì sao chọn chúng tôi (Why Us / Differentiators)

3-5 lý do cụ thể. Tránh claim chung chung ("chúng tôi đam mê, sáng tạo, customer-focused"). Dùng:

- Dự án trong quá khứ tương tự kèm kết quả đo được
- Domain expertise đúng ngành của khách hàng
- Tool, accelerator, hoặc framework độc quyền giảm thời gian/chi phí
- Credentials team trực tiếp liên quan đến công việc

Reinforce win themes đã xác định ở Phase 1. Section này là nơi tổng hợp lại differentiator đã rải xuyên suốt proposal.

## 19. Bước tiếp theo (Next Steps)

Call-to-action rõ ràng. Reader làm gì sau khi đọc xong?

- Cần ra quyết định trước [ngày]
- Ngày kickoff đề xuất
- Người liên hệ (point of contact)
- Chuẩn bị nào cần từ phía khách hàng trước kickoff

## 20. Phụ lục (Appendices), khi cần

- Diagram architecture chi tiết
- Bảng pricing chi tiết
- CV team / case study
- Glossary thuật ngữ
- Reference / nguồn nghiên cứu đã cite
- RACI matrix đầy đủ (nếu Governance Model chỉ tóm tắt)
