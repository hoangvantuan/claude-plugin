# Graph recipes — the less common write and lookup cases

Every command here goes through `m365 request`, so the three rules of the Graph route always apply: heredoc the body to a file and pass `@path`, add `--content-type "application/json"` whenever there is a body, and add `--prefer 'outlook.timezone="SE Asia Standard Time"'` to anything with a time component.

Contents:

1. [Recurring events](#1-recurring-events)
2. [All-day events](#2-all-day-events)
3. [Responding to invitations](#3-responding-to-invitations)
4. [Meeting rooms](#4-meeting-rooms)
5. [Free/busy (getSchedule)](#5-freebusy)
6. [Finding a common slot (findMeetingTimes)](#6-finding-a-common-slot)

---

## 1. Recurring events

`recurrence` has two mandatory halves that travel together: `pattern` answers "how does it repeat" and `range` answers "until when". Graph rejects the request if either is missing.

```bash
SP="${TMPDIR:-/tmp}"
cat > "$SP/ev.json" <<'JSON'
{
  "subject": "Monday standup",
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

The response comes back as `type: "seriesMaster"`, and `calendarView` expands the individual occurrences (verified: a 4-week series yields 4 `occurrence` entries).

Common `pattern` shapes:

| Need | `pattern` |
|------|-----------|
| daily | `{"type":"daily","interval":1}` |
| specific weekdays | `{"type":"weekly","interval":1,"daysOfWeek":["monday","wednesday","friday"]}` |
| every two weeks | `{"type":"weekly","interval":2,"daysOfWeek":["tuesday"]}` |
| the 15th of every month | `{"type":"absoluteMonthly","interval":1,"dayOfMonth":15}` |
| the first Monday of every month | `{"type":"relativeMonthly","interval":1,"daysOfWeek":["monday"],"index":"first"}` |

`index` accepts `first`, `second`, `third`, `fourth`, `last`.

The `range` shapes:

| Need | `range` |
|------|---------|
| until a specific date | `{"type":"endDate","startDate":"2026-09-07","endDate":"2026-12-28"}` |
| repeat N times | `{"type":"numbered","startDate":"2026-09-07","numberOfOccurrences":10}` |
| no end date | `{"type":"noEnd","startDate":"2026-09-07"}` |

`startDate` inside `range` must match the date of `start.dateTime`. When they disagree, Graph **raises no error**: it silently shifts the first occurrence to `startDate`. Measured for real: `start.dateTime` on Sep 7 with `startDate` written as Sep 14 produced an event starting Sep 14, and the POST still returned 201 as usual. The way to protect yourself is to read `start.dateTime` back from the POST response and compare it with the date you intended.

To change the whole series, PATCH the `seriesMaster` ID. See section 6 of SKILL.md for the difference from editing one occurrence.

---

## 2. All-day events

Three conditions must hold at once, and Graph errors if one is missing: `isAllDay: true`, the times of both `start` and `end` are `00:00:00`, and `end` is the day **after** the event's last day.

```bash
cat > "$SP/ev.json" <<'JSON'
{
  "subject": "Annual leave",
  "isAllDay": true,
  "start": { "dateTime": "2026-09-12T00:00:00", "timeZone": "SE Asia Standard Time" },
  "end":   { "dateTime": "2026-09-13T00:00:00", "timeZone": "SE Asia Standard Time" }
}
JSON
```

The example above is **one** day off, Sep 12. For Sep 12 through 14, `end` becomes `2026-09-15T00:00:00`.

---

## 3. Responding to invitations

Three actions, one shape, differing only in the last URL segment: `accept`, `tentativelyAccept`, `decline`.

```bash
m365 request --url "https://graph.microsoft.com/v1.0/me/events/EVENT_ID/accept" --method post \
  --content-type "application/json" \
  --body '{"comment":"I can attend","sendResponse":true}'
```

`sendResponse: true` mails the reply to the organizer, so something does leave the mailbox. The user should know that before you run it, and should know which meeting is being answered, so print the subject and organizer for them to confirm first.

To propose a different time to the organizer, add `proposedNewTime` to the body of `tentativelyAccept` or `decline`:

```json
{
  "comment": "I have a conflict then, proposing one hour later",
  "sendResponse": true,
  "proposedNewTime": {
    "start": { "dateTime": "2026-09-05T15:00:00", "timeZone": "SE Asia Standard Time" },
    "end":   { "dateTime": "2026-09-05T16:00:00", "timeZone": "SE Asia Standard Time" }
  }
}
```

---

## 4. Meeting rooms

Listing rooms has to go through `beta`, because both `v1.0/places` and `m365 outlook room list` return 403 for a regular account (they need admin-level `Place.Read.All`). The `beta/me/findRooms` endpoint only needs `Calendars.Read`, and it is the route the Outlook app itself uses:

```bash
# Room list
m365 request --url 'https://graph.microsoft.com/beta/me/findRooms' -o json --query 'value[].{name:name, email:address}'

# Room lists (grouped by building, floor, site)
m365 request --url 'https://graph.microsoft.com/beta/me/findRoomLists' -o json --query 'value[].{name:name, email:address}'

# Rooms belonging to one room list
m365 request --url "https://graph.microsoft.com/beta/me/findRooms(RoomList='miichisoft.room@contoso.com')" -o json --query 'value[].{name:name, email:address}'
```

This is a `beta` endpoint and Microsoft does not guarantee its stability. A 404 means Microsoft retired it, not that the skill broke: at that point ask an Exchange admin to grant `Place.Read.All` and switch to `v1.0/places/microsoft.graph.room` or `m365 outlook room list`.

Booking a room means adding it to `attendees` with `type: "resource"`, plus a `location` for readability:

```bash
cat > "$SP/ev.json" <<'JSON'
{
  "subject": "Project kickoff",
  "start": { "dateTime": "2026-09-05T14:00:00", "timeZone": "SE Asia Standard Time" },
  "end":   { "dateTime": "2026-09-05T15:00:00", "timeZone": "SE Asia Standard Time" },
  "location": { "displayName": "Apolo", "locationEmailAddress": "apolo@contoso.com" },
  "attendees": [
    { "type": "required", "emailAddress": { "address": "persona@contoso.com", "name": "Person A" } },
    { "type": "resource", "emailAddress": { "address": "apolo@contoso.com", "name": "Apolo" } }
  ]
}
JSON
```

The room mailbox accepts or declines automatically according to the room's policy, so a successful POST **does not yet mean the room is held**. Read `attendees[].status.response` back from the event after creation to see whether the room accepted:

```bash
m365 request --url "https://graph.microsoft.com/v1.0/me/events/EVENT_ID?\$select=attendees" -o json \
  --query 'attendees[].{who:emailAddress.name, response:status.response}'
```

To be sure before booking, check the room's availability with `getSchedule` below, passing the room email like any other person.

---

## 5. Free/busy

`getSchedule` returns the free/busy state of several people or rooms at once as a character string, where each character covers one `availabilityViewInterval` in minutes.

```bash
cat > "$SP/sched.json" <<'JSON'
{
  "schedules": ["persona@contoso.com", "apolo@contoso.com"],
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

Decoding each character of `availabilityView`:

| Character | Meaning |
|-----------|---------|
| `0` | free |
| `1` | tentative |
| `2` | busy |
| `3` | out of office |
| `4` | working elsewhere |

A real measurement with `availabilityViewInterval: 60` over 08:00 to 18:00: `0220000000` means busy from 09:00 to 11:00 and free otherwise. The first character covers the slot beginning at `startTime`, so count from there to convert to clock time.

`getSchedule` only reports free or busy; it does **not** return meeting subjects, not even for your own calendar. To learn what someone is busy with, read `calendarView`.

Limit: at most 20 addresses in `schedules` per call. Batch beyond that.

---

## 6. Finding a common slot

`findMeetingTimes` lets Graph propose the slots instead of you reading `availabilityView` and reasoning it out.

```bash
cat > "$SP/find.json" <<'JSON'
{
  "attendees": [
    { "type": "required", "emailAddress": { "address": "persona@contoso.com" } },
    { "type": "required", "emailAddress": { "address": "personb@contoso.com" } }
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

A few things to know:

- This is the command that exposes the `Prefer` header pitfall most clearly: without it the response comes back in UTC, measured as `01:00` instead of `08:00`, exactly 7 hours off even though the body spelled out the timezone.
- `meetingDuration` uses the ISO 8601 duration format: `PT30M` is 30 minutes, `PT1H` is one hour, `PT1H30M` is an hour and a half.
- `activityDomain`: `work` confines suggestions to working hours; `personal` and `unrestricted` allow any time.
- `confidence` is the percentage likelihood everyone is free. Lower `minimumAttendeePercentage` to 70 when nothing comes back and you still want suggestions.
- When Graph finds no slot, `emptySuggestionsReason` says why, and it is worth reading so you can explain it to the user rather than just reporting "nothing". Seen in practice: `OrganizerUnavailable` (you are busy, or the window falls outside working hours) and `AttendeesUnavailable` (an invitee is busy).
