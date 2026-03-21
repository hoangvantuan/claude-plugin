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
# Positional syntax (content as first argument)
bash "$(dirname "$0")/scripts/fb-post.sh" "<content>" [options]

# Named syntax
bash "$(dirname "$0")/scripts/fb-post.sh" --content "<content>" [options]
```

**Parameters:**

| Param              | Required | Default   | Description                                                      |
| ------------------ | -------- | --------- | ---------------------------------------------------------------- |
| `<content>`        | Yes      | —         | First positional arg = post content (alternative to `--content`) |
| `--content`        | Yes*     | —         | Post text content (supports multi-line). *Not needed if positional arg used |
| `--profile`        | No       | `default` | PinchTab profile name (must have Facebook session)               |
| `--user-id`        | No       | auto      | Facebook user ID (wall mode). Omit to auto-detect                |
| `--group`          | No       | —         | Group slug or full URL. When set, posts to group instead of wall |
| `--tag`            | No       | —         | Friend's display name to tag                                     |
| `--tag-id`         | No       | —         | Friend's Facebook ID for precise tag matching                    |
| `--publish`        | No       | `false`   | `true` = publish immediately, `false` = prepare only             |
| `--mode`           | No       | `headed`  | `headed` = visible browser, `headless` = background              |
| `--debug`          | No       | `false`   | Save screenshots at each step to `/tmp/` for review              |
| `--dry-run`        | No       | —         | Log all actions without browser interaction (for testing)        |
| `--keep-instance`  | No       | —         | Don't stop browser instance on exit (for reuse across runs)      |

### 1. Post to Personal Wall

```bash
# Positional arg — simplest form
bash scripts/fb-post.sh "Hello world!"

# Post + tag friend
bash scripts/fb-post.sh "Hello world!" --tag "Hoang Van Tuan" --publish false

# Post to specific user's wall
bash scripts/fb-post.sh "Quick update" --user-id 100003782705460 --publish true

# Dry run — verify params without opening browser
bash scripts/fb-post.sh "Test content" --tag "Ngoc" --dry-run
```

### 2. Post to Group

```bash
# Post to group by slug
bash scripts/fb-post.sh "Hello group!" --group tuhoccungai --publish false

# Post to group by full URL
bash scripts/fb-post.sh "Nội dung bài viết" \
  --group "https://www.facebook.com/groups/tuhoccungai" --publish true

# Post to group + tag someone
bash scripts/fb-post.sh "Check this out!" \
  --group tuhoccungai --tag "Ngoc" --publish true

# Headless + keep instance for next run
bash scripts/fb-post.sh "Automated post" \
  --group tuhoccungai --mode headless --keep-instance --publish true
```

## How It Works

The script uses PinchTab's accessibility snapshot to find UI elements by role and **multi-language keywords** (Vietnamese, English). Each element lookup tries all supported language variants until a match is found — no locale configuration needed.

1. **Start/reuse browser** — checks for running instance, health-checks before reuse (restarts stale instances)
2. **Navigate** — wall mode: opens user profile (auto-detect or `--user-id`); group mode: opens group URL
3. **Validate page** — in group mode, verifies the create-post button exists before continuing (early error for wrong URL or no access)
4. **Open post dialog** — clicks button with retry logic: verifies textbox appeared, retries up to 3 times if click didn't open dialog
5. **Type content** — uses `inserttext` to preserve line breaks
6. **Tag friend** (optional) — opens tag dialog, searches by name, selects via keyboard (ArrowDown + Enter); uses `--tag-id` for precise match, prioritizes "Bạn bè" (friends) when matching by name
7. **Publish or hold** — uses **exact match** for "Đăng"/"Post" button to avoid clicking "Đăng ẩn danh" (anonymous post)

### Wall vs Group Differences

| Aspect             | Wall mode              | Group mode                      |
| ------------------ | ---------------------- | ------------------------------- |
| Navigation         | `facebook.com/me` or profile ID | Group URL (slug or full) |
| Create post button | "nghĩ gì" / "what's on your mind" | "viết gì" / "write something" |
| Page validation    | —                      | Checks create-post button exists |
| Post textbox       | Same keyword set       | Same keyword set                |
| Tagging            | Identical workflow     | Identical workflow              |
| Publish button     | Exact match "Đăng"    | Exact match "Đăng"             |

## Exit Codes

| Code | Meaning                                              |
| ---- | ---------------------------------------------------- |
| `0`  | Success                                              |
| `1`  | Missing or invalid arguments                         |
| `2`  | Instance failure (can't start browser, bad profile)  |
| `3`  | Element not found (button, textbox, or page invalid) |
| `4`  | Publish failed (publish button not found)            |

## Important Notes

- Element matching uses **multi-language keywords with accent-insensitive Unicode normalization** — works regardless of Facebook's display language.
- Default `--publish false` is a safety net: the post dialog stays open so the user can review before publishing.
- Use `--mode headed` (default) when debugging or when the user wants to see the browser. Use `headless` for automated/scheduled posts.
- The `--user-id` is the numeric Facebook ID, not the vanity URL. Find it via facebook.com profile URL or page source.
- Use `--debug true` to capture screenshots at each step (saved to `/tmp/fb-post-debug-<timestamp>/`).
- Use `--dry-run` to validate parameters and see what the script would do without opening a browser.
- Use `--keep-instance` to avoid stopping the browser after the script finishes — useful for chaining multiple posts.
- When tagging, use `--tag-id` to avoid selecting the wrong person when multiple results share the same name.
- The **publish button uses exact match** to avoid clicking "Đăng ẩn danh" (post anonymously) in groups.
- Tag search results in Facebook are **not directly clickable** — the script uses keyboard navigation (ArrowDown + Enter) as a workaround.

## Instance Lifecycle

Scripts reuse running instances by default. Use `--keep-instance` to prevent auto-cleanup after the script finishes — useful when chaining multiple posts or continuing manual work in the same browser session.

**Start instance manually** (if no script has started one yet):

```bash
# Headed — visible browser for debugging or manual login
pinchtab instance start --profile default --mode headed

# Headless — background automation
pinchtab instance start --profile default --mode headless
```

**Stop instance after a session** — stop when done to free resources and avoid stale instances:

```bash
# List running instances
pinchtab instance list

# Stop a specific instance
pinchtab instance stop <instance_id>
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
| Bad profile name       | Script shows clear error with exit code 2. Verify profile exists in PinchTab.              |
| Group not accessible   | Script validates group page early (exit code 3). Check URL and membership.                 |
| Dialog didn't open     | Script retries click up to 3 times automatically. Check `--debug true` screenshots.        |
