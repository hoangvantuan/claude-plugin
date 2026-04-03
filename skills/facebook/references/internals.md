# Facebook Skill — Internals

Chi tiết kỹ thuật bên trong script. Đọc khi cần debug, xử lý sự cố, hoặc hiểu cách script hoạt động.

## How It Works

Script dùng PinchTab accessibility snapshot để tìm UI elements theo role và **multi-language keywords** (Tiếng Việt + English). Mỗi lần tìm element sẽ thử tất cả ngôn ngữ cho đến khi match — không cần cấu hình locale.

1. **Start/reuse browser** — kiểm tra instance đang chạy, health-check trước khi reuse (restart nếu stale)
2. **Navigate** — wall mode: mở profile (auto-detect hoặc `--user-id`); group mode: mở group URL
3. **Validate page** — group mode kiểm tra create-post button tồn tại (early error nếu URL sai hoặc không có quyền)
4. **Open post dialog** — click button với retry logic: verify textbox xuất hiện, retry tối đa 3 lần
5. **Type content** — dùng `inserttext` để giữ line breaks
6. **Tag friend** (optional) — mở tag dialog, search theo tên, chọn bằng keyboard (ArrowDown + Enter); dùng `--tag-id` cho precise match, ưu tiên "Bạn bè" (friends)
7. **Publish or hold** — dùng **exact match** cho nút "Đăng"/"Post" để tránh click nhầm "Đăng ẩn danh"

### Wall vs Group — Điểm khác biệt chính

| Aspect | Wall | Group |
|---|---|---|
| Navigation | `facebook.com/me` hoặc profile ID | Group URL (slug hoặc full) |
| Create post button | "nghĩ gì" / "what's on your mind" | "viết gì" / "write something" |
| Page validation | Không | Kiểm tra create-post button tồn tại |

Các bước còn lại (textbox, tagging, publish) hoạt động giống nhau.

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
