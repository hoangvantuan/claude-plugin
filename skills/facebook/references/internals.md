# Facebook Skill — Internals

Chi tiết kỹ thuật bên trong script. Đọc khi cần debug, xử lý sự cố, hoặc hiểu cách script hoạt động.

## How It Works

Script dùng PinchTab accessibility snapshot để tìm UI elements theo role và **multi-language keywords** (Tiếng Việt + English). Mỗi lần tìm element sẽ thử tất cả ngôn ngữ cho đến khi match — không cần cấu hình locale.

0. **Fail-fast checks** — validate image magic bytes (JPEG/PNG/GIF/WebP), kiểm tra `allowEvaluate` TRƯỚC khi mở browser
1. **Start/reuse browser** — kiểm tra instance qua `GET /instances/{id}` API (status: running), restart nếu stale. Export `PINCHTAB_INSTANCE`
2. **Navigate** — dùng `pinchtab nav <url> --new-tab --print-tab-id` để tạo tab mới (tránh stale tab mặc định). Export `PINCHTAB_TAB` từ tab ID trả về
3. **Validate page** — group mode kiểm tra create-post button tồn tại (early error nếu URL sai hoặc không có quyền)
4. **Open post dialog** — click button với retry logic: verify textbox xuất hiện, retry tối đa 3 lần
5. **Type content** — dùng `pinchtab focus` + `pinchtab keyboard inserttext` để giữ line breaks trong contenteditable. Fallback sang CLI type nếu fail
6. **Attach images** (optional) — focus composer, dùng `pinchtab eval` với ClipboardEvent + DataTransfer chứa ảnh base64 inline. Verify "Gỡ file đính kèm" xuất hiện trước khi tiếp tục
7. **Tag friend** (optional) — mở tag dialog, search theo tên, chọn bằng keyboard (ArrowDown + Enter); dùng `--tag-id` cho precise match, ưu tiên "Bạn bè" (friends)
8. **Publish or hold** — dùng **exact match** cho nút "Đăng"/"Post" để tránh click nhầm "Đăng ẩn danh"

### Wall vs Group — Điểm khác biệt chính

| Aspect | Wall | Group |
|---|---|---|
| Navigation | `facebook.com/me` hoặc profile ID | Group URL (slug hoặc full) |
| Create post button | "nghĩ gì" / "what's on your mind" | "viết gì" / "write something" |
| Page validation | Không | Kiểm tra create-post button tồn tại |
| Title field | Không hỗ trợ | Có (`--title`), rich text H1 formatting |

Các bước còn lại (textbox, tagging, publish) hoạt động giống nhau.

### Image Upload Flow

Khi `--image` được cung cấp:

1. **Magic byte validation** — kiểm tra 4 byte đầu file: FFD8FF (JPEG), 89504E47 (PNG), 47494638 (GIF), 52494646 (WebP/RIFF). File sai format (vd: HTML lưu thành .jpg) bị reject trước khi mở browser
2. **Permission check** — verify `security.allowEvaluate` qua `GET /api/config`. Bắt buộc cho image upload. Hard fail nếu tắt
3. **Focus composer** — `pinchtab focus` vào composer textbox (đã mở từ Step 4)
4. **Eval ClipboardEvent paste** — Python đọc file ảnh → base64 encode → build JS snippet → gửi qua HTTP `/evaluate` API. JS tạo `ClipboardEvent("paste")` với `DataTransfer` chứa image `File` object → dispatch lên `document.activeElement`. Chi tiết xem "### Eval Paste Method"
5. **Post-upload verification** — poll accessibility snapshot tối đa 10s, tìm: blob: URL, nút "Gỡ file"/"Remove file", hoặc role=img có blob/scontent URL

### Eval Paste Method

Upload ảnh qua `pinchtab eval` (HTTP `/evaluate` API) + ClipboardEvent + DataTransfer.

**Tại sao dùng eval thay vì CDP paste hay file picker:**

- **File picker** (click "Ảnh/video" → OS dialog) — CDP Cmd+V paste vào file picker text field, không upload ảnh
- **CDP paste** (clipboard + dispatchKeyEvent) — phụ thuộc macOS clipboard, Chrome debug port, `ws` module. Không ổn định
- **Eval ClipboardEvent** — gửi trực tiếp qua HTTP API, không phụ thuộc clipboard hay debug port. Base64 inline trong JS → FB composer nhận paste event và attach ảnh

**Flow:**

1. Python đọc binary file, encode base64
2. Build JS: `atob(base64)` → `Uint8Array` → `Blob` → `File` → `DataTransfer` → `ClipboardEvent("paste")` → `dispatch`
3. Gửi JS qua `POST /evaluate` (HTTP API, không giới hạn shell ARG_MAX)
4. PinchTab evaluate JS trong page context → FB nhận paste event với image data

**Bật quyền cần thiết:**

```bash
pinchtab config set security.allowEvaluate true
```

### Text Input

`pinchtab focus <ref>` + `pinchtab keyboard inserttext "<content>"` — giữ nguyên newlines trong contenteditable. Fallback sang `pinchtab type` nếu fail.

### Tab Management

Sau instance start, env `PINCHTAB_TAB` mặc định trỏ tab cũ (stale). Navigation không có `--new-tab` sẽ 404. Script xử lý:

1. Export `PINCHTAB_INSTANCE` ngay sau instance start/reuse
2. Mọi navigation dùng `pinchtab nav <url> --new-tab --print-tab-id`
3. Capture tab ID mới, export `PINCHTAB_TAB`

**Quirks quan trọng:**
- `pinchtab nav` (không phải `pinchtab navigate`)
- `pinchtab nav` chỉ nhận 1 arg (url), instance qua env `PINCHTAB_INSTANCE`
- `--new-tab` bắt buộc cho lần nav đầu tiên sau instance start

### Instance Health Check

Script dùng `GET /instances/{id}` API và kiểm tra field `status == "running"`. Timeout 5s để tránh block trên instance zombie.

## Instance Lifecycle

Scripts tự động reuse instance đang chạy. Dùng `--keep-instance` để giữ browser sau khi script kết thúc — hữu ích khi chain nhiều posts.

**Start instance thủ công** (nếu chưa có):

```bash
# Headed — visible browser
pinchtab instance start --profile default --mode headed

# Headless — background (default)
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
| "Cannot find button" | Facebook UI có thể đã thay đổi. Dùng `--debug` và check screenshots + `pinchtab snap`. |
| Session expired | Re-login thủ công ở headed mode để refresh cookies trong profile. |
| Browser won't start | Đảm bảo `pinchtab server` đang chạy và không có instance conflict. |
| Stale instance | Script detect qua `/instances/{id}` API (status != running) và restart tự động. |
| Stale tab (404 khi nav) | Script dùng `--new-tab --print-tab-id` tự động. Nếu vẫn lỗi: check `PINCHTAB_INSTANCE` env. |
| Wrong person tagged | Dùng `--tag-id <facebook_id>` thay vì chỉ search theo tên. |
| Bad profile name | Script báo lỗi rõ với exit code 2. Verify profile tồn tại trong PinchTab. |
| Group not accessible | Script validate group page sớm (exit code 3). Check URL và membership. |
| Dialog didn't open | Script tự retry click 3 lần. Check `--debug` screenshots. |
| Upload failed (exit 5) | Bật `security.allowEvaluate`: `pinchtab config set security.allowEvaluate true`. |
| Image not attached | Script verify blob:/nút "Gỡ file" trong 10s. Nếu fail: check file format (magic bytes), `allowEvaluate`. |
| Invalid image format | Script check magic bytes trước khi mở browser. File .jpg thật ra là HTML sẽ bị reject ngay. |
| Text bị cắt/mất line breaks | Bật `security.allowEvaluate`: `pinchtab config set security.allowEvaluate true`. |

## Known Limitations (PinchTab)

| Limitation | Workaround |
|---|---|
| `security.allowEvaluate` mặc định off | Cần bật thủ công. Áp dụng ngay, không cần restart server |
| PinchTab 0.10+ nested config key | `GET /api/config` trả `config.security.allowEvaluate` (nested) thay vì flat key. Script hỗ trợ cả hai format |
| `pinchtab snap --instance <id>` không tồn tại | Dùng `GET /instances/{id}` API để health-check thay vì CLI snap |
| PINCHTAB_TAB stale sau instance start | Script dùng `--new-tab --print-tab-id` khi nav, tự export tab ID mới |
| Eval payload lớn (ảnh > 5MB) | Base64 ~6.7MB cho ảnh 5MB. Gửi qua HTTP API (không giới hạn ARG_MAX). PinchTab xử lý OK |
| FB Lexical editor | `pinchtab keyboard inserttext` giữ newlines. Nếu fail, fallback sang CLI `type` (có thể mất format) |
| Default headless mode | Dùng `--mode headed` nếu cần nhìn browser. Headed có quirk snap discovery |
