$ErrorActionPreference = "Stop"

$containerName = "mexico-property-db"
$projectRoot = Split-Path -Parent $MyInvocation.MyCommand.Path
Set-Location $projectRoot

if (-not (docker ps -a --format '{{.Names}}' | Select-String -SimpleMatch $containerName)) {
    docker run --name $containerName `
      -e POSTGRES_USER=postgres `
      -e POSTGRES_PASSWORD=postgres `
      -e POSTGRES_DB=property_data `
      -p 5432:5432 `
      -d postgres:16-alpine
}

if (-not (docker ps --format '{{.Names}}' | Select-String -SimpleMatch $containerName)) {
    docker start $containerName
}

$schemaFile = Join-Path $projectRoot "db_schema.sql"
$tablesExist = docker exec $containerName psql -U postgres -d property_data -tAc "SELECT COUNT(*) FROM information_schema.tables WHERE table_schema = 'public' AND table_name IN ('sources', 'properties', 'compliance_audit', 'source_registry', 'community_content', 'property_followups', 'alliance_contacts', 'kpi_entries', 'monitoring_alerts');"

if ([int]$tablesExist.Trim() -lt 9) {
    docker cp $schemaFile "$containerName`:/tmp/db_schema.sql"
    docker exec $containerName psql -U postgres -d property_data -f /tmp/db_schema.sql
}

if (-not (Test-Path ".venv\Scripts\python.exe")) {
    python -m venv .venv
    if ($LASTEXITCODE -ne 0) {
        throw "Failed to create the Python virtual environment (exit code $LASTEXITCODE)."
    }
}

.\.venv\Scripts\python.exe -m pip install -r requirements.txt
if ($LASTEXITCODE -ne 0) {
    throw "Dependency installation failed (exit code $LASTEXITCODE)."
}

.\.venv\Scripts\python.exe ingest_sources.py
if ($LASTEXITCODE -ne 0) {
    throw "Source ingestion failed (exit code $LASTEXITCODE)."
}

.\.venv\Scripts\python.exe import_to_postgres.py
if ($LASTEXITCODE -ne 0) {
    throw "Import to PostgreSQL failed (exit code $LASTEXITCODE)."
}

Write-Host "Pipeline completed successfully."
