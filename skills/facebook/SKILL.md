---
name: facebook
description: Facebook automation via PinchTab browser control. Use when the user wants to post on Facebook wall, post to Facebook groups, tag friends in posts, schedule Facebook content, automate Facebook interactions, or manage Facebook posting workflows. Trigger on mentions of "facebook", "fb", "dang bai", "post len wall", "post len group", "tag ban be", "facebook wall post", "facebook group post", or any task involving creating/publishing content on Facebook.
allowed-tools:
  - Bash
  - Read
---

# Facebook Automation via PinchTab

Automate Facebook tasks using PinchTab browser control. This skill manages browser instances with saved profiles (cookies/sessions) so you don't need to re-login each time.

## Prerequisites

- **PinchTab** installed and server running (`pinchtab server &`)
- A PinchTab **profile** with an active Facebook login session (cookies saved from a previous manual login)
- The profile name (default: `default`)

If the user hasn't logged in yet, guide them to start a headed instance, manually log into Facebook, then reuse that profile for automation.

## Available Workflows

Both workflows use the same script with different parameters. The script handles instance lifecycle, element lookup, tagging, and publishing automatically.

**Script:** `scripts/fb-post.sh`

```bash
bash "$(dirname "$0")/scripts/fb-post.sh" \
  --profile <profile_name> \
  --user-id <facebook_user_id> \
  --group <group_slug_or_url> \
  --content "<post content>" \
  --tag "<friend name>" \
  --tag-id "<friend facebook id>" \
  --publish <true|false> \
  --mode <headed|headless> \
  --debug <true|false>
```

**Parameters:**

| Param       | Required | Default   | Description                                                   |
| ----------- | -------- | --------- | ------------------------------------------------------------- |
| `--profile` | No       | `default` | PinchTab profile name (must have Facebook session)            |
| `--user-id` | No       | auto      | Facebook user ID (wall mode). Omit to auto-detect             |
| `--group`   | No       | —         | Group slug or full URL. When set, posts to group instead of wall |
| `--content` | Yes      | —         | Post text content (supports multi-line)                       |
| `--tag`     | No       | —         | Friend's display name to tag                                  |
| `--tag-id`  | No       | —         | Friend's Facebook ID for precise tag matching                 |
| `--publish` | No       | `false`   | `true` = publish immediately, `false` = prepare only          |
| `--mode`    | No       | `headed`  | `headed` = visible browser, `headless` = background           |
| `--debug`   | No       | `false`   | Save screenshots at each step to `/tmp/` for review           |

### 1. Post to Personal Wall

```bash
# Post to own wall, preview before publishing
bash scripts/fb-post.sh \
  --content "Hello world!" \
  --publish false

# Post + tag friend
bash scripts/fb-post.sh \
  --tag "Hoang Van Tuan" \
  --content "Hello world!" \
  --publish false

# Post to specific user's wall
bash scripts/fb-post.sh \
  --user-id 100003782705460 \
  --content "Quick update from CLI" \
  --publish true
```

### 2. Post to Group

```bash
# Post to group by slug
bash scripts/fb-post.sh \
  --group tuhoccungai \
  --content "Hello group!" \
  --publish false

# Post to group by full URL
bash scripts/fb-post.sh \
  --group "https://www.facebook.com/groups/tuhoccungai" \
  --content "Nội dung bài viết cho group" \
  --publish true

# Post to group + tag someone
bash scripts/fb-post.sh \
  --group tuhoccungai \
  --content "Check this out!" \
  --tag "Ngoc" \
  --publish true

# Headless mode
bash scripts/fb-post.sh \
  --group tuhoccungai \
  --content "Automated post" \
  --mode headless \
  --publish true
```

## How It Works

The script uses PinchTab's accessibility snapshot to find UI elements by role and **multi-language keywords** (Vietnamese, English). Each element lookup tries all supported language variants until a match is found — no locale configuration needed.

1. **Start/reuse browser** — checks for running instance, health-checks before reuse (restarts stale instances)
2. **Navigate** — wall mode: opens user profile (auto-detect or `--user-id`); group mode: opens group URL
3. **Open post dialog** — wall uses "nghĩ gì" button, group uses "viết gì" button (auto-selected based on mode)
4. **Type content** — uses `inserttext` to preserve line breaks
5. **Tag friend** (optional) — opens tag dialog, searches by name, selects via keyboard (ArrowDown + Enter) because search results aren't directly clickable; uses `--tag-id` for precise match
6. **Publish or hold** — uses **exact match** for "Đăng"/"Post" button to avoid clicking "Đăng ẩn danh" (anonymous post)

### Wall vs Group Differences

| Aspect             | Wall mode              | Group mode                      |
| ------------------ | ---------------------- | ------------------------------- |
| Navigation         | `facebook.com/me` or profile ID | Group URL (slug or full) |
| Create post button | "nghĩ gì" / "what's on your mind" | "viết gì" / "write something" |
| Post textbox       | Same keyword set       | Same keyword set                |
| Tagging            | Identical workflow     | Identical workflow              |
| Publish button     | Exact match "Đăng"    | Exact match "Đăng"             |

## Important Notes

- Element matching uses **multi-language keywords with accent-insensitive Unicode normalization** — works regardless of Facebook's display language.
- Default `--publish false` is a safety net: the post dialog stays open so the user can review before publishing.
- Use `--mode headed` (default) when debugging or when the user wants to see the browser. Use `headless` for automated/scheduled posts.
- The `--user-id` is the numeric Facebook ID, not the vanity URL. Find it via facebook.com profile URL or page source.
- Use `--debug true` to capture screenshots at each step (saved to `/tmp/fb-post-debug-<timestamp>/`).
- When tagging, use `--tag-id` to avoid selecting the wrong person when multiple results share the same name.
- The **publish button uses exact match** to avoid clicking "Đăng ẩn danh" (post anonymously) in groups.
- Tag search results in Facebook are **not directly clickable** — the script uses keyboard navigation (ArrowDown + Enter) as a workaround.

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

