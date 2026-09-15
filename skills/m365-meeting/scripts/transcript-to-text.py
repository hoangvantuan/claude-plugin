#!/usr/bin/env python3
"""Turn a Teams meeting transcript into a compact, AI-readable .txt.

Teams hands out one cue per breath: a 45-minute meeting is ~600 cues of two or three
words each, and feeding that to a model burns tokens on timestamps rather than content.
This merges consecutive cues from the same speaker so a turn reads as a sentence, while
keeping one timestamp per turn so the reader can still cite a moment in the recording.

Two input shapes, both WEBVTT containers, auto-detected:
  content?$format=text/vtt  payload is `<v Speaker>words</v>`
  metadataContent           payload is a JSON object with speakerName / spokenText

Usage:
  transcript-to-text.py --input sample.vtt --meta meta.json --output out.txt
"""
import argparse
import json
import re
import sys
from datetime import datetime, timedelta, timezone

GMT7 = timezone(timedelta(hours=7))
TIME_RE = re.compile(r"(\d{1,2}):(\d{2}):(\d{2})[.,](\d{1,3})\s*-->\s*(\d{1,2}):(\d{2}):(\d{2})[.,](\d{1,3})")
VOICE_RE = re.compile(r"<v\s+([^>]*)>(.*?)(?:</v>)?$", re.DOTALL)


def _secs(h, m, s, ms):
    return int(h) * 3600 + int(m) * 60 + int(s) + int(ms.ljust(3, "0")) / 1000


def parse_cues(raw):
    """Yield (start, end, speaker, text). Speaker is None when the cue carries no tag.

    Teams cues overlap: two people talking at once produce cues whose spans intersect,
    so never assume cue N ends before cue N+1 starts. Order follows the file, which is
    ordered by start time, and that order is what makes the transcript readable.
    """
    cues = []
    for block in re.split(r"\n\s*\n", raw.replace("\r\n", "\n")):
        lines = [ln for ln in block.strip().split("\n") if ln.strip()]
        if not lines or lines[0].strip().upper().startswith("WEBVTT"):
            continue
        idx = next((i for i, ln in enumerate(lines) if "-->" in ln), None)
        if idx is None:
            continue
        m = TIME_RE.search(lines[idx])
        if not m:
            continue
        start, end = _secs(*m.group(1, 2, 3, 4)), _secs(*m.group(5, 6, 7, 8))
        payload = "\n".join(lines[idx + 1:]).strip()
        if not payload:
            continue
        speaker, text = _payload(payload)
        if text:
            cues.append((start, end, speaker, text))
    return cues


def _payload(payload):
    """metadataContent wraps each cue in JSON; plain VTT uses a <v> tag; neither is guaranteed."""
    if payload.startswith("{"):
        try:
            obj = json.loads(payload)
            return (obj.get("speakerName") or None), (obj.get("spokenText") or "").strip()
        except json.JSONDecodeError:
            pass
    m = VOICE_RE.match(payload)
    if m:
        return m.group(1).strip() or None, re.sub(r"\s+", " ", m.group(2)).strip()
    return None, re.sub(r"\s+", " ", payload).strip()


def group_turns(cues, merge_gap=3.0, max_turn=60.0):
    """Merge consecutive cues from one speaker into a turn.

    merge_gap keeps a pause from being swallowed: a gap over ~3s is usually a real
    handover, not a breath. max_turn caps how much text hides behind a single timestamp,
    so a long monologue still gets quotable marks roughly every minute.
    """
    turns = []
    for start, end, speaker, text in cues:
        if turns:
            prev = turns[-1]
            same = prev["speaker"] == speaker
            if same and start - prev["end"] <= merge_gap and end - prev["start"] <= max_turn:
                prev["text"] += " " + text
                prev["end"] = max(prev["end"], end)
                continue
        turns.append({"start": start, "end": end, "speaker": speaker, "text": text})
    return turns


def hms(seconds):
    s = int(seconds)
    return f"{s // 3600:02d}:{s % 3600 // 60:02d}:{s % 60:02d}"


def local(iso):
    """Render a Graph instant in GMT+7.

    A naive timestamp is refused rather than assumed. calendarView returns naive local times
    when the request carried a Prefer header and naive UTC when it did not, the two look
    identical, and picking wrong prints a meeting seven hours from when it happened. Graph
    also sends 7-digit fractional seconds, which fromisoformat rejects before Python 3.11.
    """
    if not iso:
        return None
    txt = re.sub(r"(\.\d{6})\d+", r"\1", iso.strip()).replace("Z", "+00:00")
    try:
        dt = datetime.fromisoformat(txt)
    except ValueError:
        return iso
    if dt.tzinfo is None:
        raise SystemExit(
            f"Timestamp '{iso}' carries no UTC offset, so its zone is a guess. Take the meeting "
            "times from meeting-resolver.py (eventStartUtc / endedUtc), not from raw calendarView.")
    return dt.astimezone(GMT7).strftime("%Y-%m-%d %H:%M")


def header(meta, turns):
    """Everything the reader would otherwise have to ask for. Absent fields are dropped
    rather than printed empty, so a thin header still reads as complete information."""
    speakers, seen = [], set()
    for t in turns:
        if t["speaker"] and t["speaker"] not in seen:
            seen.add(t["speaker"])
            speakers.append(t["speaker"])
    anon = [s for s in speakers if re.fullmatch(r"@\d+", s)]
    unlabelled = sum(1 for t in turns if not t["speaker"])

    out = [f"# {meta.get('subject') or 'Teams meeting'}", ""]
    when = local(meta.get("start"))
    if when:
        end = local(meta.get("end"))
        out.append(f"Time (GMT+7): {when}" + (f" to {end[-5:] if end else ''}" if end else ""))
    for label, key in (("Organizer", "organizer"), ("Source", "source"), ("Transcript id", "transcriptId"),
                       ("Original VTT", "vttFile")):
        if meta.get(key):
            out.append(f"{label}: {meta[key]}")
    for label, key in (("Invited", "invitees"), ("Present", "attendees")):
        vals = meta.get(key) or []
        if vals:
            out.append(f"{label} ({len(vals)}): " + ", ".join(str(v) for v in vals))
    if speakers:
        out.append(f"Speakers ({len(speakers)}): " + ", ".join(speakers))
    if unlabelled:
        # Teams leaves system notices untagged, which is harmless. A transcript where NOTHING
        # is tagged means the tenant has EnableAttributedTranscripts off, and that is worth
        # saying out loud: every downstream who-said-what analysis would otherwise be silently wrong.
        out.append(f"Unattributed lines: {unlabelled}" + ("" if speakers else
                   ". No line carries a speaker name at all, so the tenant is exposing transcripts "
                   "without speaker attribution. Ask IT for -EnableAttributedTranscripts."))
    if anon:
        out.append(f"Anonymous: {', '.join(anon)}. Teams did not attribute a name, usually a "
                   "guest from outside the tenant. Names were left as-is, not guessed.")
    if turns:
        out.append(f"Turns: {len(turns)}, transcript length {hms(turns[-1]['end'])}")
    out += ["", "---", ""]
    return out


def render(cues, meta, merge_gap=3.0, max_turn=60.0):
    turns = group_turns(cues, merge_gap, max_turn)
    lines = header(meta, turns)
    for t in turns:
        lines.append(f"[{hms(t['start'])}] {t['speaker'] or '(unlabelled)'}: {t['text']}")
    return "\n".join(lines) + "\n"


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--input", required=True, help="VTT or metadataContent file, - for stdin")
    ap.add_argument("--meta", help="JSON file with meeting metadata for the header")
    ap.add_argument("--output", help="destination .txt, default stdout")
    ap.add_argument("--merge-gap", type=float, default=3.0)
    ap.add_argument("--max-turn", type=float, default=60.0)
    args = ap.parse_args()

    raw = sys.stdin.read() if args.input == "-" else open(args.input, encoding="utf-8").read()
    meta = json.load(open(args.meta, encoding="utf-8")) if args.meta else {}
    cues = parse_cues(raw)
    if not cues:
        sys.exit("No cues found. The file is not a Teams transcript, or the download returned an error body.")
    text = render(cues, meta, args.merge_gap, args.max_turn)
    if args.output:
        with open(args.output, "w", encoding="utf-8") as fh:
            fh.write(text)
        print(f"{args.output}  ({len(cues)} cues -> {text.count(chr(10))} lines)")
    else:
        sys.stdout.write(text)


if __name__ == "__main__":
    main()
