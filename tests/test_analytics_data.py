import unittest

import pandas as pd

from analytics_data import build_analytics_from_content, demo_analytics_data


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


if __name__ == "__main__":
    unittest.main()
