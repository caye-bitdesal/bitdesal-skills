#!/usr/bin/env python3
"""Merge post-commit review hook into the target project's .cursor/hooks.json."""

from __future__ import annotations

import argparse
import json
import os
import stat
from pathlib import Path

HOOK_SCRIPT = "post_git_commit_hook.py"
GITIGNORE_LINE = ".cursor/local-review/"


def merge_hooks(hooks_path: Path, hook_command: str) -> None:
    if hooks_path.is_file():
        data = json.loads(hooks_path.read_text(encoding="utf-8"))
    else:
        data = {"version": 1, "hooks": {}}

    hooks = data.setdefault("hooks", {})
    entries = hooks.setdefault("postToolUse", [])

    for entry in entries:
        if HOOK_SCRIPT in entry.get("command", ""):
            print(f"Hook already registered in {hooks_path}")
            return

    entries.append(
        {
            "command": hook_command,
            "matcher": "Shell",
        }
    )
    hooks_path.parent.mkdir(parents=True, exist_ok=True)
    hooks_path.write_text(json.dumps(data, indent=2) + "\n", encoding="utf-8")
    print(f"Updated {hooks_path}")


def ensure_gitignore(repo: Path) -> None:
    gi = repo / ".gitignore"
    lines: list[str] = []
    if gi.is_file():
        lines = gi.read_text(encoding="utf-8").splitlines()
    if any(GITIGNORE_LINE in line for line in lines):
        return
    if lines and lines[-1].strip():
        lines.append("")
    lines.append("# Local last-commit AI review state (bitdesal-review-last-commit)")
    lines.append(GITIGNORE_LINE)
    gi.write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(f"Appended {GITIGNORE_LINE} to .gitignore")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--repo", type=Path, default=Path.cwd())
    parser.add_argument(
        "--skill-root",
        type=Path,
        default=None,
        help="Path to bitdesal-review-last-commit skill directory",
    )
    args = parser.parse_args()

    repo = args.repo.resolve()
    skill_root = args.skill_root or (Path(__file__).resolve().parent.parent)
    hook_src = skill_root / "scripts" / HOOK_SCRIPT
    if not hook_src.is_file():
        raise SystemExit(f"Missing hook script: {hook_src}")

    dest_dir = repo / ".cursor" / "hooks"
    dest_dir.mkdir(parents=True, exist_ok=True)
    dest_hook = dest_dir / HOOK_SCRIPT

    content = hook_src.read_bytes()
    dest_hook.write_bytes(content)
    dest_hook.chmod(dest_hook.stat().st_mode | stat.S_IXUSR | stat.S_IXGRP | stat.S_IXOTH)

    # Copy should_auto_review.py (hook imports it)
    helper = skill_root / "scripts" / "should_auto_review.py"
    dest_helper = dest_dir / "should_auto_review.py"
    dest_helper.write_bytes(helper.read_bytes())
    dest_helper.chmod(dest_helper.stat().st_mode | stat.S_IXUSR)

    hook_command = f".cursor/hooks/{HOOK_SCRIPT}"
    merge_hooks(repo / ".cursor" / "hooks.json", hook_command)
    ensure_gitignore(repo)


if __name__ == "__main__":
    main()
