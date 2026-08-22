#!/usr/bin/env bash
# Quy đổi mốc thời gian tương đối thành khoảng ISO 8601 UTC cho Microsoft Graph / m365 CLI.
#
# Vì sao cần script, hai lý do đều là lỗi âm thầm (vẫn trả về event, chỉ là sai):
#   1. Graph từ chối thẳng chuỗi thiếu hậu tố Z ("2026-08-17T00:00:00" -> lỗi
#      "is not a valid ISO date-time"), còn tự cộng trừ tuần bằng suy luận thì dễ trượt.
#   2. Nửa đêm UTC không phải nửa đêm giờ VN. Mốc 00:00:00Z tương ứng 07:00 sáng GMT+7,
#      nên một cuộc họp 06:00 sáng thứ Hai sẽ rơi ra ngoài "tuần này", còn họp 06:00 sáng
#      thứ Hai tuần sau lại bị đếm vào. Script neo vào nửa đêm GIỜ VN rồi quy về UTC,
#      nên "week" in ra ...T17:00:00Z của ngày hôm trước, đó là đúng chứ không phải lỗi.
#
# Dùng: read START END < <(./date-range.sh week)
# Cú pháp date -v là của BSD/macOS. Trên Linux phải đổi sang date -d.

set -euo pipefail

usage() {
  cat >&2 <<'USAGE'
Dùng: date-range.sh <mốc>
  today | tomorrow | yesterday
  week | next-week | last-week      (tuần bắt đầu thứ Hai)
  month | next-month
  <YYYY-MM-DD> <YYYY-MM-DD>         (chỉ định tay: từ ngày, đến ngày không bao gồm)
In ra: "START END" dạng 2026-08-17T00:00:00Z 2026-08-24T00:00:00Z
USAGE
  exit 1
}

# Nửa đêm giờ VN (GMT+7) quy về UTC: trừ 7 tiếng, nên ngày lùi lại 1 và giờ thành 17:00Z.
TZ_OFFSET_HOURS=7
iso() {
  date -v-"${TZ_OFFSET_HOURS}"H -j -f '%Y-%m-%d %H:%M:%S' "$1 00:00:00" '+%Y-%m-%dT%H:%M:%SZ'
}
d()   { date -v"$1" -j -f '%Y-%m-%d' "$2" '+%Y-%m-%d'; }

# Thứ Hai của tuần chứa ngày truyền vào. date +%u: 1 = thứ Hai, 7 = Chủ Nhật.
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
