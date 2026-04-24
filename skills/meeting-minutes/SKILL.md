---
name: meeting-minutes
description: 'Tạo biên bản họp (meeting minutes) từ transcript, ghi chú, hoặc file nội dung cuộc họp. Bao gồm metadata, danh sách tham dự, quyết định, action items (người phụ trách + deadline), và bước tiếp theo. Dùng skill này khi user cung cấp nội dung cuộc họp và muốn tạo biên bản chuẩn, hoặc khi user nhắc đến "biên bản", "meeting minutes", "ghi chú cuộc họp", "tóm tắt cuộc họp", "meeting notes".'
---

# Meeting Minutes: Tạo biên bản họp

Tạo biên bản họp chất lượng cao, nhất quán từ nội dung cuộc họp. Output ưu tiên quyết định và action items để team chuyển nhanh từ thảo luận sang thực thi. Biên bản xuất bằng tiếng Việt.

## Khi nào dùng

- Họp sync, standup, design review, triage, planning, hoặc họp ad-hoc
- Cần bản ghi rõ ràng về quyết định, action items, và follow-up
- Tạo biên bản chuẩn từ transcript, recording, hoặc ghi chú thô

## Output

```
{CWD}/meeting-minutes/
└── {slug}-{YYMMDD-HHmm}/
    └── minutes.md
```

- `{slug}`: kebab-case từ tên cuộc họp (max 30 ký tự)
- `{YYMMDD-HHmm}`: timestamp lúc tạo

## Workflow

### Bước 1: Tiếp nhận nội dung

1. Nhận input từ user: text trực tiếp hoặc file path
2. Hỗ trợ đọc file: `.txt`, `.md`, `.pdf`, `.docx`
3. Nếu input là file, đọc nội dung bằng Read tool (PDF dùng tham số `pages` cho file lớn)
4. Scan nhanh nội dung: xác định ngôn ngữ gốc, độ dài, số người tham gia ước lượng

### Bước 2: Hỏi bổ sung (tối đa 3 câu)

Trước khi tạo biên bản, kiểm tra thông tin còn thiếu. Dùng AskUserQuestion hỏi tối đa 3 câu:

**Chỉ hỏi khi thông tin KHÔNG thể suy ra từ nội dung.** Nếu transcript/ghi chú đã chứa đủ metadata, bỏ qua bước này.

Các thông tin cần xác nhận (nếu thiếu):

1. Tên cuộc họp, ngày, thời gian bắt đầu (hoặc thời lượng), người tổ chức?
2. Có agenda hoặc tài liệu bổ sung nào không?
3. Ai duyệt biên bản?

Nếu user trả lời "không có transcript" hoặc "không có agenda", đánh dấu nguồn là "ghi chú ad-hoc" và ghi chú những chỗ có thể thiếu thông tin.

### Bước 3: Tạo biên bản

Tạo biên bản theo cấu trúc chuẩn. Tham khảo chi tiết tại `references/minutes-schema.md`.

Quy tắc xử lý:

- **Trích xuất quyết định**: tìm các cụm "đồng ý", "quyết định", "thống nhất", "approved", "decided", "agreed" trong nội dung
- **Trích xuất action items**: tìm các cụm "sẽ làm", "phụ trách", "deadline", "trước ngày", "assigned to", "action", "TODO", "task"
- **Suy luận owner**: nếu nội dung nói "Minh sẽ xử lý", owner = Minh
- **Suy luận deadline**: nếu nội dung nói "xong trước thứ 6", tính ngày cụ thể từ ngày họp
- **Trích xuất pending / parking lot**: các hạng mục có thảo luận nhưng chưa có quyết định hay action chính thức, hoặc bị hoãn lại. Ví dụ: "đang cân nhắc", "sẽ bàn thêm", "chưa kết luận", "để sprint sau"
- Mỗi action item PHẢI có owner và deadline. Nếu không suy ra được, ghi "Cần xác nhận"
- Thông tin không chắc chắn ghi `TBD` kèm ghi chú cần lấy từ đâu
- Metadata chỉ hiển thị thông tin có sẵn hoặc suy ra được. Không liệt kê field với giá trị TBD nếu field đó không quan trọng (ví dụ: "Gửi cho", "Địa điểm"). Chỉ dùng TBD cho thông tin quan trọng cần bổ sung sau

### Bước 4: Lưu và trình bày

1. Tạo thư mục output theo cấu trúc đã định
2. Lưu biên bản vào `minutes.md`
3. Hiển thị tóm tắt cho user: số quyết định, số action items, những chỗ cần xác nhận

## Nguyên tắc chất lượng

- Ngắn gọn: họp ≤30 phút thì biên bản ≤1 trang A4, họp ≤60 phút thì ≤2 trang
- Dùng ngôn ngữ đơn giản, bullet list cho dễ đọc
- Ưu tiên quyết định và action items lên đầu
- Không đưa suy đoán hoặc thông tin chưa xác minh. Không chắc thì ghi `TBD`
- Ngày tháng dùng ISO 8601 (YYYY-MM-DD)
- Giữ sự thật, tách bạch ý kiến cá nhân (nếu có, đánh dấu rõ "Ý kiến")
- Không đưa thông tin cá nhân nhạy cảm trừ khi cần thiết

## Lưu ý quan trọng

- Quyết định và action items là giá trị cốt lõi của biên bản. Không được bỏ sót
- Action items luôn có owner + deadline. Thiếu thì đánh dấu "Cần xác nhận"
- Acceptance criteria cho action items khi có thể
- Link đến tài liệu liên quan (ticket, slide, recording) nếu có
