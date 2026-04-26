# Facebook Skill — Internals

Chi tiết kỹ thuật bên trong script. Đọc khi cần debug, xử lý sự cố, hoặc hiểu cách script hoạt động.

## How It Works

Script dùng PinchTab accessibility snapshot để tìm UI elements theo role và **multi-language keywords** (Tiếng Việt + English). Mỗi lần tìm element sẽ thử tất cả ngôn ngữ cho đến khi match — không cần cấu hình locale.

1. **Start/reuse browser** — kiểm tra instance đang chạy, health-check trước khi reuse (restart nếu stale)
2. **Navigate** — wall mode: mở profile (auto-detect hoặc `--user-id`); group mode: mở group URL
3. **Validate page** — group mode kiểm tra create-post button tồn tại (early error nếu URL sai hoặc không có quyền)
4. **Open post dialog** — click button với retry logic: verify textbox xuất hiện, retry tối đa 3 lần
5. **Type content** — dùng HTTP API `/evaluate` + `document.execCommand('insertText')` để giữ line breaks và tránh CLI cắt nội dung chứa ký tự đặc biệt
6. **Attach images** (optional) — click "Ảnh/Video" button, upload từng file qua PinchTab `/upload` API
7. **Tag friend** (optional) — mở tag dialog, search theo tên, chọn bằng keyboard (ArrowDown + Enter); dùng `--tag-id` cho precise match, ưu tiên "Bạn bè" (friends)
8. **Publish or hold** — dùng **exact match** cho nút "Đăng"/"Post" để tránh click nhầm "Đăng ẩn danh"

### Wall vs Group — Điểm khác biệt chính

| Aspect | Wall | Group |
|---|---|---|
| Navigation | `facebook.com/me` hoặc profile ID | Group URL (slug hoặc full) |
| Create post button | "nghĩ gì" / "what's on your mind" | "viết gì" / "write something" |
| Page validation | Không | Kiểm tra create-post button tồn tại |

Các bước còn lại (textbox, tagging, publish) hoạt động giống nhau.

### Image Upload Flow

Khi `--image` được cung cấp:

1. **Pre-check** — validate file tồn tại, resolve đường dẫn tuyệt đối, kiểm tra `security.allowUpload` qua PinchTab config API
2. **Click "Ảnh/Video"** — tìm button bằng keyword multi-language ("ảnh/video", "photo/video"). Fallback: tìm không giới hạn role
3. **Upload từng file** — gọi PinchTab HTTP API `POST /upload` với selector `input[type="file"]` và đường dẫn file. Mỗi file upload riêng lẻ với delay 2-4 giây cho Facebook xử lý
4. **Retry logic** — nếu upload fail, script dừng ngay (exit code 5) thay vì tiếp tục

Giới hạn PinchTab: 5MB/file, tối đa 8 file/request, tổng 10MB. Bật quyền upload:

```bash
pinchtab config set security.allowUpload true
```

## Instance Lifecycle

Scripts tự động reuse instance đang chạy. Dùng `--keep-instance` để giữ browser sau khi script kết thúc — hữu ích khi chain nhiều posts.

**Start instance thủ công** (nếu chưa có):

```bash
# Headed — visible browser
pinchtab instance start --profile default --mode headed

# Headless — background
pinchtab instance start --profile default --mode headless
```

**Stop instance** — stop khi xong để free resources:

```bash
pinchtab instance list
pinchtab instance stop <instance_id>
```

Nếu instance stale (commands timeout), scripts tự detect và restart. Force-restart thủ công: stop rồi start lại.

## Troubleshooting

| Issue | Solution |
|---|---|
| "Cannot find button" | Facebook UI có thể đã thay đổi. Dùng `--debug true` và check screenshots + `pinchtab snap`. |
| Session expired | Re-login thủ công ở headed mode để refresh cookies trong profile. |
| Browser won't start | Đảm bảo `pinchtab server` đang chạy và không có instance conflict. |
| Stale instance | Script tự detect và restart. Manual fix: `pinchtab instance stop <id>`. |
| Wrong person tagged | Dùng `--tag-id <facebook_id>` thay vì chỉ search theo tên. |
| Bad profile name | Script báo lỗi rõ với exit code 2. Verify profile tồn tại trong PinchTab. |
| Group not accessible | Script validate group page sớm (exit code 3). Check URL và membership. |
| Dialog didn't open | Script tự retry click 3 lần. Check `--debug true` screenshots. |
| Upload failed (exit 5) | Bật `security.allowUpload`: `pinchtab config set security.allowUpload true` |
| Photo/Video button not found | Facebook UI có thể thay đổi. Check `pinchtab snap` cho keyword mới. |
| Image quá lớn | PinchTab giới hạn 5MB/file. Resize ảnh trước khi upload. |
