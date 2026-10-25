# Digest: Dimension 1 — internal project data (context, NOT market size)
Round 1 · 2026-10-24 · Class: internal

Source: project files (data/export/*.csv, community_sources.json, ROADMAP_FUTURO.md, pdf_text.txt). These describe the *pipeline's own* coverage, not the external market. Cited as context only — the research firewall keeps them out of market-size claims.

## Current listing snapshot (data/export/market_dashboard_by_city.csv, Oct 2026)
10 listings across target municipalities:

| Municipality | Listings | Avg price (MXN) | Min | Max |
|---|---|---|---|---|
| Benito Juárez (CDMX) | 2 | 4,025,000 | 3,850,000 | 4,200,000 |
| Cuauhtémoc (CDMX) | 2 | 8,150,000 | 6,500,000 | 9,800,000 |
| Cuajimalpa (CDMX) | 1 | 7,100,000 | 7,100,000 | 7,100,000 |
| Miguel Hidalgo (CDMX) | 1 | 14,500,000 | 14,500,000 | 14,500,000 |
| Tlalpan (CDMX) | 1 | 4,700,000 | 4,700,000 | 4,700,000 |
| Álvaro Obregón (CDMX) | 1 | 6,300,000 | 6,300,000 | 6,300,000 |
| Naucalpan (Edo. México) | 1 | 8,600,000 | 8,600,000 | 8,600,000 |
| Tlalnepantla (Edo. México) | 1 | 2,550,000 | 2,550,000 | 2,550,000 |

Price bands: 2M–5M (4 listings, avg 4.25M), 5M–10M (5, avg 7.425M), 10M–20M (1, 14.5M).

**Note:** Toluca and Metepec themselves are *absent* from this snapshot — the pipeline's own coverage of the primary focus area is currently zero listings.

## Sources tracked (data/export/property_summary.csv)
9 sources: Public Registry MX (2, avg 6.65M), Casas y Terrenos (1, 2.55M), Inmuebles24 (1, 6.5M), Lamudi Mexico (1, 9.8M), Mercado Libre Inmuebles (1, 6.3M), Mitula Mexico (1, 3.85M), Propiedades.com (1, 4.2M), Vive Anuncios (1, 7.1M), iCasas.mx (1, 14.5M).

## Compliance posture (data/export/source_configs.csv)
- 9 portal/marketplace sources: all `status = restricted`, `legal_basis = partner required` / `not for mass scraping`
- 1 government source (Public Registry MX): `licensed public government dataset`, `allowed`
- 17 community/forum/social sources: `manual_review`, most `enabled = false`, `crawl_policy = no_mass_scrape_without_permission` / `no_scrape`

## Community source registry (community_sources.json)
20 sources targeting Toluca/Metepec + CDMX: InmobiliariaWeb forums, Lamudi forums, Vivanuncios discussions, Mercado Libre Real Estate Q&A (official API only), Propiedades.com community, Reddit (r/Mexico, r/MexicoFinanciero, r/EstadoDeMexico, r/PersonalFinanceMexico, r/mexicoexpats), Facebook groups (Compra Venta Toluca, Inmobiliarias Metepec, etc.), Quora Spanish housing, LinkedIn, local news (Milenio EdoMex, El Sol de Toluca), Infonavit/FOVISSSTE official Q&A, hashtag discovery.

## Operational context (pdf_text.txt, ROADMAP_FUTURO.md)
- Team targets: 20+ properties/day, 10+ appointments/week
- Example reading: Toluca team 23/09 → 24 properties captured, 3 appointments, 18 calls, 5 negotiation advances
- Metepec example: house with −12% price reduction converted to a Saturday visit
- Alert vocabulary in use: "Venta urgente", "Reducción de precio", "Urgent Sale", "Reduction Price", "remate", "liquidación"
- Analytics example: Metepec +38% increase in questions about "casas con estudio" (home-office), last 30 days
- Hard constraint: restricted portals (Inmuebles24, Lamudi, Mercado Libre) are explicitly NOT extracted; only authorized content is imported