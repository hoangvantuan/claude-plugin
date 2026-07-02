# Frameworks — Khung chấm ưu tiên

Tài liệu này dùng ở **pha 3** (chỉ khi verdict = Go). Nó cung cấp: công thức từng khung, cách chấm từng yếu tố, map khung↔loại, và map điểm→P-level định tính.

Nguyên tắc bao trùm: **điểm số là công cụ minh bạch hóa lý do, không phải máy phán quyết.** Bảng điểm giúp user thấy bạn cân nhắc gì; P-level cuối do bạn diễn giải từ điểm + bối cảnh.

## Map khung ↔ loại hạng mục

| Loại | Khung | Vì sao khung này |
|---|---|---|
| Feature (hướng user) | **RICE** | Reach (số user chạm tới) có nghĩa thật với feature |
| Bug | **ICE** | Bug không cần Reach riêng; mức đau gộp vào Impact |
| Techdebt | **WSJF** | Đo trực tiếp "càng để lâu càng đắt" |
| Task / khác | **ICE** | Nhẹ, đủ dùng cho việc không thuộc 3 nhóm trên |

**Hạng mục lai**: chọn theo *quyết định cần ra*, không theo nhãn. "API chậm, sửa ngay không?" → coi là bug → ICE. "API chậm, refactor kiến trúc không?" → coi là techdebt → WSJF. Luôn ghi rõ đã chọn khung nào và vì sao trong brief.

## RICE (Feature)

```
RICE = (Reach × Impact × Confidence) ÷ Effort
```

| Yếu tố | Ý nghĩa | Cách chấm |
|---|---|---|
| **Reach** | Số đối tượng chạm tới trong một khoảng thời gian (vd user/tháng) | Số thực, ước lượng từ dữ liệu. Không có dữ liệu → hỏi user hoặc ghi giả định phụ |
| **Impact** | Mức tác động lên mỗi đối tượng | Thang: 3 = rất lớn, 2 = lớn, 1 = vừa, 0.5 = nhỏ, 0.25 = rất nhỏ |
| **Confidence** | Độ tin vào ước lượng Reach/Impact | 100% = có dữ liệu chắc, 80% = có cơ sở, 50% = phỏng đoán. Giả định phụ chưa verify → kéo xuống 50% |
| **Effort** | Công sức, tính bằng person-month (hoặc person-week, nhất quán toàn brief) | Số thực > 0 |

Đơn vị Effort phải nhất quán. Confidence nhập dạng thập phân (80% = 0.8).

## ICE (Bug, Task)

```
ICE = Impact × Confidence × Ease
```

| Yếu tố | Ý nghĩa | Cách chấm (thang 1-10) |
|---|---|---|
| **Impact** | Mức đau × tần suất. Với bug: lỗi chặn nghiệp vụ chính + xảy ra thường xuyên → cao | 10 = nghiêm trọng & thường xuyên; 1 = phiền nhẹ & hiếm |
| **Confidence** | Độ chắc rằng làm xong sẽ giải quyết được vấn đề | 10 = đã reproduce & rõ root cause; thấp khi còn giả định then chốt (nhưng then chốt treo thì không tới được pha 3) |
| **Ease** | Mức dễ thực hiện (nghịch đảo Effort) | 10 = sửa nhanh, ít rủi ro; 1 = phức tạp, rủi ro lan rộng |

Điểm ICE = tích 3 yếu tố (tối đa 1000). Bug: Impact phản ánh cả mức nghiêm trọng (severity) lẫn tần suất gặp, đừng tách rời hai chiều này.

## WSJF (Techdebt)

```
WSJF = Cost of Delay ÷ Effort (Job Size)
```

Cost of Delay (CoD) = tổng 3 thành phần, mỗi thành phần thang 1-10:

| Thành phần CoD | Câu hỏi |
|---|---|
| **User/Business Value** | Để nguyên debt này, giá trị nào đang bị bào mòn? |
| **Time Criticality** | Càng để lâu càng đắt theo cấp số nhân không? Có deadline/ngưỡng vỡ không? |
| **Risk Reduction / Opportunity Enablement** | Trả debt này có mở khóa việc khác, giảm rủi ro hệ thống không? |

```
CoD = Value + Time Criticality + Risk/Opportunity
WSJF = CoD ÷ Effort
```

Effort cùng thang tương đối (story points hoặc person-week), nhất quán toàn brief. WSJF cao = nên làm sớm vì "trì hoãn đắt tương đối so với công bỏ ra". Lưu ý: ở skill này WSJF **chỉ** dùng cho Priority của techdebt, KHÔNG dùng để xếp trục timing.

## Map điểm → P-level (định tính, chung mọi khung)

Điểm số xếp hạng tương đối và minh bạch lý do. P-level cuối neo vào **tiêu chí định tính**, không vào ngưỡng số cứng.

| P-level | Nghĩa định tính | Tín hiệu thường thấy |
|---|---|---|
| **P0** | Đang chảy máu / chặn việc khác / rủi ro nghiêm trọng. Làm ngay | Bug chặn nghiệp vụ chính ở production; debt sắp gây sự cố; security |
| **P1** | Giá trị cao, rõ ràng đáng làm sớm | Điểm khung cao + tác động rõ; không chặn nhưng lợi ích lớn |
| **P2** | Đáng làm, chưa gấp | Điểm trung bình; có giá trị nhưng hoãn được không tổn hại nhiều |
| **P3** | Biên, làm khi rảnh hoặc gộp dịp khác | Điểm thấp; tác động nhỏ hoặc đối tượng hẹp |

**Cách diễn giải đúng** (điểm là đầu vào, bối cảnh là trọng tài):

- Ví dụ đảo chiều theo bối cảnh: "ICE=320 (không phải cao nhất), nhưng đây là bug chặn checkout của khách hàng đang trả tiền → P0."
- Ví dụ điểm cao nhưng hạ bậc: "RICE=410 nhờ Reach lớn, nhưng Confidence chỉ 50% vì Reach là giả định phụ chưa verify → để P2, ghi rõ cần đo lại Reach trước khi nâng bậc."

Luôn hiện **bảng từng yếu tố + điểm tổng + P-level + một câu lý do diễn giải**. Người đọc phải thấy được vì sao P-level này, không chỉ thấy con số.
