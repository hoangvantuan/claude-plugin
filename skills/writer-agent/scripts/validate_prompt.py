#!/usr/bin/env python3
"""Validate template variables in writer-agent subagent prompts.

Usage:
    python validate_prompt.py --tier <1|2|3> --prompt-file <path>
    python validate_prompt.py --tier 3 --prompt-file /tmp/prompt.txt
    echo "prompt text" | python validate_prompt.py --tier 1 --stdin

Output: JSON with validation result

Exit codes:
    0 - All required variables present (PASS)
    1 - Missing variables (FAIL)
    2 - Usage error
"""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any, Dict, List

# Required variables for ALL tiers
REQUIRED_ALL = [
    "{title}",
    "{style}",
    "{outputPath}",
    "{seriesList}",
    "{target_words}",
    "{detail_level}",
]

# Additional required variables per tier
REQUIRED_TIER = {
    1: {
        "all": ["{sourcePath}", "{start}", "{end}", "{inlineGlossary}"],
    },
    2: {
        "one_of": ["{contextFilePath}", "{sourcePath}"],
    },
    3: {
        "all": ["{sourcePath}", "{start}", "{end}", "{inlineGlossary}"],
    },
}


def validate_prompt(prompt_text: str, tier: int) -> Dict[str, Any]:
    """Validate that prompt contains all required template variables.

    Args:
        prompt_text: The prompt string to validate
        tier: Document tier (1, 2, or 3)

    Returns:
        dict with validation result
    """
    result: Dict[str, Any] = {
        "passed": True,
        "tier": tier,
        "missing": [],
        "warnings": [],
    }

    # Check common required variables
    for var in REQUIRED_ALL:
        if var not in prompt_text:
            result["missing"].append(var)

    # Check tier-specific variables
    tier_reqs = REQUIRED_TIER.get(tier, {})

    if "all" in tier_reqs:
        for var in tier_reqs["all"]:
            if var not in prompt_text:
                result["missing"].append(var)

    if "one_of" in tier_reqs:
        found = any(var in prompt_text for var in tier_reqs["one_of"])
        if not found:
            result["missing"].append(
                f"one of {tier_reqs['one_of']}"
            )

    result["passed"] = len(result["missing"]) == 0
    return result


def main() -> None:
    """CLI entry point."""
    parser = argparse.ArgumentParser(
        description="Validate writer-agent subagent prompt template variables"
    )
    parser.add_argument(
        "--tier",
        type=int,
        choices=[1, 2, 3],
        required=True,
        help="Document tier (1, 2, or 3)",
    )
    parser.add_argument(
        "--prompt-file",
        type=str,
        help="Path to file containing the prompt text",
    )
    parser.add_argument(
        "--stdin",
        action="store_true",
        help="Read prompt from stdin",
    )

    args = parser.parse_args()

    # Read prompt text
    if args.stdin:
        prompt_text = sys.stdin.read()
    elif args.prompt_file:
        path = Path(args.prompt_file)
        if not path.exists():
            print(
                json.dumps(
                    {"passed": False, "error": f"File not found: {args.prompt_file}"},
                    indent=2,
                )
            )
            sys.exit(2)
        prompt_text = path.read_text(encoding="utf-8")
    else:
        print(
            json.dumps(
                {"passed": False, "error": "Provide --prompt-file or --stdin"},
                indent=2,
            )
        )
        sys.exit(2)

    result = validate_prompt(prompt_text, args.tier)
    print(json.dumps(result, indent=2, ensure_ascii=False))

    sys.exit(0 if result["passed"] else 1)


if __name__ == "__main__":
    main()
