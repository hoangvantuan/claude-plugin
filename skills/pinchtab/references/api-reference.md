# PinchTab API Reference

Base URL: `http://localhost:9867` (default)

All responses follow this format:

```json
{"success": true, "data": {...}, "error": null}
```

Error responses:

```json
{"success": false, "error": "message", "code": "ERR_CODE"}
```

---

## Server

| Method | Endpoint | Purpose |
|--------|----------|---------|
| GET | `/health` | Server status, tab count, crash logs |
| POST | `/ensure-chrome` | Force initialize Chrome (idempotent) |
| GET | `/help` | List all available endpoints |
| GET | `/openapi.json` | OpenAPI 3.0 specification |
| GET | `/metrics` | Global metrics (uptime, instance/tab counts) |
| POST | `/shutdown` | Graceful server shutdown |
| GET | `/api/events` | SSE stream — real-time events (init, action, system, monitoring) |
| GET | `/welcome` | Dashboard welcome page |

---

## Profiles

| Method | Endpoint | Body | Purpose |
|--------|----------|------|---------|
| GET | `/profiles` | — | List all profiles |
| POST | `/profiles` | `{"name":"str","description":"str"}` | Create profile |
| GET | `/profiles/{prof}` | — | Get profile details |
| PUT | `/profiles/{prof}` | `{"name":"str","description":"str"}` | Update profile |
| DELETE | `/profiles/{prof}` | — | Delete profile and all data |

**Profile ID format:** `prof_XXXXXXXX`

---

## Instances

| Method | Endpoint | Body | Purpose |
|--------|----------|------|---------|
| GET | `/instances` | — | List running instances |
| POST | `/instances/start` | `{"mode":"headless"\|"headed","profileId":"prof_XXX"}` | Launch Chrome |
| GET | `/instances/{inst}` | — | Instance details |
| POST | `/instances/{inst}/stop` | — | Stop instance |
| GET | `/instances/{inst}/port` | — | Get bridge port |
| POST | `/instances/attach` | `{"name":"str","cdpUrl":"ws://..."}` | Attach existing Chrome |

**Instance ID format:** `inst_XXXXXXXX`

**Rules:**
- Max 1 active instance per profile
- `headless` = no visible window (default). `headed` = visible window (debugging)
- Start response returns `id` and `port` — port is the **bridge** port

### Bridge (Direct Instance Access)

Each instance exposes a bridge on `http://localhost:<port>`. Direct access without instance/tab IDs:

| Method | Endpoint | Body | Purpose |
|--------|----------|------|---------|
| POST | `/navigate` | `{"url":"https://..."}` | Navigate to URL |
| GET | `/snapshot` | — | Accessibility tree |
| POST | `/action` | `{"kind":"click","ref":"e5"}` | Execute action |

**Bridge uses `kind` (not `type`) for action field:**

| Action | Bridge Payload |
|--------|---------------|
| click | `{"kind":"click","ref":"e5"}` |
| type | `{"kind":"type","ref":"e3","text":"hello"}` |
| press | `{"kind":"press","key":"Enter"}` |

---

## Tabs

| Method | Endpoint | Body | Purpose |
|--------|----------|------|---------|
| GET | `/instances/{inst}/tabs` | — | List open tabs |
| POST | `/instances/{inst}/tabs/open` | `{"url":"https://..."}` | Open new tab |
| GET | `/instances/{inst}/tabs/{tab}` | — | Get tab info |
| POST | `/instances/{inst}/tabs/{tab}/close` | — | Close tab |
| GET | `/instances/{inst}/tabs/{tab}/metrics` | — | Per-tab metrics |
| POST | `/tab/lock` | — | Lock current tab |
| POST | `/tab/unlock` | — | Unlock current tab |

**Tab ID format:** `tab_XXXXXXXX`

---

## Tab Content

| Method | Endpoint | Purpose | Token Cost |
|--------|----------|---------|------------|
| GET | `.../tabs/{tab}/text` | Plain text extraction | ~800 |
| GET | `.../tabs/{tab}/snapshot` | Accessibility tree + element refs | ~800 |
| GET | `.../tabs/{tab}/screenshot` | PNG screenshot | High |

### Snapshot Query Parameters

| Param | Values | Purpose |
|-------|--------|---------|
| `interactive` | `true` | Only interactive elements |
| `compact` | `true` | Compact format |
| `format` | `diff` | Only changed elements since last snapshot |

### Snapshot Response

```json
{
  "success": true,
  "data": {
    "url": "https://example.com",
    "title": "Example Domain",
    "tree": [
      {"ref": "e0", "type": "header", "text": "Example Domain"},
      {"ref": "e1", "type": "paragraph", "text": "This domain is..."},
      {"ref": "e5", "type": "link", "text": "More info", "clickable": true}
    ]
  }
}
```

---

## Navigation

| Method | Endpoint | Body | Purpose |
|--------|----------|------|---------|
| POST | `/navigate` | `{"url":"str","timeout":30000,"blockImages":bool,"blockAds":bool,"newTab":bool}` | Navigate current/new tab |
| POST | `/instances/{inst}/tabs/{tab}/navigate` | `{"url":"https://..."}` | Navigate specific tab |
| POST | `/back` | — | Go back |
| POST | `/forward` | — | Go forward |
| POST | `/reload` | — | Reload page |

---

## Actions

### Single Action

`POST /instances/{inst}/tabs/{tab}/action` or `POST /action` (bridge)

| Action | Payload |
|--------|---------|
| click | `{"type":"click","ref":"e5"}` |
| dblclick | `{"type":"dblclick","ref":"e5"}` |
| type | `{"type":"type","ref":"e3","text":"hello"}` |
| fill | `{"type":"fill","ref":"e3","value":"email@x.com"}` |
| key | `{"type":"key","key":"Enter"}` |
| scroll | `{"type":"scroll","direction":"down","amount":3}` |
| focus | `{"type":"focus","ref":"e5"}` |
| hover | `{"type":"hover","ref":"e5"}` |
| select | `{"type":"select","ref":"e7","value":"opt-id"}` |
| check | `{"type":"check","ref":"e4"}` |
| uncheck | `{"type":"uncheck","ref":"e4"}` |
| drag | `{"type":"drag","ref":"e3","target":"e5"}` |

Common keys: `Enter`, `Tab`, `Escape`, `Backspace`, `ArrowDown`, `ArrowUp`, `Control+a`, `Space`

### Batch Actions

`POST /actions` — Execute multiple actions sequentially:

```json
{
  "actions": [
    {"type":"fill","ref":"e3","value":"user@example.com"},
    {"type":"fill","ref":"e5","value":"password"},
    {"type":"click","ref":"e8"}
  ]
}
```

### Macro (Per-Step Timeout)

`POST /macro` — Multi-step with individual timeouts:

```json
{
  "steps": [
    {"action":{"type":"click","ref":"e8"},"timeout":5000},
    {"action":{"type":"fill","ref":"e3","value":"data"},"timeout":3000}
  ]
}
```

---

## Page Analysis

| Method | Endpoint | Body/Params | Purpose |
|--------|----------|-------------|---------|
| GET | `/snapshot` | `?interactive=true&compact=true&format=diff` | Accessibility tree |
| GET | `/text` | — | Plain text extraction |
| POST | `/find` | `{"query":"login button","limit":5,"threshold":0.7}` | Semantic element search |
| POST | `/evaluate` | `{"expression":"document.title"}` | Execute JavaScript (requires `security.allowEvaluate = true`) |

---

## Media & Files

| Method | Endpoint | Purpose | Security Gate |
|--------|----------|---------|---------------|
| GET | `/screenshot` | Tab screenshot (`?quality=95&format=png\|jpeg\|webp`) | — |
| GET | `/pdf` | PDF export (`?landscape=true&scale=1.5`) | — |
| GET | `/download` | File download via browser | `security.allowDownload` |
| POST | `/upload` | File upload (`{"selector":"input[type=file]","filePath":"/path"}`) | `security.allowUpload` |
| GET | `/screencast` | WebRTC stream URL | `security.allowScreencast` |

> **Security gates**: Các endpoint có cột Security Gate bị **tắt mặc định**. Phải bật trong config trước khi gọi, nếu không sẽ trả `ERR_UPLOAD_FAILED` / `ERR_DOWNLOAD_FAILED`.

---

## Cookies

| Method | Endpoint | Purpose |
|--------|----------|---------|
| GET | `/cookies` | Get cookies (`?domain=example.com&path=/admin`) |
| POST | `/cookies` | Set cookie |

### Set Cookie Body

```json
{
  "name": "session_id",
  "value": "abc123",
  "domain": ".example.com",
  "secure": true,
  "httpOnly": true,
  "sameSite": "Lax"
}
```

---

## Tasks (Queue)

| Method | Endpoint | Purpose |
|--------|----------|---------|
| POST | `/tasks` | Submit task (`{"name":"str","payload":{...},"priority":1,"timeout":60000}`) |
| GET | `/tasks` | List queued/running tasks |
| GET | `/tasks/{id}` | Task details |
| POST | `/tasks/{id}/cancel` | Cancel task |

---

## Configuration

| Method | Endpoint | Purpose |
|--------|----------|---------|
| GET | `/api/config` | Current configuration |
| PUT | `/api/config` | Update config (server.token excluded from dashboard) |

### Key Config Options

```json
{
  "server.port": 9867,
  "server.bind": "127.0.0.1",
  "chrome.headless": true,
  "chrome.stealth": "light",
  "dashboard.enabled": true,
  "logging.level": "info"
}
```

### Sensitive Endpoint Gates

5 tính năng nhạy cảm bị **tắt mặc định** (`false`). Bật qua `PUT /api/config` hoặc CLI `pinchtab config set`:

| Key | Ảnh hưởng endpoint |
|-----|---------------------|
| `security.allowUpload` | `POST /upload` |
| `security.allowDownload` | `GET /download` |
| `security.allowEvaluate` | `POST /evaluate` |
| `security.allowMacro` | `POST /macro` |
| `security.allowScreencast` | `GET /screencast` |

Upload limits khi đã bật:

| Key | Mặc định |
|-----|----------|
| `security.uploadMaxFileBytes` | 5 MB |
| `security.uploadMaxFiles` | 8 |
| `security.uploadMaxTotalBytes` | 10 MB |

---

## Authentication

If `PINCHTAB_TOKEN` is set:

```bash
curl -H "Authorization: Bearer $PINCHTAB_TOKEN" http://localhost:9867/health
```

All API calls must include the Bearer token header when auth is enabled.

Default security: localhost-only (`server.bind = 127.0.0.1`). For remote access, use SSH tunneling or reverse proxy.

---

## Error Codes

| Code | Meaning |
|------|---------|
| `ERR_ELEMENT_NOT_FOUND` | Ref/selector doesn't match |
| `ERR_ACTION_TIMEOUT` | Action exceeded timeout |
| `ERR_NAVIGATION_TIMEOUT` | Page load exceeded timeout |
| `ERR_INVALID_INSTANCE` | Instance doesn't exist or stopped |
| `ERR_INVALID_TAB` | Tab doesn't exist |
| `ERR_SCRIPT_ERROR` | JavaScript evaluation failed |
| `ERR_DOWNLOAD_FAILED` | File download error |
| `ERR_UPLOAD_FAILED` | File upload error |

Common errors:
- `Instance not found` — instance was stopped or doesn't exist
- `Profile already has active instance` — stop existing instance first
- `Element ref not found` — re-fetch snapshot, refs may have changed
