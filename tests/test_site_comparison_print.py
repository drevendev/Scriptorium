"""Print/readability contract for the private comparison, without an external browser.

The browser/print visual route is separately verified when executable.
"""
from __future__ import annotations

import re
import unittest

from scriptorium import site_browser_compare


class BrowserComparisonPrintTests(unittest.TestCase):
    def test_print_cards_preserve_every_comparison_field(self):
        expected = [
            "Metric", "Left", "Right", "Unit", "Difference",
            "Difference unit", "Status", "Reason",
        ]
        screen_headers = re.findall(
            r'<th scope="col">([^<]+)</th>', site_browser_compare.BODY
        )
        self.assertEqual(screen_headers, expected)
        print_css = site_browser_compare.CSS.split("@media print {", 1)[1]
        labels = re.findall(
            r'\.private-desk tbody td:nth-of-type\((\d+)\)::before\s*'
            r'\{\s*content:\s*"([^"]+)";\s*\}', print_css
        )
        self.assertEqual(
            labels, [(str(i), label) for i, label in enumerate(expected[1:], 1)]
        )
        self.assertIn('id="comparison-rows"', site_browser_compare.BODY)

    def test_print_layout_overrides_screen_min_width_and_scroll_clipping(self):
        css = site_browser_compare.CSS
        screen, print_css = css.split("@media print {", 1)
        self.assertIn(".private-desk table { min-width: 64rem; }", screen)
        self.assertIn(".private-desk th:first-child { min-width: 17rem; }", screen)
        for rule in (
            ".private-desk .table-wrap { overflow: visible; border: 0; }",
            ".private-desk table, .private-desk tbody { display: block; width: 100%; min-width: 0; }",
            ".private-desk thead { display: none; }",
            "grid-template-columns: repeat(2, minmax(0, 1fr))",
            ".private-desk tbody th, .private-desk tbody th:first-child {",
            "grid-column: 1 / -1; min-width: 0;",
            "break-inside: avoid;",
            "overflow-wrap: anywhere;",
        ):
            with self.subTest(rule=rule):
                self.assertIn(rule, print_css)
        # Hide redundant print column headers, never the values, row titles or reasons.
        self.assertNotRegex(
            print_css,
            r"\.private-desk tbody\s+(?:th|td|tr)\s*\{\s*display:\s*none",
        )

    def test_print_only_does_not_change_privacy_or_screen_accessibility(self):
        css = site_browser_compare.CSS
        self.assertEqual(css.count("@media print {"), 1)
        self.assertIn('role="region"', site_browser_compare.BODY)
        self.assertIn('tabindex="0"', site_browser_compare.BODY)
        self.assertIn('role="status"', site_browser_compare.BODY)
        self.assertIn('scope="col"', site_browser_compare.BODY)
        self.assertIn('aria-label="29 report measurements"', site_browser_compare.BODY)
        self.assertIn("min-height: 44px", css)
        self.assertIn("@media(max-width:720px)", css)


if __name__ == "__main__":
    unittest.main()
