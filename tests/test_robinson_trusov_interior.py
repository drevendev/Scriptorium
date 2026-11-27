"""Source-free positive/negative tests for a deliberately incomplete Trusov sample."""
import copy
import json
import unittest

from test_robinson_trusov_content import fixture, mock_query, PRIVATE_SOURCE
from scriptorium.robinson_trusov_interior import measure_interior, InteriorCollector, SEAM_SCHEMA, FIRST, LAST
from scriptorium.robinson_trusov_projection import capture_projection


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


    def test_join_sensitivity_is_source_free_and_gated(self):
        graph, sha = fixture()
        collector = InteriorCollector()
        projection = capture_projection(graph, sha, query=mock_query(graph, self.fake_source),
                                        page_observer=collector.observe)
        baseline = collector.build(graph, sha, projection)
        report = collector.seam_sensitivity(baseline)
        repeated = collector.seam_sensitivity(baseline)
        self.assertEqual(report, repeated)
        self.assertEqual(report["schema_version"], SEAM_SCHEMA)
        self.assertEqual(report["baseline_normalized_sha256"], baseline["normalized_sha256"])
        self.assertEqual(report["source_page_graph_sha256"], sha)
        self.assertEqual(report["baseline_numeric_metrics"], baseline["numeric_metric_count"])
        self.assertEqual(report["scope"], "SYNTHETIC_PAGE_JOIN_SENSITIVITY_ONLY")
        for gate in ("historical_page_join_verified", "complete_literary_body",
                     "corpus_admitted", "m2_parity_admissible", "source_text_committed"):
            self.assertIs(report[gate], False)
        self.assertEqual(
            [v["join_profile"] for v in report["alternatives"]],
            ["direct_concatenation_stress_test",
             "one_space_ProofreadPage_default_hypothesis",
             "two_LF_paragraph_stress_test"],
        )
        self.assertEqual(
            [v["normalized_characters_including_spaces"] for v in report["alternatives"]],
            [baseline["normalized_characters_including_spaces"] - 144,
             baseline["normalized_characters_including_spaces"],
             baseline["normalized_characters_including_spaces"] + 144],
        )
        space = report["alternatives"][1]
        self.assertNotEqual(space["joined_sha256"],
                            baseline["join"]["joined_projected_wikitext_sha256"])
        self.assertNotEqual(space["normalized_sha256"], baseline["normalized_sha256"])
        reference = {r["metric_id"]: r for r in baseline["metric_rows"]}
        for variant in report["alternatives"]:
            self.assertEqual(len(variant["metrics"]), 29)
            self.assertEqual(
                variant["changed_numeric_metrics"],
                sum(r["status"] == "CHANGED" for r in variant["metrics"]),
            )
            for row in variant["metrics"]:
                before = reference[row["metric_id"]]["actual"]
                after = row["alternate_value"]
                expected = after - before if before is not None and after is not None else None
                self.assertEqual(row["delta_from_one_LF"], expected)
                self.assertEqual(row["unit"], reference[row["metric_id"]]["unit"])
        serialized = json.dumps(report, sort_keys=True, ensure_ascii=False)
        self.assertNotIn(PRIVATE_SOURCE, serialized)
        self.assertNotIn("Предложение!", serialized)
        self.assertEqual(len(baseline["metric_rows"]), 29)  # original artifact unchanged

    def test_join_sensitivity_rejects_wrong_baseline_or_incomplete_pages(self):
        graph, sha = fixture()
        collector = InteriorCollector()
        projection = capture_projection(graph, sha, query=mock_query(graph, self.fake_source),
                                        page_observer=collector.observe)
        baseline = collector.build(graph, sha, projection)
        modified = copy.deepcopy(baseline)
        modified["normalized_sha256"] = "0" * 64
        with self.assertRaisesRegex(ValueError, "baseline/source identity"):
            collector.seam_sensitivity(modified)
        # Source hashes alone do not authenticate a supplied metric row.
        # Tampering must fail before the signed alternate deltas are emitted.
        modified = copy.deepcopy(baseline)
        char_row = next(row for row in modified["metric_rows"]
                        if row["metric_id"] == "fantlab.general.characters")
        char_row["actual"] += 1
        with self.assertRaisesRegex(ValueError, "baseline metric drift"):
            collector.seam_sensitivity(modified)
        modified = copy.deepcopy(baseline)
        dictionary_row = next(row for row in modified["metric_rows"]
                              if row["metric_id"] == "fantlab.vocabulary.active_dictionary")
        self.assertIsNone(dictionary_row["actual"])
        dictionary_row["actual"] = 0
        with self.assertRaisesRegex(ValueError, "baseline metric drift"):
            collector.seam_sensitivity(modified)
        modified = copy.deepcopy(baseline)
        modified["metric_rows"][0]["result"] = "MEASURED_INTERIOR_EXCERPT_ONLY"
        # Either changed or unchanged based on the first row; force corruption.
        modified["metric_rows"][0]["unit"] = "fabricated_unit"
        with self.assertRaisesRegex(ValueError, "baseline metric drift"):
            collector.seam_sensitivity(modified)
        modified = copy.deepcopy(baseline)
        modified["numeric_metric_count"] += 1
        with self.assertRaisesRegex(ValueError, "baseline metric replay mismatch"):
            collector.seam_sensitivity(modified)
        modified = copy.deepcopy(baseline)
        modified["gates"]["corpus_admitted_for_calibration"] = True
        with self.assertRaisesRegex(ValueError, "verified incomplete interior"):
            collector.seam_sensitivity(modified)
        collector.selected.pop(42)
        with self.assertRaisesRegex(ValueError, "verified incomplete interior"):
            collector.seam_sensitivity(baseline)


    def test_pinned_folio_variant_changes_one_seam_only(self):
        from scriptorium.robinson_trusov_interior import folio_join_variants
        pages = ["Синтетическая строка."] * 145
        i = 106 - FIRST
        pages[i] = "начало слова пере-\n "
        pages[i + 1] = "\tход. конец"
        literal, omitted, edits = folio_join_variants(pages)
        expected = pages[:i] + ["начало слова пере-ход. конец"] + pages[i + 2:]
        self.assertEqual(literal, "\n".join(expected))
        expected[i] = "начало слова переход. конец"
        self.assertEqual(omitted, "\n".join(expected))
        self.assertEqual(edits, {"left_edge_whitespace_removed": 2,
                                 "right_edge_whitespace_removed": 1,
                                 "synthetic_LF_removed": 1, "ascii_hyphen_removed": 1})
        for left, right in (("пере", "ход"), ("пере--", "ход"), ("пере-", "Ход")):
            invalid = pages.copy()
            invalid[i:i + 2] = [left, right]
            with self.assertRaises(ValueError):
                folio_join_variants(invalid)
        with self.assertRaises(ValueError):
            folio_join_variants(pages[:-1])

    def test_folio_metrics_refuse_missing_proof(self):
        from scriptorium.robinson_trusov_interior import folio_metric_sensitivity
        with self.assertRaisesRegex(ValueError, "unverified pinned folio join evidence"):
            folio_metric_sensitivity(InteriorCollector(), {}, {})

    def test_folio_metric_rows_bind_proof_and_replay_baseline(self):
        from hashlib import sha256
        from scriptorium.robinson_trusov_interior import folio_metric_sensitivity
        from scriptorium.robinson_trusov_missing_folios import PINS
        from scriptorium.metrics import analyze_deterministic_metrics
        from scriptorium.text import normalize_text

        def digest(text):
            return sha256(text.encode("utf-8")).hexdigest()

        collector = InteriorCollector()
        for n in range(FIRST, LAST + 1):
            value = "Синтетическая строка. "
            if n == 106:
                value = "Слово пере- "
            elif n == 107:
                value = "ход. Конец."
            collector.selected[n] = ({"revision_id": PINS.get(n, n)}, value)
        original = "\n".join(collector.selected[n][1] for n in range(FIRST, LAST + 1))
        measured = analyze_deterministic_metrics(original)
        baseline = {"source_page_graph_sha256": "a" * 64,
                    "status": "INCOMPLETE_INTERIOR_EXCERPT_NOT_CORPUS_OR_PARITY",
                    "join": {"joined_projected_wikitext_sha256": digest(original)},
                    "normalized_sha256": digest(normalize_text(original)),
                    "metric_rows": [{"metric_id": k, "actual": m["value"], "unit": m["unit"]}
                                    for k, m in measured["metrics"].items()]}
        proof = {"schema_version": "scriptorium-trusov-missing-folios-v3",
                 "source_page_graph_sha256": "a" * 64, "carrier_revision_id": 5041937,
                 "left_edge_comparison": "SOURCE_LITERAL_CARRIER_OMISSION",
                 "scope_projection_byte_equal": True,
                 "current_render_edge_joins": {"left": {
                     "matches": {"DIRECT": 0, "SPACE": 0, "HYPHEN_OMITTED_DIRECT": 1,
                                 "HYPHEN_OMITTED_SPACE": 0}, "selected": "HYPHEN_OMITTED_DIRECT"}},
                 "pinned_left_hyphen": {"left_revision_id": PINS[106], "right_revision_id": PINS[107],
                     "terminal_ascii_hyphen_count": 1, "raw_before_terminal_noinclude": True,
                     "scoped_retained": True, "projected_retained": True},
                 "pages": [{"page_sequence": n, "revision_id": PINS[n],
                            "projected_sha256": digest(collector.selected[n][1])} for n in sorted(PINS)]}
        result = folio_metric_sensitivity(collector, baseline, proof)
        self.assertEqual(len(result["metric_rows"]), 29)
        chars = next(row for row in result["metric_rows"] if row["metric_id"] == "fantlab.general.characters")
        self.assertEqual((chars["delta_join_only"], chars["delta_hyphen_only"], chars["delta_total"]), (-2, -1, -3))
        self.assertFalse(result["corpus_admitted"])
        self.assertNotIn("Синтетическая", json.dumps(result, ensure_ascii=False))
        broken = copy.deepcopy(proof)
        broken["pages"][0]["projected_sha256"] = "0" * 64
        with self.assertRaisesRegex(ValueError, "receipt/source identity mismatch"):
            folio_metric_sensitivity(collector, baseline, broken)
        broken = copy.deepcopy(baseline)
        next(row for row in broken["metric_rows"] if row["metric_id"] == "fantlab.general.characters")["actual"] += 1
        with self.assertRaisesRegex(ValueError, "baseline drift"):
            folio_metric_sensitivity(collector, broken, proof)


if __name__ == "__main__":
    unittest.main()
