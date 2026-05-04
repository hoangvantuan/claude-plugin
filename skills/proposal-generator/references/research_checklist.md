# Research Checklist theo Domain

Dùng khi plan Phase 2 research. Chọn domain section liên quan; combine nếu dự án trải qua nhiều domain.

---

## Universal: luôn research các mục này

1. **Giải pháp tương đương / đối thủ** trong problem space: search "[problem] solutions" hoặc "[problem] software vendors"
2. **Industry report / analyst take gần đây** (trong 12 tháng): "[domain] market size 2026", "[domain] trends"
3. **Best-practice technical pattern cho lớp vấn đề**: "[problem type] architecture patterns", "[problem type] reference architecture"
4. **Failure mode / pitfall thường gặp** trong dự án loại này: "[problem type] project failures", "[problem type] lessons learned"

Làm cho mọi proposal bất kể domain nào.

---

## Web / SaaS application

- Frontend framework state-of-the-art (React, Vue, Svelte, Solid: team chọn cái nào và vì sao)
- So sánh backend framework theo ngôn ngữ chọn
- Database choice (Postgres vs specialized: search vector DB nếu có AI feature, time-series DB nếu metrics, v.v.)
- Hosting options (AWS / GCP / Azure / Vercel / Cloudflare) và so sánh chi phí
- Approach authentication (Auth0 / Clerk / Cognito / self-hosted Keycloak)

## Mobile application

- Tradeoff native (Swift, Kotlin) vs cross-platform (React Native, Flutter, KMP) cho dự án
- Timeline app store submission (đặc biệt Apple: review thường 1-3 ngày nhưng plan dài hơn)
- Setup push notification và limit per platform
- Pattern offline-first nếu liên quan
- Considerations về fragmentation Android (coverage version)

## Data / Analytics platform

- Inventory data source và volume ước lượng
- Yêu cầu batch vs streaming
- Warehouse choice (Snowflake / BigQuery / Redshift / Databricks)
- Tooling ETL / ELT (Fivetran / Airbyte / dbt / custom)
- BI layer (Looker / Tableau / Metabase / custom)
- Yêu cầu data governance (lineage, catalog, access control)

## AI / ML project

- **Model selection**: search current state cho task: search "best [task] model 2026" vì cái này thay đổi hàng tháng
- Tradeoff API vs self-hosted: pricing API hiện tại của các provider chính, chi phí hardware self-host
- Methodology eval: "good" trông như thế nào, đo bằng gì
- Latency và cost per request kỳ vọng
- Strategy fallback / degradation khi model fail hoặc hallucinate
- Implication data privacy (data training/inference có rời environment khách hàng không?)

## Integration / Migration project

- Tài liệu source system và limitation đã biết
- Volume và độ phức tạp data (số entity, số record, custom field)
- Options strategy cutover (big-bang / phased / parallel run)
- Rollback plan
- Nhu cầu retraining user

## Public-sector / Regulated industry

- Regulation cụ thể áp dụng (GDPR / HIPAA / PCI-DSS / SOC 2 / data residency địa phương)
- Yêu cầu framework procurement (ví dụ: format yêu cầu của hồ sơ thầu chính phủ)
- Certification yêu cầu cho vendor
- Yêu cầu audit trail
- Standard accessibility (WCAG level)

---

## Vietnam-specific context

Khi proposal cho khách hàng Việt Nam hoặc vận hành tại Việt Nam, research thêm:

- **Nghị định 13/2023 về bảo vệ dữ liệu cá nhân** (luật privacy của VN)
- **Luật An ninh mạng 2018** yêu cầu data localization
- **Quy định hóa đơn điện tử** (nếu có invoicing: yêu cầu nghiêm ngặt, phải tích hợp với cơ quan thuế GDT)
- **Banking / fintech**: thông tư SBV (Ngân hàng Nhà nước) về fintech, license payment intermediary
- **Đấu thầu khu vực công**: quy định nếu buyer là chính phủ / SOE

Nếu user hoặc công ty hoạt động tại Việt Nam, mặc định context Việt Nam trừ khi được nói khác.

---

## Bao nhiêu search?

| Mức độ đầy đủ input | Số search |
|---|---|
| Thin (1 dòng ý tưởng) | 5-8 |
| Medium (brief 1 trang) | 3-5 |
| Rich (RFP / dossier chi tiết) | 1-3 (chỉ gap-fill targeted) |

Đừng research vì research. Mỗi search phải lấp một gap cụ thể giúp proposal tốt hơn.

---

## Làm gì với research findings

- **Quantitative facts** (market size, benchmark numbers, regulatory specifics) → cite nguồn trong proposal
- **Qualitative patterns** (architectural approach, pitfall thường gặp) → dùng để inform recommendations, không cần cite
- **Competitive intelligence** → dùng để position differentiator trong section "Why Us"
- **Tech state-of-the-art** → dùng để section stack có credibility

Luôn paraphrase. Direct quote chỉ khi exact wording matters (ví dụ: một điều khoản pháp lý cụ thể).