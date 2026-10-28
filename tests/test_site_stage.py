"""Current-stage Reader snapshot is derived from the retained source-free matrix."""
from __future__ import annotations

import copy
import json
from html.parser import HTMLParser
from pathlib import Path
import unittest

from scriptorium import site_benchmark_matrix
from scriptorium.site_stage import STAGE_CSS, render_stage
from scriptorium.site_renderer import _render_index


ROOT = Path(__file__).resolve().parents[1]


class _Tags(HTMLParser):
    def __init__(self, text: str):
        super().__init__()
        self.elements = []
        self.feed(text)

    def handle_starttag(self, tag, attrs):
        self.elements.append((tag, dict(attrs)))


def _real_matrix_entry() -> dict:
    result = site_benchmark_matrix.build(ROOT)
    return dict(site_benchmark_matrix.EXPECTED_ENTRY,
                render_mode="benchmark_matrix", json_data=result["json"])


class StageAtGlanceTests(unittest.TestCase):
    def test_live_source_frozen_evidence_is_derived_not_fabricated(self):
        entry = _real_matrix_entry()
        doc = json.loads(entry["json_data"])
        section = render_stage([entry])
        self.assertIn(">5</strong><span>five-work core: measured books", section)
        self.assertIn(">118</strong><span>five-work core: numeric values", section)
        self.assertIn(">24</strong><span>five-work core: unavailable values", section)
        self.assertIn(">0/5</strong><span>proven FantLab source-matched works", section)
        self.assertIn("Coverage is not parity", section)
        self.assertIn("Resurrection evidence adds 29 more rows", section)
        self.assertIn("unknown", section.lower())
        self.assertIn('href="evidence/fantlab/"', section)
        self.assertIn("24</td><td>5</td><td>Unverified", section)
        self.assertNotIn("source text", section.lower())
        self.assertEqual(section.count("<tr>"), len(doc["entries"]) + 1)
        self.assertEqual(section.count("<th scope=\"row\">"), 5)
        parsed = _Tags(section)
        regions = [attrs for tag, attrs in parsed.elements if attrs.get("class") == "stage-table-scroll"]
        self.assertEqual(len(regions), 1)
        self.assertEqual(regions[0]["tabindex"], "0")
        self.assertIn("stage-table-hint", regions[0]["aria-describedby"])
        self.assertIn("grid-template-columns:repeat(2", STAGE_CSS)
        self.assertIn("@media print", STAGE_CSS)
        home = _render_index([entry])
        self.assertIn('id="stage-title"', home)
        self.assertIn('id="works"', home)

    def test_missing_matrix_does_not_invent_statistics(self):
        self.assertEqual(render_stage([]), "")
        self.assertNotIn("stage-overview", _render_index([]))

    def test_false_parity_or_changed_coverage_fails_closed(self):
        entry = _real_matrix_entry()
        source = json.loads(entry["json_data"])
        for modifier in (
            lambda d: d.update(m2_source_matched_pass_count=1),
            lambda d: d.update(retained_metric_rows=112),
            lambda d: d["entries"][0].update(exact_fantlab_input_identity="MATCHED"),
            lambda d: d["entries"][0].update(metric_rows_with_actual=50),
            lambda d: d["entries"][0]["metric_rows"][0].update(actual="unknown"),
            lambda d: d["entries"][0]["metric_rows"][0].update(display_rounding_evidence="PASS"),
            lambda d: d["entries"][0].update(title="<script>alert(1)</script>"),
        ):
            with self.subTest(modifier=modifier):
                corrupted = copy.deepcopy(source)
                modifier(corrupted)
                changed = dict(entry, json_data=json.dumps(corrupted))
                if corrupted["entries"][0]["title"].startswith("<script>"):
                    text = render_stage([changed])
                    self.assertIn("&lt;script&gt;", text)
                    self.assertNotIn("<script>", text)
                else:
                    with self.assertRaises(ValueError):
                        render_stage([changed])

    def test_invalid_or_duplicate_work_list_is_rejected(self):
        entry = _real_matrix_entry()
        source = json.loads(entry["json_data"])
        source["entries"].append(copy.deepcopy(source["entries"][0]))
        source["works_reported"] += 1
        with self.assertRaisesRegex(ValueError, "duplicated"):
            render_stage([dict(entry, json_data=json.dumps(source))])


if __name__ == "__main__":
    unittest.main()
