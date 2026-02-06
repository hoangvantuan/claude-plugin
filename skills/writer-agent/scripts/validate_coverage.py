#!/usr/bin/env python3
"""Validate coverage report for writer-agent.

Usage:
    python validate_coverage.py <coverage_file> [threshold]
    python validate_coverage.py docs/generated/my-book/analysis/_coverage.md
    python validate_coverage.py docs/generated/my-book/analysis/_coverage.md 98 --target-words 3000
    python validate_coverage.py docs/generated/my-book/analysis/_coverage.md --structure docs/generated/my-book/analysis/structure.json

Output: JSON with validation result

Exit codes:
    0 - Coverage >= 98% (PASS)
    1 - Coverage < 98% (FAIL)
    2 - Parse error or file not found
"""
from __future__ import annotations

import json
import re
import sys
from pathlib import Path
from typing import Any, Dict, List, Optional


# Valid skip reasons (case-insensitive match)
VALID_SKIP_REASONS = ["redundant", "off-topic", "user instruction"]


def parse_coverage_file(filepath: str) -> Dict[str, Any]:
    """Parse _coverage.md file and extract coverage data.

    Args:
        filepath: Path to _coverage.md file

    Returns:
        dict with sections, stats, and issues
    """
    result = {
        "success": False,
        "filepath": filepath,
        "sections": [],
        "stats": {
            "total": 0,
            "used": 0,
            "missing": 0,
            "critical_total": 0,
            "critical_used": 0,
            "critical_missing": 0,
        },
        "coverage_percent": 0.0,
        "critical_coverage_percent": 0.0,
        "issues": [],
        "warnings": [],
        "missing_sections": [],
        "missing_critical": [],
    }

    path = Path(filepath)
    if not path.exists():
        result["error"] = f"File not found: {filepath}"
        return result

    content = path.read_text(encoding="utf-8")

    # Parse table rows
    # Expected format: | S01 | 01-context.md | 01-intro.md | ✅ USED |
    # Or: | S03 ⭐ | 02-context.md | 02-core.md | ✅ verbatim |
    table_pattern = re.compile(
        r"\|\s*(S\d+)\s*(⭐)?\s*\|\s*([^|]+)\|\s*([^|]+)\|\s*([^|]+)\|"
    )

    # Track sections per article for duplicate detection
    section_assignments: Dict[str, List[str]] = {}

    for match in table_pattern.finditer(content):
        section_id = match.group(1).strip()
        is_critical = bool(match.group(2))
        assigned_to = match.group(3).strip()
        used_in = match.group(4).strip()
        status = match.group(5).strip().lower()

        section = {
            "id": section_id,
            "critical": is_critical,
            "assigned_to": assigned_to,
            "used_in": used_in,
            "status": status,
        }
        result["sections"].append(section)

        # Count stats
        result["stats"]["total"] += 1
        if is_critical:
            result["stats"]["critical_total"] += 1

        # Check if used (✅, used, verbatim, quoted, summarized)
        is_used = any(
            indicator in status
            for indicator in ["✅", "used", "verbatim", "quoted", "summarized"]
        )

        if is_used:
            result["stats"]["used"] += 1
            if is_critical:
                result["stats"]["critical_used"] += 1

            # Phase 2.1b: Critical section verbatim check
            if is_critical and "summarized" in status:
                if "verbatim" not in status and "quoted" not in status:
                    result["warnings"].append(
                        f"Critical section {section_id} is only summarized, "
                        f"should be verbatim or quoted"
                    )
        else:
            result["stats"]["missing"] += 1
            result["missing_sections"].append(section_id)
            if is_critical:
                result["stats"]["critical_missing"] += 1
                result["missing_critical"].append(section_id)

            # Phase 2.1a: Skip reason validation
            has_valid_skip = any(
                reason in status for reason in VALID_SKIP_REASONS
            )
            if not has_valid_skip:
                result["issues"].append(
                    f"Section {section_id} not used and has no valid skip reason "
                    f"(expected: {', '.join(VALID_SKIP_REASONS)}). "
                    f"Status: '{status.strip()}'"
                )

        # Phase 2.1c: Track for duplicate detection
        if assigned_to:
            section_assignments.setdefault(section_id, []).append(assigned_to)

    # Phase 2.1c: Duplicate coverage detection (warning only)
    for sec_id, articles in section_assignments.items():
        unique_articles = list(set(articles))
        if len(unique_articles) > 1:
            result["warnings"].append(
                f"Section {sec_id} assigned to multiple articles: "
                f"{', '.join(unique_articles)}"
            )

    # Calculate coverage percentages
    if result["stats"]["total"] > 0:
        result["coverage_percent"] = round(
            (result["stats"]["used"] / result["stats"]["total"]) * 100, 1
        )
    if result["stats"]["critical_total"] > 0:
        result["critical_coverage_percent"] = round(
            (result["stats"]["critical_used"] / result["stats"]["critical_total"])
            * 100,
            1,
        )

    # Check for issues
    if result["coverage_percent"] < 98:
        result["issues"].append(
            f"Coverage {result['coverage_percent']}% is below 98% threshold"
        )

    if result["missing_critical"]:
        result["issues"].append(
            f"Critical sections missing: {', '.join(result['missing_critical'])}"
        )

    # Also try to parse summary line if present
    # Format: - Total: 15 | Used: 14 | Missing: 1
    summary_pattern = re.compile(
        r"Total:\s*(\d+)\s*\|\s*Used:\s*(\d+)\s*\|\s*Missing:\s*(\d+)"
    )
    summary_match = summary_pattern.search(content)
    if summary_match:
        parsed_total = int(summary_match.group(1))
        parsed_used = int(summary_match.group(2))
        parsed_missing = int(summary_match.group(3))

        # Verify consistency
        if parsed_total != result["stats"]["total"]:
            result["issues"].append(
                f"Summary total ({parsed_total}) doesn't match table count ({result['stats']['total']})"
            )

    result["success"] = len(result["issues"]) == 0

    return result


def validate_word_count(
    coverage_content: str,
    target_words: int,
    tolerance: float = 0.15,
) -> Dict[str, Any]:
    """Validate word count against target with tolerance.

    Parses WORDS line from coverage report:
        WORDS: {actual} / {target} ({ratio}%)

    Args:
        coverage_content: Raw coverage file content
        target_words: Expected word count target
        tolerance: Acceptable deviation (default 0.15 = ±15%)

    Returns:
        dict with word count validation result
    """
    result: Dict[str, Any] = {
        "word_count_status": "unknown",
        "target_words": target_words,
        "actual_words": 0,
        "tolerance": tolerance,
        "tolerance_pass": False,
        "min_acceptable": int(target_words * (1 - tolerance)),
        "max_acceptable": int(target_words * (1 + tolerance)),
    }

    # Try to parse WORDS line: "WORDS: 3200 / 3000 (107%)"
    # or from table: "WORDS: 3200"
    words_pattern = re.compile(r"WORDS:\s*(\d[\d,]*)")
    match = words_pattern.search(coverage_content)

    if match:
        actual = int(match.group(1).replace(",", ""))
        result["actual_words"] = actual
        result["tolerance_pass"] = (
            result["min_acceptable"] <= actual <= result["max_acceptable"]
        )
        result["word_count_status"] = "pass" if result["tolerance_pass"] else "fail"
        result["actual_ratio"] = round(actual / target_words * 100, 1) if target_words > 0 else 0
    else:
        result["word_count_status"] = "not_found"
        result["tolerance_pass"] = False

    return result


def validate_structure_coverage(
    coverage_sections: List[str],
    structure_path: str,
) -> Dict[str, Any]:
    """Cross-reference coverage section IDs against structure.json.

    Args:
        coverage_sections: List of section IDs found in _coverage.md (e.g. ["S01", "S02"])
        structure_path: Path to structure.json file

    Returns:
        dict with cross-reference results
    """
    result: Dict[str, Any] = {
        "structure_path": structure_path,
        "structure_valid": False,
        "uncovered_in_structure": [],
        "extra_in_coverage": [],
        "issues": [],
    }

    path = Path(structure_path)
    if not path.exists():
        result["issues"].append(f"structure.json not found: {structure_path}")
        return result

    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except (json.JSONDecodeError, OSError) as e:
        result["issues"].append(f"Failed to parse structure.json: {e}")
        return result

    # Extract section IDs from structure.json outline
    # structure.json has an "outline" array with objects containing section info
    structure_sections: List[str] = []

    outline = data.get("outline", [])
    for i, entry in enumerate(outline):
        # Section IDs are typically S01, S02, etc. (1-indexed)
        section_id = f"S{i + 1:02d}"
        structure_sections.append(section_id)

    coverage_set = set(coverage_sections)
    structure_set = set(structure_sections)

    result["structure_valid"] = True
    result["structure_section_count"] = len(structure_sections)
    result["coverage_section_count"] = len(coverage_sections)

    # Sections in structure but not in coverage
    uncovered = sorted(structure_set - coverage_set)
    if uncovered:
        result["uncovered_in_structure"] = uncovered
        result["issues"].append(
            f"Sections in structure.json but not in coverage: {', '.join(uncovered)}"
        )

    # Sections in coverage but not in structure (may be valid, just flag)
    extra = sorted(coverage_set - structure_set)
    if extra:
        result["extra_in_coverage"] = extra

    return result


def validate_coverage(filepath: str, threshold: float = 98.0) -> Dict[str, Any]:
    """Validate coverage meets threshold.

    Args:
        filepath: Path to _coverage.md
        threshold: Minimum coverage percentage (default 98%)

    Returns:
        Validation result dict
    """
    result = parse_coverage_file(filepath)

    if "error" in result:
        return result

    result["threshold"] = threshold
    result["passed"] = result["coverage_percent"] >= threshold

    # Generate recommendations
    if not result["passed"]:
        result["recommendations"] = []

        if result["missing_critical"]:
            result["recommendations"].append(
                f"PRIORITY: Include critical sections {result['missing_critical']} verbatim"
            )

        if result["missing_sections"]:
            non_critical = [
                s for s in result["missing_sections"] if s not in result["missing_critical"]
            ]
            if non_critical:
                result["recommendations"].append(
                    f"Include or summarize sections: {non_critical}"
                )

        gap = threshold - result["coverage_percent"]
        sections_needed = max(1, int(gap * result["stats"]["total"] / 100))
        result["recommendations"].append(
            f"Need to cover {sections_needed} more section(s) to reach {threshold}%"
        )

    return result


def main():
    """CLI entry point."""
    if len(sys.argv) < 2 or sys.argv[1] in ("-h", "--help"):
        print(
            "Usage: python validate_coverage.py <coverage_file> [threshold] "
            "[--target-words N] [--structure path/to/structure.json]\n"
            "\n"
            "Arguments:\n"
            "  coverage_file       Path to _coverage.md file\n"
            "  threshold           Minimum coverage % (default: 98)\n"
            "\n"
            "Options:\n"
            "  --target-words N    Validate word count against target (±15% tolerance)\n"
            "  --structure PATH    Cross-reference with structure.json\n"
            "\n"
            "Exit codes:\n"
            "  0 - PASS (coverage >= threshold)\n"
            "  1 - FAIL (coverage < threshold)\n"
            "  2 - Error (parse error, file not found)"
        )
        sys.exit(2 if len(sys.argv) < 2 else 0)

    filepath = sys.argv[1]

    # Parse optional arguments
    threshold = 98.0
    target_words: Optional[int] = None
    structure_path: Optional[str] = None

    i = 2
    while i < len(sys.argv):
        arg = sys.argv[i]
        if arg == "--target-words" and i + 1 < len(sys.argv):
            target_words = int(sys.argv[i + 1])
            i += 2
        elif arg == "--structure" and i + 1 < len(sys.argv):
            structure_path = sys.argv[i + 1]
            i += 2
        else:
            # Positional: threshold
            try:
                threshold = float(arg)
            except ValueError:
                pass
            i += 1

    result = validate_coverage(filepath, threshold)

    # Optional: Word count validation
    if target_words is not None and "error" not in result:
        content = Path(filepath).read_text(encoding="utf-8")
        result["word_count"] = validate_word_count(content, target_words)

    # Optional: Structure cross-reference
    if structure_path is not None and "error" not in result:
        coverage_section_ids = [s["id"] for s in result.get("sections", [])]
        result["structure_check"] = validate_structure_coverage(
            coverage_section_ids, structure_path
        )
        # Merge structure issues into main issues
        for issue in result["structure_check"].get("issues", []):
            result["issues"].append(f"[structure] {issue}")

    print(json.dumps(result, indent=2, ensure_ascii=False))

    if "error" in result:
        sys.exit(2)
    elif result.get("passed", False):
        sys.exit(0)
    else:
        sys.exit(1)


if __name__ == "__main__":
    main()
