"""Source-free CSV lexical-contrast contract and installed CLI regressions."""
from __future__ import annotations

import contextlib
import csv
import json
from io import StringIO
from pathlib import Path
import tempfile
import unittest

from scriptorium import cli
from scriptorium.lexical_contrast import build_lexical_contrast, render_lexical_contrast


def sample(left="кот " * 8 + "пёс " * 2, right="пёс " * 9 + "кот", **kwargs):
    return build_lexical_contrast(
        left, right, left_edition_id="edition-left",
        right_edition_id="edition-right", **kwargs
    )


def rows(report):
    rendered = render_lexical_contrast(report, "csv")
    parsed = csv.DictReader(StringIO(rendered))
    assert parsed.fieldnames == ["section", "field", "value", "unit"]
    records = {(r["section"], r["field"]): r for r in parsed}
    assert len(records) == len(list(csv.DictReader(StringIO(rendered))))
    return rendered, records


class LexicalContrastCsvTests(unittest.TestCase):
    def test_numeric_units_and_source_identity_are_replayable_without_words(self):
        report = sample()
        rendered, data = rows(report)
        self.assertEqual(data["comparison", "status"]["value"], "COMPARABLE")
        self.assertEqual(data["comparison", "public_release_ready"]["value"], "false")
        self.assertEqual(data["left", "edition_id"]["value"], "edition-left")
        self.assertEqual(data["right", "edition_id"]["value"], "edition-right")
        self.assertEqual(data["left", "normalized_sha256"]["value"],
                         report["left"]["normalized_sha256"])
        self.assertEqual(data["left", "source_text_embedded"]["value"], "false")
        self.assertEqual(data["aggregate", "eligible_form_count"]["value"], "2")
        self.assertEqual(data["aggregate", "eligible_form_count"]["unit"], "forms")
        self.assertEqual(data["aggregate", "left_dominant_token_share_percent"]["unit"],
                         "% of left tokens")
        self.assertEqual(data["aggregate", "jensen_shannon_divergence_bits"]["unit"], "bits (0-1)")
        self.assertIn("private", rendered.lower())
        self.assertNotIn("кот", rendered)
        self.assertNotIn("пёс", rendered)

    def test_token_ratio_csv_is_typed_and_old_v1_artifacts_remain_readable(self):
        report = sample("кот " * 10, "а б " * 10)
        _, data = rows(report)
        self.assertEqual(data["comparison", "length_imbalance_warning"]["value"], "false")
        self.assertEqual(data["comparison", "word_token_ratio_max_over_min"]["value"], "2.0")
        self.assertEqual(data["comparison", "word_token_ratio_max_over_min"]["unit"], "ratio")
        self.assertEqual(data["comparison", "word_token_imbalance_warning"]["value"], "true")
        _, unavailable = rows(sample("", "кот"))
        self.assertEqual(unavailable["comparison", "word_token_ratio_max_over_min"]["value"], "UNKNOWN")
        legacy = {key: value for key, value in report.items()
                  if key not in ("word_token_ratio_max_over_min", "word_token_imbalance_warning")}
        _, old = rows(legacy)
        self.assertNotIn(("comparison", "word_token_ratio_max_over_min"), old)
        with self.assertRaises(ValueError):
            rows({**legacy, "word_token_ratio_max_over_min": 2})
        with self.assertRaises(ValueError):
            rows({**report, "word_token_imbalance_warning": False})

    def test_type_overlap_rows_and_pre_overlap_v1_artifacts(self):
        report = sample("кот кот пёс", "пёс мышь мышь")
        _, data = rows(report)
        self.assertEqual(data["aggregate", "shared_form_count"]["value"], "1")
        self.assertEqual(data["aggregate", "left_only_form_count"]["value"], "1")
        self.assertEqual(data["aggregate", "right_only_form_count"]["value"], "1")
        self.assertEqual(data["aggregate", "type_jaccard_percent"]["value"], "33.333333")
        self.assertEqual(data["aggregate", "type_jaccard_percent"]["unit"], "% of pooled types")
        self.assertEqual(data["method", "type_overlap_profile"]["value"],
                         "scriptorium-lexical-type-overlap-v1")
        _, absent = rows(sample("", "кот"))
        self.assertEqual(absent["aggregate", "type_jaccard_percent"]["value"], "NOT_RUN")
        old = {**report, "method": {
            k: v for k, v in report["method"].items()
            if k not in ("type_overlap_profile", "type_overlap")
        }, "aggregate": {
            k: v for k, v in report["aggregate"].items()
            if k not in ("shared_form_count", "left_only_form_count",
                         "right_only_form_count", "type_jaccard_percent")
        }}
        _, legacy = rows(old)
        self.assertNotIn(("aggregate", "type_jaccard_percent"), legacy)
        self.assertIn("Eligible pooled forms", render_lexical_contrast(old, "html"))
        self.assertNotIn("Type Jaccard similarity", render_lexical_contrast(old, "markdown"))
        for malformed in (
            {**report, "aggregate": {k: v for k, v in report["aggregate"].items()
                                    if k != "right_only_form_count"}},
            {**report, "aggregate": {**report["aggregate"], "shared_form_count": 2}},
            {**report, "aggregate": {**report["aggregate"], "type_jaccard_percent": 120}},
            {**report, "method": {**report["method"], "type_overlap_profile": "forged"}},
        ):
            with self.subTest(malformed=malformed["aggregate"]):
                with self.assertRaises(ValueError):
                    rows(malformed)

    def test_token_overlap_is_versioned_numeric_and_old_reports_still_render(self):
        report = sample("кот " * 9 + "пёс ", "кот " + "пёс " * 9)
        _, data = rows(report)
        self.assertEqual(data["aggregate", "token_distribution_overlap_percent"]["value"], "20.0")
        self.assertEqual(data["aggregate", "token_distribution_overlap_percent"]["unit"],
                         "% of token mass")
        self.assertEqual(data["method", "token_overlap_profile"]["value"],
                         "scriptorium-lexical-token-overlap-v1")
        _, unavailable = rows(sample("", "кот"))
        self.assertEqual(unavailable["aggregate", "token_distribution_overlap_percent"]["value"],
                         "NOT_RUN")
        legacy = {**report, "method": {
            k: v for k, v in report["method"].items()
            if k not in ("token_overlap_profile", "token_overlap")
        }, "aggregate": {
            k: v for k, v in report["aggregate"].items()
            if k != "token_distribution_overlap_percent"
        }}
        _, older = rows(legacy)
        self.assertNotIn(("aggregate", "token_distribution_overlap_percent"), older)
        self.assertNotIn("Token-distribution overlap", render_lexical_contrast(legacy, "html"))
        self.assertNotIn("Token-distribution overlap", render_lexical_contrast(legacy, "markdown"))
        for forged in (
            {**report, "method": {k: v for k, v in report["method"].items()
                                  if k != "token_overlap"}},
            {**report, "aggregate": {k: v for k, v in report["aggregate"].items()
                                     if k != "token_distribution_overlap_percent"}},
            {**report, "aggregate": {**report["aggregate"],
                                     "token_distribution_overlap_percent": 101}},
            {**report, "aggregate": {**report["aggregate"],
                                     "token_distribution_overlap_percent": "20"}},
        ):
            with self.subTest(forged=forged.get("method")):
                with self.assertRaises(ValueError):
                    rows(forged)
        with self.assertRaises(ValueError):
            render_lexical_contrast({**report, "aggregate": {
                k: v for k, v in report["aggregate"].items()
                if k != "token_distribution_overlap_percent"
            }}, "html")

    def test_unavailable_is_not_zero_and_true_zero_is_preserved(self):
        _, empty = rows(sample("", "кот"))
        self.assertEqual(empty["comparison", "status"]["value"], "NOT_RUN_EMPTY")
        for (section, key), row in empty.items():
            if section == "aggregate":
                self.assertEqual(row["value"], "NOT_RUN", key)
        _, identical = rows(sample("кот " * 6, "КОТ " * 6))
        self.assertEqual(identical["aggregate", "jensen_shannon_divergence_bits"]["value"], "0.0")
        self.assertEqual(identical["aggregate", "left_dominant_form_count"]["value"], "0")

    def test_untrusted_labels_are_quoted_and_formula_neutralized(self):
        report = sample(left_translator="=2+2,evil", right_translator="@SUM(1)")
        rendered, data = rows(report)
        self.assertEqual(data["left", "translator"]["value"], "'=2+2,evil")
        self.assertEqual(data["right", "translator"]["value"], "'@SUM(1)")
        self.assertIn('"\'=2+2,evil"', rendered)
        self.assertEqual(data["left", "metadata_verified"]["value"], "false")
        self.assertEqual(data["right", "original_work_id"]["value"], "UNKNOWN")

    def test_bad_schema_incomplete_rows_and_numeric_spoofs_fail_closed(self):
        original = sample()
        for report in (
            {**original, "schema_version": "forged"},
            {**original, "aggregate": {}},
            {**original, "aggregate": {**original["aggregate"],
                                      "jensen_shannon_divergence_bits": float("nan")}},
            {**original, "aggregate": {**original["aggregate"],
                                      "eligible_form_count": "5"}},
            {**original, "aggregate": {**original["aggregate"],
                                      "left_dominant_token_share_percent": 101}},
            {**original, "left": {"edition_id": "a"}},
        ):
            with self.subTest(report=report.get("schema_version")):
                with self.assertRaises(ValueError):
                    render_lexical_contrast(report, "csv")

    def test_human_readable_reports_reject_forged_measurements(self):
        report = sample()
        cases = (
            ("manuscript word in count", {**report, "aggregate": {
                **report["aggregate"], "eligible_form_count": "кот"
            }}),
            ("nonfinite divergence", {**report, "aggregate": {
                **report["aggregate"], "jensen_shannon_divergence_bits": float("nan")
            }}),
            ("impossible percentage", {**report, "aggregate": {
                **report["aggregate"], "token_distribution_overlap_percent": 101
            }}),
            ("inconsistent type totals", {**report, "aggregate": {
                **report["aggregate"],
                "shared_form_count": report["aggregate"]["shared_form_count"] + 1
            }}),
            ("forged method", {**report, "method": {
                **report["method"], "token_overlap_profile": "unreviewed"
            }}),
            ("missing witness", {**report, "left": {"edition_id": "edition-left"}}),
            ("contradictory token warning", {**report,
                "word_token_imbalance_warning": True}),
        )
        from scriptorium.lexical_contrast_html import render_lexical_contrast_html
        for label, forged in cases:
            for kind in ("html", "markdown"):
                with self.subTest(label=label, kind=kind), self.assertRaises(ValueError):
                    render_lexical_contrast(forged, kind)
            with self.subTest(label=label, kind="direct html"), self.assertRaises(ValueError):
                render_lexical_contrast_html(forged)
        for kind in ("html", "markdown"):
            with self.subTest(kind=kind):
                self.assertIn("Token-distribution overlap",
                              render_lexical_contrast(report, kind))
                self.assertIn("NOT_RUN", render_lexical_contrast(sample("", "кот"), kind))


    def test_json_replay_rejects_forged_evidence_and_hidden_source_fields(self):
        report = sample()
        serialized = render_lexical_contrast(report, "json")
        self.assertEqual(json.loads(serialized), report)
        # The verified JSON envelope is byte-identical to the earlier format.
        self.assertEqual(serialized, json.dumps(
            report, ensure_ascii=False, sort_keys=True, indent=2,
            allow_nan=False,
        ) + "\n")

        legacy = {key: value for key, value in report.items()
                  if key not in ("word_token_ratio_max_over_min",
                                 "word_token_imbalance_warning")}
        legacy["method"] = {key: value for key, value in report["method"].items()
                            if key not in ("type_overlap_profile", "type_overlap",
                                           "token_overlap_profile", "token_overlap")}
        legacy["aggregate"] = {key: value for key, value in report["aggregate"].items()
                               if key not in ("shared_form_count", "left_only_form_count",
                                              "right_only_form_count", "type_jaccard_percent",
                                              "token_distribution_overlap_percent")}
        self.assertEqual(json.loads(render_lexical_contrast(legacy, "json")), legacy)
        self.assertIsNone(json.loads(render_lexical_contrast(sample("", "кот"), "json"))[
            "aggregate"])

        for name, forged in (
            ("extra top-level manuscript", {**report, "source_text": "PRIVATE_SOURCE_PASSAGE"}),
            ("extra witness manuscript", {**report, "left": {
                **report["left"], "source_excerpt": "PRIVATE_SOURCE_PASSAGE"
            }}),
            ("forged method description", {**report, "method": {
                **report["method"], "denominator": "PRIVATE_SOURCE_PASSAGE"
            }}),
            ("forged numeric count", {**report, "aggregate": {
                **report["aggregate"], "eligible_form_count": "PRIVATE_SOURCE_PASSAGE"
            }}),
            ("invalid numeric divergence", {**report, "aggregate": {
                **report["aggregate"], "jensen_shannon_divergence_bits": float("nan")
            }}),
            ("inconsistent token warning", {**report, "word_token_imbalance_warning": True}),
            ("partial optional witness", {**report,
                "word_token_ratio_max_over_min": None}),
            ("missing required field", {key: value for key, value in report.items()
                                        if key != "scientific_boundary"}),
        ):
            with self.subTest(case=name), self.assertRaises(ValueError):
                render_lexical_contrast(forged, "json")

    def test_stored_witness_and_fixed_boundaries_fail_closed(self):
        original = sample()
        invalid_witness = (
            ("word token text", "word_tokens", "кот"),
            ("word token string", "word_tokens", "10"),
            ("boolean count", "word_tokens", True),
            ("negative count", "distinct_forms", -1),
            ("impossible distinct count", "distinct_forms", 100),
            ("character count text", "characters_including_spaces", "кот"),
            ("forged true floor", "meets_300000_character_floor", "true"),
            ("forged false floor", "meets_300000_character_floor", True),
            ("embedded manuscript", "source_text_embedded", True),
            ("forged metadata verification", "metadata_verified", True),
            ("non-hex digest", "normalized_sha256", "кот" * 32),
            ("invalid edition", "edition_id", "raw manuscript words"),
            ("invalid language", "language", "ru manuscript"),
            ("bad normalization", "normalization_profile", "unreviewed"),
            ("bad vocabulary", "vocabulary_profile", "unreviewed"),
        )
        from scriptorium.lexical_contrast_html import render_lexical_contrast_html
        for label, key, value in invalid_witness:
            report = {**original, "left": {**original["left"], key: value}}
            for kind in ("html", "markdown", "csv"):
                with self.subTest(case=label, kind=kind), self.assertRaises(ValueError):
                    render_lexical_contrast(report, kind)
            with self.subTest(case=label, kind="direct html"), self.assertRaises(ValueError):
                render_lexical_contrast_html(report)

        for field, value in (
            ("length_ratio_max_over_min", " кот"),
            ("length_imbalance_warning", True),
            ("word_token_ratio_max_over_min", 999),
            ("profile", "unreviewed"),
            ("public_release_ready", True),
            ("corpus_admission", "ADMITTED"),
        ):
            with self.subTest(field=field), self.assertRaises(ValueError):
                render_lexical_contrast({**original, field: value}, "html")

        # Prior v1 reports without either optional overlap family or token
        # imbalance metadata remain renderable, with the same CSV bytes.
        legacy = {key: value for key, value in original.items()
                  if key not in ("word_token_ratio_max_over_min", "word_token_imbalance_warning")}
        legacy["method"] = {k: v for k, v in original["method"].items()
                            if k not in ("type_overlap_profile", "type_overlap",
                                         "token_overlap_profile", "token_overlap")}
        legacy["aggregate"] = {k: v for k, v in original["aggregate"].items()
                               if k not in ("shared_form_count", "left_only_form_count",
                                            "right_only_form_count", "type_jaccard_percent",
                                            "token_distribution_overlap_percent")}
        baseline, _ = rows(legacy)
        self.assertIn("Edition ID", render_lexical_contrast(legacy, "html"))
        self.assertIn("Eligible shared-pool types", render_lexical_contrast(legacy, "markdown"))
        self.assertEqual(baseline, render_lexical_contrast(legacy, "csv"))

    def test_stored_method_metadata_cannot_inject_unreviewed_text(self):
        from scriptorium.lexical_contrast_html import render_lexical_contrast_html

        report = sample()
        methods = (
            ("forged denominator", {**report["method"],
                                    "denominator": "PRIVATE_SOURCE_PASSAGE"}),
            ("forged overlap description", {**report["method"],
                                             "token_overlap": "PRIVATE_SOURCE_PASSAGE"}),
            ("boolean threshold", {**report["method"], "min_pooled_occurrences": True}),
            ("forged dependency", {**report["method"],
                                   "dictionary_dependency": "PRIVATE_SOURCE_PASSAGE"}),
            ("missing base field", {k: v for k, v in report["method"].items()
                                    if k != "divergence"}),
            ("unexpected excerpt", {**report["method"],
                                     "manuscript_excerpt": "PRIVATE_SOURCE_PASSAGE"}),
        )
        for name, method in methods:
            forged = {**report, "method": method}
            for kind in ("csv", "markdown", "html"):
                with self.subTest(name=name, kind=kind), self.assertRaises(ValueError):
                    render_lexical_contrast(forged, kind)
            with self.subTest(name=name, kind="direct html"), self.assertRaises(ValueError):
                render_lexical_contrast_html(forged)

        # Additive overlap method families remain optional for historical v1.
        legacy = {**report, "method": {k: v for k, v in report["method"].items()
                  if k not in ("type_overlap_profile", "type_overlap",
                               "token_overlap_profile", "token_overlap")}}
        legacy["aggregate"] = {k: v for k, v in report["aggregate"].items()
                               if k not in ("shared_form_count", "left_only_form_count",
                                            "right_only_form_count", "type_jaccard_percent",
                                            "token_distribution_overlap_percent")}
        for kind in ("csv", "markdown", "html"):
            with self.subTest(kind=kind):
                self.assertTrue(render_lexical_contrast(legacy, kind))

    def test_stored_status_and_disclaimer_must_match_measurement_evidence(self):
        from scriptorium.lexical_contrast_html import render_lexical_contrast_html

        measured = sample()
        empty = sample("", "кот")
        cross_language = sample(right_language="en")
        bad_lineage = sample(left_original_work_id="first", right_original_work_id="second",
                             translation_pair=True)
        identical = sample("кот " * 6, "кот " * 6)
        self.assertEqual(empty["status"], "NOT_RUN_EMPTY")
        self.assertEqual(cross_language["status"], "INCOMPARABLE_LANGUAGE")
        self.assertEqual(bad_lineage["status"], "INCOMPARABLE_TRANSLATION_LINEAGE")
        self.assertEqual(identical["status"], "IDENTICAL_NORMALIZED_TEXT")
        legacy = {key: value for key, value in measured.items()
                  if key not in ("word_token_ratio_max_over_min",
                                 "word_token_imbalance_warning")}
        legacy["method"] = {key: value for key, value in measured["method"].items()
                            if key not in ("type_overlap_profile", "type_overlap",
                                           "token_overlap_profile", "token_overlap")}
        legacy["aggregate"] = {key: value for key, value in measured["aggregate"].items()
                               if key not in ("shared_form_count", "left_only_form_count",
                                              "right_only_form_count", "type_jaccard_percent",
                                              "token_distribution_overlap_percent")}
        baseline_csv, _ = rows(measured)
        for name, report in (("measured", measured), ("empty", empty),
                             ("language", cross_language), ("lineage", bad_lineage),
                             ("identical", identical), ("legacy", legacy)):
            for kind in ("csv", "markdown", "html"):
                with self.subTest(valid=name, kind=kind):
                    self.assertTrue(render_lexical_contrast(report, kind))
            self.assertIn("Lexical contrast", render_lexical_contrast_html(report))
        self.assertEqual(rows(measured)[0], baseline_csv)

        for name, forged in (
            ("status manuscript", {**measured, "status": "PRIVATE_SOURCE_PASSAGE"}),
            ("status non-string", {**measured, "status": True}),
            ("disclaimer manuscript", {**measured,
                "scientific_boundary": "PRIVATE_SOURCE_PASSAGE_SHOULD_NOT_APPEAR"}),
            ("public verification claim", {**measured, "status": "PUBLICLY_VERIFIED"}),
            ("fake no-run", {**measured, "status": "NOT_RUN_EMPTY"}),
            ("fake identical", {**measured, "status": "IDENTICAL_NORMALIZED_TEXT"}),
            ("fake measured empty", {**empty, "status": "COMPARABLE"}),
            ("fake unavailable measured", {**measured, "aggregate": None}),
            ("fake available language", {**cross_language, "status": "COMPARABLE",
                                        "aggregate": measured["aggregate"]}),
            ("fake lineage with matching origin", {**sample(
                left_original_work_id="same", right_original_work_id="same"),
                "status": "INCOMPARABLE_TRANSLATION_LINEAGE", "aggregate": None}),
            ("fake comparison despite lineage", {**bad_lineage,
                "status": "COMPARABLE"}),
            ("conflicting same edition", {**measured, "right": {
                **measured["right"], "edition_id": measured["left"]["edition_id"]}}),
        ):
            for kind in ("csv", "markdown", "html"):
                with self.subTest(forged=name, kind=kind), self.assertRaises(ValueError):
                    render_lexical_contrast(forged, kind)
            with self.subTest(forged=name, kind="direct html"), self.assertRaises(ValueError):
                render_lexical_contrast_html(forged)

    def test_stored_dominance_and_eligible_partitions_fail_closed(self):
        from scriptorium.lexical_contrast_html import render_lexical_contrast_html

        original = sample()
        aggregate = original["aggregate"]
        # Current v1 and pre-overlap legacy v1 both partition eligible types.
        legacy = {**original, "method": {
            key: value for key, value in original["method"].items()
            if key not in ("type_overlap_profile", "type_overlap",
                           "token_overlap_profile", "token_overlap")
        }, "aggregate": {
            key: value for key, value in aggregate.items()
            if key not in ("shared_form_count", "left_only_form_count",
                           "right_only_form_count", "type_jaccard_percent",
                           "token_distribution_overlap_percent")
        }}
        for name, report in (("current", original), ("legacy", legacy)):
            for kind in ("csv", "markdown", "html"):
                with self.subTest(valid=name, format=kind):
                    self.assertTrue(render_lexical_contrast(report, kind))
            self.assertIn("Lexical contrast", render_lexical_contrast_html(report))

        for name, changes in (
            ("dominance exceeds eligible", {
                "left_dominant_form_count": aggregate["eligible_form_count"] + 1
            }),
            ("dominance partition exceeds eligible", {
                "balanced_form_count": aggregate["balanced_form_count"] + 1
            }),
            ("excluded rare count breaks pooled union", {
                "excluded_rare_form_count": aggregate["excluded_rare_form_count"] + 1
            }),
        ):
            forged = {**original, "aggregate": {**aggregate, **changes}}
            for kind in ("csv", "markdown", "html"):
                with self.subTest(forged=name, format=kind), self.assertRaises(ValueError):
                    render_lexical_contrast(forged, kind)
            with self.subTest(forged=name, format="direct_html"), self.assertRaises(ValueError):
                render_lexical_contrast_html(forged)

        # A pre-overlap report must still fail an impossible dominance split.
        forged_legacy = {**legacy, "aggregate": {
            **legacy["aggregate"], "left_dominant_form_count":
                legacy["aggregate"]["eligible_form_count"] + 1
        }}
        with self.assertRaises(ValueError):
            render_lexical_contrast(forged_legacy, "markdown")

    def test_replayed_identical_text_and_zero_dominance_invariants(self):
        from scriptorium.lexical_contrast_html import render_lexical_contrast_html

        identical = sample("кот " * 6, "кот " * 6)
        self.assertEqual(identical["status"], "IDENTICAL_NORMALIZED_TEXT")
        aggregate = identical["aggregate"]
        self.assertEqual(aggregate["jensen_shannon_divergence_bits"], 0)
        self.assertEqual(aggregate["type_jaccard_percent"], 100)
        self.assertEqual(aggregate["token_distribution_overlap_percent"], 100)

        # Historical pre-overlap v1 retains its original measurement contract.
        legacy = {**identical, "method": {
            key: value for key, value in identical["method"].items()
            if key not in ("type_overlap_profile", "type_overlap",
                           "token_overlap_profile", "token_overlap")
        }, "aggregate": {
            key: value for key, value in aggregate.items()
            if key not in ("shared_form_count", "left_only_form_count",
                           "right_only_form_count", "type_jaccard_percent",
                           "token_distribution_overlap_percent")
        }}
        for name, report in (("current", identical), ("legacy", legacy)):
            for kind in ("csv", "markdown", "html"):
                with self.subTest(valid=name, kind=kind):
                    self.assertTrue(render_lexical_contrast(report, kind))
            self.assertIn("Lexical contrast", render_lexical_contrast_html(report))

        # All aggregates below have individually valid numeric types/ranges.
        # Without cross-field invariants they would silently mislead readers.
        altered = (
            ("nonzero identical divergence", {**identical, "aggregate": {
                **aggregate, "jensen_shannon_divergence_bits": 0.5
            }}),
            ("nonzero legacy identical divergence", {**legacy, "aggregate": {
                **legacy["aggregate"], "jensen_shannon_divergence_bits": 0.5
            }}),
            ("nonfull identical token overlap", {**identical, "aggregate": {
                **aggregate, "token_distribution_overlap_percent": 90
            }}),
            # Keep the forged Jaccard and union arithmetic internally consistent:
            # matching digests, not only per-field bounds, make this impossible.
            ("nonfull identical type overlap", {**identical, "aggregate": {
                **aggregate, "shared_form_count": 0,
                "left_only_form_count": 1, "right_only_form_count": 1,
                "type_jaccard_percent": 0, "excluded_rare_form_count": 1
            }}),
            ("nonzero share for absent left class", {**identical, "aggregate": {
                **aggregate, "left_dominant_token_share_percent": 25
            }}),
            ("nonzero share for absent right class", {**identical, "aggregate": {
                **aggregate, "right_dominant_token_share_percent": 25
            }}),
        )

        # Also exercise the zero-form rule independently of identical-text
        # status, with a valid non-identical comparison and intact partitions.
        different = sample("кот " * 6, "пёс " * 6)
        different_aggregate = different["aggregate"]
        self.assertEqual(different["status"], "COMPARABLE")
        for side in ("left", "right"):
            count_key = side + "_dominant_form_count"
            share_key = side + "_dominant_token_share_percent"
            self.assertGreater(different_aggregate[count_key], 0)
            self.assertGreater(different_aggregate[share_key], 0)
            broken = {**different_aggregate, count_key: 0,
                      "balanced_form_count": (
                          different_aggregate["balanced_form_count"] +
                          different_aggregate[count_key]
                      )}
            altered += (("nonidentical absent " + side + " class", {
                **different, "aggregate": broken
            }),)

        for label, report in altered:
            for kind in ("csv", "markdown", "html"):
                with self.subTest(forged=label, kind=kind), self.assertRaises(ValueError):
                    render_lexical_contrast(report, kind)
            with self.subTest(forged=label, kind="direct_html"), self.assertRaises(ValueError):
                render_lexical_contrast_html(report)

    def test_stored_length_ratio_type_and_identical_witness_counts_fail_closed(self):
        from scriptorium.lexical_contrast_html import render_lexical_contrast_html

        original = sample("кот " * 6, "кот " * 6)
        self.assertEqual(original["status"], "IDENTICAL_NORMALIZED_TEXT")
        # Old pre-overlap v1 still renders, even with no optional token ratio.
        legacy = {key: value for key, value in original.items()
                  if key not in ("word_token_ratio_max_over_min",
                                 "word_token_imbalance_warning")}
        legacy["method"] = {key: value for key, value in original["method"].items()
                            if key not in ("type_overlap_profile", "type_overlap",
                                           "token_overlap_profile", "token_overlap")}
        legacy["aggregate"] = {key: value for key, value in original["aggregate"].items()
                               if key not in ("shared_form_count", "left_only_form_count",
                                              "right_only_form_count", "type_jaccard_percent",
                                              "token_distribution_overlap_percent")}
        for name, report in (("current", original), ("legacy", legacy)):
            for kind in ("csv", "markdown", "html"):
                with self.subTest(valid=name, kind=kind):
                    self.assertTrue(render_lexical_contrast(report, kind))
            self.assertIn("Lexical contrast", render_lexical_contrast_html(report))

        forged_reports = [
            ("boolean character ratio", {**original, "length_ratio_max_over_min": True}),
            ("string character ratio", {**original, "length_ratio_max_over_min": "1.0"}),
        ]
        for field in ("characters_including_spaces", "word_tokens", "distinct_forms"):
            changed = {**legacy["right"], field: legacy["right"][field] + 1}
            forged = {**legacy, "right": changed}
            if field == "characters_including_spaces":
                counts = (legacy["left"][field], changed[field])
                forged["length_ratio_max_over_min"] = round(
                    max(counts) / min(counts), 6
                )
            # Legacy format has no word-token ratio or type-overlap fields to
            # catch the contradiction incidentally; SHA identity must catch it.
            forged_reports.append(("identical SHA with forged " + field, forged))

        for name, report in forged_reports:
            for kind in ("csv", "markdown", "html"):
                with self.subTest(forged=name, kind=kind), self.assertRaises(ValueError):
                    render_lexical_contrast(report, kind)
            with self.subTest(forged=name, kind="direct_html"), self.assertRaises(ValueError):
                render_lexical_contrast_html(report)

    def test_cli_offline_csv_and_create_only_destination(self):
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            left, right, destination = (root / n for n in ("left.txt", "right.txt", "contrast.csv"))
            left.write_text("кот " * 8 + "пёс " * 2, encoding="utf-8")
            right.write_text("пёс " * 9 + "кот", encoding="utf-8")
            args = ["distinctives", str(left), str(right), "--left-edition", "edition-left",
                    "--right-edition", "edition-right", "--format", "csv", "--output", str(destination)]
            with contextlib.redirect_stdout(StringIO()):
                self.assertEqual(cli.main(args), 0)
            csv_text = destination.read_text(encoding="utf-8")
            self.assertEqual(rows(sample())[0], csv_text)
            with contextlib.redirect_stderr(StringIO()), self.assertRaises(SystemExit):
                cli.main(args)
            self.assertEqual(destination.read_text(encoding="utf-8"), csv_text)


if __name__ == "__main__":
    unittest.main()
