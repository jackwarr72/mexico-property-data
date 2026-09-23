import json
import tempfile
import unittest
from pathlib import Path

from ingest_sources import dedupe, export_community_csv, normalize_community_record


class CommunityIngestionTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        with open("community_sources.json", encoding="utf-8") as source_file:
            cls.source = json.load(source_file)[5]

    def test_normalizes_public_discussion_fields(self):
        record = normalize_community_record(
            {
                "post_id": "reddit-demo-1",
                "content_type": "forum_posts",
                "title": "Venta urgente en Metepec",
                "body": "Casa con referencia a Infonavit",
                "author": "public_display_name",
                "source_url": "https://example.invalid/post/1",
                "municipality": "Metepec",
                "asking_price": 3500000,
                "housing_program_references": ["Infonavit"],
            },
            self.source,
        )

        self.assertEqual(record["content_id"], "reddit-demo-1")
        self.assertEqual(record["municipality"], "Metepec")
        self.assertEqual(record["asking_price"], 3500000)
        self.assertEqual(record["legal_status"], "manual_review")

    def test_dedupe_keeps_distinct_content_ids(self):
        records = [
            {"content_id": "one", "source_name": "Reddit"},
            {"content_id": "one", "source_name": "Reddit"},
            {"content_id": "two", "source_name": "Reddit"},
        ]
        self.assertEqual(len(dedupe(records)), 2)

    def test_exports_community_csv_headers(self):
        record = normalize_community_record({"post_id": "csv-demo"}, self.source)
        with tempfile.TemporaryDirectory() as directory:
            output = Path(directory) / "community_content.csv"
            export_community_csv([record], str(output))
            contents = output.read_text(encoding="utf-8")
            self.assertIn("content_id", contents.splitlines()[0])
            self.assertIn("csv-demo", contents)


if __name__ == "__main__":
    unittest.main()
