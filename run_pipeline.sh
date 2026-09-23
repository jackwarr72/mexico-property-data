#!/usr/bin/env bash
set -euo pipefail

CONTAINER_NAME="mexico-property-db"
PROJECT_ROOT="$(cd "$(dirname "$0")" && pwd)"
cd "$PROJECT_ROOT"

if ! docker ps -a --format '{{.Names}}' | grep -Fxq "$CONTAINER_NAME"; then
  docker run --name "$CONTAINER_NAME" \
    -e POSTGRES_USER=postgres \
    -e POSTGRES_PASSWORD=postgres \
    -e POSTGRES_DB=property_data \
    -p 5432:5432 \
    -d postgres:16-alpine
fi

if ! docker ps --format '{{.Names}}' | grep -Fxq "$CONTAINER_NAME"; then
  docker start "$CONTAINER_NAME"
fi

TABLE_COUNT=$(docker exec "$CONTAINER_NAME" psql -U postgres -d property_data -tAc "SELECT COUNT(*) FROM information_schema.tables WHERE table_schema = 'public' AND table_name IN ('sources', 'properties', 'compliance_audit', 'source_registry', 'community_content', 'property_followups', 'alliance_contacts', 'kpi_entries', 'monitoring_alerts');")

if [ "$TABLE_COUNT" -lt 9 ]; then
  docker cp "$PROJECT_ROOT/db_schema.sql" "$CONTAINER_NAME:/tmp/db_schema.sql"
  docker exec "$CONTAINER_NAME" psql -U postgres -d property_data -f /tmp/db_schema.sql
fi

if [ ! -x .venv/bin/python ]; then
  python3 -m venv .venv
fi

.venv/bin/python -m pip install -r requirements.txt
.venv/bin/python ingest_sources.py
.venv/bin/python import_to_postgres.py

echo "Pipeline completed successfully."
