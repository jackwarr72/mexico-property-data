---
title: Mexico Property Data Dashboard Feature Completion
created: 2026-10-07
updated: 2026-10-07
---

# PRD: Mexico Property Data Dashboard Feature Completion

## 0. Document Purpose

This PRD is for the development team and product stakeholders working on the Mexico Property Data dashboard. It defines the remaining features needed to complete the dashboard, building on the existing implementation in `streamlit_app.py`. The dashboard already has a working foundation but requires completion across five epic areas: analytics with real data, export improvements, mobile responsiveness, data quality features, and operational enhancements. This document references the existing `ROADMAP_FUTURO.md` and the current codebase.

## 1. Vision

The Mexico Property Data Dashboard is a bilingual (Spanish) Streamlit application that serves as the central operations hub for property professionals in Mexico. It combines property listings from compliant sources with community insights, market intelligence, and operational tools. The completed dashboard will provide a seamless experience across desktop, tablet, and mobile, with robust data loading states, improved analytics backed by real community data, comprehensive export capabilities, and enhanced operational efficiency tools.

The dashboard matters because real estate professionals need timely, accurate, and actionable data to make informed decisions in the Mexican property market. By consolidating property listings, community sentiment, market trends, and operational tracking into a single interface, the dashboard enables users to identify opportunities, monitor market conditions, track team performance, and export insights for client presentations.

## 2. Target User

### 2.1 Jobs To Be Done

- **Property Scouts**: Find high-priority properties matching specific criteria, track follow-ups, and maintain contact databases for brokers and partners.
- **Market Analysts**: Analyze community sentiment, track trends over time, and compare market segments by location, source, and property type.
- **Operations Managers**: Monitor daily KPIs, track team performance against targets, and manage keyword alerts for new listings.
- **Business Development**: Export reports for client presentations, share insights with stakeholders, and generate data-backed proposals.

### 2.3 Key User Journeys

- **UJ-1. Property Scout reviews and prioritizes listings.** The scout filters properties by state, type, source, and price band. The dashboard displays an executive summary with total counts, legal review items, median price, and a priority-ordered top-five list. The scout selects a property to view details, adds a follow-up note, and saves contact information for the broker.
- **UJ-2. Analyst explores community insights.** The analyst switches to the Analytics workspace, applies date range and location filters, reviews trending questions, examines neighborhood activity on a map, and drills into concerns by intent category.
- **UJ-3. Manager tracks operational KPIs.** The manager records daily property additions and appointments in the KPIs tab, reviews the 30-day summary against targets, and checks the monitoring alerts for new listings matching tracked keywords.
- **UJ-4. Business developer exports reports.** The developer selects export scope (current view, full report, discussions, trends, raw data), chooses format (CSV, Excel, PDF, JSON, PNG, SVG), and downloads the report with active filters applied.
- **UJ-5. Mobile user accesses dashboard on tablet.** The user opens the dashboard on a tablet, navigates tabs with touch-friendly targets, and exports a filtered view while away from the office.

## 3. Glossary

- **Workspace** — A top-level navigation section in the sidebar: "Panel principal" (main operations), "Análisis y hallazgos" (analytics), and "Tendencias" (trends). Currently implemented as a radio button selector since Streamlit does not expose URL routes.
- **Property** — A normalized real estate listing with fields defined in `property_schema.json`, stored in the `properties` table in PostgreSQL.
- **Community Content** — User-generated discussion content (forum posts, Q&A, comments) from compliant sources, stored in `community_content` table with normalized fields per `community_content_schema.json`.
- **AnalyticsData** — The abstraction layer (`analytics_data.py`) that provides analytics and trends data, using demo data when `community_content` is empty and real data from PostgreSQL when populated.
- **Export Scope** — The dataset to export: "Vista actual" (current view), "Informe completo" (full report), "Discusiones" (discussions), "Tendencias" (trends), or "Datos sin procesar" (raw data).
- **Price Band** — A predefined price range grouping for property filtering (e.g., "MXN 2M-5M", "MXN 5M-10M").
- **KPI** — Key Performance Indicator: daily metrics for properties added and appointments, with targets of 20+ properties per day and 10+ appointments per week.
- **Monitoring Alert** — A match found when scanning property titles and descriptions for tracked keywords (e.g., "Venta urgente", "Reducción de precio").
- **Source Registry** — The list of data sources with compliance metadata, stored in `source_registry`. Sources are disabled by default until explicitly authorized.
- **Legal Review Count** — Properties requiring legal status verification, identified by legal_status being empty, manual_review, pending, or unknown.

## 4. Features

### 4.1 Analytics with Real Data

Replace demo analytics data with real aggregations from `community_content` while maintaining graceful degradation.

**Functional Requirements:**

#### FR-1: Load real analytics data from PostgreSQL
When `community_content` has records, `AnalyticsData` computes quick stats (questions, sources, topics, sentiment) and trends from actual dates and data instead of using demo data. Realizes UJ-2.

**Consequences (testable):**
- AnalyticsData is_demo returns False when community_content has records.
- Quick stats reflect actual counts from community_content rows.
- Trending questions reflect actual question frequency from the last 7 days.

#### FR-2: Server-side filtering for analytics
Filters for date range, location, source, intent, and sentiment are applied at the SQL query level for large datasets, not just in-memory Python filtering. Realizes UJ-2.

**Consequences (testable):**
- Filtering by 7/30/90-day period reduces query result set to matching dates.
- Location and source filters return only matching records.
- Intent and sentiment filters correctly map display labels to internal values.

**Out of Scope:**
- Full-text search on question content (deferred).

#### FR-3: Analytics loading states and error handling
Each analytics widget displays appropriate loading, empty, and error states with retry capability. Realizes UJ-2.

**Consequences (testable):**
- Empty state shown when no discussions match filters.
- Error message displayed when PostgreSQL query fails.
- Retry button reloads analytics data.

### 4.2 Enhanced Export Capabilities

Enhance export features with better PDF formatting, GeoSJON export, table exports, and background jobs.

**Functional Requirements:**

#### FR-4: Improve PDF export with visual identity
PDF exports include proper visual identity, pagination, fonts, and vector graphics for charts. Realizes UJ-4.

**Consequences (testable):**
- PDF includes active filters in header.
- Sentiment chart rendered as vector SVG in PDF.
- Multi-page PDF correctly paginates long content.

#### FR-5: Export filtered tables from widgets
Each analytics widget can export its visible filtered table as CSV with active filters applied. Realizes UJ-4.

**Consequences (testable):**
- Clicking export on a discussion results table downloads CSV with visible rows.
- Export filename includes timestamp and filter description.

#### FR-6: Add GeoJSON export format
Geographic data (neighborhood rankings, location activity) can be exported as GeoJSON for use in mapping applications. Realizes UJ-4.

**Consequences (testable):**
- GeoJSON contains valid FeatureCollection with neighborhood polygons.
- Export filename uses `.geojson` extension.

**Out of Scope:**
- Real polygon geometry from GIS sources (deferred).

### 4.3 Mobile Responsiveness

Ensure the dashboard is fully usable on tablets and mobile devices with touch-friendly controls.

**Functional Requirements:**

#### FR-7: Mobile-friendly navigation and controls
All interactive elements (tabs, selects, buttons, inputs) meet touch target minimums (44px) and adapt layout for narrow screens. Realizes UJ-5.

**Consequences (testable):**
- All buttons and inputs have min-height: 44px on mobile.
- Tab navigation is vertically stacked on narrow screens.
- Selectbox dropdowns are usable on touch devices.

#### FR-8: Mobile export workflow
Export controls and download buttons are optimized for mobile interactions. Realizes UJ-5.

**Consequences (testable):**
- Export control container does not overflow on 375px width.
- Download buttons are full-width on mobile.

### 4.4 Data Quality and Review System

Implement data quality validation, review states, and price history tracking.

**Functional Requirements:**

#### FR-9: Property review status system
Properties have a review status (new, reviewed, approved, rejected, archived) that is tracked and filterable. Realizes UJ-1.

**Consequences (testable):**
- New `status` column on properties table.
- Filter available for review status in sidebar.
- Properties default to "new" status.

#### FR-10: Price change history tracking
Detects and records property price changes, including previous prices, change dates, and percentage change. Realizes UJ-1.

**Consequences (testable):**
- `price_history` table stores price changes with timestamps.
- Changed prices are flagged in the property detail view.

### 4.5 Operational Enhancements

Add data refresh controls, global filters, background export jobs, and role-based permissions.

**Functional Requirements:**

#### FR-11: Manual and automatic data refresh
Users can manually trigger a data refresh, and the dashboard can auto-refresh analytics data on a configurable interval. Realizes UJ-2.

**Consequences (testable):**
- Refresh button in sidebar reloads all data.
- Analytics auto-refresh every 60 seconds when enabled.

#### FR-12: Global filter sharing
Filters applied in the sidebar are shared across all widgets in the current workspace. Realizes UJ-2.

**Consequences (testable):**
- Changing state filter updates property count, intelligence charts, and priority list simultaneously.
- Filters persist in session state across widget renders.

#### FR-13: Background export jobs
Large export jobs run asynchronously with progress tracking, status display, and automatic file cleanup. Realizes UJ-4.

**Consequences (testable):**
- Export history table shows job status (pending, completed, failed).
- Long-running exports display progress bar.
- Files older than 7 days are automatically deleted.

## 5. Non-Goals (Explicit)

- Building a separate admin panel for source management (existing source_registry is sufficient).
- Implementing real-time WebSocket updates (auto-refresh via polling is acceptable for v1).
- Adding user authentication and role-based permissions (planned for Phase 4 per ROADMAP_FUTURO.md).
- Migrating from Streamlit to a separate frontend framework.
- Integrating paid third-party APIs for sentiment analysis or geocoding.

## 6. MVP Scope

### 6.1 In Scope
- Replace demo analytics data with real aggregations from community_content.
- Add loading, empty, and error states for all analytics widgets.
- Improve PDF export with better formatting and vector charts.
- Mobile-friendly touch targets and responsive layout.
- Property review status system with filtering.
- Manual data refresh button.

### 6.2 Out of Scope for MVP
- Server-side SQL filtering for analytics (deferred to v2 — in-memory filtering works for current dataset sizes). [NOTE FOR PM: Reconsider if community_content approaches 100K rows.]
- GeoSJON export format (deferred to v2).
- Background export jobs with progress tracking (deferred to v2).
- Price change history tracking (deferred to v2).
- Auto-refresh for analytics data (deferred to v2 — manual refresh sufficient for MVP).
- Role-based access control (deferred, planned for Phase 4).

## 7. Success Metrics

**Primary**
- **SM-1**: Dashboard loads successfully on mobile devices within 3 seconds. Validates FR-7, FR-8.
- **SM-2**: Analytics views display real data from community_content when records exist. Validates FR-1.
- **SM-3**: PDF exports achieve 100% completion rate with proper formatting. Validates FR-4.

**Secondary**
- **SM-4**: User successfully exports at least one report within first session. Validates FR-5.
- **SM-5**: Data refresh completes within 5 seconds for datasets under 10K properties. Validates FR-11.
- **SM-6**: All interactive elements pass accessibility touch-target audit. Validates FR-7.

**Counter-metrics (do not optimize)**
- **SM-C1**: Do not optimize for total number of features — prioritize polish and reliability of existing workflows.

## 8. Open Questions

1. What is the expected growth rate of community_content data? (Affects decision on server-side filtering.)
2. Which PDF visual identity assets will be used? (Colors, fonts, logo.)
3. Should mobile users have a condensed feature set or full functionality?

## 9. Assumptions Index

- Users will have PostgreSQL accessible via Docker locally.
- Python 3 virtual environment is already configured.
- The Streamlit app will remain the delivery mechanism (not migrated to a web framework).
- Demo data will remain for development when community_content is empty.
- Users understand this is not an investment advice tool.
