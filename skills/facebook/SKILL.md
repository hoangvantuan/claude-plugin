---
name: facebook
description: Facebook automation via PinchTab browser control. Use when the user wants to post on Facebook wall, tag friends in posts, schedule Facebook content, automate Facebook interactions, or manage Facebook posting workflows. Trigger on mentions of "facebook", "fb", "dang bai", "post len wall", "tag ban be", "facebook wall post", or any task involving creating/publishing content on Facebook.
allowed-tools:
  - Bash
  - Read
---

# Facebook Automation via PinchTab

Automate Facebook tasks using PinchTab browser control. This skill manages browser instances with saved profiles (cookies/sessions) so you don't need to re-login each time.

## Prerequisites

- **PinchTab** installed and server running (`pinchtab server &`)
- A PinchTab **profile** with an active Facebook login session (cookies saved from a previous manual login)
- The profile name (default: `default`) and the target Facebook user ID

If the user hasn't logged in yet, guide them to start a headed instance, manually log into Facebook, then reuse that profile for automation.

## Available Workflows

### 1. Post to Personal Wall

Post content to a Facebook user's wall, optionally tag friends.

**Script:** `scripts/fb-post.sh`

```bash
bash "$(dirname "$0")/scripts/fb-post.sh" \
  --profile <profile_name> \
  --user-id <facebook_user_id> \
  --content "<post content>" \
  --tag "<friend name>" \
  --tag-id "<friend facebook id>" \
  --publish <true|false> \
  --mode <headed|headless> \
  --debug <true|false>
```

**Parameters:**

| Param       | Required | Default   | Description                                          |
| ----------- | -------- | --------- | ---------------------------------------------------- |
| `--profile` | No       | `default` | PinchTab profile name (must have Facebook session)   |
| `--user-id` | No       | auto      | Facebook user ID. Omit to auto-detect from session   |
| `--content` | Yes      | —         | Post text content (supports multi-line)              |
| `--tag`     | No       | —         | Friend's display name to tag                         |
| `--tag-id`  | No       | —         | Friend's Facebook ID for precise tag matching        |
| `--publish` | No       | `false`   | `true` = publish immediately, `false` = prepare only |
| `--mode`    | No       | `headed`  | `headed` = visible browser, `headless` = background  |
| `--debug`   | No       | `false`   | Save screenshots at each step to `/tmp/` for review  |


**Examples:**

```bash
# Post to own wall (auto-detect profile), preview before publishing
bash scripts/fb-post.sh \
  --content "Hello world!" \
  --publish false

# Post + tag friend, auto-detect profile
bash scripts/fb-post.sh \
  --tag "Hoang Van Tuan" \
  --content "Hello world!" \
  --publish false

# Post to specific user's wall
bash scripts/fb-post.sh \
  --user-id 100003782705460 \
  --content "Quick update from CLI" \
  --publish true

# Headless mode (no browser window)
bash scripts/fb-post.sh \
  --content "Background post" \
  --mode headless \
  --publish true
```

## How It Works

The script uses PinchTab's accessibility snapshot to find UI elements by role and **multi-language keywords** (Vietnamese, English). Each element lookup tries all supported language variants until a match is found — no locale configuration needed.

1. **Start/reuse browser** — checks for running instance, health-checks before reuse (restarts stale instances)
2. **Navigate to wall** — if `--user-id` given, opens that profile; otherwise navigates to `facebook.com/me` to auto-detect logged-in user's wall
3. **Open post dialog** — poll-waits for create post button across languages ("nghĩ gì", "what's on your mind", etc.)
4. **Type content** — uses `inserttext` to preserve line breaks
5. **Tag friend** (optional) — opens tag dialog, searches by name, prioritizes friend results across languages; uses `--tag-id` for precise match; falls back to keyboard if element is not clickable
6. **Publish or hold** — clicks publish button or leaves dialog open for manual review

## Important Notes

- Element matching uses **multi-language keywords with accent-insensitive Unicode normalization** — works regardless of Facebook's display language.
- Default `--publish false` is a safety net: the post dialog stays open so the user can review before publishing.
- Use `--mode headed` (default) when debugging or when the user wants to see the browser. Use `headless` for automated/scheduled posts.
- The `--user-id` is the numeric Facebook ID, not the vanity URL. Find it via facebook.com profile URL or page source.
- Use `--debug true` to capture screenshots at each step (saved to `/tmp/fb-post-debug-<timestamp>/`).
- When tagging, use `--tag-id` to avoid selecting the wrong person when multiple results share the same name.

## Instance Lifecycle

Scripts reuse running instances by default but do **not** auto-close them — the user may want to continue browsing or run another workflow on the same session.

**Start instance manually** (if no script has started one yet):

```bash
# Headed — visible browser for debugging or manual login
pinchtab instance start --profile default --mode headed

# Headless — background automation
pinchtab instance start --profile default --mode headless
```

**Stop instance after a session** — always stop when done to free resources and avoid stale instances:

```bash
# List running instances
pinchtab instance list

# Stop a specific instance
pinchtab instance stop <instance_id>

# Stop all instances for a profile
curl -s http://localhost:9867/instances -H "Authorization: Bearer $TOKEN" \
  | python3 -c "
import sys, json
for i in json.load(sys.stdin):
    if i.get('status') == 'running':
        print(i['id'])
" | xargs -I{} pinchtab instance stop {}
```

If an instance becomes stale (commands timeout), the scripts auto-detect and restart it. To force-restart manually: stop then start again.

## Troubleshooting

| Issue                  | Solution                                                                                   |
| ---------------------- | ------------------------------------------------------------------------------------------ |
| "Cannot find button"   | Facebook UI may have changed. Use `--debug true` and check screenshots + `pinchtab snap`.  |
| Session expired        | Re-login manually in headed mode to refresh cookies in the profile.                        |
| Browser won't start    | Ensure `pinchtab server` is running and no conflicting instance exists.                    |
| Stale instance         | Script auto-detects and restarts. Manual fix: `pinchtab instance stop <id>`.               |
| Wrong person tagged    | Use `--tag-id <facebook_id>` for precise matching instead of name-only search.             |
| Element not clickable  | Script auto-falls back to keyboard navigation (ArrowDown + Enter).                         |

