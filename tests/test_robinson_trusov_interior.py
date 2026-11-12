"""Source-free positive/negative tests for a deliberately incomplete Trusov sample."""
import copy
import json
import unittest

from test_robinson_trusov_content import fixture, mock_query, PRIVATE_SOURCE
from scriptorium.robinson_trusov_interior import measure_interior, FIRST, LAST


class TrusovInteriorTests(unittest.TestCase):
    @staticmethod
    def fake_source(page):
        n = int(page["title"].rsplit("/", 1)[-1])
        if n == 2:
            source = "{{#if:unknown|first|last}} " + PRIVATE_SOURCE
        elif n in (148, 149, 150, 151):
            source = "{{ВАР|историческое|современное}} " + PRIVATE_SOURCE
        else:
            source = (PRIVATE_SOURCE + ". Предложение!\n") * 3
        page["revisions"][0]["slots"]["main"]["content"] = source

    def test_exact_page_sample_yields_29_explicitly_nonparity_measurements(self):
        graph, graph_sha = fixture()
        report = measure_interior(graph, graph_sha,
                                  query=mock_query(graph, self.fake_source))
        self.assertEqual(report["page_interval"], {
            "from": FIRST, "to": LAST, "count": 145,
            "excluded_pages": [2, 148, 149, 150, 151],
            "opening_truncated": True, "ending_truncated": True,
        })
        self.assertEqual(len(report["metric_rows"]), 29)
        self.assertGreaterEqual(report["numeric_metric_count"], 20)
        self.assertEqual(report["numeric_metric_count"] + report["unavailable_metric_count"], 29)
        self.assertEqual(report["join"]["projected_page_join_seams"], 144)
        self.assertEqual(report["source_page_graph_sha256"], graph_sha)
        self.assertFalse(report["gates"]["corpus_admitted_for_calibration"])
        self.assertFalse(report["gates"]["m2_parity_admissible"])
        self.assertEqual(report["gates"]["full_literary_body"], "NOT_RUN")
        self.assertEqual(report["gates"]["page_join_historical_identity"], "UNKNOWN")
        self.assertEqual(report["normalized_characters_including_spaces"],
                         next(row["actual"] for row in report["metric_rows"]
                              if row["metric_id"] == "fantlab.general.characters"))
        self.assertNotIn(PRIVATE_SOURCE, json.dumps(report, ensure_ascii=False))
        self.assertNotIn("историческое", json.dumps(report, ensure_ascii=False))

    def test_source_replay_and_report_are_deterministic(self):
        graph, sha = fixture()
        a = measure_interior(graph, sha, query=mock_query(graph, self.fake_source))
        b = measure_interior(graph, sha, query=mock_query(graph, self.fake_source))
        self.assertEqual(json.dumps(a, sort_keys=True), json.dumps(b, sort_keys=True))
        self.assertEqual(a["join"]["joined_projected_wikitext_characters_including_spaces"],
                         145 * len((PRIVATE_SOURCE + ". Предложение!\n") * 3) + 144)

    def test_unresolved_interior_template_fails_closed(self):
        graph, sha = fixture()
        def invalid(page):
            self.fake_source(page)
            if page["title"].endswith("/25"):
                page["revisions"][0]["slots"]["main"]["content"] += "\n{{ВАР|old|new}}"
        with self.assertRaisesRegex(ValueError, "interior Page 25 not safely projected"):
            measure_interior(graph, sha, query=mock_query(graph, invalid))

    def test_unrendered_wiki_syntax_fails_closed(self):
        graph, sha = fixture()
        for bad in ("[[link]]", "<ref>note</ref>", "{{nested}}"):
            def invalid(page):
                self.fake_source(page)
                if page["title"].endswith("/42"):
                    page["revisions"][0]["slots"]["main"]["content"] += " " + bad
            with self.subTest(bad=bad), self.assertRaises(ValueError):
                measure_interior(graph, sha, query=mock_query(graph, invalid))

    def test_provider_sha_drift_and_page_coverage_cannot_measure(self):
        graph, sha = fixture()
        def invalid(page):
            self.fake_source(page)
            if page["title"].endswith("/22"):
                page["revisions"][0]["sha1"] = "f" * 40
        with self.assertRaisesRegex(ValueError, "identity drift"):
            measure_interior(graph, sha, query=mock_query(graph, invalid))
        changed = copy.deepcopy(graph)
        changed["selection"]["to"] = 150
        with self.assertRaises(ValueError):
            measure_interior(changed, sha, query=mock_query(changed, self.fake_source))


if __name__ == "__main__":
    unittest.main()
