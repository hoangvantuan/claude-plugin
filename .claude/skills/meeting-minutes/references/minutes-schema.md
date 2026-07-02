# Cấu trúc biên bản họp chuẩn

Biên bản tuân theo cấu trúc dưới đây. Chỉ hiển thị các field có thông tin. Thông tin quan trọng nhưng thiếu thì ghi `TBD`.

## 1. Metadata

Chỉ liệt kê field có giá trị thực. Bỏ qua field không quan trọng khi không có thông tin (ví dụ: "Gửi cho", "Địa điểm" nếu không biết).

```
- Tiêu đề:
- Ngày (YYYY-MM-DD):
- Bắt đầu:
- Kết thúc / Thời lượng:
- Người tổ chức:
- Địa điểm / Link: (chỉ hiện nếu biết)
- Người ghi biên bản:
```

## 2. Danh sách tham dự

```
- Có mặt: [tên + vai trò]
- Vắng mặt: [tên + lý do nếu biết]
```

## 3. Agenda

Danh sách các mục thảo luận theo thứ tự:

```
- Mục 1: tiêu đề ngắn
- Mục 2: tiêu đề ngắn
```

## 4. Tóm tắt

1-3 câu: mục tiêu cuộc họp và kết quả tổng quan.

## 5. Quyết định

Mỗi quyết định một bullet riêng:

```
- Quyết định 1: nội dung quyết định
  - Ai quyết định: [tên hoặc nhóm]
  - Lý do (1-2 câu): giải thích ngắn
  - Hiệu lực từ (nếu có): YYYY-MM-DD
```

## 6. Action Items

Dùng bảng cho dễ nhìn tổng quan. Tiêu chí hoàn thành ghi trong cột riêng.

```
| # | Action | Phụ trách | Deadline | Tiêu chí hoàn thành |
|---|--------|-----------|----------|---------------------|
| A1 | Mô tả action | Tên (team) | YYYY-MM-DD | Điều kiện done |
| A2 | ... | ... | ... | ... |
```

Nếu có liên kết đến ticket/URL, ghi bên dưới bảng:
```
- A1: https://github.com/owner/repo/issues/123
```

## 7. Ghi chú theo mục Agenda

Ngắn gọn, thực tế, có timestamp nếu có:

```
- Mục 1: tiêu đề
  - Điểm chính:
    - Ý A (timestamp 00:05)
    - Ý B (timestamp 00:12)
  - Vấn đề mở:
    - Q1: câu hỏi (owner nếu đã assign)
```

## 8. Pending / Parking Lot

Gộp 2 loại vào đây: (1) hạng mục đang trao đổi nhưng chưa có quyết định/action chính thức, (2) vấn đề bị hoãn lại để xử lý sau.

```
- Hạng mục: mô tả ngắn
  - Tình trạng: đang cân nhắc / hoãn lại / cần thêm data / chờ input từ [ai]
  - Bước tiếp: cuộc họp tiếp hoặc thời điểm cụ thể
```

Nếu không có, bỏ section này.

## 9. Rủi ro / Blocker (nếu có)

```
- Rủi ro 1: mô tả, tác động, người xử lý
```

Nếu không có, bỏ section này.

## 10. Cuộc họp tiếp / Follow-up

```
- Ngày giờ dự kiến (nếu có):
- Mục tiêu cuộc họp tiếp:
```

## 11. Tài liệu đính kèm

```
- Agenda: URL
- Slides: URL
- Transcript / Recording: URL
- Tickets liên quan: danh sách URL/ID
```

Nếu không có tài liệu, bỏ section này.
