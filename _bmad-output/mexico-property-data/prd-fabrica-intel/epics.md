---
status: final
stepsCompleted: ["step-01-validate-prerequisites", "step-02-design-epics", "step-03-create-stories", "step-04-final-validation", "approved-by-user"]
inputDocuments:
  - _bmad-output/mexico-property-data/prd-fabrica-intel/prd.md
  - _bmad-output/mexico-property-data/specs/spec-fabrica-intel/SPEC.md
---

# Fábrica Intel™ - Epic Breakdown

## Overview

This document provides the complete epic and story breakdown for Fábrica Intel™, decomposing the requirements from the PRD and Technical SPEC into implementable stories for the engineering team.

## Requirements Inventory

### Functional Requirements

- **FR-1.1** Price distribution view — min/max/median price by colonia/municipality with histogram visualization
- **FR-1.2** Inventory trends — active listing count over time by property type, municipality, price band
- **FR-1.3** Days-on-market (DOM) — distribution and trends by area and property type
- **FR-1.4** Price/m² geographic heatmap — interactive map with colonia-level granularity
- **FR-1.5** Transaction volume proxy — listing velocity, new vs. resale mix, absorption indicators
- **FR-1.6** Role-based default views — broker view, developer view, investor view
- **FR-1.7** Territorial specialization — per-colonia market briefs generated on demand for any target zone
- **FR-1.8** Territory expertise profiles — persistent per-colonia intelligence dossiers updated on each ingestion cycle
- **FR-2.1** Topic modeling on community Q&A — clusters: Infonavit/financing, pricing, neighborhoods, legal, amenities
- **FR-2.2** Sentiment polarity — positive/negative/neutral by topic, municipality, time window
- **FR-2.3** Question intent classification — buy/sell/rent/finance/legal/investment
- **FR-2.4** Trend detection — topic frequency and sentiment velocity over 7/30/90 days
- **FR-2.5** Neighborhood sentiment profiles — safety, amenities, development, gentrification signals per colonia
- **FR-2.6** Pain point extraction — urgency keywords, financing barriers, legal concerns, agent complaints with frequency tracking
- **FR-2.7** Source attribution — every insight traces to source URL, author (public display name), date, platform
- **FR-2.8** Broker question intake — system returns structured advisory brief grounded in market data + community sentiment + programs
- **FR-3.1** Price reduction alerts — % drop threshold configurable per user/saved search
- **FR-3.2** Urgency keyword detection — "venta urgente", "remate", "liquidación", "reducción de precio", "urgent sale"
- **FR-3.3** Saved criteria matching — new listings matching user-defined filters
- **FR-3.4** Development/zoning signals — new development announcements, zoning changes, infrastructure projects, permit filings
- **FR-3.5** Competitive intelligence alerts — competitor listing activity, broker network moves, portfolio transactions, institutional buyer signals
- **FR-3.6** Delivery channels — in-app, email, webhook (API), scheduled digest
- **FR-4.1** Tier: Starter (individual broker) — dashboard + basic alerts + 5 exports/mo
- **FR-4.2** Tier: Growth (small agency, 2-5 seats) — + sentiment intelligence + 50 exports/mo + API access (1k calls/mo)
- **FR-4.3** Tier: Scale (developer/fund, 5-20 seats) — + competitive alerts + 500 exports/mo + API (50k calls/mo) + webhooks
- **FR-4.4** Tier: Custom (enterprise, 20+ seats) — white-label, dedicated support, custom integrations, SLA, unlimited exports/API
- **FR-4.5** Billing — per-seat monthly, 20% annual discount, usage-based API overage, Stripe integration
- **FR-4.6** Role-based access — admin, analyst, operator, read-only per tier
- **FR-4.7** Trial — 14-day free trial for Starter/Growth, demo for Scale/Custom
- **FR-5.1** Formats — CSV, Excel, PDF reports, GeoJSON (GIS), PNG/SVG charts
- **FR-5.2** Role-based export gates — Starter: manual CSV/Excel/PDF only; Growth+: all formats + scheduled + API
- **FR-5.3** Audit log — every export records user, timestamp, filters, row count, format
- **FR-5.4** Watermarking — dynamic watermark with user ID, timestamp, tier on PDF/Excel exports
- **FR-5.5** Scheduled exports — recurring daily/weekly/monthly with email delivery
- **FR-5.6** Data minimization — exports respect LFPDPPP: no unnecessary PII, public display names only, attribution preserved

### NonFunctional Requirements

- **NFR-1** Compliance — LFPDPPP full compliance; no mass scraping; official APIs only with credentials; robots.txt/ToS respected; data minimization; attribution/traceability preserved
- **NFR-2** Security — SSRF mitigation (host validation, redirect blocking), HTTPS only, secrets in env vars, no PII in logs
- **NFR-3** Performance — Dashboard loads <3s; alerts delivered <5min of trigger; exports <30s for 10k rows
- **NFR-4** Availability — 99.5% uptime SLA for Scale/Custom tiers; 99% for Starter/Growth
- **NFR-5** Scalability — PostgreSQL handles 1M+ properties, 10M+ community content items; horizontal read replicas for analytics
- **NFR-6** Observability — Structured logging, metrics (latency, error rate, alert delivery), health endpoints

### Additional Requirements

- **ARCH-1** Stack: FastAPI (async, OpenAPI), SQLAlchemy + Alembic ORM, Pydantic v2 schemas, APScheduler, Redis, Stripe Python SDK, Streamlit UI, ReportLab/OpenPyXL/Matplotlib.
- **ARCH-2** Data model: Existing tables (`properties`, `source_registry`, `community_content`) retained. New tables: `users`, `subscriptions`, `saved_searches`, `alerts`, `alert_deliveries`, `export_jobs`, `export_audit`, `territory_dossiers`, `analytics_materialized_views`.
- **ARCH-3** Security: Outbound fetches use `require_public_host()` + custom no-redirect handler.

### UX Design Requirements

- None specified (pure B2B SaaS dashboard and API platform).

### FR Coverage Map

| FR | Requirement | Epic | Story | Status |
| --- | --- | --- | --- | --- |
| FR-1.1 | Price distribution view | Epic 3 | Story 3.2 | Covered |
| FR-1.2 | Inventory trends | Epic 3 | Story 3.3 | Covered |
| FR-1.3 | Days-on-market | Epic 3 | Story 3.4 | Covered |
| FR-1.4 | Price/m² heatmap | Epic 3 | Story 3.5 | Covered |
| FR-1.5 | Transaction volume proxy | Epic 3 | Story 3.8 | Covered |
| FR-1.6 | Role-based default views | Epic 3 | Story 3.1 | Covered |
| FR-1.7 | Territorial specialization | Epic 3 | Story 3.6 | Covered |
| FR-1.8 | Territory expertise profiles | Epic 3 | Story 3.6 | Covered |
| FR-2.1 | Topic modeling | Epic 4 | Story 4.1 | Covered |
| FR-2.2 | Sentiment polarity | Epic 4 | Story 4.2 | Covered |
| FR-2.3 | Question intent classification | Epic 4 | Story 4.3 | Covered |
| FR-2.4 | Trend detection | Epic 4 | Story 4.2 | Covered |
| FR-2.5 | Neighborhood sentiment profiles | Epic 4 | Story 4.4 | Covered |
| FR-2.6 | Pain point extraction | Epic 4 | Story 4.5 | Covered |
| FR-2.7 | Source attribution | Epic 4 | Story 4.6 | Covered |
| FR-2.8 | Broker question intake | Epic 4 | Story 4.7 | Covered |
| FR-3.1 | Price reduction alerts | Epic 5 | Story 5.2 | Covered |
| FR-3.2 | Urgency keyword detection | Epic 5 | Story 5.3 | Covered |
| FR-3.3 | Saved criteria matching | Epic 5 | Story 5.4 | Covered |
| FR-3.4 | Development/zoning signals | Epic 5 | Story 5.5 | Covered |
| FR-3.5 | Competitive intelligence alerts | Epic 5 | Story 5.8 | Covered |
| FR-3.6 | Delivery channels | Epic 5 | Story 5.6 | Covered |
| FR-4.1 | Starter tier | Epic 6 | Story 6.1 | Covered |
| FR-4.2 | Growth tier | Epic 6 | Story 6.1 | Covered |
| FR-4.3 | Scale tier | Epic 6 | Story 6.1 | Covered |
| FR-4.4 | Custom tier | Epic 6 | Story 6.8 | Covered |
| FR-4.5 | Billing | Epic 6 | Story 6.2 | Covered |
| FR-4.6 | Role-based access | Epic 1 | Story 1.3 | Covered |
| FR-4.7 | Trial | Epic 6 | Story 6.2 | Covered |
| FR-5.1 | Export formats | Epic 6 | Story 6.4 | Covered |
| FR-5.2 | Role-based export gates | Epic 6 | Story 6.4 | Covered |
| FR-5.3 | Audit log | Epic 6 | Story 6.5 | Covered |
| FR-5.4 | Watermarking | Epic 6 | Story 6.5 | Covered |
| FR-5.5 | Scheduled exports | Epic 6 | Story 6.6 | Covered |
| FR-5.6 | Data minimization | Epic 6 | Story 6.7 | Covered |

### NFR Coverage Map

| NFR | Requirement | Epic(s) | Stories |
| --- | --- | --- | --- |
| NFR-1 | Compliance (LFPDPPP) | Epic 2, Epic 4, Epic 6 | 2.1, 2.2, 2.3, 4.6, 6.7 |
| NFR-2 | Security (SSRF) | Epic 1 | 1.4 |
| NFR-3 | Performance | Epic 3, Epic 5 | 3.7, 5.6 |
| NFR-4 | Availability SLA | Epic 2, Epic 5, Epic 6 | 2.4, 6.2, 6.6 |
| NFR-5 | Scalability | Epic 2, Epic 3 | 2.2, 3.7 |
| NFR-6 | Observability | Epic 2, Epic 3, Epic 5 | 2.4, 3.7, 5.6 |

## Epic List

### Epic 1: Secure Foundation + Authentication
Secure infrastructure and access control. Users can be provisioned with JWT auth + role-based access; the system enforces SSRF mitigation on all outbound fetches and rate-limits API calls.

**User outcome:** An admin can provision a Growth-tier agency user; that user authenticates via JWT, accesses the dashboard, and cannot reach Scale-only features.

**FRs covered:** FR-4.6, FR-4.7, NFR-1, NFR-2, ARCH-1, ARCH-2 (users, subscriptions tables, roles, JWT, SSRF guard)

### Story 1.1: User Registration and Profile Creation
As a first-time broker,
I want to register with email + password and set up my profile (name, brokerage, territory colonias),
So that my dashboard and alerts are scoped to my target market.

**Acceptance Criteria:**

**Given** no account exists, **When** I submit email + password, **Then** a `users` record is created with role=`read-only` (default tier=Starter)
**And** the user ID is returned in the response
**Given** registration complete, **When** I provide name + brokerage + colonias, **Then** profile is saved and persists in `users` table
**Given** I enter an existing email, **Then** I see "email in use" error

### Story 1.2: JWT-Based Authentication
As an authenticated user,
I want to receive a JWT on login,
So that every subsequent request is authorized by role/tier.

**Acceptance Criteria:**

**Given** my email + password are valid, **When** I POST `/api/v1/auth/login`, **Then** a signed JWT is returned with `role`, `tier`, `user_id` claims
**Given** JWT is expired, **When** I access any endpoint, **Then** I receive 401
**Given** JWT has role=read_only, **When** I try `/api/v1/admin/users`, **Then** I receive 403

### Story 1.3: Role-Based Access Control
As a system admin,
I want to assign roles (admin/analyst/operator/read-only) per seat,
So that access to features is enforced by role, not trust.

**Acceptance Criteria:**

**Given** user has role=admin, **When** admin endpoint is accessed, **Then** 200
**Given** user has role=operator, **When** operator attempts export creation, **Then** 403 (only analyst+ can export)
**Given** role changes, **Then** next request reflects new permission without re-auth

### Story 1.4: SSRF Protection for Outbound Fetches
As the ingestion system,
I want every outbound fetch validated against `require_public_host()`,
So that SSRF attacks through source URLs are blocked.

**Acceptance Criteria:**

**Given** a source URL resolves to `192.168.1.1`, **When** fetch is attempted, **Then** it is blocked and logged with reason "private IP range"
**Given** a source URL returns 301 to `localhost`, **When** redirect handler activates, **Then** it raises and blocks with reason "redirect to private host"
**Given** a source URL resolves to `187.190.x.x` (public MX), **When** fetched, **Then** fetch proceeds and content is stored in `data/raw/`

### Epic 2: Data Ingestion & Compliance Layer
Authorized source ingestion with full LFPDPPP compliance tracing — source registry, normalization, attribution, and compliance refusal logging.

**User outcome:** An operator activates 10 community sources and 1 portal API; every ingested record carries source URL, platform, date, and legal_status; a restricted portal without partnership produces zero records and logs a compliance refusal.

**FRs covered:** FR-1.1–1.8 (data model support), CAP-1, all of NFR-1, ARCH-3 (SSRF mitigation)

### Epic 3: Market Intelligence Dashboard
Property analytics dashboard with colonia-level price distribution, inventory, DOM, heatmap, and territory dossiers — rendered from materialized views for sub-3s load.

**User outcome:** A broker in Toluca opens the dashboard and sees the price distribution, inventory trend, and DOM heatmap for Metepec filtered to $4M–$6M casas, loading in under 3 seconds.

**FRs covered:** FR-1.1–1.6, NFR-3 (dashboard <3s), NFR-5 (scalability), NFR-6 (dashboard metrics)

### Epic 4: Community Intelligence & Sentiment Analysis
Community Q&A ingestion, topic modeling, sentiment polarity, intent classification, neighborhood profiles, pain-point extraction, and broker question intake (advisory briefs).

**User outcome:** A broker submits "¿Qué está pasando en Metepec con casas $4-6M?" and receives a cited advisory brief with price context, DOM trend, neighborhood sentiment, pain points (e.g., financing barriers), and active Infonavit/FOVISSSTE program references — each traceable to a source URL.

**FRs covered:** FR-2.1–2.8, NFR-1 (community attribution), NFR-3 (brief generation <10min)

### Epic 5: Market Alert Engine
Configurable alert rules (price drops, urgency keywords, saved criteria, dev/zoning signals, competitive intelligence) with multi-channel delivery and deduplication.

**User outcome:** A broker saves a search for "$4M–$6M casas in Metepec" and receives an in-app + email alert when a price drops 10% or a listing contains "venta urgente" — never the same listing twice.

**FRs covered:** FR-3.1–3.6, NFR-3 (alert delivery <5min), NFR-6 (alert delivery metrics)

### Epic 6: Subscriptions, Exports & Billing
Tiered subscriptions (Starter/Growth/Scale/Custom), Stripe billing with trials and overages, and controlled exports with RBAC gates, audit logging, watermarking, and scheduled delivery.

**User outcome:** A Growth-tier analyst exports a weekly Excel report of Metepec listings — the export is logged to the audit trail, stamped with their user ID + timestamp + tier watermark, and counts against their tier's 50/month quota.

**FRs covered:** FR-4.1–4.5, FR-5.1–5.6

### Story 2.1: Source Registry with Compliance Status
As an operator,
I want to import and view source configurations in `source_registry` with legal_basis/status/access_method,
So that the system knows which sources are authorized for ingestion.

**Acceptance Criteria:**

**Given** `source_configs.csv` exists, **When** `import_to_postgres.py` runs, **Then** all rows land in `source_registry` with `enabled`, `status`, `legal_basis` columns populated
**Given** a source has `status=restricted` and `access_method=partner_required`, **When** ingestion cycle starts, **Then** it is skipped with compliance log entry "restricted source skipped"
**Given** I query `/api/v1/sources`, **Then** I see enabled sources marked green, restricted marked red

### Story 2.2: Normalized Property Ingestion
As the ingestion system,
I want to normalize raw property JSON into records with full attribution (source_url, broker_name, legal_status),
So that every property is traceable to its origin.

**Acceptance Criteria:**

**Given** raw JSON exists at `data/raw/inmuebles24.json`, **When** `ingest_sources.py` runs, **Then** normalized records appear in `data/export/properties.csv` with `legal_status=approved_public_record` or `manual_review`
**Given** a listing lacks `latitude/longitude`, **Then** it is stored with NULL, not fabricated coordinates
**Given** duplicate listings are detected (same source_url), **Then** only the first record is kept after dedup

### Story 2.3: Community Content Ingestion with Attribution
As the ingestion system,
I want to normalize community Q&A with author_display_name (public), source_url, platform, and legal_status,
So that sentiment analysis respects LFPDPPP data minimization.

**Acceptance Criteria:**

**Given** raw Reddit JSON exists at `data/raw/reddit_mexico_network.json`, **When** ingestion runs, **Then** records land in `community_content.csv` with `legal_status=manual_review` (default for non-official sources)
**Given** a post has `author_display_name=juan_87`, **Then** only that display name is stored (no email or user_id)
**Given** a Facebook post has no Graph API authorization, **Then** ingestion is blocked with compliance log entry

### Story 2.4: Ingestion Cycle Scheduler
As the system,
I want to run ingestion cycles every X hours per source's crawl_frequency,
So that data freshness stays within SLAs.

**Acceptance Criteria:**

**Given** a source has `crawl_frequency=daily`, **When** APScheduler fires, **Then** that source's adapter runs and logs completion
**Given** a source has `crawl_frequency=manual`, **Then** it only ingests when manually triggered via `POST /api/v1/ingest/{source_key}`
**Given** ingestion fails, **Then** the `last_error` field in `source_registry` is updated with the error message
### Story 3.1: Dashboard Layout with Role-Based Views
As a broker,
I want the dashboard to open on my default view (broker mode: price distribution + recent sentiment),
So that my first glance gives me what I need to advise today.

**Acceptance Criteria:**

**Given** I log in as a broker with role=analyst, **When** I open `/dashboard`, **Then** I see two columns: left — price distribution histogram for my default territory; right — recent neighborhood sentiment
**Given** I switch role to developer via `/settings`, **Then** the dashboard re-renders with dev view: absorption rate + zoning signals panel
**Given** I have no saved colonias, **Then** dashboard defaults to Toluca metropolitan area

### Story 3.2: Price Distribution by Colonia
As a broker,
I want to see min/max/median price and histogram for any colonia filtered by property type and price band,
So that I can set realistic expectations without spreadsheet gymnastics.

**Acceptance Criteria:**

**Given** I select colonia="San Antonio", municipality="Toluca", property_type="house", price_band="$3M-$6M", **When** I click Apply, **Then** the histogram shows 10 bins with min/max/median annotations
**Given** there are fewer than 5 listings in my filter, **Then** a warning "Low sample size" appears
**Given** I export the histogram, **Then** the downloaded PNG includes the same filters as title text

### Story 3.3: Inventory Trends Over Time
As a broker,
I want to see active listing count trends by property type and price band,
So that I can identify whether the market is heating up or cooling down.

**Acceptance Criteria:**

**Given** I view the inventory trend chart for Toluca last 90 days, **When** the data loads, **Then** I see a line chart with 7-day buckets, colored by property type
**Given** I switch to 30-day view, **Then** the chart re-renders with daily buckets
**Given** inventory dropped 15% week-over-week, **Then** a subtle annotation "−15% YoY" appears on the trend line

### Story 3.4: Days-on-Market Distribution
As a broker,
I want to see DOM distribution and trends by area and property type,
So that I can price competitively and advise sellers.

**Acceptance Criteria:**

**Given** I view DOM for Metepec houses $4M-$6M, **When** the chart loads, **Then** I see a box plot (Q1, median, Q3, whiskers) with average DOM overlaid
**Given** I drill into a specific listing, **Then** I see its individual DOM vs. the colonia median
**Given** DOM exceeds the colonia median by 2 standard deviations, **Then** the listing is flagged with "stale" badge

### Story 3.5: Price/m² Geographic Heatmap
As a broker,
I want an interactive heatmap showing price/m² by colonia,
So that I can spot overvalued/undervalued zones at a glance.

**Acceptance Criteria:**

**Given** I open the heatmap tab, **When** the map renders, **Then** colonias are color-coded green (low) → red (high) by price/m²
**Given** I click a colonia, **Then** a tooltip shows median price/m², inventory count, and 7-day trend
**Given** I change filter to apartments, **Then** the heatmap recalculates and re-colors in under 2 seconds

### Story 3.6: Territory Dossier Generation
As a broker,
I want to generate a one-click per-colonia market brief (price bands, DOM, sentiment, active programs),
So that I can prep for client conversations quickly.

**Acceptance Criteria:**

**Given** I am on any dashboard view, **When** I click "Generate Brief" for colonia X, **Then** a PDF opens with: price band mix table, DOM box plot, sentiment trend, and active Infonavit/FOVISSSTE programs
**Given** no sentiment data exists for that colonia, **Then** the brief states "No community activity in past 14 days"
**Given** I save a dossier, **Then** it persists in the `territory_dossiers` table with `updated_at = now()`

### Story 3.7: Dashboard Performance (Sub-3s)
As a dashboard user,
I want every view to load from materialized views in under 3 seconds,
So that the tool stays responsive under load.

**Acceptance Criteria:**

**Given** 10 concurrent users load the dashboard simultaneously, **When** timing includes DB query + render, **Then** 95th percentile < 3 seconds
**Given** a materialized view is stale (>1 hour since refresh), **Then** the dashboard shows a subtle "data refreshed HH:MM" indicator
**Given** a query takes >3s, **Then** the observability layer logs a slow-query event with the dashboard view name

### Story 3.8: Transaction Volume & Absorption Metrics
As a broker,
I want to see listing velocity, new vs. resale mix, and absorption rate by colonia and price band,
So that I can gauge market liquidity and advise on pricing strategy.

**Acceptance Criteria:**

**Given** I view the Transaction Volume panel for Toluca last 90 days, **When** the data loads, **Then** I see: (a) weekly new listings count, (b) new vs. resale ratio stacked bar, (c) absorption rate (listings sold / new listings) per week
**Given** I filter to Metepec houses $4M-$6M, **Then** the metrics recalculate for that specific segment
**Given** absorption rate drops below 0.3 for two consecutive weeks, **Then** a "market cooling" indicator appears on the panel
**Given** I export this view, **Then** the CSV includes week, new_listings, resale_listings, absorption_rate columns

### Story 4.1: Topic Modeling on Community Q&A
As an analyst,
I want to see topic clusters from community discussions (Infonavit, pricing, neighborhoods, legal, amenities),
So that I understand what buyers/sellers are actually concerned about.

**Acceptance Criteria:**

**Given** community content has ingested for Toluca/Metepec in the last 30 days, **When** I open the Topics view, **Then** I see 5–7 clusters with top 5 keywords each and mention counts
**Given** I click "Infonavit" cluster, **Then** I see a timeline of mentions and sample posts (truncated, with source links)
**Given** content has `legal_status=manual_review`, **Then** it is excluded from topic modeling and logged as "skipped: unverified"

### Story 4.2: Sentiment Polarity Dashboard
As an analyst,
I want sentiment polarity (positive/negative/neutral) by topic and municipality over time with trend detection at 7/30/90 day windows,
So that I can gauge neighborhood mood and spot sentiment shifts.

**Acceptance Criteria:**

**Given** I select municipality=Toluca and topic=Pricing, **When** the chart loads, **Then** I see stacked bars (positive/neutral/negative) by week with a 7-day trend line
**Given** I switch to 30-day view, **Then** the chart shows daily buckets with 30-day sentiment velocity (delta %/week)
**Given** I switch to 90-day view, **Then** the chart shows weekly buckets with 90-day trend and topic frequency velocity
**Given** negative sentiment spikes 40% over 7 days, **Then** the bar is color-coded amber and a "sentiment alert" icon appears
**Given** I export the chart, **Then** the PNG includes the sentiment breakdown legend and the selected time window

### Story 4.3: Question Intent Classification
As an analyst,
I want to classify questions into buy/sell/rent/finance/legal/intent,
So that I can route and prioritize attention.

**Acceptance Criteria:**

**Given** a community post says "¿Alguien sabe cuándo subvenciona Infonavit?", **When** intent classification runs, **Then** it is tagged `intent=finance` with confidence >0.8
**Given** a post says "Vendo departamento en Metepec urgente", **Then** it is tagged `intent=sell` + `urgency=high`
**Given** confidence is below 0.6, **Then** the item is flagged "needs review" and excluded from dashboards

### Story 4.4: Neighborhood Sentiment Profiles
As a broker,
I want neighborhood-level sentiment profiles (safety, amenities, development, gentrification) per colonia,
So that I can advise clients on lifestyle fit.

**Acceptance Criteria:**

**Given** I open the colonia profile for "Lomas de la Selva", **When** the profile loads, **Then** I see 4 sentiment gauges: safety, amenities, development, gentrification
**Given** no comments mention safety in the last 30 days, **Then** the safety gauge shows "insufficient data"
**Given** I compare two colonias side-by-side, **Then** the profiles stack horizontally for visual comparison

### Story 4.5: Pain Point Extraction
As an analyst,
I want to extract and track pain points (urgency keywords, financing barriers, legal concerns, agent complaints) with frequency.
So that I can identify market friction points.

**Acceptance Criteria:**

**Given** community content contains "no tengo crédito", "demora en escrituración", "interés 15%", **When** pain extraction runs, **Then** these are tagged as `barriers=financing`, `barriers=legal`, `barrier=interest_rate` respectively
**Given** urgency keywords ("urgente", "remate", "liquidación") appear 25 times this week, **Then** they surface in the Pain Points table with trend indicator "↑ 15% from last week"
**Given** a pain point cluster has fewer than 3 mentions, **Then** it is collapsed into "other"

### Story 4.6: Source Attribution on All Insights
As a compliance reviewer,
I want every insight traceable to source URL, author_display_name, date, and platform.
So that LFPDPPP attribution is preserved.

**Acceptance Criteria:**

**Given** a sentiment score is computed from 50 posts, **When** I hover the insight, **Then** I see a popover: "Sources: Reddit (25), Facebook (12), Vivanuncios (8), Infonavit (5) — last updated 2026-10-25"
**Given** I click a source name, **Then** I'm linked to the original post URL (for public content only)
**Given** attribution is missing for a record, **Then** it is excluded from the analysis and logged

### Story 4.7: Broker Question Intake — Advisory Brief
As a broker,
I want to submit a natural-language question and receive a structured advisory brief (price context, DOM, sentiment, programs) with cited sources.
So that I can answer client questions fast with data.

**Acceptance Criteria:**

**Given** I type "¿Qué está pasando en Metepec con casas de $4M-$6M?" and click Submit, **When** the brief generates (within 10 minutes), **Then** it contains: price distribution (min/max/median), DOM box plot, neighborhood sentiment polarity, and active Infonavit/FOVISSSTE programs
**Given** no community content exists for Metepec, **Then** the brief states "No sentiment data for this zone in past 30 days"
**Given** the brief is generated, **Then** it is logged in `advisory_briefs` with question, filters, timestamp, and a unique shareable link

### Story 5.1: Saved Search Criteria
As a broker,
I want to save a search (location, price band, property type, keywords) and name it,
So that the alert engine evaluates the right conditions for me.

**Acceptance Criteria:**

**Given** I am on the search page, **When** I set municipality="Toluca", price_band="$4M-$6M", property_type="house", and click "Save Search", **Then** a `saved_searches` record is created with my user_id, filters, and name "Toluca casas $4-6M"
**Given** I save a second search with the same name, **Then** I'm prompted to rename or overwrite
**Given** I delete a saved search, **Then** it is removed from `saved_searches` and no new alerts fire for that criteria

### Story 5.2: Price Drop Alert
As a broker,
I want to receive an alert when a saved search match drops in price by a configurable %,
So that I can move fast on opportunities.

**Acceptance Criteria:**

**Given** I have a saved search with price_drop_threshold=10%, **When** a matching listing's price drops from $5.5M to $4.9M, **Then** an alert is created in `alerts` table with `rule_type=PRICE_DROP`, `severity=MEDIUM`
**Given** the price drop is < my threshold, **Then** no alert fires
**Given** the alert fires, **Then** I receive it via my configured channel within 5 minutes of the `import_to_postgres` cycle

### Story 5.3: Urgency Keyword Detection
As a broker,
I want alerts when listings contain urgency keywords ("venta urgente", "remate", "liquidación"),
So that I catch distressed inventory first.

**Acceptance Criteria:**

**Given** a new listing description contains "remate por liquidación urgente", **When** ingestion completes, **Then** an alert is created with `rule_type=URGENCY_KEYWORD`, `severity=HIGH`, and the matched keywords stored in `keywords_matched`
**Given** the same listing already triggered an alert in the last 24 hours, **Then** no duplicate alert fires
**Given** I have urgency alerts disabled in my notification settings, **Then** the alert is suppressed

### Story 5.4: New Listing Criteria Match
As a broker,
I want alerts when new listings match my saved criteria,
So that I'm the first to know about fresh inventory.

**Acceptance Criteria:**

**Given** I have a saved search for Metepec houses $4M-$6M, **When** a new listing matching all criteria is ingested, **Then** an alert is created with `rule_type=NEW_LISTING`, `severity=LOW`
**Given** a listing matches 8 of 9 criteria (missing only keywords), **Then** no alert fires (strict match)
**Given** an alert fires, **Then** it includes the listing's price, square_meters, and a direct link to view on dashboard

### Story 5.5: Development/Zoning Signal Alerts
As a developer,
I want alerts for new development announcements, zoning changes, infrastructure projects, and permit filings in my target zone,
So that I can get ahead of market shifts.

**Acceptance Criteria:**

**Given** I have an alert subscription for municipality="Toluca" and topic="infrastructure", **When** a local news article mentions "nueva autopista Toluca-Naucalpan", **Then** an alert is created with `rule_type=DEV_ZONING_SIGNAL`, `severity=MEDIUM`
**Given** the signal comes from a source with `legal_status=manual_review`, **Then** the alert is tagged `confidence=low` and requires manual review before delivery
**Given** I have 3 infrastructure alerts in 7 days, **Then** they are bundled into a weekly digest

### Story 5.6: Multi-Channel Alert Delivery
As a user,
I want alerts delivered via in-app, email, webhook, or scheduled digest,
So that I consume alerts in my preferred workflow.

**Acceptance Criteria:**

**Given** I set my delivery preference to email+digest, **When** alerts fire between 8PM–8AM, **Then** they are queued for the 8AM digest instead of immediate email
**Given** I provide a webhook URL, **When** a HIGH-severity alert fires, **Then** a POST is sent with the alert payload to my webhook
**Given** delivery fails (bounce, webhook timeout), **Then** the alert falls back to in-app and I see a "delivery failed" banner

### Story 5.7: Alert Deduplication
As a system,
I want to deduplicate alerts by alert key (source_listing + rule_type + user),
So that users don't get spammed.

**Acceptance Criteria:**

**Given** the same trigger condition fires twice in the same ingestion cycle, **When** deduplication runs, **Then** only one alert is created per (source_listing_id, rule_type, user_id, 24h window)
**Given** a new ingestion cycle runs, **Then** alerts from the prior cycle are eligible again
**Given** an alert is deduplicated, **Then** a log entry records "deduplicated: key=PRICE_DROP:listing_001:user_42"

### Story 5.8: Competitive Intelligence Alerts
As a developer,
I want alerts for competitor listing activity, broker network moves, portfolio transactions, and institutional buyer signals in my target zone,
So that I can track competitive dynamics and market positioning.

**Acceptance Criteria:**

**Given** I have a competitive alert subscription for municipality="Toluca", **When** a new listing from a known competitor brokerage is ingested, **Then** an alert is created with `rule_type=COMPETITIVE_LISTING`, `severity=LOW`
**Given** a portfolio transaction (multiple properties from same seller in 30 days) is detected, **Then** an alert is created with `rule_type=PORTFOLIO_TRANSACTION`, `severity=MEDIUM`
**Given** an institutional buyer signal (large fund purchase pattern) is detected, **Then** an alert is created with `rule_type=INSTITUTIONAL_BUYER`, `severity=HIGH`
**Given** the signal comes from a source with `legal_status=manual_review`, **Then** the alert is tagged `confidence=low` and requires manual review before delivery

### Story 6.1: Tier Definition and Feature Gates
As a system,
I want tiers (Starter/Growth/Scale/Custom) with per-tier feature gates (exports, API calls, formats),
So that users only access what their subscription allows.

**Acceptance Criteria:**

**Given** a user has tier=Starter, **When** they attempt to export GeoJSON, **Then** the export button is disabled with "Upgrade to Growth for GeoJSON"
**Given** a Growth-tier user has consumed 50 exports this month, **When** they attempt export #51, **Then** they receive "quota exceeded, upgrade to Scale"
**Given** a Scale-tier user, **Then** all formats (CSV, Excel, PDF, GeoJSON, PNG/SVG) are available with 500 exports/mo limit

### Story 6.2: Stripe Subscription Checkout and Trial
As a user,
I want to sign up for a 14-day free trial and then pay per-seat monthly via Stripe,
So that I can try before I buy and pay predictably.

**Acceptance Criteria:**

**Given** I select "Growth: $1,200 MXN/seat/month" and 3 seats, **When** I click "Start Trial", **Then** I am redirected to Stripe Checkout with trial=14 days, then redirected back with a `subscriptions` record created (status=trialing)
**Given** my trial expires, **When** I do nothing, **Then** I can still log in but dashboard shows "subscription expired, renew to continue"
**Given** I cancel during trial, **Then** the `subscriptions` record is marked status=canceled and no charge is made

### Story 6.3: Usage-Based Overage Tracking
As a Growth-tier user,
I want to see my API call quota (1,000/mo) and be alerted at 80% usage,
So that I can upgrade before hitting limits.

**Acceptance Criteria:**

**Given** I have used 800 of 1,000 API calls this month, **When** I make call #801, **Then** my dashboard shows "80% of API quota used"
**Given** I exceed 1,000 calls, **When** my next invoice is generated, **Then** I am charged $0.10/call overage
**Given** I upgrade from Growth to Scale mid-cycle, **Then** my API quota resets immediately to 50,000

### Story 6.4: Export Format Selection with RBAC Gates
As a broker,
I want to export CSV/Excel/PDF and (if Growth+) GeoJSON/PNG/SVG,
So that I can share insights in the format my client needs.

**Acceptance Criteria:**

**Given** I am Starter-tier, **When** I click Export, **Then** I only see CSV, Excel, PDF options
**Given** I am Growth-tier, **Then** GeoJSON and PNG/SVG are available as export formats
**Given** I select PNG, **Then** the exported image matches the dashboard view exactly (filters, zoom level, date range)

### Story 6.5: Export Audit Log and Watermarking
As a compliance reviewer,
I want every export logged with user+timestamp+filters+row_count+format, and PDF/Excel stamped with a dynamic watermark,
So that data usage is auditable and traceable.

**Acceptance Criteria:**

**Given** I export a PDF with filter "Metepec houses $4M-$6M", **When** the PDF is downloaded, **Then** every page has a footer: "Exported by {name} | {timestamp} | Fábrica Intel {tier} | Metepec / houses / $4-6M"
**Given** the export generates 847 rows, **Then** `export_audit` table records user_id, format=pdf, filters, row_count=847, timestamp
**Given** I am a compliance reviewer, **Then** I can query `export_audit` by user_id, date range, and format

### Story 6.6: Scheduled Exports
As an analyst,
I want to schedule recurring exports (daily/weekly/monthly) with email delivery,
So that my team gets regular reports without manual effort.

**Acceptance Criteria:**

**Given** I configure a weekly Excel export of "Metepec inventory" every Monday at 8AM, **When** the scheduler fires, **Then** an `export_jobs` record is created and an email is sent to my subscribers list
**Given** a scheduled export fails (DB timeout), **Then** a retry with exponential backoff runs up to 3 times, and on failure I receive an error email
**Given** I cancel a scheduled export, **Then** no future `export_jobs` are queued and the schedule is removed from `export_jobs`

### Story 6.7: Data Minimization on Exports
As an exporter,
I want exports to strip PII beyond public display names and preserve attribution,
So that LFPDPPP compliance is enforced at the data boundary.

**Acceptance Criteria:**

**Given** I export a property CSV, **When** the export is generated, **Then** no `broker_phone` is included — only `broker_name` and `source_url`
**Given** I export a community content CSV, **Then** only `author_display_name` is included (never email, user_id, or IP)
**Given** a source has `legal_status=manual_review`, **Then** it is flagged with a "review status" column so downstream users know to verify

### Story 6.8: Custom Tier Enterprise Configuration
As an enterprise admin,
I want to configure Custom tier with white-label branding, dedicated support channels, custom integrations, SLA guarantees, and unlimited exports/API access,
So that large organizations (20+ seats) get a tailored deployment.

**Acceptance Criteria:**

**Given** I am an admin for a Custom tier account, **When** I access `/api/v1/admin/custom-tier`, **Then** I can configure: white-label domain/logo, SLA tier (99.5% uptime), dedicated support email/Slack, custom webhook endpoints
**Given** a Custom tier user attempts an export, **Then** no quota limit applies and all formats (CSV, Excel, PDF, GeoJSON, PNG/SVG) are available
**Given** a Custom tier user makes API calls, **Then** no rate limit applies (unlimited) and usage is logged but not billed as overage
**Given** the Custom tier subscription is created, **Then** a `subscriptions` record is created with `tier=custom`, `seats>=20`, and `custom_config` JSON with branding/SLA/integrations
