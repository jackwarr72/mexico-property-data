"""Typed analytics models and replaceable PostgreSQL/demo data provider."""

from __future__ import annotations

import json
from dataclasses import dataclass, field
from datetime import date, timedelta
from typing import Callable, Literal

import pandas as pd

TrendDirection = Literal["up", "down", "stable", "new"]
InsightType = Literal["trend", "sentiment_shift", "content_gap"]


@dataclass(frozen=True)
class Metric:
    value: int | float
    change: float | None = None
    change_label: str = ""


@dataclass(frozen=True)
class SentimentMetric:
    value: float
    label: str
    change: float | None = None


@dataclass(frozen=True)
class QuickStats:
    questions: Metric
    sources: Metric
    topics: Metric
    sentiment: SentimentMetric


@dataclass(frozen=True)
class TrendingQuestion:
    id: str
    question: str
    mentions: int
    trend: TrendDirection


@dataclass(frozen=True)
class SentimentPoint:
    date: str
    positive: float
    neutral: float
    negative: float


@dataclass(frozen=True)
class Concern:
    intent: Literal["buying", "selling", "renting"]
    topic: str
    count: int


@dataclass(frozen=True)
class AIInsight:
    id: str
    type: InsightType
    title: str
    description: str
    opportunity: str = ""
    metric: float | None = None
    action: str = ""
    period: str = "This week"
    source_reference: str = "Demo data; replace with a verified analytics reference."


@dataclass(frozen=True)
class DiscussionResult:
    id: str
    source: str
    location: str
    published_at: str
    intent: str
    question: str
    summary: str
    key_points: list[str]
    sentiment: str
    engagement: int
    source_url: str = ""


@dataclass(frozen=True)
class Trend:
    id: str
    topic: str
    mentions: int
    growth_percent: float
    previous_period_mentions: int
    explanation: str
    opportunity: str
    direction: TrendDirection
    source_reference: str = "Demo data; replace with a verified source."


@dataclass(frozen=True)
class NeighborhoodMetric:
    neighborhood: str
    mentions: int
    trend_percent: float
    sentiment: str
    latitude: float
    longitude: float


@dataclass
class AnalyticsData:
    quick_stats: QuickStats
    trending_questions: list[TrendingQuestion] = field(default_factory=list)
    sentiment: list[SentimentPoint] = field(default_factory=list)
    concerns: list[Concern] = field(default_factory=list)
    insights: list[AIInsight] = field(default_factory=list)
    discussions: list[DiscussionResult] = field(default_factory=list)
    trends: list[Trend] = field(default_factory=list)
    topic_evolution: pd.DataFrame = field(default_factory=pd.DataFrame)
    neighborhoods: list[NeighborhoodMetric] = field(default_factory=list)
    is_demo: bool = True


ConnectionFactory = Callable[[], object]


class AnalyticsDataLoadError(RuntimeError):
    """Raised when analytics cannot be loaded from the configured provider."""


def demo_analytics_data() -> AnalyticsData:
    today = date.today()
    sentiment = []
    for offset in range(29, -1, -1):
        current = today - timedelta(days=offset)
        sentiment.append(SentimentPoint(current.isoformat(), 46 + (29 - offset) % 6, 34 - (29 - offset) % 3, 20 - (29 - offset) % 3))

    dates = [today - timedelta(days=89 - index * 3) for index in range(30)]
    topic_evolution = pd.DataFrame(
        {
            "date": dates * 4,
            "topic": (["Infonavit"] * 30) + (["Metepec"] * 30) + (["FOVISSSTE"] * 30) + (["Toluca Centro"] * 30),
            "mentions": (
                [55 + index for index in range(30)]
                + [35 + index * 2 for index in range(30)]
                + [22 + index * 3 for index in range(30)]
                + [80 - index for index in range(30)]
            ),
        }
    )

    return AnalyticsData(
        quick_stats=QuickStats(Metric(2847, 8, "+8% (7d)"), Metric(73, 3, "+3 new"), Metric(156, 7, "+7 new"), SentimentMetric(12, "positive", 12)),
        trending_questions=[
            TrendingQuestion("q1", "¿Cuánto cuesta escriturar en Metepec?", 89, "up"),
            TrendingQuestion("q2", "¿Conviene comprar en Residencial Colón?", 67, "up"),
            TrendingQuestion("q3", "¿Cómo funciona el crédito FOVISSSTE?", 54, "stable"),
            TrendingQuestion("q4", "Opiniones sobre Villas Fontana", 48, "new"),
            TrendingQuestion("q5", "¿Es seguro invertir en Toluca?", 45, "down"),
        ],
        sentiment=sentiment,
        concerns=[
            Concern("buying", "Financiamiento", 234), Concern("buying", "Ubicación", 198), Concern("buying", "Precio", 167),
            Concern("selling", "Momento de venta", 89), Concern("selling", "Precio de venta", 76), Concern("selling", "Legal", 54),
            Concern("renting", "Contratos", 43), Concern("renting", "Depósitos", 38), Concern("renting", "Mantenimiento", 29),
        ],
        insights=[
            AIInsight("i1", "trend", 'Aumento de preguntas sobre "crédito verde"', "Los préstamos para mejoras ambientales aparecen con mayor frecuencia en las discusiones.", "Crear contenido explicativo.", action="Más información →"),
            AIInsight("i2", "sentiment_shift", "El sentimiento positivo sobre los precios de Metepec bajó 18%", "Las discusiones recientes muestran un cambio medible en el sentimiento sobre los precios de Metepec.", metric=-18, action="Ver detalles →", period="Últimos 7 días vs 7 días anteriores"),
            AIInsight("i3", "content_gap", "34 preguntas sin respuesta sobre la cofinanciación de Infonavit", "Un grupo de preguntas sin respuesta indica una posible brecha de contenido.", "", metric=34, action="Generar contenido →"),
        ],
        discussions=[
            DiscussionResult("d1", "Reddit", "Metepec", "hace 3 días", "BUYING_INTENT", "¿Vale la pena comprar en Metepec con más de 3M?", "Una persona que compra por primera vez pregunta si los precios de Metepec están justificados y expresa preocupación por la plusvalía futura.", ["Preocupación por el precio: 3.5M por 120m2 parece alto", "Interés en: zona de La Asunción", "Financiamiento: cofinanciación de Infonavit"], "Neutral-Negative", 3),
            DiscussionResult("d2", "Comentarios de noticias públicas", "Toluca Centro", "hace 5 días", "SELLING_INTENT", "¿Cómo está el mercado en Toluca Centro?", "Discusión sobre el momento adecuado para vender cerca de nuevos proyectos de infraestructura.", ["La principal preocupación es el momento de venta", "Interés en proyectos de desarrollo"], "Neutral", 2),
        ],
        trends=[
            Trend("t1", "Ampliación de crédito FOVISSSTE", 47, 180, 17, "Se detectó un nuevo grupo de discusiones relacionadas con el programa.", "Crear videos explicativos y preguntas frecuentes.", "up"),
            Trend("t2", "Precios en Metepec", 66, 24, 53, "El volumen de menciones está aumentando en el periodo seleccionado.", "Publicar una comparación de precios.", "up"),
            Trend("t3", "Toluca Centro", 31, -12, 35, "El volumen de menciones es menor que en el periodo anterior.", "Revisar contenido específico de la colonia.", "down"),
        ],
        topic_evolution=topic_evolution,
        neighborhoods=[
            NeighborhoodMetric("Metepec Centro", 845, 18, "Positive", 19.2500, -99.6000),
            NeighborhoodMetric("La Asunción", 673, 12, "Neutral", 19.2530, -99.5900),
            NeighborhoodMetric("Residencial Colón", 589, -4, "Neutral", 19.2750, -99.6550),
            NeighborhoodMetric("Toluca Centro", 512, -9, "Neutral-Negative", 19.2826, -99.6557),
            NeighborhoodMetric("San Mateo Atenco", 487, 7, "Positive", 19.2670, -99.5300),
        ],
        is_demo=True,
    )


def empty_analytics_data() -> AnalyticsData:
    return AnalyticsData(
        quick_stats=QuickStats(
            questions=Metric(0),
            sources=Metric(0),
            topics=Metric(0),
            sentiment=SentimentMetric(0, "neutral"),
        ),
        is_demo=False,
    )


def _parse_json_list(value: object) -> list[str]:
    if not value:
        return []
    if isinstance(value, list):
        return [str(item) for item in value]
    try:
        parsed = json.loads(str(value))
        return [str(item) for item in parsed] if isinstance(parsed, list) else []
    except json.JSONDecodeError:
        return []


def load_analytics_data(connection_factory: ConnectionFactory) -> AnalyticsData:
    query = """
        SELECT content_id, source_name, municipality, state, title, content, source_url,
               published_at, sentiment, extracted_keywords, engagement_metrics
        FROM community_content
        ORDER BY published_at DESC NULLS LAST
        LIMIT 1000;
    """
    try:
        with connection_factory() as connection:
            frame = pd.read_sql_query(query, connection)
    except Exception as error:
        raise AnalyticsDataLoadError(
            "Unable to load analytics from community_content"
        ) from error
    if frame.empty:
        return empty_analytics_data()
    return build_analytics_from_content(frame)


def build_analytics_from_content(frame: pd.DataFrame) -> AnalyticsData:
    source_count = int(frame["source_name"].nunique())
    location_count = int(frame["municipality"].replace("", pd.NA).dropna().nunique())
    question_count = len(frame)
    sentiment_counts = frame["sentiment"].fillna("Neutral").str.lower().value_counts()
    positive = int(sentiment_counts.get("positive", 0))
    negative = int(sentiment_counts.get("negative", 0))
    neutral = max(0, question_count - positive - negative)
    sentiment_value = round(((positive - negative) / question_count) * 100, 1) if question_count else 0
    question_rows = frame.assign(question=frame["title"].fillna("").replace("", "Untitled discussion")).groupby("question").size().reset_index(name="mentions").sort_values("mentions", ascending=False).head(5)
    questions = [TrendingQuestion(f"q-{index}", row.question, int(row.mentions), "stable") for index, row in enumerate(question_rows.itertuples(), 1)]
    discussions = [
        DiscussionResult(
            str(row.content_id), str(row.source_name or "Unknown"), str(row.municipality or row.state or "Mexico"),
            str(row.published_at or "Unknown"), "DISCUSSION", str(row.title or "Untitled discussion"),
            str(row.content or "No summary available."), [], str(row.sentiment or "Neutral"), 0, str(row.source_url or "")
        )
        for row in frame.head(20).itertuples()
    ]
    locations = []
    for index, row in frame.groupby("municipality", dropna=True).size().sort_values(ascending=False).head(10).items():
        locations.append(NeighborhoodMetric(str(index), int(row), 0, "Neutral", 19.2826, -99.6557))
    return AnalyticsData(
        quick_stats=QuickStats(Metric(question_count), Metric(source_count), Metric(location_count), SentimentMetric(sentiment_value, "positive" if sentiment_value > 0 else "neutral")),
        trending_questions=questions,
        sentiment=[SentimentPoint(date.today().isoformat(), positive / max(question_count, 1) * 100, neutral / max(question_count, 1) * 100, negative / max(question_count, 1) * 100)],
        discussions=discussions,
        neighborhoods=locations,
        is_demo=False,
    )
