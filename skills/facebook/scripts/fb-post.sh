#!/bin/bash
# =============================================================
# Facebook Personal Wall Post + Tag User via PinchTab
# =============================================================
# Usage:
#   ./fb-post.sh --profile default \
#                --user-id 100003782705460 \
#                --content "Noi dung bai viet" \
#                --tag "Hoang Van Tuan" \
#                --publish false \
#                --debug true
# =============================================================

set -euo pipefail

# ---- Default config ----
PROFILE="default"
USER_ID=""
CONTENT=""
TAG_NAME=""
TAG_ID=""
PUBLISH="false"
MODE="headed"
DEBUG="false"
DEBUG_DIR="/tmp/fb-post-debug-$(date +%s)"

# ---- Parse arguments ----
while [[ $# -gt 0 ]]; do
  case $1 in
    --profile)  PROFILE="$2";  shift 2 ;;
    --user-id)  USER_ID="$2";  shift 2 ;;
    --content)  CONTENT="$2";  shift 2 ;;
    --tag)      TAG_NAME="$2"; shift 2 ;;
    --tag-id)   TAG_ID="$2";   shift 2 ;;
    --publish)  PUBLISH="$2";  shift 2 ;;
    --mode)     MODE="$2";     shift 2 ;;
    --debug)    DEBUG="$2";    shift 2 ;;
    *) echo "Unknown option: $1"; exit 1 ;;
  esac
done

if [[ -z "$USER_ID" || -z "$CONTENT" ]]; then
  echo "Required: --user-id <facebook_user_id> --content <content>"
  exit 1
fi

# ---- Helpers ----
TOKEN=$(python3 -c "import json; print(json.load(open('$HOME/.pinchtab/config.json'))['server']['token'])")
BASE="http://localhost:9867"
AUTH="Authorization: Bearer $TOKEN"

# Debug screenshot helper — captures screenshot at key steps when --debug true
debug_screenshot() {
  if [[ "$DEBUG" == "true" ]]; then
    mkdir -p "$DEBUG_DIR"
    local step_name="$1"
    pinchtab screenshot "$DEBUG_DIR/${step_name}.png" 2>/dev/null || true
    echo "   [debug] Screenshot: $DEBUG_DIR/${step_name}.png"
  fi
}

# Accent-insensitive search: normalize Vietnamese diacritics before matching
# This handles both accented ("nghĩ gì") and non-accented ("nghi gi") keywords
snap_find() {
  local role="$1" keyword="$2"
  pinchtab snap 2>/dev/null | python3 -c "
import sys, json, unicodedata
def normalize(s):
    return unicodedata.normalize('NFD', s.lower())
role = '$role'
kw = normalize('$keyword')
for n in json.load(sys.stdin)['nodes']:
    if n['role'] == role and kw in normalize(n.get('name','')):
        print(n['ref']); break
" 2>/dev/null
}

snap_find_button() { snap_find "button" "$1"; }
snap_find_textbox() { snap_find "textbox" "$1"; }

# Poll-based wait: retry snap_find until element appears or timeout
# Usage: wait_for_element <role> <keyword> [timeout_seconds=10]
wait_for_element() {
  local role="$1" keyword="$2" timeout="${3:-10}" elapsed=0
  while [[ $elapsed -lt $timeout ]]; do
    local ref
    ref=$(snap_find "$role" "$keyword")
    if [[ -n "$ref" ]]; then
      echo "$ref"
      return 0
    fi
    sleep 1
    elapsed=$((elapsed + 1))
  done
  return 1
}

# Health check: verify instance is responsive by attempting a snap
# Returns 0 if healthy, 1 if stale/unresponsive
instance_health_check() {
  local inst_id="$1"
  # Try snap with 5s timeout — if it hangs, instance is stale
  timeout 5 pinchtab snap >/dev/null 2>&1
  return $?
}

# Safe click with keyboard fallback for non-focusable elements
safe_click() {
  local ref="$1"
  if ! pinchtab click "$ref" 2>&1 | grep -qi "not focusable"; then
    return 0
  fi
  # Fallback: use keyboard navigation
  echo "   [fallback] Element not focusable, using keyboard"
  pinchtab press ArrowDown >/dev/null 2>&1
  sleep 0.5
  pinchtab press Enter >/dev/null 2>&1
}

# Track whether we created the instance (to auto-stop on exit)
CREATED_INSTANCE="false"

# Cleanup: auto-stop instance if we created it
cleanup() {
  if [[ "$CREATED_INSTANCE" == "true" && -n "${INST:-}" ]]; then
    echo ""
    echo "Stopping instance $INST..."
    pinchtab instance stop "$INST" 2>/dev/null || true
    echo "   -> Instance stopped."
  fi
}
trap cleanup EXIT

start_new_instance() {
  INST=$(pinchtab instance start --profile "$PROFILE" --mode "$MODE" 2>/dev/null \
    | python3 -c "import sys,json; print(json.load(sys.stdin)['id'])")
  CREATED_INSTANCE="true"
  echo "   -> Created instance: $INST"
  sleep 3
}

# =============================================================
# STEP 1: Start browser instance with health check
# =============================================================
echo "[1/6] Starting browser with profile: $PROFILE"

EXISTING=$(curl -s "$BASE/instances" -H "$AUTH" 2>/dev/null | python3 -c "
import sys, json
for i in json.load(sys.stdin):
    if i.get('profileName') == '$PROFILE' and i.get('status') == 'running':
        print(i['id']); break
" 2>/dev/null || true)

if [[ -n "$EXISTING" ]]; then
  if instance_health_check "$EXISTING"; then
    INST="$EXISTING"
    echo "   -> Reusing healthy instance: $INST"
  else
    echo "   -> Instance $EXISTING is stale, restarting..."
    pinchtab instance stop "$EXISTING" 2>/dev/null || true
    sleep 1
    start_new_instance
  fi
else
  start_new_instance
fi

# =============================================================
# STEP 2: Navigate to personal wall
# =============================================================
echo "[2/6] Opening profile page: $USER_ID"

pinchtab nav "https://www.facebook.com/profile.php?id=$USER_ID" >/dev/null 2>&1

# Wait for page load by checking for title in snap (not URL — FB redirects)
TITLE=""
for i in $(seq 1 10); do
  TITLE=$(pinchtab snap 2>/dev/null | python3 -c "
import sys, json
nodes = json.load(sys.stdin).get('nodes',[])
print(nodes[0].get('name','') if nodes else '')
" 2>/dev/null || true)
  [[ -n "$TITLE" ]] && break
  sleep 1
done
echo "   -> Page: $TITLE"
debug_screenshot "02-profile-page"

# =============================================================
# STEP 3: Open "Create post" dialog
# =============================================================
echo "[3/6] Opening create post dialog"

BTN_CREATE=$(wait_for_element "button" "nghĩ gì" 10)
if [[ -z "$BTN_CREATE" ]]; then
  echo "ERROR: Cannot find 'Bạn đang nghĩ gì?' button."
  debug_screenshot "03-error-no-button"
  exit 1
fi

pinchtab click "$BTN_CREATE" >/dev/null 2>&1
debug_screenshot "03-post-dialog"

# =============================================================
# STEP 4: Type post content
# =============================================================
echo "[4/6] Typing post content"

TXT_POST=$(wait_for_element "textbox" "nghĩ gì" 5)
if [[ -z "$TXT_POST" ]]; then
  echo "ERROR: Cannot find post textbox."
  debug_screenshot "04-error-no-textbox"
  exit 1
fi

pinchtab click "$TXT_POST" >/dev/null 2>&1
sleep 0.5
pinchtab keyboard inserttext "$CONTENT" >/dev/null 2>&1
sleep 1
echo "   -> Content entered (${#CONTENT} chars)"
debug_screenshot "04-content-entered"

# =============================================================
# STEP 5: Tag user (optional)
# =============================================================
if [[ -n "$TAG_NAME" ]]; then
  echo "[5/6] Tagging: $TAG_NAME"

  BTN_TAG=$(snap_find_button "gắn thẻ người khác")
  if [[ -z "$BTN_TAG" ]]; then
    # Fallback: try finding tag button by partial match
    BTN_TAG=$(snap_find_button "gắn thẻ")
  fi

  if [[ -z "$BTN_TAG" ]]; then
    echo "   WARN: Tag button not found, skipping."
  else
    pinchtab click "$BTN_TAG" >/dev/null 2>&1

    TXT_SEARCH=$(wait_for_element "textbox" "tìm kiếm" 5)
    if [[ -n "$TXT_SEARCH" ]]; then
      pinchtab click "$TXT_SEARCH" >/dev/null 2>&1
      sleep 0.5
      pinchtab keyboard type "$TAG_NAME" >/dev/null 2>&1

      # Wait for search results to appear
      sleep 2
      debug_screenshot "05-tag-search-results"

      if [[ -n "$TAG_ID" ]]; then
        # Precise selection by user ID — find the exact match in results
        TAG_REF=$(pinchtab snap 2>/dev/null | python3 -c "
import sys, json
for n in json.load(sys.stdin)['nodes']:
    if '$TAG_ID' in n.get('name','') or '$TAG_ID' in n.get('description',''):
        print(n['ref']); break
" 2>/dev/null || true)
        if [[ -n "$TAG_REF" ]]; then
          safe_click "$TAG_REF"
        else
          echo "   WARN: Tag ID $TAG_ID not found in results, selecting first friend"
          pinchtab press ArrowDown >/dev/null 2>&1
          sleep 0.3
          pinchtab press Enter >/dev/null 2>&1
        fi
      else
        # Prioritize results labeled "Bạn bè" (Friends) over pages/other
        TAG_REF=$(pinchtab snap 2>/dev/null | python3 -c "
import sys, json, unicodedata
def norm(s): return unicodedata.normalize('NFD', s.lower())
nodes = json.load(sys.stdin)['nodes']
# Prefer friend results over pages
friend_ref = None
first_ref = None
for n in nodes:
    name = n.get('name','')
    desc = n.get('description','')
    if norm('$TAG_NAME') in norm(name) or norm('$TAG_NAME') in norm(desc):
        if first_ref is None:
            first_ref = n['ref']
        if 'bạn bè' in desc.lower() or 'friend' in desc.lower():
            friend_ref = n['ref']; break
print(friend_ref or first_ref or '')
" 2>/dev/null || true)

        if [[ -n "$TAG_REF" ]]; then
          safe_click "$TAG_REF"
        else
          # Fallback: keyboard selection
          pinchtab press ArrowDown >/dev/null 2>&1
          sleep 0.3
          pinchtab press Enter >/dev/null 2>&1
        fi
      fi

      sleep 2

      # Click "Xong" (Done)
      BTN_DONE=$(snap_find_button "xong")
      if [[ -n "$BTN_DONE" ]]; then
        pinchtab click "$BTN_DONE" >/dev/null 2>&1
        sleep 1
        echo "   -> Tagged successfully"
      fi
    fi
  fi
else
  echo "[5/6] No tagging (skipped)"
fi

# =============================================================
# STEP 6: Publish or hold
# =============================================================
if [[ "$PUBLISH" == "true" ]]; then
  echo "[6/6] Publishing..."
  BTN_POST=$(wait_for_element "button" "đăng" 5)
  if [[ -n "$BTN_POST" ]]; then
    pinchtab click "$BTN_POST" >/dev/null 2>&1
    sleep 3
    echo "   -> Post published!"
    debug_screenshot "06-published"
  else
    echo "   -> ERROR: Publish button not found"
    debug_screenshot "06-error-no-publish"
  fi
else
  echo "[6/6] Post ready, NOT PUBLISHED."
  echo "   -> Open browser and click 'Post' when ready."
  debug_screenshot "06-ready"
fi

if [[ "$DEBUG" == "true" ]]; then
  echo ""
  echo "Debug screenshots saved to: $DEBUG_DIR"
fi

echo ""
echo "Done!"
