#!/usr/bin/env python3
"""Decide whether to auto-trigger last-commit review after git commit."""

from __future__ import annotations

import re
import sys

SKIP_PATTERNS = [
    re.compile(r"(?im)^WIP(\s|:|$)"),
    re.compile(r"(?i)\[skip[\s-]?review\]"),
]

EVALUATE_SUBJECT = re.compile(r"(?i)\[AI review #\d+\]")
EVALUATE_BODY = re.compile(r"(?i)Resolves AI PR review issue #\d+")


def is_evaluate_commit(message: str) -> bool:
    if EVALUATE_SUBJECT.search(message):
        return True
    if EVALUATE_BODY.search(message):
        return True
    return False


def matches_skip_pattern(message: str) -> bool:
    return any(pattern.search(message) for pattern in SKIP_PATTERNS)


def should_auto_review(commit_message: str) -> bool:
    if is_evaluate_commit(commit_message):
        return True
    if matches_skip_pattern(commit_message):
        return False
    return True


def main() -> None:
    message = sys.stdin.read() if not sys.argv[1:] else "\n".join(sys.argv[1:])
    sys.exit(0 if should_auto_review(message) else 1)


if __name__ == "__main__":
    main()
