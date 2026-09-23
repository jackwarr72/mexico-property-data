import unittest

from analytics_data import demo_analytics_data
from export_service import (
    concerns_frame,
    discussions_frame,
    export_chart,
    export_csv,
    export_json,
    export_pdf,
    export_xlsx,
    filtered_analytics_frames,
)


class ExportServiceTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.analytics = demo_analytics_data()
        cls.filters = {"date_range": "Last 30 Days", "location": "Metepec", "source": "Reddit", "intent": "Buying", "sentiment": "Negative"}

    def test_csv_is_utf8_and_has_expected_headers(self):
        frame = filtered_analytics_frames(self.analytics)["Discussions"]
        name, content = export_csv(frame, self.filters, "analytics-discussions")
        self.assertTrue(name.endswith(".csv"))
        self.assertTrue(content.startswith(b"\xef\xbb\xbf"))
        self.assertIn("question".encode(), content)
        self.assertIn("Metepec".encode(), content)

    def test_json_contains_filters_and_all_sections(self):
        name, content = export_json(filtered_analytics_frames(self.analytics), self.filters)
        self.assertTrue(name.endswith(".json"))
        self.assertIn(b'"filters"', content)
        self.assertIn(b'"Trending Questions"', content)

    def test_xlsx_has_workbook_sheets(self):
        name, content = export_xlsx(self.analytics, self.filters)
        self.assertTrue(name.endswith(".xlsx"))
        self.assertTrue(content[:2] == b"PK")
        self.assertGreater(len(content), 1000)

    def test_pdf_and_chart_exports_are_non_empty(self):
        pdf_name, pdf_content = export_pdf(self.analytics, self.filters)
        png_name, png_content, png_mime = export_chart(self.analytics, self.filters, "png")
        svg_name, svg_content, svg_mime = export_chart(self.analytics, self.filters, "svg")
        self.assertTrue(pdf_name.endswith(".pdf"))
        self.assertTrue(png_name.endswith(".png"))
        self.assertTrue(svg_name.endswith(".svg"))
        self.assertTrue(pdf_content.startswith(b"%PDF"))
        self.assertTrue(png_content.startswith(b"\x89PNG"))
        self.assertIn(b"<svg", svg_content[:500])
        self.assertEqual(png_mime, "image/png")
        self.assertEqual(svg_mime, "image/svg")

    def test_concerns_include_percentages(self):
        frame = concerns_frame(self.analytics)
        self.assertIn("percentage", frame.columns)
        self.assertAlmostEqual(frame.groupby("intent")["percentage"].sum().loc["buying"], 100)


if __name__ == "__main__":
    unittest.main()
