---
name: m365-meeting
description: "Teams meeting transcripts via the m365 CLI and Microsoft Graph: find the session, save it as a readable .txt beside the original .vtt, recordings, attendance. Use to fetch a transcript, not summarize one."
allowed-tools:
  - Bash
  - Read
---

# m365-meeting: Teams Transcripts, Recordings, Attendance

Fetch a transcript, write two files, stop. The `.txt` is for a model to read, the `.vtt` is the
untouched original. Summarizing is a different job with a different skill, so do not start one.

## Prerequisites

Run the preflight once at the start of a session. Three different walls all surface as a 403,
and it takes the guesswork out of which one you hit:

```bash
SK="<absolute path of the directory holding this SKILL.md>"   # cwd is usually the project, not the skill
"$SK/scripts/preflight.sh"
```

Exit 0 means go, 2 means partial (say which part is unavailable and carry on), 1 means blocked
and the output already contains the message to forward to IT. If a command fails with a 403
later in the session, rerun with `--full`: a freshly enabled tenant policy propagates gradually
and a single 403 is not a verdict.

Sign in with `m365 login --authType browser`. Never a bare `m365 login`: it defaults to the
device code flow, which private app registrations often disable, and the failure is a bare
`invalid_client` that says nothing about the real cause. Shared auth notes live in
`../m365-shared/references/authentication.md`.

## Operating principles

**A meeting is identified by `(meetingId, start time)`, never by name.** Names are not unique and
a recurring series reuses one `meetingId` for every occurrence. Every entry point (a name plus a
time anchor, a listing, a pasted link) resolves down to that pair before anything is downloaded.

**Two routes, decided by who organized the meeting.** This is the single most useful thing to know,
because the cheap route only covers half the meetings:

| Route              | Covers                        | How                                                                            | Cost                   |
| ------------------ | ----------------------------- | ------------------------------------------------------------------------------ | ---------------------- |
| bulk               | meetings **you** organized    | `getAllTranscripts(meetingOrganizerUserId='<you>')`, paged                     | one call for all of it |
| per-meeting thread | meetings you **attended**     | build the `meetingId` from the event's join URL, then `/onlineMeetings/{id}/transcripts` | one call per thread    |

There is no bulk endpoint for meetings other people organized, so the attended route costs a call
per meeting thread. Dedupe by thread before looping: that endpoint returns **every occurrence** of
a series, so a daily standup is one call for the whole week rather than five.

**Graph through `m365 request`, not the native commands.** `m365 teams meeting transcript list`
exists but takes one `--meetingId` at a time with no bulk form, and `transcript get` has no format
flag, so there is no way to ask for VTT. Use Graph for everything here.

**Fetch calendar events for matching WITHOUT the `Prefer` header.** This is the exact opposite of
the rule in `m365-calendar`, and the reason matters: matching happens on instants, and a naive
local timestamp cannot be compared to a transcript's UTC `createdDateTime` without knowing its
zone. No `Prefer` means Graph returns UTC and says so in `start.timeZone`. The resolver accepts
a `SE Asia Standard Time` file too, and refuses any zone it cannot convert exactly rather than
guessing, because guessing here silently selects a neighbouring occurrence.

---

## Verified pitfalls

Every row below was measured against a real tenant in this skill's build. Most are **silent**: the
call succeeds, returns data, and the data is incomplete or wrong.

| Pitfall                                           | Symptom                                                                                                                                     | Correct approach                                                                                     |
| ------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------ |
| `getAllTranscripts` pages, and page one looks whole | measured: page one returned **6** transcripts, following `@odata.nextLink` produced **3 more**. Nothing signals the shortfall                | always page. `scripts/list-transcripts.sh` does it                                                     |
| `while nextLink` never terminates                 | past the end Graph keeps returning a `nextLink` with an **empty** `value` array, forever                                                     | stop on an empty page, not on a missing link                                                           |
| Server-side date filters are accepted and ignored | `?startDateTime=...&endDateTime=...` **and** `$filter=createdDateTime ge ...` both return the full unfiltered list. A September window returned an August 13 transcript | filter client-side with `meeting-resolver.py --from/--to`                                             |
| Transcripts carry no meeting name                 | the payload has `meetingId` and timestamps and nothing human-readable                                                                       | decode the `meetingId` to a thread id and match it to the calendar, see below                          |
| A recurring series shares one `meetingId`         | five weekly occurrences are indistinguishable by id alone                                                                                   | pick the occurrence whose start is nearest the transcript's `createdDateTime`                          |
| Recording starts after the meeting does           | measured gaps between scheduled start and `createdDateTime`: 5.0, 5.1, 5.9, 7.8, 9.3, 11.4 minutes                                          | never require an exact time match; the resolver's default tolerance is 240 minutes and picks the nearest |
| `metadataContent` is not JSON                     | it is a WEBVTT file whose every cue payload happens to be a JSON object                                                                          | feed it to `transcript-to-text.py` like any VTT, it detects the shape                                  |
| `thread.tacv2` in a join URL                      | a **channel** meeting. The transcript routes return nothing for it, with no error                                                           | recognise it and tell the user it is out of reach, do not keep probing                                 |
| `3003: User does not have access to lookup meeting` | a 403 on a meeting that IS on your calendar and that you were invited to                                                                    | not fixable from here. Report it for that meeting and continue with the others                         |
| `$expand=attendanceRecords` returns null          | the report comes back, the records inside are empty                                                                                         | read the `attendanceReports/{id}/attendanceRecords` sub-endpoint instead                               |
| Cues overlap and interleave                       | two people talking at once produce cues whose spans intersect; cue N may not end before cue N+1 starts                                       | already handled by the converter, do not "fix" the ordering                                            |
| Reading the app registration needs admin          | `applications?$filter=appId eq '...'` returns **403** for an ordinary user                                                                  | you cannot tell "not declared" from "declared but not consented", so ask IT for both at once           |

`OnlineMeetingTranscript.Read.All` and `OnlineMeetingRecording.Read.All` are **not** in the `m365
setup` "All" preset, so a fresh install will not have them even after a successful login. The
preflight says so explicitly. Transcript and recording content are also billed under the Teams
meeting API model; the listing calls are not.

---

## 1. Transcripts of meetings you organized

```bash
SK="<absolute path of the skill directory>"
DR="$SK/../m365-calendar/scripts/date-range.sh"     # reused, do not duplicate it
ME=$(m365 request --url 'https://graph.microsoft.com/v1.0/me?$select=id' -o json --query 'id' | tr -d '"')
RANGE=$("$DR" week); START="${RANGE% *}"; END="${RANGE#* }"

"$SK/scripts/list-transcripts.sh" > transcripts.json      # paged for you

# Events for matching: no --prefer, so start.dateTime comes back as UTC
m365 request --url "https://graph.microsoft.com/v1.0/me/calendarView?startDateTime=$START&endDateTime=$END&\$select=subject,start,organizer,onlineMeeting&\$top=200" \
  -o json > events.json

python3 "$SK/scripts/meeting-resolver.py" match \
  --transcripts transcripts.json --events events.json --me "$ME" --from "$START" --to "$END"
```

Each row carries `subject`, `eventStartLocal` (GMT+7, for showing the user), `eventStartUtc` and
`endedUtc` (for the converter), `role`, `meetingId`, `transcriptId`, and `gapMinutes`. Print the
resolved window to the user, the same way `m365-calendar` does, so a different reading of "last
week" is caught immediately.

A row with `matched: false` is a transcript whose meeting is not in the calendar window. Usually
it is an ad-hoc "Meet now", or the window is too narrow. Widen the window before concluding
anything; never attach the nearest name to it as a guess.

## 2. Transcripts of meetings you attended

```bash
python3 "$SK/scripts/meeting-resolver.py" attended --events events.json --me "$ME" > attended.json

jq -r '.[].meetingId' attended.json | while read -r MID; do
  "$SK/scripts/list-transcripts.sh" --meeting-id "$MID"
done | jq -s 'add // []' > attended-transcripts.json
```

Then run the same `match` as section 1 with this file. Some of these calls return 403
(`3003: User does not have access to lookup meeting`) even for meetings you were invited to;
that is a Microsoft-side restriction. Note which meetings it hit and carry on with the rest.

## 3. "What do I have this week?"

Run sections 1 and 2 over the default 7-day window and present one table:

| Date (GMT+7) | Meeting | You are | Transcript |
| ------------ | ------- | ------- | ---------- |

The "no" rows are the meetings with nothing to fetch: events in `events.json` that carry a
`joinUrl` whose thread id appears in no matched row. Drop `thread.tacv2` threads from that list,
since a channel meeting never surfaces here even when it was transcribed.

Cost is roughly one bulk call plus one call per attended thread, about 15 calls for a normal week.
For a wider window pass a different anchor to `date-range.sh` (`month`, or two explicit dates);
say which window you used.

## 4. A pasted Teams link

The join URL already contains everything needed, so no lookup and no `OnlineMeetings.Read`:

```bash
MID=$(python3 "$SK/scripts/meeting-resolver.py" meeting-id --join-url 'https://teams.microsoft.com/l/meetup-join/...')
"$SK/scripts/list-transcripts.sh" --meeting-id "$MID"
```

If that returns several transcripts, the link points at a recurring series. Show the dates and ask
which one, unless the user's message already named a date.

## 5. Download and convert

```bash
jq '.[0]' rows.json > row.json          # or select the row the user picked, by transcriptId
MEETING_ID=$(jq -r '.meetingId' row.json); TRANSCRIPT_ID=$(jq -r '.transcriptId' row.json)
DATE=$(jq -r '.eventStartLocal' row.json | cut -d' ' -f1)
SLUG=$(jq -r '.subject' row.json | tr '/\\:*?"<>|' '_________')   # only what a filesystem forbids
BASE="${DATE}_${SLUG}"                  # braces are required: $DATE_ would read as an empty variable

EM=$(jq -rn --arg s "$MEETING_ID" '$s|@uri'); ET=$(jq -rn --arg s "$TRANSCRIPT_ID" '$s|@uri')
m365 request --url "https://graph.microsoft.com/v1.0/users/$ME/onlineMeetings/$EM/transcripts/$ET/content?\$format=text/vtt" \
  -o text > "$BASE.vtt"

# Metadata for the header, taken from the resolver row so the times carry an offset
jq --arg f "$BASE.vtt" '{subject, start: .eventStartUtc, end: .endedUtc, organizer,
   source: "Microsoft Graph", transcriptId, vttFile: $f}' row.json > meta.json

python3 "$SK/scripts/transcript-to-text.py" --input "$BASE.vtt" --meta meta.json --output "$BASE.txt"
```

Take `start` and `end` from the resolver row, never by copying `start.dateTime` out of
`calendarView`: that string is naive, its zone depends on a header you did not send, and the
converter refuses it rather than print a time seven hours out.

**File names**: `YYYY-MM-DD_<subject>`, keeping Vietnamese diacritics intact. Replace only the
characters a filesystem forbids, `/ \ : * ? " < > |`. Write to the current directory unless the
user named another one.

**Then stop.** Print both paths and one line of what is in the `.txt` (meeting, time, how many
speakers and turns), then offer the next step:

> Saved. For minutes or a communication analysis, run the `meeting-minutes` skill on the `.txt`.

Do not summarize, do not quote highlights, do not call another skill. The user asked for a
transcript; spending their tokens on analysis they did not request is the failure mode here.

## 6. Adding attendance to the header

Only for meetings you organized, and only with `OnlineMeetingArtifact.Read.All`:

```bash
R=$(m365 request --url "https://graph.microsoft.com/v1.0/users/$ME/onlineMeetings/$EM/attendanceReports" -o json --query 'value[0].id' | tr -d '"')
m365 request --url "https://graph.microsoft.com/v1.0/users/$ME/onlineMeetings/$EM/attendanceReports/$R/attendanceRecords" \
  -o json --query 'value[].{name:identity.displayName, role:role, seconds:totalAttendanceInSeconds}'
```

Feed the result into `meta.json` as `attendees` (for example `"Trần Bảo Ngọc (54m)"`). The header
then shows who was invited, who actually came, and who spoke, which is exactly what a minutes
pass would otherwise have to ask for.

---

## When there is no transcript

Say which of these it is rather than retrying:

- **Recording exists, transcript does not.** The meeting was recorded without live transcription.
  Point the user at `speech-to-text`, which transcribes the recording audio. Listing and
  downloading the recording is in `references/advanced-commands.md`.
- **Channel meeting** (`thread.tacv2` in the join URL). Out of reach on these routes.
- **The meeting is old enough that the `onlineMeeting` expired.** Per-meeting endpoints start
  failing; the bulk route may still have it.
- **Nobody turned transcription on.** Nothing to fetch.

## Known limits

Channel meetings. Recordings of meetings other people organized (Microsoft blocks this for
delegated auth). Assigning real names to `@1`, `@2` anonymous speakers: they are guests from
outside the tenant and Teams withholds the name, so the skill keeps the handle and says so rather
than guessing. Changing tenant configuration or app registrations: the preflight diagnoses and
hands you the wording, a human still has to act on it.

## Verified by running

Against a real tenant during this skill's build: paged `getAllTranscripts` (9 transcripts across
2 pages), transcript download as VTT and as `metadataContent`, the attended route (3 of 11 probed
meetings organized by other people returned transcripts, one returned `3003`, the rest were
genuinely empty), decoding a `meetingId` and matching it to a calendar event, correct occurrence
selection for a weekly series, `getAllRecordings` with delegated auth, and `attendanceRecords`.
The converter, resolver and preflight have offline tests in `tests/`, run with `tests/run-tests.sh`.

Not exercised: a tenant with the policy switched off or mid-propagation (the preflight's handling
of those is covered by tests against a fake CLI, not by a real blocked tenant), and downloading
recording content.

## References

| File                                          | When to read                                                                      |
| --------------------------------------------- | ----------------------------------------------------------------------------------- |
| `references/graph-recipes.md`                 | endpoint list, `meetingId` construction, paging loop, raw evidence for the pitfalls |
| `references/advanced-commands.md`             | recordings and attendance in full                                                   |
| `../m365-calendar/SKILL.md`                   | anything about the calendar itself, including creating the meeting                  |
| `../m365-shared/references/authentication.md` | login methods and the two consent traps                                             |
