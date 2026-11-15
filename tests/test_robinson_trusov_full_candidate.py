"""Full Trusov projected-candidate gating: 150 Pages or no full metric."""
import copy
import json
import unittest

from test_robinson_trusov_content import fixture, mock_query, PRIVATE_SOURCE
from scriptorium.robinson_trusov_full_candidate import (
    BLOCKED, READY, FullCandidateCollector, measure_full_candidate,
)
from scriptorium.robinson_trusov_projection import capture_projection


class TrusovFullCandidateTests(unittest.TestCase):
    @staticmethod
    def safe_page(page):
        # Deliberately synthetic, no public historical text.
        page["revisions"][0]["slots"]["main"]["content"] = (
            PRIVATE_SOURCE + ". Тестовое предложение! "
        ) * 60

    @staticmethod
    def blocked_edges(page):
        n = int(page["title"].rsplit("/", 1)[-1])
        if n == 2:
            text = "{{#if:unknown|before|after}}" + PRIVATE_SOURCE
        elif n in (148, 149, 150, 151):
            text = "{{ВАР|до|после}}" + PRIVATE_SOURCE
        else:
            text = (PRIVATE_SOURCE + " проверка! ") * 60
        page["revisions"][0]["slots"]["main"]["content"] = text

    def test_150_safe_pages_compute_inferred_metrics_but_never_admit_book(self):
        graph, digest = fixture()
        report = measure_full_candidate(
            graph, digest, query=mock_query(graph, self.safe_page))
        self.assertEqual(report["status"], READY)
        self.assertEqual(report["page_interval"], {"from": 2, "to": 151, "count": 150})
        self.assertEqual(report["blocked_pages"], [])
        self.assertEqual(report["projected_join"]["projected_page_join_seams"], 149)
        self.assertGreaterEqual(report["normalized_characters_including_spaces"], 300_000)
        self.assertEqual(len(report["metric_rows"]), 29)
        self.assertEqual(report["numeric_metric_count"] + report["unavailable_metric_count"], 29)
        self.assertEqual(
            next(r["actual"] for r in report["metric_rows"]
                 if r["metric_id"] == "fantlab.general.characters"),
            report["normalized_characters_including_spaces"])
        self.assertTrue(all(r["fantlab_display"] is None for r in report["metric_rows"]))
        self.assertFalse(report["gates"]["corpus_admitted_for_calibration"])
        self.assertFalse(report["gates"]["m2_parity_admissible"])
        self.assertEqual(report["gates"]["historical_page_join_identity"], "UNKNOWN")
        self.assertEqual(report["gates"]["full_literary_body"], "NOT_VERIFIED")
        self.assertNotIn(PRIVATE_SOURCE, json.dumps(report, ensure_ascii=False))

    def test_realistic_five_bad_edges_block_all_full_metrics(self):
        graph, digest = fixture()
        report = measure_full_candidate(
            graph, digest, query=mock_query(graph, self.blocked_edges))
        self.assertEqual(report["status"], BLOCKED)
        self.assertEqual([r["page_sequence"] for r in report["blocked_pages"]],
                         [2, 148, 149, 150, 151])
        self.assertTrue(all(r["unresolved_invocations"] > 0
                            for r in report["blocked_pages"]))
        for key in ("metric_rows", "numeric_metric_count", "unavailable_metric_count",
                    "normalized_sha256", "normalized_characters_including_spaces",
                    "projected_join", "scriptorium"):
            self.assertIsNone(report[key], key)
        self.assertEqual(report["gates"]["full_literary_body"], "NOT_VERIFIED")
        self.assertFalse(report["gates"]["author_profile_admissible"])
        self.assertNotIn(PRIVATE_SOURCE, json.dumps(report, ensure_ascii=False))
        self.assertNotIn("до", json.dumps(report, ensure_ascii=False))
        # A branch preview is not a verified historic rendering.
        self.assertEqual(report["blocked_pages"][0]["unresolved_non_var_invocations"], 1)
        self.assertEqual(report["blocked_pages"][0]["var_preview_only_invocations"], 0)
        for page in report["blocked_pages"][1:]:
            self.assertEqual(page["unresolved_non_var_invocations"], 0)
            self.assertEqual(page["var_preview_only_invocations"], 1)
            self.assertEqual(page["var_preview_refusals"], {})

    def test_blocked_page_reasons_distinguish_limits_and_unsupported_shapes(self):
        graph, digest = fixture()

        def different_call_forms(page):
            self.safe_page(page)
            number = int(page["title"].rsplit("/", 1)[-1])
            if number == 2:
                call = "{{#if:condition|left|right}}"
            elif number == 148:
                call = "{{ВАР|" + "\n".join(["old"] * 14) + "|new}}"
            elif number == 151:
                call = "{{ВАР|old|new|extra}}"
            elif number in (149, 150):
                call = "{{ВАР|old|new}}"
            else:
                return
            page["revisions"][0]["slots"]["main"]["content"] = (
                call + PRIVATE_SOURCE
            )

        report = measure_full_candidate(
            graph, digest, query=mock_query(graph, different_call_forms))
        self.assertEqual(report["status"], BLOCKED)
        pages = {row["page_sequence"]: row for row in report["blocked_pages"]}
        self.assertEqual(set(pages), {2, 148, 149, 150, 151})
        self.assertEqual(pages[2]["unresolved_non_var_invocations"], 1)
        self.assertEqual(pages[148]["var_preview_refusals"],
                         {"too_many_line_breaks": 1})
        self.assertEqual(pages[151]["var_preview_refusals"],
                         {"extra_arguments": 1})
        self.assertEqual(pages[149]["var_preview_only_invocations"], 1)
        self.assertEqual(pages[150]["var_preview_only_invocations"], 1)
        self.assertIsNone(report["metric_rows"])
        self.assertNotIn(PRIVATE_SOURCE, json.dumps(report, ensure_ascii=False))

    def test_blocked_projection_classification_tamper_fails_closed(self):
        graph, digest = fixture()
        collector = FullCandidateCollector()
        projection = capture_projection(
            graph, digest, query=mock_query(graph, self.blocked_edges),
            page_observer=collector.observe)
        corrupted = copy.deepcopy(projection)
        blocked = next(row for row in corrupted["pages"]
                       if row["page_sequence"] == 148)
        blocked["flat_var_preview_count"] += 2
        with self.assertRaisesRegex(ValueError, "VAR classification drift"):
            collector.build(graph, digest, corrupted)
        corrupted = copy.deepcopy(projection)
        blocked = next(row for row in corrupted["pages"]
                       if row["page_sequence"] == 148)
        blocked["var_preview_refusal_reasons"]["extra_arguments"] = -1
        with self.assertRaisesRegex(ValueError, "invalid VAR classification"):
            collector.build(graph, digest, corrupted)

    def test_malformed_markup_and_tampered_identity_fail_closed(self):
        graph, digest = fixture()
        def bad_markup(page):
            self.safe_page(page)
            if page["title"].endswith("/29"):
                page["revisions"][0]["slots"]["main"]["content"] += "[[unrendered]]"
        report = measure_full_candidate(
            graph, digest, query=mock_query(graph, bad_markup))
        self.assertEqual(report["status"], BLOCKED)
        self.assertEqual([b["page_sequence"] for b in report["blocked_pages"]], [29])
        self.assertTrue(report["blocked_pages"][0]["unrendered_markup"])
        self.assertIsNone(report["metric_rows"])

        def bad_sha(page):
            self.safe_page(page)
            if page["title"].endswith("/22"):
                page["revisions"][0]["sha1"] = "f" * 40
        with self.assertRaisesRegex(ValueError, "identity drift"):
            measure_full_candidate(graph, digest, query=mock_query(graph, bad_sha))

    def test_all_safe_join_rejects_forged_aggregate_receipt(self):
        # Even when all 150 individual Page digests are correct, a forged
        # aggregate join digest, count, seam count or policy must fail closed.
        graph, digest = fixture()
        collector = FullCandidateCollector()
        projection = capture_projection(
            graph, digest, query=mock_query(graph, self.safe_page),
            page_observer=collector.observe)
        self.assertEqual(collector.build(graph, digest, projection)["status"], READY)
        corruptions = {
            "joined_projected_wikitext_sha256": "0" * 64,
            "joined_projected_wikitext_characters_including_spaces":
                projection["joined_projected_wikitext_characters_including_spaces"] + 1,
            "projected_page_join_seams": 150,
            "alphabetic_page_edge_seams":
                projection["alphabetic_page_edge_seams"] + 1,
            "projected_page_join_profile": "different_join_policy",
        }
        for key, fake in corruptions.items():
            with self.subTest(field=key):
                altered = copy.deepcopy(projection)
                altered[key] = fake
                with self.assertRaisesRegex(ValueError, "projection receipt drift"):
                    collector.build(graph, digest, altered)

    def test_observation_coverage_and_projection_tampering_do_not_measure(self):
        graph, digest = fixture()
        collector = FullCandidateCollector()
        projection = capture_projection(
            graph, digest, query=mock_query(graph, self.blocked_edges),
            page_observer=collector.observe)
        altered = copy.deepcopy(projection)
        altered["pages"][0]["revision_id"] += 1
        with self.assertRaisesRegex(ValueError, "identity drift"):
            collector.build(graph, digest, altered)
        collector.safe.pop(30)
        with self.assertRaisesRegex(ValueError, "incomplete/mismatched"):
            collector.build(graph, digest, projection)


if __name__ == "__main__":
    unittest.main()
