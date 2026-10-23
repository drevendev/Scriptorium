"""Unit and privacy regressions for the #283 evidence-gallery filters."""
import unittest

from scriptorium.site_gallery_filter import (
    evidence_kind, FILTER_JS, FILTER_CSS, FILTER_CONTROLS,
)


class GalleryFilterContractTests(unittest.TestCase):
    def test_mode_classification_is_presentation_only(self):
        cases = {
            "frozen_diagnostic": "full_work",
            "comparison": "full_work",
            "provenance": "provenance",
        }
        for mode, expected in cases.items():
            with self.subTest(mode=mode):
                self.assertEqual(
                    evidence_kind({"render_mode": mode, "publication_status": "diagnostic"}),
                    expected,
                )
        self.assertEqual(evidence_kind({"publication_status": "illustrative_excerpt"}), "excerpt")
        self.assertEqual(evidence_kind({"publication_status": "diagnostic"}), "other")
        self.assertEqual(
            evidence_kind({"render_mode": "unknown", "publication_status": "diagnostic"}),
            "other",
        )

    def test_zero_js_fallback_keeps_all_cards_visible(self):
        self.assertIn('id="evidence-filters"', FILTER_CONTROLS)
        self.assertIn("hidden>", FILTER_CONTROLS)
        self.assertIn("panel.hidden = false", FILTER_JS)
        self.assertIn("if (cards.length === 0) return", FILTER_JS)
        self.assertIn(".card[hidden]", FILTER_CSS)

    def test_accessible_controls_and_feedback(self):
        for term in ('type="search"', "<select", 'aria-controls="works"',
                     'role="status"', 'aria-live="polite"',
                     "No evidence pages match", "Clear filters"):
            with self.subTest(term=term):
                self.assertIn(term, FILTER_CONTROLS)
        self.assertIn("min-height: 44px", FILTER_CSS)
        self.assertIn(":focus-visible", FILTER_CSS)

    def test_search_only_title_author_and_russian_normalization(self):
        self.assertNotIn("card.textContent", FILTER_JS)
        self.assertIn("card.querySelector('h2')", FILTER_JS)
        self.assertIn("card.querySelector('h2 + p')", FILTER_JS)
        self.assertIn("normalize('NFC')", FILTER_JS)
        self.assertIn("toLocaleLowerCase('ru-RU')", FILTER_JS)
        self.assertIn("replace(/ё/g, 'е')", FILTER_JS)
        self.assertIn("!titleKnown", FILTER_JS)

    def test_never_uploads_or_tracks_queries(self):
        forbidden = ("fetch(", "XMLHttpRequest", "sendBeacon", "localStorage",
                     "sessionStorage", "document.cookie", "innerHTML =",
                     "navigator.", "window.location")
        for token in forbidden:
            with self.subTest(token=token):
                self.assertNotIn(token, FILTER_JS)
        self.assertIn("status.textContent =", FILTER_JS)


if __name__ == "__main__":
    unittest.main()
