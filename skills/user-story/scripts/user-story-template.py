#!/usr/bin/env python3
"""Generate a deterministic user story Markdown stub.

No network access. Prints to stdout unless --output is provided.
"""

from __future__ import annotations

import argparse
from pathlib import Path


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Generate a user story with persona, problem, and Gherkin criteria.",
    )
    parser.add_argument("--story-id", default="[ID]", help="Story id.")
    parser.add_argument("--summary", help="Short value-focused title.")
    parser.add_argument("--persona", help='Persona or role for "As a".')
    parser.add_argument("--problem", help="User-centered problem statement.")
    parser.add_argument("--action", help='Action for "I want to".')
    parser.add_argument("--outcome", help='Outcome for "so that".')
    parser.add_argument("--assumption", action="append", default=[], help="Assumption, repeatable.")
    parser.add_argument("--scenario", help="Scenario description.")
    parser.add_argument("--given", action="append", default=[], help="Given precondition, repeatable.")
    parser.add_argument("--when", dest="when_text", help="When trigger.")
    parser.add_argument("--then", dest="then_text", help="Then outcome.")
    parser.add_argument("--open-question", action="append", default=[], help="Open question, repeatable.")
    parser.add_argument("--split-needed", choices=["Yes", "No", "Unknown"], default="Unknown")
    parser.add_argument("--output", help="Write Markdown to this file instead of stdout.")
    return parser.parse_args()


def value(text: str | None, placeholder: str) -> str:
    if text and text.strip():
        return text.strip()
    return placeholder


def bullet_lines(items: list[str], placeholder: str, indent: str = "") -> list[str]:
    values = [item.strip() for item in items if item.strip()]
    if not values:
        values = [placeholder]
    return [f"{indent}- {item}" for item in values]


def render(args: argparse.Namespace) -> str:
    story_id = value(args.story_id, "[ID]")
    summary = value(args.summary, "[Brief, memorable title focused on user value]")
    persona = value(args.persona, "[specific persona or role]")
    problem = value(
        args.problem,
        "[Persona] needs a way to [desired outcome] because [root cause], which currently [impact].",
    )
    action = value(args.action, "[action the user takes]")
    outcome = value(args.outcome, "[desired user outcome]")
    scenario = value(args.scenario, "[Brief, human-readable scenario]")
    when_text = value(args.when_text, "[Event that triggers the action]")
    then_text = value(args.then_text, "[Expected observable outcome]")

    givens = [item.strip() for item in args.given if item.strip()]
    if not givens:
        givens = ["[Initial context or precondition]"]

    lines: list[str] = [
        "## User Story",
        "",
        "### Context",
        f"- **Persona:** {persona}",
        f"- **Problem:** {problem}",
        "- **Assumptions:**",
        *bullet_lines(args.assumption, "[Assumption to validate]", "  "),
        "",
        f"### Story {story_id}",
        f"- **Summary:** {summary}",
        f"- **As a** {persona}",
        f"- **I want to** {action}",
        f"- **so that** {outcome}",
        "",
        "### Acceptance Criteria",
        f"- **Scenario:** {scenario}",
    ]

    for index, given in enumerate(givens):
        label = "Given" if index == 0 else "And Given"
        lines.append(f"- **{label}:** {given}")

    lines.extend(
        [
            f"- **When:** {when_text}",
            f"- **Then:** {then_text}",
            "",
            "### Quality Check",
            "- **INVEST:** [Independent, Negotiable, Valuable, Estimable, Small, Testable]",
            f"- **Split needed:** {args.split_needed}",
            "- **Open questions:**",
            *bullet_lines(args.open_question, "[Question to resolve before delivery]", "  "),
            "",
        ]
    )
    return "\n".join(lines)


def main() -> int:
    args = parse_args()
    content = render(args)
    if args.output:
        Path(args.output).write_text(content, encoding="utf-8")
    else:
        print(content)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
