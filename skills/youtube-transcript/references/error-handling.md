# Error Handling

## yt-dlp not installed

Thử cài tự động theo thứ tự: brew > apt > pip3.
Nếu tất cả fail, hướng dẫn user cài thủ công.

## No subtitles available

1. Đã thử `--write-sub` và `--write-auto-sub`?
2. Thử chỉ định ngôn ngữ: `--sub-langs en`
3. Nếu vẫn không có, thông báo cho user video không có phụ đề

## Invalid or private video

- Kiểm tra URL format: `https://www.youtube.com/watch?v=VIDEO_ID` hoặc `https://youtu.be/VIDEO_ID`
- Video private/age-restricted/geo-blocked: thông báo lỗi cụ thể từ yt-dlp cho user

## SSL errors

Thử thêm `--no-check-certificate` (chỉ dùng khi cần thiết).

## Multiple subtitle languages

Liệt kê bằng `--list-subs`, sau đó chọn cụ thể:
```bash
yt-dlp --write-auto-sub --sub-langs en --skip-download --output "transcript_temp" "$VIDEO_URL"
```

## Download interrupted

- Kiểm tra kết nối mạng
- Kiểm tra dung lượng ổ đĩa
- Chạy lại lệnh (yt-dlp hỗ trợ resume tự động)
