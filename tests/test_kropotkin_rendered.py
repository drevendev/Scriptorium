import json
import unittest
from unittest.mock import patch

from scriptorium import kropotkin_rendered as k


class RenderedCandidateTests(unittest.TestCase):
    def test_body_and_notes_separate(self):
        html = ('<div><p>Navigation</p><div class="prp-pages-output">'
                '<p>Первая <i>строка</i><sup class="reference">[1]</sup>.</p>'
                '<span class="pagenum">12</span><p>Вторая&nbsp;строка.</p></div>'
                '<ol class="references"><li id="cite_note-1">'
                '<span class="mw-cite-backlink">↑</span>Авторское примечание.</li></ol>'
                '<p>Rights notice</p></div>')
        self.assertEqual(k.extract(html), ("RENDERED_CANDIDATE",
                         "Первая строка.\nВторая строка.", "Авторское примечание.", 1))

    def test_missing_multiple_empty_and_broken(self):
        cases = [("<p>outside</p>", "BODY_CONTAINER_COUNT"),
                 ('<div class="prp-pages-output"></div>', "EMPTY_BODY"),
                 ('<div class="prp-pages-output">a</div><div class="prp-pages-output">b</div>',
                  "BODY_CONTAINER_COUNT"),
                 ('<div class="prp-pages-output"><p>broken</div>', "UNBALANCED_HTML")]
        for html, status in cases:
            with self.subTest(status=status):
                self.assertEqual(k.extract(html)[:3], (status, None, None))

    def test_capture_counts_drift_and_privacy(self):
        title = "Fixture"
        selectors = {"routes": [{"title": title, "revision_id": 1,
                      "literal_page_selectors": [{"status": "LITERAL_CANDIDATE",
                                                 "candidate_scan_pages": [5, 6]}]}]}
        def query(params):
            self.assertEqual(params["oldid"], "1")
            return {"parse": {"title": title, "revid": 1,
                    "text": '<div class="prp-pages-output"><p>Private prose</p></div>',
                    "templates": [{"ns": 104, "title": f"Страница:{k.SCAN}/5"},
                                  {"ns": 104, "title": f"Страница:{k.SCAN}/7"}]}}
        with patch.object(k, "ROUTES", (title,)), patch.object(k, "REVISION_IDS", (1,)):
            report = k.capture(selectors, query)
            self.assertEqual(report["extracted_route_count"], 1)
            self.assertEqual(report["candidate_composite_characters"], 13)
            self.assertFalse(report["candidate_meets_size_threshold"])
            self.assertEqual(report["routes"][0]["missing_candidate_scans"], [6])
            self.assertEqual(report["routes"][0]["unexpected_reported_scans"], [7])
            self.assertNotIn("Private prose", json.dumps(report))
            self.assertFalse(report["body_frozen"])
            self.assertFalse(report["m2_parity_admissible"])
            def drift(params):
                result = query(params)
                result["parse"]["revid"] = 2
                return result
            with self.assertRaises(ValueError):
                k.capture(selectors, drift)
            def absent(params):
                result = query(params)
                result["parse"]["text"] = "<p>outside</p>"
                return result
            self.assertIsNone(k.capture(selectors, absent)["candidate_composite_characters"])
