# Competitive research, monetization, and scores

Read this during Steps 3–4 of `/bitdesal-draft-idea`. Do not invent the market.

## Search queries

Run **at least 5** web searches. Adapt to the idea's language and geography.

Replace `{idea}`, `{category}`, `{audience}`, `{country}`:

1. `{idea}` app
2. `{category}` app `{country}`
3. best `{category}` app 2026
4. `{category}` for `{audience}`
5. `{competitor or category}` vs `{adjacent tool}`
6. `{category}` Product Hunt
7. `{category}` Google Play / App Store
8. `{problem}` spreadsheet / WhatsApp / Notion (status quo)
9. `{category}` pricing / subscription / "how they make money"
10. `{competitor}` pricing

Add regional queries when geography is known (`España`, `LatAm`, `Finland`,
`EU`). Search in the user's language **and** English.

## What to open

`WebFetch` a few of the best hits, not only titles:

- Product homepage or help docs (what they actually ship)
- App Store / Play listing (permissions, ratings, last update)
- Pricing page
- How competitors monetize (IAP, SaaS, take-rate, ads)
- A recent review or comparison article if it names several players

Skip random SEO blogs that only repeat "top 10 apps" with no substance.

## Competitor types (use all three)

| Type | Meaning | Example |
|------|---------|---------|
| Direct | Same job, similar product | Another app in the same category |
| Indirect | Same job, different shape | Web SaaS, marketplace, agency |
| Status quo | How people cope today | Spreadsheet, chat group, paper, nothing |

A "no competitors" section is almost always a research failure, not a blue ocean.

## Gap verdict (pick one)

**Real gap** — a specific user + job is poorly served; named competitors miss a
concrete dimension (locale, workflow, trust, price, platform). Evidence from
listings/reviews, not vibes.

**Partial gap** — category exists; differentiation is possible but narrow
(niche, integration, UX, distribution). Winning depends on focus.

**No clear gap** — several products already do this well for the same user.
Recommend: do not build, buy/partner, or shrink to a wedge the incumbents ignore.

Default to the harsher verdict when evidence is mixed.

## Monetization study

Propose 3–6 models that could actually apply (do not dump "ads, sub, IAP" on
every idea). For each: who pays, mechanism, short-term vs long-term, v1 fit,
and a **1–5**. Then one **overall** score for the idea.

Consider a model only if it fits: subscription, one-time IAP, freemium,
usage/API, take-rate/marketplace, B2B/SaaS (company or community), lead-gen,
affiliate, ads, white-label, services on top.

**Model 1–5** (economic potential short **and** long term):

| Score | Anchor |
|-------|--------|
| 1 | No payer; people expect it free; ads on a tiny audience |
| 2 | Weak willingness to pay; tips/donations; crowded free alternative |
| 3 | Plausible sub or B2B, modest ARPU, unproven in this niche |
| 4 | Clear payer, comparable products already charge, room to expand |
| 5 | Pays soon **and** compounds (high ARPU, expansion, switching costs) |

Overall Monetization: judge the **idea**, not the flashiest hypothetical model.
A B2B plan that needs an enterprise sales team this product will never have
is not a 5.

## Score anchors (higher = more attractive)

Integers only for the five section scores. Do not default to 3.

### Requirements (1 = very complex, 5 = tiny complexity)

| Score | Anchor |
|-------|--------|
| 1 | Two-sided marketplace, realtime, ML, payments, regulated data, two native apps, heavy ops |
| 2 | Full native + backend + several integrations / moderation |
| 3 | Standard CRUD: both platforms + API + auth + push |
| 4 | One platform or BaaS, few screens, little custom backend |
| 5 | Landing + sheet / almost no backend |

### Competition (1 = lots of competition, 5 = none)

| Score | Anchor |
|-------|--------|
| 1 | Strong incumbents + good status quo; same user, same job |
| 2 | Many direct apps; differentiation is a slogan |
| 3 | Some players; a niche or locale is still open |
| 4 | Mostly indirect or weak; local/workflow gap is real |
| 5 | No relevant competition — almost never; WhatsApp/Excel count |

### Risks (1 = high risk, 5 = no risk)

| Score | Anchor |
|-------|--------|
| 1 | Existential: legal ban, safety, marketplace with no distribution |
| 2 | Several High risks that can kill the product |
| 3 | Mix of Medium; survivable with the listed mitigations |
| 4 | Few, manageable risks |
| 5 | Negligible — use almost never |

### Action plan (1 = slow/hard, 5 = relatively fast to a credible v1)

| Score | Anchor |
|-------|--------|
| 1 | Years / hardware / heavy regulation / huge chicken-egg |
| 2 | Many months for two stores + backend + payments + trust |
| 3 | About a quarter for a small team to ship a real MVP |
| 4 | Weeks to a thin but usable v1 |
| 5 | Days–couple of weeks |

Score the **MVP**, not Phase 0 interviews.

## Scorecard math

Five scored sections. Total is the unweighted average:

```
total = (requirements + competition + monetization + risks + action_plan) / 5
```

Round to **one decimal** (e.g. 13 / 5 = 2.6).

## JSON schema (`ideas/<slug>/idea.json`)

Shared root, then full copies of the brief under `es` and `en`. Scores are
not translated. Full sample: `templates/idea.example.json`.

```json
{
  "slug": "hyphen-name",
  "working_name": "Display name",
  "date": "YYYY-MM-DD",
  "status": "draft",
  "gap_verdict": "real gap | partial gap | no clear gap",
  "scores": {
    "requirements": 1,
    "competition": 1,
    "monetization": 1,
    "risks": 1,
    "action_plan": 1,
    "total": 1.0
  },
  "es": { },
  "en": { }
}
```

Each locale object:

| Field | Shape |
|-------|--------|
| `working_name`, `thesis` | string |
| `idea.problem/solution/who_primary/who_secondary/who_not/why_now` | string |
| `idea.scope_in`, `idea.scope_out` | string[] |
| `requirements.mobile/backend/cross_cutting/score_why` | string |
| `competition.method/positioning/gap_verdict_text/score_why` | string |
| `competition.competitors[]` | `name, type, url, what, strengths, weaknesses, pricing, relevance` |
| `monetization.models[]` | `name, score, who_pays, how, short_term, long_term, v1_fit, why_score` |
| `monetization.recommended_v1`, `monetization.score_why` | string |
| `risks.{technical,product,market,legal,business}[]` | `{ "level": "High\|Medium\|Low", "text": "..." }` |
| `risks.score_why` | string |
| `action_plan.phase0/phase1/phase2/score_why` | string |
| `action_plan.next_14_days` | string[] |
| `open_questions` | string[] |

`type` of competitor: `direct` \| `indirect` \| `status quo`. `v1_fit`:
`yes` \| `later` \| `no`.

## PDF generator

From the skill directory:

```bash
python3 scripts/generate_idea_pdf.py \
  --brief ideas/<slug>/idea.json \
  --out ideas/<slug>
```

Stdlib only. Writes `<slug>-idea-es.pdf`, `<slug>-idea-en.pdf`, and
`<slug>-download.html` (browser save dialog for both files).

## Requirements — coverage checklist

If a bullet would apply and is missing, add it or put it in Out of v1.

**Mobile**

- OS + min version, phone/tablet, online-only vs offline
- Auth (email, social, passkeys, guest)
- Primary navigation and 5–12 core screens/flows
- Local storage / sync conflict behavior
- Push: which events
- Payments / subscriptions (store vs Stripe vs none)
- Permissions (camera, location, notifications) and why
- Empty, loading, error, permission-denied
- Accessibility and i18n

**Backend**

- Entities and who owns data
- Public/authenticated API surface (resources, not every endpoint)
- Authn/authz (sessions, tokens, roles)
- File/media storage
- Background jobs (email, digest, webhooks)
- Third-party APIs (maps, payments, LLM, auth) and failure mode if they die
- Admin: what a human must do in week 1
- Environments (dev/staging/prod) and secrets
- Privacy: retention, export, delete account (GDPR)

## Risk prompts

Write 2–4 bullets per category. Each: risk → why it matters → mitigation.

- **Technical:** sync, LLM cost/quality, store review, multiplatform, PII.
- **Product:** two-sided marketplace cold start, habit, "nice to have".
- **Market:** incumbent with distribution, free alternatives, SEO already owned.
- **Legal:** health, minors, payments, scraping, user-generated content.
- **Business:** who pays, support load, solo-maintainer bus factor.

## Action plan bar

Phase 0 must be **falsifiable**. Bad: "build landing and see". Good: "10
interviews with `{audience}` this fortnight; kill if fewer than 4 would pay
€X or switch from `{status quo}`."

Next 14 days: 5–8 tasks, each completable without a full engineering team.
