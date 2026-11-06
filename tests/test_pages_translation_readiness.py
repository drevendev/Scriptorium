"""Source-backed Robinson translation-pair readiness without invented measurements."""
from __future__ import annotations

from html.parser import HTMLParser
import json
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


class TranslationReadinessTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.html = (ROOT / "index.html").read_text(encoding="utf-8")
        cls.snapshot = json.loads((ROOT / "assets/evidence-snapshot.json").read_text(encoding="utf-8"))
        cls.trusov = json.loads((TRACES / "defoe-robinson-crusoe-trusov-1775-ru.page-graph.json").read_text(encoding="utf-8"))
        cls.receipt = json.loads((TRACES / "defoe-robinson-crusoe-trusov-1775-ru.page-graph-receipt.json").read_text(encoding="utf-8"))
        cls.measured = json.loads((ROOT / "corpus/candidates/diagnostics/defoe-robinson-crusoe-shishmareva-1935-ru.measured.json").read_text(encoding="utf-8"))

    def test_real_source_records_and_accessible_fallback(self):
        check_panel(self.html, self.snapshot, self.trusov, self.receipt, self.measured)
        self.assertIn('aria-label="Готовность двух переводов Робинзона Крузо"', self.html)
        self.assertIn('id="translation-readiness-title"', self.html)
        css = (ROOT / "assets/pages-reader.css").read_text(encoding="utf-8")
        self.assertIn(".translation-readiness a:focus-visible", css)
        self.assertIn(".translation-readiness table { width:100%; min-width:700px", css)
        self.assertIn("@media print { .translation-readiness", css)

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
