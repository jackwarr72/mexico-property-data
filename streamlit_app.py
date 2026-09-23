import os
import json
from datetime import date
from urllib.parse import quote_plus

import pandas as pd
import psycopg2
import streamlit as st
from dotenv import load_dotenv

from analytics_data import AnalyticsData, load_analytics_data
from export_service import (
    discussions_frame,
    export_chart,
    export_csv,
    export_json,
    export_pdf,
    export_xlsx,
    filtered_analytics_frames,
    write_export,
)
from market_dashboard import validate_filters

load_dotenv()

DB_CONFIG = {
    "host": os.getenv("POSTGRES_HOST", "localhost"),
    "port": int(os.getenv("POSTGRES_PORT", "5432")),
    "database": os.getenv("POSTGRES_DB", "property_data"),
    "user": os.getenv("POSTGRES_USER", "postgres"),
    "password": os.getenv("POSTGRES_PASSWORD", "postgres"),
}

PRICE_BANDS = {
    "Todos los precios": (None, None),
    "Menos de MXN 2M": (0, 2_000_000),
    "MXN 2M-5M": (2_000_000, 5_000_000),
    "MXN 5M-10M": (5_000_000, 10_000_000),
    "MXN 10M-20M": (10_000_000, 20_000_000),
    "MXN 20M o más": (20_000_000, None),
}
KPI_TARGETS = {"properties_added": 20, "appointments": 10}


def connect():
    return psycopg2.connect(**DB_CONFIG)


def execute(statement, params=(), fetch=False):
    with connect() as conn:
        with conn.cursor() as cur:
            cur.execute(statement, params)
            return cur.fetchall() if fetch else None


def ensure_operational_tables():
    statements = [
        """CREATE TABLE IF NOT EXISTS property_followups (
            id SERIAL PRIMARY KEY, property_id INTEGER NOT NULL REFERENCES properties(id) ON DELETE CASCADE,
            note TEXT NOT NULL, status VARCHAR(50) DEFAULT 'open', next_follow_up DATE,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )""",
        """CREATE TABLE IF NOT EXISTS alliance_contacts (
            id SERIAL PRIMARY KEY, name VARCHAR(255) NOT NULL, role VARCHAR(100) NOT NULL,
            company VARCHAR(255), phone VARCHAR(100), email VARCHAR(255), state VARCHAR(255),
            municipality VARCHAR(255), notes TEXT, created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )""",
        """CREATE TABLE IF NOT EXISTS kpi_entries (
            id SERIAL PRIMARY KEY, metric_date DATE NOT NULL UNIQUE,
            properties_added INTEGER NOT NULL DEFAULT 0 CHECK (properties_added >= 0),
            appointments INTEGER NOT NULL DEFAULT 0 CHECK (appointments >= 0), notes TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )""",
        """CREATE TABLE IF NOT EXISTS monitoring_alerts (
            id SERIAL PRIMARY KEY, keyword VARCHAR(255) NOT NULL,
            property_id INTEGER REFERENCES properties(id) ON DELETE SET NULL,
            source_name VARCHAR(255), status VARCHAR(50) DEFAULT 'new', notes TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )""",
        """CREATE TABLE IF NOT EXISTS export_history (
            id SERIAL PRIMARY KEY, created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            report_type VARCHAR(50) NOT NULL, format VARCHAR(20) NOT NULL,
            filename VARCHAR(255) NOT NULL, filters JSONB, status VARCHAR(30) DEFAULT 'completed'
        )""",
    ]
    with connect() as conn:
        with conn.cursor() as cur:
            for statement in statements:
                cur.execute(statement)


def get_options(column):
    if column not in {"state", "property_type", "source_name"}:
        raise ValueError("Unsupported option column")
    query = f"SELECT DISTINCT {column} FROM properties WHERE {column} IS NOT NULL ORDER BY {column};"
    return [row[0] for row in execute(query, fetch=True)]


def build_query_filters(state, property_type, source_name, min_price, max_price):
    clauses = []
    params = []
    for column, value in (("state", state), ("property_type", property_type), ("source_name", source_name)):
        if value:
            clauses.append(f"LOWER({column}) = LOWER(%s)")
            params.append(value)
    if min_price is not None:
        clauses.append("price >= %s")
        params.append(min_price)
    if max_price is not None:
        clauses.append("price < %s" if min_price is not None else "price <= %s")
        params.append(max_price)
    return ("WHERE " + " AND ".join(clauses)) if clauses else "", params


def load_properties(state, property_type, source_name, min_price, max_price):
    where_clause, params = build_query_filters(state, property_type, source_name, min_price, max_price)
    query = f"""
        SELECT id, listing_id, source_name, source_url, title, description, price, currency,
               property_type, bedrooms, bathrooms, parking_spaces, square_meters, lot_meters,
               state, municipality, colonia, address, latitude, longitude, listing_status,
               broker_name, broker_phone, legal_status,
               CASE WHEN price < 2000000 THEN '<2M' WHEN price < 5000000 THEN '2M-5M'
                    WHEN price < 10000000 THEN '5M-10M' WHEN price < 20000000 THEN '10M-20M'
                    ELSE '20M+' END AS price_band
        FROM properties {where_clause} ORDER BY price DESC NULLS LAST;
    """
    with connect() as conn:
        return pd.read_sql_query(query, conn, params=params)


def render_listing_detail(data):
    if data.empty:
        st.warning("Ninguna propiedad coincide con los filtros seleccionados.")
        return
    labels = {row.id: f"{row.title or 'Untitled'} | {row.state or ''} | MXN {row.price:,.0f}" for row in data.itertuples()}
    selected_id = st.selectbox("Selecciona una propiedad", list(labels), format_func=lambda value: labels[value])
    selected = data[data.id == selected_id].iloc[0]
    left, right = st.columns(2)
    with left:
        st.write(f"**{selected['title'] or 'Untitled listing'}**")
        st.write(f"{selected['address'] or selected['municipality'] or ''}, {selected['state'] or ''}")
        st.write(f"Precio: MXN {selected['price']:,.0f}" if pd.notna(selected["price"]) else "Precio: no disponible")
        st.write(f"Fuente: {selected['source_name'] or 'Desconocida'}")
        if selected["source_url"]:
            st.link_button("Abrir anuncio original", selected["source_url"])
    with right:
        st.write(f"Tipo de propiedad: {selected['property_type'] or 'Desconocido'}")
        st.write(f"Recámaras: {selected['bedrooms'] or '-'} | Baños: {selected['bathrooms'] or '-'}")
        st.write(f"Superficie: {selected['square_meters'] or '-'} m2 | Terreno: {selected['lot_meters'] or '-'} m2")
        st.write(f"Estatus legal: {selected['legal_status'] or 'Desconocido'}")
    st.write(selected["description"] or "No hay descripción disponible.")
    with st.form(f"followup_{selected_id}"):
        st.subheader("Nota de seguimiento")
        note = st.text_area("Nota")
        status = st.selectbox("Estatus", ["open", "contacted", "scheduled", "closed"], format_func=lambda value: {"open": "Abierto", "contacted": "Contactado", "scheduled": "Programado", "closed": "Cerrado"}[value])
        next_follow_up = st.date_input("Próximo seguimiento", value=None)
        if st.form_submit_button("Guardar nota"):
            if not note.strip():
                st.error("La nota de seguimiento es obligatoria.")
            else:
                execute("INSERT INTO property_followups (property_id, note, status, next_follow_up) VALUES (%s, %s, %s, %s)", (selected_id, note.strip(), status, next_follow_up))
                st.success("Seguimiento guardado.")
                st.rerun()
    notes = execute("SELECT note, status, next_follow_up, created_at FROM property_followups WHERE property_id = %s ORDER BY created_at DESC", (selected_id,), True)
    if notes:
        st.dataframe(pd.DataFrame(notes, columns=["note", "status", "next_follow_up", "created_at"]), use_container_width=True, hide_index=True)


def render_alliances():
    st.subheader("Alianzas estratégicas")
    with st.form("new_contact"):
        cols = st.columns(3)
        name = cols[0].text_input("Nombre")
        role = cols[1].selectbox("Rol", ["Broker", "Notario", "Valuador", "Abogado", "Financiamiento", "Otro"])
        company = cols[2].text_input("Empresa")
        phone = cols[0].text_input("Teléfono")
        email = cols[1].text_input("Correo electrónico")
        location = cols[2].text_input("Estado / municipio")
        notes = st.text_area("Notas")
        if st.form_submit_button("Agregar contacto"):
            if not name.strip():
                st.error("El nombre es obligatorio.")
            else:
                execute("INSERT INTO alliance_contacts (name, role, company, phone, email, state, notes) VALUES (%s, %s, %s, %s, %s, %s, %s)", (name.strip(), role, company.strip(), phone.strip(), email.strip(), location.strip(), notes.strip()))
                st.success("Contacto agregado.")
                st.rerun()
    rows = execute("SELECT name, role, company, phone, email, state, notes FROM alliance_contacts ORDER BY name", fetch=True)
    st.dataframe(pd.DataFrame(rows, columns=["name", "role", "company", "phone", "email", "location", "notes"]), use_container_width=True, hide_index=True)


def render_kpis():
    st.subheader("Indicadores operativos semanales")
    st.caption("Metas: 20 o más propiedades agregadas por día y 10 o más citas por semana.")
    with st.form("kpi_entry"):
        metric_date = st.date_input("Fecha", value=date.today())
        properties_added = st.number_input("Propiedades agregadas", min_value=0, step=1)
        appointments = st.number_input("Citas", min_value=0, step=1)
        notes = st.text_input("Notas")
        if st.form_submit_button("Guardar indicador diario"):
            execute("INSERT INTO kpi_entries (metric_date, properties_added, appointments, notes) VALUES (%s, %s, %s, %s) ON CONFLICT (metric_date) DO UPDATE SET properties_added = EXCLUDED.properties_added, appointments = EXCLUDED.appointments, notes = EXCLUDED.notes", (metric_date, properties_added, appointments, notes.strip()))
            st.success("Indicador guardado.")
            st.rerun()
    rows = execute("SELECT metric_date, properties_added, appointments, notes FROM kpi_entries WHERE metric_date >= CURRENT_DATE - INTERVAL '30 days' ORDER BY metric_date DESC", fetch=True)
    kpi_data = pd.DataFrame(rows, columns=["date", "properties_added", "appointments", "notes"])
    if not kpi_data.empty:
        cols = st.columns(3)
        cols[0].metric("Meta diaria de propiedades", f"{KPI_TARGETS['properties_added']}+")
        cols[1].metric("Citas registradas", int(kpi_data.appointments.sum()), f"Meta {KPI_TARGETS['appointments']}/semana")
        cols[2].metric("Promedio diario de propiedades", f"{kpi_data.properties_added.mean():.1f}", f"Meta {KPI_TARGETS['properties_added']}")
        st.dataframe(kpi_data, use_container_width=True, hide_index=True)
    else:
        st.info("Agrega el primer indicador diario para comenzar a comparar el desempeño contra las metas.")


def render_intelligence(data):
    st.subheader("Inteligencia de negocio")
    source_summary = data.groupby("source_name", dropna=False).agg(listings=("id", "size"), avg_price=("price", "mean")).reset_index().sort_values("listings", ascending=False)
    type_summary = data.groupby("property_type", dropna=False).agg(listings=("id", "size"), avg_price=("price", "mean")).reset_index().sort_values("listings", ascending=False)
    left, right = st.columns(2)
    with left:
        st.write("Fuentes de propiedades")
        st.dataframe(source_summary, use_container_width=True, hide_index=True)
        st.bar_chart(source_summary.set_index("source_name")["listings"])
    with right:
        st.write("Tipos de propiedad")
        st.dataframe(type_summary, use_container_width=True, hide_index=True)
        st.bar_chart(type_summary.set_index("property_type")["listings"])


def render_alerts():
    st.subheader("Alertas de monitoreo")
    keywords = st.text_input("Palabras clave", value="Venta urgente, Reducción de precio")
    keyword_list = [item.strip() for item in keywords.split(",") if item.strip()]
    if st.button("Escanear anuncios"):
        for keyword in keyword_list:
            matches = execute("SELECT id, source_name FROM properties WHERE LOWER(COALESCE(title, '') || ' ' || COALESCE(description, '')) LIKE LOWER(%s)", (f"%{keyword}%",), True)
            for property_id, source_name in matches:
                execute("INSERT INTO monitoring_alerts (keyword, property_id, source_name) SELECT %s, %s, %s WHERE NOT EXISTS (SELECT 1 FROM monitoring_alerts WHERE keyword = %s AND property_id = %s)", (keyword, property_id, source_name, keyword, property_id))
        st.success("Escaneo completado.")
        st.rerun()
    rows = execute("SELECT keyword, property_id, source_name, status, notes, created_at FROM monitoring_alerts ORDER BY created_at DESC", fetch=True)
    st.dataframe(pd.DataFrame(rows, columns=["keyword", "property_id", "source", "status", "notes", "created_at"]), use_container_width=True, hide_index=True)


def render_search():
    st.subheader("Búsqueda avanzada en Google")
    site = st.text_input("Dominio del sitio", placeholder="example.gob.mx")
    intitle = st.text_input("Frase del título", placeholder="registro de propiedades")
    inurl = st.text_input("Frase de URL", placeholder="datos-abiertos")
    keywords = st.text_input("Palabras clave adicionales", value="datos inmobiliarios México")
    parts = [keywords.strip()]
    if site.strip():
        parts.append(f"site:{site.strip()}")
    if intitle.strip():
        parts.append(f"intitle:{intitle.strip()}")
    if inurl.strip():
        parts.append(f"inurl:{inurl.strip()}")
    query = " ".join(parts)
    st.code(query)
    st.link_button("Ejecutar búsqueda en Google", f"https://www.google.com/search?q={quote_plus(query)}")


def record_export(report_type, format_name, filename_value, filters):
    execute(
        "INSERT INTO export_history (report_type, format, filename, filters) VALUES (%s, %s, %s, %s::jsonb)",
        (report_type, format_name, filename_value, json.dumps(filters, ensure_ascii=False)),
    )


def render_export_controls(analytics, filters, discussions, report_type="analytics"):
    st.subheader("Exportar")
    columns = st.columns([2, 2, 2, 2])
    export_scope = columns[0].selectbox("Qué exportar", ["Vista actual", "Informe completo", "Discusiones", "Tendencias", "Datos sin procesar"], key=f"export_scope_{report_type}")
    export_format = columns[1].selectbox("Formato", ["CSV", "Excel", "PDF", "JSON", "PNG", "SVG"], key=f"export_format_{report_type}")
    include_charts = columns[2].checkbox("Incluir gráficos", value=True, key=f"export_charts_{report_type}")
    generate = columns[3].button("Generar exportación", key=f"generate_export_{report_type}", use_container_width=True)
    if not generate:
        return

    frames = filtered_analytics_frames(analytics, discussions)
    selected_frame = frames.get("Discussions" if export_scope in {"Vista actual", "Discusiones", "Datos sin procesar"} else "Trends", discussions_frame(analytics, discussions))
    if export_scope == "Tendencias":
        selected_frame = frames["Trends"]
    if export_scope == "Datos sin procesar":
        selected_frame = frames["Discussions"]

    try:
        if export_format == "CSV":
            filename_value, content = export_csv(selected_frame, filters, f"{report_type}-{export_scope}")
            mime = "text/csv"
        elif export_format == "JSON":
            filename_value, content = export_json(frames, filters, f"{report_type}-{export_scope}")
            mime = "application/json"
        elif export_format == "Excel":
            filename_value, content = export_xlsx(analytics, filters, discussions)
            mime = "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        elif export_format == "PDF":
            filename_value, content = export_pdf(analytics, filters, discussions)
            mime = "application/pdf"
        else:
            filename_value, content, mime = export_chart(analytics, filters, export_format.lower())
        write_export(filename_value, content)
        record_export(export_scope, export_format, filename_value, filters)
        st.download_button("Descargar exportación", content, file_name=filename_value, mime=mime, key=f"download_{report_type}_{export_format}")
        st.success(f"Exportación lista: {filename_value}")
    except Exception as error:
        st.error(f"La exportación falló: {error}")


def render_export_history():
    rows = execute("SELECT created_at, report_type, format, filename, filters, status FROM export_history ORDER BY created_at DESC LIMIT 20", fetch=True)
    if rows:
        st.subheader("Historial de exportaciones")
        st.dataframe(pd.DataFrame(rows, columns=["created_at", "report_type", "format", "filename", "filters", "status"]), use_container_width=True, hide_index=True)


def render_analytics_filters(analytics):
    locations = sorted({item.location for item in analytics.discussions if item.location})
    sources = sorted({item.source for item in analytics.discussions if item.source})
    intent_labels = {"BUYING_INTENT": "Compra", "SELLING_INTENT": "Venta", "RENTING_INTENT": "Renta", "DISCUSSION": "Discusión"}
    intents = sorted({intent_labels.get(item.intent, item.intent) for item in analytics.discussions if item.intent})
    with st.container(border=True):
        st.subheader("Filtros de análisis")
        columns = st.columns(5)
        date_range = columns[0].selectbox("Periodo", ["Últimos 7 días", "Últimos 30 días", "Últimos 90 días"])
        location = columns[1].selectbox("Ubicación", ["Todas las ubicaciones", *locations])
        source = columns[2].selectbox("Fuente", ["Todas las fuentes", *sources])
        intent = columns[3].selectbox("Intención", ["Todas las intenciones", *intents])
        sentiment = columns[4].selectbox("Sentimiento", ["Todos los sentimientos", "Positivo", "Neutral", "Negativo", "Neutral-Negativo"])
    return date_range, location, source, intent, sentiment


def filtered_discussions(analytics, location, source, intent, sentiment, search=""):
    search_value = search.strip().lower()
    intent_labels = {"Compra": "BUYING_INTENT", "Venta": "SELLING_INTENT", "Renta": "RENTING_INTENT", "Discusión": "DISCUSSION"}
    sentiment_labels = {"Positivo": "Positive", "Neutral": "Neutral", "Negativo": "Negative", "Neutral-Negativo": "Neutral-Negative"}
    internal_intent = intent_labels.get(intent, intent)
    internal_sentiment = sentiment_labels.get(sentiment, sentiment)
    return [
        item for item in analytics.discussions
        if (location == "Todas las ubicaciones" or item.location == location)
        and (source == "Todas las fuentes" or item.source == source)
        and (intent == "Todas las intenciones" or item.intent == internal_intent)
        and (sentiment == "Todos los sentimientos" or item.sentiment == internal_sentiment)
        and (not search_value or search_value in f"{item.question} {item.summary}".lower())
    ]


def render_quick_stats(analytics):
    st.subheader("Estadísticas rápidas")
    stats = [
        ("Preguntas", analytics.quick_stats.questions, "❓"),
        ("Fuentes", analytics.quick_stats.sources, "◎"),
        ("Temas", analytics.quick_stats.topics, "#"),
        ("Sentimiento", analytics.quick_stats.sentiment, "◒"),
    ]
    columns = st.columns(4)
    for column, (label, metric, icon) in zip(columns, stats):
        with column:
            if isinstance(metric.value, str):
                value = metric.value
                delta = metric.change
            elif label == "Sentimiento":
                value = f"{metric.value:+.0f}%"
                delta = metric.label
            else:
                value = f"{metric.value:,}"
                delta = metric.change_label or (f"{metric.change:+.0f}%" if metric.change is not None else None)
            st.metric(f"{icon} {label}", value, delta=delta, help=f"{label} from the selected analytics data period.")


def render_trending_questions(analytics):
    st.subheader("Preguntas populares - últimos 7 días")
    for index, question in enumerate(analytics.trending_questions, 1):
        direction = {"up": "↑", "down": "↓", "stable": "→", "new": "NEW"}[question.trend]
        with st.container(border=True):
            columns = st.columns([0.5, 6, 1.5, 1])
            columns[0].write(f"**{index}**")
            columns[1].write(f"**{question.question}**")
            columns[1].caption(f"{question.mentions} menciones")
            columns[2].write(direction)
            if columns[3].button("Open", key=f"question_{question.id}"):
                st.session_state["analytics_search"] = question.question
                st.info(f"Discussion results filtered for: {question.question}")
    st.button("Ver todas →", key="view_all_questions")


def render_location_and_sentiment(analytics):
    left, right = st.columns(2)
    with left:
        st.subheader("Mapa de actividad por ubicación")
        map_data = pd.DataFrame([{"latitude": item.latitude, "longitude": item.longitude, "mentions": item.mentions} for item in analytics.neighborhoods])
        if not map_data.empty:
            st.map(map_data, latitude="latitude", longitude="longitude", size="mentions", zoom=10)
            st.caption("Los marcadores más grandes indican mayor actividad de discusión. Selecciona una ubicación para ver sus detalles.")
            selected = st.selectbox("Detalle de ubicación", [item.neighborhood for item in analytics.neighborhoods], key="map_location")
            item = next(item for item in analytics.neighborhoods if item.neighborhood == selected)
            st.write(f"**{item.neighborhood}**: {item.mentions:,} mentions, {item.sentiment} sentiment, {item.trend_percent:+.0f}% trend")
        else:
            st.info("No hay datos de ubicación para este periodo.")
    with right:
        st.subheader("Sentimiento a lo largo del tiempo")
        sentiment_frame = pd.DataFrame([point.__dict__ for point in analytics.sentiment])
        if not sentiment_frame.empty:
            sentiment_frame["date"] = pd.to_datetime(sentiment_frame["date"])
            st.line_chart(sentiment_frame.set_index("date")["positive neutral negative".split()])
            st.caption("Los porcentajes provienen del proveedor de análisis. Los datos demo están identificados en la pantalla.")
        else:
            st.info("No hay una serie temporal de sentimiento para este periodo.")


def render_concerns(analytics):
    st.subheader("Principales preocupaciones por intención")
    columns = st.columns(3)
    for column, intent in zip(columns, ["buying", "selling", "renting"]):
        with column:
            intent_label = {"buying": "Compra", "selling": "Venta", "renting": "Renta"}[intent]
            st.markdown(f"**{intent_label}**")
            concerns = sorted((item for item in analytics.concerns if item.intent == intent), key=lambda item: item.count, reverse=True)
            for concern in concerns:
                if st.button(f"{concern.topic}  {concern.count}", key=f"concern_{intent}_{concern.topic}", use_container_width=True):
                    st.info(f"Drill-down ready for {intent} / {concern.topic}.")


def render_insights(analytics):
    st.subheader("🚀 Hallazgos generados por IA - Esta semana")
    if analytics.is_demo:
        st.caption("Los hallazgos demo están separados de los datos de producción y deben reemplazarse por análisis verificados antes de usarse operativamente.")
    columns = st.columns(3)
    for column, insight in zip(columns, analytics.insights):
        with column:
            with st.container(border=True):
                insight_type = {"trend": "NUEVA TENDENCIA", "sentiment_shift": "CAMBIO DE SENTIMIENTO", "content_gap": "BRECHA DE CONTENIDO"}[insight.type]
                st.caption(insight_type)
                st.write(f"**{insight.title}**")
                st.write(insight.description)
                if insight.metric is not None:
                    st.metric("Underlying metric", f"{insight.metric:+.0f}%" if insight.type == "sentiment_shift" else f"{insight.metric:.0f}")
                if insight.opportunity:
                    st.caption(f"Oportunidad: {insight.opportunity}")
                st.caption(f"Periodo: {insight.period}")
                st.caption(f"Referencia: {insight.source_reference}")
                if st.button(insight.action or "View details →", key=f"insight_{insight.id}"):
                    st.info("Esta acción está preparada como punto de integración para el futuro flujo de contenido.")


def render_discussion_results(analytics, location, source, intent, sentiment):
    st.subheader("Resultados de discusiones")
    search = st.text_input("Buscar discusiones", key="analytics_search", placeholder="Busca preguntas, resúmenes o temas")
    result_list = filtered_discussions(analytics, location, source, intent, sentiment, search)
    sort_by = st.selectbox("Ordenar", ["Más recientes", "Interacción", "Ubicación"], key="discussion_sort")
    if sort_by == "Interacción":
        result_list.sort(key=lambda item: item.engagement, reverse=True)
    elif sort_by == "Ubicación":
        result_list.sort(key=lambda item: item.location)
    page_size = 5
    page_count = max(1, (len(result_list) + page_size - 1) // page_size)
    page = st.number_input("Página", min_value=1, max_value=page_count, value=1, step=1, key="discussion_page")
    st.write(f"**Resultados: {len(result_list)} discusiones encontradas**")
    for discussion in result_list[(page - 1) * page_size:page * page_size]:
        with st.container(border=True):
            intent_label = {"BUYING_INTENT": "COMPRA", "SELLING_INTENT": "VENTA", "RENTING_INTENT": "RENTA", "DISCUSSION": "DISCUSIÓN"}.get(discussion.intent, discussion.intent)
            st.caption(f"📍 {discussion.location} • {discussion.source} • {discussion.published_at} • {intent_label}")
            st.write(f"**{discussion.question}**")
            st.write(discussion.summary)
            for point in discussion.key_points:
                st.write(f"- {point}")
            sentiment_label = {"Positive": "Positivo", "Negative": "Negativo", "Neutral-Negative": "Neutral-Negativo", "Neutral": "Neutral"}.get(discussion.sentiment, discussion.sentiment)
            st.caption(f"Sentimiento: {sentiment_label}   Interacción: {'⭐' * max(1, discussion.engagement)}")
            buttons = st.columns(2)
            if discussion.source_url:
                buttons[0].link_button("Ver discusión completa →", discussion.source_url)
            if buttons[1].button("Similar questions →", key=f"similar_{discussion.id}"):
                st.info("La recuperación de preguntas similares está preparada para una futura API de análisis.")


def render_analytics(analytics):
    st.header("Análisis y hallazgos")
    if analytics.is_demo:
        st.info("Se muestran datos demo aislados porque todavía no hay registros importados en community_content.")
    render_quick_stats(analytics)
    date_range, location, source, intent, sentiment = render_analytics_filters(analytics)
    st.caption(f"Periodo activo: {date_range}")
    render_trending_questions(analytics)
    render_location_and_sentiment(analytics)
    render_concerns(analytics)
    render_insights(analytics)
    active_filters = {"date_range": date_range, "location": location, "source": source, "intent": intent, "sentiment": sentiment}
    selected_discussions = filtered_discussions(analytics, location, source, intent, sentiment, st.session_state.get("analytics_search", ""))
    render_discussion_results(analytics, location, source, intent, sentiment)
    render_export_controls(analytics, active_filters, selected_discussions, "analytics")
    render_export_history()


def render_trends(analytics):
    st.header("Tendencias emergentes")
    st.caption("Las tendencias muestran por defecto los últimos 90 días. Las explicaciones requieren una fuente verificada antes de tomar decisiones de producción.")
    for trend in analytics.trends:
        with st.container(border=True):
            direction = "↑" if trend.direction == "up" else "↓" if trend.direction == "down" else "→"
            st.write(f"**{direction} {trend.topic}**")
            columns = st.columns(3)
            columns[0].metric("Crecimiento", f"{trend.growth_percent:+.0f}% vs periodo anterior")
            columns[1].metric("Menciones", f"{trend.mentions:,}")
            columns[2].metric("Periodo anterior", f"{trend.previous_period_mentions:,}")
            st.write(trend.explanation)
            st.caption(f"Oportunidad: {trend.opportunity}")
            st.caption(f"Referencia: {trend.source_reference}")
            actions = st.columns(2)
            if actions[0].button("Generar ideas de contenido →", key=f"trend_content_{trend.id}"):
                st.info("La generación de contenido está preparada para una futura integración.")
            if actions[1].button("Ver discusiones →", key=f"trend_discussions_{trend.id}"):
                st.info("El detalle de discusiones está preparado para una futura integración.")

    st.subheader("Evolución de temas - últimos 90 días")
    topics = sorted(analytics.topic_evolution["topic"].unique()) if not analytics.topic_evolution.empty else []
    selected_topics = st.multiselect("Temas", topics, default=topics, key="topic_toggles")
    evolution = analytics.topic_evolution[analytics.topic_evolution["topic"].isin(selected_topics)]
    if not evolution.empty:
        st.line_chart(evolution.pivot(index="date", columns="topic", values="mentions"))
    else:
        st.info("No hay datos de evolución de temas disponibles.")

    st.subheader("Ranking de colonias - por volumen de menciones")
    ranking_metric = st.selectbox("Ordenar por", ["Volumen de menciones", "Tasa de crecimiento"], key="ranking_metric")
    ranking = pd.DataFrame([item.__dict__ for item in analytics.neighborhoods])
    if not ranking.empty:
        sort_column = "mentions" if ranking_metric == "Volumen de menciones" else "trend_percent"
        st.dataframe(ranking.sort_values(sort_column, ascending=False), use_container_width=True, hide_index=True)
        st.button("Ranking completo →", key="full_rankings")
    render_export_controls(analytics, {"date_range": "Últimos 90 días", "location": "Todas las ubicaciones"}, analytics.discussions, "trends")
    render_export_history()


st.set_page_config(page_title="Operaciones inmobiliarias de México", page_icon="MX", layout="wide")
st.title("Operaciones inmobiliarias de México")
st.caption("Propiedades, relaciones, metas, inteligencia, monitoreo e investigación conforme a la normativa")

try:
    ensure_operational_tables()
    states = get_options("state")
    property_types = get_options("property_type")
    sources = get_options("source_name")
except Exception as error:
    st.error(f"No se pudo conectar a PostgreSQL: {error}")
    st.stop()

with st.sidebar:
    workspace = st.radio("Área de trabajo", ["Operaciones", "Análisis y hallazgos", "Tendencias"], key="workspace")
    st.header("Filtros de propiedades")
    selected_state = st.selectbox("Estado", ["Todos los estados", *states])
    selected_type = st.selectbox("Tipo de propiedad", ["Todos los tipos de propiedad", *property_types])
    selected_source = st.selectbox("Fuente", ["Todas las fuentes", *sources])
    selected_band = st.selectbox("Rango de precio", list(PRICE_BANDS))

state_filter = None if selected_state == "Todos los estados" else selected_state
type_filter = None if selected_type == "Todos los tipos de propiedad" else selected_type
source_filter = None if selected_source == "Todas las fuentes" else selected_source
min_price, max_price = PRICE_BANDS[selected_band]

try:
    validate_filters(state_filter, min_price, max_price)
    data = load_properties(state_filter, type_filter, source_filter, min_price, max_price)
except Exception as error:
    st.error(f"No se pudieron cargar los datos de propiedades: {error}")
    st.stop()

analytics = load_analytics_data(connect)

if workspace == "Análisis y hallazgos":
    render_analytics(analytics)
elif workspace == "Tendencias":
    render_trends(analytics)
else:
    metric_columns = st.columns(4)
    metric_columns[0].metric("Propiedades", f"{len(data):,}")
    metric_columns[1].metric("Precio promedio", f"MXN {data['price'].mean():,.0f}" if not data.empty else "-")
    metric_columns[2].metric("Fuentes", f"{data['source_name'].nunique():,}")
    metric_columns[3].metric("Tipos de propiedad", f"{data['property_type'].nunique():,}")

    tabs = st.tabs(["Propiedades", "Alianzas", "Indicadores", "Inteligencia de negocio", "Alertas de monitoreo", "Búsqueda avanzada"])
    with tabs[0]:
        st.subheader("Anuncios interactivos")
        display_columns = ["id", "title", "state", "municipality", "property_type", "price", "price_band", "source_name", "listing_status"]
        st.dataframe(data[display_columns], use_container_width=True, hide_index=True)
        render_listing_detail(data)
    with tabs[1]:
        render_alliances()
    with tabs[2]:
        render_kpis()
    with tabs[3]:
        render_intelligence(data)
    with tabs[4]:
        render_alerts()
    with tabs[5]:
        render_search()
