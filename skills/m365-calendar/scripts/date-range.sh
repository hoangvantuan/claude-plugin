#!/usr/bin/env bash
# Turn a relative time anchor into an ISO 8601 UTC range for Microsoft Graph / the m365 CLI.
#
# Why a script is needed; both reasons are silent failures (events still come back, just wrong):
#   1. Graph rejects a string missing the Z suffix outright ("2026-08-17T00:00:00" -> error
#      "is not a valid ISO date-time"), and adding or subtracting weeks by reasoning slips easily.
#   2. UTC midnight is not Vietnam midnight. The 00:00:00Z mark is 07:00 in GMT+7, so a 06:00
#      Monday meeting falls outside "this week" while next Monday's 06:00 meeting gets counted in.
#      The script anchors midnight in VIETNAM time and converts to UTC, so "week" prints
#      ...T17:00:00Z of the previous day, which is correct, not a bug.
#
# Usage: read START END < <(./date-range.sh week)
# The date -v syntax is BSD/macOS. On Linux switch to date -d.

set -euo pipefail

usage() {
  cat >&2 <<'USAGE'
Usage: date-range.sh <anchor>
  today | tomorrow | yesterday
  week | next-week | last-week      (weeks start on Monday)
  month | next-month
  <YYYY-MM-DD> <YYYY-MM-DD>         (explicit: from date, to date exclusive)
Prints: "START END" as 2026-08-17T00:00:00Z 2026-08-24T00:00:00Z
USAGE
  exit 1
}

# Vietnam midnight (GMT+7) in UTC: subtract 7 hours, so the date rolls back one day and the time becomes 17:00Z.
TZ_OFFSET_HOURS=7
iso() {
  date -v-"${TZ_OFFSET_HOURS}"H -j -f '%Y-%m-%d %H:%M:%S' "$1 00:00:00" '+%Y-%m-%dT%H:%M:%SZ'
}
d()   { date -v"$1" -j -f '%Y-%m-%d' "$2" '+%Y-%m-%d'; }

# The Monday of the week containing the given date. date +%u: 1 = Monday, 7 = Sunday.
monday_of() {
  local ref="$1" dow
  dow=$(date -j -f '%Y-%m-%d' "$ref" '+%u')
  d "-$((dow - 1))d" "$ref"
}

TODAY=$(date '+%Y-%m-%d')

case "${1:-}" in
  today)      START=$TODAY;                       END=$(d +1d "$TODAY") ;;
  tomorrow)   START=$(d +1d "$TODAY");            END=$(d +2d "$TODAY") ;;
  yesterday)  START=$(d -1d "$TODAY");            END=$TODAY ;;
  week)       START=$(monday_of "$TODAY");        END=$(d +7d "$START") ;;
  next-week)  START=$(d +7d "$(monday_of "$TODAY")"); END=$(d +7d "$START") ;;
  last-week)  START=$(d -7d "$(monday_of "$TODAY")"); END=$(d +7d "$START") ;;
  month)      START=$(date '+%Y-%m-01');          END=$(d +1m "$START") ;;
  next-month) START=$(d +1m "$(date '+%Y-%m-01')"); END=$(d +1m "$START") ;;
  ????-??-??)
    [ $# -eq 2 ] || usage
    date -j -f '%Y-%m-%d' "$1" '+%Y-%m-%d' >/dev/null
    date -j -f '%Y-%m-%d' "$2" '+%Y-%m-%d' >/dev/null
    START=$1; END=$2 ;;
  *) usage ;;
esac

printf '%s %s\n' "$(iso "$START")" "$(iso "$END")"
