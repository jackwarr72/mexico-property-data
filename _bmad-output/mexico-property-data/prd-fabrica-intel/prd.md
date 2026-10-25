---
title: "Fábrica Intel™ — Real Estate Intelligence SaaS PRD"
status: draft
created: "2026-10-24"
updated: "2026-10-24"
---

# Fábrica Intel™ — Real Estate Intelligence SaaS PRD

## 1. Vision

**Fábrica Inmobiliaria** builds an industrialized, standardized system — like a factory — that produces successful, repeatable real estate transactions using **properties, data, and questions** as raw material. It solves the problem of isolated, disconnected daily processes by transforming operational dispersion into an enterprise architecture with clear routines, territorial and commercial specialization, and the capacity to convert complex data into high-value advisory that closes deals.

The system is a **broker operating system**: daily/weekly/monthly routines (market scan → alert triage → advisory prep → deal close) that turn the dispersion of day-to-day work into repeatable, measurable deal-closing workflows.

## 2. Problem & Opportunity

### 2.1 Problem
- **No dedicated Real Estate Intelligence SaaS exists** for Toluca-Metepec (primary) or 6 CDMX delegations (secondary: Benito Juárez, Cuauhtémoc, Venustiano Carranza, Álvaro Obregón, Santa Fe, Cuajimalpa)
- All named proptechs (Flat.mx, Yave, LaHaus, Homie) are **finance-first** (mortgage/rental), not data products
- Portal layer (Inmuebles24, Lamudi, Vivanuncios, Propiedades.com, Mercado Libre Inmuebles) is the **supply layer** — all restricted, partner-required, explicitly not scraped
- Brokers operate on spreadsheets with no price distribution (min/max/median), no days-on-market, no neighborhood sentiment, no automated alerts
- Community Q&A layer (Reddit, Facebook, forums, Infonavit) is completely unmined — zero automated sentiment, topic modeling, or pain-point extraction

### 2.2 Opportunity
- **Data-as-a-service niche is unoccupied** in target geographies
- Competitive advantage = **hyperlocal intelligence + community sentiment**, NOT listing aggregation
- 20 community sources registered (Reddit, Facebook groups, Quora, forums, Infonavit Q&A, local news) ready to activate
- Government open data (Public Registry) available as licensed public dataset
- Clear compliance framework already encoded (LFPDPPP, no prohibited scraping, attribution/traceability)

## 3. Users & Personas

### 3.1 Primary: Independent Brokers & Agencies
- **Context**: Operate in Toluca-Metepec + 6 CDMX delegations
- **Current workflow**: Spreadsheets, manual Google `site:`/`intitle:` searches for "venta urgente"/"reducción de precio", WhatsApp groups
- **Pain**: No price distribution (min/max/median by colonia), no DOM, no neighborhood sentiment, no automated alerts
- **Value**: Dashboard with price trends, inventory, DOM, heatmaps; alerts for price drops/urgency; sentiment to advise clients

### 3.2 Secondary: Developers, Investors, Land Acquisition Teams, RE Funds
- **Context**: Need market intelligence for acquisition decisions, portfolio monitoring
- **Pain**: No transaction volume data, no absorption rates, no development/zoning signals, no competitive intelligence
- **Value**: Market alerts for new developments/zoning/permits; competitive intelligence; controlled exports for IC memos

## 4. Value Proposition

| Segment | Core Value | Differentiator |
| --- | --- | --- |
| Brokers | Close deals faster with data-backed advisory | Hyperlocal price distribution + neighborhood sentiment from community Q&A |
| Developers | De-risk acquisitions with market intelligence | Development/zoning alerts + competitive signals + absorption trends |
| Investors/Funds | Portfolio monitoring + opportunity detection | Controlled exports + audit trail + API access + sentiment leading indicators |

## 5. Features & Functional Requirements

### Module 1: Real Estate Dashboard
**FR-1.1** Price distribution view — min/max/median price by colonia/municipality with histogram visualization  
**FR-1.2** Inventory trends — active listing count over time by property type, municipality, price band  
**FR-1.3** Days-on-market (DOM) — distribution and trends by area and property type  
**FR-1.4** Price/m² geographic heatmap — interactive map with colonia-level granularity  
**FR-1.5** Transaction volume proxy — listing velocity, new vs. resale mix, absorption indicators  
**FR-1.6** Role-based default views — broker view, developer view, investor view  
**FR-1.7** Territorial specialization — per-colonia market briefs (price trends, inventory, sentiment, notable signals) generated on demand for any target zone  
**FR-1.8** Territory expertise profiles — persistent per-colonia intelligence dossiers updated on each ingestion cycle (price band mix, DOM trajectory, sentiment trend, active programs)  

### Module 2: Sentiment Intelligence
**FR-2.1** Topic modeling on community Q&A — clusters: Infonavit/financing, pricing, neighborhoods, legal, amenities  
**FR-2.2** Sentiment polarity — positive/negative/neutral by topic, municipality, time window  
**FR-2.3** Question intent classification — buy/sell/rent/finance/legal/investment  
**FR-2.4** Trend detection — topic frequency and sentiment velocity over 7/30/90 days  
**FR-2.5** Neighborhood sentiment profiles — safety, amenities, development, gentrification signals per colonia  
**FR-2.6** Pain point extraction — urgency keywords, financing barriers, legal concerns, agent complaints with frequency tracking  
**FR-2.7** Source attribution — every insight traces to source URL, author (public display name), date, platform  
**FR-2.8** Broker question intake — broker submits a question (e.g., "¿Qué está pasando en la colonia X con casas de $4M-6M?"); system returns a structured advisory brief grounded in market data + community sentiment + relevant programs, with all sources cited  

### Module 3: Market Alerts
**FR-3.1** Price reduction alerts — % drop threshold configurable per user/saved search  
**FR-3.2** Urgency keyword detection — "venta urgente", "remate", "liquidación", "reducción de precio", "urgent sale"  
**FR-3.3** Saved criteria matching — new listings matching user-defined filters (area, type, price, features)  
**FR-3.4** Development/zoning signals — new development announcements, zoning changes, infrastructure projects, permit filings in target zones  
**FR-3.5** Competitive intelligence alerts — competitor listing activity, broker network moves, portfolio transactions, institutional buyer signals  
**FR-3.6** Delivery channels — in-app, email, webhook (API), scheduled digest  

### Module 4: SaaS Subscriptions
**FR-4.1** Tier: Starter (individual broker) — dashboard + basic alerts + 5 exports/mo  
**FR-4.2** Tier: Growth (small agency, 2-5 seats) — + sentiment intelligence + 50 exports/mo + API access (1k calls/mo)  
**FR-4.3** Tier: Scale (developer/fund, 5-20 seats) — + competitive alerts + 500 exports/mo + API (50k calls/mo) + webhooks  
**FR-4.4** Tier: Custom (enterprise, 20+ seats) — white-label, dedicated support, custom integrations, SLA, unlimited exports/API  
**FR-4.5** Billing — per-seat monthly, 20% annual discount, usage-based API overage, Stripe integration  
**FR-4.6** Role-based access — admin, analyst, operator, read-only per tier  
**FR-4.7** Trial — 14-day free trial for Starter/Growth, demo for Scale/Custom  

### Module 5: Controlled Exports
**FR-5.1** Formats — CSV, Excel, PDF reports, GeoJSON (GIS), PNG/SVG charts  
**FR-5.2** Role-based export gates — Starter: manual CSV/Excel/PDF only; Growth+: all formats + scheduled + API  
**FR-5.3** Audit log — every export records user, timestamp, filters, row count, format  
**FR-5.4** Watermarking — dynamic watermark with user ID, timestamp, tier on PDF/Excel exports  
**FR-5.5** Scheduled exports — recurring daily/weekly/monthly with email delivery  
**FR-5.6** Data minimization — exports respect LFPDPPP: no unnecessary PII, public display names only, attribution preserved  

## 6. Non-Functional Requirements

**NFR-1** Compliance — LFPDPPP full compliance; no mass scraping; official APIs only with credentials; robots.txt/ToS respected; data minimization; attribution/traceability preserved  
**NFR-2** Security — SSRF mitigation (host validation, redirect blocking), HTTPS only, secrets in env vars, no PII in logs  
**NFR-3** Performance — Dashboard loads <3s; alerts delivered <5min of trigger; exports <30s for 10k rows  
**NFR-4** Availability — 99.5% uptime SLA for Scale/Custom tiers; 99% for Starter/Growth  
**NFR-5** Scalability — PostgreSQL handles 1M+ properties, 10M+ community content items; horizontal read replicas for analytics  
**NFR-6** Observability — Structured logging, metrics (latency, error rate, alert delivery), health endpoints  

## 7. Success Metrics

| Metric | Target (90 days) | Target (1 year) |
| --- | --- | --- |
| Activated community sources | 10/20 | 18/20 |
| Portal partnerships / official APIs | 1-2 | 4+ |
| Paying subscribers (Starter+) | 25 | 200 |
| Monthly active users | 50 | 500 |
| Alert precision (relevant/total) | >70% | >85% |
| Export volume (rows/mo) | 100k | 5M |
| NPS (brokers) | >30 | >50 |
| Churn (monthly) | <5% | <3% |
| **Transactions influenced** (broker-reported deals where Fábrica Intel advisory was used) | 15 | 200+ |
| **Advisory briefs generated** (FR-2.8 broker questions answered) | 50 | 2,000+ |

**Counter-metrics** (watch for gaming):

- Alert click-through rate dropping while alert volume rises → alerts are noise, not signal
- Export row count rising while MAU flat → exports are bulk-downloads, not workflow use
- High churn in first 30 days → onboarding/first-value gap, not product-market fit

## 8. Constraints & Risks

| Risk | Likelihood | Impact | Mitigation |
|------|------------|--------|------------|
| Portal partnerships not secured | High | High | Launch with community + govt data first; partnership BD parallel |
| LFPDPPP legal challenge on community content | Medium | High | Legal review pre-launch; conservative ingestion; attribution mandatory |
| Community content density insufficient | Medium | High | Activate Reddit API + Infonavit official first; Facebook Graph if authorized |
| Competitor launches data product | Low | Medium | Speed to MVP; lock in brokers with workflow integration |
| Technical debt from Python/Streamlit stack | Medium | Medium | Modular architecture; API layer separable for future Next.js migration |

## 9. MVP Scope (90 Days)

### Must Have
- PostgreSQL schema for properties, source_configs, community_content, alerts, users, subscriptions, exports
- Ingestion pipeline: JSON raw → CSV export → PostgreSQL (existing, hardened)
- Module 1: Dashboard (4 core views)
- Module 2: Sentiment Intelligence (topic modeling, sentiment, neighborhood profiles, pain points)
- Module 3: Market Alerts (price drops, urgency keywords, criteria matching, dev/zoning, competitive)
- Module 4: Starter + Growth tiers with Stripe billing
- Module 5: Controlled Exports (CSV, Excel, PDF, GeoJSON, PNG/SVG + RBAC + audit + watermarking + scheduled)
- LFPDPPP compliance review complete
- 10 community sources activated (Reddit, Infonavit, forums, local news)
- 1 portal partnership / official API secured

### Should Have
- Scale tier + API access + webhooks
- Custom tier discovery calls
- Advanced alert filtering (ML-based relevance scoring)

### Could Have
- White-label Custom tier
- Mobile-responsive Streamlit enhancements

### Won't Have (v1)
- Listing aggregation from portals without partnership
- Facebook Graph API (pending authorization)
- AI-generated narrative reports
- Multi-language beyond Spanish

### Non-Goals (explicitly out of scope for this PRD)
- Listing aggregation / scraping portals without written partnership or official API authorization
- Operating as a transaction marketplace (no offers, no escrow, no agent matching)
- Consuming private social media accounts, auth bypass, or paywall evasion
- Replacing licensed legal or tax advisory
- Building proprietary map tiles or GIS engine — use open-source (OpenStreetMap/Leaflet)
- Mobile native apps at v1

## 10. Roadmap

| Phase | Timeline | Focus |
|-------|----------|-------|
| **MVP** | 0-90 days | Core 5 modules, Starter/Growth tiers, 10 community sources, 1 portal API |
| **v1.1** | 90-180 days | Scale tier, API/webhooks, 2+ portal APIs, ML alert relevance |
| **v1.5** | 180-270 days | Custom tier, white-label, advanced analytics, mobile app |
| **v2.0** | 270-360 days | Next.js/TypeScript frontend migration, marketplace features, internationalization |

## 11. Glossary

| Term | Definition |
| --- | --- |
| **Fábrica Intel** | The Real Estate Intelligence SaaS platform (working name) |
| **Colonia** | Official neighborhood subdivision within a Mexican municipality (e.g., Roma Norte, Polanco) |
| **Municipality** | Administrative division containing colonias (e.g., Toluca, Metepec, Cuauhtémoc) |
| **DOM** | Days on Market — days a listing has been active |
| **Community content** | User-generated Q&A, forum posts, and social discussions ingested via authorized channels |
| **Sentiment** | Polarity (positive/negative/neutral) derived from community content |
| **Alert** | Triggered notification when a configured condition is met (price drop, urgency keyword, new listing match, dev/zoning signal, competitive event) |
| **Advisory brief** | Structured answer to a broker-submitted question (FR-2.8), grounded in market data + community sentiment, with cited sources |
| **Territory dossier** | Persistent per-colonia intelligence profile (FR-1.8): price band mix, DOM trajectory, sentiment trend, active programs |
| **Tier** | Subscription plan: Starter / Growth / Scale / Custom |
| **LFPDPPP** | Ley Federal de Protección de Datos Personales en Posesión de los Particulares — Mexican Federal Law on Personal Data Protection |
| **Source registry** | `source_configs.csv` — the compliance authority for every ingested source (access method, robots policy, legal basis, status) |

## 12. Open Questions

1. **User tiering validation** — Confirm broker willingness to pay at Starter/Growth price points via 5-10 interviews
2. **Portal partnership terms** — API rate limits, data freshness, commercial terms for Inmuebles24/Lamudi/Vivanuncios/Propiedades.com/Mercado Libre
3. **LFPDPPP legal opinion** — Specific review for community Q&A ingestion, sentiment analysis, and export of derived insights
4. **Pricing calibration** — Exact MXN price points per tier after buyer interviews
5. **Community content density** — Measure actual signal volume from activated sources before committing to sentiment ML investment