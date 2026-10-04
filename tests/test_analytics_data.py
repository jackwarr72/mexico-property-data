import unittest
from contextlib import nullcontext
from unittest.mock import patch

import pandas as pd

from analytics_data import (
    AnalyticsDataLoadError,
    build_analytics_from_content,
    demo_analytics_data,
    empty_analytics_data,
    load_analytics_data,
)


class AnalyticsDataTests(unittest.TestCase):
    def test_demo_provider_is_explicitly_marked(self):
        analytics = demo_analytics_data()
        self.assertTrue(analytics.is_demo)
        self.assertEqual(analytics.quick_stats.questions.value, 2847)
        self.assertEqual(len(analytics.trending_questions), 5)
        self.assertFalse(analytics.topic_evolution.empty)

    def test_database_rows_build_non_demo_analytics(self):
        frame = pd.DataFrame(
            [
                {
                    "content_id": "1",
                    "source_name": "Reddit",
                    "municipality": "Metepec",
                    "state": "Estado de Mexico",
                    "title": "Comprar en Metepec",
                    "content": "Pregunta sobre precio",
                    "source_url": "https://example.invalid/1",
                    "published_at": "2026-09-20",
                    "sentiment": "Positive",
                    "extracted_keywords": "[]",
                    "engagement_metrics": "{}",
                }
            ]
        )
        analytics = build_analytics_from_content(frame)
        self.assertFalse(analytics.is_demo)
        self.assertEqual(analytics.quick_stats.questions.value, 1)
        self.assertEqual(analytics.discussions[0].location, "Metepec")

    def test_empty_database_result_is_not_demo_data(self):
        with patch("analytics_data.pd.read_sql_query", return_value=pd.DataFrame()):
            analytics = load_analytics_data(lambda: nullcontext(object()))

        self.assertFalse(analytics.is_demo)
        self.assertEqual(analytics.quick_stats.questions.value, 0)
        self.assertEqual(analytics.trending_questions, [])

    def test_database_failure_is_raised_instead_of_replaced_with_demo_data(self):
        def failing_connection():
            raise OSError("database unavailable")

        with self.assertRaises(AnalyticsDataLoadError) as raised:
            load_analytics_data(failing_connection)

        self.assertIsInstance(raised.exception.__cause__, OSError)

    def test_empty_analytics_data_has_zeroed_metrics(self):
        analytics = empty_analytics_data()

        self.assertFalse(analytics.is_demo)
        self.assertEqual(analytics.quick_stats.sources.value, 0)
        self.assertEqual(analytics.quick_stats.topics.value, 0)


if __name__ == "__main__":
    unittest.main()
