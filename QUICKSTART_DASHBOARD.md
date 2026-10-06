# Quick Loading Guide — Streamlit Dashboard

Fastest way to get the interactive dashboard running on Windows. Run the commands from the project root (the folder containing `run_pipeline.ps1`).

## Prerequisites

- Docker Desktop running (PostgreSQL runs in the `mexico-property-db` container)
- Python 3 (the guide uses the project `.venv`)
- `.env` in the project root with the PostgreSQL connection settings. Create it if it does not exist; this file is ignored by Git:

```env
POSTGRES_HOST=localhost
POSTGRES_PORT=5432
POSTGRES_DB=property_data
POSTGRES_USER=postgres
POSTGRES_PASSWORD=postgres
```

`POSTGRES_PORT` must match the host-side port published by Docker for the database container. A newly created container uses port `5432`; for an existing container, check the published port:

```powershell
docker port mexico-property-db 5432
```

For example, if the output is `127.0.0.1:5433`, set `POSTGRES_PORT=5433` in `.env`. The dashboard and data importer both read these settings.

## Fast path (first run or data refresh)

```powershell
powershell -ExecutionPolicy Bypass -File .\run_pipeline.ps1
./.venv/Scripts/python.exe -m streamlit run streamlit_app.py
```

Run these commands from the project root. The execution-policy bypass applies only to this invocation; it does not change the machine's policy.

The pipeline script automatically:
1. creates/starts the `mexico-property-db` Docker container,
2. applies `db_schema.sql` if tables are missing,
3. creates `.venv` if needed and installs `requirements.txt`,
4. runs `ingest_sources.py` and `import_to_postgres.py`.

It stops with an error if a Python setup, ingestion, or import command fails.

## Quick path (DB and data already set up)

```powershell
./.venv/Scripts/python.exe -m streamlit run streamlit_app.py
```

Then open **http://localhost:8501** in your browser (Streamlit opens it automatically). If the browser does not open, use that URL directly.

## If PostgreSQL is not running

```powershell
docker start mexico-property-db
```

Wait a few seconds for it to accept connections. Confirm the host port with `docker port mexico-property-db 5432` and make sure it matches `POSTGRES_PORT` in `.env`, then launch Streamlit with the quick path above.

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
| `No se pudo conectar a PostgreSQL` in the browser | Start the container with `docker start mexico-property-db`, check its published port using `docker port mexico-property-db 5432`, and ensure that port matches `POSTGRES_PORT` in `.env`. Restart the dashboard after changing `.env`. |
| Connection refused on `localhost:5432` while the container is running | The container may be published on a different host port. Run `docker port mexico-property-db 5432` and set `POSTGRES_PORT` in `.env` to the reported host port (for example, `5433`), then restart the dashboard. |
| Analytics cannot load `community_content` | Check the PostgreSQL connection and table; a successful query with no rows shows a separate import-data prompt. |
| Empty tables / zero properties | Run `powershell -ExecutionPolicy Bypass -File .\run_pipeline.ps1` from the project root to ingest and import data. |
| Port already in use | Another Streamlit instance is running: close it, or launch on another port with `--server.port 8502`. |
| `streamlit` not recognized | Use the full interpreter path `./.venv/Scripts/python.exe -m streamlit ...` instead. |
| PowerShell says the script is not digitally signed | Run it with `powershell -ExecutionPolicy Bypass -File .\run_pipeline.ps1`; this bypass applies only to that invocation. |
| Credentials error | Check that `POSTGRES_DB`, `POSTGRES_USER`, and `POSTGRES_PASSWORD` in `.env` match the database container. The defaults used by the pipeline are `property_data`, `postgres`, and `postgres`. |

## What you should see

The app title is **"Operaciones inmobiliarias de México"** with a sidebar offering three workspaces — `Panel principal`, `Análisis y hallazgos`, and `Tendencias` — plus filters for state, property type, source, and price band. The main panel opens on an executive summary and a top-five listing order based on an experimental, unvalidated heuristic. The index uses the filtered-set average asking price, fixed source weights, and recorded listing, legal-status, and location fields; its weighted score is normalized to reduce saturation at the upper bound. It does not use local comparables or independently verify those fields. It is not a risk measure or investment recommendation. Confirm listing validity, comparable prices, and legal documents independently before acting. Summary counts, legal-review totals, the median price, and the top-five ordering cover the complete filtered result set; the Pipeline table loads 50 properties per page and shows its exact total. Operational tables (`property_followups`, `alliance_contacts`, `kpi_entries`, `monitoring_alerts`, `export_history`) are created automatically on first launch.

For full details, see the *Interactive dashboard* section in [README.md](README.md).
