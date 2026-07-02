---
name: facebook
description: "Đăng bài Facebook (wall cá nhân hoặc group) qua PinchTab browser automation. Hỗ trợ: đính kèm nhiều ảnh (tối đa 8), tag bạn bè, tiêu đề group, chế độ draft/publish. Trigger: đăng facebook, post facebook, đăng bài lên fb, facebook wall, facebook group, post lên group, đăng ảnh facebook, tag bạn. Skill này CHỈ đăng bài, KHÔNG viết nội dung — user cung cấp nội dung sẵn hoặc dùng skill viết khác trước."
allowed-tools:
  - Bash
  - Read
---

# Facebook Automation via PinchTab

Đăng bài Facebook (wall/group) + đính kèm ảnh + tag bạn bè qua PinchTab browser control.

## Prerequisites

- **PinchTab** installed và server đang chạy (`pinchtab server &`)
- Một PinchTab **profile** có Facebook login session (cookies đã lưu từ lần login thủ công trước)
- Bật `pinchtab config set security.allowEvaluate true` (bắt buộc cho image upload, khuyến khích cho text input)
- **macOS**: khuyến khích `brew install coreutils` (cung cấp `gtimeout`). Không bắt buộc, script có pure-bash fallback

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
| `--user-id` | No | `100003782705460` | Facebook numeric ID (wall mode) |
| `--group` | No | — | Group slug hoặc full URL → post vào group thay vì wall |
| `--title` | No | — | Tiêu đề bài viết (chỉ group, hiển thị bold phía trên nội dung) |
| `--image` | No | — | Đường dẫn ảnh đính kèm (dùng nhiều lần cho nhiều ảnh, tối đa 8) |
| `--tag` | No | — | Tên hiển thị của bạn bè cần tag |
| `--tag-id` | No | — | Facebook ID của bạn bè (chính xác hơn search theo tên) |
| `--publish` | No | `false` | `true` = đăng ngay, `false` = chỉ soạn (user review trước) |
| `--mode` | No | `headless` | `headed` = hiển thị browser, `headless` = chạy nền |
| `--debug` | No | `false` | Chụp screenshot mỗi bước vào `/tmp/` (flag, không cần value: `--debug`) |
| `--dry-run` | No | — | Log actions mà không mở browser (kiểm tra params) |
| `--keep-instance` | No | — | Giữ browser instance sau khi xong (dùng cho chain nhiều posts) |

### Post lên Wall

```bash
bash scripts/fb-post.sh "Hello world!"
bash scripts/fb-post.sh "Hello!" --tag "Hoang Van Tuan" --publish true
```

### Post với ảnh đính kèm

```bash
bash scripts/fb-post.sh "Check this out!" --image /path/to/photo.jpg --publish true
bash scripts/fb-post.sh "Ảnh đẹp!" --image photo1.jpg --image photo2.jpg --tag "Ngoc" --group tuhoccungai --publish true
```

### Post vào Group

```bash
bash scripts/fb-post.sh "Hello group!" --group tuhoccungai --publish true
bash scripts/fb-post.sh "Nội dung" --group "https://www.facebook.com/groups/tuhoccungai" --keep-instance --publish true
bash scripts/fb-post.sh "Nội dung bài viết" --title "[Series AI Agent] Vòng lặp nghĩ-làm" --group tuhoccungai --publish true
```

## Exit Codes & Lỗi thường gặp

| Code | Meaning | Nguyên nhân & cách xử lý |
|---|---|---|
| `0` | Thành công | — |
| `1` | Sai arguments | Thiếu content, `--user-id` nhận vanity URL thay vì numeric ID, file ảnh không tồn tại hoặc sai format (script validate magic bytes trước khi mở browser) |
| `2` | Instance failure | PinchTab chưa chạy (`pinchtab server &`) hoặc profile không tồn tại |
| `3` | Element not found | FB UI thay đổi, group URL sai, không có quyền. Dùng `--debug` kiểm tra screenshot |
| `4` | Publish failed | Nút đăng không tìm thấy |
| `5` | Upload failed | `security.allowEvaluate` tắt → `pinchtab config set security.allowEvaluate true`. Ảnh dispatch nhưng không attach → verify blob: URL trong 10s |
| `6` | Missing dependency | Thiếu binary cần thiết (pinchtab, python3, curl, xxd). Log ghi rõ binary nào thiếu và cách cài |

**Lỗi AI hay mắc (không báo exit code):**

- Quên `--publish true` — default là `false`, user phải xác nhận trước khi thêm
- Tag sai người — nhiều người trùng tên, dùng `--tag-id` cho chính xác
- Content chứa quotes — wrap bằng double quotes, escape `"` bên trong
- Fast failure (< 1s) — script báo "timed out" nhưng thực ra binary không tồn tại hoặc server chưa chạy. Xem exit code và thời gian thực tế trong log

## Chi tiết kỹ thuật

Cách script hoạt động, instance lifecycle, troubleshooting → [internals](references/internals.md). Đọc khi cần debug hoặc xử lý sự cố.
