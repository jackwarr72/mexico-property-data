---
type: epic
---

# Epic: Enhanced Exports

## Goal
Enhance the dashboard's export capabilities with improved PDF formatting, vector chart exports, per-widget table exports, and GeoJSON support for geographic data.

## Outcome
Users can export filtered data in multiple formats with professional formatting. PDF exports include visual identity, proper pagination, fonts, and vector SVG charts rather than rasterized screenshots. Each analytics widget can export its visible filtered table. Geographic data can be exported as GeoJSON for use in mapping applications. All exports preserve UTF-8 encoding for Spanish characters and use descriptive, safe filenames.

## References
- PRD: `../../prd-dashboard-feature-completion.md` (FR-4, FR-5, FR-6)
- `export_service.py` — current export service implementation
- `streamlit_app.py:399-436` — render_export_controls
- `ROADMAP_FUTURO.md` Section 2 (Exportaciones)

## Done When
- PDF exports include visual identity, pagination, fonts, and vector charts (FR-4)
- Each analytics widget can export its filtered table as CSV (FR-5)
- GeoJSON export format available for geographic data (FR-6)
- Export filenames include timestamps and active filter descriptions
- UTF-8 encoding preserved for all export formats
- Export history table remains accurate and complete
