import argparse
import csv
import math
import os
import re
import unicodedata
from pathlib import Path

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


def write_csv(path: str, headers, rows):
    with open(path, "w", newline="", encoding="utf-8") as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(headers)
        writer.writerows(rows)


def validate_filters(state=None, min_price=None, max_price=None):
    if state is not None and not state.strip():
        raise ValueError("--state cannot be empty or whitespace only.")
    for name, value in (("--min-price", min_price), ("--max-price", max_price)):
        if value is not None and (not math.isfinite(value) or value < 0):
            raise ValueError(f"{name} must be a finite, non-negative number.")
    if min_price is not None and max_price is not None and min_price > max_price:
        raise ValueError("--min-price cannot be greater than --max-price.")


def slugify(value):
    normalized = unicodedata.normalize("NFKD", value).encode("ascii", "ignore").decode("ascii")
    slug = re.sub(r"[^a-z0-9]+", "_", normalized.lower()).strip("_")
    return slug or "all"


def price_slug(value):
    if value is None:
        return "any"
    if value >= 1000000 and value % 1000000 == 0:
        return f"{int(value / 1000000)}m"
    if value >= 1000 and value % 1000 == 0:
        return f"{int(value / 1000)}k"
    return str(value).replace(".", "_")


def output_stem(state=None, min_price=None, max_price=None):
    if state is None and min_price is None and max_price is None:
        return "market_dashboard"
    state_part = slugify(state) if state else "all_states"
    return f"market_dashboard_{state_part}_{price_slug(min_price)}_{price_slug(max_price)}"


def build_filters(state=None, min_price=None, max_price=None):
    clauses = []
    params = []

    if state:
        clauses.append("LOWER(state) = LOWER(%s)")
        params.append(state)
    if min_price is not None:
        clauses.append("price >= %s")
        params.append(float(min_price))
    if max_price is not None:
        clauses.append("price <= %s")
        params.append(float(max_price))

    where_clause = "WHERE " + " AND ".join(clauses) if clauses else ""
    return where_clause, params


def get_city_metrics(state=None, min_price=None, max_price=None):
    where_clause, params = build_filters(state=state, min_price=min_price, max_price=max_price)
    query = f"""
        SELECT
            state,
            municipality,
            COUNT(*) AS total_listings,
            ROUND(AVG(price), 2) AS avg_price,
            MIN(price) AS min_price,
            MAX(price) AS max_price
        FROM properties
        {where_clause}
        GROUP BY state, municipality
        ORDER BY total_listings DESC, state, municipality;
    """
    with psycopg2.connect(**DB_CONFIG) as conn:
        with conn.cursor() as cur:
            cur.execute(query, params)
            return cur.fetchall()


def get_property_type_metrics(state=None, min_price=None, max_price=None):
    where_clause, params = build_filters(state=state, min_price=min_price, max_price=max_price)
    query = f"""
        SELECT
            property_type,
            COUNT(*) AS total_listings,
            ROUND(AVG(price), 2) AS avg_price,
            MIN(price) AS min_price,
            MAX(price) AS max_price
        FROM properties
        {where_clause}
        GROUP BY property_type
        ORDER BY total_listings DESC, property_type;
    """
    with psycopg2.connect(**DB_CONFIG) as conn:
        with conn.cursor() as cur:
            cur.execute(query, params)
            return cur.fetchall()


def get_state_price_band_metrics(state=None, min_price=None, max_price=None):
    where_clause, params = build_filters(state=state, min_price=min_price, max_price=max_price)
    query = f"""
        SELECT
            state,
            CASE
                WHEN price < 2000000 THEN '<2M'
                WHEN price < 5000000 THEN '2M-5M'
                WHEN price < 10000000 THEN '5M-10M'
                WHEN price < 20000000 THEN '10M-20M'
                ELSE '20M+'
            END AS price_band,
            COUNT(*) AS total_listings,
            ROUND(AVG(price), 2) AS avg_price,
            MIN(price) AS min_price,
            MAX(price) AS max_price
        FROM properties
        {where_clause}
        GROUP BY state,
            CASE
                WHEN price < 2000000 THEN '<2M'
                WHEN price < 5000000 THEN '2M-5M'
                WHEN price < 10000000 THEN '5M-10M'
                WHEN price < 20000000 THEN '10M-20M'
                ELSE '20M+'
            END
        ORDER BY state, price_band;
    """
    with psycopg2.connect(**DB_CONFIG) as conn:
        with conn.cursor() as cur:
            cur.execute(query, params)
            return cur.fetchall()


def main():
    parser = argparse.ArgumentParser(description="Export a market dashboard for property listings.")
    parser.add_argument("--state", help="Filter results to a specific state, e.g. 'Ciudad de México'.")
    parser.add_argument("--min-price", type=float, help="Minimum listing price in MXN.")
    parser.add_argument("--max-price", type=float, help="Maximum listing price in MXN.")
    args = parser.parse_args()

    try:
        validate_filters(args.state, args.min_price, args.max_price)
    except ValueError as error:
        parser.error(str(error))

    output_dir = Path("data/export")
    output_dir.mkdir(parents=True, exist_ok=True)

    stem = output_stem(args.state, args.min_price, args.max_price)
    city_path = output_dir / f"{stem}_by_city.csv"
    type_path = output_dir / f"{stem}_by_property_type.csv"
    band_path = output_dir / f"{stem}_by_state_and_price_band.csv"

    city_rows = get_city_metrics(state=args.state, min_price=args.min_price, max_price=args.max_price)
    city_headers = ["state", "municipality", "total_listings", "avg_price", "min_price", "max_price"]
    write_csv(str(city_path), city_headers, city_rows)

    type_rows = get_property_type_metrics(state=args.state, min_price=args.min_price, max_price=args.max_price)
    type_headers = ["property_type", "total_listings", "avg_price", "min_price", "max_price"]
    write_csv(str(type_path), type_headers, type_rows)

    band_rows = get_state_price_band_metrics(state=args.state, min_price=args.min_price, max_price=args.max_price)
    band_headers = ["state", "price_band", "total_listings", "avg_price", "min_price", "max_price"]
    write_csv(str(band_path), band_headers, band_rows)

    print(f"Exported city dashboard to {city_path}")
    print(f"Exported property type dashboard to {type_path}")
    print(f"Exported state + price band dashboard to {band_path}")

    if args.state or args.min_price is not None or args.max_price is not None:
        print("Applied filters: state=%s min_price=%s max_price=%s" % (args.state, args.min_price, args.max_price))
        total_rows = len(city_rows) + len(type_rows) + len(band_rows)
        if total_rows == 0:
            print("Warning: the filters matched no records; CSV files contain headers only.")


if __name__ == "__main__":
    main()
