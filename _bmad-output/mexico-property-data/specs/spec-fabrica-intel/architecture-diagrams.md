# Architecture Diagrams — Fábrica Intel

## System context

```
                     ┌─────────────────────────────────────────────────────┐
                     │                     Internet                         │
                     │  Authorized sources (partnership/API/official)      │
                     │  Inmuebles24 · Lamudi · Vivanuncios ·              │
                     │  Propiedades.com · Mercado Libre Inmuebles          │
                     │  Reddit API · Infonavit · local news · forums      │
                     └──────────────┬──────────────────────────────────────┘
                                    │ HTTPS only, require_public_host()
                                    │ no redirects, rate-limited, logged
                                    ▼
┌──────────────────────────────────────────────────────────────────────────────┐
│                        Fábrica Intel ingestion layer                          │
│  ┌────────────┐ ┌──────────────┐ ┌──────────────┐ ┌─────────────────────┐  │
│  │ adapter    │ │ adapter     │ │ adapter      │ │ community adapter   │  │
│  │ (listings) │ │ (listings)  │ │ (listings)   │ │ (Q&A / sentiment)   │  │
│  │ per source│ │ per source  │ │ per source   │ │ per source          │  │
│  └─────┬──────┘ └──────┬───────┘ └──────┬───────┘ └──────────┬──────────┘  │
│        │               │                │                     │             │
│        └───────────────┼────────────────┼─────────────────────┘             │
│                        ▼                ▼                                   │
│              ┌──────────────────────────────────────┐                       │
│              │  ingest_sources.py                   │                       │
│              │  normalize → dedupe → CSV export     │                       │
│              └──────────────────┬───────────────────┘                       │
│                                     ▼                                           │
│              ┌──────────────────────────────────────┐                       │
│              │  import_to_postgres.py               │                       │
│              │  CSV → PostgreSQL (ON CONFLICT upsert)│                       │
│              └──────────────────┬───────────────────┘                       │
└─────────────────────────────────────┼──────────────────────────────────────┘
                                      │
                    ┌─────────────────┴──────────────────┐
                    ▼                                    ▼
        ┌───────────────────────┐          ┌──────────────────────────┐
        │   PostgreSQL          │          │   Alert engine           │
        │   (source of truth)   │          │   (APScheduler + Redis)  │
        │                       │          │                          │
        │  properties           │          │  On each ingestion cycle │
        │  source_registry      │          │  evaluate rules → emit  │
        │  community_content    │          │  → in-app / email /      │
        │  users                │          │    webhook / digest      │
        │  subscriptions        │          └───────────┬──────────────┘
        │  saved_searches       │                      │
        │  alerts               │                      │
        │  alert_deliveries     │                      │
        │  export_jobs          │                      │
        │  export_audit         │                      │
        │  territory_dossiers   │                      │
        │  analytics_mviews     │                      │
        └───────────┬───────────┘                      │
                    │ SQL                              │
                    └──────────────┬───────────────────┘
                                   ▼
                    ┌──────────────────────────────┐
                    │   Analytics engine           │
                    │   (materialized views +      │
                    │    SQL rollups)              │
                    └──────────────┬───────────────┘
                                   │
                    ┌──────────────┴───────────────┐
                    ▼                              ▼
        ┌───────────────────────┐      ┌──────────────────────────────┐
        │   FastAPI app         │      │   Streamlit dashboard        │
        │   /api/v1/*           │      │   (reads analytics mviews)   │
        │   auth · alerts ·     │      │                              │
        │   exports · billing   │      │                              │
        │   advisory briefs     │      │                              │
        └───────────┬───────────┘      └──────────────────────────────┘
                    │ REST
                    │ (authenticated)
                    │
        ┌───────────┴──────────────────────────┐
        │   Export service (reuse)             │
        │   export_service.py                  │
        │   CSV / Excel / PDF / GeoJSON / PNG   │
        │   + watermark + audit log            │
        └──────────────────────────────────────┘
                    │
        ┌───────────┴──────────────────────────┐
        │   Billing                             │
        │   Stripe SDK                          │
        │   webhooks: invoice.paid,             │
        │   customer.subscription.updated       │
        └──────────────────────────────────────┘
```

## Data flow — ingestion cycle

```
source_registry (enabled, allowed_use != restricted)
        │
        ▼
  adapter fetch (require_public_host, no redirect, rate limit)
        │
        ▼
  raw JSON → normalize_record / normalize_community_record
        │
        ▼
  dedupe()  (key = listing_id | content_id | source_url | source+address+price)
        │
        ▼
  export CSV → import_to_postgres ON CONFLICT DO UPDATE
        │
        ▼
  refresh analytics materialized views
        │
        ▼
  alert engine evaluates rules → alert_deliveries
        │
        ▼
  territory_dossiers updated for affected colonias
```

## Security boundary

```
Client HTTPS → Reverse proxy (TLS terminate)
        │
        ▼
  FastAPI (JWT auth, rate limit via Redis)
        │
        ▼
  PostgreSQL (TLS, least-privilege role, no secrets in logs)
        │
        ▼
  Outbound fetches → require_public_host() → allowlist only
```