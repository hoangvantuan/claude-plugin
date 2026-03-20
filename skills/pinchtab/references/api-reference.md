# PinchTab API Reference

Base URL: `http://localhost:9867` (default)

All responses follow this format:
```json
{"success": true, "data": {...}, "error": null}
```

---

## Server

| Method | Endpoint | Purpose |
|--------|----------|---------|
| GET | `/health` | Server status, profile/instance counts |
| GET | `/api/events` | SSE stream — real-time events (init, actions, metrics) |

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
| POST | `/instances/start` | `{"mode":"headless"\|"headed","profile":"prof_XXX"}` | Launch Chrome instance |
| GET | `/instances/{inst}` | — | Get instance details |
| POST | `/instances/{inst}/stop` | — | Stop instance (closes Chrome) |
| GET | `/instances/{inst}/port` | — | Get bridge port number |

**Instance ID format:** `inst_XXXXXXXX`

**Rules:**
- Max 1 active instance per profile
- `headless` = no visible browser window (default for automation)
- `headed` = visible browser window (for debugging)

---

## Tabs

| Method | Endpoint | Body | Purpose |
|--------|----------|------|---------|
| GET | `/instances/{inst}/tabs` | — | List open tabs |
| POST | `/instances/{inst}/tabs/open` | `{"url":"https://..."}` | Open new tab |
| GET | `/instances/{inst}/tabs/{tab}` | — | Get tab info |
| POST | `/instances/{inst}/tabs/{tab}/close` | — | Close tab |

**Tab ID format:** `tab_XXXXXXXX`

---

## Tab Content

| Method | Endpoint | Purpose | Token Cost |
|--------|----------|---------|------------|
| GET | `/instances/{inst}/tabs/{tab}/text` | Plain text extraction | ~800 |
| GET | `/instances/{inst}/tabs/{tab}/snapshot` | Accessibility tree + element refs | ~800 |
| GET | `/instances/{inst}/tabs/{tab}/screenshot` | PNG screenshot | High |

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

## Tab Navigation

| Method | Endpoint | Body | Purpose |
|--------|----------|------|---------|
| POST | `/instances/{inst}/tabs/{tab}/navigate` | `{"url":"https://..."}` | Navigate to URL |

---

## Tab Actions

**Endpoint:** `POST /instances/{inst}/tabs/{tab}/action`

### Click
```json
{"type": "click", "ref": "e5"}
```

### Type (appends text)
```json
{"type": "type", "ref": "e3", "text": "hello world"}
```

### Fill (replaces field content)
```json
{"type": "fill", "ref": "e3", "value": "john@example.com"}
```

### Key Press
```json
{"type": "key", "key": "Enter"}
```
Common keys: `Enter`, `Tab`, `Escape`, `Backspace`, `ArrowDown`, `ArrowUp`

### Scroll
```json
{"type": "scroll", "direction": "down", "amount": 3}
```
Directions: `up`, `down`, `left`, `right`

### Focus
```json
{"type": "focus", "ref": "e5"}
```

### Hover
```json
{"type": "hover", "ref": "e5"}
```

### Select (dropdown)
```json
{"type": "select", "ref": "e7", "value": "option-id"}
```

---

## Authentication

If `PINCHTAB_TOKEN` is set on the server:

```bash
curl -H "Authorization: Bearer $PINCHTAB_TOKEN" http://localhost:9867/health
```

All API calls must include the Bearer token header when auth is enabled.

---

## Error Responses

```json
{
  "success": false,
  "data": null,
  "error": "Instance not found: inst_XXXXXXXX"
}
```

Common errors:
- `Instance not found` — instance was stopped or doesn't exist
- `Profile already has active instance` — stop existing instance first
- `Element ref not found` — re-fetch snapshot, refs may have changed
- `Tab not found` — tab was closed or doesn't exist
