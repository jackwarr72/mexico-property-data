# Mexico Property Data Project

This project is a compliant property-data ingestion pipeline for Mexico.

Consulta [ROADMAP_FUTURO.md](ROADMAP_FUTURO.md) para el resumen de funciones actuales, mejoras futuras, restricciones legales y técnicas, pruebas y prioridades de evolución.

## Purpose
Collect and normalize property listing data from sources with explicit legal access, partner status, or public-data licensing.

## Important
This project does not rely on scraping restricted consumer portals like Inmuebles24, Lamudi, or Mercado Libre without partner or API access.

## Project structure
- sources.json: source registry with compliance metadata
- property_schema.json: normalized property schema
- ingest_sources.py: basic ingestion, normalization, deduplication, and CSV export
- db_schema.sql: PostgreSQL schema
- import_to_postgres.py: import normalized CSV into PostgreSQL
- data/raw: source data files
- data/export: normalized output

## Installation
```bash
python -m venv .venv
source .venv/bin/activate   # Linux/macOS
# or .venv\Scripts\activate  # Windows
pip install -r requirements.txt
```

## Usage
```bash
python ingest_sources.py
python import_to_postgres.py
```

## Run locally with Docker + PostgreSQL

1. Start a PostgreSQL container from the project root:
```bash
docker run --name mexico-property-db \
  -e POSTGRES_USER=postgres \
  -e POSTGRES_PASSWORD=postgres \
  -e POSTGRES_DB=property_data \
  -p 5432:5432 \
  -d postgres:16-alpine
```

2. Load the schema:
```bash
docker cp db_schema.sql mexico-property-db:/tmp/db_schema.sql
docker exec mexico-property-db psql -U postgres -d property_data -f /tmp/db_schema.sql
```

3. Run the pipeline:
```bash
python ingest_sources.py
python import_to_postgres.py
```

4. To stop and remove the container:
```bash
docker stop mexico-property-db
docker rm mexico-property-db
```

## Environment configuration
The app reads PostgreSQL settings from environment variables so you can run it without editing code.
Create a `.env` file in the project root:

```env
POSTGRES_HOST=localhost
POSTGRES_PORT=5432
POSTGRES_DB=property_data
POSTGRES_USER=postgres
POSTGRES_PASSWORD=postgres
```

Then either export them in your shell or use a loader such as `python-dotenv` if you add it later.

## One-command local run

On Windows PowerShell:
```powershell
./run_pipeline.ps1
```

On macOS/Linux:
```bash
chmod +x run_pipeline.sh
./run_pipeline.sh
```

These scripts will:
- create/start the local PostgreSQL container,
- apply the schema from `db_schema.sql`,
- create the virtual environment if needed,
- install requirements,
- run the ingestion job,
- import the normalized records into PostgreSQL.

## Inspecting imported data

Run a quick summary in Postgres:
```bash
python query_properties.py
```

This prints a grouped breakdown by source with counts and price ranges.

To export a CSV summary to `data/export/property_summary.csv`:
```bash
python summarize_properties.py
```

## CSV market dashboard

Generate a CSV dashboard grouped by city and by property type:
```bash
python market_dashboard.py
```

Optional filters:
```bash
python market_dashboard.py --state "Ciudad de México"
python market_dashboard.py --min-price 5000000 --max-price 10000000
python market_dashboard.py --state "Ciudad de México" --min-price 3000000 --max-price 15000000
```

Filtered runs use distinct filenames, for example:
- data/export/market_dashboard_ciudad_de_mexico_3m_15m_by_city.csv
- data/export/market_dashboard_ciudad_de_mexico_3m_15m_by_property_type.csv
- data/export/market_dashboard_ciudad_de_mexico_3m_15m_by_state_and_price_band.csv

Invalid ranges such as a negative price or a minimum greater than the maximum are rejected. If a valid filter matches no records, the script writes headers-only CSV files and prints a warning.

This creates:
- data/export/market_dashboard_by_city.csv
- data/export/market_dashboard_by_property_type.csv
- data/export/market_dashboard_by_state_and_price_band.csv

The state + price band file is especially useful for filtering by both market segment and price tier.

## Interactive dashboard

Start the Streamlit dashboard after PostgreSQL is running and the pipeline has imported data:
```bash
streamlit run streamlit_app.py
```

The dashboard provides selectors for state, property type, and price band, plus summary metrics and filtered tables.

The dashboard also includes:
- Properties: interactive listing table, detailed property sheet, and persisted follow-up notes.
- Strategic alliances: contact directory for brokers, notaries, appraisers, lawyers, and lenders.
- KPIs: manual daily registration with comparisons against 20+ properties per day and 10+ appointments per week.
- Business intelligence: source and property-type summaries with charts.
- Monitoring alerts: keyword scans for terms such as `Urgent Sale` and `Reduction Price`.
- Advanced search: Google query generation using `site:`, `intitle:`, and `inurl:` operators.

The sidebar workspace selector now also provides:
- `Analytics / Insights`: quick stats, trending questions, location activity, sentiment over time, intent concerns, AI-insight cards, and filterable discussion results.
- `Trends`: emerging trends, topic evolution for the last 90 days, and dynamically sorted neighborhood rankings.

Analytics data is isolated behind [analytics_data.py](analytics_data.py). When `community_content` is empty, the UI uses clearly labeled deterministic demo data; once authorized community content is imported, the provider builds analytics from PostgreSQL rows. The current Streamlit architecture does not expose URL routes, so the Trends page is implemented as a dedicated workspace rather than `/trends`.

Analytics and Trends now expose reusable exports for the current view or full report:
- CSV: UTF-8 structured data for the selected dataset;
- Excel: formatted multi-sheet workbook with summary, questions, discussions, sentiment, topics, concerns, trends, neighborhoods, and raw data;
- PDF: executive report with active filters, tables, sentiment chart, trends, and clearly labeled AI insight data/interpretation/opportunity sections;
- JSON: structured analytics sections plus filter metadata;
- PNG/SVG: actual sentiment chart exports rather than browser screenshots.

Files are written to `data/exports` with descriptive names such as `real-estate-intelligence-metepec-last-30-days.pdf`. Exports use the same `AnalyticsData` object as the dashboard and completed jobs are recorded in the `export_history` PostgreSQL table. The current local dataset uses immediate downloads; a queue/worker can later be placed behind the same service functions for large exports.

The first dashboard launch creates these additional tables if they do not exist: `property_followups`, `alliance_contacts`, `kpi_entries`, and `monitoring_alerts`.

## Output
The script writes:
- data/export/properties.csv
- data/export/property_summary.csv
- data/export/market_dashboard_by_city.csv
- data/export/market_dashboard_by_property_type.csv
- data/export/market_dashboard_by_state_and_price_band.csv
- into PostgreSQL via import_to_postgres.py

## Public community and housing-content ingestion

The community discovery registry is in `community_sources.json`. It covers:
- real-estate forums and Q&A: InmobiliariaWeb.com, Lamudi, Vivanuncios, Mercado Libre Real Estate Q&A, and Propiedades.com;
- Reddit communities including `r/Mexico`, `r/MexicoFinanciero`, `r/EstadoDeMexico`, `r/PersonalFinanceMexico`, and `r/mexicoexpats`;
- Facebook public-group targets, Quora Spanish, LinkedIn public discussions, local news, official Infonavit/FOVISSSTE-style housing-program content, and public social hashtag discovery for Facebook, X/Twitter, TikTok, and YouTube;
- Mexico-wide coverage with priority for Estado de Mexico, Toluca, Metepec, Lerma, Zinacantepec, San Mateo Atenco, Mexicaltzingo, and Calimaya.

Every registry entry records its URL, discovery method, access method, robots/crawl policy, frequency, enablement, content types, geography, adapter, deduplication strategy, timestamps, error state, legal basis, and attribution metadata. The registry is intentionally conservative: community and social sources are disabled by default until an official API, permitted feed, partner authorization, or reviewed export is available.

Place an authorized or manually reviewed JSON export in `data/raw/<source_key>.json`. The ingestion pipeline recognizes forum posts, questions and answers, discussions, comments, public social posts, public video comments, articles, housing-program questions, and investment discussions. It writes:
- `data/export/community_content.csv`
- `data/export/source_configs.csv`

The normalized field contract is defined in [community_content_schema.json](community_content_schema.json), and imported into PostgreSQL tables `community_content` and `source_registry`.

Discovery evidence and review decisions are recorded in [source_discovery_notes.md](source_discovery_notes.md).

## Testing imports

Run the transformation tests:
```powershell
.\.venv\Scripts\python.exe -m unittest discover -s tests -v
```

Run the full local import check:
```powershell
.\.venv\Scripts\python.exe ingest_sources.py
.\.venv\Scripts\python.exe import_to_postgres.py
docker exec mexico-property-db psql -U postgres -d property_data -c "SELECT 'properties' AS table_name, COUNT(*) AS rows FROM properties UNION ALL SELECT 'source_registry', COUNT(*) FROM source_registry UNION ALL SELECT 'community_content', COUNT(*) FROM community_content;"
```

For an authorized community export, place a JSON array at `data/raw/<source_key>.json`, for example:
```json
[
  {
    "post_id": "approved-post-1",
    "content_type": "forum_posts",
    "title": "Public discussion title",
    "body": "Public content supplied through an authorized export",
    "source_url": "https://example.org/public/thread/1",
    "state": "Estado de Mexico",
    "municipality": "Metepec",
    "asking_price": 3500000,
    "extracted_keywords": ["Infonavit", "venta"]
  }
]
```

The filename must match a `source_key` in `community_sources.json`. After running the two pipeline commands, the record should appear in `data/export/community_content.csv` and the PostgreSQL `community_content` table. Do not use synthetic or unreviewed content in production imports.

Do not scrape private accounts or groups, bypass authentication or technical controls, ignore robots rules, exceed rate limits, or use Facebook Graph API/X/Twitter/TikTok/YouTube APIs without the required official authorization. Official housing information is stored separately from user-generated discussion by `source_type` and `legal_status`.
