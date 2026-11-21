"""Accessible offline N-comparison page: faithful data and adversarial rendering."""
from __future__ import annotations

import contextlib
import copy
from html.parser import HTMLParser
from io import StringIO
from pathlib import Path
import tempfile
import unittest

from scriptorium import cli
from scriptorium.native_n_crosswork_cli import build_crosswork_report, render_crosswork_report

ROOT = Path(__file__).resolve().parents[1]


class _PageStructure(HTMLParser):
    def __init__(self):
        super().__init__()
        self.tags = []
        self.links = []
        self.languages = []

    def handle_starttag(self, tag, attrs):
        self.tags.append((tag, dict(attrs)))
        attributes = dict(attrs)
        if tag == "a":
            self.links.append(attributes.get("href"))
        if tag == "html":
            self.languages.append(attributes.get("lang"))


class NativeNCrossworkHTMLTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.report = build_crosswork_report(ROOT)

    def test_readable_source_bound_and_semantically_accessible(self):
        html = render_crosswork_report(self.report, "html")
        self.assertEqual(html, render_crosswork_report(self.report, "html"))
        self.assertIn("<!doctype html>", html)
        self.assertIn("M2: 0/5", html)
        self.assertIn("Неопределённость N", html)
        self.assertIn("Анна Каренина", html)
        self.assertIn("Воскресение", html)
        self.assertIn("+2.84", html)
        self.assertIn("+2.56", html)
        self.assertIn("55\u202f081", html)
        self.assertIn("31\u202f708", html)
        self.assertIn("269\u202f358", html)
        self.assertIn("136\u202f129", html)
        self.assertIn("aria-hidden=\"true\"", html)
        self.assertNotIn("<script", html)
        self.assertNotIn("normalized_text", html)
        self.assertNotIn("private manuscript", html)
        parser = _PageStructure()
        parser.feed(html)
        self.assertEqual(parser.languages, ["ru"])
        self.assertEqual(sum(tag == "tr" for tag, _ in parser.tags), 4)
        self.assertEqual(sum(attrs.get("scope") == "row" for _, attrs in parser.tags), 3)
        self.assertTrue(any(tag == "caption" for tag, _ in parser.tags))
        self.assertEqual(
            parser.links,
            [work["native_workflow"] for work in self.report["works"]],
        )
        for work in self.report["works"]:
            for name in ("candidate_id", "normalized_sha256", "runtime_analysis_sha256"):
                self.assertIn(work[name], html)

    def test_escaped_content_and_strict_scientific_boundary(self):
        edited = copy.deepcopy(self.report)
        edited["works"][0]["title"] = '<script>alert("bad")</script>'
        output = render_crosswork_report(edited, "html")
        self.assertIn("&lt;script&gt;", output)
        self.assertNotIn("<script", output)
        for change in (
            lambda x: x.update(m2_parity_admissible=True),
            lambda x: x.update(source_text_included=True),
            lambda x: x["works"][1].update(native_workflow="javascript:alert(1)"),
            lambda x: x["works"][0].update(normalized_sha256="0" * 63),
            lambda x: x["rows"][0].update(anna_count=True),
            lambda x: x["rows"][0].update(anna_percent_of_word_tokens=float("nan")),
            lambda x: x["rows"][1].update(resurrection_minus_anna_percentage_points=99),
            lambda x: x["rows"][2].update(anna_count=1),
        ):
            broken = copy.deepcopy(self.report)
            change(broken)
            with self.subTest(change=change):
                with self.assertRaises(ValueError):
                    render_crosswork_report(broken, "html")

    def test_cli_html_create_only(self):
        with tempfile.TemporaryDirectory() as temp:
            target = Path(temp) / "n-comparison.html"
            with contextlib.redirect_stdout(StringIO()) as printed:
                self.assertEqual(cli.main([
                    "n-compare", "--root", str(ROOT),
                    "--format", "html", "--output", str(target),
                ]), 0)
            self.assertEqual(printed.getvalue(), "")
            original = target.read_text(encoding="utf-8")
            self.assertIn("<html lang=\"ru\">", original)
            with contextlib.redirect_stderr(StringIO()) as errors:
                with self.assertRaises(SystemExit) as raised:
                    cli.main([
                        "n-compare", "--root", str(ROOT),
                        "--format", "html", "--output", str(target),
                    ])
            self.assertEqual(raised.exception.code, 2)
            self.assertIn("already exists", errors.getvalue())
            self.assertEqual(target.read_text(encoding="utf-8"), original)


if __name__ == "__main__":
    unittest.main()
