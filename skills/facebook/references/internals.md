# Facebook Skill — Internals

Chi tiết kỹ thuật bên trong script. Đọc khi cần debug, xử lý sự cố, hoặc hiểu cách script hoạt động.

## How It Works

Script dùng PinchTab accessibility snapshot để tìm UI elements theo role và **multi-language keywords** (Tiếng Việt + English). Mỗi lần tìm element sẽ thử tất cả ngôn ngữ cho đến khi match — không cần cấu hình locale.

0. **Fail-fast checks** — validate image magic bytes (JPEG/PNG/GIF/WebP), kiểm tra `allowUpload` và `allowEvaluate` TRƯỚC khi mở browser
1. **Start/reuse browser** — kiểm tra instance qua `GET /instances/{id}` API (status: running), restart nếu stale
2. **Tab discovery** — sau khi instance sẵn sàng, query `GET /instances/{id}/tabs` để lấy active tab ID, set context qua `pinchtab tab <id>`. Tránh stale tab ID từ instance cũ bị kill
3. **Navigate** — wall mode: mở profile (auto-detect hoặc `--user-id`); group mode: mở group URL
4. **Validate page** — group mode kiểm tra create-post button tồn tại (early error nếu URL sai hoặc không có quyền)
5. **Open post dialog** — click button với retry logic: verify textbox xuất hiện, retry tối đa 3 lần
6. **Type content** — dùng HTTP API `/evaluate` + `document.execCommand('insertText')` để giữ line breaks và tránh CLI cắt nội dung chứa ký tự đặc biệt. Fallback sang CLI nếu `allowEvaluate` tắt
7. **Attach images** (optional) — click "Ảnh/Video" button, upload qua PinchTab `/upload` API với scoped selector (`[role="dialog"] input[type=file]`). Fallback DataTransfer JS nếu `/upload` fail. Verify ảnh thực sự attach trước khi tiếp tục
8. **Tag friend** (optional) — mở tag dialog, search theo tên, chọn bằng keyboard (ArrowDown + Enter); dùng `--tag-id` cho precise match, ưu tiên "Bạn bè" (friends)
9. **Publish or hold** — dùng **exact match** cho nút "Đăng"/"Post" để tránh click nhầm "Đăng ẩn danh"

### Wall vs Group — Điểm khác biệt chính

| Aspect | Wall | Group |
|---|---|---|
| Navigation | `facebook.com/me` hoặc profile ID | Group URL (slug hoặc full) |
| Create post button | "nghĩ gì" / "what's on your mind" | "viết gì" / "write something" |
| Page validation | Không | Kiểm tra create-post button tồn tại |

Các bước còn lại (textbox, tagging, publish) hoạt động giống nhau.

### Image Upload Flow

Khi `--image` được cung cấp:

1. **Magic byte validation** — kiểm tra 4 byte đầu file: FFD8FF (JPEG), 89504E47 (PNG), 47494638 (GIF), 52494646 (WebP/RIFF). File sai format (vd: HTML lưu thành .jpg) bị reject trước khi mở browser
2. **Permission check** — verify `security.allowUpload` và `security.allowEvaluate` qua `GET /api/config`. Hỗ trợ cả flat key (`security.allowUpload`) và nested key (`config.security.allowUpload`) cho PinchTab 0.10+. Fail-fast nếu tắt
3. **Click "Ảnh/Video"** — tìm button bằng keyword multi-language ("ảnh/video", "photo/video"). Fallback: tìm không giới hạn role
4. **Upload qua CDP paste** — copy ảnh vào macOS clipboard, dùng Chrome DevTools Protocol để dispatch native paste event (isTrusted=true). Chi tiết xem "### CDP Paste Method"
5. **Post-upload verification** — poll accessibility snapshot tối đa 8s, tìm blob image, nút "Gỡ"/"Remove", hoặc thumbnail/photo indicators. Nếu không detect ảnh thì exit code 5

### CDP Paste Method

Upload ảnh qua CDP native paste. Facebook reject synthetic events (isTrusted=false), nên CDP paste là phương pháp duy nhất đáng tin cậy.

**CDP paste hoạt động thế nào:**

1. Copy ảnh vào macOS system clipboard: `osascript -e 'set the clipboard to (read POSIX file "/path" as JPEG picture)'`
2. Script `cdp-paste.js` discover Chrome debug port (từ `ps aux` hoặc port mặc định 9222)
3. Fetch `http://localhost:<port>/json` để lấy WebSocket debugger URL
4. Connect WebSocket, gửi `Input.dispatchKeyEvent` với `commands: ['Paste']`
5. Chrome thực hiện native paste từ clipboard → FB nhận event với `isTrusted=true` → chấp nhận ảnh

**Tại sao CDP paste hiệu quả:**
- `commands: ['Paste']` trong CDP kích hoạt browser-internal paste handler
- Khác với synthetic JS events (isTrusted=false) mà FB block
- Khác với PinchTab CLI keyboard shortcuts (không hỗ trợ modifier chord)
- Chrome debug port thường đã exposed sẵn khi PinchTab start Chrome

**Bật quyền cần thiết:**

```bash
pinchtab config set security.allowUpload true
pinchtab config set security.allowEvaluate true
```

### Text Input (Per-line)

Script tách content theo newlines, type từng dòng qua `document.execCommand("insertText")` (mỗi dòng không chứa `\n`), chèn `pinchtab press Enter` giữa các dòng. FB Lexical editor tạo paragraph break cho mỗi Enter event.

Lý do: Lexical editor bỏ qua `\n` trong insertText. Phải chia nhỏ và dùng keyboard event.

### Tab Management

PinchTab CLI lưu "current tab" context. Khi instance bị kill và restart, tab ID cũ trở thành stale. Script xử lý bằng cách:

1. Sau khi instance sẵn sàng (start mới hoặc reuse), query `GET /instances/{id}/tabs`
2. Lấy tab đầu tiên từ response
3. Gọi `pinchtab tab <id>` để set CLI context

Nếu không discover được tab, script tiếp tục với CLI default (có thể fail nếu stale).

### Instance Health Check

Thay vì `pinchtab snap --instance <id>` (flag không tồn tại), script dùng `GET /instances/{id}` API và kiểm tra field `status == "running"`. Timeout 5s để tránh block trên instance zombie.

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
| Stale instance | Script detect qua `/instances/{id}` API (status != running) và restart tự động. |
| Stale tab ID | Script discover tab mới sau mỗi instance start/reuse. Nếu vẫn lỗi: `pinchtab tab` để list, `pinchtab tab <id>` để set. |
| Wrong person tagged | Dùng `--tag-id <facebook_id>` thay vì chỉ search theo tên. |
| Bad profile name | Script báo lỗi rõ với exit code 2. Verify profile tồn tại trong PinchTab. |
| Group not accessible | Script validate group page sớm (exit code 3). Check URL và membership. |
| Dialog didn't open | Script tự retry click 3 lần. Check `--debug true` screenshots. |
| Upload failed (exit 5) | Bật `security.allowUpload`: `pinchtab config set security.allowUpload true`. Script thử DataTransfer JS fallback tự động. |
| Image not attached | Script verify blob img/nút Gỡ trong 8s. Nếu fail: check file format (magic bytes), `allowEvaluate` (cho JS fallback). |
| Invalid image format | Script check magic bytes trước khi mở browser. File .jpg thật ra là HTML sẽ bị reject ngay. |
| Photo/Video button not found | Facebook UI có thể thay đổi. Check `pinchtab snap` cho keyword mới. |
| Image quá lớn | PinchTab giới hạn 5MB/file. DataTransfer fallback giới hạn ~700KB. Resize ảnh trước khi upload. |
| Text bị cắt/mất line breaks | Bật `security.allowEvaluate`: `pinchtab config set security.allowEvaluate true`. |

## Known Limitations (PinchTab)

| Limitation | Workaround |
|---|---|
| `security.allowEvaluate` mặc định off | Cần bật thủ công. Áp dụng ngay, không cần restart server |
| PinchTab 0.10+ nested config key | `GET /api/config` trả `config.security.allowUpload` (nested) thay vì `security.allowUpload` (flat). Script hỗ trợ cả hai format |
| `pinchtab press "Meta+V"` không chord | Giải quyết bằng CDP `Input.dispatchKeyEvent` với `commands: ['Paste']`. Không dùng PinchTab CLI cho paste |
| `pinchtab snap --instance <id>` không tồn tại | Dùng `GET /instances/{id}` API để health-check thay vì CLI snap |
| PinchTab CLI lưu stale tab ID | Script export `PINCHTAB_TAB` sau mỗi instance start/reuse. Query `/instances/{id}/tabs` API rồi set |
| CDP paste chỉ hỗ trợ macOS | `osascript set the clipboard to` là macOS-only. Linux cần thay bằng `xclip` / `wl-copy` |
| FB Lexical editor bỏ `\n` trong insertText | Script type per-line với Enter key giữa các dòng |
| Headed mode đóng browser | Mặc định headed luôn stop instance khi xong. Dùng `--keep-instance` để giữ |
