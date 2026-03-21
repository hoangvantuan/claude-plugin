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
  --publish <true|false> \
  --mode <headed|headless>
```

**Parameters:**

| Param | Required | Default | Description |
|-------|----------|---------|-------------|
| `--profile` | No | `default` | PinchTab profile name (must have Facebook session) |
| `--user-id` | Yes | — | Facebook numeric user ID (e.g., `100003782705460`) |
| `--content` | Yes | — | Post text content (supports multi-line) |
| `--tag` | No | — | Friend's display name to tag |
| `--publish` | No | `false` | `true` = publish immediately, `false` = prepare only |
| `--mode` | No | `headed` | `headed` = visible browser, `headless` = background |

**Examples:**

```bash
# Post + tag, preview before publishing
bash scripts/fb-post.sh \
  --profile default \
  --user-id 100003782705460 \
  --tag "Hoang Van Tuan" \
  --content "Hello world!" \
  --publish false

# Post without tag, publish immediately
bash scripts/fb-post.sh \
  --profile default \
  --user-id 100003782705460 \
  --content "Quick update from CLI" \
  --publish true

# Headless mode (no browser window)
bash scripts/fb-post.sh \
  --profile default \
  --user-id 100003782705460 \
  --content "Background post" \
  --mode headless \
  --publish true
```

## How It Works

The script uses PinchTab's accessibility snapshot to find UI elements by role and Vietnamese text labels:

1. **Start/reuse browser** — checks for running instance with the profile, starts one if needed
2. **Navigate to wall** — opens `facebook.com/profile.php?id=<user-id>`
3. **Open post dialog** — finds and clicks the "Ban dang nghi gi?" button
4. **Type content** — uses `inserttext` to preserve line breaks
5. **Tag friend** (optional) — opens tag dialog, searches by name, selects first match
6. **Publish or hold** — clicks "Dang" button or leaves dialog open for manual review

## Important Notes

- The script finds Facebook UI elements by Vietnamese labels (`nghi gi`, `gan the nguoi khac`, `tim kiem`, `xong`, `dang`). If the user's Facebook language is not Vietnamese, the element search will fail — adjust keywords accordingly.
- Default `--publish false` is a safety net: the post dialog stays open so the user can review before publishing.
- Use `--mode headed` (default) when debugging or when the user wants to see the browser. Use `headless` for automated/scheduled posts.
- The `--user-id` is the numeric Facebook ID, not the vanity URL. Find it via facebook.com profile URL or page source.

## Troubleshooting

| Issue | Solution |
|-------|----------|
| "Cannot find button" | Facebook UI may have changed, or language is not Vietnamese. Check `pinchtab snap` output. |
| Session expired | Re-login manually in headed mode to refresh cookies in the profile. |
| Browser won't start | Ensure `pinchtab server` is running and no conflicting instance exists. |
| Content not typed | Try `--mode headed` to visually debug. Ensure dialog is fully loaded (increase sleep). |
