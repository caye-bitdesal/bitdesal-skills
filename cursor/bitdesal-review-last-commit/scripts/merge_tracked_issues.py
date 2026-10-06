#!/usr/bin/env python3
"""Merge Fable review JSON with existing tracked issues for save-state."""

from __future__ import annotations

import json
import re
import sys

ID_PATTERN = re.compile(r"^L(\d+)$")


def next_id(existing: list[dict]) -> str:
    max_n = 0
    for item in existing:
        match = ID_PATTERN.match(str(item.get("id", "")))
        if match:
            max_n = max(max_n, int(match.group(1)))
    return f"L{max_n + 1}"


def main() -> None:
    data = json.load(sys.stdin)
    prior: list[dict] = (
        data.get("tracked_issues")
        or data.get("open_tracked_issues")
        or data.get("prior_tracked")
        or []
    )
    review: dict = data["review"]

    by_id = {item["id"]: dict(item) for item in prior if item.get("id")}

    for update in review.get("tracked_issue_updates", []):
        iid = update.get("id")
        status = update.get("status", "still_open")
        if iid in by_id:
            by_id[iid]["status"] = status

    all_tracked = list(by_id.values())

    for issue in review.get("issues", []):
        iid = next_id(all_tracked)
        all_tracked.append(
            {
                "id": iid,
                "status": "open",
                "file": issue.get("file"),
                "line": issue.get("line"),
                "severity": issue.get("severity"),
                "category": issue.get("category"),
                "title": issue.get("title"),
            }
        )
        issue["local_id"] = iid

    still_open = [
        {
            "id": item["id"],
            "title": item.get("title"),
            "summary": item.get("title"),
        }
        for item in all_tracked
        if item.get("status") == "open"
    ]
    review["still_open"] = still_open

    json.dump({"tracked_issues": all_tracked, "review": review}, sys.stdout, indent=2)
    sys.stdout.write("\n")


if __name__ == "__main__":
    main()
