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
which m365 || echo "m365 CLI not installed. Run: npm i -g @pnp/cli-microsoft365"
m365 status || echo "Not signed in. Run: m365 login"
```

Auth details: `../m365-shared/references/authentication.md`.

## Operating Principles

The native `m365 outlook` commands have no `event add`/`event set`, so this skill runs on **two parallel routes**, and knowing which route you are on is what keeps the syntax right:

| Route | Used for | Syntax quirks |
|-------|----------|---------------|
| Native `m365 outlook ...` | calendar CRUD, reading a single event, cancelling/removing an event | `--userName` is mandatory, times must carry `Z` |
| Graph through `m365 request` | reading a date range, creating/updating events, free/busy, finding times, meeting rooms | write the body to a file via heredoc, the `Prefer` header is mandatory |

Two opening lines cover almost every task:

```bash
# Current user (every native command needs it, there is no "me" default)
USER=$(m365 status -o json --query 'connectedAs' | tr -d '"')

# Date-range helper script, sitting next to this SKILL.md. Use the absolute path of the
# directory holding the SKILL.md you just read, because the current working directory is
# usually NOT the skill directory (installed as a plugin the skill lives under ~/.claude,
# while cwd is the project).
DR="<skill-directory-path>/scripts/date-range.sh"

# Date range, already anchored to midnight Vietnam time. Do NOT use `read < <(...)`:
# process substitution is not portable, it is a syntax error under POSIX `sh`.
# Command substitution is verified working in both bash and zsh.
RANGE=$("$DR" week); START="${RANGE% *}"; END="${RANGE#* }"
```

Reading someone else's calendar requires that calendar to be shared with you, or admin rights. On a 403, state the permission limit plainly instead of probing around with other commands.

---

## Verified pitfalls

The eight items below were measured by running against a real tenant; documentation does not surface them. Seven of the eight are **silent failures**: the command still runs, still returns events, the result is simply wrong, so there is no way to notice except knowing in advance.

| Pitfall | Symptom | Correct approach |
|---------|---------|------------------|
| `event list` drops recurring meetings | same week: `/me/events` returns **12**, `/me/calendarView` returns **46**. `/me/events` only returns the `seriesMaster`, it does not expand the individual occurrences | every date-range question goes through `calendarView`, see section 1 |
| Missing `Prefer` header | Graph returns UTC, off by exactly 7 hours. `findMeetingTimes` returns `01:00` instead of `08:00` even when the body carries a timezone | every Graph call with a time component adds `--prefer 'outlook.timezone="SE Asia Standard Time"'`. A timezone in the body is **not enough** |
| UTC midnight is not Vietnam midnight | `00:00:00Z` is 07:00 in GMT+7, so a 06:00 Monday meeting falls outside "this week" | always take the range from `scripts/date-range.sh`; it anchors GMT+7 midnight, so it prints `...T17:00:00Z` of the previous day, which is correct |
| Times missing `Z` | `--startDateTime 2026-08-17T00:00:00` is rejected outright: "is not a valid ISO date-time" | always include `Z` or an offset |
| `--userName` has no "me" default | `Error: Specify either userId or userName, but not both` even when it is merely missing, not both passed. The message is misleading | mandatory for `calendar *` and `event list`/`event get`; `event cancel`/`event remove` do not need it with delegated auth |
| A `calendarView` ID is a single-occurrence ID | `calendarView` returns `type: "occurrence"` with a `seriesMasterId`. PATCHing that ID changes only that occurrence (it becomes an `exception`), not the whole series | to change the whole series, PATCH the `seriesMasterId`. See section 6 |
| `recurrence` shifts the date without an error | when `range.startDate` disagrees with `start.dateTime`, Graph silently moves the first occurrence to `startDate` and the POST still reports success | the two dates must match, and read `start.dateTime` back from the response to confirm |
| Meeting room list | `outlook room list` and `v1.0/places` return **403** (they need admin-level `Place.Read.All`), yet rooms are still discoverable | use `beta/me/findRooms`, the route the Outlook app itself uses; it only needs `Calendars.Read` |

Not available with the m365 CLI default app: working hours and automatic replies (`mailboxSettings` returns 403, missing `MailboxSettings.Read`).

---

## 1. Read the calendar over a date range

This is the most frequent task, and `calendarView` is the only correct route because it expands each occurrence of a recurring series.

```bash
RANGE=$("$DR" week); START="${RANGE% *}"; END="${RANGE#* }"

m365 request \
  --url "https://graph.microsoft.com/v1.0/me/calendarView?startDateTime=$START&endDateTime=$END&\$select=subject,start,end,location,isAllDay,type,seriesMasterId&\$orderby=start/dateTime&\$top=200" \
  --prefer 'outlook.timezone="SE Asia Standard Time"' \
  -o json --query 'value[].{start:start.dateTime, end:end.dateTime, subject:subject, where:location.displayName}'
```

Things to know:

- `$top=200` because Graph pages at 10 items by default; without it you lose events with no sign anything went missing.
- `calendarView` reads **one** calendar per call, the primary calendar by default. To merge several calendars, loop over each `id` with `me/calendars/{id}/calendarView`.
- `$` inside the URL must be escaped as `\$` when it sits in a bash double-quoted string.
- **Print the resolved date range to the user** in your answer (for example "week of Aug 17 to 23"), so they immediately catch it if you read "this week" differently than they meant.

```bash
# Merge every calendar. Use -o text so each line is one id, no JSON slicing needed
m365 outlook calendar list --userName "$USER" -o text --query '[].id' | while read -r CAL; do
  m365 request --url "https://graph.microsoft.com/v1.0/me/calendars/$CAL/calendarView?startDateTime=$START&endDateTime=$END&\$select=subject,start&\$top=200" \
    --prefer 'outlook.timezone="SE Asia Standard Time"' -o json --query 'value[].{start:start.dateTime, subject:subject}'
done
```

---

## 2. Calendars (native commands, full CRUD)

```bash
# List
m365 outlook calendar list --userName "$USER" -o json --query '[].{id:id, name:name, canEdit:canEdit, isDefault:isDefaultCalendar}'

# Get one calendar by name
m365 outlook calendar get --userName "$USER" --name "Calendar" -o json

# Create
m365 outlook calendar add --userName "$USER" --name "Project Alpha" --color lightGreen -o json --query 'id'

# Rename or recolor (--id is mandatory, --name is not accepted as the identifier)
m365 outlook calendar set --userName "$USER" --id "CAL_ID" --name "New name" --color lightBlue

# Delete (deletes the events inside too, ask the user first)
m365 outlook calendar remove --userName "$USER" --name "Project Alpha" --force
```

`--color`: `auto`, `lightBlue`, `lightGreen`, `lightOrange`, `lightGray`, `lightYellow`, `lightTeal`, `lightPink`, `lightBrown`, `lightRed`, `maxColor`.

---

## 3. Read a single event and read a series definition

```bash
# One event by ID
m365 outlook event get --userName "$USER" --id "EVENT_ID" --timeZone "SE Asia Standard Time" -o json \
  --query '{subject:subject, start:start.dateTime, organizer:organizer.emailAddress.name, attendees:attendees[].emailAddress.address}'

# The recurring series definition (this is where event list earns its keep: it returns the seriesMaster and does not expand occurrences)
m365 outlook event list --userName "$USER" --calendarName "Calendar" \
  --startDateTime "$START" --endDateTime "$END" --timeZone "SE Asia Standard Time" \
  -o json --query "[?type=='seriesMaster'].{id:id, subject:subject, pattern:recurrence.pattern.type}"
```

`--timeZone` is mandatory in practice: without it you get UTC, off by 7 hours.

---

## 4. Create and update events (Graph)

Always heredoc the body to a file and pass `@path`. Reason: accented subjects, a single quote (`"Tuan's team sync"`), or a multi-line body crammed into a one-line `--body '{...}'` breaks the quoting. Put the delimiter in single quotes (`<<'JSON'`) so bash interpolates nothing.

### 4.1 Single event

```bash
SP="${TMPDIR:-/tmp}"
cat > "$SP/ev.json" <<'JSON'
{
  "subject": "Q4 plan review",
  "body": { "contentType": "text", "content": "Agenda notes" },
  "start": { "dateTime": "2026-09-05T10:00:00", "timeZone": "SE Asia Standard Time" },
  "end":   { "dateTime": "2026-09-05T11:00:00", "timeZone": "SE Asia Standard Time" },
  "location": { "displayName": "Apolo Room" }
}
JSON

m365 request --url 'https://graph.microsoft.com/v1.0/me/events' --method post \
  --content-type "application/json" --body "@$SP/ev.json" \
  --prefer 'outlook.timezone="SE Asia Standard Time"' \
  -o json --query '{id:id, subject:subject, start:start.dateTime}'
```

To create in a different calendar, change the URL to `me/calendars/{calendarId}/events`. Native `--id` flags take the raw ID untouched. For a hand-built URL, URL-encode it first as a precaution: `ENC=$(jq -rn --arg s "$CALID" '$s|@uri')`. Measured ids are base64url (`-`, `_`, `=`) and splice in fine unencoded, but Graph does not guarantee that alphabet, and a `/` or `+` would silently break the path.

**Avoid duplicate creation**: if the POST times out or its success is unclear, do not resend it right away. Read the `calendarView` for that range first, because a second POST creates another event rather than overwriting. Watch for one easy variant of this: an error appearing on the **line after** the POST (a shell error, an empty variable, broken quoting) does not mean the POST failed. The event is already on the calendar; check before rerunning.

### 4.2 Event with attendees

```bash
cat > "$SP/ev.json" <<'JSON'
{
  "subject": "Project kickoff",
  "start": { "dateTime": "2026-09-05T14:00:00", "timeZone": "SE Asia Standard Time" },
  "end":   { "dateTime": "2026-09-05T15:00:00", "timeZone": "SE Asia Standard Time" },
  "attendees": [
    { "type": "required", "emailAddress": { "address": "persona@contoso.com", "name": "Person A" } },
    { "type": "optional", "emailAddress": { "address": "personb@contoso.com", "name": "Person B" } }
  ]
}
JSON
```

With `attendees` present, Graph **sends real invitations** the moment the POST succeeds; there is no draft step. Confirm the recipient list with the user before running it.

### 4.3 Teams online meeting

Add two fields to the body from 4.1 or 4.2:

```json
"isOnlineMeeting": true,
"onlineMeetingProvider": "teamsForBusiness"
```

Graph generates the link; read it back at `onlineMeeting.joinUrl` (verified: the link is present right after creation).

### 4.4 Update an event

A PATCH only needs the fields you want to change; the rest stay as they are:

```bash
m365 request --url "https://graph.microsoft.com/v1.0/me/events/EVENT_ID" --method patch \
  --content-type "application/json" \
  --body '{"subject":"New subject"}' \
  --prefer 'outlook.timezone="SE Asia Standard Time"' -o json --query 'subject'
```

To move the time you must send **both** `start` and `end`; sending `start` alone yields an event whose end time precedes its start.

---

## 5. Cancel and remove

These two differ in whether mail goes out, and picking the wrong one sends unintended cancellation mail to the guests:

| Command | What it does | When |
|---------|--------------|------|
| `event cancel` | cancels the meeting and **sends a cancellation to every attendee** | you are the organizer and people need to be told |
| `event remove` | only drops the event from your own calendar, notifies nobody | an event you created with no guests, or tidying your own calendar |

Neither can be undone, and `cancel` also leaves the organization, so before running either, print the event in full for the user to identify, then wait for their confirmation, one event at a time, never in bulk:

```bash
m365 outlook event get --userName "$USER" --id "EVENT_ID" --timeZone "SE Asia Standard Time" -o json \
  --query '{subject:subject, start:start.dateTime, organizer:organizer.emailAddress.name, attendeeCount:length(attendees)}'
```

After the user agrees:

```bash
m365 outlook event cancel --id "EVENT_ID" --comment "Reason for cancelling" --force
m365 outlook event remove --id "EVENT_ID" --force
```

---

## 6. One occurrence or the whole series

This is the easiest thing in the whole skill to get wrong, because the two look alike but carry different IDs. `calendarView` returns individual **occurrences**, not the series:

| `type` | Meaning | PATCH/DELETE on this ID |
|--------|---------|-------------------------|
| `singleInstance` | standalone event | changes itself |
| `occurrence` | one occurrence of a series, carries `seriesMasterId` | changes **that occurrence only**, it becomes an `exception`, the others stay untouched |
| `exception` | an occurrence already edited on its own | keeps editing that occurrence |
| `seriesMaster` | the series definition | changes **all** occurrences; PATCHing its `start`/`end` additionally **resets** individually edited occurrences |

Verified: a 4-occurrence weekly Monday series, PATCHing the second occurrence's ID to move it to 11:00, results in that occurrence becoming an `exception` at 11:00 while the other three stay at 09:00.

Practical rule: when the user says "move tomorrow's meeting", ask explicitly whether they mean **that occurrence only or from now on**. Moving one occurrence PATCHes the `occurrence` ID; changing the series takes the `seriesMasterId` and PATCHes that.

Measured for real: with one `exception` in the series, PATCHing only the `subject` on the master preserves that exception at its moved time; PATCHing `start`/`end` on the master wipes it, the occurrence snaps back to the new pattern time and reverts to type `occurrence`. Before moving a whole series that has hand-edited occurrences, warn the user those edits will be lost.

---

## 7. Workflows

### 7.1 View the calendar over a range

```bash
USER=$(m365 status -o json --query 'connectedAs' | tr -d '"')
RANGE=$("$DR" week); START="${RANGE% *}"; END="${RANGE#* }"
echo "Range in view: $START to $END"   # print it so the user can double-check
m365 request --url "https://graph.microsoft.com/v1.0/me/calendarView?startDateTime=$START&endDateTime=$END&\$select=subject,start,end,location&\$orderby=start/dateTime&\$top=200" \
  --prefer 'outlook.timezone="SE Asia Standard Time"' \
  -o json --query 'value[].{start:start.dateTime, subject:subject, where:location.displayName}'
```

### 7.2 Book a meeting, invite people, pick a room

1. If the user has not fixed a time, find a common slot first (7.4).
2. If a room is needed, list rooms and check which are free, see `references/graph-recipes.md`.
3. Confirm with the user: time, invitee list, room. This step matters because the POST sends real invitations.
4. Heredoc the body (4.2, adding the room as a `resource` attendee if any) and POST.
5. Read it back with `calendarView` to confirm the event landed at the right time; do not just trust the POST response.

### 7.3 Move one occurrence of a recurring series

```bash
RANGE=$("$DR" tomorrow); START="${RANGE% *}"; END="${RANGE#* }"
# Fetch that occurrence, including type so you know whether you hold an occurrence or a series
m365 request --url "https://graph.microsoft.com/v1.0/me/calendarView?startDateTime=$START&endDateTime=$END&\$select=id,subject,type,seriesMasterId,start" \
  --prefer 'outlook.timezone="SE Asia Standard Time"' \
  -o json --query 'value[].{id:id, subject:subject, type:type, start:start.dateTime}'
```

Ask the user whether to move one occurrence or the whole series (section 6), then PATCH the matching ID with the new `start` and `end`.

### 7.4 Find a common free slot

Use `findMeetingTimes` for suggestions, or `getSchedule` when you need to see directly who is busy when. Both live in `references/graph-recipes.md`. Remember the `Prefer` header, this is exactly where missing it costs you 7 hours.

### 7.5 Cancel a meeting and notify the guests

1. Find the event, print the full details including the attendee count (section 5).
2. The user confirms it is the right event.
3. Distinguish `cancel` from `remove` using the table in section 5, and tell the user plainly whether the command about to run mails the guests.
4. Run it with `--comment` if the user wants to include a reason.

---

## Not yet exercised

Verified by running for real: reading `calendarView`, calendar CRUD, creating a single event, a recurring event, an all-day event, a Teams online meeting, PATCHing a whole series and PATCHing one occurrence, `getSchedule`, `findMeetingTimes`, `findRooms`, `event cancel`, `event remove`.

Not tried, because it would send real mail into other people's inboxes: inviting external attendees, and cancelling a meeting that has guests. Those schemas follow the Graph documentation. On first use, verify the result in Outlook.

## References

| File | When to read |
|------|--------------|
| `references/graph-recipes.md` | recurrence, all-day events, responding to invitations, booking meeting rooms, `getSchedule`, `findMeetingTimes` |
| `references/advanced-commands.md` | calendargroup, calendar sharing, the admin-level `/places` route |
| `../m365-shared/SKILL.md` | output format, JMESPath, error handling |
| `../m365-shared/references/authentication.md` | authentication methods |
