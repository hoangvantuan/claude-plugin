#!/usr/bin/env python3
"""Behaviour of the converter: VTT in, readable .txt out. No network, no tenant."""
import importlib.util
import json
import pathlib
import re
import unittest

HERE = pathlib.Path(__file__).parent
FIX = HERE / "fixtures"
spec = importlib.util.spec_from_file_location("conv", HERE.parent / "scripts" / "transcript-to-text.py")
conv = importlib.util.module_from_spec(spec)
spec.loader.exec_module(conv)


def convert(name="sample.vtt", **kw):
    raw = (FIX / name).read_text(encoding="utf-8")
    meta = json.loads((FIX / "meta.json").read_text(encoding="utf-8"))
    return conv.render(conv.parse_cues(raw), meta, **kw)


class Cues(unittest.TestCase):
    def test_reads_every_cue_including_the_untagged_one(self):
        cues = conv.parse_cues((FIX / "sample.vtt").read_text(encoding="utf-8"))
        self.assertEqual(len(cues), 12)
        self.assertIsNone([c for c in cues if "Recording started" in c[3]][0][2])

    def test_metadata_content_json_payload_is_understood_too(self):
        cues = conv.parse_cues((FIX / "sample-metadata.vtt").read_text(encoding="utf-8"))
        self.assertEqual([c[2] for c in cues], ["Trần Bảo Ngọc", "Trần Bảo Ngọc", "@1"])
        self.assertEqual(cues[2][3], "はい。")

    def test_empty_input_yields_no_cues_rather_than_a_crash(self):
        self.assertEqual(conv.parse_cues("WEBVTT\n\n"), [])


class Turns(unittest.TestCase):
    def test_same_speaker_within_three_seconds_becomes_one_turn(self):
        out = convert()
        self.assertIn("[00:00:03] Trần Bảo Ngọc: Trước đây. Mình đã trao đổi rồi.", out)

    def test_a_pause_longer_than_three_seconds_starts_a_new_turn(self):
        out = convert()
        self.assertIn("[00:00:12] Trần Bảo Ngọc: Nhưng hôm nay khác.", out)

    def test_a_monologue_is_split_so_timestamps_stay_quotable(self):
        # @1 runs 2:00->2:25, 2:26->2:50, 2:51->3:15 with nobody interrupting. The first two
        # merge (50s), the third would push the turn to 75s and hide over a minute of speech
        # behind one mark, so it has to open a new turn instead.
        out = convert()
        self.assertIn("[00:02:00] @1: Phần một của đoạn dài. Phần hai của đoạn dài.", out)
        self.assertIn("[00:02:51] @1: Phần ba của đoạn dài.", out)

    def test_an_interjection_inside_another_turn_keeps_the_spoken_order(self):
        # Teams cues overlap: Osada backchannels at 0:20 while @1 is still talking (0:15-0:35).
        # Merging @1 across that would reorder the conversation, so the turn breaks instead.
        out = convert().split("\n---\n")[1].strip().splitlines()
        self.assertEqual(out[2:5], [
            "[00:00:15] @1: Ok giờ em sẽ xin phép bắt đầu buổi họp ngày hôm nay.",
            "[00:00:20] Shogo Osada: はい、わかりました。",
            "[00:00:36] @1: Phần thứ hai là báo cáo tiến độ. Phần thứ ba là các khó khăn gặp phải.",
        ])

    def test_turn_boundaries_are_configurable(self):
        self.assertIn("[00:00:03] Trần Bảo Ngọc: Trước đây.\n", convert(merge_gap=0.1))


class Header(unittest.TestCase):
    def setUp(self):
        self.out = convert()
        self.head = self.out.split("\n---\n")[0]

    def test_carries_every_field_the_reader_would_otherwise_ask_for(self):
        for needle in ("# [Solution] Weekly MTG", "Time (GMT+7): 2026-09-15 13:30",
                       "Organizer: Trần Bảo Ngọc", "Invited (2):", "Present (2):",
                       "Source: Microsoft Graph", "Transcript id: ktVizInGAAAAtest", "Original VTT:"):
            self.assertIn(needle, self.head, needle)

    def test_times_are_shown_in_gmt7_not_the_utc_graph_returned(self):
        self.assertIn("2026-09-15 13:30 to 14:30", self.head)  # 06:30Z is 13:30 in GMT+7

    def test_speakers_are_derived_from_the_transcript_not_taken_on_trust(self):
        self.assertIn("Speakers (4): Trần Bảo Ngọc, @1, Shogo Osada, @2", self.head)

    def test_untagged_system_lines_are_counted_apart_from_real_speakers(self):
        # Counting a "Recording started" notice as a participant would skew every
        # speaking-ratio analysis built on this file.
        self.assertIn("Unattributed lines: 1", self.head)

    def test_a_transcript_with_no_attribution_at_all_names_the_tenant_toggle(self):
        out = conv.render(conv.parse_cues("WEBVTT\n\n00:00:01.000 --> 00:00:02.000\nhello\n"), {})
        self.assertNotIn("Speakers (", out)
        self.assertIn("EnableAttributedTranscripts", out)

    def test_anonymous_speakers_are_listed_and_left_unguessed(self):
        self.assertIn("Anonymous: @1, @2", self.head)
        self.assertIn("not guessed", self.head)

    def test_absent_metadata_is_dropped_rather_than_printed_empty(self):
        out = conv.render(conv.parse_cues((FIX / "sample.vtt").read_text(encoding="utf-8")), {})
        self.assertTrue(out.startswith("# Teams meeting"))
        for absent in ("Organizer:", "Invited", "Present", "Time (GMT+7)"):
            self.assertNotIn(absent, out.split("\n---\n")[0])

    def test_a_graph_timestamp_with_seven_fractional_digits_still_parses(self):
        self.assertEqual(conv.local("2026-09-15T06:35:06.3111043Z"), "2026-09-15 13:35")

    def test_a_timestamp_without_an_offset_is_refused_rather_than_guessed(self):
        # calendarView returns naive local times with a Prefer header and naive UTC without one.
        # They are indistinguishable, and assuming either way is a silent seven-hour error.
        with self.assertRaises(SystemExit) as cm:
            conv.local("2026-09-15T06:30:00.0000000")
        self.assertIn("meeting-resolver.py", str(cm.exception))


class Body(unittest.TestCase):
    def test_every_line_is_timestamped_and_attributed(self):
        body = convert().split("\n---\n")[1].strip().splitlines()
        self.assertTrue(body)
        for line in body:
            self.assertRegex(line, r"^\[\d{2}:\d{2}:\d{2}\] .+: .+")

    def test_vietnamese_and_japanese_survive_the_round_trip(self):
        out = convert()
        self.assertIn("Nhưng hôm nay khác.", out)
        self.assertIn("はい、わかりました。", out)

    def test_a_cue_with_no_speaker_tag_is_marked_not_dropped(self):
        self.assertIn("(unlabelled): Recording started by the organizer.", convert())

    def test_anonymous_handles_are_kept_verbatim(self):
        self.assertTrue(re.search(r"^\[.*\] @2: Cảm ơn mọi người\.$", convert(), re.M))


if __name__ == "__main__":
    unittest.main(verbosity=2)
