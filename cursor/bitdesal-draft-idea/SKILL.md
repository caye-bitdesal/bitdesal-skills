---
name: bitdesal-draft-idea
description: >-
  Turns a short project idea into bilingual PDF briefs (Spanish and English):
  polished idea, mobile and backend requirements, competitive analysis,
  monetization study, risks, action plan, 1–5 scores, and a download page so
  the user can save the PDFs anywhere. Use when the user runs /bitdesal-draft-idea.
disable-model-invocation: true
---

# /bitdesal-draft-idea

Turn a few lines of raw idea into a decision-ready product brief as **two
PDFs** (Spanish and English). Research the market before claiming there is a
gap. Score five sections 1–5 (higher = more attractive) and average them. Do
not cheerlead.

## Invocation

```text
/bitdesal-draft-idea <a few lines describing the idea>
```

The text after the command is the idea. If it is missing, ask for 3–8 lines
before starting (problem, who it is for, what the app would do).

Draft the brief in **Spanish and English** (faithful translation, same scores).
Content fields follow the template below; the deliverable is PDF, not markdown.

## Workflow

Copy this checklist and track progress:

```text
Idea Progress:
- [ ] Step 1: Ingest and name the idea
- [ ] Step 2: Ask only blocking unknowns
- [ ] Step 3: Research competition and monetization (mandatory web search)
- [ ] Step 4: Draft the brief in ES + EN and score each section
- [ ] Step 5: Write idea.json, generate PDFs, open the download page
```

### Step 1: Ingest and name the idea

From the user's lines, infer a working **name**, a lowercase hyphenated
**slug**, and a one-sentence thesis. If the user already named it, keep that
name. Do not invent a cute brand if a descriptive working title is enough.

### Step 2: Ask only blocking unknowns

Ask at most 4 questions, only if the answer would change the brief. Batch them
in one message. Skip anything already clear.

Ask when missing:

| Area | Ask |
|------|-----|
| Platforms | iOS, Android, both, web too? |
| Geography / language | Where would it launch first? |
| User | Who pays / who uses it? |
| Constraint | Hard constraint (regulated domain, existing stack, must-ship date) |

If the idea is already enough to research, **do not wait** — proceed and state
assumptions in the brief. Never invent product decisions silently as facts.

### Step 3: Research competition and monetization (mandatory)

You **must** search the live web. Training-memory names are not evidence.

Read [reference.md](reference.md) for query patterns. Then:

1. Run several `WebSearch` queries (category, "app", region, adjacent tools,
   pricing, "how they make money").
2. `WebFetch` 2–4 of the strongest competitor pages (site, store listing,
   pricing, or Product Hunt) to verify what they actually do and how they
   charge.
3. List **direct**, **indirect**, and **status-quo** alternatives (spreadsheets,
   WhatsApp groups, doing nothing).
4. Note competitor monetization (ads, sub, take-rate, B2B, freemium, none).
5. End with an honest **gap verdict**: real gap, partial gap, or no clear gap.

If search fails or returns little, say so. Do not pad the section with
hypothetical startups.

### Step 4: Draft the brief (ES + EN) and score

Fill every section of the template **twice**: `es` and `en` in the JSON
schema in [reference.md](reference.md). Same facts and **identical scores**.
Translate; do not rewrite the strategy in the second language.

Requirements must cover **mobile and backend**. Risks must mix technical and
non-technical. Monetization must list concrete models with a 1–5 each, plus
one overall monetization score. The action plan must start with validation.

Score **Requirements**, **Competitive analysis**, **Monetization**, **Risks**,
and **Action plan** using the 1–5 anchors in [reference.md](reference.md).
Higher is always more attractive. Justify each score. Do not default to 3.
Total = sum ÷ 5 (one decimal).

Quality bar: specific names, platforms, and sources. If the idea is weak, low
scores and still complete the brief.

### Step 5: Generate PDFs and let the user save them

1. Write `ideas/<slug>/idea.json` (schema and example in [reference.md](reference.md);
   sample at `templates/idea.example.json`).
2. Run the generator. Locate `scripts/generate_idea_pdf.py` next to this
   `SKILL.md` (when installed: `.cursor/skills/bitdesal-draft-idea/scripts/`):

```bash
python3 <skill-dir>/scripts/generate_idea_pdf.py \
  --brief ideas/<slug>/idea.json \
  --out ideas/<slug>
```

This writes:

- `ideas/<slug>/<slug>-idea-es.pdf`
- `ideas/<slug>/<slug>-idea-en.pdf`
- `ideas/<slug>/<slug>-download.html`

3. **Open the download HTML** so the user can click and pick a folder:
   - Prefer `open_resource` with a `file://` URI to
     `ideas/<slug>/<slug>-download.html`.
   - If a browser tool is available, navigate to that file as well.
4. In chat, show: working name, gap verdict, the scorecard, paths to both
   PDFs, and tell the user to use the two buttons (**Descargar PDF en español**
   / **Download English PDF**). The browser save dialog is how they choose
   where to keep the files.
5. Also offer: if they paste a destination folder, copy both PDFs there
   (`cp` the two `.pdf` files; do not move the workspace copies). Confirm the
   copied paths.

Do not commit unless the user asks. Do not skip the download page.

## Brief template

This is the **content** outline (what must exist in `es` and `en` of
`idea.json`). Do not write `idea.md`. Headings below are for you; the PDF
generator localizes them.

```markdown
# <Working name>

> Slug: `<slug>`
> Date: <YYYY-MM-DD>
> Status: draft
> Gap verdict: <real gap | partial gap | no clear gap>
> Total score: <average of 5 section scores, one decimal>/5

## Thesis

<One paragraph: who, problem, proposed product, why now.>

## Idea

### Problem
<Who hurts, how often, what they do today, cost of the status quo.>

### Solution
<What the product is, in concrete user terms. Not a feature dump.>

### Who it is for
- Primary:
- Secondary (optional):
- Who it is not for:

### Why now
<Timing: regulation, platform shift, habit, distribution, tech that just became cheap.>

### Scope of v1
- In:
- Out:

## Requirements

### Mobile
Platforms, core screens/flows, auth, offline/sync, push, payments, permissions,
empty/error states, accessibility. Split **must-have (v1)** vs **later**.

### Backend
Domain model, APIs, auth/identity, storage, jobs/queues, third-party
integrations, admin/ops, environments, security/privacy baseline. Split
**must-have (v1)** vs **later**.

### Cross-cutting
Analytics, feature flags, i18n, App Store / Play compliance, backup, support.

### Score
**Requirements: <1–5>/5** — 1 = very complex; 5 = very little complexity.
<one-sentence why>

## Competitive analysis

### Method
<Queries run and date. Note if search was thin.>

### Competitors

For each (aim for 4–8 real ones):

#### <Name>
- Type: direct | indirect | status quo
- URL:
- What they do:
- Strengths:
- Weaknesses / openings:
- Pricing (if found):
- Relevance to us:

### Positioning
<One paragraph: how this idea would sit vs the set above.>

### Gap verdict
<real gap | partial gap | no clear gap>

<2–4 sentences of evidence. Name the underserved need or say the category is
crowded and what that implies (don't build / niche down / copy with distribution).>

### Score
**Competition: <1–5>/5** — 1 = lots of competition; 5 = no relevant competition
(status quo counts). <one-sentence why>

## Monetization

Suggest **3–6** concrete ways this app could make money. Score **each model
1–5**: 1 = little economic potential, 5 = strong potential **short and long
term**. Use competitor pricing from Step 3. Then give one **overall**
Monetization score for the idea (not a blind average of the models).

### Models

#### <Model name> — <1–5>/5
- Who pays:
- How it works:
- Short term:
- Long term:
- Fit for v1: yes / later / no
- Why this score:

### Recommended v1
<Which model, price point if known, what must be true before charging.>

### Score
**Monetization: <1–5>/5** — overall economic potential of the idea.
<one-sentence why>

## Risks

Rate each **High / Medium / Low** with a one-line mitigation.

### Technical
<Architecture, platforms, data, AI, 3rd-party APIs, scale, offline, security.>

### Product
<Adoption, habit, chicken-egg, scope creep, trust.>

### Market
<Competition, switching costs, timing, distribution.>

### Legal & compliance
<GDPR/privacy, payments, regulated content, IP, stores.>

### Business & operations
<Monetization, CAC, support load, team capacity, single-vendor lock-in.>

### Score
**Risks: <1–5>/5** — 1 = severe / existential risk; 5 = negligible risk.
Use 5 almost never. <one-sentence why>

## Action plan

### Phase 0 — Validate (before building)
Concrete checks that could kill or reshape the idea (talks, landing, pretotype).

### Phase 1 — MVP
Smallest shippable loop. Map to the v1 requirements above.

### Phase 2 — After signal
What you only do if Phase 0/1 worked.

### Next 14 days
Numbered, owner-agnostic tasks for the coming two weeks. First items are
research/validation, not scaffolding a repo.

### Score
**Action plan: <1–5>/5** — 1 = slow / hard to ship; 5 = relatively little time
to a credible v1 (not the pretotype). <one-sentence why>

## Scorecard

All scales: **higher = more attractive**. Total = (sum of the five scores) ÷ 5.

| Section | Score (1–5) | Meaning of 1 | Meaning of 5 |
|---------|-------------|--------------|--------------|
| Requirements | <n> | Very complex | Very little complexity |
| Competition | <n> | Lots of competition | No competition |
| Monetization | <n> | Little economic potential | High potential short + long term |
| Risks | <n> | High risk | No risk |
| Action plan | <n> | Slow / hard to implement | Relatively fast to implement |
| **Total** | **<average, one decimal>** | | Average of the five scores |

## Open questions
- …
```

## Rules

- Never skip competitive research because the idea "sounds unique".
- Never list fake competitors. Unverified names from memory must be confirmed
  with search or dropped.
- Mobile + backend requirements are both required. If v1 is mobile-only UX,
  still specify the API, data, and auth the app needs.
- Prefer an honest "no clear gap" over a flattering brief.
- Always include Monetization, five section scores, and the Scorecard. Total
  is (requirements + competition + monetization + risks + action plan) / 5.
- Always produce **both** PDFs (ES and EN) and open the download HTML.
- Do not implement the product in this skill. The output is the brief only.
- Workspace files: `ideas/<slug>/idea.json`, two PDFs, and the download HTML.
  Do not write `idea.md`.

## Example

Content quality: [example.md](example.md). JSON shape:
[templates/idea.example.json](templates/idea.example.json). Research and schema:
[reference.md](reference.md).
