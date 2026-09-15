#!/usr/bin/env bash
# List Teams transcripts as one flat JSON array, following Graph's paging correctly.
#
# Paging here is a silent failure in both directions and costs a whole script to get right:
#   - The first page LOOKS complete. Measured on a real tenant: page one returned 6 transcripts
#     and an @odata.nextLink, and following it produced 3 more. Reading only page one silently
#     loses a third of the history, with nothing to indicate anything is missing.
#   - `while nextLink` never terminates. Past the end, Graph keeps handing back a nextLink with
#     an EMPTY value array, forever. The loop has to stop on an empty page, not on a missing link.
#   - `$filter`, `startDateTime` and `endDateTime` are all accepted and all ignored on this
#     endpoint, so there is no server-side way to narrow the window. Filter with
#     meeting-resolver.py --from/--to after the fact.
#
# Usage:
#   list-transcripts.sh                     meetings you organized (the bulk endpoint)
#   list-transcripts.sh --meeting-id <b64>  one meeting you attended, all its occurrences
set -uo pipefail

MEETING_ID=""; MAX_PAGES=50
while [ $# -gt 0 ]; do
  case "$1" in
    --meeting-id) MEETING_ID="$2"; shift ;;
    --max-pages) MAX_PAGES="$2"; shift ;;
    -h|--help) sed -n '2,20p' "$0"; exit 0 ;;
    *) echo "unknown option: $1" >&2; exit 64 ;;
  esac; shift
done
command -v jq >/dev/null || { echo "jq is required" >&2; exit 1; }

OID=$(m365 request --url 'https://graph.microsoft.com/v1.0/me?$select=id' -o json --query 'id' 2>/dev/null | tr -d '"')
[ -n "$OID" ] || { echo "Not signed in, or Graph refused /me. Run scripts/preflight.sh" >&2; exit 1; }

if [ -n "$MEETING_ID" ]; then
  ENC=$(jq -rn --arg s "$MEETING_ID" '$s|@uri')
  URL="https://graph.microsoft.com/v1.0/users/$OID/onlineMeetings/$ENC/transcripts"
else
  URL="https://graph.microsoft.com/v1.0/users/$OID/onlineMeetings/getAllTranscripts(meetingOrganizerUserId='$OID')"
fi

TMP=$(mktemp -d); trap 'rm -rf "$TMP"' EXIT
: > "$TMP/all.ndjson"
PAGE=0
while [ -n "$URL" ] && [ "$PAGE" -lt "$MAX_PAGES" ]; do
  if ! m365 request --url "$URL" -o json > "$TMP/page.json" 2>"$TMP/err"; then
    # A 403 on the very first page is the tenant policy, not a paging problem. Say which.
    [ "$PAGE" = 0 ] && echo "Graph refused this call. Run scripts/preflight.sh --full to find out which wall this is." >&2
    cat "$TMP/err" >&2; exit 1
  fi
  N=$(jq '.value | length' "$TMP/page.json")
  [ "$N" = 0 ] && break            # the only reliable end of the sequence
  jq -c '.value[]' "$TMP/page.json" >> "$TMP/all.ndjson"
  URL=$(jq -r '."@odata.nextLink" // empty' "$TMP/page.json")
  PAGE=$((PAGE + 1))
done
[ "$PAGE" -ge "$MAX_PAGES" ] && echo "stopped at --max-pages $MAX_PAGES, there may be more" >&2

jq -s '.' "$TMP/all.ndjson"
