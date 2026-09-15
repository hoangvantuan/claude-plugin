#!/usr/bin/env bash
# preflight.sh has to tell three lookalike failures apart, and every one of them arrives as a
# 403. These run it against a fake m365 so each wall can be reproduced without a tenant.
set -uo pipefail
cd "$(dirname "$0")"
PREFLIGHT="../scripts/preflight.sh"
SANDBOX=$(mktemp -d); trap 'rm -rf "$SANDBOX"' EXIT
cp fixtures/fake-m365 "$SANDBOX/m365"; chmod +x "$SANDBOX/m365"
PASS=0; FAIL=0

# scenario, expected exit code, then every string the output must contain
check() {
  local scen="$1" want_code="$2"; shift 2
  local out code
  : > "$SANDBOX/state"
  out=$(FAKE_SCENARIO="$scen" FAKE_STATE="$SANDBOX/state" PREFLIGHT_PROBE_SLEEP=0 \
        PATH="$SANDBOX:$PATH" bash "$PREFLIGHT" --probes 2 2>&1); code=$?
  local problems=""
  [ "$code" = "$want_code" ] || problems="exit $code, wanted $want_code"
  for needle in "$@"; do
    case "$out" in *"$needle"*) ;; *) problems="$problems; missing '$needle'" ;; esac
  done
  if [ -z "$problems" ]; then PASS=$((PASS + 1)); printf 'ok    %s\n' "$scen"
  else FAIL=$((FAIL + 1)); printf 'FAIL  %s: %s\n%s\n' "$scen" "$problems" "$out"; fi
}

# A working tenant must not nag, and must not spend probes it does not need.
check ready 0 "Ready." "signed in as probe@example.com" "tenant policy allows"

# Optional scopes missing is a limitation, not a wall: transcripts still work.
check minimal 0 "Ready." "OnlineMeetingArtifact.Read.All missing" "Transcripts still work"

# Not signed in: name the browser flow, because a bare `m365 login` fails with invalid_client
# on app registrations that have the device code flow switched off.
check logged-out 1 "Not signed in" "m365 login --authType browser" "device code"

# The scope is the wall, so say plainly that signing in again is not the fix.
check no-transcript-scope 1 "OnlineMeetingTranscript.Read.All missing" \
  "NOT fixed by signing in again" "Grant admin consent" "send this to IT"
check no-calendar-scope 1 "Calendars.Read missing" "no meeting name"

# Policy off is the tenant default. It is not an app permission, so consent cannot fix it.
check policy-off 1 "tenant policy blocks" "EnableGraphTranscriptAccess" "not an app permission"

# One 403 during propagation must not be read as a closed door: the retry is worth it.
check propagating 2 "still propagating" "Wait a few minutes"

# Half-on tenant: transcripts arrive, speaker names do not. Different switch, different ask.
check speaker-attribution 2 "speaker names are withheld" "EnableAttributedTranscripts"

printf '\n%s passed, %s failed\n' "$PASS" "$FAIL"
[ "$FAIL" = 0 ]
