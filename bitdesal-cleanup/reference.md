# bitdesal-cleanup — reference

## Why “internally connected but unreachable”?

Static analysis often misses chains where `A` calls `B` calls `C`, but nothing calls `A`. Each symbol looks “used” within the cluster; only tracing from app entry points reveals the orphan.

Example (removed from Weel):

```
sendFeedback(buildConfigProxy)          ← root: never called
  → getSupportEmailTemplate()         ← BuildConfigProxy extension
  → EmailSupport(...)                 ← only caller of that subclass
BuildConfigProxyImpl(debuggableConfig) ← never instantiated
DebuggableConfig                       ← interface, no impl
```

Live code (`openExternalApp`) was reachable; the feedback branch was not.

## Grep patterns

Find references to a type or file-scoped API:

```bash
rg 'BuildConfigProxy|sendFeedback' app/src/
rg 'NavigationContract|CustomNavHost' app/src/
rg 'class Foo|object Foo|fun barBaz' app/src/main/java/.../Foo.kt
```

If results are only under the same directory or same file cluster → candidate chain.

## Partial chain example

`OpenExternalAppRequest.kt` stayed because `Maps` is used from `WeelNavGraph`. Dead subclasses (`Email`, `Phone`, `InsertCalendar`, …) and `getIntent()` were trimmed; `openExternalApp()` reads `action` / `dataUri` / `extras` directly.

## Android-specific traps

| Looks dead | Actually live because |
|------------|----------------------|
| Room DAO method | KSP / generated impl |
| `@Serializable` data class | Polymorphic JSON / nav args |
| Composable with only `@Preview` | Preview/screenshot tests |
| Receiver class | `AndroidManifest.xml` |
| `provideFactory` on ViewModel | Nav graph `viewModel(factory = …)` |

## Re-scan trigger

Run full Phase 1 again after:

- Large refactors (e.g. DI migration, nav rewrite)
- Removing Hilt or changing module structure
- Adding features that might revive old utilities
