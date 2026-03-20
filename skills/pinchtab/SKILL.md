---
name: pinchtab
description: Browser automation for AI agents via PinchTab HTTP API. Use whenever the user wants to control a browser, navigate websites, extract page content, fill forms, click elements, scrape data, automate web workflows, or do anything involving web browsing. Also trigger when user mentions "pinchtab", "browser automation", "open website", "scrape page", "fill form", "click button", "get page text", "web automation", "headless browser", or any task requiring interaction with web pages.
allowed-tools:
  - Bash
  - Read
---

# PinchTab — Browser Automation for AI Agents

Control Chrome browsers via PinchTab's HTTP API. Token-efficient (~800 tokens/page), fast (<100ms startup), stable element references.

## Prerequisites

### Install PinchTab

```bash
# macOS (Homebrew)
brew install pinchtab/tap/pinchtab

# Or download binary from GitHub
curl -fsSL https://github.com/pinchtab/pinchtab/releases/latest/download/pinchtab-darwin-arm64 -o /usr/local/bin/pinchtab && chmod +x /usr/local/bin/pinchtab
```

### Start Server

```bash
# Start server (runs on port 9867)
pinchtab server &

# Verify it's running
curl -s http://localhost:9867/health | python3 -m json.tool
```

If the server is already running, skip this step.

## Core Concepts

- **Server** — HTTP API gateway on port 9867
- **Profile** (`prof_XXX`) — Persistent browser data (cookies, storage, extensions)
- **Instance** (`inst_XXX`) — Running Chrome process (1 per profile max)
- **Tab** (`tab_XXX`) — Individual browser tab within an instance
- **Element Ref** (`e0`, `e1`, `e5`) — Stable IDs for interactive elements on the page

### Hierarchy

```
Server → Profile → Instance → Tab → Element Refs
```

## Standard Workflow

Every browser automation task follows this pattern:

```bash
BASE="http://localhost:9867"

# 1. Create or reuse a profile
PROF=$(curl -s -X POST "$BASE/profiles" \
  -H "Content-Type: application/json" \
  -d '{"name":"my-profile"}' | python3 -c "import sys,json; print(json.load(sys.stdin)['data']['id'])")

# 2. Start a browser instance
INST=$(curl -s -X POST "$BASE/instances/start" \
  -H "Content-Type: application/json" \
  -d "{\"mode\":\"headless\",\"profile\":\"$PROF\"}" | python3 -c "import sys,json; print(json.load(sys.stdin)['data']['id'])")

# 3. Open a tab with URL
TAB=$(curl -s -X POST "$BASE/instances/$INST/tabs/open" \
  -H "Content-Type: application/json" \
  -d '{"url":"https://example.com"}' | python3 -c "import sys,json; print(json.load(sys.stdin)['data']['id'])")

# 4. Get page snapshot (accessibility tree with element refs)
curl -s "$BASE/instances/$INST/tabs/$TAB/snapshot" | python3 -m json.tool

# 5. Interact with elements
curl -s -X POST "$BASE/instances/$INST/tabs/$TAB/action" \
  -H "Content-Type: application/json" \
  -d '{"type":"click","ref":"e5"}'

# 6. Extract text content
curl -s "$BASE/instances/$INST/tabs/$TAB/text" | python3 -m json.tool
```

## Action Types

Use these with `POST /instances/{inst}/tabs/{tab}/action`:

| Action | Payload | Purpose |
|--------|---------|---------|
| **click** | `{"type":"click","ref":"e5"}` | Click element |
| **type** | `{"type":"type","ref":"e3","text":"hello"}` | Type text into field |
| **fill** | `{"type":"fill","ref":"e3","value":"email@x.com"}` | Fill form field |
| **key** | `{"type":"key","key":"Enter"}` | Press keyboard key |
| **scroll** | `{"type":"scroll","direction":"down","amount":3}` | Scroll page |
| **focus** | `{"type":"focus","ref":"e5"}` | Focus element |
| **hover** | `{"type":"hover","ref":"e5"}` | Hover over element |
| **select** | `{"type":"select","ref":"e7","value":"opt-id"}` | Select dropdown option |

## Reading Page Content

Three ways to read page content, from most to least token-efficient:

1. **Text extraction** (~800 tokens) — plain text, no element refs
   ```bash
   curl -s "$BASE/instances/$INST/tabs/$TAB/text"
   ```

2. **Snapshot** (~800 tokens + element refs) — accessibility tree with clickable refs
   ```bash
   curl -s "$BASE/instances/$INST/tabs/$TAB/snapshot"
   ```

3. **Screenshot** (high tokens) — visual capture, use as fallback only
   ```bash
   curl -s "$BASE/instances/$INST/tabs/$TAB/screenshot" --output page.png
   ```

Always prefer **text** or **snapshot** over screenshot for token efficiency.

## Multi-Step Interaction Pattern

For complex tasks (login, form submission, multi-page navigation):

```bash
# 1. Navigate to page
curl -s -X POST "$BASE/instances/$INST/tabs/$TAB/navigate" \
  -H "Content-Type: application/json" -d '{"url":"https://app.example.com/login"}'

# 2. Get snapshot to find form elements
curl -s "$BASE/instances/$INST/tabs/$TAB/snapshot"
# → Returns elements like: e3 (username field), e5 (password field), e8 (submit button)

# 3. Fill form
curl -s -X POST "$BASE/instances/$INST/tabs/$TAB/action" \
  -H "Content-Type: application/json" -d '{"type":"fill","ref":"e3","value":"user@example.com"}'

curl -s -X POST "$BASE/instances/$INST/tabs/$TAB/action" \
  -H "Content-Type: application/json" -d '{"type":"fill","ref":"e5","value":"password123"}'

# 4. Submit
curl -s -X POST "$BASE/instances/$INST/tabs/$TAB/action" \
  -H "Content-Type: application/json" -d '{"type":"click","ref":"e8"}'

# 5. Wait briefly, then get new snapshot
sleep 2
curl -s "$BASE/instances/$INST/tabs/$TAB/snapshot"
```

## Cleanup

Always clean up when done:

```bash
# Stop instance (closes Chrome)
curl -s -X POST "$BASE/instances/$INST/stop"

# Or delete profile entirely (removes all data)
curl -s -X DELETE "$BASE/profiles/$PROF"
```

## Environment Variables

| Variable | Purpose | Default |
|----------|---------|---------|
| `PINCHTAB_PORT` | Server port | 9867 |
| `PINCHTAB_TOKEN` | API auth token | (none) |
| `PINCHTAB_HEADLESS` | Headless mode | true |

If `PINCHTAB_TOKEN` is set, include in requests: `-H "Authorization: Bearer $PINCHTAB_TOKEN"`

## Troubleshooting

| Issue | Solution |
|-------|----------|
| Server not running | `pinchtab server &` |
| Port conflict | `PINCHTAB_PORT=8080 pinchtab server` |
| Instance won't start | Check if profile already has active instance: `curl -s $BASE/instances` |
| Stale element refs | Re-fetch snapshot after page navigation or dynamic content changes |
| Auth required | Set `PINCHTAB_TOKEN` env var and include Bearer token header |

## Reference

For complete API endpoint documentation, read [references/api-reference.md](references/api-reference.md).
For common workflow patterns (scraping, form automation, multi-tab), read [references/workflow-patterns.md](references/workflow-patterns.md).
