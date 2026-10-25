---
type: epic
---

# Epic: Analytics with Real Data

## Goal
Replace demo analytics data with real aggregations from `community_content` in PostgreSQL, add server-side filtering for large datasets, and provide clear loading, empty, and error states for all analytics widgets.

## Outcome
When `community_content` has records, the Analytics and Trends workspaces display real statistics computed from actual data — question counts, source diversity, topic extraction, sentiment distribution, trending questions, neighborhood activity, concerns by intent, and AI-generated insights. When `community_content` is empty, the dashboard falls back to clearly labeled demo data as it does today. Filtering by date range, location, source, intent, and sentiment works efficiently via SQL queries rather than in-memory Python filtering for large datasets. Each widget gracefully handles loading, empty results, and errors with appropriate messaging.

## References
- PRD: `../../prd-dashboard-feature-completion.md` (FR-1, FR-2, FR-3)
- `analytics_data.py` — current AnalyticsData abstraction and demo data provider
- `streamlit_app.py:606-667` — render_analytics and render_trends
- `ROADMAP_FUTURO.md` Section 2 (Datos y backend, Analytics)

## Done When
- AnalyticsData computes metrics from PostgreSQL when community_content has data
- Demo data is used only when community_content is empty, with clear labeling
- Filter changes apply to SQL queries, not just in-memory filtering
- All analytics widgets display proper loading, empty, and error states
- Loading states visible during data fetch
- Empty states guide users to import data
- Error handling for PostgreSQL connection failures
- Retry mechanism for failed loads
