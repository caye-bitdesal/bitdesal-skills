---
name: bitdesal-kmp-use-case-spec
description: >-
  Analyzes a Kotlin Multiplatform project (ViewModels, repositories, Composables,
  and project README/docs) and writes use-case specs with coverage vs gaps, a
  deduplicated test plan, and Mermaid sequence diagrams and flowcharts. Use when
  the user runs /bitdesal-kmp-use-case-spec, analyze-all for the whole project,
  or asks for KMP use-case coverage, missing edge cases, or test gaps.
disable-model-invocation: true
---

# BitDesal KMP Use Case Spec

Turn **existing** KMP code into an evidence-based use-case specification: what
each flow does today, what is **covered** vs **missing** (edge cases, network
errors, empty states, etc.), which **tests to add** (relevant only — no redundant
variations), and **diagrams** per use case.

This skill **reads the codebase**; it does not interview for greenfield features.
For interview-driven feature specs, use `bitdesal-create-spec` instead.

## Invocation

```text
/bitdesal-kmp-use-case-spec
/bitdesal-kmp-use-case-spec analyze-all
/bitdesal-kmp-use-case-spec Login and session refresh
/bitdesal-kmp-use-case-spec module :app:shared feature habits
```

**Scope modes**

| Input | Meaning |
|-------|---------|
| `analyze-all` (or `all`, `whole-project`) | Every Gradle module and feature area in the repo — see [Analyze-all](#analyze-all-whole-project) |
| Named feature / module / screens | Partial scope — single `SPEC.md` under one slug |
| *(empty)* | Ask once: `analyze-all` or a narrower scope; then proceed |

Do not block on a long questionnaire after that one question.

## Role and Tone

Act like a staff engineer writing a test strategy brief for the team:

- Every claim ties to a **file, symbol, or test** you opened.
- Separate **observed behavior** from **inferred intent**.
- Prefer **few, high-signal tests** over exhaustive matrices.
- Call out KMP-specific risks (shared vs platform source sets, coroutine scope,
  Compose effects, client vs server persistence).

## Workflow Checklist

```text
KMP Spec Progress:
- [ ] Step 1: Confirm scope and output location
- [ ] Step 1b: Collect README and project documentation
- [ ] Step 2: Discover ViewModels, repositories, Composables, tests
- [ ] Step 3: Derive use cases from docs + code + scope
- [ ] Step 4: Trace each use case through layers
- [ ] Step 5: Coverage vs gaps per use case
- [ ] Step 6: Deduplicated test plan
- [ ] Step 7: Sequence + flow diagrams (Mermaid)
- [ ] Step 8: Write spec artifact and summarize
```

### Step 1: Confirm scope and output location

- **Scope**: `analyze-all`, feature name, package prefix, module (`:app:shared`,
  `:core`, etc.), or explicit file list from the user.
- **Slug**: lowercase hyphenated name, e.g. `login`, `habit-dashboard`. For
  analyze-all use the fixed slug `project` (see below).
- **Output** (scoped feature):

```text
specs/kmp-use-cases/<slug>/SPEC.md
specs/kmp-use-cases/<slug>/diagrams.md   # optional split if SPEC is long
```

Do not commit unless the user asks.

#### Analyze-all (whole project)

When the user passes **`analyze-all`** (case-insensitive; aliases: `all`,
`whole-project`, `entire-project`):

1. **Discover boundaries** — Gradle `settings.gradle.kts` / `settings.gradle`
   included modules; top-level packages; navigation graphs; README-defined
   feature areas (Step 1b).
2. **Partition** — One **feature bundle** per logical area (e.g. `:app:shared`
   screen groups, `:server` route groups, `:core` only if it exposes use-case
   contracts). Name slugs from module + package or README section titles.
3. **Write**:

```text
specs/kmp-use-cases/project/
├── INDEX.md              # master index + cross-feature summary
├── DOCUMENTATION.md      # synthesized README/doc context (required)
├── features/
│   ├── <feature-slug>/SPEC.md
│   └── …
└── diagrams/             # optional shared or oversized diagrams
```

4. **INDEX.md** must include: module map, use-case count per feature, rollup of
   gaps and planned tests, links to each `features/*/SPEC.md`.
5. **Same quality bar** per feature spec as a single-scope run; use global UC ids
   (`UC-001` …) across the project or prefix by feature (`AUTH-UC-01`) — pick
   one scheme in INDEX and stay consistent.
6. **Order of work** — Step 1b and full Step 2 once for the repo, then loop
   Steps 3–8 per feature bundle without re-scanning READMEs unless a bundle has
   its own README.

If the project is small (e.g. one module, fewer than five screens), a single
`specs/kmp-use-cases/project/SPEC.md` instead of `features/*` is acceptable;
still write `INDEX.md` and `DOCUMENTATION.md`.

### Step 1b: Collect README and project documentation

Before code discovery (and again when a feature folder has its own README),
search and read documentation that shapes the spec. Patterns are in
[reference.md](reference.md#documentation-discovery).

For each file read, capture in working notes (and in `DOCUMENTATION.md` for
analyze-all, or a **Documentation context** section in scoped `SPEC.md`):

| Extract | Use in spec |
|---------|-------------|
| Stated user flows / features | Names and ordering of use cases |
| API or endpoint lists | Repository ↔ server alignment |
| Architecture rules | Layer expectations, what must not happen on client |
| Known limitations / TODOs | Candidate gaps |
| Setup or env assumptions | Out-of-scope or test notes |

**Rules**

- Cite doc claims as `(doc: path#section)` alongside code citations.
- If docs describe a flow **with no code**, add use case **Documented, not
  implemented** — do not invent implementation detail.
- If code exists but **contradicts** docs, call out explicitly under the use case.
- Prefer module-local READMEs when analyzing that module; root README for
  product-level flows.

### Step 2: Discover artifacts

Search the repo using patterns in [reference.md](reference.md). For each hit,
record:

| Field | Purpose |
|-------|---------|
| Symbol | Class/function name |
| Path | Repo-relative file |
| Layer | UI / ViewModel / Repository / API / Domain |
| Existing tests | Test file paths that reference this symbol |

**AGENTS.md** and README content from Step 1b override generic KMP assumptions.

Typical KMP layout (adapt to what you find):

- `commonMain` — shared ViewModels, repositories, Composables, DTOs
- `androidMain` / `iosMain` / `jvmMain` / `wasmJsMain` — platform adapters
- `:core` — models and contracts; `:server` — Ktor routes; client repositories
  call remote APIs

### Step 3: Derive use cases

A **use case** is a user- or system-visible goal (not a single function).

Sources (in order):

1. User scope (if given); for `analyze-all`, every feature bundle in the partition
2. README / docs (Step 1b) — flows, endpoints, feature names
3. Screen-level Composables and their ViewModel public API (`*Intent`, `*Action`,
   `onEvent`, public `fun` entry points)
4. Repository methods that map 1:1 to product flows
5. Navigation routes / deep links if present

Name use cases in **verb + object** form: `Sign in with email`, `Refresh habit
list`, `Delete account`.

Cap at what scope requires; merge trivial CRUD that shares identical error
handling into one use case with sub-flows when that reduces noise.

### Step 4: Trace each use case

For each use case, document the **happy path** chain:

```text
Composable / Screen → ViewModel (state + events) → Repository → Remote/Local
```

Note:

- State types (`UiState`, sealed classes, `StateFlow` emissions)
- Where loading/error/success is set
- Retry, debounce, pagination, cache
- Threading: which scope (`viewModelScope`, `SupervisorJob`, etc.)

Link every step to **concrete symbols and paths**.

### Step 5: Coverage vs gaps

For **each use case**, two lists:

**Covered today** — behaviors already implemented *and* evidenced in code (and in
tests if they exist). Examples: empty list UI, 401 clears session, validation on
submit.

**Missing or weak** — use the gap categories in [reference.md](reference.md).
Only include gaps that **matter for this use case**; skip generic boilerplate
unless the code path is exposed.

Mark each gap:

- **Not handled** — no branch in code
- **Handled, untested** — logic exists, no test found
- **Partial** — e.g. only generic `Throwable`, no offline distinction

### Step 6: Deduplicated test plan

Rules (see [reference.md](reference.md) for examples):

- **One test per distinct behavior or outcome**, not per HTTP code if one handler
  covers all errors.
- Prefer **unit tests** on ViewModel/repository mapping; **Compose/UI tests** only
  for non-trivial interaction or visual state wiring not reachable from unit tests.
- Name tests as `should <outcome> when <condition>`.
- Tag each test with **layer** and **use case id** (`UC-03`).
- If a gap is **not handled**, list an test that would **fail today** (TDD) or
  skip with reason — be explicit.

Do **not** list: duplicate parametrized rows, “same test for iOS and Android” when
`commonTest` suffices, or multiple network codes mapped to the same UI state.

### Step 7: Diagrams

For **each use case** (or merged group with identical topology), add:

1. **Sequence diagram** (Mermaid `sequenceDiagram`) — participants: User/Actor,
   Composable, ViewModel, Repository, API (and Server DB if in scope).
2. **Flowchart** (Mermaid `flowchart TD` or `flowchart LR`) — decisions for
   validation failures, errors, empty data, success.

Diagram rules:

- Match **actual** call order from code; add `alt`/`opt` for error branches that
  exist or are listed as gaps (dashed note in caption).
- Keep participants ≤ 6; use `Note` for platform-specific steps.
- If Archify is installed and the user wants HTML exports, you may additionally
  run Archify **after** Mermaid is correct — Mermaid in the spec is required either
  way.

Put diagrams in `SPEC.md` under each use case, or in `diagrams.md` linked from
the spec if the file grows large.

### Step 8: Write spec artifact

Use the template in [templates/use-case-spec.example.md](templates/use-case-spec.example.md).

Deliver to the user:

- Path(s) to `SPEC.md` (and `INDEX.md` + `DOCUMENTATION.md` for analyze-all)
- Table of use cases with counts: covered items, gaps, planned tests
- Top 3 risk gaps (network, auth, data loss, concurrency)
- List of README/doc files used (with paths)

## Output Quality Bar

Before finishing, verify:

- [ ] Every use case has Composable + ViewModel + Repository citations
- [ ] Covered vs missing lists are non-empty or explicitly “none” with reason
- [ ] Test list has no obvious duplicates (same assertion, different label)
- [ ] Each use case has sequence + flow Mermaid blocks that parse
- [ ] Scope outside analysis is stated (“server routes not in scope”)
- [ ] README/doc context cited where it informed use cases or gaps
- [ ] analyze-all: INDEX links every feature spec; DOCUMENTATION.md summarizes docs

## Additional Resources

- Discovery patterns, gap taxonomy, test dedup: [reference.md](reference.md)
- Feature spec skeleton: [templates/use-case-spec.example.md](templates/use-case-spec.example.md)
- analyze-all index: [templates/index.example.md](templates/index.example.md)
- analyze-all doc synthesis: [templates/documentation.example.md](templates/documentation.example.md)
