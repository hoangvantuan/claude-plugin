---
name: pinchtab
description: Browser automation for AI agents via PinchTab HTTP API and CLI. Use whenever the user wants to control a browser, navigate websites, extract page content, fill forms, click elements, scrape data, automate web workflows, take screenshots, export PDFs, run JavaScript on pages, manage cookies, or do anything involving web browsing. Also trigger when user mentions "pinchtab", "browser automation", "open website", "scrape page", "fill form", "click button", "get page text", "web automation", "headless browser", "web scraping", "page screenshot", "download file from web", or any task requiring interaction with web pages.
allowed-tools:
  - Bash
  - Read
---

# PinchTab — Browser Automation for AI Agents

Control Chrome browsers via PinchTab's CLI and HTTP API. Token-efficient (~800 tokens/page), fast startup, stable element references, built-in stealth.

## Prerequisites

```bash
# Install (pick one)
curl -fsSL https://pinchtab.com/install.sh | bash   # one-liner
brew install pinchtab/tap/pinchtab                    # Homebrew
npm install -g pinchtab                               # npm (Node 18+)

# Start server
pinchtab server &
curl -s http://localhost:9867/health
```

If the server is already running, skip the start step.

## Core Concepts

- **Server** — HTTP API + dashboard on port 9867
- **Profile** (`prof_XXX`) — Persistent browser data (cookies, storage, extensions). The durable object.
- **Instance** (`inst_XXX`) — Running Chrome process (1 per profile max). The runtime object.
- **Tab** (`tab_XXX`) — Individual browser tab within an instance
- **Element Ref** (`e0`, `e1`, `e5`) — Stable IDs for interactive elements from snapshots

```
Server → Profile → Instance → Tab → Element Refs
```

## CLI Workflow (Recommended)

The CLI is the simplest way to automate. No curl, no JSON parsing.

```bash
# Navigate to a page
pinchtab nav https://example.com

# Get accessibility snapshot (element refs for interaction)
pinchtab snap

# Interactive elements only (compact)
pinchtab snap -ic

# Click an element
pinchtab click e5

# Fill a form field (clears first)
pinchtab fill e3 "user@example.com"

# Type text (appends)
pinchtab type e3 "search query"

# Press keyboard key
pinchtab press Enter

# Extract plain text (most token-efficient)
pinchtab text

# Take screenshot
pinchtab screenshot

# Quick: navigate + snapshot in one command
pinchtab quick https://example.com
```

### CLI Multi-Step Example

```bash
# Login flow
pinchtab nav https://app.example.com/login
pinchtab snap -i          # show interactive elements
pinchtab fill e3 "user@example.com"
pinchtab fill e5 "password123"
pinchtab click e8         # submit button
sleep 2
pinchtab snap             # verify logged in
```

### Tab Management (CLI)

```bash
pinchtab tab                    # list all tabs
pinchtab tab new https://x.com  # open new tab
pinchtab tab close tab_XXX      # close tab
```

## HTTP API Workflow

For programmatic control when CLI isn't sufficient:

```bash
BASE="http://localhost:9867"

# 1. Create profile
PROF=$(curl -s -X POST "$BASE/profiles" \
  -H "Content-Type: application/json" \
  -d '{"name":"my-profile"}' | python3 -c "import sys,json; print(json.load(sys.stdin)['data']['id'])")

# 2. Start instance
INST=$(curl -s -X POST "$BASE/instances/start" \
  -H "Content-Type: application/json" \
  -d "{\"mode\":\"headless\",\"profileId\":\"$PROF\"}" \
  | python3 -c "import sys,json; print(json.load(sys.stdin)['data']['id'])")

# 3. Open tab
TAB=$(curl -s -X POST "$BASE/instances/$INST/tabs/open" \
  -H "Content-Type: application/json" \
  -d '{"url":"https://example.com"}' \
  | python3 -c "import sys,json; print(json.load(sys.stdin)['data']['id'])")

# 4. Snapshot (accessibility tree with element refs)
curl -s "$BASE/instances/$INST/tabs/$TAB/snapshot"

# 5. Interact
curl -s -X POST "$BASE/instances/$INST/tabs/$TAB/action" \
  -H "Content-Type: application/json" \
  -d '{"type":"click","ref":"e5"}'

# 6. Extract text
curl -s "$BASE/instances/$INST/tabs/$TAB/text"
```

## Action Types

Use with `POST /instances/{inst}/tabs/{tab}/action` or CLI commands:

| Action | HTTP Payload | CLI |
|--------|-------------|-----|
| **click** | `{"type":"click","ref":"e5"}` | `pinchtab click e5` |
| **dblclick** | `{"type":"dblclick","ref":"e5"}` | `pinchtab dblclick e5` |
| **type** | `{"type":"type","ref":"e3","text":"hello"}` | `pinchtab type e3 "hello"` |
| **fill** | `{"type":"fill","ref":"e3","value":"email"}` | `pinchtab fill e3 "email"` |
| **press** | `{"type":"key","key":"Enter"}` | `pinchtab press Enter` |
| **scroll** | `{"type":"scroll","direction":"down","amount":3}` | `pinchtab scroll --down` |
| **hover** | `{"type":"hover","ref":"e5"}` | `pinchtab hover e5` |
| **select** | `{"type":"select","ref":"e7","value":"opt"}` | `pinchtab select e7 "opt"` |
| **check** | `{"type":"check","ref":"e4"}` | `pinchtab check e4` |
| **uncheck** | `{"type":"uncheck","ref":"e4"}` | `pinchtab uncheck e4` |

## Reading Page Content

From most to least token-efficient:

| Method | Tokens | CLI | HTTP |
|--------|--------|-----|------|
| **Text** | ~800 | `pinchtab text` | `GET .../tabs/{tab}/text` |
| **Snapshot** | ~800 + refs | `pinchtab snap` | `GET .../tabs/{tab}/snapshot` |
| **Snapshot (compact)** | Less | `pinchtab snap -ic` | `GET /snapshot?interactive=true&compact=true` |
| **Diff snapshot** | Minimal | `pinchtab snap -d` | `GET /snapshot?format=diff` |
| **Screenshot** | High | `pinchtab screenshot` | `GET .../tabs/{tab}/screenshot` |

Always prefer **text** or **snapshot** over screenshot. Use **diff snapshot** after interactions to get only changed elements.

## Advanced Features

### Batch Actions

Execute multiple actions in sequence with one request:

```bash
curl -s -X POST "$BASE/actions" \
  -H "Content-Type: application/json" \
  -d '{"actions":[
    {"type":"fill","ref":"e3","value":"user@example.com"},
    {"type":"fill","ref":"e5","value":"password"},
    {"type":"click","ref":"e8"}
  ]}'
```

### Macro (Multi-Step with Timeouts)

```bash
curl -s -X POST "$BASE/macro" \
  -H "Content-Type: application/json" \
  -d '{"steps":[
    {"action":{"type":"click","ref":"e8"},"timeout":5000},
    {"action":{"type":"fill","ref":"e3","value":"data"},"timeout":3000}
  ]}'
```

### JavaScript Evaluation

```bash
# CLI
pinchtab eval "document.title"

# HTTP
curl -s -X POST "$BASE/evaluate" \
  -H "Content-Type: application/json" \
  -d '{"expression":"document.querySelectorAll(\"a\").length"}'
```

### Find Elements (Semantic Search)

```bash
# CLI
pinchtab find "login button"

# HTTP
curl -s -X POST "$BASE/find" \
  -H "Content-Type: application/json" \
  -d '{"query":"login button","limit":5}'
```

### Cookies Management

```bash
# Get cookies
curl -s "$BASE/cookies?domain=example.com"

# Set cookie
curl -s -X POST "$BASE/cookies" \
  -H "Content-Type: application/json" \
  -d '{"name":"session","value":"abc123","domain":".example.com","secure":true}'
```

### PDF Export

```bash
# CLI
pinchtab pdf

# HTTP
curl -s "$BASE/pdf" --output page.pdf
```

### File Download & Upload

```bash
# Download file via browser
curl -s "$BASE/download" --output file.pdf

# Upload file to input element
curl -s -X POST "$BASE/upload" \
  -H "Content-Type: application/json" \
  -d '{"selector":"input[type=file]","filePath":"/path/to/file.pdf"}'
```

### Navigation with Blocking

```bash
# Block images and ads for faster loading
pinchtab nav https://example.com --block-images --block-ads
```

### Stealth Mode (Anti-Detection)

Bypass bot detection (Cloudflare, reCAPTCHA):

```bash
# Configure stealth level
pinchtab config set chrome.stealth light   # recommended
# Options: none (default) | light (UA+webdriver patch) | full (canvas/WebGL spoofing)

# Humanized interactions (natural mouse/keyboard)
pinchtab click e0 --humanize
```

### Attach Existing Chrome

```bash
# Start Chrome with debug port
google-chrome --remote-debugging-port=9222 &

# Attach to PinchTab
curl -s -X POST "$BASE/instances/attach" \
  -H "Content-Type: application/json" \
  -d '{"name":"my-chrome","cdpUrl":"ws://127.0.0.1:9222/devtools/browser/..."}'
```

## Cleanup

```bash
# Stop instance
curl -s -X POST "$BASE/instances/$INST/stop"

# Or delete profile entirely
curl -s -X DELETE "$BASE/profiles/$PROF"
```

## Environment Variables

| Variable | Purpose | Default |
|----------|---------|---------|
| `PINCHTAB_PORT` | Server port | 9867 |
| `PINCHTAB_TOKEN` | API auth token | (none) |
| `PINCHTAB_HEADLESS` | Headless mode | true |

If `PINCHTAB_TOKEN` is set, include: `-H "Authorization: Bearer $PINCHTAB_TOKEN"`

## Troubleshooting

| Issue | Solution |
|-------|----------|
| Server not running | `pinchtab server &` |
| Port conflict | `pinchtab config set server.port 8080` |
| Instance won't start | Check active: `curl -s $BASE/instances` |
| Stale element refs | Re-snapshot after page changes |
| Auth required | Set `PINCHTAB_TOKEN` and include Bearer header |
| Bot detection | `pinchtab config set chrome.stealth light` |
| Slow page load | `pinchtab nav URL --block-images --block-ads` |

## Reference

- Full HTTP API: [references/api-reference.md](references/api-reference.md)
- CLI commands: [references/cli-reference.md](references/cli-reference.md)
- Workflow patterns: [references/workflow-patterns.md](references/workflow-patterns.md)
