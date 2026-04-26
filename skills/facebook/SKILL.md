---
name: facebook
description: "Đăng bài lên Facebook (wall cá nhân hoặc group) với ảnh đính kèm và tag bạn bè qua PinchTab browser control."
allowed-tools:
  - Bash
  - Read
---

# Facebook Automation via PinchTab

Đăng bài Facebook (wall/group) + đính kèm ảnh + tag bạn bè qua PinchTab browser control. Script quản lý browser instance với saved profiles (cookies/sessions) nên không cần re-login mỗi lần.

## Prerequisites

- **PinchTab** installed và server đang chạy (`pinchtab server &`)
- Một PinchTab **profile** có Facebook login session (cookies đã lưu từ lần login thủ công trước)
- Nếu dùng `--image`: cần bật `pinchtab config set security.allowUpload true`
- Nên bật `pinchtab config set security.allowEvaluate true` để script nhập text chính xác (giữ line breaks, ký tự đặc biệt). Nếu tắt, script dùng CLI fallback nhưng có thể cắt nội dung dài

Nếu user chưa login: hướng dẫn start headed instance → login thủ công → reuse profile.

## Script Usage

**Script:** `scripts/fb-post.sh`

```bash
# Positional syntax
bash scripts/fb-post.sh "<content>" [options]

# Named syntax
bash scripts/fb-post.sh --content "<content>" [options]
```

**Parameters:**

| Param | Required | Default | Description |
|---|---|---|---|
| `<content>` | Yes | — | Post content (positional arg hoặc `--content`) |
| `--profile` | No | `default` | PinchTab profile name |
| `--user-id` | No | auto | Facebook numeric ID (wall mode) |
| `--group` | No | — | Group slug hoặc full URL → post vào group thay vì wall |
| `--image` | No | — | Đường dẫn ảnh đính kèm (dùng nhiều lần cho nhiều ảnh, tối đa 8) |
| `--tag` | No | — | Tên hiển thị của bạn bè cần tag |
| `--tag-id` | No | — | Facebook ID của bạn bè (chính xác hơn search theo tên) |
| `--publish` | No | `false` | `true` = đăng ngay, `false` = chỉ soạn (user review trước) |
| `--mode` | No | `headed` | `headed` = hiển thị browser, `headless` = chạy nền |
| `--debug` | No | `false` | Chụp screenshot mỗi bước vào `/tmp/` |
| `--dry-run` | No | — | Log actions mà không mở browser (kiểm tra params) |
| `--keep-instance` | No | — | Giữ browser instance sau khi xong (dùng cho chain nhiều posts) |

### Post lên Wall

```bash
bash scripts/fb-post.sh "Hello world!"
bash scripts/fb-post.sh "Hello!" --tag "Hoang Van Tuan" --publish false
bash scripts/fb-post.sh "Quick update" --user-id 100003782705460 --publish true
bash scripts/fb-post.sh "Test" --tag "Ngoc" --dry-run
```

### Post với ảnh đính kèm

```bash
# Một ảnh
bash scripts/fb-post.sh "Check this out!" --image /path/to/photo.jpg --publish true

# Nhiều ảnh
bash scripts/fb-post.sh "Album mới" --image photo1.jpg --image photo2.png --image photo3.jpg

# Ảnh + tag + group
bash scripts/fb-post.sh "Ảnh đẹp!" --image sunset.jpg --tag "Ngoc" --group tuhoccungai --publish true
```

### Post vào Group

```bash
bash scripts/fb-post.sh "Hello group!" --group tuhoccungai --publish false
bash scripts/fb-post.sh "Nội dung" --group "https://www.facebook.com/groups/tuhoccungai" --publish true
bash scripts/fb-post.sh "Check this!" --group tuhoccungai --tag "Ngoc" --publish true
bash scripts/fb-post.sh "Auto" --group tuhoccungai --mode headless --keep-instance --publish true
```

## Exit Codes

| Code | Meaning |
|---|---|
| `0` | Thành công |
| `1` | Thiếu hoặc sai arguments |
| `2` | Instance failure (không start được browser, profile sai) |
| `3` | Element not found (button, textbox, hoặc page không hợp lệ) |
| `4` | Publish failed (không tìm thấy nút đăng) |
| `5` | Upload failed (ảnh không upload được, hoặc `security.allowUpload` tắt) |

## Failure Modes — Lỗi AI hay mắc

- **Gọi script khi PinchTab chưa chạy** — luôn kiểm tra `pinchtab server` trước khi gọi fb-post.sh
- **Dùng vanity URL thay vì numeric ID** — `--user-id` chỉ nhận numeric Facebook ID, không phải username
- **Quên `--publish true`** — default là `false` (chỉ soạn), user phải xác nhận trước khi thêm `--publish true`
- **Tag sai người** — khi có nhiều người trùng tên, dùng `--tag-id` để chính xác
- **Post content chứa quotes** — wrap content bằng double quotes, escape `"` bên trong nếu cần
- **Upload ảnh lỗi ERR_UPLOAD_FAILED** — cần bật `pinchtab config set security.allowUpload true` trước khi dùng `--image`
- **File ảnh không tồn tại hoặc sai format** — script validate path VÀ magic bytes (JPEG/PNG/GIF/WebP) trước khi mở browser. File .jpg thật ra là HTML sẽ bị bắt ngay
- **Ảnh quá lớn** — PinchTab giới hạn 5MB/file, tối đa 8 file, tổng 10MB. DataTransfer JS fallback giới hạn ~700KB/file (base64 inline)
- **Ảnh upload nhưng không attach** — script verify ảnh thực sự hiện trong post (blob img hoặc nút Gỡ) trước khi publish. Nếu không detect trong 8s sẽ exit code 5

## Chi tiết kỹ thuật

Cách script hoạt động, instance lifecycle, troubleshooting → [internals](references/internals.md). Đọc khi cần debug hoặc xử lý sự cố.
