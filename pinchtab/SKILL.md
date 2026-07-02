---
name: pinchtab
description: "Browser automation for AI agents via PinchTab HTTP API/CLI. Navigate, extract text, fill forms, click elements, scrape pages, take screenshots, export PDF, multi-tab. Token-efficient (~800 tokens/page), built-in stealth, persistent login sessions. Dùng khi user nhắc 'PinchTab', 'pinchtab', hoặc cần tự động hóa trình duyệt qua PinchTab cụ thể (khác agent-browser). Hỗ trợ: scraping, login automation, pagination, form filling, screenshot, PDF export, batch actions via macro endpoint."
allowed-tools:
  - Bash
  - Read
---

# PinchTab — Browser Automation for AI Agents

Control Chrome browsers via PinchTab's CLI and HTTP API. Token-efficient (~800 tokens/page), fast startup, stable element references, built-in stealth.

## Prerequisites

```bash
# Install (pick one)
curl -fsSL https://pinchtab.com/install.sh | bash
brew install pinchtab/tap/pinchtab
npm install -g pinchtab

# Start server (skip if already running)
pinchtab server &
curl -s http://localhost:9867/health
```

## Core Concepts

```
Server → Profile (prof_XXX) → Instance (inst_XXX) → Tab (tab_XXX) → Element Refs (e0, e1, e5)
```

- **Profile** — Persistent browser data (cookies, storage). Reuse profiles to keep login sessions alive.
- **Instance** — Running Chrome process (max 1 per profile).
- **Element Ref** — Stable IDs from snapshots for clicking/filling. Re-snapshot after page changes because refs become stale.

## Choosing the Right Approach

| Situation | Approach | Why |
|-----------|----------|-----|
| Hầu hết tasks | **CLI** | Đơn giản, không cần parse JSON, 1 lệnh = 1 hành động |
| Cần batch actions hoặc tích hợp script | **HTTP API** | Batch/macro endpoint giảm request overhead |
| Chỉ cần đọc nội dung trang | `pinchtab text` | Token-efficient nhất (~800 tokens) |
| Cần tương tác (click, fill) | `pinchtab snap -ic` → action | Compact interactive snapshot cho refs, rồi act |
| Sau khi thực hiện action | `pinchtab snap -d` | Diff snapshot — chỉ lấy thay đổi, tiết kiệm token |
| Cần debug visual | `pinchtab screenshot` | Token cost cao — chỉ dùng khi text/snap không đủ |
| Site có bot detection | Bật stealth trước | `pinchtab config set chrome.stealth light` |

## CLI Workflow (Default)

```bash
# 1. Navigate
pinchtab nav https://example.com

# 2. Read content (chọn 1)
pinchtab text              # plain text — most efficient
pinchtab snap -ic          # interactive elements only — for interaction
pinchtab quick <url>       # navigate + snapshot in one command

# 3. Interact
pinchtab fill e3 "value"   # fill field (clears first)
pinchtab click e5          # click element
pinchtab press Enter       # keyboard key

# 4. Verify result
sleep 1                    # wait for page update
pinchtab snap -d           # diff snapshot — only changes
```

### Multi-Tab

```bash
pinchtab tab new https://source.com    # open new tab
pinchtab tab                           # list tabs with IDs
pinchtab tab tab_XXX                   # switch to tab
pinchtab tab close tab_XXX             # close tab
```

## Security Gates

5 tính năng nhạy cảm bị **tắt mặc định**. Nếu dùng upload, download, eval, macro, hoặc screencast mà bị lỗi, bật gate tương ứng:

```bash
pinchtab config set security.allowUpload true      # cho pinchtab upload
pinchtab config set security.allowDownload true     # cho pinchtab download
pinchtab config set security.allowEvaluate true     # cho pinchtab eval
pinchtab config set security.allowMacro true        # cho POST /macro
pinchtab config set security.allowScreencast true   # cho pinchtab screencast
```

Upload limits mặc định: 5 MB/file, 8 file/request, 10 MB tổng.

**Lưu ý PinchTab 0.10+:** `GET /api/config` trả config dạng nested (`config.security.allowUpload`) thay vì flat (`security.allowUpload`). Script cần hỗ trợ cả hai format khi kiểm tra permission. Setting áp dụng ngay sau `pinchtab config set`, không cần restart server.

## Error Recovery

Lỗi phổ biến nhất: **stale element refs** (action fail vì trang đã thay đổi).

```
Action fail → re-snapshot (pinchtab snap -ic) → retry với ref mới
```

| Lỗi | Xử lý |
|-----|--------|
| Element ref not found | Re-snapshot, dùng ref mới |
| Upload/Download/Eval fail | Bật security gate tương ứng (xem mục trên) |
| Server not running | `pinchtab server &` |
| Instance won't start | Kiểm tra `pinchtab instances`, stop instance cũ nếu cần |
| Bot detection | `pinchtab config set chrome.stealth light` + `--humanize` flag |

## Environment Variables

| Variable | Purpose | Default |
|----------|---------|---------|
| `PINCHTAB_PORT` | Server port | 9867 |
| `PINCHTAB_TOKEN` | API auth token (thêm `-H "Authorization: Bearer $TOKEN"` nếu set) | (none) |
| `PINCHTAB_HEADLESS` | Headless mode | true |

## Reference

Chi tiết tra cứu khi cần:

- [HTTP API](references/api-reference.md) — Endpoints, payloads, response formats, error codes. Đọc khi cần gọi HTTP API trực tiếp.
- [CLI commands](references/cli-reference.md) — Tất cả CLI commands + flags. Đọc khi cần tìm lệnh cụ thể hoặc flags nâng cao.
- [Workflow patterns](references/workflow-patterns.md) — 12 patterns phổ biến (scraping, login, pagination, stealth, multi-tab...). Đọc khi gặp scenario phức tạp cần tham khảo.
