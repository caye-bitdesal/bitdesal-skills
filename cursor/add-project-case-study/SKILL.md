---
name: add-project-case-study
description: >-
  Creates a Bitdesal project case study page (like Kivra or Yössä) and adds its
  card to /projects. Use when adding a new project showcase, case study page,
  project card, or when the user mentions Kivra/Yössä-style project pages.
---

# Add Project Case Study (Bitdesal Web)

Creates `/projects/{slug}` dark-theme case study pages and registers the project card on `/projects`.

## Before coding — gather inputs

Ask the user for anything missing. Minimum required:

| Field | Example | Notes |
|-------|---------|-------|
| `slug` | `kivra`, `yossa` | lowercase, URL-safe; drives file names and i18n keys |
| `displayName` | `Kivra Finland` | Card title |
| `tag` | `Android · Productivity` | Platform · category |
| `updatedYear` | `2026` | Shown on card |
| `cardDescription` | one sentence | Card only — no Bitdesal self-promo unless user asks |
| `accentColor` | `#3dcc58` | Hex; used everywhere (Kivra green, Yössä `#6eb5ff`) |
| `appIcon` | user-provided image | Save to `public/projects/{slug}/` or `public/{slug}-app-icon.png` |
| `screenshots` | hero ×3, carousel ×N, play-section ×2 | PNG paths under `public/projects/{slug}/` |
| `variant` | `live` or `legacy` | See below |
| `featureOnHome` | yes/no | Home shows **one** featured card only (replace current if yes) |

### Variant: `live` (copy from Kivra)

- Hero CTAs: optional website URL + Google Play URL
- Play section title references Google Play
- Metrics: typically users, rating, reviews, years (adapt to project)

### Variant: `legacy` (copy from Yössä)

- No external store/website links in hero
- Show `discontinued` notice paragraph instead
- Play section title references legacy/Android listing
- Metrics: adapt (e.g. rating, city, offers, platform)

## Reference implementations

| | Kivra (`live`) | Yössä (`legacy`) |
|---|---|---|
| Page | `src/pages/projects/kivra.astro` | `src/pages/projects/yossa.astro` |
| Wrapper class | `kivra-case` | `yossa-case` |
| Accent | `#3dcc58` | `#6eb5ff` |
| i18n card | `projects.kivra` | `projects.yossa` |
| i18n detail | `projects.kivraDetail` | `projects.yossaDetail` |

**Always copy the closest variant** and do a systematic rename — do not invent a new layout.

## Workflow checklist

Copy and track progress:

```
- [ ] 1. Save assets to public/projects/{slug}/
- [ ] 2. Create src/pages/projects/{slug}.astro
- [ ] 3. Add i18n: projects.{slug} + projects.{slug}Detail in es, en, fi
- [ ] 4. Add card to src/pages/projects.astro (newest first)
- [ ] 5. Optionally update featured card in src/pages/index.astro
- [ ] 6. npm run build — fix errors before finishing
```

## Step 1 — Assets

```
public/projects/{slug}/
  {slug}-app-icon.png      # card + CTA icon
  screen-*.png             # hero, carousel, play-section images
```

Use descriptive filenames (`screen-login.png`, `screen-home.png`, …).

## Step 2 — Case study page

1. Copy `kivra.astro` or `yossa.astro` → `src/pages/projects/{slug}.astro`
2. Replace systematically:

| Find | Replace with |
|------|--------------|
| `kivra` / `yossa` | `{slug}` |
| `kivra-case` / `yossa-case` | `{slug}-case` |
| `kivraDetail` / `yossaDetail` | `{slug}Detail` |
| `#3dcc58` / `#6eb5ff` | `{accent}` |
| `#35b84f` / `#5aa8f5` | darker hover of accent |
| `rgba(61,204,88,0.18)` etc. | RGBA of accent at ~0.18–0.2 opacity |
| Carousel IDs/classes | `{slug}-carousel`, `{slug}-carousel-slide`, `{slug}-slide-frame` |

3. Update frontmatter arrays:

```astro
const heroPhones = [ /* 3 screenshots */ ];
const carouselScreens = [ { src, key: 'projects.{slug}Detail.screens.{id}', label } ];
const features = [ { icon, titleKey, descKey } ];  // 6 items typical
const playDetails = [ /* category, updated, company, country */ ];
```

4. Hero section:
   - **live**: `websiteUrl`, `playStoreUrl` + both buttons
   - **legacy**: remove external buttons; add `<p data-i18n-key="projects.{slug}Detail.discontinued">`

5. Metrics bar: 4 stats with `{slug}Detail.metrics.*` keys matching your data.

6. Play section images: two phone screenshots (Kivra) or mixed layout (Yössä) — match reference.

7. Global `<style is:global>`: replace `.kivra-case` / `.yossa-case` with `.{slug}-case` and accent color.

8. Carousel `<script>`: update element IDs and class selectors to `{slug}-*` prefix.

### Feature icons

Reuse SVG branches from Kivra/Yössä (`mailbox`, `payment`, `document`, `folder`, `users`, `bell`, `map`, `ticket`, `star`, `location`, `filter`, `feed`). Pick closest match; add a new icon branch only if none fits.

## Step 3 — i18n (`src/i18n/translations.ts`)

Add in **all three** language blocks (`es`, `en`, `fi`):

```ts
projects: {
  // existing keys…
  {slug}: {
    name: '…',
    tag: 'Android · …',
    updated: '2026',
    description: '…',  // card copy only
  },
  {slug}Detail: { /* full page copy — see reference.md */ },
}
```

Do **not** edit `make-translations.ts` for project content — overrides live in `translations.ts`.

Translate faithfully; keep metrics numbers consistent across languages (e.g. `4.3★`).

## Step 4 — Project card (`src/pages/projects.astro`)

Copy an existing `<a href="/projects/…">` block. Insert **at the top** of the card list (newest first).

```astro
<a href="/projects/{slug}" class="group block border border-border rounded-xl p-8 md:p-10 hover:border-primary transition-colors shadow-sm hover:shadow-md">
  <div class="flex items-start gap-6 mb-8">
    <img src="/projects/{slug}/{slug}-app-icon.png" alt="{displayName}" width="96" height="96" class="w-24 h-24 rounded-2xl shadow-lg shrink-0" loading="lazy" decoding="async" />
    <div class="min-w-0 pt-1">
      <h2 class="text-3xl md:text-4xl mb-2 group-hover:text-primary transition-colors" data-i18n-key="projects.{slug}.name">{displayName}</h2>
      <p class="text-foreground/60">
        <span data-i18n-key="projects.{slug}.tag">…</span>
        <span aria-hidden="true"> · </span>
        <span data-i18n-key="projects.{slug}.updated">{year}</span>
      </p>
    </div>
  </div>
  <p class="text-lg text-foreground/80 leading-relaxed mb-8" data-i18n-key="projects.{slug}.description">…</p>
  <span class="inline-flex items-center gap-2 text-primary text-lg group-hover:gap-3 transition-all">
    <span data-i18n-key="projects.viewProject">View project</span>
    <span aria-hidden="true">→</span>
  </span>
</a>
```

## Step 5 — Home featured card (optional)

If `featureOnHome` is yes, replace the single card in `src/pages/index.astro` Projects section (~lines 227–283) with the new project's card markup (same as Step 4, wrapped in `bg-white` card).

If no, leave home unchanged.

## No changes needed

- `src/components/Header.astro` — `/projects` nav already covers case study URLs
- `src/components/Footer.astro` — same
- Active nav highlights `/projects/*` via prefix match

## Verification

```bash
npm run build
```

Confirm `/projects/{slug}` and `/projects` render. Check:
- Accent color consistent (hero, metrics, carousel ring, CTA)
- All `data-i18n-key` resolve in es/en/fi (switch `?lang=`)
- Footer hidden on case study page; copyright in CTA section
- External links use `target="_blank" rel="noopener noreferrer"`

## Additional resources

- Full i18n key tree: [reference.md](reference.md)
- Kivra example: `src/pages/projects/kivra.astro`
- Yössä example: `src/pages/projects/yossa.astro`
