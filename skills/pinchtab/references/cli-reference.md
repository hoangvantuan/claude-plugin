# PinchTab CLI Reference

## Server Management

```bash
pinchtab server              # Start with dashboard + API on :9867
pinchtab bridge              # Start API-only (no dashboard)
pinchtab daemon install      # Install as background daemon
pinchtab daemon start        # Start daemon
pinchtab daemon stop         # Stop daemon
pinchtab daemon restart      # Restart daemon
```

---

## Navigation

```bash
pinchtab nav <url>           # Navigate to URL
  --new-tab                  # Open in new tab
  --tab <id>                 # Navigate existing tab
  --block-images             # Skip image loading
  --block-ads                # Skip ad networks
  --timeout 30000            # Max wait time (ms)

pinchtab quick <url>         # Navigate + snapshot combo (fast page analysis)

pinchtab back [--tab <id>]   # Go back
pinchtab forward [--tab <id>] # Go forward
pinchtab reload [--tab <id>] # Reload page
```

---

## Tab Operations

```bash
pinchtab tab                 # List all tabs
pinchtab tab <id>            # Focus tab
pinchtab tab new [url]       # Create new tab
pinchtab tab close <id>      # Close tab
pinchtab tab metrics <id>    # Per-tab stats
```

---

## Interaction

All commands accept element refs (`e0`, `e5`) or CSS selectors.

```bash
pinchtab click <ref|selector>          # Click element
pinchtab dblclick <ref|selector>       # Double-click
pinchtab type <ref|selector> "text"    # Type text (appends)
pinchtab fill <ref|selector> "value"   # Fill field (clears first)
pinchtab press [ref] <keys>            # Press keyboard key(s)
pinchtab hover <ref|selector>          # Hover over element
pinchtab select <ref|selector> "value" # Select dropdown option
pinchtab check <ref|selector>          # Check checkbox
pinchtab uncheck <ref|selector>        # Uncheck checkbox
pinchtab scroll [--down|--up|--to <ref>] # Scroll page
```

### Common Keys for `press`

`Enter`, `Tab`, `Escape`, `Backspace`, `Space`, `ArrowDown`, `ArrowUp`, `ArrowLeft`, `ArrowRight`, `Control+a`, `Control+c`, `Control+v`

### Humanized Interaction

```bash
pinchtab click e0 --humanize   # Natural mouse path + timing
```

---

## Page Analysis

```bash
pinchtab snap                  # Full accessibility tree snapshot
  -i, --interactive            # Only interactive elements
  -c, --compact                # Compact output format
  -d, --diff                   # Only changes since last snapshot

pinchtab text                  # Extract plain text (~800 tokens)

pinchtab find "query"          # Semantic element search
  --limit 5                    # Max results
  --threshold 0.7              # Match threshold

pinchtab eval "expression"     # Execute JS (requires security.allowEvaluate = true)
```

### Snapshot Flags Combo

```bash
pinchtab snap -ic    # Interactive + compact (most efficient for interaction)
pinchtab snap -d     # Differential (only changes, token-saving after actions)
```

---

## Media & Capture

```bash
pinchtab screenshot            # Capture current tab
  --quality 95                 # Image quality
  --format png|jpeg|webp       # Output format

pinchtab pdf                   # Export page as PDF
  --landscape                  # Landscape orientation
  --scale 1.5                  # Scale factor

pinchtab download "selector"   # Download file (requires security.allowDownload = true)
pinchtab upload "selector" /path/to/file  # Upload file (requires security.allowUpload = true)

pinchtab screencast            # Start WebRTC stream
```

---

## Instance & Profile Management

```bash
# Instances
pinchtab instances             # List running instances
pinchtab instances start       # Start new instance
  --headless true|false        # Headless mode (default: true)
  --profile <prof_id>          # Use specific profile

pinchtab instances stop <id>   # Stop instance
pinchtab instances logs <id>   # View instance logs

# Profiles
pinchtab profiles              # List all profiles
pinchtab profiles create "name" # Create new profile
pinchtab profiles delete <id>  # Delete profile

# Health
pinchtab health                # Server health check
```

---

## Configuration

```bash
pinchtab config init           # Initialize config file
pinchtab config show           # Display current config
pinchtab config get <key>      # Get specific setting
pinchtab config set <key> <val> # Set setting
pinchtab config patch file.json # Patch with JSON file
pinchtab config validate       # Check config syntax
```

### Key Settings

```bash
pinchtab config set server.port 9868
pinchtab config set server.bind 127.0.0.1   # localhost only (secure)
pinchtab config set chrome.headless true
pinchtab config set chrome.stealth light     # none|light|full
pinchtab config set logging.level debug      # debug|info|warn|error
```

---

## Security

```bash
pinchtab security              # Review security posture
pinchtab security up           # Harden configuration
pinchtab security down         # Relax restrictions
```

### Sensitive Endpoint Gates

5 tính năng nhạy cảm bị **tắt mặc định**. Phải bật thủ công trước khi dùng:

| Key | Mặc định | Ảnh hưởng lệnh |
|-----|----------|-----------------|
| `security.allowUpload` | `false` | `pinchtab upload` |
| `security.allowDownload` | `false` | `pinchtab download` |
| `security.allowEvaluate` | `false` | `pinchtab eval` |
| `security.allowMacro` | `false` | `POST /macro` |
| `security.allowScreencast` | `false` | `pinchtab screencast` |

Bật từng gate:

```bash
pinchtab config set security.allowUpload true
pinchtab config set security.allowDownload true
pinchtab config set security.allowEvaluate true
```

### Upload Limits

| Key | Mặc định |
|-----|----------|
| `security.uploadMaxFileBytes` | 5 MB |
| `security.uploadMaxFiles` | 8 file/request |
| `security.uploadMaxTotalBytes` | 10 MB |

### Download Limits

| Key | Mặc định |
|-----|----------|
| `security.downloadMaxBytes` | 20 MB |
| `security.downloadAllowedDomains` | `[]` (tất cả domain) |

---

## MCP Server

Start PinchTab as MCP server for AI agent integration:

```bash
pinchtab mcp                   # Start MCP server (stdio JSON-RPC 2.0)
```

Configure in Claude Desktop / VS Code / Cursor:

```json
{
  "command": "pinchtab",
  "args": ["mcp"]
}
```

Exposes 21 tools: navigate, snapshot, screenshot, text, click, type, press, fill, action, evaluate, pdf, find, tabs, close_tab, health, cookies, wait, monitor.
