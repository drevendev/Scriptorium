"""Regression contract for eight source-backed all-book Russian Reader charts."""
from __future__ import annotations
from html.parser import HTMLParser
import json
from pathlib import Path
import shutil
import subprocess
import unittest

ROOT = Path(__file__).resolve().parents[1]
IDS = (
    "fantlab.dialogue.share_percent",
    "fantlab.general.mean_sentence_length_chars",
    "fantlab.punctuation.comma.per_1000_words",
    "fantlab.punctuation.dash.per_1000_words",
    "fantlab.general.mean_word_length_chars",
    "fantlab.dialogue.author_text_inside_dialogue_percent",
    "fantlab.dialogue.mean_dialogue_sentence_length_chars",
    "fantlab.dialogue.mean_narration_sentence_length_chars",
)

class ChartButtons(HTMLParser):
    def __init__(self, html):
        super().__init__()
        self.buttons = []
        self.feed(html)
    def handle_starttag(self, tag, attrs):
        if tag == 'button':
            item = dict(attrs)
            if 'data-chart' in item:
                self.buttons.append(item)

class ExpandedChartTests(unittest.TestCase):
    def test_chart_buttons_and_literary_accessibility(self):
        html = (ROOT / "index.html").read_text(encoding="utf-8")
        buttons = ChartButtons(html).buttons
        self.assertEqual(tuple(x["data-chart"] for x in buttons), IDS)
        self.assertTrue(all("disabled" in x for x in buttons))
        self.assertEqual(sum(x["aria-pressed"] == "true" for x in buttons), 1)
        self.assertIn('id="chart-unit" class="chart-unit" aria-live="polite"', html)
        self.assertIn('<details class="chart-table">', html)
        self.assertIn('id="chart-table-rows"', html)
        self.assertIn('id="chart-table-caption"', html)
        self.assertIn('aria-label="Таблица чисел выбранной диаграммы"', html)
        chart_rows = html.split('<tbody id="chart-table-rows">', 1)[1].split('</tbody>', 1)[0]
        self.assertEqual(chart_rows.count('<tr><th scope="row">'), 7)
        self.assertIn("«Нет данных»", html)

    def test_sort_toggle_accessibility_and_fallback(self):
        html = (ROOT / "index.html").read_text(encoding="utf-8")
        css = (ROOT / "assets/pages-reader.css").read_text(encoding="utf-8")
        js = (ROOT / "assets/pages-reader.js").read_text(encoding="utf-8")
        self.assertIn('id="chart-sort" aria-pressed="false" disabled', html)
        self.assertIn("порядок каталога", html)
        self.assertIn("if (sortChart) rows.sort", js)
        self.assertIn("a.ordinal-b.ordinal", js)
        self.assertIn('chartSortButton.setAttribute("aria-pressed",String(sortChart))', js)
        self.assertIn(".chart-sort button:focus-visible", css)
        self.assertIn(".chart-sort { display:none !important; }", css)

    def test_no_js_table_uses_exact_frozen_values(self):
        """Static fallback must not mislabel rounded values as exact."""
        import re

        html = (ROOT / "index.html").read_text(encoding="utf-8")
        fallback = html.split('<tbody id="chart-table-rows">', 1)[1].split('</tbody>', 1)[0]
        pattern = r'<tr><th scope="row">([^<]+)</th><td>([^<]+)</td><td>%</td></tr>'
        rows = re.findall(pattern, fallback)
        data = json.loads((ROOT / "assets/evidence-snapshot.json").read_text(encoding="utf-8"))
        measured = [b for b in data["books"] if b["text_status"] == "measured"]
        expected = [(b["display_title"], str(next(m["actual"] for m in b["metrics"]
                        if m["id"] == "fantlab.dialogue.share_percent"))) for b in measured]
        self.assertEqual(len(rows), 7)
        self.assertEqual(rows, expected)
        self.assertNotEqual(re.findall(pattern, fallback.replace(
            f"<td>{expected[0][1]}</td>", "<td>34,97</td>", 1)), expected)

    def test_measured_coverage_and_profile_identity(self):
        data = json.loads((ROOT / "assets/evidence-snapshot.json").read_text(encoding="utf-8"))
        books = [b for b in data["books"] if b["text_status"] == "measured"]
        self.assertEqual(len(books), 7)
        keys = ("metrics", "normalization", "dialogue", "punctuation")
        self.assertEqual(len({tuple(b["profiles"][k] for k in keys) for b in books}), 1)
        for metric_id in IDS:
            with self.subTest(metric=metric_id):
                actual = [next((row["actual"] for row in b["metrics"] if row["id"] == metric_id), None) for b in books]
                present = sum(type(v) in (int, float) for v in actual)
                self.assertEqual(present, 6 if metric_id in IDS[-2:] else 7)
                if metric_id in IDS[-2:]: self.assertIsNone(actual[5])  # Beketova translation

    def test_render_fail_closed_and_no_synthetic_zeros(self):
        js = (ROOT / "assets/pages-reader.js").read_text(encoding="utf-8")
        css = (ROOT / "assets/pages-reader.css").read_text(encoding="utf-8")
        self.assertIn('throw Error("Показатель диаграммы не разрешён")', js)
        self.assertIn('row.value===null?"нет данных"', js)
        self.assertIn("row.value!==null", js)
        self.assertIn("book.profiles?.[k]===baseline[k]", js)
        self.assertIn(".chart-row.chart-missing", css)
        self.assertIn(".chart-table summary:focus-visible", css)
        self.assertIn('el("chart-table-rows").replaceChildren(tableNodes)', js)
        self.assertNotIn("innerHTML", js)

    @unittest.skipUnless(shutil.which("node"), "Node unavailable: structural checks still run")
    def test_real_shipped_chart_renderer(self):
        for command in (
            ["node", "--check", str(ROOT / "assets/pages-reader.js")],
            ["node", str(ROOT / "tests/pages_chart_metrics_smoke.cjs")],
        ):
            result = subprocess.run(command, cwd=ROOT, text=True, capture_output=True,
                                    timeout=20, check=False)
            self.assertEqual(result.returncode, 0, result.stdout + result.stderr)

if __name__ == "__main__":
    unittest.main()
