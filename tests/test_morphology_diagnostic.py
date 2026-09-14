import unittest

from scriptorium.morphology_diagnostic import (
    DIAGNOSTIC_SCHEMA,
    build_fantlab_pos_accounting,
    classify_runtime_candidates,
    decompose_runtime_candidates,
)


class MorphologyDiagnosticTests(unittest.TestCase):
    def test_reason_partition_is_mutually_exclusive_and_source_free(self):
        rows = (
            ("A",),
            (),
            ("N",),
            ("N", "V"),
            ("POSL",),
            ("A", "ADJ_SHORT"),
            ("A", "V"),
        )
        artifact = decompose_runtime_candidates(rows)

        self.assertEqual(artifact["schema_version"], DIAGNOSTIC_SCHEMA)
        self.assertEqual(artifact["token_count"], 7)
        self.assertEqual(artifact["defined_count"], 1)
        self.assertEqual(artifact["undefined_count"], 6)
        self.assertEqual(
            artifact["undefined_reason_counts"],
            {
                "no_analysis": 1,
                "runtime_n_only": 1,
                "runtime_n_mixed": 1,
                "extra_runtime_only": 1,
                "extra_runtime_mixed": 1,
                "direct_cross_bucket_ambiguity": 1,
            },
        )
        self.assertEqual(artifact["known_conservative_policy_blocked_count"], 5)
        self.assertEqual(artifact["provider_no_analysis_count"], 1)
        self.assertEqual(
            artifact["unresolved_runtime_pos_token_presence"]["N"],
            2,
        )
        self.assertEqual(
            artifact["unresolved_runtime_pos_token_presence"]["POSL"],
            1,
        )
        self.assertEqual(
            artifact["unresolved_runtime_pos_token_presence"]["ADJ_SHORT"],
            1,
        )
        self.assertEqual(
            artifact["direct_ambiguity_bucket_set_counts"],
            {"adjective|verb": 1},
        )

    def test_classifier_does_not_turn_same_bucket_duplicates_into_ambiguity(self):
        self.assertEqual(classify_runtime_candidates(("A", "A")), "defined")
        self.assertEqual(classify_runtime_candidates(("N", "N")), "runtime_n_only")
        self.assertEqual(
            classify_runtime_candidates(("ADJ_SHORT", "PARTICIPLE_SHORT")),
            "extra_runtime_only",
        )

    def test_unknown_or_blank_runtime_values_fail_closed(self):
        with self.assertRaisesRegex(ValueError, "unknown runtime POS"):
            classify_runtime_candidates(("NEW_POS",))
        with self.assertRaisesRegex(ValueError, "non-empty strings"):
            classify_runtime_candidates(("",))

    def test_fantlab_accounting_records_only_integer_partition_deltas(self):
        expected = {
            "words": 100,
            "defined_pos_words": 75,
            "undefined_pos_words": 25,
        }
        pos = {
            "input": {"word_count": 110},
            "metrics": {
                "defined": {"count": 60},
                "undefined": {"count": 50},
            },
        }
        accounting = build_fantlab_pos_accounting(expected, pos)
        self.assertEqual(accounting["word_count"]["delta"], 10)
        self.assertEqual(accounting["defined_pos_words"]["delta"], -15)
        self.assertEqual(accounting["undefined_pos_words"]["delta"], 25)
        self.assertTrue(accounting["source_match_required_for_attribution"])

    def test_inconsistent_reference_or_scriptorium_partition_fails_closed(self):
        expected = {
            "words": 100,
            "defined_pos_words": 75,
            "undefined_pos_words": 24,
        }
        pos = {
            "input": {"word_count": 100},
            "metrics": {
                "defined": {"count": 75},
                "undefined": {"count": 25},
            },
        }
        with self.assertRaisesRegex(ValueError, "FantLab defined/undefined"):
            build_fantlab_pos_accounting(expected, pos)

        expected["undefined_pos_words"] = 25
        pos["metrics"]["undefined"]["count"] = 24
        with self.assertRaisesRegex(ValueError, "Scriptorium defined/undefined"):
            build_fantlab_pos_accounting(expected, pos)


if __name__ == "__main__":
    unittest.main()
