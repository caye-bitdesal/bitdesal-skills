# BitDesal Create KMP Spec — Reference

Read this when running the interview or before generating the artifact.

## Interview Principles

- Client scope first. Do not ask about a disabled client later.
- One topic at a time. Resolve the current layer before going deeper.
- Always propose a concrete implementation and an example answer.
- Restate what you understood from images before asking how to build it.
- Track open questions; do not move on while a blocking one is unanswered.
- Big picture first, then details, then states and edge cases.

## Client scope presets

Ask the user to pick one (or custom). Map to JSON flags.

| Preset id | Label | server | android | desktop | web | ios |
|-----------|-------|--------|---------|---------|-----|-----|
| `server_only` | Server only | ✓ | | | | |
| `server_all_compose` | Server + all clients (Android, desktop, web, iOS) | ✓ | ✓ | ✓ | ✓ | ✓ |
| `server_android` | Server + Android | ✓ | ✓ | | | |
| `server_desktop` | Server + desktop | ✓ | | ✓ | | |
| `server_web` | Server + web | ✓ | | | ✓ | |
| `server_ios` | Server + iOS | ✓ | | | | ✓ |
| `android_only` | Android only | | ✓ | | | |
| `desktop_only` | Desktop only | | | ✓ | | |
| `web_only` | Web only | | | | ✓ | |
| `ios_only` | iOS only | | | | | ✓ |
| `custom` | Any mix the user states | user-defined | | | | |

Also store `external_public_api` (boolean). That is **not** the same as `web`
(`:app:webApp`). Astro / other out-of-repo sites are `external_systems`.

**All clients** = Compose Multiplatform on Android, desktop, web, **and iOS**.

### Scope gates

| If… | Then… |
|-----|--------|
| `server` is false | No Flyway/route/SQLDelight tasks. Document existing endpoints only. If the user describes new tables, re-scope. |
| No UI client is true | Skip screenshot, macro, and section UI interviews. Tasks stay in `:core` / `:server`. |
| A UI client is true | Shared screens in `:app:shared` `commonMain`. Thin app-module tasks only for bootstrap/expect-actual. |
| `ios` is true and no `:app:iosApp` | Keep iOS in scope; add a thin-shell / `iosMain` task. Do not assume SwiftUI. |
| `external_public_api` | Document public routes + RGPD; optional `target: external-doc` task. No Gradle UI work. |

## Question Bank

### Round 1 — Client scope (blocking)

- Which clients does this feature target? (read the preset menu)
- Custom mix? (example answer: "server + Android + desktop, no web, no iOS")
- External public API consumer (Astro or similar)? yes/no
- If iOS is included: is there already an `:app:iosApp` module?

### Round 2 — Assets and base facts

Ask only for enabled clients.

- Screenshots of how the feature looks on each enabled UI client (Android,
  desktop, web, iOS). iOS shots are useful as parity even when Compose is shared.
- Mockups if they exist.
- What should the parent package be named (under `:app:shared`)?
- Feature slug (hyphenated) if not obvious.
- Describe the general behavior of the feature.
- Navigation route name / shared scaffold (if any UI client).
- Is this feature using any endpoint? List them. New or existing?
- Does the data model change (`data-model.json`, new Flyway version)?
- Auth: Firebase ID token (management) vs public route vs both?
- File uploads under `files/`?

### Round 3 — Existing artifacts

Run before designing UI or new routes. For each candidate: reuse, modify, or
create new?

- Found `X` in `:core` / `:server` / `:app:shared`. Reuse, modify, or build new?
- If modify: what exactly should change?
- If create new: name, module, source set, path.
- Are there design-system widgets (buttons, cards, dialogs) to enforce?

#### How to search

Adjust paths if the repo is not Tabala-shaped.

- `:core` — `**/core/**/*.kt`, `@Serializable`, enums.
- `:server` — `**/server/**/*.kt`, `routing {`, `get(`, `post(`,
  `**/*.sqm`, `**/sqldelight/**`.
- Shared UI — `@Composable`, `**/*Screen*.kt`, `**/*ViewModel*.kt`,
  `**/app/shared/**`.
- Repos — `**/*Repository*.kt`, `HttpClient`, Ktor Client.
- Koin — `module {`, `**/*Module*.kt`.
- Thin apps — `**/androidApp/**`, `**/desktopApp/**`, `**/webApp/**`,
  `**/iosApp/**` only when bootstrap might change.
- Skip `build/`, `.gradle/`, `node_modules/`.

Confirm signatures by reading the file before proposing reuse or modification.

### Round 4 — Macro structure (UI only)

- How many main sections does the screen have, and how are they divided?
- How should the top-level layout be implemented? (example: "two boxes inside
  a Column, each with weight(1f)")
- Shared scaffold, top bar, bottom bar, FAB?
- Scrollable as a whole, or per section?
- Any desktop window / web viewport / iOS safe-area constraints?

### Round 5 — Sections and details

- For section X, what does it contain?
- How are items arranged (list, grid, row, pager)?
- What does a single item look like, and which existing component does it reuse?
- Spacing, alignment, sizing that matter?
- Same Compose on all enabled clients, or a documented platform delta?

### Round 6 — Behavior, data, edge cases

- Tap / long press / keyboard / swipe for each interactive element.
- Navigation from here, and what is passed along.
- Loading, empty, and error states.
- How each endpoint maps to the ViewModel. When is it called?
- Persistence: server SQLite is source of truth unless user overrides.
- Validation and edge cases the mockups do not show.
- 401 / role denied / double-submit / empty list.

## Task Breakdown Guidance

Smallest tasks that still produce a reviewable result. Drop rows whose
`client_scope` / module is disabled.

1. `:core` — DTOs, enums, validation (`target: core`).
2. Data-model documentation if the vault JSON must change (`target: external-doc`
   or a checklist item on the core task).
3. `:server` — Flyway `V<n>__…sqm` → SQLDelight queries → Ktor routes → auth/roles
   → `files/` if needed (`target: server`).
4. `:app:shared` repository — Ktor Client, map to `:core` types (`target: shared`).
5. ViewModel / `UiState` / intents in `commonMain`.
6. Shared Composable screen + navigation + Koin in `commonMain`.
7. Thin `:app:androidApp` / `:app:desktopApp` / `:app:webApp` / `:app:iosApp`
   only when the feature needs permissions, windowing, Firebase actuals, or a
   new iOS shell (`target: android` | `desktop` | `web` | `ios`).
8. External public API notes (`target: external-doc`).

Each task needs: `id`, `title`, focused `spec`, `acceptance_criteria`,
`dependencies` (earlier ids), `target`, `module`, `clients_affected`, and
optional `components` (names from the top-level list).

**Server only:** stop after core + server (+ external-doc).  
**Client only:** start at shared repository/UI; no new migrations.  
**Desktop only / web only / ios only / android only:** do not emit tasks for
other thin app modules.

## Spec JSON Schema

The generator (`scripts/generate_spec_html.py`) reads this shape. Required:
`feature_name`. Arrays may be empty. Image `path` values are relative to the
JSON file.

```json
{
  "feature_name": "Event Attendance",
  "feature_slug": "event-attendance",
  "project_profile": "tabala",
  "parent_package": "com.muixeranga.tabala.feature.attendance",
  "scaffold": "AttendanceScaffold",
  "summary": "One-paragraph overview.",
  "overview": "Longer description. Supports **bold**, lists, and `code`.",
  "client_scope": {
    "preset": "server_all_compose",
    "server": true,
    "android": true,
    "desktop": true,
    "web": true,
    "ios": true,
    "external_public_api": false
  },
  "modules": {
    "core": ":core",
    "server": ":server",
    "shared": ":app:shared",
    "androidApp": ":app:androidApp",
    "desktopApp": ":app:desktopApp",
    "webApp": ":app:webApp",
    "iosApp": ":app:iosApp"
  },
  "shared_ui_policy": "Prefer commonMain in :app:shared; platform modules only for expect/actual.",
  "out_of_scope": "Markdown listing disabled clients and non-goals.",
  "external_systems": [
    {
      "name": "Web pública Astro",
      "relationship": "Consumes public API only",
      "base_url": "https://api.example.com",
      "in_repo": false
    }
  ],
  "auth": {
    "client": "Firebase ID token on management routes",
    "server": "Verify token; UID + role; no passwords"
  },
  "data_model_refs": [
    "backend/data-model/data-model.json",
    "server/src/main/sqldelight/migrations/V1__initial_schema.sqm"
  ],
  "images": [
    { "kind": "ios", "caption": "iOS parity reference", "path": "images/ios-attendance.png" },
    { "kind": "mockup", "caption": "Shared Compose mockup", "path": "images/mockup.png" }
  ],
  "components": [
    {
      "name": "AttendanceRow",
      "location": "app/shared/src/commonMain/.../AttendanceRow.kt",
      "decision": "reuse",
      "usage": "Each member row in the list.",
      "notes": "Optional.",
      "layer": "ui",
      "module": ":app:shared",
      "sourceSet": "commonMain",
      "clients": ["android", "desktop", "web", "ios"]
    }
  ],
  "structure": "Markdown describing the shared macro layout.",
  "sections": [
    {
      "title": "Member list",
      "description": "What it contains and how it is arranged.",
      "behavior": "Interactions, states, navigation.",
      "components": ["AttendanceRow"],
      "clients": ["android", "desktop", "web", "ios"]
    }
  ],
  "endpoints": [
    {
      "name": "List attendance",
      "method": "GET",
      "path": "/api/events/{id}/attendance",
      "notes": "Called on screen load.",
      "implemented_on": "server",
      "consumed_by": ["android", "desktop", "web", "ios"],
      "auth": "firebase"
    }
  ],
  "persistence": "Markdown describing storage. Default: SQLite on :server.",
  "tasks": [
    {
      "id": "T1",
      "title": "Add Attendance DTO in :core",
      "spec": "Focused spec for an agent.",
      "acceptance_criteria": ["Criterion 1"],
      "dependencies": [],
      "components": ["AttendanceDto"],
      "target": "core",
      "module": ":core",
      "clients_affected": ["server", "android", "desktop", "web", "ios"]
    }
  ]
}
```

### Field notes

- `client_scope.preset` must be one of the preset ids (or `custom`).
- Component `decision` is `reuse`, `modify`, or `create`.
- Component `layer` is typically `core` | `server` | `ui` | `viewmodel` | `repository`.
- Task `target` is `core` | `server` | `shared` | `android` | `desktop` | `web` |
  `ios` | `external-doc`.
- Section and task `components` arrays reference `name`s in the top-level
  `components` list.
- Image `kind`: `android` | `desktop` | `web` | `ios` | `mockup` | `server`.

### Supported lightweight markdown

The generator renders a small markdown subset in text fields (`summary`,
`overview`, `structure`, `out_of_scope`, `persistence`, `shared_ui_policy`,
section `description`/`behavior`, task `spec`): headings (`#`–`####`),
unordered lists (`-` / `*`), ordered lists, fenced code blocks, inline
`` `code` ``, and `**bold**`. Everything else is treated as paragraphs and
HTML-escaped.
