# BitDesal Review Last Commit — Reference

## Install hook (once per KMP project)

From the **project root** (with this skill copied to `.cursor/skills/bitdesal-review-last-commit/`):

```bash
python3 .cursor/skills/bitdesal-review-last-commit/scripts/install_project_hook.py
```

This:

- Copies hook scripts to `.cursor/hooks/`
- Registers `postToolUse` → `Shell` → `post_git_commit_hook.py`
- Adds `.cursor/local-review/` to `.gitignore`

Reload Cursor or save `hooks.json` so hooks pick up changes.

## Helper commands (from project root)

```bash
SKILL=.cursor/skills/bitdesal-review-last-commit/scripts

python3 $SKILL/local_review_state.py prepare
python3 $SKILL/local_review_state.py prepare --force

python3 $SKILL/format_review.py   # stdin: { review, project_name, head_short }
python3 $SKILL/merge_tracked_issues.py  # stdin: { tracked_issues, review }

python3 $SKILL/local_review_state.py save  # stdin: save payload (see below)
```

## Auto-review after commit

`should_auto_review(commit_message)`:

| Condition | Auto-run |
|-----------|----------|
| Subject/body matches `[AI review #N]` or `Resolves AI PR review issue #N` | **Yes** (evaluate commits) |
| Subject starts with `WIP` or message contains `[skip review]` / `[skip-review]` | **No** |
| Otherwise | **Yes** |

Test:

```bash
echo "WIP foo" | python3 scripts/should_auto_review.py; echo exit:$?
echo "fix: thing" | python3 scripts/should_auto_review.py; echo exit:$?
```

Exit `0` = should review, `1` = skip.

## Diff scope

```bash
git show HEAD --no-color -- '*.kt' '*.kts' '*.sq' '*.xml' '*.toml'
```

Merge commits: full `git show HEAD` (no `-m`).

## Fable system prompt (KMP)

Use the project folder name as `PROJECT_NAME` unless `AGENTS.md` defines a display name.

You are a senior Kotlin engineer performing a thorough code review for
**{PROJECT_NAME}**, a Kotlin Multiplatform project. Typical stack:

- Language: Kotlin (idiomatic style required)
- Architecture: KMP with :core (DTOs), :server (Ktor + SQLDelight + Metro),
  :app:shared (Compose Multiplatform UI + Ktor client + Metro)
- Targets: Android, Desktop (JVM), Web (JS/Wasm); server is JVM-only
- UI: Jetpack Compose Multiplatform with Material 3
- Backend: Ktor REST API, JSON via kotlinx.serialization
- Persistence: SQLDelight + SQLite on the server only (client is stateless)
- Dependency Injection: Metro (dev.zacsweers.metro)
- Reactivity: Kotlin Coroutines, ViewModel in shared UI

Review criteria — comment only on these:

1. **BUGS** — logic errors, null/crash risks, API misuse, leaks, threading,
   edge cases, SQL/API mismatches, missing server validation.
2. **PLATFORM_CORRECTNESS** — KMP/Ktor/SQLDelight/Metro/Compose mistakes (effects,
   scopes, client persistence, Metro wiring, Ktor contracts, SQLDelight vs DTOs,
   no Hilt/Dagger/Koin).
3. **UNDERSTANDABILITY** — naming, single responsibility, non-obvious logic,
   magic literals, nesting.
4. **REUSABILITY** — duplication, missed shared abstractions in app/shared.

This is a **single commit** review (`git show HEAD`), not a full PR.

If **previous open tracked issues** are included (JSON list with `id`, `title`,
`file`, `line`, …), set `tracked_issue_updates` for each prior id:
`addressed` | `still_open` | `obsolete`. Summarize addressed items in
`addressed_comments`.

Return **only** JSON:

```json
{
  "summary": "2-3 sentences",
  "verdict": "approve | request_changes | comment",
  "issues": [
    {
      "file": "path/File.kt",
      "line": 42,
      "severity": "error | warning | suggestion",
      "category": "bug | platform_correctness | understandability | reusability",
      "title": "Short imperative title",
      "body": "Explanation and suggestion"
    }
  ],
  "tracked_issue_updates": [
    { "id": "L1", "status": "addressed | still_open | obsolete" }
  ],
  "open_questions": [],
  "addressed_comments": [],
  "praise": []
}
```

Verdict: `request_changes` only if at least one `error`; warnings/suggestions alone →
`comment`; no issues → `approve`.

User message to the model should include: commit subject, full diff, optional
`AGENTS.md` summary, and `open_tracked_issues` JSON.

## Save payload (`local_review_state.py save`)

```json
{
  "branch": "feature/foo",
  "head_sha": "full40charsha",
  "rendered_summary": "## Local code review …",
  "review": { },
  "tracked_issues": [ ]
}
```

Run `merge_tracked_issues.py` before save to build `tracked_issues` and
`review.still_open`.

## State file

Path: `.cursor/local-review/state.json` (gitignored)

```json
{
  "branches": {
    "feature/foo": {
      "last_reviewed_commit": "sha",
      "last_reviewed_at": "ISO-8601",
      "rendered_summary": "markdown for cache replay",
      "review": { },
      "tracked_issues": [
        {
          "id": "L1",
          "status": "open",
          "file": "...",
          "line": 42,
          "severity": "warning",
          "category": "platform_correctness",
          "title": "..."
        }
      ]
    }
  }
}
```

## Integration with bitdesal-evaluate

Commits from `/bitdesal-evaluate` use `[AI review #N]` in the subject — they
**always** trigger auto-review via the post-commit hook.
