# Project Case Study — Reference

## i18n key tree (`projects.{slug}Detail`)

```
{slug}Detail
├── back
├── tag
├── title
├── titleAccent
├── heroDescription
├── website              # live variant only
├── playStore            # live variant only
├── discontinued         # legacy variant only
├── metrics
│   ├── {stat1}          # e.g. users, rating — value shown large
│   ├── {stat1}Label
│   ├── {stat2}
│   ├── {stat2}Label
│   ├── {stat3}
│   ├── {stat3}Label
│   ├── {stat4}
│   └── {stat4}Label
├── screensTitle
├── screens
│   └── {screenId}       # one key per carousel slide
├── featuresTitle
├── features
│   └── {featureId}
│       ├── title
│       └── description
├── playSection
│   ├── title
│   ├── description
│   ├── categoryLabel / category
│   ├── updatedLabel / updated
│   ├── companyLabel / company
│   └── countryLabel / country
├── cta
│   ├── title
│   ├── titleAccent
│   ├── subtitle
│   └── button
└── copyright
```

Card-only keys under `projects.{slug}`:

```
{slug}
├── name
├── tag
├── updated
└── description
```

Shared keys (do not duplicate): `projects.viewProject`, `projects.hero.*`, `home.projects.*`

## Page section order

1. Hero — back link, tag, title + accent line, description, CTAs, 3-phone mosaic
2. Metrics — 4-column grid, `border-y border-white/10`
3. Screens carousel — horizontal snap scroll + dot pagination
4. Features — 3-column grid, `bg-[#141414]` cards
5. Play/Legacy — 2-col: metadata `<dl>` + screenshots
6. CTA — app icon, two-line heading, contact button, inline copyright

## Accent color replacements

When copying a page, replace **every** occurrence:

| Usage | Kivra | Yössä |
|-------|-------|-------|
| Accent text/border | `#3dcc58` | `#6eb5ff` |
| CTA hover | `#35b84f` | `#5aa8f5` |
| Hero radial gradient | `rgba(61,204,88,0.18)` | `rgba(110,181,255,0.2)` |
| Feature icon bg | `bg-[#3dcc58]/15` | `bg-[#6eb5ff]/15` |
| Carousel active dot | `bg-[#3dcc58]` | `bg-[#6eb5ff]` |
| Slide frame ring | `box-shadow: 0 0 0 2px #3dcc58` | `0 0 0 2px #6eb5ff` |

Convert hex to RGB for `rgba()` in hero gradient: `#3dcc58` → `61, 204, 88`.

## Global styles template

```css
body:has(.{slug}-case) header {
  background-color: #0a0a0a;
  border-color: rgba(255, 255, 255, 0.1);
}
body:has(.{slug}-case) header a,
body:has(.{slug}-case) header button,
body:has(.{slug}-case) header .text-foreground\/70 {
  color: rgba(255, 255, 255, 0.75);
}
body:has(.{slug}-case) header a:hover,
body:has(.{slug}-case) header [data-lang].text-primary {
  color: {accent};
}
body:has(.{slug}-case) header .text-primary,
body:has(.{slug}-case) header [data-lang].text-primary {
  color: {accent};
}
body:has(.{slug}-case) footer {
  display: none;
}
body:has(.{slug}-case) {
  background-color: #0a0a0a;
}
.{slug}-carousel-slide.is-active .{slug}-slide-frame {
  box-shadow: 0 0 0 2px {accent};
  border-radius: 1.85rem;
}
```

## Kivra metrics reference

| Key | EN value |
|-----|----------|
| users | 100K+ |
| rating | 4.3★ |
| reviews | 5.1K+ |
| years | 7+ |

## Yössä metrics reference

| Key | EN value |
|-----|----------|
| rating | 4★ |
| city | Helsinki |
| offers | Drink deals |
| platform | Android |

## Files touched per project

| Action | Path |
|--------|------|
| Create | `src/pages/projects/{slug}.astro` |
| Create | `public/projects/{slug}/*.png` |
| Edit | `src/i18n/translations.ts` (es, en, fi) |
| Edit | `src/pages/projects.astro` |
| Edit (optional) | `src/pages/index.astro` |

## Example invocation

User: "Añade el proyecto FooBar con estas capturas"

Agent should:
1. Read this skill + open `kivra.astro` or `yossa.astro`
2. Ask: slug, variant (live/legacy), accent color, Play Store URL, feature on home?
3. Implement checklist
4. Run `npm run build`
