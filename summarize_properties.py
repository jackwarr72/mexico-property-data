import csv
import os

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


def export_summary(output_path: str):
    query = """
        SELECT
            source_name,
            COUNT(*) AS total_listings,
            ROUND(AVG(price), 2) AS avg_price,
            MIN(price) AS min_price,
            MAX(price) AS max_price
        FROM properties
        GROUP BY source_name
        ORDER BY total_listings DESC, source_name;
    """

    with psycopg2.connect(**DB_CONFIG) as conn:
        with conn.cursor() as cur:
            cur.execute(query)
            rows = cur.fetchall()

    with open(output_path, "w", newline="", encoding="utf-8") as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(["source_name", "total_listings", "avg_price", "min_price", "max_price"])
        writer.writerows(rows)

    print(f"Exported summary to {output_path}")


if __name__ == "__main__":
    export_summary("data/export/property_summary.csv")
