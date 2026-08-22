# Graph recipes — các ca ghi và tra cứu ít gặp hơn

Mọi lệnh ở đây đi qua `m365 request`, nên ba quy tắc của đường Graph luôn áp dụng: body heredoc ra file rồi truyền `@đường-dẫn`, thêm `--content-type "application/json"` khi có body, và thêm `--prefer 'outlook.timezone="SE Asia Standard Time"'` với mọi thứ có yếu tố thời gian.

Mục lục:

1. [Event lặp lại (recurrence)](#1-event-lặp-lại)
2. [Event cả ngày](#2-event-cả-ngày)
3. [Trả lời thư mời](#3-trả-lời-thư-mời)
4. [Phòng họp](#4-phòng-họp)
5. [Xem rảnh bận (getSchedule)](#5-xem-rảnh-bận)
6. [Tìm khung giờ chung (findMeetingTimes)](#6-tìm-khung-giờ-chung)

---

## 1. Event lặp lại

`recurrence` gồm hai phần bắt buộc đi cùng nhau: `pattern` trả lời "lặp thế nào" và `range` trả lời "lặp đến bao giờ". Thiếu một trong hai thì Graph từ chối.

```bash
SP="${TMPDIR:-/tmp}"
cat > "$SP/ev.json" <<'JSON'
{
  "subject": "Họp đầu tuần",
  "start": { "dateTime": "2026-09-07T09:00:00", "timeZone": "SE Asia Standard Time" },
  "end":   { "dateTime": "2026-09-07T09:30:00", "timeZone": "SE Asia Standard Time" },
  "recurrence": {
    "pattern": { "type": "weekly", "interval": 1, "daysOfWeek": ["monday"] },
    "range":   { "type": "endDate", "startDate": "2026-09-07", "endDate": "2026-12-28" }
  }
}
JSON

m365 request --url 'https://graph.microsoft.com/v1.0/me/events' --method post \
  --content-type "application/json" --body "@$SP/ev.json" \
  --prefer 'outlook.timezone="SE Asia Standard Time"' -o json --query '{id:id, type:type}'
```

Kết quả trả về `type: "seriesMaster"`, và `calendarView` sẽ bung ra từng buổi (đã xác minh: chuỗi 4 tuần cho ra 4 buổi `occurrence`).

Các dạng `pattern` hay dùng:

| Nhu cầu | `pattern` |
|---------|-----------|
| hàng ngày | `{"type":"daily","interval":1}` |
| các ngày trong tuần | `{"type":"weekly","interval":1,"daysOfWeek":["monday","wednesday","friday"]}` |
| hai tuần một lần | `{"type":"weekly","interval":2,"daysOfWeek":["tuesday"]}` |
| ngày 15 hàng tháng | `{"type":"absoluteMonthly","interval":1,"dayOfMonth":15}` |
| thứ Hai đầu mỗi tháng | `{"type":"relativeMonthly","interval":1,"daysOfWeek":["monday"],"index":"first"}` |

`index` nhận `first`, `second`, `third`, `fourth`, `last`.

Các dạng `range`:

| Nhu cầu | `range` |
|---------|---------|
| đến một ngày cụ thể | `{"type":"endDate","startDate":"2026-09-07","endDate":"2026-12-28"}` |
| lặp N lần | `{"type":"numbered","startDate":"2026-09-07","numberOfOccurrences":10}` |
| không có ngày kết thúc | `{"type":"noEnd","startDate":"2026-09-07"}` |

`startDate` trong `range` phải trùng ngày của `start.dateTime`. Lệch nhau thì Graph **không báo lỗi**: nó âm thầm dịch buổi đầu tiên sang ngày `startDate`. Đã đo thật: `start.dateTime` là 07/09 mà `startDate` ghi 14/09 thì event tạo ra bắt đầu từ 14/09, POST vẫn trả về 201 như bình thường. Cách tự bảo vệ là đọc lại `start.dateTime` trong response của POST và đối chiếu với ngày mình định đặt.

Sửa cả chuỗi thì PATCH vào ID của `seriesMaster`. Xem mục 6 của SKILL.md để phân biệt với việc sửa một buổi.

---

## 2. Event cả ngày

Ba điều kiện phải đủ cùng lúc, thiếu một là Graph báo lỗi: `isAllDay: true`, giờ của `start` và `end` đều là `00:00:00`, và `end` là ngày **hôm sau** ngày cuối cùng của event.

```bash
cat > "$SP/ev.json" <<'JSON'
{
  "subject": "Nghỉ phép",
  "isAllDay": true,
  "start": { "dateTime": "2026-09-12T00:00:00", "timeZone": "SE Asia Standard Time" },
  "end":   { "dateTime": "2026-09-13T00:00:00", "timeZone": "SE Asia Standard Time" }
}
JSON
```

Ví dụ trên là nghỉ **một** ngày 12/09. Nghỉ 12 đến 14/09 thì `end` là `2026-09-15T00:00:00`.

---

## 3. Trả lời thư mời

Ba hành động, cùng một hình dạng, khác nhau ở đoạn cuối URL: `accept`, `tentativelyAccept`, `decline`.

```bash
m365 request --url "https://graph.microsoft.com/v1.0/me/events/EVENT_ID/accept" --method post \
  --content-type "application/json" \
  --body '{"comment":"Tôi tham dự được","sendResponse":true}'
```

`sendResponse: true` là gửi thư trả lời cho người tổ chức, tức có phát ra ngoài. Người dùng nên biết điều đó trước khi chạy, và biết mình đang trả lời cuộc họp nào, nên in tiêu đề với người tổ chức ra cho họ xác nhận trước.

Đề xuất giờ khác cho người tổ chức thì thêm `proposedNewTime` vào body của `tentativelyAccept` hoặc `decline`:

```json
{
  "comment": "Giờ đó tôi có việc, đề xuất muộn hơn 1 tiếng",
  "sendResponse": true,
  "proposedNewTime": {
    "start": { "dateTime": "2026-09-05T15:00:00", "timeZone": "SE Asia Standard Time" },
    "end":   { "dateTime": "2026-09-05T16:00:00", "timeZone": "SE Asia Standard Time" }
  }
}
```

---

## 4. Phòng họp

Liệt kê phòng phải đi qua `beta`, vì `v1.0/places` và `m365 outlook room list` đều trả 403 với account thường (cần `Place.Read.All` mức admin). Endpoint `beta/me/findRooms` chỉ cần `Calendars.Read`, đây là đường Outlook app dùng:

```bash
# Danh sách phòng
m365 request --url 'https://graph.microsoft.com/beta/me/findRooms' -o json --query 'value[].{name:name, email:address}'

# Danh sách nhóm phòng (theo toà nhà, tầng, cơ sở)
m365 request --url 'https://graph.microsoft.com/beta/me/findRoomLists' -o json --query 'value[].{name:name, email:address}'

# Phòng thuộc một nhóm
m365 request --url "https://graph.microsoft.com/beta/me/findRooms(RoomList='miichisoft.room@contoso.com')" -o json --query 'value[].{name:name, email:address}'
```

Đây là endpoint `beta`, Microsoft không bảo đảm ổn định. Nếu nó trả 404 nghĩa là Microsoft đã bỏ, không phải skill hỏng: lúc đó nhờ Exchange admin cấp `Place.Read.All` rồi chuyển sang `v1.0/places/microsoft.graph.room` hoặc `m365 outlook room list`.

Đặt phòng là thêm phòng vào `attendees` với `type: "resource"`, kèm `location` cho dễ đọc:

```bash
cat > "$SP/ev.json" <<'JSON'
{
  "subject": "Họp kickoff",
  "start": { "dateTime": "2026-09-05T14:00:00", "timeZone": "SE Asia Standard Time" },
  "end":   { "dateTime": "2026-09-05T15:00:00", "timeZone": "SE Asia Standard Time" },
  "location": { "displayName": "Apolo", "locationEmailAddress": "apolo@contoso.com" },
  "attendees": [
    { "type": "required", "emailAddress": { "address": "nguoia@contoso.com", "name": "Người A" } },
    { "type": "resource", "emailAddress": { "address": "apolo@contoso.com", "name": "Apolo" } }
  ]
}
JSON
```

Hộp thư phòng tự động nhận hoặc từ chối theo chính sách của phòng, nên POST thành công **chưa có nghĩa là giữ được phòng**. Đọc lại `attendees[].status.response` của event sau khi tạo để biết phòng đã nhận chưa:

```bash
m365 request --url "https://graph.microsoft.com/v1.0/me/events/EVENT_ID?\$select=attendees" -o json \
  --query 'attendees[].{who:emailAddress.name, response:status.response}'
```

Muốn chắc trước khi đặt thì xem phòng rảnh chưa bằng `getSchedule` ở mục dưới, truyền email phòng như một người bình thường.

---

## 5. Xem rảnh bận

`getSchedule` trả về tình trạng rảnh bận của nhiều người hoặc phòng cùng lúc, dạng chuỗi ký tự, mỗi ký tự là một khoảng bằng `availabilityViewInterval` phút.

```bash
cat > "$SP/sched.json" <<'JSON'
{
  "schedules": ["nguoia@contoso.com", "apolo@contoso.com"],
  "startTime": { "dateTime": "2026-09-05T08:00:00", "timeZone": "SE Asia Standard Time" },
  "endTime":   { "dateTime": "2026-09-05T18:00:00", "timeZone": "SE Asia Standard Time" },
  "availabilityViewInterval": 30
}
JSON

m365 request --url 'https://graph.microsoft.com/v1.0/me/calendar/getSchedule' --method post \
  --content-type "application/json" --body "@$SP/sched.json" \
  --prefer 'outlook.timezone="SE Asia Standard Time"' \
  -o json --query 'value[].{who:scheduleId, view:availabilityView}'
```

Giải mã từng ký tự của `availabilityView`:

| Ký tự | Nghĩa |
|-------|-------|
| `0` | rảnh |
| `1` | chưa chắc (tentative) |
| `2` | bận |
| `3` | ra ngoài (out of office) |
| `4` | làm việc ở nơi khác |

Ví dụ đã đo thật với `availabilityViewInterval: 60` cho khoảng 08:00 đến 18:00: `0220000000` nghĩa là bận 09:00 đến 11:00, còn lại rảnh. Ký tự đầu ứng với khoảng bắt đầu từ `startTime`, nên muốn quy ra giờ thì đếm từ đó.

`getSchedule` chỉ cho biết rảnh hay bận, **không** trả về tiêu đề cuộc họp, kể cả lịch của chính mình. Cần biết bận vì việc gì thì đọc `calendarView`.

Giới hạn: tối đa 20 địa chỉ trong `schedules` mỗi lần gọi. Nhiều hơn thì chia lô.

---

## 6. Tìm khung giờ chung

`findMeetingTimes` để Graph tự đề xuất khung giờ, thay vì mình tự đọc `availabilityView` rồi suy luận.

```bash
cat > "$SP/find.json" <<'JSON'
{
  "attendees": [
    { "type": "required", "emailAddress": { "address": "nguoia@contoso.com" } },
    { "type": "required", "emailAddress": { "address": "nguoib@contoso.com" } }
  ],
  "timeConstraint": {
    "activityDomain": "work",
    "timeSlots": [{
      "start": { "dateTime": "2026-09-07T08:00:00", "timeZone": "SE Asia Standard Time" },
      "end":   { "dateTime": "2026-09-11T18:00:00", "timeZone": "SE Asia Standard Time" }
    }]
  },
  "meetingDuration": "PT1H",
  "maxCandidates": 5,
  "minimumAttendeePercentage": 100
}
JSON

m365 request --url 'https://graph.microsoft.com/v1.0/me/findMeetingTimes' --method post \
  --content-type "application/json" --body "@$SP/find.json" \
  --prefer 'outlook.timezone="SE Asia Standard Time"' \
  -o json --query 'meetingTimeSuggestions[].{confidence:confidence, start:meetingTimeSlot.start.dateTime, end:meetingTimeSlot.end.dateTime}'
```

Vài điểm cần biết:

- Đây chính là lệnh bộc lộ bẫy header `Prefer` rõ nhất: thiếu nó thì response trả UTC, đã đo được `01:00` thay vì `08:00`, tức lệch đúng 7 tiếng dù body ghi timezone đầy đủ.
- `meetingDuration` theo định dạng ISO 8601 duration: `PT30M` là 30 phút, `PT1H` là 1 tiếng, `PT1H30M` là 1 tiếng 30.
- `activityDomain`: `work` giới hạn trong giờ làm việc, `personal`, `unrestricted` cho phép mọi lúc.
- `confidence` là phần trăm khả năng mọi người rảnh. Hạ `minimumAttendeePercentage` xuống 70 nếu không tìm được khung giờ nào mà vẫn muốn có gợi ý.
- Nếu Graph không tìm được khung nào, `emptySuggestionsReason` cho biết vì sao, đáng đọc để giải thích cho người dùng thay vì chỉ báo "không có". Đã gặp: `OrganizerUnavailable` (chính mình bận hoặc khoảng giờ nằm ngoài giờ làm việc), `AttendeesUnavailable` (người được mời bận).
