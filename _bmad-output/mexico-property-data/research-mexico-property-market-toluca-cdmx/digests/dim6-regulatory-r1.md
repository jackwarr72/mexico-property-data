# Digest: Dimension 6 — Regulatory & compliance
Round 1 · 2026-10-24 · Class: regulatory

## Verified (sourced)

| # | Claim | Source | Publisher | Pub date | Confidence |
|---|-------|--------|-----------|----------|------------|
| 6-1 | **LFPDPPP applies:** Federal Law on Personal Data Protection (Ley Federal de Protección de Datos Personales en Posesión de los Particulares) governs private-sector personal data handling in Mexico. | ROADMAP_FUTURO.md (constraints section) | Project internal | 2026-09-23 | High |
| 6-2 | **Hard constraints listed:** Only ingest publicly accessible & legally permitted content; no private accounts/groups; no auth bypass; no paywall evasion; respect robots.txt/ToS/rate limits; no mass scraping restricted portals without written authorization; use official APIs only with credentials/authorized scope. | ROADMAP_FUTURO.md §3 (lines 97–106) | Project internal | 2026-09-23 | High |
| 6-3 | **Platform-specific:** Facebook Graph API only when officially permitted; X/Twitter, TikTok, YouTube, Reddit, LinkedIn, Quora must respect their APIs/policies. | ROADMAP_FUTURO.md §3 (lines 105–106) | Project internal | 2026-09-23 | High |
| 6-4 | **Data minimization:** No unnecessary personal data; prefer public display names; no inferring identity/finances/private address; limited retention & deletion. | ROADMAP_FUTURO.md §3 (lines 107–110) | Project internal | 2026-09-23 | High |
| 6-5 | **Attribution & traceability:** Preserve URL, source, date, license, attribution requirements; separate official govt data from user-generated; mark unverified as `manual_review`; never present AI interpretation as fact. | ROADMAP_FUTURO.md §3 (lines 111–115) | Project internal | 2026-09-23 | High |
| 6-6 | **Source registry compliance posture:** 9 portals → `restricted` / `partner required` / `not for mass scraping`; 1 govt → `licensed public government dataset` / `allowed`; 17 community → `manual_review` / mostly `enabled = false` / `no_mass_scrape_without_permission`. | data/export/source_configs.csv + community_sources.json | Project internal | 2026-10-07 | High |
| 6-7 | **INEGI / Sedatu / Infonavit** — official government sources; Infonavit Q&A marked `official public information` / `public official information with attribution`. | community_sources.json | Project internal | 2026-09-23 | High |

## Unverified (no public source obtained this run)

- Specific scraping case law in Mexico (LFPDPPP enforcement vs. web scraping)
- INEGI open data license terms for commercial reuse
- Sedatu housing data licensing
- Portal ToS enforcement history (Inmuebles24, Lamudi, Vivanuncios, Propiedades.com, Mercado Libre)

## Retrieval outcome

INEGI, Sedatu, Infonavit web pages are JS-rendered nav shells with no license text in fetched content. No public legal analysis of scraping vs. LFPDPPP for real estate listings found.

## Leads

- The project's own compliance framework (ROADMAP §3) is unusually detailed and restrictive — it already encodes a conservative, partnership-based stance.
- The "data as a service" decision hinges on whether a partnership/API model with portals is viable, or whether the *community* + *government* layers alone provide sufficient data density.
- Upgrade path: legal review of LFPDPPP + portal ToS for the specific data types (listings, Q&A, sentiment) intended for the product.