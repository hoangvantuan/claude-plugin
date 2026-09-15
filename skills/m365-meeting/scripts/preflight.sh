#!/usr/bin/env bash
# Diagnose whether this machine can actually read Teams transcripts, and if not, say which
# of the three walls you hit and exactly what to ask for.
#
# The walls look alike from the outside (every one of them surfaces as a 403 or an empty
# list) but need completely different fixes, and guessing wrong costs an hour:
#   1. Not signed in, or signed in without the transcript scope.
#   2. The scope is declared on the app registration but nobody consented to it. Signing in
#      again does NOT fix this and shows no consent prompt, so it reads like a bug.
#   3. The tenant policy that exposes transcripts to Graph is off. It is off by DEFAULT, and
#      when an admin turns it on it propagates gradually, so a single 403 proves nothing.
#
# Usage: preflight.sh [--full] [--probes N]
#   default   one policy probe, escalates to the repeat loop only if that probe fails
#   --full    always run the repeat loop, use after an admin says they just flipped the switch
set -uo pipefail

PROBES=5; FULL=0
# Spacing between policy probes. Overridable so the test suite does not have to wait out
# a real propagation window; leave it alone in normal use.
PROBE_SLEEP="${PREFLIGHT_PROBE_SLEEP:-6}"
while [ $# -gt 0 ]; do
  case "$1" in
    --full) FULL=1 ;;
    --probes) PROBES="$2"; shift ;;
    -h|--help) sed -n '2,14p' "$0"; exit 0 ;;
    *) echo "unknown option: $1" >&2; exit 64 ;;
  esac; shift
done

ok()   { printf 'ok    %s\n' "$1"; }
warn() { printf 'warn  %s\n' "$1"; }
bad()  { printf 'BLOCK %s\n' "$1"; }

# --- 1. CLI present and signed in -------------------------------------------------------
command -v m365 >/dev/null || {
  bad "m365 CLI not installed. Install it with: npm i -g @pnp/cli-microsoft365"; exit 1; }

STATUS=$(m365 status -o json 2>&1) || true
case "$STATUS" in
  *connectedAs*) : ;;
  *) bad "Not signed in. Run: m365 login --authType browser"
     echo "      Use --authType browser, not a bare 'm365 login'. The bare form defaults to the"
     echo "      device code flow, which a private app registration often has disabled and which"
     echo "      fails with a bare 'invalid_client' that says nothing about the real cause."
     exit 1 ;;
esac
USER_UPN=$(printf '%s' "$STATUS" | sed -n 's/.*"connectedAs": *"\([^"]*\)".*/\1/p')
APP_ID=$(printf '%s' "$STATUS" | sed -n 's/.*"appId": *"\([^"]*\)".*/\1/p')
ok "signed in as $USER_UPN (app $APP_ID)"

OID=$(m365 request --url 'https://graph.microsoft.com/v1.0/me?$select=id' -o json --query 'id' 2>/dev/null | tr -d '"')
[ -n "$OID" ] || { bad "Signed in but Graph refused /me. The session is stale: m365 logout && m365 login --authType browser"; exit 1; }

# --- 2. Scopes actually granted in the token --------------------------------------------
# The token lists what was CONSENTED, which is the only thing that counts at request time.
# What the app registration declares is a separate list and the two drift apart constantly.
SCOPES=""
if command -v python3 >/dev/null; then
  SCOPES=$(m365 util accesstoken get --resource https://graph.microsoft.com -o text 2>/dev/null | python3 -c '
import sys, base64, json
try:
    p = sys.stdin.read().strip().split(".")[1]
    print(json.loads(base64.urlsafe_b64decode(p + "=" * (-len(p) % 4))).get("scp", ""))
except Exception:
    pass' 2>/dev/null)
fi

has() { case " $SCOPES " in *" $1 "*) return 0 ;; *) return 1 ;; esac; }
MISSING_REQUIRED=0
if [ -z "$SCOPES" ]; then
  warn "could not decode the token, skipping the scope check (python3 missing?)"
else
  has OnlineMeetingTranscript.Read.All \
    && ok "OnlineMeetingTranscript.Read.All granted (transcripts)" \
    || { bad "OnlineMeetingTranscript.Read.All missing. Without it no transcript can be read."; MISSING_REQUIRED=1; }
  has Calendars.Read || has Calendars.ReadWrite \
    && ok "Calendars.Read granted (meeting names come from the calendar)" \
    || { bad "Calendars.Read missing. Transcripts would arrive with no meeting name attached."; MISSING_REQUIRED=1; }
  has OnlineMeetingArtifact.Read.All && ok "OnlineMeetingArtifact.Read.All granted (attendance)" \
    || warn "OnlineMeetingArtifact.Read.All missing: no attendance list in the header. Transcripts still work."
  has OnlineMeetingRecording.Read.All && ok "OnlineMeetingRecording.Read.All granted (recordings)" \
    || warn "OnlineMeetingRecording.Read.All missing: cannot list recordings. Transcripts still work."
  has OnlineMeetings.Read && ok "OnlineMeetings.Read granted (lookup by pasted join link)" \
    || warn "OnlineMeetings.Read missing: a pasted Teams link cannot be looked up directly. Finding the meeting by name still works."
fi

if [ "$MISSING_REQUIRED" = 1 ]; then
  echo
  echo "A missing scope is NOT fixed by signing in again. Entra only prompts for consent the"
  echo "first time a permission is requested; once an admin has consented to the app, newly"
  echo "added permissions are granted silently or not at all, with no prompt either way."
  # Refines the message when the signed-in user happens to be able to read the app. Most
  # users cannot (403), and that is fine: the ask below covers both possible causes.
  if m365 request --url "https://graph.microsoft.com/v1.0/applications?\$filter=appId eq '$APP_ID'&\$select=id" -o json >/dev/null 2>&1; then
    echo "You can read the app registration, so check its API permissions directly before asking IT."
  fi
  echo
  echo "--- send this to IT ---"
  echo "On Entra app registration $APP_ID, please add these delegated Microsoft Graph"
  echo "permissions and click Grant admin consent for the tenant:"
  echo "  OnlineMeetingTranscript.Read.All, OnlineMeetingArtifact.Read.All, OnlineMeetingRecording.Read.All"
  echo "They are admin-consent-only, so adding them without granting consent changes nothing."
  echo "-----------------------"
  exit 1
fi

# --- 3. Tenant transcript policy --------------------------------------------------------
URL="https://graph.microsoft.com/v1.0/users/$OID/onlineMeetings/getAllTranscripts(meetingOrganizerUserId='$OID')?\$top=1"
probe() { m365 request --url "$URL" -o json >/dev/null 2>&1 && echo 200 || echo 403; }

FIRST=$(probe)
if [ "$FIRST" = 200 ] && [ "$FULL" = 0 ]; then
  ok "tenant policy allows Graph transcript access"
  echo; echo "Ready."; exit 0
fi

# A single 403 is not a verdict: while a freshly enabled policy propagates, the same call
# alternates 200 and 403 across Graph front ends (measured: roughly 4 minutes to settle).
GOOD=0; BAD_N=0; DETAIL=""
[ "$FIRST" = 200 ] && GOOD=1 || BAD_N=1
echo "probing the tenant policy ${PROBES}x, a lone 403 can be propagation rather than a closed door"
for _ in $(seq 2 "$PROBES"); do
  sleep "$PROBE_SLEEP"
  if [ "$(probe)" = 200 ]; then GOOD=$((GOOD + 1)); else
    BAD_N=$((BAD_N + 1))
    [ -n "$DETAIL" ] || DETAIL=$(m365 request --url "$URL" -o json --debug 2>&1 | grep -o '"message": *"[^"]*"' | head -1)
  fi
done

case "$DETAIL" in *SpeakerAttributionNotAllowed*|*peaker*ttribution*)
  warn "policy half-on: transcripts are exposed but speaker names are withheld ($GOOD/$PROBES ok)"
  echo "--- send this to IT ---"
  echo "Please also set -EnableAttributedTranscripts \$true in the Teams meeting policy."
  echo "  Set-CsTeamsMeetingPolicy -Identity Global -EnableAttributedTranscripts \$true"
  echo "Without it Graph returns transcripts with no speaker names, which makes them"
  echo "unusable for minutes and for who-said-what analysis."
  echo "-----------------------"
  exit 2 ;;
esac

if [ "$GOOD" = "$PROBES" ]; then
  ok "tenant policy allows Graph transcript access ($GOOD/$PROBES)"
  echo; echo "Ready."; exit 0
elif [ "$GOOD" -gt 0 ]; then
  warn "policy is still propagating ($GOOD ok, $BAD_N forbidden). Wait a few minutes and rerun."
  echo "      Transcripts fetched right now may fail intermittently. Retrying is worth it."
  exit 2
fi

bad "tenant policy blocks Graph transcript access ($BAD_N/$PROBES forbidden)"
[ -n "$DETAIL" ] && echo "      Graph said: $DETAIL"
echo
echo "This is the default state of a tenant. It is a Teams policy, not an app permission,"
echo "so no amount of re-consenting or signing in again will change it."
echo "--- send this to IT ---"
echo "Please enable Graph access to Teams meeting transcripts for our tenant:"
echo "  Set-CsTeamsMeetingPolicy -Identity Global -EnableGraphTranscriptAccess \$true \\"
echo "                           -EnableAttributedTranscripts \$true"
echo "Both switches are needed: the first exposes transcripts to Microsoft Graph, the second"
echo "keeps speaker names attached. Changes take a few minutes to propagate."
echo "Reference: https://learn.microsoft.com/microsoftteams/teams-powershell-overview"
echo "-----------------------"
exit 1
