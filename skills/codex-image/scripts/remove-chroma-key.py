#!/usr/bin/env python3
"""Remove chroma-key background from image, producing transparent PNG."""

import argparse
import sys

try:
    from PIL import Image
except ImportError:
    print("Cần cài Pillow: uv pip install --python ~/.venv/claude/bin/python Pillow")
    sys.exit(1)


def remove_chroma(input_path, output_path, color, tolerance):
    img = Image.open(input_path).convert("RGBA")
    pixels = img.load()
    w, h = img.size

    if color == "green":
        target = (0, 255, 0)
    elif color == "magenta":
        target = (255, 0, 255)
    else:
        parts = color.lstrip("#")
        target = tuple(int(parts[i : i + 2], 16) for i in (0, 2, 4))

    count = 0
    for y in range(h):
        for x in range(w):
            r, g, b, a = pixels[x, y]
            dr = abs(r - target[0])
            dg = abs(g - target[1])
            db = abs(b - target[2])
            if dr <= tolerance and dg <= tolerance and db <= tolerance:
                pixels[x, y] = (0, 0, 0, 0)
                count += 1

    img.save(output_path, "PNG")
    total = w * h
    pct = count / total * 100
    print(f"Done: {count}/{total} pixels removed ({pct:.1f}%)")
    print(f"Output: {output_path}")


def main():
    parser = argparse.ArgumentParser(description="Remove chroma-key background")
    parser.add_argument("input", help="Input image path")
    parser.add_argument("-o", "--output", required=True, help="Output PNG path")
    parser.add_argument(
        "--color",
        default="green",
        help="Chroma color: green, magenta, or hex (#RRGGBB). Default: green",
    )
    parser.add_argument(
        "--tolerance",
        type=int,
        default=30,
        help="Color matching tolerance (0-255). Default: 30",
    )
    args = parser.parse_args()
    remove_chroma(args.input, args.output, args.color, args.tolerance)


if __name__ == "__main__":
    main()
