#!/usr/bin/env python3
"""
Cursor hook: after a successful git commit, ask the agent to run last-commit review.

Works with postToolUse (Shell) — returns additional_context JSON on stdout.
"""

from __future__ import annotations

import json
import re
import subprocess
import sys
from pathlib import Path

# Import sibling module without package layout
SCRIPT_DIR = Path(__file__).resolve().parent
sys.path.insert(0, str(SCRIPT_DIR))
from should_auto_review import should_auto_review  # noqa: E402

GIT_COMMIT = re.compile(r"\bgit\b.*\bcommit\b", re.IGNORECASE)


def extract_fields(payload: dict) -> tuple[str, int | None, str | None]:
    command = (
        payload.get("command")
        or payload.get("tool_input", {}).get("command")
        or payload.get("toolInput", {}).get("command")
        or ""
    )
    exit_code = payload.get("exitCode")
    if exit_code is None:
        exit_code = payload.get("exit_code")
    if exit_code is None:
        exit_code = payload.get("result", {}).get("exitCode")
    cwd = payload.get("cwd") or payload.get("workspace_roots", [None])[0]
    if isinstance(cwd, list):
        cwd = cwd[0] if cwd else None
    return str(command), exit_code, cwd


def last_commit_message(repo: Path) -> str:
    subject = subprocess.run(
        ["git", "-C", str(repo), "log", "-1", "--format=%s"],
        capture_output=True,
        text=True,
        check=False,
    )
    body = subprocess.run(
        ["git", "-C", str(repo), "log", "-1", "--format=%b"],
        capture_output=True,
        text=True,
        check=False,
    )
    subj = (subject.stdout or "").strip()
    bod = (body.stdout or "").strip()
    if bod:
        return f"{subj}\n\n{bod}"
    return subj


def main() -> None:
    raw = sys.stdin.read()
    if not raw.strip():
        sys.exit(0)

    try:
        payload = json.loads(raw)
    except json.JSONDecodeError:
        sys.exit(0)

    command, exit_code, cwd = extract_fields(payload)
    if not GIT_COMMIT.search(command):
        sys.exit(0)
    if exit_code not in (0, "0", None):
        # If exit code missing, still try (some hook payloads omit it on success)
        if exit_code is not None:
            sys.exit(0)

    repo = Path(cwd or ".").resolve()
    if not (repo / ".git").exists():
        sys.exit(0)

    message = last_commit_message(repo)
    if not should_auto_review(message):
        sys.exit(0)

    short = subprocess.run(
        ["git", "-C", str(repo), "rev-parse", "--short", "HEAD"],
        capture_output=True,
        text=True,
        check=False,
    ).stdout.strip()

    context = (
        f"A `git commit` just succeeded in `{repo}` at `{short}`. "
        "Run the **bitdesal-review-last-commit** skill now (`/bitdesal-review-last-commit`). "
        "Post the review in chat only; do not create commits."
    )
    print(json.dumps({"additional_context": context}))


if __name__ == "__main__":
    main()
