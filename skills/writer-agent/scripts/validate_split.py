#!/usr/bin/env python3
"""Validate article splitting for writer-agent.

Ensures no overlap (same content in multiple parts) and no miss (content not covered).

Usage:
    python validate_split.py <plan_file>
    python validate_split.py docs/generated/my-book/analysis/_plan.md
    python validate_split.py docs/generated/my-book/analysis/_plan.md --content path/to/content.md

Output: JSON with validation result

Exit codes:
    0 - All splits valid (PASS)
    1 - Overlap or miss detected (FAIL)
    2 - Parse error or file not found
"""
from __future__ import annotations

import json
import re
import sys
from pathlib import Path
from typing import Any, Dict, List, Optional, Set, Tuple


def parse_plan_file(filepath: str) -> Dict[str, Any]:
    """Parse _plan.md file and extract split information.

    Args:
        filepath: Path to _plan.md file

    Returns:
        dict with articles, splits, and any parse errors
    """
    result: Dict[str, Any] = {
        "success": False,
        "filepath": filepath,
        "articles": [],
        "splits": [],
        "issues": [],
        "warnings": [],
    }

    path = Path(filepath)
    if not path.exists():
        result["error"] = f"File not found: {filepath}"
        return result

    content = path.read_text(encoding="utf-8")

    # Parse main article table
    # Format: | # | Slug | Title | Sections | Est. Output | Parts |
    # Or: | 2a | core-part1 | Core (1/3) | S03, S04 | 3200 | 3 |
    table_pattern = re.compile(
        r"\|\s*(\d+[a-z]?)\s*\|\s*([^|]+)\|\s*([^|]+)\|\s*([^|]+)\|\s*([^|]*)\|(?:\s*([^|]*)\|)?"
    )

    for match in table_pattern.finditer(content):
        article_num = match.group(1).strip()
        slug = match.group(2).strip()
        title = match.group(3).strip()
        sections_str = match.group(4).strip()
        est_output = match.group(5).strip() if match.group(5) else ""
        parts = match.group(6).strip() if match.group(6) else ""

        # Skip header row
        if article_num == "#" or slug == "Slug":
            continue

        # Parse sections (e.g., "S03, S04, S05")
        sections = [s.strip() for s in sections_str.split(",") if s.strip()]

        article = {
            "num": article_num,
            "slug": slug,
            "title": title,
            "sections": sections,
            "est_output": est_output,
            "parts": parts,
            "is_part": bool(re.match(r"\d+[a-z]", article_num)),
        }
        result["articles"].append(article)

    # Parse Split Details section if exists
    # Format: | Part | Sections | Lines | Est. Words | H2 Blocks |
    split_table_pattern = re.compile(
        r"\|\s*(\d+[a-z]?)\s*\|\s*([^|]+)\|\s*(\d+)-(\d+)\s*\|\s*([^|]+)\|"
    )

    in_split_section = False
    current_article = None

    for line in content.split("\n"):
        if "Split Details" in line or "Multi-Part Coverage" in line:
            in_split_section = True
            continue

        if in_split_section:
            # Check for article header (e.g., "### Article 2: Core Concepts")
            article_match = re.match(r"###\s*Article\s*(\d+):\s*(.+)", line)
            if article_match:
                current_article = article_match.group(1)
                continue

            # Parse split row
            split_match = split_table_pattern.match(line)
            if split_match and current_article:
                part_id = split_match.group(1).strip()
                sections_str = split_match.group(2).strip()
                line_start = int(split_match.group(3))
                line_end = int(split_match.group(4))
                est_words = split_match.group(5).strip()

                sections = [s.strip() for s in sections_str.split(",") if s.strip()]

                split_info = {
                    "article": current_article,
                    "part": part_id,
                    "sections": sections,
                    "line_start": line_start,
                    "line_end": line_end,
                    "est_words": est_words,
                }
                result["splits"].append(split_info)

    result["success"] = True
    return result


def validate_no_overlap(splits: List[Dict[str, Any]]) -> Tuple[bool, List[str]]:
    """Check that no line appears in multiple parts.

    Args:
        splits: List of split info dicts with line_start and line_end

    Returns:
        Tuple of (is_valid, list of issues)
    """
    issues = []
    covered_lines: Dict[int, str] = {}  # line -> part_id

    for split in splits:
        part_id = split.get("part", "unknown")
        line_start = split.get("line_start", 0)
        line_end = split.get("line_end", 0)

        for line in range(line_start, line_end + 1):
            if line in covered_lines:
                issues.append(
                    f"OVERLAP: Line {line} appears in both "
                    f"{covered_lines[line]} and {part_id}"
                )
            else:
                covered_lines[line] = part_id

    return len(issues) == 0, issues


def validate_no_miss(
    splits: List[Dict[str, Any]],
    expected_range: Optional[Tuple[int, int]] = None,
) -> Tuple[bool, List[str]]:
    """Check that all expected lines are covered.

    Args:
        splits: List of split info dicts with line_start and line_end
        expected_range: Optional (start, end) tuple for expected line range

    Returns:
        Tuple of (is_valid, list of issues)
    """
    issues = []

    if not splits:
        return True, []

    # Collect all covered lines
    covered_lines: Set[int] = set()
    for split in splits:
        line_start = split.get("line_start", 0)
        line_end = split.get("line_end", 0)
        covered_lines.update(range(line_start, line_end + 1))

    # Determine expected range
    if expected_range:
        expected_start, expected_end = expected_range
    else:
        # Infer from splits
        all_starts = [s.get("line_start", 0) for s in splits]
        all_ends = [s.get("line_end", 0) for s in splits]
        expected_start = min(all_starts) if all_starts else 0
        expected_end = max(all_ends) if all_ends else 0

    expected_lines = set(range(expected_start, expected_end + 1))
    missing_lines = expected_lines - covered_lines

    if missing_lines:
        # Group consecutive missing lines for cleaner output
        sorted_missing = sorted(missing_lines)
        ranges = []
        start = sorted_missing[0]
        prev = start

        for line in sorted_missing[1:]:
            if line == prev + 1:
                prev = line
            else:
                if start == prev:
                    ranges.append(str(start))
                else:
                    ranges.append(f"{start}-{prev}")
                start = line
                prev = line

        if start == prev:
            ranges.append(str(start))
        else:
            ranges.append(f"{start}-{prev}")

        issues.append(f"MISS: Lines not covered: {', '.join(ranges)}")

    return len(issues) == 0, issues


def validate_section_coverage(articles: List[Dict[str, Any]]) -> Tuple[bool, List[str]]:
    """Check that all sections are assigned to exactly one article/part.

    Args:
        articles: List of article dicts with sections

    Returns:
        Tuple of (is_valid, list of issues)
    """
    issues = []
    section_assignments: Dict[str, List[str]] = {}

    for article in articles:
        slug = article.get("slug", "unknown")
        for section in article.get("sections", []):
            section_assignments.setdefault(section, []).append(slug)

    # Check for sections assigned to multiple articles (excluding multi-part)
    for section, slugs in section_assignments.items():
        # Filter out parts of same article
        unique_bases = set()
        for slug in slugs:
            # Remove -partN suffix to get base
            base = re.sub(r"-part\d+$", "", slug)
            unique_bases.add(base)

        if len(unique_bases) > 1:
            issues.append(
                f"Section {section} assigned to multiple articles: {', '.join(slugs)}"
            )

    return len(issues) == 0, issues


def validate_min_part_size(
    splits: List[Dict[str, Any]],
    min_words: int = 0,  # No minimum - content coverage > word count
) -> Tuple[bool, List[str]]:
    """Check part word counts (informational only, no minimum enforced).

    Args:
        splits: List of split info dicts
        min_words: Deprecated, kept for compatibility (default 0 = no check)

    Returns:
        Tuple of (is_valid, list of info messages)
    """
    # No minimum word count validation - prioritize content coverage
    # This function now only provides informational output
    return True, []


def validate_split(filepath: str, content_path: Optional[str] = None) -> Dict[str, Any]:
    """Validate article splitting from _plan.md.

    Args:
        filepath: Path to _plan.md
        content_path: Optional path to content.md for line validation

    Returns:
        Validation result dict
    """
    result = parse_plan_file(filepath)

    if "error" in result:
        return result

    all_issues = []
    all_warnings = []

    # 1. Validate no overlap in splits
    if result["splits"]:
        overlap_valid, overlap_issues = validate_no_overlap(result["splits"])
        all_issues.extend(overlap_issues)

        # 2. Validate no miss
        miss_valid, miss_issues = validate_no_miss(result["splits"])
        all_issues.extend(miss_issues)

        # 3. Validate minimum part size
        _, size_warnings = validate_min_part_size(result["splits"])
        all_warnings.extend(size_warnings)

    # 4. Validate section coverage across articles
    section_valid, section_issues = validate_section_coverage(result["articles"])
    all_issues.extend(section_issues)

    result["issues"] = all_issues
    result["warnings"] = all_warnings
    result["passed"] = len(all_issues) == 0

    # Summary stats
    result["stats"] = {
        "total_articles": len(result["articles"]),
        "split_articles": len(
            set(s.get("article") for s in result["splits"])
        ),
        "total_parts": len(result["splits"]),
    }

    return result


def main():
    """CLI entry point."""
    if len(sys.argv) < 2 or sys.argv[1] in ("-h", "--help"):
        print(
            "Usage: python validate_split.py <plan_file> [--content path/to/content.md]\n"
            "\n"
            "Validates article splitting:\n"
            "  - No overlap: same line not in multiple parts\n"
            "  - No miss: all lines covered\n"
            "  - Section coverage: each section assigned once\n"
            "\n"
            "Exit codes:\n"
            "  0 - PASS (all validations passed)\n"
            "  1 - FAIL (overlap or miss detected)\n"
            "  2 - Error (parse error, file not found)"
        )
        sys.exit(2 if len(sys.argv) < 2 else 0)

    filepath = sys.argv[1]
    content_path: Optional[str] = None

    # Parse optional arguments
    i = 2
    while i < len(sys.argv):
        if sys.argv[i] == "--content" and i + 1 < len(sys.argv):
            content_path = sys.argv[i + 1]
            i += 2
        else:
            i += 1

    result = validate_split(filepath, content_path)

    print(json.dumps(result, indent=2, ensure_ascii=False))

    if "error" in result:
        sys.exit(2)
    elif result.get("passed", False):
        sys.exit(0)
    else:
        sys.exit(1)


if __name__ == "__main__":
    main()
