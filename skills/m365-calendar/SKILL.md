---
name: m365-calendar
description: "Outlook calendar via the m365 CLI and Microsoft Graph: agenda, events, attendees, meeting rooms, free/busy, recurring series. Use for any question about the user's calendar, schedule, or availability."
allowed-tools:
  - Bash
  - Read
---

# m365-calendar — Outlook Calendar Management

## Prerequisites

```bash
which m365 || echo "Chưa cài m365 CLI. Chạy: npm i -g @pnp/cli-microsoft365"
m365 status || echo "Chưa đăng nhập. Chạy: m365 login"
```

Auth chi tiết: `../m365-shared/references/authentication.md`.

## Operating Principles

Lệnh native `m365 outlook` không có `event add`/`event set`, nên skill này đi **hai đường song song**, và biết đang ở đường nào là điều kiện để không sai cú pháp:

| Đường | Dùng cho | Đặc thù cú pháp |
|-------|----------|-----------------|
| Native `m365 outlook ...` | CRUD calendar, đọc event lẻ, huỷ/xoá event | bắt buộc `--userName`, thời gian phải có `Z` |
| Graph qua `m365 request` | đọc theo khoảng, tạo/sửa event, rảnh/bận, tìm giờ, phòng họp | body heredoc ra file, bắt buộc header `Prefer` |

Hai dòng lệnh mở đầu cho gần như mọi việc:

```bash
# Người dùng hiện tại (mọi lệnh native cần, không có mặc định "me")
USER=$(m365 status -o json --query 'connectedAs' | tr -d '"')

# Script tính khoảng thời gian, nằm cạnh SKILL.md này. Dùng đường dẫn tuyệt đối tới
# thư mục chứa file SKILL.md vừa đọc, vì thư mục làm việc hiện tại thường không phải
# thư mục skill (khi cài qua plugin thì skill nằm trong ~/.claude, còn cwd là project).
DR="<đường-dẫn-thư-mục-skill>/scripts/date-range.sh"

# Khoảng thời gian, đã neo đúng nửa đêm giờ VN
read START END < <("$DR" week)
```

Xem lịch người khác cần lịch đó được chia sẻ cho mình hoặc cần quyền admin. Gặp 403 thì báo thẳng giới hạn quyền, đừng thử vòng vo các lệnh khác.

---

## Bẫy đã xác minh

Tám điều dưới đây đo được bằng cách chạy thật trên tenant, không tra tài liệu ra được. Bảy trong tám là **lỗi âm thầm**: lệnh vẫn chạy, vẫn trả về event, chỉ là kết quả sai, nên không có cách nào phát hiện ngoài việc biết trước.

| Bẫy | Biểu hiện | Cách đúng |
|-----|-----------|-----------|
| `event list` bỏ mất họp định kỳ | cùng một tuần: `/me/events` trả **12**, `/me/calendarView` trả **46**. `/me/events` chỉ trả `seriesMaster`, không bung từng buổi | mọi câu hỏi theo khoảng thời gian dùng `calendarView`, xem mục 1 |
| Thiếu header `Prefer` | Graph trả UTC, lệch đúng 7 tiếng. `findMeetingTimes` trả `01:00` thay vì `08:00` dù body đã ghi timezone | mọi lệnh Graph có yếu tố thời gian đều thêm `--prefer 'outlook.timezone="SE Asia Standard Time"'`. Body ghi timezone là **không đủ** |
| Nửa đêm UTC không phải nửa đêm giờ VN | `00:00:00Z` là 07:00 sáng GMT+7, nên họp 06:00 thứ Hai rơi ra ngoài "tuần này" | luôn lấy khoảng từ `scripts/date-range.sh`, nó neo nửa đêm GMT+7 nên in ra `...T17:00:00Z` của ngày hôm trước, đó là đúng |
| Thời gian thiếu `Z` | `--startDateTime 2026-08-17T00:00:00` bị từ chối thẳng: "is not a valid ISO date-time" | luôn có `Z` hoặc offset |
| `--userName` không có mặc định "me" | `Error: Specify either userId or userName, but not both` dù chỉ thiếu, không phải truyền cả hai. Thông báo lỗi này gây hiểu lầm | `calendar *` và `event list`/`event get` **bắt buộc**; `event cancel`/`event remove` thì không cần với delegated auth |
| ID của `calendarView` là ID một buổi | `calendarView` trả `type: "occurrence"` kèm `seriesMasterId`. PATCH vào ID đó chỉ đổi buổi đó (nó thành `exception`), không đổi cả chuỗi | sửa cả chuỗi thì PATCH vào `seriesMasterId`. Xem mục 6 |
| `recurrence` dịch ngày không báo lỗi | `range.startDate` lệch với `start.dateTime` thì Graph âm thầm dời buổi đầu sang `startDate`, POST vẫn trả về thành công | hai ngày đó phải trùng nhau, và đọc lại `start.dateTime` trong response để đối chiếu |
| Danh sách phòng họp | `outlook room list` và `v1.0/places` trả **403** (cần `Place.Read.All` mức admin), nhưng phòng vẫn tra được | dùng `beta/me/findRooms`, đây là đường Outlook app dùng, chỉ cần `Calendars.Read` |

Không khả dụng với app mặc định của m365 CLI: giờ làm việc và trả lời tự động (`mailboxSettings` trả 403, thiếu `MailboxSettings.Read`).

---

## 1. Đọc lịch theo khoảng thời gian

Đây là việc hay làm nhất, và `calendarView` là đường duy nhất đúng vì nó bung từng buổi của chuỗi định kỳ.

```bash
read START END < <("$DR" week)

m365 request \
  --url "https://graph.microsoft.com/v1.0/me/calendarView?startDateTime=$START&endDateTime=$END&\$select=subject,start,end,location,isAllDay,type,seriesMasterId&\$orderby=start/dateTime&\$top=200" \
  --prefer 'outlook.timezone="SE Asia Standard Time"' \
  -o json --query 'value[].{start:start.dateTime, end:end.dateTime, subject:subject, where:location.displayName}'
```

Điểm cần biết:

- `$top=200` vì mặc định Graph phân trang 10 mục, thiếu nó là mất event mà không có dấu hiệu gì.
- `calendarView` đọc **một** calendar mỗi lần, mặc định là calendar chính. Muốn gộp nhiều calendar thì lặp qua từng `id` với `me/calendars/{id}/calendarView`.
- `$` trong URL phải escape thành `\$` khi ở trong nháy kép của bash.
- Khoảng thời gian đã tính ra được nên **in cho người dùng thấy** trong câu trả lời (ví dụ "tuần 17 đến 23/08"), để họ phát hiện ngay nếu mình hiểu sai ý "tuần này".

```bash
# Gộp mọi calendar. Dùng -o text để mỗi dòng là một id, khỏi phải cắt chuỗi JSON
m365 outlook calendar list --userName "$USER" -o text --query '[].id' | while read -r CAL; do
  m365 request --url "https://graph.microsoft.com/v1.0/me/calendars/$CAL/calendarView?startDateTime=$START&endDateTime=$END&\$select=subject,start&\$top=200" \
    --prefer 'outlook.timezone="SE Asia Standard Time"' -o json --query 'value[].{start:start.dateTime, subject:subject}'
done
```

---

## 2. Calendar (lệnh native, đủ CRUD)

```bash
# Liệt kê
m365 outlook calendar list --userName "$USER" -o json --query '[].{id:id, name:name, canEdit:canEdit, isDefault:isDefaultCalendar}'

# Lấy một calendar theo tên
m365 outlook calendar get --userName "$USER" --name "Calendar" -o json

# Tạo
m365 outlook calendar add --userName "$USER" --name "Dự án Alpha" --color lightGreen -o json --query 'id'

# Đổi tên hoặc màu (bắt buộc --id, không nhận --name để định danh)
m365 outlook calendar set --userName "$USER" --id "CAL_ID" --name "Tên mới" --color lightBlue

# Xoá (xoá cả event bên trong, hỏi người dùng trước)
m365 outlook calendar remove --userName "$USER" --name "Dự án Alpha" --force
```

`--color`: `auto`, `lightBlue`, `lightGreen`, `lightOrange`, `lightGray`, `lightYellow`, `lightTeal`, `lightPink`, `lightBrown`, `lightRed`, `maxColor`.

---

## 3. Đọc event lẻ và đọc định nghĩa chuỗi

```bash
# Một event theo ID
m365 outlook event get --userName "$USER" --id "EVENT_ID" --timeZone "SE Asia Standard Time" -o json \
  --query '{subject:subject, start:start.dateTime, organizer:organizer.emailAddress.name, attendees:attendees[].emailAddress.address}'

# Định nghĩa chuỗi định kỳ (đây là chỗ event list có ích: nó trả seriesMaster, không bung từng buổi)
m365 outlook event list --userName "$USER" --calendarName "Calendar" \
  --startDateTime "$START" --endDateTime "$END" --timeZone "SE Asia Standard Time" \
  -o json --query "[?type=='seriesMaster'].{id:id, subject:subject, pattern:recurrence.pattern.type}"
```

`--timeZone` là bắt buộc về mặt thực dụng: thiếu nó thì trả UTC, lệch 7 tiếng.

---

## 4. Tạo và sửa event (Graph)

Body luôn heredoc ra file rồi truyền `@đường-dẫn`. Lý do: tiêu đề tiếng Việt có dấu, dấu nháy đơn (`"Họp anh Tuấn's team"`), hay body nhiều dòng nhồi vào `--body '{...}'` một dòng là vỡ quote. Delimiter đặt trong nháy đơn (`<<'JSON'`) để bash không nội suy gì.

### 4.1 Event đơn

```bash
SP="${TMPDIR:-/tmp}"
cat > "$SP/ev.json" <<'JSON'
{
  "subject": "Rà soát kế hoạch Q4",
  "body": { "contentType": "text", "content": "Nội dung ghi chú" },
  "start": { "dateTime": "2026-09-05T10:00:00", "timeZone": "SE Asia Standard Time" },
  "end":   { "dateTime": "2026-09-05T11:00:00", "timeZone": "SE Asia Standard Time" },
  "location": { "displayName": "Phòng Apolo" }
}
JSON

m365 request --url 'https://graph.microsoft.com/v1.0/me/events' --method post \
  --content-type "application/json" --body "@$SP/ev.json" \
  --prefer 'outlook.timezone="SE Asia Standard Time"' \
  -o json --query '{id:id, subject:subject, start:start.dateTime}'
```

Tạo vào calendar khác thì đổi URL thành `me/calendars/{calendarId}/events`.

**Chống tạo trùng**: nếu lệnh POST timeout hoặc không rõ đã thành công chưa, đừng gửi lại ngay. Đọc `calendarView` của khoảng đó trước, vì POST lại là tạo thêm một event nữa chứ không phải ghi đè. Chú ý một biến thể dễ mắc: lỗi hiện ra ở **dòng lệnh sau** POST (lỗi shell, biến rỗng, quote vỡ) không có nghĩa là POST thất bại. Event đã nằm trên lịch rồi, kiểm tra trước khi chạy lại.

### 4.2 Event có người tham dự

```bash
cat > "$SP/ev.json" <<'JSON'
{
  "subject": "Họp kickoff dự án",
  "start": { "dateTime": "2026-09-05T14:00:00", "timeZone": "SE Asia Standard Time" },
  "end":   { "dateTime": "2026-09-05T15:00:00", "timeZone": "SE Asia Standard Time" },
  "attendees": [
    { "type": "required", "emailAddress": { "address": "nguoia@contoso.com", "name": "Người A" } },
    { "type": "optional", "emailAddress": { "address": "nguoib@contoso.com", "name": "Người B" } }
  ]
}
JSON
```

Có `attendees` là Graph **gửi thư mời thật** ngay khi POST thành công, không có bước nháp. Xác nhận danh sách người nhận với người dùng trước khi chạy.

### 4.3 Họp online Teams

Thêm hai trường vào body của 4.1 hoặc 4.2:

```json
"isOnlineMeeting": true,
"onlineMeetingProvider": "teamsForBusiness"
```

Graph tự sinh link, đọc lại ở `onlineMeeting.joinUrl` (đã xác minh có link sau khi tạo).

### 4.4 Sửa event

PATCH chỉ cần những trường muốn đổi, các trường khác giữ nguyên:

```bash
m365 request --url "https://graph.microsoft.com/v1.0/me/events/EVENT_ID" --method patch \
  --content-type "application/json" \
  --body '{"subject":"Tiêu đề mới"}' \
  --prefer 'outlook.timezone="SE Asia Standard Time"' -o json --query 'subject'
```

Đổi giờ thì phải gửi **cả** `start` và `end`, gửi một mình `start` sẽ cho ra event có giờ kết thúc trước giờ bắt đầu.

---

## 5. Huỷ và xoá

Hai lệnh này khác nhau ở chỗ có phát thư ra ngoài hay không, chọn sai là gửi thư huỷ ngoài ý muốn cho khách mời:

| Lệnh | Làm gì | Khi nào |
|------|--------|---------|
| `event cancel` | huỷ cuộc họp và **gửi thư huỷ cho toàn bộ người tham dự** | mình là người tổ chức, cần thông báo |
| `event remove` | chỉ bỏ event khỏi lịch của mình, không thông báo ai | event mình tự tạo không có khách, hoặc dọn lịch riêng |

Cả hai không hoàn tác được, và `cancel` còn ra khỏi tổ chức, nên trước khi chạy hãy in đầy đủ để người dùng nhận diện đúng event rồi chờ họ xác nhận, mỗi lần một event, không xoá theo lô:

```bash
m365 outlook event get --userName "$USER" --id "EVENT_ID" --timeZone "SE Asia Standard Time" -o json \
  --query '{subject:subject, start:start.dateTime, organizer:organizer.emailAddress.name, soNguoiThamDu:length(attendees)}'
```

Sau khi người dùng đồng ý:

```bash
m365 outlook event cancel --id "EVENT_ID" --comment "Lý do huỷ" --force
m365 outlook event remove --id "EVENT_ID" --force
```

---

## 6. Một buổi hay cả chuỗi

Đây là chỗ dễ sai nhất của cả skill, vì hai thứ trông giống nhau nhưng ID khác nhau. `calendarView` trả về từng **buổi**, không phải chuỗi:

| `type` | Nghĩa | PATCH/DELETE vào ID này thì |
|--------|-------|------------------------------|
| `singleInstance` | event lẻ | đổi chính nó |
| `occurrence` | một buổi của chuỗi, có `seriesMasterId` | chỉ đổi **buổi đó**, nó thành `exception`, các buổi khác nguyên vẹn |
| `exception` | buổi đã bị sửa riêng | đổi tiếp buổi đó |
| `seriesMaster` | định nghĩa chuỗi | đổi **toàn bộ** các buổi chưa bị sửa riêng |

Đã xác minh: chuỗi 4 buổi thứ Hai hàng tuần, PATCH vào ID buổi thứ hai để dời sang 11:00, kết quả buổi đó thành `exception` lúc 11:00 và ba buổi còn lại vẫn 09:00.

Quy tắc thực hành: khi người dùng nói "dời buổi họp mai", hỏi rõ **buổi đó thôi hay từ nay về sau**. Dời một buổi thì PATCH vào ID `occurrence`; đổi cả chuỗi thì lấy `seriesMasterId` rồi PATCH vào đó.

---

## 7. Workflow

### 7.1 Xem lịch một khoảng thời gian

```bash
USER=$(m365 status -o json --query 'connectedAs' | tr -d '"')
read START END < <("$DR" week)
echo "Khoảng đang xem: $START đến $END"   # in ra để người dùng đối chiếu
m365 request --url "https://graph.microsoft.com/v1.0/me/calendarView?startDateTime=$START&endDateTime=$END&\$select=subject,start,end,location&\$orderby=start/dateTime&\$top=200" \
  --prefer 'outlook.timezone="SE Asia Standard Time"' \
  -o json --query 'value[].{start:start.dateTime, subject:subject, where:location.displayName}'
```

### 7.2 Đặt cuộc họp, mời người, chọn phòng

1. Nếu người dùng chưa chốt giờ, tìm khung giờ chung trước (7.4).
2. Nếu cần phòng, liệt kê phòng rồi xem phòng nào rảnh, xem `references/graph-recipes.md`.
3. Xác nhận với người dùng: giờ, danh sách người mời, phòng. Bước này quan trọng vì POST là gửi thư mời thật.
4. Heredoc body (4.2, thêm phòng làm attendee `resource` nếu có) rồi POST.
5. Đọc lại bằng `calendarView` để xác nhận event đã nằm đúng giờ, đừng chỉ tin response của POST.

### 7.3 Dời một buổi trong chuỗi định kỳ

```bash
read START END < <("$DR" tomorrow)
# Lấy đúng buổi đó, kèm type để biết đang xử lý buổi hay chuỗi
m365 request --url "https://graph.microsoft.com/v1.0/me/calendarView?startDateTime=$START&endDateTime=$END&\$select=id,subject,type,seriesMasterId,start" \
  --prefer 'outlook.timezone="SE Asia Standard Time"' \
  -o json --query 'value[].{id:id, subject:subject, type:type, start:start.dateTime}'
```

Hỏi người dùng dời một buổi hay cả chuỗi (mục 6), rồi PATCH vào ID tương ứng với `start` và `end` mới.

### 7.4 Tìm khung giờ rảnh chung

Dùng `findMeetingTimes` để lấy gợi ý, hoặc `getSchedule` khi cần xem trực tiếp ai bận lúc nào. Cả hai ở `references/graph-recipes.md`. Nhớ header `Prefer`, đây chính là chỗ thiếu nó thì lệch 7 tiếng.

### 7.5 Huỷ họp và thông báo khách mời

1. Tìm event, in đủ thông tin gồm số người tham dự (mục 5).
2. Người dùng xác nhận đúng event đó.
3. Phân biệt `cancel` với `remove` theo bảng ở mục 5, nói rõ cho người dùng biết lệnh sắp chạy có gửi thư cho khách mời hay không.
4. Chạy với `--comment` nếu người dùng muốn kèm lý do.

---

## Phần chưa chạy thử

Đã verify bằng cách chạy thật: đọc `calendarView`, CRUD calendar, tạo event đơn, event lặp lại, event cả ngày, event họp online Teams, PATCH cả chuỗi và PATCH một buổi, `getSchedule`, `findMeetingTimes`, `findRooms`, `event cancel`, `event remove`.

Chưa chạy thử vì sẽ gửi thư thật vào hộp thư người khác: mời người tham dự bên ngoài và huỷ họp có khách mời. Schema theo tài liệu Graph. Lần đầu dùng nên kiểm lại kết quả trong Outlook.

## References

| File | Khi nào đọc |
|------|-------------|
| `references/graph-recipes.md` | recurrence, event cả ngày, trả lời thư mời, đặt phòng họp, `getSchedule`, `findMeetingTimes` |
| `references/advanced-commands.md` | calendargroup, chia sẻ calendar, đường `/places` mức admin |
| `../m365-shared/SKILL.md` | output format, JMESPath, xử lý lỗi |
| `../m365-shared/references/authentication.md` | các cách xác thực |
