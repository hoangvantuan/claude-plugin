# Design Patterns cho Skill

5 patterns đã kiểm chứng giúp skill hoạt động hiệu quả hơn. Dùng khi cải tiến hoặc viết mới — chọn pattern phù hợp với loại skill.

## DP1: Role-then-Constraint

Thiết lập vai trò cụ thể trước, rồi định nghĩa hành vi + anti-patterns. LLM diễn giải vai trò tổng thể (holistic) thay vì tuân theo lệnh nghĩa đen (literal).

```markdown
Bạn là [vai trò cụ thể] [hành vi đặc trưng].
Khi [tình huống], bạn [phản ứng tự nhiên].
Bạn không [anti-pattern].
```

**Khi nào dùng:** Skill cần persona rõ ràng (mentor, reviewer, analyst). Tránh với skill thuần workflow/automation.

## DP2: Output Contract

Định nghĩa output format như một thực tế hiện hữu thay vì yêu cầu thay đổi hành vi. Pattern ngụ ý model "đã" hoạt động theo cách này.

```markdown
Phản hồi tuân theo cấu trúc:
[PHẦN 1] (mô tả ngắn)
[PHẦN 2] (mô tả ngắn)
[PHẦN 3] (mô tả ngắn)
```

**Khi nào dùng:** Mọi skill cần output có cấu trúc nhất quán.

## DP3: Autonomy Budget

Định nghĩa rõ ranh giới: được phép làm gì tự do vs. phải hỏi trước. Nghịch lý: ranh giới rõ ràng khiến model tự tin hơn trong phạm vi cho phép.

```markdown
Được phép:
- [hành động an toàn, reversible]

Phải hỏi trước khi:
- [hành động không thể đảo ngược]
- [hành động ảnh hưởng bên ngoài]
```

**Khi nào dùng:** Skill có side effects (tạo file, gọi API, push code). Ít cần với skill chỉ phân tích/output text.

## DP4: Failure Mode Registry

Đặt tên rõ ràng các hành vi không mong muốn cần tránh. Khai thác RLHF — khi định nghĩa tường minh hành vi sai, model "được phép" hành xử khác đi.

```markdown
Failure modes cần tránh:
- [hành vi sai cụ thể #1]
- [hành vi sai cụ thể #2]
```

**Khi nào dùng:** Skill từng cho output sai theo pattern lặp lại. Liệt kê failure modes giúp model nhận diện và tránh.

## DP5: Calibrated Confidence

Hiệu chỉnh mức tự tin — giảm 40-60% hallucination trên tác vụ có cấu trúc.

```markdown
Khi chắc chắn: phát biểu trực tiếp.
Khi không chắc: nói rõ và đề xuất phương án thay thế.
Khi không biết: nói "Tôi không biết" thay vì đoán.
```

**Khi nào dùng:** Skill xử lý domain knowledge phức tạp hoặc dễ hallucinate (research, analysis, technical advice).

---

## Cách sử dụng khi cải tiến

1. Xác định loại skill (persona-based? workflow? automation? analysis?)
2. Map loại skill → patterns phù hợp:
   - Persona-based (mentor, reviewer) → DP1 + DP4
   - Workflow/automation → DP2 + DP3
   - Analysis/research → DP2 + DP5
   - Interactive/conversational → DP1 + DP4 + DP5
3. Kiểm tra skill hiện tại đã áp dụng pattern nào chưa
4. Thêm pattern thiếu nếu cải thiện được quality score
