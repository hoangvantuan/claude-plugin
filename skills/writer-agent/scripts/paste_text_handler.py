#!/usr/bin/env python3
"""Handle pasted text input for writer-agent.

Usage:
    # From file containing pasted text
    python paste_text_handler.py /tmp/pasted_content.txt [--title "My Title"] [--output docs/generated/my-doc/input-handling]

    # From stdin
    echo "My content here" | python paste_text_handler.py - [--title "My Title"]

Output: content.md + structure.json in output directory
    - If output specified: uses that folder
    - If not specified: creates docs/generated/{slug}-{YYMMDD-HHMM}/input-handling/
"""
from __future__ import annotations

import argparse
import json
import sys
from datetime import datetime
from pathlib import Path

# Import shared extract_structure module
from extract_structure import extract_structure, generate_slug


def derive_title(content: str) -> str:
    """Derive title from content first line.

    Args:
        content: Text content

    Returns:
        Title derived from first line (cleaned) or empty string
    """
    if not content.strip():
        return ""

    # Get first non-empty line
    for line in content.splitlines():
        line = line.strip()
        if line:
            # Remove markdown heading prefix if present
            if line.startswith("#"):
                line = line.lstrip("#").strip()

            # Limit to ~10 words for reasonable title
            words = line.split()
            if len(words) > 10:
                line = " ".join(words[:10]) + "..."

            return line

    return ""


def handle_pasted_text(
    content: str,
    title: str = "",
    output_dir: str = ""
) -> dict:
    """Process pasted text and save as markdown with structure.

    Args:
        content: Pasted text content
        title: Optional title (derived from content if not provided)
        output_dir: Output directory (auto-generated if not provided)

    Returns:
        dict with success, output_path, structure_path, title, or error
    """
    result = {
        "success": False,
        "source": "pasted_text",
        "output_path": None,
        "structure_path": None,
        "project_dir": None,
        "title": None,
        "error": None
    }

    # Validate content
    if not content or not content.strip():
        result["error"] = "Empty content provided"
        return result

    # Derive title if not provided
    if not title:
        title = derive_title(content)

    if not title:
        result["error"] = "No title provided and could not derive from content"
        return result

    result["title"] = title

    # Generate output directory with timestamp pattern: {slug}-{YYMMDD-HHMM}
    slug = generate_slug(title)
    timestamp = datetime.now().strftime("%y%m%d-%H%M")
    if output_dir:
        out_dir = Path(output_dir)
    else:
        out_dir = Path("docs/generated") / f"{slug}-{timestamp}" / "input-handling"

    out_dir.mkdir(parents=True, exist_ok=True)

    try:
        # Write content.md
        content_path = out_dir / "content.md"
        content_path.write_text(content, encoding="utf-8")
        result["output_path"] = str(content_path)

        # Generate and write structure.json
        structure = extract_structure(content, "pasted_text", "pasted_text", title)
        structure_path = out_dir / "structure.json"
        structure_path.write_text(
            json.dumps(structure, indent=2, ensure_ascii=False),
            encoding="utf-8"
        )
        result["structure_path"] = str(structure_path)
        result["structure"] = structure

        # Set project directory
        result["project_dir"] = str(out_dir.parent)

        # Add metadata
        result["metadata"] = {
            "char_count": structure["stats"]["char_count"],
            "word_count": structure["stats"]["word_count"],
            "line_count": structure["stats"]["line_count"],
            "tier": structure["tier_recommendation"]["tier"],
            "heading_count": len(structure["outline"]),
            "chunk_count": len(structure["suggested_chunks"])
        }

        result["success"] = True

    except Exception as e:
        result["error"] = f"Error processing content: {str(e)}"

    return result


def main():
    """CLI entry point."""
    parser = argparse.ArgumentParser(
        description="Handle pasted text input for writer-agent"
    )
    parser.add_argument("input", help="Input file path or '-' for stdin")
    parser.add_argument("--title", "-t", default="", help="Document title")
    parser.add_argument("--output", "-o", default="", help="Output directory")

    args = parser.parse_args()

    # Read content from file or stdin
    if args.input == "-":
        content = sys.stdin.read()
    else:
        input_path = Path(args.input)
        if not input_path.exists():
            print(json.dumps({
                "success": False,
                "error": f"File not found: {args.input}"
            }, indent=2))
            sys.exit(1)
        content = input_path.read_text(encoding="utf-8")

    result = handle_pasted_text(content, args.title, args.output)
    print(json.dumps(result, indent=2))

    sys.exit(0 if result["success"] else 1)


if __name__ == "__main__":
    main()
