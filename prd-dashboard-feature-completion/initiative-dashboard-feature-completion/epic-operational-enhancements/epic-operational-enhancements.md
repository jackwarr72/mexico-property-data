---
type: epic
---

# Epic: Operational Enhancements

## Goal
Enhance dashboard operations with manual data refresh, global filter sharing across widgets, background export jobs with progress tracking, and file lifecycle management.

## Outcome
Users can manually refresh data to see the latest property listings and analytics without reloading the entire page. Filters applied in the sidebar are shared across all widgets in the current workspace so that filtering by state, property type, or price band updates all views simultaneously. Large export jobs run in the background with progress indication, status tracking in the export history table, and automatic file cleanup after expiration.

## References
- PRD: `../../prd-dashboard-feature-completion.md` (FR-11, FR-12, FR-13)
- `streamlit_app.py:747-765` — sidebar filters
- `export_service.py` — export service implementation
- `ROADMAP_FUTURO.md` Sections 2 and 3 (Dashboard, Exportaciones)

## Done When
- Manual refresh button in sidebar reloads all data (FR-11)
- Auto-refresh on configurable interval (FR-11)
- Filters shared across all widgets in current workspace (FR-12)
- Filters persist in session state (FR-12)
- Background export jobs with progress bar (FR-13)
- Export history shows job status (pending, completed, failed) (FR-13)
- Automatic file cleanup after 7 days (FR-13)
- Access controls on export generation (FR-13)
