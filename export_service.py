"""Reusable analytics export service shared by Streamlit and future APIs."""

from __future__ import annotations

import io
import json
import re
from dataclasses import asdict
from datetime import datetime
from pathlib import Path
from typing import Iterable

import matplotlib.pyplot as plt
import pandas as pd
from reportlab.lib import colors
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.units import inch
from reportlab.platypus import Image, PageBreak, Paragraph, SimpleDocTemplate, Spacer, Table, TableStyle

from analytics_data import AnalyticsData

EXPORT_DIR = Path("data/exports")


def slugify(value: str) -> str:
    return re.sub(r"[^a-z0-9]+", "-", value.lower()).strip("-") or "all"


def filename(prefix: str, filters: dict[str, str] | None, extension: str) -> str:
    filters = filters or {}
    location = slugify(filters.get("location", "all-locations"))
    period = slugify(filters.get("date_range", "current-view"))
    return f"{slugify(prefix)}-{location}-{period}.{extension}"


def questions_frame(analytics: AnalyticsData) -> pd.DataFrame:
    return pd.DataFrame([
        {"id": item.id, "question": item.question, "mentions": item.mentions, "trend": item.trend,
         "source": "", "location": "", "intent": "", "sentiment": "", "first_seen": "", "last_seen": ""}
        for item in analytics.trending_questions
    ])


def sources_frame(analytics: AnalyticsData) -> pd.DataFrame:
    rows = {}
    for discussion in analytics.discussions:
        source = discussion.source or "Unknown"
        rows.setdefault(source, {"source": source, "discussion_count": 0, "questions": 0, "percentage": 0.0, "trend": "stable"})
        rows[source]["discussion_count"] += 1
        rows[source]["questions"] += 1
    frame = pd.DataFrame(rows.values())
    if not frame.empty:
        frame["percentage"] = frame["discussion_count"] / frame["discussion_count"].sum() * 100
    return frame


def topics_frame(analytics: AnalyticsData) -> pd.DataFrame:
    return pd.DataFrame([
        {"topic": item.topic, "mentions": item.mentions, "growth_percent": item.growth_percent,
         "sentiment": "", "trend": item.direction}
        for item in analytics.trends
    ])


def sentiment_frame(analytics: AnalyticsData) -> pd.DataFrame:
    frame = pd.DataFrame([asdict(item) for item in analytics.sentiment])
    if frame.empty:
        return pd.DataFrame(columns=["date", "positive", "neutral", "negative", "total"])
    frame["total"] = frame[["positive", "neutral", "negative"]].sum(axis=1)
    return frame


def concerns_frame(analytics: AnalyticsData) -> pd.DataFrame:
    frame = pd.DataFrame([asdict(item) for item in analytics.concerns]).rename(columns={"topic": "concern"})
    if not frame.empty:
        frame["percentage"] = frame["count"] / frame.groupby("intent")["count"].transform("sum") * 100
    return frame


def discussions_frame(analytics: AnalyticsData, discussions: Iterable | None = None) -> pd.DataFrame:
    records = discussions if discussions is not None else analytics.discussions
    return pd.DataFrame([
        {"id": item.id, "source": item.source, "location": item.location, "published_at": item.published_at,
         "intent": item.intent, "question": item.question, "summary": item.summary,
         "key_points": " | ".join(item.key_points), "sentiment": item.sentiment,
         "engagement": item.engagement, "url": item.source_url}
        for item in records
    ])


def trends_frame(analytics: AnalyticsData) -> pd.DataFrame:
    return pd.DataFrame([
        {"topic": item.topic, "mentions": item.mentions, "previous_mentions": item.previous_period_mentions,
         "growth_percent": item.growth_percent, "trend_direction": item.direction,
         "explanation": item.explanation, "opportunity": item.opportunity}
        for item in analytics.trends
    ])


def neighborhoods_frame(analytics: AnalyticsData) -> pd.DataFrame:
    return pd.DataFrame([
        {"neighborhood": item.neighborhood, "mentions": item.mentions, "growth_percent": item.trend_percent,
         "sentiment": item.sentiment, "discussion_count": item.mentions}
        for item in analytics.neighborhoods
    ])


def insights_frame(analytics: AnalyticsData) -> pd.DataFrame:
    return pd.DataFrame([asdict(item) for item in analytics.insights])


def filtered_analytics_frames(analytics: AnalyticsData, discussions: Iterable | None = None) -> dict[str, pd.DataFrame]:
    return {
        "Trending Questions": questions_frame(analytics),
        "Sources": sources_frame(analytics),
        "Topics": topics_frame(analytics),
        "Sentiment": sentiment_frame(analytics),
        "Concerns": concerns_frame(analytics),
        "Discussions": discussions_frame(analytics, discussions),
        "Trends": trends_frame(analytics),
        "Neighborhoods": neighborhoods_frame(analytics),
    }


def summary_frame(analytics: AnalyticsData, filters: dict[str, str]) -> pd.DataFrame:
    metric = analytics.quick_stats
    rows = [("Export date", datetime.now().isoformat(timespec="seconds")),
            ("Date range", filters.get("date_range", "Current view")),
            ("Applied filters", json.dumps(filters, ensure_ascii=False)),
            ("Questions", metric.questions.value), ("Sources", metric.sources.value),
            ("Topics", metric.topics.value), ("Sentiment", f"{metric.sentiment.value:+.1f}% {metric.sentiment.label}")]
    return pd.DataFrame(rows, columns=["metric", "value"])


def export_csv(frame: pd.DataFrame, filters: dict[str, str], prefix: str = "analytics") -> tuple[str, bytes]:
    buffer = io.StringIO()
    frame.to_csv(buffer, index=False)
    return filename(prefix, filters, "csv"), buffer.getvalue().encode("utf-8-sig")


def export_json(frames: dict[str, pd.DataFrame], filters: dict[str, str], prefix: str = "analytics") -> tuple[str, bytes]:
    payload = {name: frame.where(pd.notna(frame), None).to_dict(orient="records") for name, frame in frames.items()}
    content = json.dumps({"filters": filters, "data": payload}, ensure_ascii=False, default=str, indent=2)
    return filename(prefix, filters, "json"), content.encode("utf-8")


def _format_sheet(sheet):
    sheet.freeze_panes = "A2"
    sheet.auto_filter.ref = sheet.dimensions
    for column_cells in sheet.columns:
        length = min(max(len(str(cell.value or "")) for cell in column_cells) + 2, 48)
        sheet.column_dimensions[column_cells[0].column_letter].width = length


def export_xlsx(analytics: AnalyticsData, filters: dict[str, str], discussions: Iterable | None = None) -> tuple[str, bytes]:
    output = io.BytesIO()
    with pd.ExcelWriter(output, engine="openpyxl") as writer:
        summary_frame(analytics, filters).to_excel(writer, sheet_name="Executive Summary", index=False)
        for sheet_name, frame in filtered_analytics_frames(analytics, discussions).items():
            frame.to_excel(writer, sheet_name=sheet_name[:31], index=False)
        discussions_frame(analytics, discussions).to_excel(writer, sheet_name="Raw Data", index=False)
        for sheet in writer.book.worksheets:
            _format_sheet(sheet)
    return filename("analytics-report", filters, "xlsx"), output.getvalue()


def _chart_bytes(analytics: AnalyticsData, fmt: str = "png") -> bytes:
    frame = sentiment_frame(analytics)
    figure, axis = plt.subplots(figsize=(10, 4.5), dpi=180)
    for column, color in (("positive", "#2f855a"), ("neutral", "#718096"), ("negative", "#c53030")):
        if not frame.empty:
            axis.plot(frame["date"], frame[column], label=column.title(), color=color)
    axis.set_title("Sentiment Over Time")
    axis.set_ylabel("Percentage")
    axis.legend()
    figure.autofmt_xdate()
    buffer = io.BytesIO()
    figure.tight_layout()
    figure.savefig(buffer, format=fmt, bbox_inches="tight")
    plt.close(figure)
    return buffer.getvalue()


def export_chart(analytics: AnalyticsData, filters: dict[str, str], fmt: str = "png") -> tuple[str, bytes, str]:
    return filename("sentiment", filters, fmt), _chart_bytes(analytics, fmt), f"image/{fmt}"


def _table_from_frame(frame: pd.DataFrame):
    if frame.empty:
        return Paragraph("No data available for this section.", getSampleStyleSheet()["Normal"])
    values = [list(frame.columns)] + [[str(value)[:240] for value in row] for row in frame.head(30).itertuples(index=False, name=None)]
    table = Table(values, repeatRows=1)
    table.setStyle(TableStyle([["BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#e2e8f0")], ["GRID", (0, 0), (-1, -1), 0.25, colors.grey], ["FONTSIZE", (0, 0), (-1, -1), 7], ["VALIGN", (0, 0), (-1, -1), "TOP"]]))
    return table


def export_pdf(analytics: AnalyticsData, filters: dict[str, str], discussions: Iterable | None = None) -> tuple[str, bytes]:
    output = io.BytesIO()
    document = SimpleDocTemplate(output, pagesize=letter, rightMargin=0.55 * inch, leftMargin=0.55 * inch, topMargin=0.5 * inch, bottomMargin=0.5 * inch)
    styles = getSampleStyleSheet()
    story = [Paragraph("Real Estate Intelligence Report", styles["Title"]), Paragraph("Toluca / Metepec Market Intelligence", styles["Heading2"]), Paragraph(f"Generated: {datetime.now():%Y-%m-%d %H:%M} | Filters: {json.dumps(filters, ensure_ascii=False)}", styles["Normal"]), Spacer(1, 12)]
    story += [Paragraph("Executive Summary", styles["Heading1"]), _table_from_frame(summary_frame(analytics, filters)), Spacer(1, 10), Paragraph("Trending Questions", styles["Heading1"]), _table_from_frame(questions_frame(analytics)[["question", "mentions", "trend"]]), PageBreak(), Paragraph("Sentiment Analysis", styles["Heading1"]), Image(io.BytesIO(_chart_bytes(analytics)), width=7.2 * inch, height=3.2 * inch), Paragraph("Location Activity", styles["Heading1"]), _table_from_frame(neighborhoods_frame(analytics)), Paragraph("Top Concerns", styles["Heading1"]), _table_from_frame(concerns_frame(analytics)), Paragraph("Emerging Trends", styles["Heading1"]), _table_from_frame(trends_frame(analytics))]
    story.append(Paragraph("AI-GENERATED INSIGHTS", styles["Heading1"]))
    for insight in analytics.insights:
        story.append(Paragraph(f"<b>{insight.title}</b><br/>DATA: {insight.description}<br/>INTERPRETATION: {insight.source_reference}<br/>OPPORTUNITY: {insight.opportunity or 'None specified'}", styles["BodyText"]))
        story.append(Spacer(1, 6))
    story += [Paragraph("Discussion Examples", styles["Heading1"]), _table_from_frame(discussions_frame(analytics, discussions)[["source", "location", "published_at", "intent", "question", "sentiment"]])]
    document.build(story)
    return filename("real-estate-intelligence", filters, "pdf"), output.getvalue()


def write_export(filename_value: str, content: bytes) -> Path:
    EXPORT_DIR.mkdir(parents=True, exist_ok=True)
    path = EXPORT_DIR / filename_value
    path.write_bytes(content)
    return path
