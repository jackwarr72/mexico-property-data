# Digest: Dimension 3 — Pain points & unmet needs
Round 1 · 2026-10-24 · Class: pain-points

## Verified (sourced)

| # | Claim | Source | Publisher | Pub date | Confidence |
|---|-------|--------|-----------|----------|------------|
| 3-1 | **Hard constraint:** "No se extraen portales de consumo restringidos (por ejemplo Inmuebles24, Lamudi o Mercado Libre)" — restricted portals explicitly NOT scraped | pdf_text.txt (Instructivo v1.0) | Project internal | 2026-09-23 | High |
| 3-2 | **Legal/compliance gating:** All 9 portal sources `status = restricted`, `legal_basis = partner required` / `not for mass scraping`; 17 community sources `enabled = false`, `crawl_policy = no_mass_scrape_without_permission` | data/export/source_configs.csv | Project internal | 2026-10-07 | High |
| 3-3 | **Pipeline gap:** Toluca & Metepec are *absent* from the current 10-listing snapshot (zero listings in primary focus area) | data/export/market_dashboard_by_city.csv | Project internal | 2026-10-07 | High |
| 3-4 | **Manual workflow:** "Consultar oferta, precios y fuentes sin hojas de cálculo dispersas" — spreadsheets are the current baseline | pdf_text.txt | Project internal | 2026-09-23 | High |
| 3-5 | **Community Q&A blind spot:** "Escuchar al mercado: analítica de preguntas, sentimiento y preocupaciones de la comunidad" — community signals not yet automated; community_content.csv is empty | pdf_text.txt + data/export/community_content.csv | Project internal | 2026-09-23 | High |
| 3-6 | **Price anchoring without spread:** "Un precio promedio sin su mínimo y su máximo induce a error: use la tabla completa" — need full price distribution, not just averages | pdf_text.txt | Project internal | 2026-09-23 | High |
| 3-7 | **Alert latency:** Manual Google searches (`site:`, `intitle:`, `inurl:`) for "Venta urgente"/"Reducción de precio" — no real-time feed | pdf_text.txt | Project internal | 2026-09-23 | High |

## Unverified (no public source obtained)

- Broker/agent pain points from interviews/surveys in Toluca-Metepec
- Developer pain points on market intelligence sourcing
- Investor pain points on data access/quality
- Buyer/seller pain points from community forums (Reddit, Facebook, Quora) — registry exists but content not yet imported

## Retrieval outcome

No public research on unmet data needs for property intelligence in these geographies. The project's own constraints and operational examples are the only evidence.

## Leads

- The project's roadmap (ROADMAP_FUTURO.md) explicitly lists "Reemplazar datos demo por agregaciones reales de community_content" and "Calcular preguntas, temas, sentimiento, intención y tendencias" as Phase 2 priorities — confirming these are recognized gaps.
- The community source registry (20 sources) is the designed path; it needs activation (official APIs, authorized exports, manual review).
- "Datos demo claramente etiquetados: nunca presente esos números como hallazgos de mercado" — the project already knows not to confuse pipeline output with market research.