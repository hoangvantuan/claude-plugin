#!/bin/bash
# =============================================================
# Facebook Personal Wall Post + Tag User via PinchTab
# =============================================================
# Usage:
#   ./fb-post.sh --profile default \
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

if [[ -z "$CONTENT" ]]; then
  echo "Required: --content <content>"
  exit 1
fi

# ---- Multi-language keywords for Facebook UI elements ----
# Pipe-separated: tries each keyword until one matches.
# Covers: Vietnamese, English, French, Spanish, German, Japanese, Korean, Chinese
KW_CREATE_POST="nghĩ gì|what's on your mind|what are you thinking|quoi pensez|was denkst|qué estás pensando"
KW_TAG_OTHERS="gắn thẻ người khác|gắn thẻ|tag people|tag others|marquer des personnes|personen markieren|etiquetar personas"
KW_SEARCH="tìm kiếm|search|rechercher|suchen|buscar"
KW_DONE="xong|done|terminé|fertig|listo|完了"
KW_PUBLISH="đăng|post|publier|posten|publicar"
KW_FRIEND="bạn bè|friend|ami|freund|amigo"

# ---- Helpers ----
TOKEN=$(python3 -c "import json; print(json.load(open('$HOME/.pinchtab/config.json'))['server']['token'])")
BASE="http://localhost:9867"
AUTH="Authorization: Bearer $TOKEN"

debug_screenshot() {
  if [[ "$DEBUG" == "true" ]]; then
    mkdir -p "$DEBUG_DIR"
    local step_name="$1"
    pinchtab screenshot "$DEBUG_DIR/${step_name}.png" 2>/dev/null || true
    echo "   [debug] Screenshot: $DEBUG_DIR/${step_name}.png"
  fi
}

# Multi-keyword element search: tries each pipe-separated keyword until match found
# Usage: snap_find_multi <role> "keyword1|keyword2|keyword3"
snap_find_multi() {
  local role="$1" keywords="$2"
  pinchtab snap 2>/dev/null | python3 -c "
import sys, json, unicodedata
def norm(s):
    return unicodedata.normalize('NFD', s.lower())
role = '$role'
keywords = '$keywords'.split('|')
nodes = json.load(sys.stdin)['nodes']
for kw in keywords:
    kw_n = norm(kw.strip())
    for n in nodes:
        if n['role'] == role and kw_n in norm(n.get('name','')):
            print(n['ref']); sys.exit(0)
" 2>/dev/null
}

snap_find_button_multi() { snap_find_multi "button" "$1"; }
snap_find_textbox_multi() { snap_find_multi "textbox" "$1"; }

# Poll-based wait with multi-keyword support
wait_for_element_multi() {
  local role="$1" keywords="$2" timeout="${3:-10}" elapsed=0
  while [[ $elapsed -lt $timeout ]]; do
    local ref
    ref=$(snap_find_multi "$role" "$keywords")
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
  timeout 5 pinchtab snap >/dev/null 2>&1
  return $?
}

safe_click() {
  local ref="$1"
  if ! pinchtab click "$ref" 2>&1 | grep -qi "not focusable"; then
    return 0
  fi
  echo "   [fallback] Element not focusable, using keyboard"
  pinchtab press ArrowDown >/dev/null 2>&1
  sleep 0.5
  pinchtab press Enter >/dev/null 2>&1
}

detect_user_profile() {
  pinchtab nav "https://www.facebook.com/me" >/dev/null 2>&1
  sleep 3
  local current_url
  current_url=$(pinchtab snap 2>/dev/null | python3 -c "
import sys, json
data = json.load(sys.stdin)
print(data.get('url',''))
" 2>/dev/null || true)
  echo "$current_url"
}

# ---- Instance lifecycle ----
CREATED_INSTANCE="false"

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
echo "[2/6] Opening profile page"

if [[ -n "$USER_ID" ]]; then
  pinchtab nav "https://www.facebook.com/profile.php?id=$USER_ID" >/dev/null 2>&1
else
  echo "   -> No --user-id provided, detecting from logged-in session..."
  PROFILE_URL=$(detect_user_profile)
  if [[ -z "$PROFILE_URL" ]]; then
    echo "ERROR: Cannot detect profile. Provide --user-id or ensure Facebook is logged in."
    exit 1
  fi
  echo "   -> Detected profile: $PROFILE_URL"
fi

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

BTN_CREATE=$(wait_for_element_multi "button" "$KW_CREATE_POST" 10)
if [[ -z "$BTN_CREATE" ]]; then
  echo "ERROR: Cannot find create post button in any supported language."
  debug_screenshot "03-error-no-button"
  exit 1
fi

pinchtab click "$BTN_CREATE" >/dev/null 2>&1
debug_screenshot "03-post-dialog"

# =============================================================
# STEP 4: Type post content
# =============================================================
echo "[4/6] Typing post content"

TXT_POST=$(wait_for_element_multi "textbox" "$KW_CREATE_POST" 5)
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

  BTN_TAG=$(snap_find_button_multi "$KW_TAG_OTHERS")
  if [[ -z "$BTN_TAG" ]]; then
    echo "   WARN: Tag button not found, skipping."
  else
    pinchtab click "$BTN_TAG" >/dev/null 2>&1

    TXT_SEARCH=$(wait_for_element_multi "textbox" "$KW_SEARCH" 5)
    if [[ -n "$TXT_SEARCH" ]]; then
      pinchtab click "$TXT_SEARCH" >/dev/null 2>&1
      sleep 0.5
      pinchtab keyboard type "$TAG_NAME" >/dev/null 2>&1

      sleep 2
      debug_screenshot "05-tag-search-results"

      if [[ -n "$TAG_ID" ]]; then
        TAG_REF=$(pinchtab snap 2>/dev/null | python3 -c "
import sys, json
for n in json.load(sys.stdin)['nodes']:
    if '$TAG_ID' in n.get('name','') or '$TAG_ID' in n.get('description',''):
        print(n['ref']); break
" 2>/dev/null || true)
        if [[ -n "$TAG_REF" ]]; then
          safe_click "$TAG_REF"
        else
          echo "   WARN: Tag ID $TAG_ID not found, selecting first friend"
          pinchtab press ArrowDown >/dev/null 2>&1
          sleep 0.3
          pinchtab press Enter >/dev/null 2>&1
        fi
      else
        # Prioritize friend results using multi-language friend label
        TAG_REF=$(pinchtab snap 2>/dev/null | python3 -c "
import sys, json, unicodedata
def norm(s): return unicodedata.normalize('NFD', s.lower())
friend_keywords = '$KW_FRIEND'.split('|')
nodes = json.load(sys.stdin)['nodes']
friend_ref = None
first_ref = None
for n in nodes:
    name = n.get('name','')
    desc = n.get('description','')
    tag = norm('$TAG_NAME')
    if tag in norm(name) or tag in norm(desc):
        if first_ref is None:
            first_ref = n['ref']
        desc_l = desc.lower()
        if any(fk.strip() in desc_l for fk in friend_keywords):
            friend_ref = n['ref']; break
print(friend_ref or first_ref or '')
" 2>/dev/null || true)

        if [[ -n "$TAG_REF" ]]; then
          safe_click "$TAG_REF"
        else
          pinchtab press ArrowDown >/dev/null 2>&1
          sleep 0.3
          pinchtab press Enter >/dev/null 2>&1
        fi
      fi

      sleep 2

      BTN_DONE=$(snap_find_button_multi "$KW_DONE")
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
  BTN_POST=$(wait_for_element_multi "button" "$KW_PUBLISH" 5)
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
