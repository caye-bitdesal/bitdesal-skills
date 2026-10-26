# bitdesal-create-kmp-spec

Turn a rough KMP feature idea into a detailed, agent-ready spec through an
interview (client scope first), then generate structured artifacts you can feed
to an AI agent for incremental implementation across `:core`, `:server`, and
`:app:shared`.

## What it does

1. **Asks which clients** the feature includes (server, Android, desktop, web,
   iOS — including desktop-only and iOS-only).
2. **Interviews you** like a junior developer — screenshots, existing DTOs /
   routes / Composables, API contract, layout, behavior.
3. **Builds a full spec** — modules, auth, endpoints with `consumed_by`,
   reuse/modify/create decisions, shared Compose UI in `commonMain`.
4. **Splits the work into tasks** tagged with `target`, `module`, and
   `clients_affected`.
5. **Generates artifacts** under `specs/<feature-slug>/`:
   - `spec.json` — structured spec for AI agents (primary)
   - `spec.html` — self-contained human-readable spec with embedded images
   - `images/` — reference screenshots and mockups

## Default project (Tabala-shaped)

| Module | Role |
|--------|------|
| `:core` | Shared DTOs |
| `:server` | Ktor + SQLite + Flyway + Firebase auth |
| `:app:shared` | Compose Multiplatform UI, ViewModels, repos |
| `:app:androidApp` / `:app:desktopApp` / `:app:webApp` / `:app:iosApp` | Thin hosts |

New screens go in `:app:shared` `commonMain`. **All clients** means Android,
desktop, web, **and iOS** (Compose Multiplatform). Public Astro / other sites
are external API consumers, not in-repo UI.

## Prerequisites

- Cursor project skill at `.cursor/skills/bitdesal-create-kmp-spec/`
- Python 3 (standard library only)

## How to invoke

```text
/bitdesal-create-kmp-spec I want an event attendance screen for editors
```

If you omit the description, the agent still starts with **client scope**, then
asks for a one-paragraph summary.

### Example prompts

**Server + all Compose clients**

```text
/bitdesal-create-kmp-spec Event attendance list with toggle. Server plus all clients.
```

**Server only**

```text
/bitdesal-create-kmp-spec Public GET for upcoming events. No in-repo UI.
```

**Desktop only**

```text
/bitdesal-create-kmp-spec Offline-looking inventory browser for the workshop PC.
Uses existing API; no new tables.
```

## Interview flow

1. Client scope (blocking) — presets including desktop-only and iOS-only
2. Assets and base facts (filtered by enabled clients)
3. Analyze screenshots (skipped for server-only)
4. Inventory existing types, routes, UI
5. API and data contract
6. Macro structure (UI clients)
7. Sections and details
8. Behavior, data, edge cases
9. Confirm completeness
10. Incremental tasks
11. Generate `spec.json` and `spec.html`

## Output layout

```text
specs/
└── <feature-slug>/
    ├── spec.json
    ├── spec.html
    └── images/
```

## Using the spec in a new chat

Attach the JSON — not the HTML.

| File | Use |
|------|-----|
| `spec.json` | **Always** — primary source for the agent |
| `images/*.png` | When UI/layout parity matters |
| `spec.html` | Human review only |

```text
Implement task T2 from @specs/event-attendance/spec.json
Follow the module, client_scope, and acceptance criteria in the spec.
```

## Regenerating the HTML

From the **project** repository root:

```bash
python3 .cursor/skills/bitdesal-create-kmp-spec/scripts/generate_spec_html.py \
  --spec specs/<feature-slug>/spec.json \
  --out specs/<feature-slug>/spec.html
```

## Related

- `bitdesal-create-spec` — same interview style, Android-only UI assumptions
- `bitdesal-kmp-use-case-spec` — reverse-engineer existing KMP code, gaps, tests
