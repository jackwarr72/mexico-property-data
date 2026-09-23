import csv
import json
import os
from datetime import datetime, timezone

import psycopg2
from dotenv import load_dotenv

load_dotenv()

DB_CONFIG = {
    "host": os.getenv("POSTGRES_HOST", "localhost"),
    "port": int(os.getenv("POSTGRES_PORT", "5432")),
    "database": os.getenv("POSTGRES_DB", "property_data"),
    "user": os.getenv("POSTGRES_USER", "postgres"),
    "password": os.getenv("POSTGRES_PASSWORD", "postgres")
}


def load_csv(path):
    if not os.path.exists(path):
        print(f"CSV not found at {path}. Nothing to import.")
        return []

    with open(path, newline="", encoding="utf-8") as f:
        rows = list(csv.DictReader(f))
        if not rows:
            print(f"CSV at {path} is empty. Nothing to import.")
        return rows


def insert_properties(rows):
    if not rows:
        print("No rows to import into Postgres.")
        return

    try:
        conn = psycopg2.connect(**DB_CONFIG)
    except psycopg2.OperationalError as exc:
        print("PostgreSQL is not running or is unreachable.")
        print(f"Connection settings: host={DB_CONFIG['host']}, port={DB_CONFIG['port']}, db={DB_CONFIG['database']}")
        print("Start PostgreSQL and re-run this script, or set POSTGRES_HOST/POSTGRES_DB/POSTGRES_USER/POSTGRES_PASSWORD.")
        print(f"Original error: {exc}")
        return

    cur = conn.cursor()

    try:
        for row in rows:
            cur.execute(
                """
                INSERT INTO properties (
                    listing_id, source_name, source_url, title, description, price, currency,
                    property_type, bedrooms, bathrooms, parking_spaces, square_meters,
                    lot_meters, state, municipality, colonia, address, latitude, longitude,
                    listing_status, broker_name, broker_phone, created_at, updated_at,
                    last_seen_at, legal_status
                ) VALUES (
                    %s, %s, %s, %s, %s, %s, %s,
                    %s, %s, %s, %s, %s,
                    %s, %s, %s, %s, %s, %s, %s,
                    %s, %s, %s, %s, %s,
                    %s, %s
                )
                ON CONFLICT (source_name, listing_id) DO UPDATE SET
                    source_url = EXCLUDED.source_url,
                    title = EXCLUDED.title,
                    description = EXCLUDED.description,
                    price = EXCLUDED.price,
                    currency = EXCLUDED.currency,
                    property_type = EXCLUDED.property_type,
                    bedrooms = EXCLUDED.bedrooms,
                    bathrooms = EXCLUDED.bathrooms,
                    parking_spaces = EXCLUDED.parking_spaces,
                    square_meters = EXCLUDED.square_meters,
                    lot_meters = EXCLUDED.lot_meters,
                    state = EXCLUDED.state,
                    municipality = EXCLUDED.municipality,
                    colonia = EXCLUDED.colonia,
                    address = EXCLUDED.address,
                    latitude = EXCLUDED.latitude,
                    longitude = EXCLUDED.longitude,
                    listing_status = EXCLUDED.listing_status,
                    broker_name = EXCLUDED.broker_name,
                    broker_phone = EXCLUDED.broker_phone,
                    updated_at = EXCLUDED.updated_at,
                    last_seen_at = EXCLUDED.last_seen_at,
                    legal_status = EXCLUDED.legal_status
                """,
                (
                    row.get("listing_id"),
                    row.get("source_name"),
                    row.get("source_url"),
                    row.get("title"),
                    row.get("description"),
                    float(row.get("price") or 0),
                    row.get("currency") or "MXN",
                    row.get("property_type"),
                    int(row.get("bedrooms") or 0),
                    int(row.get("bathrooms") or 0),
                    int(row.get("parking_spaces") or 0),
                    float(row.get("square_meters") or 0),
                    float(row.get("lot_meters") or 0),
                    row.get("state"),
                    row.get("municipality"),
                    row.get("colonia"),
                    row.get("address"),
                    float(row.get("latitude") or 0) if row.get("latitude") else None,
                    float(row.get("longitude") or 0) if row.get("longitude") else None,
                    row.get("listing_status") or "active",
                    row.get("broker_name"),
                    row.get("broker_phone"),
                    row.get("created_at") or datetime.now(timezone.utc).isoformat(),
                    row.get("updated_at") or datetime.now(timezone.utc).isoformat(),
                    row.get("last_seen_at") or datetime.now(timezone.utc).isoformat(),
                    row.get("legal_status") or "manual_review"
                )
            )

        conn.commit()
        print(f"Imported {len(rows)} rows into Postgres")
    except Exception as exc:
        conn.rollback()
        print(f"Import failed while inserting rows: {exc}")
    finally:
        cur.close()
        conn.close()


def insert_source_configs(rows):
    if not rows:
        print("No source configurations to import.")
        return
    with psycopg2.connect(**DB_CONFIG) as conn:
        with conn.cursor() as cur:
            for row in rows:
                cur.execute(
                    """
                    INSERT INTO source_registry (
                        source_key, source_name, source_type, platform, country, state, municipality,
                        language, url, discovery_method, access_method, robots_policy, crawl_policy,
                        crawl_frequency, enabled, content_types, geographic_scope, extraction_strategy,
                        parser_adapter, deduplication_strategy, last_crawled_at, last_success_at,
                        last_error, attribution_metadata, legal_basis, allowed_use, status
                    ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s,
                              %s::jsonb, %s::jsonb, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                    ON CONFLICT (source_key) DO UPDATE SET
                        source_name = EXCLUDED.source_name, source_type = EXCLUDED.source_type,
                        platform = EXCLUDED.platform, url = EXCLUDED.url, access_method = EXCLUDED.access_method,
                        enabled = EXCLUDED.enabled, content_types = EXCLUDED.content_types,
                        geographic_scope = EXCLUDED.geographic_scope, status = EXCLUDED.status,
                        updated_at = CURRENT_TIMESTAMP
                    """,
                    (
                        row.get("source_key"), row.get("source_name"), row.get("source_type"), row.get("platform"),
                        row.get("country"), row.get("state"), row.get("municipality"), row.get("language"),
                        row.get("url"), row.get("discovery_method"), row.get("access_method"), row.get("robots_policy"),
                        row.get("crawl_policy"), row.get("crawl_frequency"), row.get("enabled", "false").lower() == "true",
                        row.get("content_types") or "[]", row.get("geographic_scope") or "[]", row.get("extraction_strategy"),
                        row.get("parser_adapter"), row.get("deduplication_strategy"), row.get("last_crawled_at") or None,
                        row.get("last_success_at") or None, row.get("last_error"), row.get("attribution_metadata"),
                        row.get("legal_basis"), row.get("allowed_use"), row.get("status")
                    )
                )
    print(f"Imported {len(rows)} source configurations into Postgres")


def json_value(value):
    return value if value else "[]"


def insert_community_content(rows):
    if not rows:
        print("No community content to import.")
        return
    with psycopg2.connect(**DB_CONFIG) as conn:
        with conn.cursor() as cur:
            for row in rows:
                cur.execute(
                    """
                    INSERT INTO community_content (
                        content_id, source_key, source_name, source_type, platform, content_type, title, content,
                        author_display_name, published_at, source_url, parent_url, discussion_id, comment_id,
                        engagement_metrics, state, municipality, neighborhood, property_type, asking_price,
                        rent_price, bedrooms, bathrooms, square_meters, transaction_context,
                        housing_program_references, financing_references, relevant_entities, extracted_keywords,
                        language, sentiment, crawl_timestamp, legal_status
                    ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s::jsonb,
                              %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s::jsonb, %s::jsonb, %s::jsonb,
                              %s::jsonb, %s, %s, %s, %s)
                    ON CONFLICT (source_name, content_id) DO UPDATE SET
                        title = EXCLUDED.title, content = EXCLUDED.content, source_url = EXCLUDED.source_url,
                        engagement_metrics = EXCLUDED.engagement_metrics, crawl_timestamp = EXCLUDED.crawl_timestamp,
                        legal_status = EXCLUDED.legal_status
                    """,
                    (
                        row.get("content_id"), row.get("source_key"), row.get("source_name"), row.get("source_type"),
                        row.get("platform"), row.get("content_type"), row.get("title"), row.get("content"),
                        row.get("author_display_name"), row.get("published_at") or None, row.get("source_url"),
                        row.get("parent_url"), row.get("discussion_id"), row.get("comment_id"), json_value(row.get("engagement_metrics")),
                        row.get("state"), row.get("municipality"), row.get("neighborhood"), row.get("property_type"),
                        float(row["asking_price"]) if row.get("asking_price") else None,
                        float(row["rent_price"]) if row.get("rent_price") else None,
                        int(row["bedrooms"]) if row.get("bedrooms") else None, int(row["bathrooms"]) if row.get("bathrooms") else None,
                        float(row["square_meters"]) if row.get("square_meters") else None, row.get("transaction_context"),
                        json_value(row.get("housing_program_references")), json_value(row.get("financing_references")),
                        json_value(row.get("relevant_entities")), json_value(row.get("extracted_keywords")), row.get("language"),
                        row.get("sentiment"), row.get("crawl_timestamp") or None, row.get("legal_status") or "manual_review"
                    )
                )
    print(f"Imported {len(rows)} community records into Postgres")


def main():
    rows = load_csv("data/export/properties.csv")
    insert_properties(rows)
    insert_source_configs(load_csv("data/export/source_configs.csv"))
    insert_community_content(load_csv("data/export/community_content.csv"))


if __name__ == "__main__":
    main()
