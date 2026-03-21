#!/bin/bash
# =============================================================
# Facebook Personal Wall Post + Tag User via PinchTab
# =============================================================
# Usage:
#   ./fb-post.sh --profile default \
#                --user-id 100003782705460 \
#                --content "Noi dung bai viet" \
#                --tag "Hoang Van Tuan" \
#                --publish false
# =============================================================

set -euo pipefail

# ---- Default config ----
PROFILE="default"
USER_ID=""
CONTENT=""
TAG_NAME=""
PUBLISH="false"
MODE="headed"

# ---- Parse arguments ----
while [[ $# -gt 0 ]]; do
  case $1 in
    --profile)  PROFILE="$2";  shift 2 ;;
    --user-id)  USER_ID="$2";  shift 2 ;;
    --content)  CONTENT="$2";  shift 2 ;;
    --tag)      TAG_NAME="$2"; shift 2 ;;
    --publish)  PUBLISH="$2";  shift 2 ;;
    --mode)     MODE="$2";     shift 2 ;;
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

snap_find() {
  # Find element by role + keyword in name
  # Usage: snap_find <role> <keyword>
  pinchtab snap 2>/dev/null | python3 -c "
import sys, json
role, kw = '$1', '$2'.lower()
for n in json.load(sys.stdin)['nodes']:
    if n['role'] == role and kw in n.get('name','').lower():
        print(n['ref']); break
" 2>/dev/null
}

snap_find_button() {
  snap_find "button" "$1"
}

snap_find_textbox() {
  snap_find "textbox" "$1"
}

# =============================================================
# STEP 1: Start browser instance with existing profile
# =============================================================
echo "[1/6] Starting browser with profile: $PROFILE"

# Check for running instance with this profile
EXISTING=$(curl -s "$BASE/instances" -H "$AUTH" 2>/dev/null | python3 -c "
import sys, json
for i in json.load(sys.stdin):
    if i.get('profileName') == '$PROFILE' and i.get('status') == 'running':
        print(i['id']); break
" 2>/dev/null || true)

if [[ -n "$EXISTING" ]]; then
  INST="$EXISTING"
  echo "   -> Reusing running instance: $INST"
else
  # Use CLI (not API) to preserve profile correctly
  INST=$(pinchtab instance start --profile "$PROFILE" --mode "$MODE" 2>/dev/null \
    | python3 -c "import sys,json; print(json.load(sys.stdin)['id'])")
  echo "   -> Created instance: $INST"
  sleep 3
fi

# =============================================================
# STEP 2: Navigate to personal wall
# =============================================================
echo "[2/6] Opening profile page: $USER_ID"

# Use /profile.php?id=... URL (not group URL)
pinchtab nav "https://www.facebook.com/profile.php?id=$USER_ID" >/dev/null 2>&1
sleep 3

# Confirm we're on the right page
TITLE=$(pinchtab snap 2>/dev/null | python3 -c "
import sys, json
print(json.load(sys.stdin)['nodes'][0].get('name',''))
" 2>/dev/null)
echo "   -> Page: $TITLE"

# =============================================================
# STEP 3: Open "Create post" dialog
# =============================================================
echo "[3/6] Opening create post dialog"

BTN_CREATE=$(snap_find_button "nghi gi")
if [[ -z "$BTN_CREATE" ]]; then
  echo "ERROR: Cannot find 'Ban dang nghi gi?' button. Check the page."
  exit 1
fi

pinchtab click "$BTN_CREATE" >/dev/null 2>&1
sleep 2

# =============================================================
# STEP 4: Type post content
# =============================================================
echo "[4/6] Typing post content"

# Find textbox in dialog
TXT_POST=$(snap_find_textbox "nghi gi")
if [[ -z "$TXT_POST" ]]; then
  echo "ERROR: Cannot find post textbox."
  exit 1
fi

pinchtab click "$TXT_POST" >/dev/null 2>&1
sleep 0.5

# Use inserttext to preserve line breaks
pinchtab keyboard inserttext "$CONTENT" >/dev/null 2>&1
sleep 1
echo "   -> Content entered (${#CONTENT} chars)"

# =============================================================
# STEP 5: Tag user (optional)
# =============================================================
if [[ -n "$TAG_NAME" ]]; then
  echo "[5/6] Tagging: $TAG_NAME"

  # Click "Tag others" button
  BTN_TAG=$(snap_find_button "gan the nguoi khac")
  if [[ -z "$BTN_TAG" ]]; then
    echo "   WARN: Tag button not found, skipping."
  else
    pinchtab click "$BTN_TAG" >/dev/null 2>&1
    sleep 2

    # Find friend search input
    TXT_SEARCH=$(snap_find_textbox "tim kiem")
    if [[ -n "$TXT_SEARCH" ]]; then
      # Click + type name (use type to trigger autocomplete)
      pinchtab click "$TXT_SEARCH" >/dev/null 2>&1
      sleep 1
      pinchtab keyboard type "$TAG_NAME" >/dev/null 2>&1
      sleep 2

      # Select first result via keyboard
      # (don't click because option element is not focusable)
      pinchtab press ArrowDown >/dev/null 2>&1
      sleep 0.5
      pinchtab press Enter >/dev/null 2>&1
      sleep 2

      # Click "Done"
      BTN_DONE=$(snap_find_button "xong")
      if [[ -n "$BTN_DONE" ]]; then
        pinchtab click "$BTN_DONE" >/dev/null 2>&1
        sleep 2
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
  BTN_POST=$(snap_find_button "dang")
  if [[ -n "$BTN_POST" ]]; then
    pinchtab click "$BTN_POST" >/dev/null 2>&1
    sleep 3
    echo "   -> Post published!"
  else
    echo "   -> ERROR: Publish button not found"
  fi
else
  echo "[6/6] Post ready, NOT PUBLISHED."
  echo "   -> Open browser and click 'Post' when ready."
fi

echo ""
echo "Done!"
