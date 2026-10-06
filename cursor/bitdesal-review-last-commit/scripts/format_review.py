#!/usr/bin/env python3
"""Format KMP review JSON as markdown (aligned with ai_review-kmp.py)."""

from __future__ import annotations

import json
import sys

SEVERITY_LABEL = {
    "error": "[error]",
    "warning": "[warning]",
    "suggestion": "[suggestion]",
}
CATEGORY_LABEL = {
    "bug": "Bug",
    "platform_correctness": "Platform Correctness",
    "understandability": "Understandability",
    "reusability": "Reusability",
}


def format_review_body(review: dict, project_name: str, head_short: str) -> str:
    lines = [
        f"## Local code review — {project_name} (`{head_short}`)\n",
        review.get("summary", ""),
        "",
    ]

    issues = review.get("issues", [])
    if issues:
        lines.append("---\n### New in this commit\n")
        for issue in issues:
            severity = SEVERITY_LABEL.get(issue.get("severity"), "[info]")
            category = CATEGORY_LABEL.get(issue.get("category"), issue.get("category", ""))
            location = f"`{issue['file']}`"
            if issue.get("line"):
                location += f" line {issue['line']}"
            lines.append(f"#### {severity} {issue.get('title', 'Issue')}")
            lines.append(f"**Category:** {category} | **Location:** {location}\n")
            lines.append(f"{issue.get('body', '')}\n")

    still_open = review.get("still_open", [])
    if still_open:
        lines.append("---\n### Still open on this branch\n")
        for item in still_open:
            iid = item.get("id", "?")
            lines.append(f"- **{iid}** — {item.get('title', item.get('summary', ''))}")
        lines.append("")

    questions = review.get("open_questions", [])
    if questions:
        lines.append("---\n### Open questions\n")
        for question in questions:
            lines.append(f"- {question}")
        lines.append("")

    addressed = review.get("addressed_comments", [])
    if addressed:
        lines.append("---\n### Addressed since last review\n")
        for item in addressed:
            lines.append(f"- {item}")
        lines.append("")

    praise = review.get("praise", [])
    if praise:
        lines.append("---\n### Well done\n")
        for item in praise:
            lines.append(f"- {item}")
        lines.append("")

    verdict = review.get("verdict", "comment")
    lines.append(f"**Verdict:** `{verdict}`")
    lines.append(
        "\n---\n*Local last-commit review (Claude Fable). CI PR review still applies after push.*"
    )
    return "\n".join(lines)


def main() -> None:
    data = json.load(sys.stdin)
    review = data["review"]
    project = data.get("project_name", "project")
    head_short = data.get("head_short", "HEAD")
    print(format_review_body(review, project, head_short))


if __name__ == "__main__":
    main()
