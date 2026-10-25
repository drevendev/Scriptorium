"""Conditional N-only bounds: positive, ambiguous, negative and transport cases."""
import json
import unittest

from scriptorium.n_collision_diagnostic import SCHEMA, measure_n_only_impact, build_frozen_n_only_diagnostic
from scriptorium.pylem_provider import PYLEM_RUNTIME_PROFILE
from scriptorium.pylem_transport import build_sidecar_request
from scriptorium.text import NORMALIZATION_PROFILE

TEXT = "Три дома стоят. Дом и два."
ROWS = (("N",), ("N", "V"), ("V",), ("N",), ("CONJ",), ("N",))


def fixture():
    request = build_sidecar_request(TEXT)
    response = {
        "schema_version": "scriptorium-pylem-sidecar-response-v1",
        "runtime_profile": PYLEM_RUNTIME_PROFILE,
        "provider": {"distribution": "pylem", "version": "0.0.18"},
        "source_text_included": False,
        "normalized_sha256": request["normalized_sha256"],
        "token_count": len(ROWS),
        "rows": [
            {"ordinal": i, "token_sha256": token["sha256"], "runtime_pos": list(ROWS[i])}
            for i, token in enumerate(request["tokens"])
        ],
    }
    manifest = {
        "candidate_id": "test-frozen-identity",
        "composite_identity": {
            "normalization_profile": NORMALIZATION_PROFILE,
            "normalized_sha256": request["normalized_sha256"],
        },
    }
    return request, response, manifest


class NOnlyImpactTests(unittest.TestCase):
    def test_bucket_bigram_and_sentence_position_bounds(self):
        data = measure_n_only_impact(TEXT, ROWS)
        self.assertEqual((data["word_count"], data["sentence_count"]), (6, 2))
        self.assertEqual((data["baseline_defined_token_count"], data["n_only_token_count"], data["n_mixed_token_count_excluded"]), (2, 3, 1))
        self.assertEqual(data["conditional_defined_token_count"], 5)
        self.assertEqual(data["n_only_percent_of_words"], 50)
        for bucket in ("noun", "cardinal"):
            row = data["bucket_conditional_envelopes"][bucket]
            self.assertEqual((row["conditional_min_count"], row["conditional_max_count"]), (0, 3))
            self.assertEqual(row["conditional_max_percent_of_defined"], 60)
        pairs = {(r["first"], r["second"]): r for r in data["bigram_conditional_envelopes"]}
        self.assertEqual(pairs[("noun", "conjunction")]["conditional_max_raw_count"], 1)
        self.assertEqual(pairs[("conjunction", "cardinal")]["conditional_max_raw_count"], 1)
        self.assertNotIn(("noun", "verb"), pairs)
        positions = {(r["position"], r["bucket"]): r for r in data["position_conditional_envelopes"]}
        self.assertEqual(positions[(1, "noun")]["conditional_max_raw_count"], 2)
        self.assertEqual(positions[(3, "cardinal")]["conditional_max_percent_of_sentences"], 50)
        self.assertFalse(data["boundary"]["cell_bounds_jointly_attainable"])
        self.assertFalse(data["boundary"]["m2_parity_admissible"])

    def test_overlapping_n_edges_get_exact_cellwise_maximum(self):
        # Both adjacent edges share the middle token: the independent-edge
        # upper bound for noun->cardinal (2) cannot actually occur.
        data = measure_n_only_impact("Раз два три.", (("N",),) * 3)
        pairs = {(r["first"], r["second"]): r for r in data["bigram_conditional_envelopes"]}
        row = pairs[("noun", "cardinal")]
        self.assertEqual(row["independent_edge_upper_bound_raw_count"], 2)
        self.assertEqual(row["conditional_max_raw_count"], 1)
        self.assertEqual(row["conditional_min_raw_count"], 0)
        self.assertEqual(row["fixed_edge_lower_bound_raw_count"], 0)
        self.assertEqual(row["conditional_max_per_1000_words"], 1000 / 3)
        self.assertEqual(pairs[("noun", "noun")]["conditional_max_raw_count"], 2)
        self.assertEqual(data["boundary"]["bigram_max_method"],
                         "exact_per_cell_n_only_dynamic_programming")
        # Adjacent sentences cannot create cross-sentence bigrams.
        split = measure_n_only_impact("Раз два. Три.", (("N",),) * 3)
        split_pairs = {(r["first"], r["second"]): r
                       for r in split["bigram_conditional_envelopes"]}
        self.assertEqual(split_pairs[("noun", "cardinal")]["conditional_max_raw_count"], 1)

    def test_exact_pairwise_bounds_match_exhaustive_short_assignments(self):
        from itertools import product
        from scriptorium.n_collision_diagnostic import MARKER, _max_ambiguous_pair_gain, _min_ambiguous_pair_gain
        values = (MARKER, "noun", "cardinal", "verb", None)
        for length in range(2, 6):
            for slots in product(values, repeat=length):
                assignments = [("noun", "cardinal") if value == MARKER else (value,)
                               for value in slots]
                for first, second in product(("noun", "cardinal", "verb"), repeat=2):
                    baseline = sum(left == first and right == second
                                   for left, right in zip(slots, slots[1:]))
                    actual = [
                        sum(left == first and right == second
                            for left, right in zip(variant, variant[1:]))
                        for variant in product(*assignments)
                    ]
                    self.assertEqual(
                        baseline + _max_ambiguous_pair_gain(slots, first, second),
                        max(actual), (slots, first, second),
                    )
                    self.assertEqual(
                        baseline + _min_ambiguous_pair_gain(slots, first, second),
                        min(actual), (slots, first, second),
                    )

    def test_exact_minimum_for_unavoidable_conditional_transition(self):
        from scriptorium.n_collision_diagnostic import MARKER, _min_ambiguous_pair_gain
        # Synthetic POS slots test mathematics only; no native N discriminator.
        self.assertEqual(
            _min_ambiguous_pair_gain(("noun", MARKER, "cardinal"), "noun", "cardinal"), 1
        )
        self.assertEqual(
            _min_ambiguous_pair_gain((MARKER, MARKER, MARKER), "noun", "cardinal"), 0
        )
        self.assertEqual(
            _min_ambiguous_pair_gain(("noun", MARKER, "cardinal"), "cardinal", "noun"), 0
        )

    def test_null_empty_and_unaffected_negative(self):
        empty = measure_n_only_impact("", ())
        self.assertIsNone(empty["n_only_percent_of_words"])
        self.assertIsNone(empty["bucket_conditional_envelopes"]["noun"]["conditional_max_percent_of_defined"])
        self.assertEqual(empty["bigram_conditional_envelopes"], [])
        ordinary = measure_n_only_impact("Он бежит.", (("P",), ("V",)))
        self.assertEqual(ordinary["n_only_token_count"], 0)
        self.assertEqual(ordinary["position_conditional_envelopes"], [])

    def test_unknown_or_misaligned_rows_fail_closed(self):
        with self.assertRaisesRegex(ValueError, "candidate count"):
            measure_n_only_impact(TEXT, ROWS[:-1])
        with self.assertRaisesRegex(ValueError, "unknown runtime POS"):
            measure_n_only_impact("Слово", (("WRONG",),))
        with self.assertRaisesRegex(ValueError, "non-empty"):
            measure_n_only_impact("Слово", (("",),))

    def test_exact_provider_transport_is_checked_and_source_free(self):
        request, response, manifest = fixture()
        artifact = build_frozen_n_only_diagnostic(request, response, manifest, scriptorium_revision="test")
        self.assertEqual(artifact["schema_version"], SCHEMA)
        self.assertEqual(artifact["provider"]["version"], "0.0.18")
        self.assertEqual(artifact["impact"]["n_only_token_count"], 3)
        self.assertEqual(artifact["normalized_sha256"], request["normalized_sha256"])
        self.assertFalse(artifact["source_text_included"])
        payload = json.dumps(artifact, ensure_ascii=False)
        self.assertNotIn("дома", payload)
        self.assertNotIn("normalized_text", payload)
        response["source_text_included"] = True
        with self.assertRaisesRegex(ValueError, "exclude source text"):
            build_frozen_n_only_diagnostic(request, response, manifest, scriptorium_revision="test")

    def test_forged_manifest_or_token_hash_rejected(self):
        request, response, manifest = fixture()
        manifest["composite_identity"]["normalized_sha256"] = "0" * 64
        with self.assertRaisesRegex(ValueError, "frozen manifest identity"):
            build_frozen_n_only_diagnostic(request, response, manifest, scriptorium_revision="test")
        manifest["composite_identity"]["normalized_sha256"] = request["normalized_sha256"]
        response["rows"][0]["token_sha256"] = "0" * 64
        with self.assertRaisesRegex(ValueError, "token identity"):
            build_frozen_n_only_diagnostic(request, response, manifest, scriptorium_revision="test")


if __name__ == "__main__":
    unittest.main()
