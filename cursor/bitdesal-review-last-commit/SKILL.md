---
name: bitdesal-review-last-commit
description: >-
  Reviews the latest git commit on Kotlin Multiplatform projects (Kotlin, Gradle,
  SQLDelight, config) using Claude Fable; tracks open findings per branch across
  commits. Runs on /bitdesal-review-last-commit or automatically after git commit
  (except WIP or [skip review]; always for bitdesal-evaluate commits). Chat output
  only; replays cached report for the same commit unless --force.
disable-model-invocation: true
---

# BitDesal Review Last Commit

Review **only the tip commit** (`git show HEAD`, filtered extensions). Output goes
**in chat only**. Persist state under `.cursor/local-review/state.json`.

Pair with CI PR review (`bitdesal-create-ci`) and triage fixes (`bitdesal-evaluate`).

## Invocation

```text
/bitdesal-review-last-commit
/bitdesal-review-last-commit --force
```

Optional repo path on the same line if the KMP project is not the workspace root.

## One-time project setup

From the **KMP project root**:

```bash
python3 .cursor/skills/bitdesal-review-last-commit/scripts/install_project_hook.py
```

See [reference.md](reference.md) for hook behavior and skip rules.

## Workflow checklist

```text
Review progress:
- [ ] Step 1: Resolve repo root
- [ ] Step 2: prepare (cache / diff / open issues)
- [ ] Step 3: Cache hit → post cached summary and stop
- [ ] Step 4: Empty diff → stop
- [ ] Step 5: Fable review (Task subagent)
- [ ] Step 6: merge tracked issues, format, save, post in chat
```

### Step 1: Resolve repo root

Use the path the user gave, or find the git root (`git rev-parse --show-toplevel`).

Set:

```bash
SKILL_SCRIPTS=.cursor/skills/bitdesal-review-last-commit/scripts
```

If the skill lives elsewhere, use the absolute path to `scripts/`.

### Step 2: Prepare

```bash
python3 "$SKILL_SCRIPTS/local_review_state.py" prepare [--force] --repo /path/to/repo
```

Parse JSON. Respect `--force` from the user message.

### Step 3: Cached report

If `cached` is true and the user did not pass `--force`:

- Post `rendered_summary` in chat.
- Add one line: cached review for `head_short`; use `--force` to re-run Fable.
- **Stop** — no commit, no file artifacts beyond existing state.

### Step 4: Empty diff

If `diff_empty` is true:

- Say no reviewable files in the last commit (filtered globs).
- **Stop**.

### Step 5: Fable review

Launch **one** Task subagent:

- `subagent_type`: `generalPurpose`
- `model`: `claude-fable-5-1-thinking-high`
- `run_in_background`: `false`

Prompt must include:

- System rubric and JSON schema from [reference.md](reference.md) (`PROJECT_NAME` = `project_name` from prepare)
- Commit subject and full `diff`
- `open_tracked_issues` from prepare (may be `[]`)
- Instruction: read `AGENTS.md` at repo root when present; return **only** valid JSON

If the subagent returns fenced JSON, strip fences before parsing.

### Step 6: Merge, format, save, deliver

1. Pipe to merge:

   ```bash
   python3 "$SKILL_SCRIPTS/merge_tracked_issues.py"
   ```

   Stdin: `{ "tracked_issues": [...], "review": { ... parsed ... } }` (use
   `tracked_issues` from prepare; falls back to open-only list if empty)

2. Format markdown:

   ```bash
   python3 "$SKILL_SCRIPTS/format_review.py"
   ```

   Stdin: `{ "review": merged.review, "project_name": "...", "head_short": "..." }`

3. Save:

   ```bash
   python3 "$SKILL_SCRIPTS/local_review_state.py" save --repo /path/to/repo
   ```

   Stdin:

   ```json
   {
     "branch": "<from prepare>",
     "head_sha": "<from prepare>",
     "rendered_summary": "<markdown from format_review>",
     "review": "<merged review object>",
     "tracked_issues": "<merged tracked_issues>"
   }
   ```

4. Post `rendered_summary` in chat. Do **not** commit or push unless the user asks.

## Auto-trigger (hook)

When `post_git_commit_hook.py` runs after a successful agent `git commit`, it
injects context to run this skill. Follow the same checklist starting at Step 2
(do not skip because the user did not type the slash command).

Skip auto-review when the commit message is WIP / `[skip review]` — unless it is
an evaluate commit (`[AI review #N]`). Details in [reference.md](reference.md).

## Output goal

The user gets a structured review in chat:

- New issues in the last commit (four categories)
- Still open on this branch
- Addressed since last review
- Verdict, questions, praise

Repeat invocation on the **same commit** shows the **cached** report.

## Notes

- Do not write review output to files except `state.json` via `save`.
- Do not fix code unless the user asks separately.
- For PR bot findings after push, use `bitdesal-evaluate`.
