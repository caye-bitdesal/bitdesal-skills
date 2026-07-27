---
name: bitdesal-cleanup
description: >-
  Find and remove dead Kotlin/Android code in Weel — unreachable symbol chains,
  unused resources, and legacy scaffolding. Use when the user invokes /bitdesal-cleanup,
  asks for dead-code analysis, unreachable chains, or project cleanup.
disable-model-invocation: true
---

# bitdesal-cleanup

Systematic cleanup for **Weel** (`picalandroid`): report internally connected but unreachable code, then delete **high-confidence** chains.

Read [AGENTS.md](../../AGENTS.md) for project constraints. Minimize scope; one cleanup theme per commit/PR.

## Phase 1 — Analysis (always run first)

### Entry points (roots)

Trace reachability **from** these; anything with no inbound path is a candidate:

| Root | Location |
|------|----------|
| Application | `ui/main/WeelApplication.kt` |
| Manifest components | `app/src/main/AndroidManifest.xml` |
| Navigation | `ui/navigation/WeelNavGraph.kt`, `WeelDestination.kt` |
| DI | `data/AppContainer.kt`, `AppContainerImpl.kt` |
| Tests | `app/src/test/`, `app/src/androidTest/`, `app/src/sharedTest/` |

### Exclude false positives

Do **not** flag as dead without extra verification:

- `@Preview` / `@WeelPreviews` composables
- Room `@Dao`, `@Entity`, `@TypeConverter`, KSP-generated `*_Impl`
- `@Serializable` types (kotlinx.serialization)
- Manifest-declared Activities, Receivers, Services
- Navigation route types in `WeelDestination` / `WeelNavGraph`
- Generated `BuildConfig`
- String/drawable resources referenced from XML or `@stringResource`

### Chain types

| Type | Meaning |
|------|---------|
| **Full chain** | Every exported symbol in a file set has zero callers outside that set |
| **Partial chain** | Live file/sealed class with dead subclasses or unused methods |
| **Single orphan** | One file, one type, zero external references |

### Detection workflow

1. Scan `app/src/main/java/**/*.kt` for public classes, sealed types, top-level functions.
2. For each candidate, `grep` usages across `app/src/` (main + tests).
3. If usages exist only inside the same cluster, mark **internally connected**.
4. Confirm no path from entry points → mark **unreachable**.
5. Assign confidence:
   - **High** — zero external refs; clear legacy replacement exists (e.g. Compose Nav replaced `NavigationContract`).
   - **Medium** — only referenced from other dead code or specs/docs.
   - **Low** — might be intentional stub / upcoming feature; ask user.

### Report template

```markdown
## Dead code report

| # | Chain | Files | Confidence | Root symbol(s) |
|---|-------|-------|------------|----------------|
| 1 | … | … | High | … |

### Chain N — [name]
- **Files:** …
- **Root:** …
- **Internal wiring:** …
- **Why unreachable:** …
```

Deliver the report before deleting unless the user asked to clean in the same turn.

## Phase 2 — Cleanup (high confidence only)

Delete only **High** chains unless the user explicitly approves Medium/Low.

### Pre-delete checklist

- [ ] Re-grep each symbol; no callers outside the cluster
- [ ] No spec actively planning to use the API (`specs/`)
- [ ] Partial chains: keep the live root (e.g. `OpenExternalAppRequest.Maps`)

### Delete order

1. Leaf files first (types only referenced by other dead files)
2. Partial trims (remove dead sealed subclasses / unused methods from live files)
3. Run `./gradlew testDebugUnitTest`
4. Fix compile errors ( stray imports only — do not refactor live code)

### Commit message

```
care: remove dead [chain-name] code
```

## Known high-confidence chains (Weel baseline)

Removed in baseline cleanup; re-scan if they reappear:

| Chain | Files removed |
|-------|---------------|
| BuildConfig / feedback | `BuildConfigProxy.kt`, `BuildConfigProxyImpl.kt`, `DebuggableConfig.kt`, `FeedbackUtils.kt` |
| Legacy multi-Activity nav | `NavigationContract.kt`, `ParcelableNavigationContract.kt`, `ParcelableNoDataNavigationContract.kt`, `NavigationNoData.kt`, `StartDestinationData.kt`, `PackageManagerExtensions.kt`, `ComposeNavigationUtils.kt`, `NavigationUtils.kt` |
| Icon action dispatch | `WeelIconButtonAction.kt` |
| Permission enum stub | `NeededPermission.kt` |
| Unused shape | `LineShape.kt` |
| Duplicate time extensions | `KotlinTimeExtensions.kt` |
| Partial | Trim `OpenExternalAppRequest` to `Maps` only |

For extended methodology and R8 optional verification, see [reference.md](reference.md).

## Optional verification

- **IDE:** Analyze → Inspect Code → Unused declaration (manual spot-check)
- **R8:** Temporarily `isMinifyEnabled = true` on release; review shrink report (needs ProGuard keep rules for Compose/Room/Sentry)

## Do not

- Delete code only used from tests without checking whether tests should move to `sharedTest` fakes
- Remove `@Preview` composables as “unused”
- Broad refactor while cleaning — delete-only diffs
