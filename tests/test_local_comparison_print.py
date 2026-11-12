"""Print-contract regression for the *CLI's* standalone local HTML comparison.

The browser-only Comparison Desk has a separate print contract/test; this one
covers the installable Python report generated from two private manuscripts.
Real Chromium/A4 visual acceptance remains separate from structural checks.
"""
from __future__ import annotations

import re
import unittest

from scriptorium import compare
from scriptorium.analyze import build_local_analysis


HEADERS = [
    "Metric", "Left", "Right", "Unit", "Difference",
    "Difference unit", "Status", "Compatibility", "Definition evidence",
]


def print_labels(css: str) -> list[tuple[str, str]]:
    return re.findall(
        r'tbody td:nth-of-type\\((\\d+)\\)::before\\{content:"([^"]+)"\\}', css
    )


class LocalComparisonPrintTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        left = build_local_analysis("Привет, мир!".encode("utf-8"))
        right = build_local_analysis(b"")
        cls.page = compare.render_html(
            compare.build_comparison(left, right), title="Letters < Poems"
        )

    def test_print_cards_label_all_eight_values_of_all_29_rows(self):
        page = self.page
        self.assertEqual(
            re.findall(r"<th scope='col'>([^<]+)</th>", page), HEADERS
        )
        self.assertEqual(len(re.findall(r"<tr><th scope='row'>", page)), 29)
        self.assertEqual(len(re.findall(r"<td>", page)), 29 * 8)
        print_css = page.split("@media print{", 1)[1].split("</style>", 1)[0]
        self.assertEqual(
            print_labels(print_css),
            [(str(i), header) for i, header in enumerate(HEADERS[1:], 1)],
        )
        # A missing or incorrectly numbered label must break this contract.
        broken = print_css.replace(
            'tbody td:nth-of-type(8)::before', 'tbody td:nth-of-type(7)::before'
        )
        self.assertNotEqual(print_labels(broken), print_labels(print_css))

    def test_print_cancels_wide_screen_layout_without_hiding_values(self):
        screen_css, print_css = self.page.split("@media print{", 1)
        self.assertIn("min-width:50rem", screen_css)
        for rule in (
            ".scroll{overflow:visible;border:0}",
            "table,tbody{display:block;width:100%;min-width:0}",
            "thead{display:none}",
            "tbody tr{display:grid;grid-template-columns:repeat(2,minmax(0,1fr))",
            "break-inside:avoid;page-break-inside:avoid",
            "tbody th[scope='row']{grid-column:1 / -1;display:block;min-width:0",
            "tbody td{display:block;min-width:0",
            "overflow-wrap:anywhere",
        ):
            with self.subTest(rule=rule):
                self.assertIn(rule, print_css)
        self.assertNotRegex(print_css, r"tbody (?:tr|th|td)\\{display:none")

    def test_screen_privacy_zero_and_missing_values_unchanged(self):
        page = self.page
        self.assertIn("Letters &lt; Poems", page)
        self.assertNotIn("Привет, мир!", page)
        self.assertIn("<td>0</td>", page)
        self.assertIn("Not available", page)
        self.assertIn("role='region'", page)
        self.assertIn("tabindex='0'", page)
        self.assertIn("29 source-free metric comparisons", page)
        self.assertEqual(
            compare.render_html(
                compare.build_comparison(
                    build_local_analysis("Привет, мир!".encode("utf-8")),
                    build_local_analysis(b""),
                ), title="Letters < Poems",
            ), page,
        )


if __name__ == "__main__":
    unittest.main()
