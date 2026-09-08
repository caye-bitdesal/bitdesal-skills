# Example brief (quality bar)

Illustrative only. A real run must use live search, write **Spanish and
English** into `idea.json`, and generate PDFs. This sample shows length, tone,
and honesty for one language — not a market truth.

Canonical JSON (both locales): [templates/idea.example.json](templates/idea.example.json).

**User input:** "App para que vecinos se presten taladros y escaleras. Tipo
biblioteca de cosas en el edificio. En España."

---

# Vecindario (working title)

> Slug: `vecindario`
> Date: 2026-09-08
> Status: draft
> Gap verdict: partial gap
> Total score: 2.6/5

## Thesis

Inquilinos y propietarios en bloques urbanos de España ya se prestan
herramientas por el grupo de WhatsApp de la finca, con fricción, desconfianza
y objetos que se pierden. Vecindario sería una app móvil (iOS y Android) por
comunidad de vecinos: inventario compartido, reservas y reputación ligera,
con un backend que aísla cada finca. El hueco no es "nadie lo ha intentado",
sino una versión local, simple y por edificio frente a marketplaces de
alquiler entre desconocidos.

## Idea

### Problem

Quien vive en un piso no quiere comprar un taladro que usa dos veces al año.
El grupo de WhatsApp no tiene disponibilidad, depósito ni historial; prestarle
algo a un vecino nuevo da miedo. Las apps de alquiler P2P asumen extraños,
desplazamiento y comisión.

### Solution

Un inventario cerrado al portal / la comunidad: alta de objetos, franja de
reserva, recordatorio de devolución y un perfil mínimo de fiabilidad. Sin
feed público ni matching ciudad-entera en v1.

### Who it is for

- Primary: residentes de fincas de 20–80 viviendas en ciudades españolas
- Secondary: presidentes de comunidad que quieren reducir compras duplicadas
- Who it is not for: alquiler profesional de maquinaria, campus universitarios
  (different trust model)

### Why now

Hábitos de segunda mano y "usar en vez de poseer" ya existen; WhatsApp es el
workaround. Store kits and community apps are familiar. No hay un incumbente
español obvio *por finca* con buena UX móvil.

### Scope of v1

- In: una comunidad, inventario, reserva, chat in-app mínimo o deep-link a
  WhatsApp, push de "te toca devolver"
- Out: pagos, depósitos, varias fincas por usuario, mapa ciudad, IA

## Requirements

### Mobile

Must-have (v1): Android + iOS; auth email/Google; lista de objetos; ficha;
calendario de reserva; mis préstamos; notificaciones de solicitud y atraso;
estados vacío ("aún no hay taladro") y error de red.

Later: iPad, offline queue, pagos, fotos OCR, widgets.

### Backend

Must-have (v1): tenant por `community_id`; users, items, bookings; auth;
push (FCM/APNs); reglas: no solapar reservas; fotos en object storage;
export/delete account.

Later: pagos, moderación, analytics product, admin multi-finca.

### Cross-cutting

ES copy first; analytics mínimo (signups, items, bookings completed);
cuenta GDPR; revisión de stores (user-generated photos).

### Score

**Requirements: 3/5** — Two native apps, auth, push, photos and tenant isolation
are a standard CRUD product, not a marketplace-with-payments v1.

## Competitive analysis

### Method

Queries (sample): "app prestar herramientas vecinos", "library of things
app Spain", "Peerby", "Fat Llama", "alquiler herramientas particulares
app". Fetched vendor homepages. Date: 2026-09-08.

### Competitors

#### Peerby
- Type: direct (P2P borrow)
- URL: https://www.peerby.com
- What they do: préstamo/alquiler entre particulares por zona
- Strengths: marca, liquidez en algunos mercados
- Weaknesses / openings: no está diseñado como "esta finca"; cold start ciudad
- Relevance: closest product analog; different trust boundary

#### Fat Llama / similar rental marketplaces
- Type: indirect
- What they do: alquiler con seguro y comisión entre desconocidos
- Strengths: payments, insurance narrative
- Weaknesses: overkill and pricey for a drill two floors up
- Relevance: what we are *not*

#### WhatsApp de la comunidad
- Type: status quo
- What they do: el canal real
- Strengths: already installed, zero onboarding
- Weaknesses: no inventario, no calendario, ruido
- Relevance: the product to beat on ease, not on features

### Positioning

Win on *closed community + calendar*, not on city-wide supply. If we cannot
get a presidente or 8 neighbours in one building to list 15 items, Peerby
and WhatsApp already cover the job.

### Gap verdict

partial gap

Hay demanda del trabajo ("conseguir un taladro sin comprarlo"), pero el
canal dominante es WhatsApp y los P2P city-wide ya existen. Un producto
*por portal* puede encajar si la distribución es la comunidad (administrador,
QR en el rellano), no el store. No es un océano azul.

### Score

**Competition: 2/5** — Peerby-class P2P plus the WhatsApp group already do the
job; the opening is only "this building", not an empty category.

## Monetization

### Models

#### Cuota a la comunidad (B2B2C) — 3/5
- Who pays: la comunidad / administrador (o derrama)
- How it works: 9–19 €/mes por finca, usuarios gratis
- Short term: un presidente puede aprobar un gasto pequeño
- Long term: techo bajo (una finca = un dígito de ARPU) salvo multi-finca
- Fit for v1: later (first prove usage)
- Why this score: payer exists but budget is tiny and sales-cycle-ish

#### Freemium + IAP "finca Pro" — 2/5
- Who pays: un vecino entusiasta
- How it works: inventario limitado gratis; push y fotos extra de pago
- Short term: almost nobody pays to lend a drill
- Long term: consumer IAP in a utility with a free chat alternative
- Fit for v1: no
- Why this score: weak willingness to pay against WhatsApp

#### Take-rate / depósito — 2/5
- Who pays: prestatario, comisión o fianza
- How it works: como Fat Llama, seguro y cobro por préstamo
- Short term: kills the "it's just the neighbour" pitch
- Long term: only if you leave the building and become a city marketplace
- Fit for v1: no
- Why this score: fights the product thesis

#### Ads — 1/5
- Who pays: advertisers
- How it works: banners in a 40-person building app
- Short term / long term: inventory too small
- Fit for v1: no
- Why this score: no audience

### Recommended v1

Do not charge until one building completes loans weekly. Then test a
community fee (~10 €/mes) with the presidente — not consumer IAP.

### Score

**Monetization: 2/5** — plausible community fee, but small ARPU and a free
status quo; no strong short-term or compounding long-term path.

## Risks

### Technical
- **Medium** — fotos + push + dos stores: mitigation: BaaS or a thin API first.
- **Low** — scale: v1 is tiny; tenant isolation matters more than QPS.

### Product
- **High** — chicken-egg inside each building: mitigation: seed 10 items with
  the presidente before inviting the rest.
- **High** — nobody opens another app vs WhatsApp: mitigation: WhatsApp deep
  links for requests in v1.

### Market
- **Medium** — Peerby / marketplaces absorb "serious" lenders.
- **High** — switching cost of the existing group chat is ~zero until inventory
  hurts.

### Legal & compliance
- **Medium** — daño o pérdida de objetos: v1 disclaimers, no insurance.
- **Medium** — GDPR + fotos de interiores: retention and delete account.

### Business & operations
- **High** — unclear who pays (resident vs comunidad vs never).
- **Medium** — support ("no me lo han devuelto") does not scale.

### Score

**Risks: 2/5** — chicken-egg per building, WhatsApp inertia, unclear payer, and
object-loss disputes are several High/Medium killers, not a polish problem.

## Action plan

### Phase 0 — Validate (before building)

10 conversaciones en 2 fincas reales. Éxito: ≥4 personas listarían un objeto
esta semana y el presidente reenviaría un enlace. Fracaso: "lo hablamos por
el grupo" sin dolor.

### Phase 1 — MVP

Una comunidad piloto, inventario + reserva + push, sin pagos.

### Phase 2 — After signal

Segunda finca, métrica de préstamos completados / semana, entonces iOS
parity polish or waitlist.

### Next 14 days

1. Entrevistar 8 vecinos + 1 presidente (guion: última vez que necesitaron
   una herramienta).
2. Mapear 5 alternativas reales con URLs actualizadas (incl. locales ES).
3. Pretotipo: hoja compartida + grupo WA y medir 2 semanas.
4. Decidir kill / wedge (solo herramientas vs también libros/cables).
5. Solo si hay señal: sketch de 4 pantallas y modelo `community/item/booking`.

### Score

**Action plan: 4/5** — a thin v1 (one community, inventory, booking, push, no
payments) is weeks for a small team after validation, not a multi-year build.

## Scorecard

| Section | Score (1–5) | Meaning of 1 | Meaning of 5 |
|---------|-------------|--------------|--------------|
| Requirements | 3 | Very complex | Very little complexity |
| Competition | 2 | Lots of competition | No competition |
| Monetization | 2 | Little economic potential | High potential short + long term |
| Risks | 2 | High risk | No risk |
| Action plan | 4 | Slow / hard to implement | Relatively fast to implement |
| **Total** | **2.6** | | (3+2+2+2+4) / 5 |

## Open questions

- ¿El administrador de fincas es el canal de distribución?
- ¿v1 permite comunidades abiertas (amigos) o solo un código de portal?
