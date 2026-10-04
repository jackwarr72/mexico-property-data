# Quick Loading Guide — Streamlit Dashboard

Fastest way to get the interactive dashboard running on Windows (PowerShell), from the project root `c:\Users\jacku\OneDrive\Desktop\mexico-property-data`.

## Prerequisites

- Docker Desktop running (PostgreSQL runs in the `mexico-property-db` container)
- Python 3 (the guide uses the project `.venv`)
- `.env` in the project root with the PostgreSQL credentials (already present in this repo):

```env
POSTGRES_HOST=localhost
POSTGRES_PORT=5432
POSTGRES_DB=property_data
POSTGRES_USER=postgres
POSTGRES_PASSWORD=postgres
```

## Fast path (first run or data refresh)

```powershell
./run_pipeline.ps1
./.venv/Scripts/python.exe -m streamlit run streamlit_app.py
```

The pipeline script automatically:
1. creates/starts the `mexico-property-db` Docker container,
2. applies `db_schema.sql` if tables are missing,
3. creates `.venv` if needed and installs `requirements.txt`,
4. runs `ingest_sources.py` and `import_to_postgres.py`.

## Quick path (DB and data already set up)

```powershell
./.venv/Scripts/python.exe -m streamlit run streamlit_app.py
```

Then open **http://localhost:8501** in your browser (Streamlit opens it automatically).

## If PostgreSQL is not running

```powershell
docker start mexico-property-db
```

Wait a few seconds for it to accept connections, then launch Streamlit with the quick path above.

## Verify data loaded

```powershell
./.venv/Scripts/python.exe query_properties.py
```

Or directly in SQL:

```powershell
docker exec mexico-property-db psql -U postgres -d property_data -c "SELECT COUNT(*) FROM properties;"
```

## Stop

- Dashboard: `Ctrl+C` in the Streamlit terminal.
- Database (optional): `docker stop mexico-property-db`

## Troubleshooting

| Symptom | Fix |
| --- | --- |
| `No se pudo conectar a PostgreSQL` in the browser | `docker start mexico-property-db`, wait ~5 s, then refresh the page. |
| Analytics cannot load `community_content` | Check the PostgreSQL connection and table; a successful query with no rows shows a separate import-data prompt. |
| Empty tables / zero properties | Run `./run_pipeline.ps1` once to ingest and import data. |
| Port already in use | Another Streamlit instance is running: close it, or launch on another port with `--server.port 8502`. |
| `streamlit` not recognized | Use the full interpreter path `./.venv/Scripts/python.exe -m streamlit ...` instead. |
| Credentials error | Check the `.env` values match the container (`postgres`/`postgres` by default). |

## What you should see

The app title is **"Operaciones inmobiliarias de México"** with a sidebar offering three workspaces — `Panel principal`, `Análisis y hallazgos`, and `Tendencias` — plus filters for state, property type, source, and price band. The main panel opens on an executive summary and a top-five listing order based on an experimental, unvalidated heuristic. The index uses the filtered-set average asking price, fixed source weights, and recorded listing, legal-status, and location fields; its weighted score is normalized to reduce saturation at the upper bound. It does not use local comparables or independently verify those fields. It is not a risk measure or investment recommendation. Confirm listing validity, comparable prices, and legal documents independently before acting. Summary counts, legal-review totals, the median price, and the top-five ordering cover the complete filtered result set; the Pipeline table loads 50 properties per page and shows its exact total. Operational tables (`property_followups`, `alliance_contacts`, `kpi_entries`, `monitoring_alerts`, `export_history`) are created automatically on first launch.

For full details, see the *Interactive dashboard* section in [README.md](README.md).
