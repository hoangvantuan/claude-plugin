#!/bin/bash
# =============================================================
# Facebook Post (Wall / Group) + Tag User via PinchTab
# =============================================================
# Usage (positional):
#   fb-post.sh <content> [options]
#
# Usage (named):
#   fb-post.sh --content "Noi dung" --group tuhoccungai --publish true
#
# Examples:
#   fb-post.sh "Hello world!"
#   fb-post.sh "Hello group!" --group tuhoccungai --publish true
#   fb-post.sh "Tag post" --tag "Ngoc" --tag-id 12345 --publish false
# =============================================================

set -uo pipefail

# ---- Exit codes ----
EXIT_OK=0
EXIT_ARGS=1
EXIT_INSTANCE=2
EXIT_ELEMENT=3
EXIT_PUBLISH=4

# ---- Structured logging (architecture C) ----
log() {
  local level="$1"; shift
  printf "[%s] [%-5s] %s\n" "$(date '+%H:%M:%S')" "$level" "$*"
}
log_info()  { log "INFO"  "$@"; }
log_warn()  { log "WARN"  "$@"; }
log_error() { log "ERROR" "$@"; }

# ---- Default config ----
PROFILE="default"
USER_ID=""
GROUP=""
CONTENT=""
TAG_NAME=""
TAG_ID=""
PUBLISH="false"
MODE="headed"
DEBUG="false"
DRY_RUN="false"
KEEP_INSTANCE="false"
DEBUG_DIR="/tmp/fb-post-debug-$(date +%s)"
SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"

# ---- Parse arguments (positional + named) ----
# First non-option argument is content (positional arg support)
if [[ $# -gt 0 && "${1:0:2}" != "--" ]]; then
  CONTENT="$1"; shift
fi

while [[ $# -gt 0 ]]; do
  case $1 in
    --profile)        PROFILE="$2";        shift 2 ;;
    --user-id)        USER_ID="$2";        shift 2 ;;
    --group)          GROUP="$2";          shift 2 ;;
    --content)        CONTENT="$2";        shift 2 ;;
    --tag)            TAG_NAME="$2";       shift 2 ;;
    --tag-id)         TAG_ID="$2";         shift 2 ;;
    --publish)        PUBLISH="$2";        shift 2 ;;
    --mode)           MODE="$2";           shift 2 ;;
    --debug)          DEBUG="$2";          shift 2 ;;
    --dry-run)        DRY_RUN="true";      shift ;;
    --keep-instance)  KEEP_INSTANCE="true"; shift ;;
    *) log_error "Unknown option: $1"; exit $EXIT_ARGS ;;
  esac
done

if [[ -z "$CONTENT" ]]; then
  log_error "Required: content (positional arg or --content <content>)"
  echo "Usage: fb-post.sh <content> [options]"
  echo "       fb-post.sh --content <content> [options]"
  exit $EXIT_ARGS
fi

# Determine posting mode: group or wall
if [[ -n "$GROUP" ]]; then
  POST_MODE="group"
  if [[ "$GROUP" == http* ]]; then
    GROUP_URL="$GROUP"
  else
    GROUP_URL="https://www.facebook.com/groups/$GROUP"
  fi
else
  POST_MODE="wall"
fi

if [[ "$DRY_RUN" == "true" ]]; then
  log_info "[DRY-RUN] Mode enabled — no browser actions will be performed"
  log_info "[DRY-RUN] Post mode: $POST_MODE"
  log_info "[DRY-RUN] Content: ${CONTENT:0:80}..."
  [[ -n "$TAG_NAME" ]] && log_info "[DRY-RUN] Tag: $TAG_NAME (ID: ${TAG_ID:-none})"
  [[ -n "$GROUP" ]] && log_info "[DRY-RUN] Group: ${GROUP_URL:-$GROUP}"
  log_info "[DRY-RUN] Publish: $PUBLISH"

  # Validate profile exists in PinchTab (requires server running)
  PROFILE_CHECK=$(curl -s "$BASE/profiles" -H "$AUTH" 2>/dev/null \
    | SNAP_PROFILE="$PROFILE" python3 -c "
import sys, json, os
profile = os.environ['SNAP_PROFILE']
try:
    profiles = json.load(sys.stdin)
    # Support both list format and {data: [...]} format
    if isinstance(profiles, dict):
        profiles = profiles.get('data', [])
    found = any(p.get('name') == profile for p in profiles)
    print('found' if found else 'missing')
except: print('unknown')
" 2>/dev/null) || true

  if [[ "$PROFILE_CHECK" == "missing" ]]; then
    log_error "[DRY-RUN] Profile '$PROFILE' not found in PinchTab!"
    exit $EXIT_INSTANCE
  elif [[ "$PROFILE_CHECK" == "found" ]]; then
    log_info "[DRY-RUN] Profile '$PROFILE' verified OK"
  else
    log_warn "[DRY-RUN] Cannot verify profile (server not running?)"
  fi

  exit $EXIT_OK
fi

# ---- Multi-language keywords for Facebook UI elements ----
KW_CREATE_POST_WALL="nghĩ gì|what's on your mind"
KW_CREATE_POST_GROUP="viết gì|write something"
KW_POST_TEXTBOX="bài viết|create a post|what's on your mind|nghĩ gì|viết gì"
KW_TAG_OTHERS="gắn thẻ người khác|gắn thẻ|tag people|tag others"
KW_SEARCH="tìm kiếm|search"
KW_DONE="xong|done"
KW_PUBLISH="đăng|post"
KW_FRIEND="bạn bè|friend"

if [[ "$POST_MODE" == "group" ]]; then
  KW_CREATE_POST="$KW_CREATE_POST_GROUP"
else
  KW_CREATE_POST="$KW_CREATE_POST_WALL"
fi

# ---- Helpers ----
TOKEN=$(PINCHTAB_CONFIG="$HOME/.pinchtab/config.json" python3 -c "
import json, os
print(json.load(open(os.environ['PINCHTAB_CONFIG']))['server']['token'])
")
BASE="http://localhost:9867"
AUTH="Authorization: Bearer $TOKEN"

# ---- Human-like random delay to avoid bot detection ----
# Usage: human_delay <min_ms> <max_ms>
# Sleeps for a random duration between min and max milliseconds
human_delay() {
  local min_ms="${1:-500}" max_ms="${2:-1500}"
  local range=$((max_ms - min_ms))
  local delay_ms=$((min_ms + RANDOM % (range + 1)))
  local delay_s
  delay_s=$(python3 -c "print($delay_ms / 1000.0)")
  sleep "$delay_s"
}

debug_screenshot() {
  if [[ "$DEBUG" == "true" ]]; then
    mkdir -p "$DEBUG_DIR"
    local step_name="$1"
    pinchtab screenshot -o "$DEBUG_DIR/${step_name}.png" 2>/dev/null || true
    log_info "[debug] Screenshot: $DEBUG_DIR/${step_name}.png"
  fi
}

# Element search using external Python helper (architecture A — no inline Python escaping issues)
# Uses stdin pipe instead of env var to avoid OS env size limits on large pages
snap_find_multi() {
  local role="$1" keywords="$2"
  pinchtab snap 2>/dev/null \
    | SNAP_ROLE="$role" SNAP_KW="$keywords" SNAP_MODE="multi" \
      python3 "$SCRIPT_DIR/snap-helpers.py"
}

snap_find_exact() {
  local role="$1" keywords="$2"
  pinchtab snap 2>/dev/null \
    | SNAP_ROLE="$role" SNAP_KW="$keywords" SNAP_MODE="exact" \
      python3 "$SCRIPT_DIR/snap-helpers.py"
}

snap_find_button_multi() { snap_find_multi "button" "$1"; }
snap_find_textbox_multi() { snap_find_multi "textbox" "$1"; }

# Poll-based wait (fix #6: || true to prevent set -e killing script)
wait_for_element_multi() {
  local role="$1" keywords="$2" timeout="${3:-10}" elapsed=0
  while [[ $elapsed -lt $timeout ]]; do
    local ref
    ref=$(snap_find_multi "$role" "$keywords") || true
    if [[ -n "$ref" ]]; then
      echo "$ref"
      return 0
    fi
    sleep 1
    elapsed=$((elapsed + 1))
  done
  return 1
}

wait_for_element_exact() {
  local role="$1" keywords="$2" timeout="${3:-10}" elapsed=0
  while [[ $elapsed -lt $timeout ]]; do
    local ref
    ref=$(snap_find_exact "$role" "$keywords") || true
    if [[ -n "$ref" ]]; then
      echo "$ref"
      return 0
    fi
    sleep 1
    elapsed=$((elapsed + 1))
  done
  return 1
}

instance_health_check() {
  local inst_id="$1"
  timeout 5 pinchtab snap --instance "$inst_id" >/dev/null 2>&1
  return $?
}

safe_click() {
  local ref="$1"
  if ! pinchtab click "$ref" 2>&1 | grep -qi "not focusable"; then
    return 0
  fi
  log_warn "Element not focusable, using keyboard fallback"
  pinchtab press ArrowDown >/dev/null 2>&1
  human_delay 300 700
  pinchtab press Enter >/dev/null 2>&1
}

# Insert text via HTTP API — avoids shell escaping that truncates long/special content
# Uses document.execCommand('insertText') which fires proper React input events
insert_text_via_api() {
  local text="$1"
  CONTENT_TEXT="$text" API_BASE="$BASE" API_TOKEN="$TOKEN" python3 << 'PYEOF'
import os, json, urllib.request
content = os.environ['CONTENT_TEXT']
js = 'document.execCommand("insertText", false, ' + json.dumps(content) + ')'
payload = json.dumps({'expression': js}).encode()
req = urllib.request.Request(os.environ['API_BASE'] + '/evaluate', data=payload,
    headers={'Content-Type': 'application/json', 'Authorization': 'Bearer ' + os.environ['API_TOKEN']})
urllib.request.urlopen(req)
PYEOF
}

# Click with retry (fix #7: verify element appeared, retry up to max_retries)
click_and_verify() {
  local click_ref="$1" verify_role="$2" verify_kw="$3"
  local max_retries="${4:-3}" verify_timeout="${5:-10}"

  local attempt=1
  while [[ $attempt -le $max_retries ]]; do
    pinchtab click "$click_ref" >/dev/null 2>&1

    local result
    result=$(wait_for_element_multi "$verify_role" "$verify_kw" "$verify_timeout") || true
    if [[ -n "$result" ]]; then
      echo "$result"
      return 0
    fi

    log_warn "Click attempt $attempt/$max_retries: expected element not found, retrying..."
    human_delay 800 1500
    attempt=$((attempt + 1))
  done

  return 1
}

detect_user_profile() {
  pinchtab nav "https://www.facebook.com/me" >/dev/null 2>&1
  sleep 3
  local current_url
  current_url=$(pinchtab snap 2>/dev/null | python3 -c "
import sys, json
data = json.load(sys.stdin)
print(data.get('url',''))
" 2>/dev/null) || true
  echo "$current_url"
}

# ---- Instance lifecycle (fix #9: --keep-instance support) ----
CREATED_INSTANCE="false"

cleanup() {
  if [[ "$KEEP_INSTANCE" == "true" ]]; then
    log_info "Keeping instance alive (--keep-instance)"
    return
  fi
  if [[ "$CREATED_INSTANCE" == "true" && -n "${INST:-}" ]]; then
    echo ""
    log_info "Stopping instance $INST..."
    pinchtab instance stop "$INST" 2>/dev/null || true
    log_info "Instance stopped."
  fi
}
trap cleanup EXIT

# Fix #4: validate profile exists before parsing JSON
start_new_instance() {
  local raw_output
  raw_output=$(pinchtab instance start --profile "$PROFILE" --mode "$MODE" 2>&1) || true

  INST=$(echo "$raw_output" | python3 -c "
import sys, json
try:
    data = json.load(sys.stdin)
    print(data.get('id', ''))
except (json.JSONDecodeError, KeyError):
    print('')
" 2>/dev/null) || true

  if [[ -z "$INST" ]]; then
    log_error "Cannot start instance with profile '$PROFILE'. Check profile exists."
    log_error "Raw output: $raw_output"
    exit $EXIT_INSTANCE
  fi

  CREATED_INSTANCE="true"
  log_info "Created instance: $INST"
  sleep 3
}

# =============================================================
# STEP 1: Start browser instance with health check
# =============================================================
log_info "[1/6] Starting browser with profile: $PROFILE"

# Fix #5: use env vars for Python inline
EXISTING=$(curl -s "$BASE/instances" -H "$AUTH" 2>/dev/null \
  | SNAP_PROFILE="$PROFILE" python3 -c "
import sys, json, os
profile = os.environ['SNAP_PROFILE']
try:
    for i in json.load(sys.stdin):
        if i.get('profileName') == profile and i.get('status') == 'running':
            print(i['id']); break
except (json.JSONDecodeError, KeyError, TypeError): pass
" 2>/dev/null) || true

if [[ -n "$EXISTING" ]]; then
  if instance_health_check "$EXISTING"; then
    INST="$EXISTING"
    log_info "Reusing healthy instance: $INST"
  else
    log_warn "Instance $EXISTING is stale, restarting..."
    pinchtab instance stop "$EXISTING" 2>/dev/null || true
    sleep 1
    start_new_instance
  fi
else
  start_new_instance
fi

# =============================================================
# STEP 2: Navigate to target (wall or group)
# =============================================================
if [[ "$POST_MODE" == "group" ]]; then
  log_info "[2/6] Opening group: $GROUP_URL"
  pinchtab nav "$GROUP_URL" >/dev/null 2>&1
else
  log_info "[2/6] Opening profile page"
  if [[ -n "$USER_ID" ]]; then
    pinchtab nav "https://www.facebook.com/profile.php?id=$USER_ID" >/dev/null 2>&1
  else
    log_info "No --user-id provided, detecting from logged-in session..."
    PROFILE_URL=$(detect_user_profile)
    if [[ -z "$PROFILE_URL" ]]; then
      log_error "Cannot detect profile. Provide --user-id or ensure Facebook is logged in."
      exit $EXIT_INSTANCE
    fi
    log_info "Detected profile: $PROFILE_URL"
  fi
fi

# Wait for page to load (fix #8: poll-based instead of fixed sleep)
TITLE=""
for i in $(seq 1 15); do
  TITLE=$(pinchtab snap 2>/dev/null | python3 -c "
import sys, json
nodes = json.load(sys.stdin).get('nodes',[])
print(nodes[0].get('name','') if nodes else '')
" 2>/dev/null) || true
  [[ -n "$TITLE" ]] && break
  sleep 1
done
log_info "Page: $TITLE"
debug_screenshot "02-page-loaded"

# Fix #10: validate group page has create-post button before continuing
if [[ "$POST_MODE" == "group" ]]; then
  GROUP_CHECK=$(snap_find_button_multi "$KW_CREATE_POST") || true
  if [[ -z "$GROUP_CHECK" ]]; then
    log_error "Cannot access group or not a member. Check group URL: $GROUP_URL"
    debug_screenshot "02-error-invalid-group"
    exit $EXIT_ELEMENT
  fi
fi

# =============================================================
# STEP 3: Open "Create post" dialog (fix #7: click with retry)
# =============================================================
log_info "[3/6] Opening create post dialog"

BTN_CREATE=$(wait_for_element_multi "button" "$KW_CREATE_POST" 10) || true
if [[ -z "$BTN_CREATE" ]]; then
  log_error "Cannot find create post button in any supported language."
  debug_screenshot "03-error-no-button"
  exit $EXIT_ELEMENT
fi

# Click and verify textbox appeared (fix #7 + #8: retry + smart wait)
TXT_POST=$(click_and_verify "$BTN_CREATE" "textbox" "$KW_POST_TEXTBOX" 3 10) || true
if [[ -z "$TXT_POST" ]]; then
  log_error "Cannot find post textbox after clicking create post button."
  debug_screenshot "03-error-no-textbox"
  exit $EXIT_ELEMENT
fi
debug_screenshot "03-post-dialog"

# =============================================================
# STEP 4: Type post content
# =============================================================
log_info "[4/6] Typing post content"

pinchtab click "$TXT_POST" >/dev/null 2>&1
human_delay 400 900
# HTTP API insertText — bypasses CLI argument parsing that truncates on special chars
if ! insert_text_via_api "$CONTENT" 2>/dev/null; then
  log_warn "API insertText failed, falling back to CLI type"
  pinchtab type "$TXT_POST" "$CONTENT" >/dev/null 2>&1
fi
human_delay 800 2000
log_info "Content entered (${#CONTENT} chars)"
debug_screenshot "04-content-entered"

# =============================================================
# STEP 5: Tag user (optional)
# =============================================================
if [[ -n "$TAG_NAME" ]]; then
  log_info "[5/6] Tagging: $TAG_NAME"

  BTN_TAG=$(wait_for_element_multi "button" "$KW_TAG_OTHERS" 10) || true
  if [[ -z "$BTN_TAG" ]]; then
    log_warn "Tag button not found after 10s, skipping."
  else
    # Click tag button and verify search textbox appeared (retry up to 3 times)
    TXT_SEARCH=$(click_and_verify "$BTN_TAG" "textbox" "$KW_SEARCH" 3 8) || true
    if [[ -n "$TXT_SEARCH" ]]; then
      pinchtab click "$TXT_SEARCH" >/dev/null 2>&1
      human_delay 300 800
      pinchtab type "$TXT_SEARCH" "$TAG_NAME" >/dev/null 2>&1

      # Wait for search results to populate (Facebook AJAX)
      human_delay 1500 3000
      debug_screenshot "05-tag-search-results"

      # Fix #5 + #11: use external Python helper, pipe snap data via stdin
      TAG_REF=$(pinchtab snap 2>/dev/null \
        | TAG_NAME="$TAG_NAME" TAG_ID="$TAG_ID" FRIEND_KW="$KW_FRIEND" \
          python3 "$SCRIPT_DIR/tag-search.py") || true

      if [[ -n "$TAG_REF" ]]; then
        safe_click "$TAG_REF"
      else
        if [[ -n "$TAG_ID" ]]; then
          log_warn "Tag ID $TAG_ID not found in results, selecting first result"
        fi
        pinchtab press ArrowDown >/dev/null 2>&1
        human_delay 200 600
        pinchtab press Enter >/dev/null 2>&1
      fi

      human_delay 1500 2500

      BTN_DONE=$(snap_find_button_multi "$KW_DONE") || true
      if [[ -n "$BTN_DONE" ]]; then
        pinchtab click "$BTN_DONE" >/dev/null 2>&1
        human_delay 800 1500
        log_info "Tagged successfully"
      fi
    fi
  fi
else
  log_info "[5/6] No tagging (skipped)"
fi

# =============================================================
# STEP 6: Publish or hold (exit code D)
# =============================================================
if [[ "$PUBLISH" == "true" ]]; then
  log_info "[6/6] Publishing..."
  BTN_POST=$(wait_for_element_exact "button" "$KW_PUBLISH" 5) || true
  if [[ -n "$BTN_POST" ]]; then
    pinchtab click "$BTN_POST" >/dev/null 2>&1
    human_delay 2000 4000
    log_info "Post published!"
    debug_screenshot "06-published"
  else
    log_error "Publish button not found"
    debug_screenshot "06-error-no-publish"
    exit $EXIT_PUBLISH
  fi
else
  log_info "[6/6] Post ready, NOT PUBLISHED."
  log_info "Open browser and click 'Post' when ready."
  debug_screenshot "06-ready"
fi

if [[ "$DEBUG" == "true" ]]; then
  echo ""
  log_info "Debug screenshots saved to: $DEBUG_DIR"
fi

echo ""
log_info "Done!"
exit $EXIT_OK
