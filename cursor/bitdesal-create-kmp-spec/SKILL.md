---
name: bitdesal-create-kmp-spec
description: >-
  Builds a Kotlin Multiplatform feature spec through an interview, starting with
  client scope (server, Android, desktop, web, iOS), then generates a
  self-contained HTML spec with embedded images and incremental tasks across
  :core, :server, and :app:shared. Use when the user runs /bitdesal-create-kmp-spec
  or asks to spec a KMP feature by interview. For Android-only interview specs
  use bitdesal-create-spec; for analyzing existing KMP code use
  bitdesal-kmp-use-case-spec.
disable-model-invocation: true
---

# BitDesal Create KMP Spec

Turn a rough feature idea into a detailed, agent-ready **KMP** spec by
interviewing the user, then producing a single self-contained HTML artifact
with the full spec, reference images, and the feature broken into small
incremental tasks across modules.

This skill **interviews for greenfield or planned features**. It does not
analyze existing coverage. For that, use `bitdesal-kmp-use-case-spec`. For
Android-only UI interview specs, use `bitdesal-create-spec`.

## Invocation

```text
/bitdesal-create-kmp-spec some explanation about the spec
```

The text after the command is the initial feature explanation. If it is missing,
ask the user for a one-paragraph description **after** client scope (Step 1).

## Role and Tone

Act like a junior developer who must implement this feature and cannot start
until everything is clear. Be curious, literal, and slightly cautious: surface
assumptions, propose a concrete implementation, and ask the user to confirm or
correct it. Never invent requirements silently — when unsure, ask.

## Default project profile (Tabala)

Assume this monorepo unless the repo or user says otherwise. Confirm by
skimming `AGENTS.md`, `docs/`, `.cursor/rules/`, and Gradle settings.

| Module | Role |
|--------|------|
| `:core` | Shared `@Serializable` DTOs, enums, validation. No UI, Koin, Ktor, SQL, Firebase. |
| `:server` | JVM Ktor API, SQLite + SQLDelight, Flyway, Firebase ID-token auth, `files/` uploads. Depends on `:core` only. |
| `:app:shared` | Almost all management UI: Compose Multiplatform Material 3, ViewModels, Ktor Client repos, Koin. Depends on `:core`, **not** `:server`. |
| `:app:androidApp` | Thin: Application, manifest, Koin start, hosts shared UI. |
| `:app:desktopApp` | Thin: `main()` window + Koin. |
| `:app:webApp` | Thin: JS/Wasm browser entry. |
| `:app:iosApp` | Thin iOS shell when present. Compose UI still lives in `:app:shared`. |

**Shared UI policy:** new screens go in `:app:shared` `commonMain`. Platform
source sets (`androidMain`, `jvmMain`, `iosMain`, `jsMain`, `wasmJsMain`) are
only for expect/actual. Do not duplicate screens per client unless the user
insists.

**Out of this repo (document, do not implement):** public Astro site and any
separately deployed management web that only consume `api.<dominio>`.

**Runtime:** Firebase sign-in on the client → Ktor Client + ID token →
`:server` validates token and role → JSON of `:core` types → ViewModel → Compose.

**Persistence:** SQLite on the server is the source of truth. Clients are
stateless unless the user says otherwise.

**Output:** `specs/<feature-slug>/` (this repo already uses `specs/`).

## Interview Workflow

Copy this checklist and track progress. **Do not skip Step 1.**

```text
KMP Create Spec Progress:
- [ ] Step 1: Client scope (blocking)
- [ ] Step 2: Gather assets and base facts
- [ ] Step 3: Analyze screenshots and explanation
- [ ] Step 4: Inventory existing types, routes, UI
- [ ] Step 5: API and data contract
- [ ] Step 6: Interview macro structure (UI clients only)
- [ ] Step 7: Interview sections and details
- [ ] Step 8: Interview behavior, data, edge cases
- [ ] Step 9: Confirm completeness
- [ ] Step 10: Break into incremental tasks
- [ ] Step 11: Generate the HTML artifact
```

After Step 1, **do not ask** about disabled clients. **Do not invent** server
migrations when `server` is false, unless the user describes new tables — then
escalate: add server to scope or split into two specs.

Question banks, presets, and the JSON schema are in [reference.md](reference.md).

### Step 1: Client scope (required first)

Ask **which clients this feature will have** before screenshots, packages, or
layout. Offer this menu (plus custom):

**With server**

1. Server only
2. Server + all clients (Android, desktop, web, **iOS**)
3. Server + Android
4. Server + desktop
5. Server + web
6. Server + iOS

**Client only** (no server work in this spec)

7. Android only
8. Desktop only
9. Web only
10. iOS only

**Custom** — any mix (example: server + Android + desktop, no web)

Then one extra yes/no: **external public API consumer** (e.g. Astro)?

Preset ids and JSON flags: [reference.md](reference.md#client-scope-presets).

**All clients** means Compose Multiplatform on **Android, desktop, web, and
iOS**. Shared UI is `commonMain`. If `:app:iosApp` is missing, still allow
iOS in scope and add a thin-shell / `iosMain` task — do not assume SwiftUI.

Record `client_scope` and list disabled clients as **out of scope**.

### Step 2: Gather assets and base facts

Ask only what the enabled clients need (full bank in [reference.md](reference.md)):

- Screenshots / mockups for each **enabled** UI client (`android`, `desktop`,
  `web`, `ios`). iOS shots are parity reference even when Compose is shared.
- Feature slug, parent package under `:app:shared`, navigation route / scaffold.
- General behavior.
- Endpoints (new vs existing). If `server` is false and they list **new**
  tables/routes, stop and re-scope.
- Data-model touch: new fields vs `backend/data-model/data-model.json` (or
  repo equivalent).
- Auth: Firebase management vs public/RGPD routes.

Save images to `specs/<feature-slug>/images/` and record path + caption +
`kind` (`android` | `desktop` | `web` | `ios` | `mockup` | `server`).

### Step 3: Analyze screenshots and explanation

Skip if **server only** (no UI clients).

Read the screenshots and the explanation, then describe back what you see so
the user can correct you. State the visual hierarchy before asking how to
build it. Call out what is **shared Compose** vs what might need expect/actual.

### Step 4: Inventory existing artifacts

Search the project before proposing new types or screens. For every relevant
candidate, ask **reuse / modify / create new**. Record name, module,
source set, location, decision, usage, and which clients it serves.

Search by enabled layers only:

- `:core` — DTOs, enums
- `:server` — Ktor routes, SQLDelight, Flyway `V<n>__*.sqm`
- `:app:shared` — `@Composable`, ViewModels, repositories, Koin modules
- Thin app modules — only if the feature needs bootstrap, permissions, or windowing

See [reference.md](reference.md#how-to-search).

### Step 5: API and data contract

Required when `server` is true, or when a client-only feature **calls** APIs.

Cover: method, path, request/response `:core` types, auth (Firebase vs public),
who **implements** (`:server`) vs who **consumes** (enabled clients / Astro),
errors, pagination, files under `files/`, Flyway if schema changes.

One endpoint list — do not duplicate per client. Use `consumed_by`.

If `server` is false, document **existing** endpoints the UI will call; do not
add migration tasks.

### Step 6: Interview macro structure (UI clients only)

Skip if server only.

Start with the largest building blocks for the **shared** screen. Propose an
implementation and give an example answer. Keep questions at layout/container
level until the overall structure is agreed. Ask platform shells only if a
thin app module must change.

### Step 7: Interview sections and details

Once the macro structure is clear, go section by section. Name which
inventoried components (reused, modified, or new) go where. Move from
container → list/grid → item → states. Map every widget to `:app:shared`
unless it is truly platform-specific.

### Step 8: Interview behavior, data, and edge cases

Cover interactions, navigation, loading/empty/error, how each endpoint maps
to the ViewModel, validation, and cases the mockups omit. Include
concurrency (double-tap), 401 session, and offline only if in scope.

### Step 9: Confirm completeness

Summarize the feature in your own words: **client_scope**, modules, API,
component decisions, explicit **out of scope** clients. Ask: "Is anything
missing or wrong before I split this into tasks?" Only continue when the
user confirms.

### Step 10: Break into incremental tasks

Split into small ordered tasks, each independently feedable to an agent.
Each task needs: `id`, `title`, focused `spec`, `acceptance_criteria`,
`dependencies`, `target`, `module`, `clients_affected`, and component names.

Default order (drop steps whose client/module is disabled):

1. `:core` DTOs / enums
2. Data-model note if the vault/JSON must change
3. `:server` Flyway → SQLDelight → routes → files/auth
4. `:app:shared` repository (Ktor Client)
5. ViewModel + `UiState`
6. Shared Composable + navigation + Koin
7. Thin `:app:androidApp` / `:app:desktopApp` / `:app:webApp` / `:app:iosApp`
   **only** when bootstrap/expect-actual is required
8. External-doc task for Astro/public API if `external_public_api`

Typical order detail: [reference.md](reference.md#task-breakdown-guidance).

### Step 11: Generate the HTML artifact

1. Write `specs/<feature-slug>/spec.json` (schema and example in
   [reference.md](reference.md), sample at `templates/spec.example.json`).
2. Run the generator from the **project** repository root:

```bash
python3 .cursor/skills/bitdesal-create-kmp-spec/scripts/generate_spec_html.py \
  --spec specs/<feature-slug>/spec.json \
  --out specs/<feature-slug>/spec.html
```

3. Open the generated HTML path for the user and confirm images rendered.

The generator embeds every image as base64. Image paths in the JSON are
resolved relative to the JSON file.

## Output Goal

The final artifact is one HTML file that:

- States **client_scope** and lists out-of-scope clients.
- Explains the feature with enough detail to minimize agent errors.
- Shows reference images inline.
- Lists modules, auth, endpoints (`consumed_by`), persistence, and sections.
- Lists existing/new artifacts with reuse/modify/create and where they go.
- Contains incremental tasks tagged with `target` / `module` / `clients_affected`.

## Notes

- Ask one focused topic at a time; do not dump the whole question bank at once.
- Prefer concrete proposals with example answers over open-ended questions.
- Always search the project before proposing new DTOs, routes, or Composables.
- New screens live in `:app:shared`, not duplicated per platform.
- Do not commit generated files unless the user explicitly asks.
- Use a lowercase, hyphenated `<feature-slug>` derived from the feature name.
- The generator has no third-party dependencies; Python standard library only.

## Additional Resources

- Question bank, presets, schema: [reference.md](reference.md)
- Example spec JSON: [templates/spec.example.json](templates/spec.example.json)
