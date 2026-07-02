#!/usr/bin/env python3
"""Batch generate images via Codex CLI."""

import argparse
import subprocess
import sys
import time
from pathlib import Path


def run_codex(prompt, output_path):
    filename = output_path.name
    output_dir = output_path.parent

    full_prompt = (
        f"$imagegen {prompt}. "
        f"Save the final PNG as {filename} in {output_dir.resolve()}."
    )

    cmd = [
        "codex",
        "exec",
        "--skip-git-repo-check",
        "--enable",
        "image_generation",
        full_prompt,
    ]

    print(f"Generating: {filename}")
    print(f"  Prompt: {prompt[:80]}{'...' if len(prompt) > 80 else ''}")

    result = subprocess.run(cmd, capture_output=True, text=True, timeout=300)

    if result.returncode != 0:
        print(f"  FAILED: {result.stderr[:200]}")
        return False

    if output_path.exists():
        size_kb = output_path.stat().st_size / 1024
        print(f"  OK: {filename} ({size_kb:.0f} KB)")
        return True

    print(f"  WARNING: codex completed but {filename} not found")
    return False


def main():
    parser = argparse.ArgumentParser(description="Batch image generation via Codex CLI")
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("--prompts", nargs="+", help="List of prompts")
    group.add_argument("--prompt-file", help="File with one prompt per line")
    parser.add_argument(
        "--output-dir", default="./output-images", help="Output directory"
    )
    parser.add_argument("--prefix", default="image", help="Filename prefix")
    parser.add_argument(
        "--delay", type=int, default=5, help="Delay between requests (seconds)"
    )
    args = parser.parse_args()

    if args.prompt_file:
        with open(args.prompt_file) as f:
            prompts = [line.strip() for line in f if line.strip()]
    else:
        prompts = args.prompts

    if not prompts:
        print("No prompts provided.")
        sys.exit(1)

    output_dir = Path(args.output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)

    print(f"Batch: {len(prompts)} images → {output_dir}/")
    print()

    success = 0
    failed = 0

    for i, prompt in enumerate(prompts, 1):
        filename = f"{args.prefix}-{i:03d}.png"
        output_path = output_dir / filename

        if run_codex(prompt, output_path):
            success += 1
        else:
            failed += 1

        if i < len(prompts):
            time.sleep(args.delay)

    print()
    print(f"Done: {success} OK, {failed} failed, {len(prompts)} total")


if __name__ == "__main__":
    main()
