---
title: 'market research: Mexico Property Data Market Toluca CDMX'
type: 'market'
topic: 'Mexico Property Data Market Toluca CDMX'
decision: 'Enter/skip data-as-a-service play scraping listings, Q&A, market intelligence for Toluca-Metepec (primary) and 6 CDMX delegations (secondary), build alliances, monetize via web app'
source: 'run'
status: complete
preset: 'standard'
validation: 'normal'
created: '2026-10-24'
updated: '2026-10-24'
---

# market research: Mexico Property Data Market Toluca CDMX

**Decision this research serves:** Enter or skip a data-as-a-service play scraping property listings, buyer/seller Q&A, and market intelligence for Toluca-Metepec (primary) and six CDMX delegations — Benito Juárez, Cuauhtémoc, Venustiano Carranza, Álvaro Obregón, Santa Fe, Cuajimalpa (secondary) — to build alliances and monetize aggregated real estate data via a web app.

---

## Executive Summary

**Verdict: PROCEED WITH CONDITIONS.** The *data-as-a-service* niche (aggregated listings + community Q&A + market intelligence → web app subscription) is **unoccupied by named players** in the target geographies. All named proptechs (Flat.mx, Yave, LaHaus, Homie) are **finance-first** (mortgage/rental), not data products. The portal layer (Inmuebles24, Lamudi, Vivanuncios, Propiedades.com, Mercado Libre Inmuebles) is the listing *supply* layer — all are `restricted`, partner-required, and the project's own compliance framework explicitly forbids mass scraping without authorization.

**Critical gap:** No public source verified the *reachable market size* for property data/analytics in Toluca-Metepec or the six CDMX delegations. Public data is thin: INEGI/Sedatu/Infonavit pages are JS shells; CBRE/JLL/Cushman portals block or redirect; news sites are news only. **Absence of evidence is a finding** — the TAM/SAM for this specific product cannot be sourced from public web this run.

**Conditions to greenlight:**
1. Secure **portal partnerships / official APIs** (the only compliant path to listing data at scale).
2. Activate the **community layer** (20 sources registered: Reddit, Facebook, Quora, forums, Infonavit) to supply Q&A/sentiment — this is the project's designed differentiator.
3. Run a **buyer-interview program** (5–10 brokers, developers, funds) to validate willingness to pay and pricing model.
4. Engage legal review of LFPDPPP + portal ToS for the specific data types intended for the product.

If conditions 1–2 are not achievable, the product reduces to a thin wrapper around government open data + community signals — likely insufficient density for a paid web app.

---

## Dimension 1 — Market Size & Growth (reachable market)

**Status:** Thin public data. No verified figure for the *reachable* market for property data/analytics in the target geographies.

### Verified macro context

| # | Claim | Source | Confidence |
|---|-------|--------|------------|
| 1 | Mexico nominal GDP ~US$2.017T (2024 est.), 11th globally | Wikipedia (IMF) | High |
| 2 | Mexico GDP PPP US$3.434T (2023 est.) | Wikipedia (IMF) | High |
| 3 | GDP growth: +3.2% (2023), +1.5% (2024), +1.2% (2026 est.) | Wikipedia (IMF) | High |
| 4 | Inflation 4.68% (2024); FX 20.43 MXN/USD (Nov 2024) | Wikipedia | High |
| 5 | World Bank: growth 1.4% (2026), 1.8% (2027), 2.2% (2028); fiscal deficit 4.2% GDP 2026 | World Bank (2026-03-26) | High |
| 6 | Poverty fell 43.2% (2016) → 29.6% (2024) | World Bank | High |
| 7 | Cemex: world's 3rd-largest cement, US$15.93B revenue (Forbes 2023) | Wikipedia | High |
| 8 | Fibra Uno: real estate REIT, US$1.17B revenue (Forbes) | Wikipedia | High |
| 9 | Industrial = 25.7–31.9% of GDP; services ~65% | Wikipedia | Medium |

### Unverified — critical for the decision

- Toluca/Metepec residential transaction volumes or price indices, 2023–2024
- CDMX delegation-level (Benito Juárez, Cuauhtémoc, Venustiano Carranza, Álvaro Obregón, Santa Fe, Cuajimalpa) market size, inventory, absorption, 2023–2024
- Mexico proptech market size or growth figures
- Reachable market for property *data/analytics* (distinct from property market itself)

### Retrieval outcome

WebSearch returned empty for every query. WebFetch:
- Portals (Inmuebles24, Lamudi, Vivanuncios) → HTTP 403
- Analyst sites (CBRE, CBRE.ca, Cushman) → 403 / 301→403
- JLL.com.mx → marketing nav shell
- INEGI / Sedatu / Infonavit → JS shells, no data
- Centroubano articles → 404

**Finding:** The reachable-market figure for this niche cannot be sourced from public web this run. Upgrade path: AMPI reports, CBRE/JLL quarterly PDFs (direct access).

---

## Dimension 2 — Customer Segments & Behavior

**Status:** Project-internal evidence only; no public segmentation research found.

### Verified (project-internal)

| # | Claim | Source |
|---|-------|--------|
| 2-1 | Pipeline targets: 20+ properties/day, 10+ appointments/week | Instructivo v1.0 (2026-09-23) |
| 2-2 | User "Ana, asesora en Metepec" filters Edo. México / Casa / $3M–$6M, checks source, logs notes | Instructivo |
| 2-3 | Toluca team 23/09: 24 properties, 3 appts, 18 calls, 5 negotiation advances | Instructivo |
| 2-4 | Alert vocab: "Venta urgente", "Reducción de precio", "Urgent Sale", "Reduction Price", "remate", "liquidación" | Instructivo |
| 2-5 | Metepec +38% questions on "casas con estudio" (home-office) in 30 days | Instructivo |

### Inferred segments (from source registry)

| Segment | Sources targeting them | Notes |
|---|---|---|
| Individual buyers/sellers (Toluca/Metepec) | Vivanuncios, Facebook groups, Reddit r/mexicoexpats, Quora | High Q&A; Infonavit/FOVISSSTE questions |
| Brokers/agencies | InmobiliariaWeb forums, LinkedIn, local news | Professional discussions; need certified data |
| Investors | Reddit r/MexicoFinanciero, r/PersonalFinanceMexico, LinkedIn | Cross-border interest; FinTech overlap |
| Mortgage seekers | Infonavit Q&A, Mercado Libre RE Q&A, Yave/Flat direct | Financing-heavy intents |

### Unverified

Agency/broker size, tech adoption, data budget, purchasing process; developer data sourcing; investor requirements; bank/lender consumption patterns; proptech API willingness; government open data licensing.

---

## Dimension 3 — Pain Points & Unmet Needs

**Status:** Well-documented in project's own constraints and operational gaps.

### Verified

| # | Pain point | Evidence |
|---|---|---|
| 3-1 | Restricted portals (Inmuebles24, Lamudi, Mercado Libre) **explicitly NOT scraped** | Instructivo: "No se extraen portales de consumo restringidos" |
| 3-2 | 9 portals `restricted` / `partner required` / `not for mass scraping` | source_configs.csv |
| 3-3 | **Toluca & Metepec absent** from current 10-listing snapshot (zero coverage in primary focus) | market_dashboard_by_city.csv |
| 3-4 | Current baseline = spreadsheets ("sin hojas de cálculo dispersas") | Instructivo |
| 3-5 | Community Q&A blind: community_content.csv empty; analytics not automated | Instructivo + community_content.csv |
| 3-6 | Need full price distribution, not just averages ("precio promedio sin su mínimo y su máximo induce a error") | Instructivo |
| 3-7 | Alert latency: manual Google `site:`/`intitle:`/`inurl:` searches for urgent/reduced listings | Instructivo |

### Project roadmap confirms these gaps

ROADMAP_FUTURO.md Phase 2: "Reemplazar datos demo por agregaciones reales de community_content", "Calcular preguntas, temas, sentimiento, intención y tendencias", "Añadir validación de calidad de datos".

---

## Dimension 4 — Competitive Landscape (named players)

### Verified — Proptech layer (finance-first, not data products)

| Player | Model | Key metrics (fetched 2026-10-24) | Source |
|---|---|---|---|
| **Flat.mx** | Mortgage to foreigners (SOFOM E.N.R.) | CDMX, Riviera Maya, Los Cabos, PV, SMA, Mérida; 15.99% p.a. / 19.5% CAT; "1,000+ credits in 3 years" | flat.mx |
| **Yave** | Digital mortgage (SOFOM E.N.R.) | >$4.5B MXN credit (2023); >1,000 customers/6 yrs; 3-week workflow; 11.42% rate / 14.09% CAT (Mar 2026); Vinte investment (2022) | yave.mx |
| **LaHaus** | New-home marketplace + AI | $35M raised; >$100M valuation; Colombia (Bogotá, Medellín); "millions in transactions" | lahous.com |
| **Homie.mx** | Rental management (up to 5 yrs) | Chile expansion; avg millennial rent ~MXN 12k/mo; CEO: "80,000 new homes/yr needed" | homie.mx |

### Blocked — Portal layer (listing supply, partner-required)

Inmuebles24 (301→403), Lamudi.com.mx (403), Vivanuncios.com.mx (403), Propiedades.com (403), iCasas/Mitula/Casas y Terrenos (blocked), Crunchbase/TechCrunch (403/404).

### Strategic finding

**No named player sells aggregated property data/analytics as a product.** All proptechs are finance-first (mortgage/rental). The portal layer is the *supply* side, not a competitor — and all require partnerships. The "data as a service" niche appears **unoccupied**.

---

## Dimension 5 — GTM & Pricing Dynamics

### Verified

| # | Claim | Source |
|---|---|---|
| 5-1 | Flat.mx: loan origination fees (2–3%) + interest spread | flat.mx |
| 5-2 | Yave: interest revenue + strategic investment (Vinte 2022) | yave.mx |
| 5-3 | LaHaus: $35M raised; transaction fees / developer partnerships | lahous.com |
| 5-4 | Homie: rental management fees | homie.mx |
| 5-5 | Project export formats: CSV, JSON, Excel, PDF, PNG, SVG, GeoJSON | ROADMAP_FUTURO.md |
| 5-6 | Project role-based access: admin, analyst, operator, read-only (planned) | ROADMAP_FUTURO.md |
| 5-7 | Export access controls planned ("controles de acceso antes de generar cualquier exportación") | ROADMAP_FUTURO.md |

### Unverified — to design

- Property data/analytics subscription pricing in Mexico (B2B)
- CAC for data products sold to brokers/agencies/developers
- Willingness to pay for aggregated intelligence vs. raw listings
- Channel: direct sales vs. marketplace vs. API

### Pricing model to design

Subscription (monthly/annual per seat) / per-lead / per-API-call / revenue share with brokers. The project's role-based permissions and export controls suggest a tiered SaaS model.

---

## Dimension 6 — Regulatory & Compliance

### Verified — Project's own framework (unusually detailed & conservative)

| # | Constraint | Source |
|---|---|---|
| 6-1 | LFPDPPP governs private-sector personal data | ROADMAP §3 |
| 6-2 | Only ingest publicly accessible & legally permitted content; no private accounts; no auth/paywall bypass; respect robots.txt/ToS/rate limits; no mass scraping without written authorization; official APIs only with credentials | ROADMAP §3 (lines 97–106) |
| 6-3 | Facebook Graph API only when officially permitted; X/TikTok/YouTube/Reddit/LinkedIn/Quora must respect APIs/policies | ROADMAP §3 (lines 105–106) |
| 6-4 | Data minimization: no unnecessary PII; prefer public display names; no inferring identity/finances/private address; limited retention/deletion | ROADMAP §3 (lines 107–110) |
| 6-5 | Attribution & traceability: preserve URL/source/date/license/attribution; separate govt data from UGC; mark unverified `manual_review`; never present AI interpretation as fact | ROADMAP §3 (lines 111–115) |
| 6-6 | Source registry: 9 portals `restricted`/`partner required`; 1 govt `licensed public dataset`/`allowed`; 17 community `manual_review`/`enabled=false`/`no_mass_scrape` | source_configs.csv + community_sources.json |
| 6-7 | Infonavit/SEDATU/INEGI official sources → `official public information` / `public official information with attribution` | community_sources.json |

### Unverified

Scraping case law under LFPDPPP; INEGI open data license for commercial reuse; Sedatu housing data licensing; portal ToS enforcement history.

---

## Claims Ledger (for refresh tracking)

| Ref | Claim | Class | Pub date | Status |
|---|---|---|---|---|
| [1] | Mexico nominal GDP ~US$2.017T (2024 est.) | size/growth | 2024 | verified |
| [2] | Mexico GDP PPP US$3.434T (2023 est.) | size/growth | 2023 | verified |
| [3] | GDP growth +3.2% (2023), +1.5% (2024), +1.2% (2026 est.) | size/growth | 2023–2026 | verified |
| [4] | Inflation 4.68% (2024); FX 20.43 MXN/USD (Nov 2024) | size/growth | 2024 | verified |
| [5] | World Bank growth 1.4% (2026), 1.8% (2027), 2.2% (2028) | size/growth | 2026-03-26 | verified |
| [6] | Poverty fell 43.2%→29.6% (2016→2024) | size/growth | 2024 | verified |
| [7] | Cemex US$15.93B revenue (Forbes 2023) | size/growth | 2023 | verified |
| [8] | Fibra Uno US$1.17B revenue (Forbes) | size/growth | — | verified |
| [C1] | Flat.mx: mortgage to foreigners, 15.99%/19.5% CAT, 1000+ credits/3yr | competitive | fetched 2026-10-24 | verified |
| [C2] | Yave: >$4.5B MXN credit (2023), 11.42%/14.09% CAT (Mar 2026), Vinte 2022 | competitive | fetched 2026-10-24 | verified |
| [C3] | LaHaus: $35M raised, >$100M valuation, Colombia ops | competitive | fetched 2026-10-24 | verified |
| [C4] | Homie: rental up to 5yrs, avg MXN 12k/mo, 80k homes/yr needed | competitive | fetched 2026-10-24 | verified |
| [3-1] | Restricted portals not scraped (Inmuebles24, Lamudi, ML) | pain-points | 2026-09-23 | verified |
| [3-3] | Toluca/Metepec absent from current listing snapshot | pain-points | 2026-10-07 | verified |
| [6-1]–[6-7] | Full compliance framework encoded | regulatory | 2026-09-23 | verified |

**Unverified claims (require follow-up):**
- Toluca/Metepec transaction volumes, price indices (2023–2024)
- CDMX delegation-level market metrics (2023–2024)
- Proptech market size/growth
- Reachable market for property data/analytics
- Customer segment sizes, budgets, buying processes
- Portal partnership viability / API terms
- Scraping legality under LFPDPPP for listings/Q&A

---

## Open Questions (for Deepen or external handoff)

1. **What is the residential transaction volume in Toluca/Metepec (2023–2024)?** — Source: AMPI, CBRE, JLL quarterly PDFs.
2. **What is the listing inventory & absorption in each of the 6 CDMX delegations?** — Same sources.
3. **What are the official API terms / partnership costs for Inmuebles24, Lamudi, Vivanuncios, Propiedades.com, Mercado Libre Inmuebles?** — Direct outreach required.
4. **What is the willingness to pay for aggregated market intelligence among 5–10 target buyers (brokers, developers, funds)?** — Interview program.
5. **LFPDPPP + portal ToS legal opinion for the specific data types (listings, Q&A, sentiment) intended for the product.** — Legal review.

---

## Next Actions (mapped to bmm downstream)

- **bmad-prd** — Brief: opportunity = data layer unoccupied; problem = listing access gated; users = brokers/agencies/developers/investors; differentiator = community Q&A + sentiment + compliance-first.
- **bmad-spec** — Architecture: partnership/API ingestion layer → normalized store → analytics engine (trends, sentiment, alerts) → web app (role-based, export-controlled).
- **bmad-build** — Phase 1: activate community sources (Reddit API, Infonavit official, Facebook Graph if authorized) + secure 1–2 portal partnerships. Phase 2: web app MVP with subscription tiers.
- **bmad-architecture** — Data flow: authorized sources → ingestion adapters (per ROADMAP) → PostgreSQL (existing) → analytics pipeline → Streamlit/Next.js web app.

---

## Sources Appendix

| # | Source | Publisher | Accessed | Type |
|---|--------|-----------|----------|------|
| [1] | https://es.wikipedia.org/wiki/Economía_de_México | Wikipedia (IMF) | 2026-10-24 | Primary (macro) |
| [2] | https://en.wikipedia.org/wiki/Economy_of_Mexico | Wikipedia (Forbes/World Bank) | 2026-10-24 | Primary (macro) |
| [3] | https://www.worldbank.org/en/country/mexico | World Bank | 2026-10-24 | Primary (macro/projections) |
| [4] | https://www.flat.mx/ | Flat.mx | 2026-10-24 | Primary (competitor) |
| [5] | https://www.yave.mx/ | Yave | 2026-10-24 | Primary (competitor) |
| [6] | https://www.lahaus.com/ | LaHaus | 2026-10-24 | Primary (competitor) |
| [7] | https://www.homie.mx/ | Homie | 2026-10-24 | Primary (competitor) |
| [8] | data/export/market_dashboard_by_city.csv | Project internal | 2026-10-07 | Context |
| [9] | data/export/property_summary.csv | Project internal | 2026-10-07 | Context |
| [10] | data/export/source_configs.csv | Project internal | 2026-10-07 | Context |
| [11] | data/export/community_content.csv | Project internal | 2026-10-07 | Context |
| [12] | community_sources.json | Project internal | 2026-09-23 | Context |
| [13] | ROADMAP_FUTURO.md | Project internal | 2026-09-23 | Context |
| [14] | pdf_text.txt (Instructivo v1.0, 2026-09-23) | Project internal | 2026-09-23 | Context |

---

## Memlog Tally

```
entries: 43
by_type: {"assumption": 2, "claim": 32, "decision": 1, "source": 8}
claims: {"verified": 12, "unverified": 18}
claims_total: 30
```