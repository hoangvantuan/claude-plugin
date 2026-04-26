---
name: facebook
description: "Đăng bài lên Facebook (wall cá nhân hoặc group) và tag bạn bè qua PinchTab browser control."
disable-model-invocation: true
allowed-tools:
  - Bash
  - Read
---

# Facebook Automation via PinchTab

Đăng bài Facebook (wall/group) + tag bạn bè qua PinchTab browser control. Script quản lý browser instance với saved profiles (cookies/sessions) nên không cần re-login mỗi lần.

## Prerequisites

- **PinchTab** installed và server đang chạy (`pinchtab server &`)
- Một PinchTab **profile** có Facebook login session (cookies đã lưu từ lần login thủ công trước)

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

## Failure Modes — Lỗi AI hay mắc

- **Gọi script khi PinchTab chưa chạy** — luôn kiểm tra `pinchtab server` trước khi gọi fb-post.sh
- **Dùng vanity URL thay vì numeric ID** — `--user-id` chỉ nhận numeric Facebook ID, không phải username
- **Quên `--publish true`** — default là `false` (chỉ soạn), user phải xác nhận trước khi thêm `--publish true`
- **Tag sai người** — khi có nhiều người trùng tên, dùng `--tag-id` để chính xác
- **Post content chứa quotes** — wrap content bằng double quotes, escape `"` bên trong nếu cần

## Chi tiết kỹ thuật

Cách script hoạt động, instance lifecycle, troubleshooting → [internals](references/internals.md). Đọc khi cần debug hoặc xử lý sự cố.
