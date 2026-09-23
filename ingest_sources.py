import csv
import hashlib
import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, List

DATA_DIR = Path("data")
RAW_DIR = DATA_DIR / "raw"
EXPORT_DIR = DATA_DIR / "export"


def load_json(path: str) -> Any:
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


def normalize_record(raw: Dict[str, Any], source_name: str) -> Dict[str, Any]:
    now = datetime.now(timezone.utc).isoformat()

    return {
        "listing_id": str(raw.get("listing_id") or f"{source_name}-{len(raw)}"),
        "source_name": source_name,
        "source_url": raw.get("source_url", ""),
        "title": raw.get("title", ""),
        "description": raw.get("description", ""),
        "price": float(raw.get("price", 0) or 0),
        "currency": raw.get("currency", "MXN"),
        "property_type": raw.get("property_type", ""),
        "bedrooms": int(raw.get("bedrooms", 0) or 0),
        "bathrooms": int(raw.get("bathrooms", 0) or 0),
        "parking_spaces": int(raw.get("parking_spaces", 0) or 0),
        "square_meters": float(raw.get("square_meters", 0) or 0),
        "lot_meters": float(raw.get("lot_meters", 0) or 0),
        "state": raw.get("state", ""),
        "municipality": raw.get("municipality", ""),
        "colonia": raw.get("colonia", ""),
        "address": raw.get("address", ""),
        "latitude": raw.get("latitude"),
        "longitude": raw.get("longitude"),
        "listing_status": raw.get("listing_status", "active"),
        "broker_name": raw.get("broker_name", ""),
        "broker_phone": raw.get("broker_phone", ""),
        "created_at": raw.get("created_at", now),
        "updated_at": raw.get("updated_at", now),
        "last_seen_at": now,
        "legal_status": raw.get("legal_status", "manual_review"),
    }


def normalize_community_record(raw: Dict[str, Any], source: Dict[str, Any]) -> Dict[str, Any]:
    source_key = source["source_key"]
    canonical_url = raw.get("source_url") or raw.get("thread_url") or raw.get("parent_url") or ""
    external_id = raw.get("content_id") or raw.get("comment_id") or raw.get("discussion_id") or raw.get("post_id")
    fallback = hashlib.sha256(f"{source_key}|{canonical_url}|{raw.get('title', '')}|{raw.get('content', raw.get('body', ''))}".encode("utf-8")).hexdigest()[:24]
    now = datetime.now(timezone.utc).isoformat()
    return {
        "content_id": str(external_id or f"{source_key}-{fallback}"),
        "source_key": source_key,
        "source_name": source["source_name"],
        "source_type": source.get("source_type", "community"),
        "platform": source.get("platform", "unknown"),
        "content_type": raw.get("content_type", "community_discussion"),
        "title": raw.get("title", ""),
        "content": raw.get("content", raw.get("body", raw.get("description", ""))),
        "author_display_name": raw.get("author_display_name", raw.get("author", "")),
        "published_at": raw.get("published_at", raw.get("created_at")),
        "source_url": canonical_url,
        "parent_url": raw.get("parent_url", raw.get("thread_url", "")),
        "discussion_id": raw.get("discussion_id", raw.get("thread_id", "")),
        "comment_id": raw.get("comment_id", ""),
        "engagement_metrics": json.dumps(raw.get("engagement_metrics", {}), ensure_ascii=False),
        "state": raw.get("state", source.get("state", "")),
        "municipality": raw.get("municipality", source.get("municipality", "")),
        "neighborhood": raw.get("neighborhood", raw.get("colonia", "")),
        "property_type": raw.get("property_type", ""),
        "asking_price": raw.get("asking_price", raw.get("price")),
        "rent_price": raw.get("rent_price"),
        "bedrooms": raw.get("bedrooms"),
        "bathrooms": raw.get("bathrooms"),
        "square_meters": raw.get("square_meters"),
        "transaction_context": raw.get("transaction_context", ""),
        "housing_program_references": json.dumps(raw.get("housing_program_references", []), ensure_ascii=False),
        "financing_references": json.dumps(raw.get("financing_references", []), ensure_ascii=False),
        "relevant_entities": json.dumps(raw.get("relevant_entities", []), ensure_ascii=False),
        "extracted_keywords": json.dumps(raw.get("extracted_keywords", []), ensure_ascii=False),
        "language": raw.get("language", source.get("language", "es")),
        "sentiment": raw.get("sentiment"),
        "crawl_timestamp": raw.get("crawl_timestamp", now),
        "legal_status": raw.get("legal_status", "manual_review"),
    }


def dedupe(records: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    seen = {}
    merged = []

    for record in records:
        key = (
            record.get("listing_id")
            or record.get("content_id")
            or record.get("source_url")
            or f"{record.get('source_name')}-{record.get('address')}-{record.get('price')}"
        )
        if key not in seen:
            seen[key] = True
            merged.append(record)

    return merged


def export_csv(records: List[Dict[str, Any]], path: str):
    fieldnames = [
        "listing_id", "source_name", "source_url", "title", "description", "price",
        "currency", "property_type", "bedrooms", "bathrooms", "parking_spaces",
        "square_meters", "lot_meters", "state", "municipality", "colonia",
        "address", "latitude", "longitude", "listing_status", "broker_name",
        "broker_phone", "created_at", "updated_at", "last_seen_at", "legal_status"
    ]

    with open(path, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(records)


def export_community_csv(records: List[Dict[str, Any]], path: str):
    fieldnames = [
        "content_id", "source_key", "source_name", "source_type", "platform", "content_type",
        "title", "content", "author_display_name", "published_at", "source_url", "parent_url",
        "discussion_id", "comment_id", "engagement_metrics", "state", "municipality", "neighborhood",
        "property_type", "asking_price", "rent_price", "bedrooms", "bathrooms", "square_meters",
        "transaction_context", "housing_program_references", "financing_references", "relevant_entities",
        "extracted_keywords", "language", "sentiment", "crawl_timestamp", "legal_status"
    ]
    with open(path, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(records)


def export_source_configs(sources: List[Dict[str, Any]], path: str):
    fieldnames = [
        "source_key", "source_name", "source_type", "platform", "country", "state", "municipality",
        "language", "url", "discovery_method", "access_method", "robots_policy", "crawl_policy",
        "crawl_frequency", "enabled", "content_types", "geographic_scope", "extraction_strategy",
        "parser_adapter", "deduplication_strategy", "last_crawled_at", "last_success_at", "last_error",
        "attribution_metadata", "legal_basis", "allowed_use", "status"
    ]
    with open(path, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames, extrasaction="ignore")
        writer.writeheader()
        for source in sources:
            row = dict(source)
            row["source_key"] = row.get("source_key") or row["source_name"].lower().replace(" ", "_")
            for field in ("content_types", "geographic_scope"):
                row[field] = json.dumps(row.get(field, []), ensure_ascii=False)
            writer.writerow(row)


def main():
    RAW_DIR.mkdir(parents=True, exist_ok=True)
    EXPORT_DIR.mkdir(parents=True, exist_ok=True)

    sources = load_json("sources.json")
    community_registry = Path("community_sources.json")
    if community_registry.exists():
        sources.extend(load_json(str(community_registry)))
    all_records = []
    all_community_records = []

    found_input = False
    for source in sources:
        source_name = source["source_name"]
        source_file = RAW_DIR / f"{source.get('source_key', source_name.lower().replace(' ', '_'))}.json"

        if source_file.exists():
            found_input = True
            data = load_json(str(source_file))
            items = data if isinstance(data, list) else [data]
            for item in items:
                if source.get("source_type") in {"forum", "community", "social_forum", "social_group", "marketplace_qa", "qa", "professional_social", "local_news", "government_housing", "social_discovery"} or item.get("content_type"):
                    all_community_records.append(normalize_community_record(item, source))
                else:
                    all_records.append(normalize_record(item, source_name))

    deduped = dedupe(all_records)
    export_csv(deduped, str(EXPORT_DIR / "properties.csv"))
    community_deduped = dedupe(all_community_records)
    export_community_csv(community_deduped, str(EXPORT_DIR / "community_content.csv"))
    export_source_configs(sources, str(EXPORT_DIR / "source_configs.csv"))

    if not found_input:
        print("No source files found in data/raw. Created an empty export with headers only.")
    else:
        print(f"Exported {len(deduped)} normalized records to data/export/properties.csv")
    print(f"Exported {len(community_deduped)} normalized community records to data/export/community_content.csv")
    print(f"Exported {len(sources)} source configurations to data/export/source_configs.csv")


if __name__ == "__main__":
    main()
