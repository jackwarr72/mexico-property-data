---
id: SPEC-fabrica-intel
companions:
  - architecture-diagrams.md
sources:
  - _bmad-output/mexico-property-data/prd-fabrica-intel/prd.md
---

# SPEC — Fábrica Intel Real Estate Intelligence SaaS

## Why

**Opportunity to capture.** The data-as-a-service niche for real estate intelligence in Toluca-Metepec and 6 CDMX delegations is unoccupied — all named proptechs are finance-first, and the portal listing layer is gated behind partnerships. Fábrica Intel converts authorized property data + community intelligence into broker-grade advisory, turning the dispersion of day-to-day broker work into repeatable deal-closing routines.

**Build target (90-day MVP):** all seven capabilities live behind Starter/Growth tiers; 10 of 20 registered community sources activated (Reddit API, Infonavit, forums, local news); 1 portal partnership or official API secured; LFPDPPP compliance review complete.

## Capabilities

- **CAP-1 — Ingestion adapters**
  - **intent:** System ingests authorized source data into normalized records, gated by `source_registry.legal_basis`/`access_method`/`status`, so only enabled sources with permitted use contribute.
  - **success:** Every ingested record carries source attribution (URL, platform, date, legal_status); a restricted source with no partnership/API credentials produces zero records and logs a compliance refusal.

- **CAP-2 — Analytics engine**
  - **intent:** System computes property aggregations (price distribution, inventory, DOM, price/m² heatmap, transaction velocity) and community aggregations (topic modeling, sentiment polarity, intent classification, trend detection, neighborhood profiles, pain points) so the dashboard and advisory briefs answer colonia-level questions from one consistent dataset.
  - **success:** Dashboard views load under 3 seconds; any colonia filter returns min/max/median price, DOM distribution, and neighborhood sentiment in a single query.

- **CAP-3 — Alert engine**
  - **intent:** System evaluates alert rules (price-drop %, urgency keywords, saved-criteria matches, development/zoning signals, competitive events) on each ingestion cycle and delivers alerts via in-app, email, webhook, or scheduled digest.
  - **success:** A price drop ≥ user threshold or a "remate"/"venta urgente" keyword surfaces as an alert within one ingestion cycle; duplicate events for the same alert key collapse.

- **CAP-4 — Broker advisory brief**
  - **intent:** System accepts a broker's natural-language question and returns a structured advisory brief grounded in property aggregations, community sentiment, and active housing-program references, with every claim cited to source.
  - **success:** A broker question yields a brief with price context, DOM trend, neighborhood sentiment, and program references, each traceable to a source URL — never presented as unverified fact.

- **CAP-5 — Subscriptions & billing**
  - **intent:** System provisions Starter/Growth/Scale/Custom tiers with per-seat monthly billing, 20% annual discount, usage-based API overage, and 14-day trials, enforcing role-based access per tier.
  - **success:** A Growth-tier user is blocked from Scale-only exports and API calls; a subscription change propagates to Stripe and to access rules within one webhook cycle.

- **CAP-6 — Controlled exports**
  - **intent:** System generates CSV, Excel, PDF, GeoJSON, and PNG/SVG exports under RBAC gates, recording every export in an audit log and stamping PDF/Excel with a dynamic watermark.
  - **success:** An export records user, timestamp, filters, row count, and format in the audit log; a Starter-tier user cannot request a scheduled GeoJSON export.

- **CAP-7 — AuthN/AuthZ**
  - **intent:** System authenticates users via JWT and enforces role (admin/analyst/operator/read-only) plus tier on every read, export, and API call, with per-user saved searches and alert subscriptions.
  - **success:** A read-only operator can view the dashboard and receive alerts but cannot create exports, modify subscriptions, or access admin endpoints.

## Constraints

- **LFPDPPP:** Only ingest publicly accessible and legally permitted content; no private accounts, auth bypass, or paywall evasion; respect robots.txt/ToS/rate limits; no mass scraping without written authorization; official APIs only with credentials; data minimization; attribution and traceability preserved on every record.
- **SSRF:** Every outbound fetch must pass `require_public_host()` (DNS-resolved public IP, no private/link-local/blocklisted ranges) and use a redirect handler that raises on 3xx — no exceptions for trusted hosts.
- **Stack:** FastAPI (async, OpenAPI), SQLAlchemy + Alembic, Pydantic v2, APScheduler, Redis (rate limiting + alert dedupe), Stripe SDK, Streamlit UI, pandas/matplotlib/openpyxl/reportlab for exports (reuse `export_service.py`).
- **Data model:** Existing tables `properties`, `source_registry`, `community_content` are retained unchanged. New tables: `users`, `subscriptions`, `saved_searches`, `alerts`, `alert_deliveries`, `export_jobs`, `export_audit`, `territory_dossiers`, `analytics_materialized_views` — all new tables carry `legal_status`/source attribution.
- **Deployment:** Single Docker container with external PostgreSQL; uvicorn+gunicorn; secrets via env vars only; HTTPS behind reverse proxy; structured JSON logs; health/readiness endpoints; Prometheus metrics.
- **Performance:** Dashboard <3s; alerts delivered <5min of trigger; exports <30s for 10k rows.
- **Availability:** 99.5% SLA for Scale/Custom; 99% for Starter/Growth.

## Non-goals

- No scraping of restricted portals without written partnership or official API authorization.
- No auth bypass, paywall evasion, or private-account access.
- No transaction marketplace (no offers, escrow, or agent matching).
- No proprietary map tiles or GIS engine — use OpenStreetMap/Leaflet.
- No mobile native apps at v1.

## Success signal

A broker in Toluca submits *"¿Qué está pasando en Metepec con casas de $4M–$6M?"* and receives a cited advisory brief with price distribution, DOM trend, neighborhood sentiment, and active Infonavit/FOVISSSTE program references within 10 minutes — while every restricted portal without a partnership produces zero records and logs a compliance refusal.

## Assumptions

- Stripe supports MXN billing for Mexican merchants (verify before wiring billing).
- Reddit API and Infonavit public pages are reachable without authorization for MVP community activation.
- Exact MXN price points per tier are calibrated after 5–10 broker interviews (not decided here).

## Open Questions

- Portal partnership API terms, rate limits, and commercial terms for Inmuebles24, Lamudi, Vivanuncios, Propiedades.com, and Mercado Libre Inmuebles (direct outreach required).
- Community content signal volume from activated sources before committing to sentiment-ML investment.
- LFPDPPP legal opinion on community Q&A ingestion, sentiment analysis, and export of derived insights.