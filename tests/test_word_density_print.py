"""Source-bound Anna case must print tables without clipping scientific evidence."""
from pathlib import Path
import unittest

ROOT = Path(__file__).resolve().parents[1]
MARKER = "/* Print: keep the two source-bound tables readable on portrait paper. */"


class AnnaPrintContractTests(unittest.TestCase):
    def assert_print_contract(self, html: str) -> None:
        self.assertEqual(html.count(MARKER), 1)
        rules = html.split(MARKER, 1)[1].split("\n}\n", 1)[0]
        for required in (
            ".gap-panel { break-inside: auto; page-break-inside: auto; }",
            ".gap-table { overflow: visible; border: 0; }",
            ".gap-table table { min-width: 0; width: 100%; table-layout: fixed; font-size: 9pt; }",
            ".gap-table thead { display: table-header-group; }",
            ".gap-table tr { break-inside: avoid; }",
            ".gap-table th,.gap-table td { color: #000 !important; padding: .3rem .35rem; overflow-wrap: anywhere; }",
            ".probe-hash { overflow-wrap: anywhere; word-break: break-all; }",
        ):
            with self.subTest(rule=required):
                self.assertIn(required, rules)
        self.assertNotIn(".gap-table { display: none", rules)
        self.assertNotIn(".gap-table table { display: none", rules)
        self.assertIn('data-probe="exclude_numeric_only:word_count"', html)
        self.assertIn('data-diagnostic="expected_words"', html)
        self.assertIn("DIAGNOSTIC_ONLY", html)
        self.assertIn('class="probe-hash"', html)
        self.assertIn("при сохранении страницы в PDF", html)

    def test_both_real_number_tables_are_printable(self):
        html = (ROOT / "word-density.html").read_text(encoding="utf-8")
        self.assert_print_contract(html)
        self.assertEqual(html.count('<div class="gap-table" role="region"'), 2)
        # On small screens, keep scrolling; only the print layout removes it.
        self.assertIn(".gap-table{overflow-x:auto", html)

    def test_layout_regressions_fail_closed(self):
        html = (ROOT / "word-density.html").read_text(encoding="utf-8")
        for before, after in (
            ("min-width: 0; width: 100%; table-layout: fixed;",
             "min-width: 610px; width: 100%; table-layout: fixed;"),
            ("break-inside: auto; page-break-inside: auto;",
             "break-inside: avoid; page-break-inside: avoid;"),
            (".gap-table { overflow: visible; border: 0; }",
             ".gap-table { overflow: auto; border: 0; }"),
        ):
            with self.subTest(before=before):
                self.assertIn(before, html)
                altered = html.replace(before, after, 1)
                self.assertNotEqual(altered, html)
                with self.assertRaises(AssertionError):
                    self.assert_print_contract(altered)


if __name__ == "__main__":
    unittest.main()
