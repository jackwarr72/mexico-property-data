---
type: epic
---

# Epic: Data Quality Review System

## Goal
Implement a property review status system and price change history tracking to support data quality workflows and human review processes.

## Outcome
Properties in the dashboard have a review status (new, reviewed, approved, rejected, archived) that can be tracked and filtered. Price changes are automatically detected and recorded with history of previous prices, change dates, and percentage change. Legal review counts and data quality metrics are visible to users, enabling systematic review of new and modified listings.

## References
- PRD: `../../prd-dashboard-feature-completion.md` (FR-9, FR-10)
- `streamlit_app.py:58-87` — ensure_operational_tables
- `ROADMAP_FUTURO.md` Section 2 (Datos y backend, Data quality)

## Done When
- Properties have a review status column (new, reviewed, approved, rejected, archived) (FR-9)
- Status is filterable in the sidebar (FR-9)
- New properties default to "new" status (FR-9)
- Price changes are detected and recorded in price_history table (FR-10)
- Changed prices are flagged in property detail view (FR-10)
- Price history includes previous price, change date, and percentage change (FR-10)
- Legal review count remains accurate with new status workflows
