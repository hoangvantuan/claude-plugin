#!/usr/bin/env python3
"""Convert VTT subtitle file to clean deduplicated plain text."""

import re
import sys


def convert_vtt_to_txt(vtt_path: str, output_path: str) -> None:
    seen: set[str] = set()
    lines_out: list[str] = []

    with open(vtt_path, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            if line.startswith("WEBVTT"):
                continue
            if line.startswith("Kind:") or line.startswith("Language:"):
                continue
            if "-->" in line:
                continue

            clean = re.sub(r"<[^>]*>", "", line)
            clean = (
                clean.replace("&amp;", "&")
                .replace("&gt;", ">")
                .replace("&lt;", "<")
            )
            clean = clean.strip()

            if clean and clean not in seen:
                lines_out.append(clean)
                seen.add(clean)

    with open(output_path, "w", encoding="utf-8") as f:
        f.write("\n".join(lines_out) + "\n")

    print(f"Saved to: {output_path}")
    print(f"Total lines: {len(lines_out)}")


if __name__ == "__main__":
    if len(sys.argv) != 3:
        print(f"Usage: {sys.argv[0]} <input.vtt> <output.txt>")
        sys.exit(1)
    convert_vtt_to_txt(sys.argv[1], sys.argv[2])
