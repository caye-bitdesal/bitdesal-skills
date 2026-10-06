#!/usr/bin/env python3
"""Load/save local last-commit review state under .cursor/local-review/."""

from __future__ import annotations

import argparse
import json
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path

REVIEWED_GLOBS = ("*.kt", "*.kts", "*.sq", "*.xml", "*.toml")
MAX_DIFF_CHARS = 90_000
STATE_DIR = Path(".cursor/local-review")
STATE_FILE = STATE_DIR / "state.json"


def run_git(repo: Path, *args: str) -> str:
    result = subprocess.run(
        ["git", "-C", str(repo), *args],
        capture_output=True,
        text=True,
        check=False,
    )
    if result.returncode != 0:
        raise RuntimeError(result.stderr.strip() or f"git failed: {' '.join(args)}")
    return result.stdout


def git_show_diff(repo: Path) -> str:
    paths = " ".join(f"'{g}'" for g in REVIEWED_GLOBS)
    result = subprocess.run(
        f"git -C {repo} show HEAD --no-color -- {paths}",
        shell=True,
        capture_output=True,
        text=True,
        check=False,
    )
    diff = result.stdout
    if len(diff) > MAX_DIFF_CHARS:
        diff = diff[:MAX_DIFF_CHARS] + "\n\n[diff truncated: exceeds size limit]"
    return diff


def load_state(repo: Path) -> dict:
    path = repo / STATE_FILE
    if not path.is_file():
        return {"branches": {}}
    return json.loads(path.read_text(encoding="utf-8"))


def save_state(repo: Path, state: dict) -> None:
    path = repo / STATE_FILE
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(state, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")


def branch_entry(state: dict, branch: str) -> dict:
    branches = state.setdefault("branches", {})
    return branches.setdefault(
        branch,
        {
            "last_reviewed_commit": None,
            "last_reviewed_at": None,
            "rendered_summary": None,
            "review": None,
            "tracked_issues": [],
        },
    )


def cmd_prepare(repo: Path, force: bool) -> None:
    branch = run_git(repo, "branch", "--show-current").strip()
    head = run_git(repo, "rev-parse", "HEAD").strip()
    short = run_git(repo, "rev-parse", "--short", "HEAD").strip()
    subject = run_git(repo, "log", "-1", "--format=%s").strip()
    body = run_git(repo, "log", "-1", "--format=%b").strip()
    message = subject if not body else f"{subject}\n\n{body}"

    state = load_state(repo)
    entry = branch_entry(state, branch)
    cached = (
        not force
        and entry.get("last_reviewed_commit") == head
        and entry.get("rendered_summary")
    )

    diff = git_show_diff(repo)
    diff_empty = not diff.strip()

    tracked = entry.get("tracked_issues") or []
    open_issues = [i for i in tracked if i.get("status", "open") == "open"]

    out = {
        "repo": str(repo.resolve()),
        "branch": branch,
        "head_sha": head,
        "head_short": short,
        "commit_subject": subject,
        "commit_message": message,
        "diff": diff,
        "diff_empty": diff_empty,
        "cached": cached,
        "rendered_summary": entry.get("rendered_summary") if cached else None,
        "open_tracked_issues": open_issues,
        "tracked_issues": tracked,
        "project_name": repo.name,
    }
    json.dump(out, sys.stdout, ensure_ascii=False, indent=2)
    sys.stdout.write("\n")


def cmd_save(repo: Path) -> None:
    payload = json.load(sys.stdin)
    branch = payload["branch"]
    head = payload["head_sha"]
    rendered = payload["rendered_summary"]
    review = payload["review"]
    tracked = payload.get("tracked_issues", [])

    state = load_state(repo)
    entry = branch_entry(state, branch)
    entry["last_reviewed_commit"] = head
    entry["last_reviewed_at"] = datetime.now(timezone.utc).isoformat()
    entry["rendered_summary"] = rendered
    entry["review"] = review
    entry["tracked_issues"] = tracked
    save_state(repo, state)


def main() -> None:
    parser = argparse.ArgumentParser(description="Local last-commit review state")
    parser.add_argument("--repo", type=Path, default=Path.cwd())
    sub = parser.add_subparsers(dest="cmd", required=True)

    prep = sub.add_parser("prepare", help="Git context + cache flag for review")
    prep.add_argument("--force", action="store_true")

    sub.add_parser("save", help="Persist review JSON from stdin")

    args = parser.parse_args()
    repo = args.repo.resolve()

    if args.cmd == "prepare":
        cmd_prepare(repo, args.force)
    elif args.cmd == "save":
        cmd_save(repo)


if __name__ == "__main__":
    main()
