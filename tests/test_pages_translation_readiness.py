"""Source-backed Robinson translation-pair readiness without invented measurements."""
from __future__ import annotations

from html.parser import HTMLParser
import json
import re
from pathlib import Path
import unittest

ROOT = Path(__file__).resolve().parents[1]
TRACES = ROOT / "corpus/candidates/source-edition-traces"


class ReadinessTable(HTMLParser):
    def __init__(self, document: str):
        super().__init__()
        self.rows: dict[str, dict[str, str | None]] = {}
        self.links: list[str] = []
        self._active: str | None = None
        self.feed(document)

    def handle_starttag(self, tag, attrs):
        a = dict(attrs)
        if tag == "tr" and "data-translation-witness" in a:
            key = a["data-translation-witness"]
            if key in self.rows:
                raise AssertionError("duplicate witness")
            self.rows[key] = a
            self._active = key
        if tag == "a" and self._active:
            self.links.append(a.get("href", ""))

    def handle_endtag(self, tag):
        if tag == "tr":
            self._active = None


def check_panel(html: str, snapshot: dict, trusov: dict, receipt: dict, measured: dict) -> None:
    panel = ReadinessTable(html)
    assert set(panel.rows) == {"shishmareva", "trusov"}
    sh = panel.rows["shishmareva"]
    book = next(b for b in snapshot["books"] if b["key"] == "shishmareva")
    assert sh["data-analysis-status"] == "measured"
    assert int(sh["data-source-revision"]) == book["source_revision_id"] == measured["source"]["revision_id"] == 5634933
    assert int(sh["data-numeric-metrics"]) == book["measured"] == measured["numeric_metric_count"] == 24
    assert int(sh["data-character-count"]) == measured["body"]["characters_including_spaces"] == 572587
    assert book["unavailable"] == measured["unavailable_metric_count"] == 5
    assert book["translator"]["name"] == "Мария Шишмарёва"
    assert measured["gates"]["comparison_with_trusov"] == "NOT_RUN"
    tr = panel.rows["trusov"]
    assert tr["data-analysis-status"] == "unmeasured"
    assert tr["data-candidate-id"] == trusov["candidate_id"] == receipt["candidate_id"]
    assert int(tr["data-carrier-revision"]) == trusov["carrier"]["revision_id"] == receipt["carrier_oldid"] == 5041937
    assert int(tr["data-pages"]) == len(trusov["pages"]) == trusov["selection"]["page_count"] == receipt["page_revision_count"] == 150
    assert trusov["selection"]["from"] == 2 and trusov["selection"]["to"] == 151
    for record in (trusov, receipt):
        assert record["source_text_committed"] is False
        assert record["literary_body_sha256"] is None
        assert record["m2_parity_admissible"] is False
    assert "data-catalog-key=\"trusov\"" not in html
    assert html.count("data-catalog-key=") == snapshot["counts"]["work_count"] == 13
    assert "?book=shishmareva#measurements" in panel.links
    assert any(url.endswith("defoe-robinson-crusoe-trusov-1775-ru.page-graph-receipt.json") for url in panel.links)
    assert "Исторический рендеринг" in html and "NOT_RUN" in html
    assert "французский" in html and "FantLab M2: 0/5" in html



def check_excerpt(html: str, sample: dict) -> None:
    assert sample["page_interval"]["count"] == 145
    assert sample["page_interval"]["excluded_pages"] == [2, 148, 149, 150, 151]
    assert sample["numeric_metric_count"] == 22
    assert sample["unavailable_metric_count"] == 7
    assert sample["gates"]["full_literary_body"] == "NOT_RUN"
    assert sample["gates"]["m2_parity_admissible"] is False
    assert sample["gates"]["corpus_admitted_for_calibration"] is False
    assert 'id="trusov-excerpt"' in html
    assert 'data-coverage="incomplete"' in html
    assert f'data-normalized-sha256="{sample["normalized_sha256"]}"' in html
    ids = (
        "fantlab.general.characters", "fantlab.general.words",
        "scriptorium.general.sentences", "fantlab.general.mean_sentence_length_chars",
        "fantlab.punctuation.comma.per_1000_words",
        "fantlab.punctuation.dash.per_1000_words",
        "fantlab.dialogue.share_percent", "fantlab.vocabulary.active_dictionary",
    )
    rows = re.findall(
        r'<tr data-excerpt-metric="([^"]+)" data-actual="([^"]+)" data-status="([^"]+)">',
        html,
    )
    assert len(rows) == len(ids)
    assert [metric_id for metric_id, _, _ in rows] == list(ids)
    actuals = {row["metric_id"]: row for row in sample["metric_rows"]}
    for metric_id, value, status in rows:
        expected = actuals[metric_id]
        assert status == expected["result"]
        assert (value == "unknown" if expected["actual"] is None
                else float(value) == float(expected["actual"]))
    assert "303 882" in html and "22 / 29" in html and "7 / 29" in html
    assert "не полный перевод" in html
    assert "В корпус не принят" in html and "M2: 0/5" in html
    assert "href=\"./metrics.html\"" in html
    assert "interior-measured.json" in html
    assert "data-catalog-key=\"trusov\"" not in html


class TranslationReadinessTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.html = (ROOT / "index.html").read_text(encoding="utf-8")
        cls.snapshot = json.loads((ROOT / "assets/evidence-snapshot.json").read_text(encoding="utf-8"))
        cls.trusov = json.loads((TRACES / "defoe-robinson-crusoe-trusov-1775-ru.page-graph.json").read_text(encoding="utf-8"))
        cls.receipt = json.loads((TRACES / "defoe-robinson-crusoe-trusov-1775-ru.page-graph-receipt.json").read_text(encoding="utf-8"))
        cls.measured = json.loads((ROOT / "corpus/candidates/diagnostics/defoe-robinson-crusoe-shishmareva-1935-ru.measured.json").read_text(encoding="utf-8"))
        cls.excerpt = json.loads((ROOT / "corpus/candidates/diagnostics/defoe-robinson-crusoe-trusov-1775-ru.interior-measured.json").read_text(encoding="utf-8"))

    def test_real_source_records_and_accessible_fallback(self):
        check_panel(self.html, self.snapshot, self.trusov, self.receipt, self.measured)
        self.assertIn('aria-label="Готовность двух переводов Робинзона Крузо"', self.html)
        self.assertIn('id="translation-readiness-title"', self.html)
        css = (ROOT / "assets/pages-reader.css").read_text(encoding="utf-8")
        self.assertIn(".translation-readiness a:focus-visible", css)
        self.assertIn(".translation-readiness table { width:100%; min-width:700px", css)
        self.assertIn("@media print { .translation-readiness", css)

    def test_real_partial_sample_is_source_bound_and_not_a_twelfth_book(self):
        check_excerpt(self.html, self.excerpt)
        css = (ROOT / "assets/pages-reader.css").read_text(encoding="utf-8")
        assert ".translation-excerpt .table-region:focus-visible" in css
        assert "@media (max-width:560px)" in css
        assert "@media print { .translation-excerpt" in css
        readme = (ROOT / "README.md").read_text(encoding="utf-8")
        assert "303,882 characters including spaces" in readme
        assert "/#trusov-excerpt" in readme

    def test_excerpt_refuses_tampered_metrics_or_false_full_body(self):
        check_excerpt(self.html, self.excerpt)
        for altered in (
            self.html.replace('data-actual="303882"', 'data-actual="303883"'),
            self.html.replace('data-status="NOT_RUN_DICTIONARY_UNBOUND"',
                              'data-status="MEASURED_INTERIOR_EXCERPT_ONLY"'),
            self.html.replace('data-coverage="incomplete"', 'data-coverage="complete"'),
            self.html.replace('data-normalized-sha256="', 'data-normalized-sha256="0'),
        ):
            with self.subTest(altered=altered[:75]), self.assertRaises(AssertionError):
                check_excerpt(altered, self.excerpt)

    def test_tampered_counts_and_false_second_measurement_fail(self):
        for old, new in (
            ('data-pages="150"', 'data-pages="151"'),
            ('data-analysis-status="unmeasured"', 'data-analysis-status="measured"'),
            ('data-source-revision="5634933"', 'data-source-revision="5634934"'),
            ('data-numeric-metrics="24"', 'data-numeric-metrics="29"'),
        ):
            with self.subTest(new=new), self.assertRaises(AssertionError):
                check_panel(self.html.replace(old, new), self.snapshot,
                            self.trusov, self.receipt, self.measured)


if __name__ == "__main__":
    unittest.main()
