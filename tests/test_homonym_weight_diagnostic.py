import json
import unittest

from scriptorium.homonym_weight_diagnostic import (
    CANDIDATE_METADATA_SCHEMA,
    DIAGNOSTIC_SCHEMA,
    analyze_homonym_weight_signal,
    build_frozen_homonym_weight_diagnostic,
)
from scriptorium.pylem_provider import PYLEM_RUNTIME_PROFILE
from scriptorium.pylem_transport import RESPONSE_SCHEMA, build_sidecar_request
from scriptorium.text import NORMALIZATION_PROFILE


class HomonymWeightDiagnosticTests(unittest.TestCase):
    def _response(self, request, rows):
        return {
            "schema_version": RESPONSE_SCHEMA,
            "candidate_metadata_schema": CANDIDATE_METADATA_SCHEMA,
            "runtime_profile": PYLEM_RUNTIME_PROFILE,
            "provider": {"distribution": "pylem", "version": "0.0.18"},
            "normalized_sha256": request["normalized_sha256"],
            "token_count": len(rows),
            "rows": [
                {
                    "ordinal": ordinal,
                    "token_sha256": request["tokens"][ordinal]["sha256"],
                    "runtime_pos": [candidate[0] for candidate in candidates],
                    "candidate_metadata": [
                        {
                            "runtime_pos": candidate[0],
                            "predicted": candidate[1],
                            "homonym_weight": candidate[2],
                            "word_weight": candidate[3],
                        }
                        for candidate in candidates
                    ],
                }
                for ordinal, candidates in enumerate(rows)
            ],
            "source_text_included": False,
        }

    def _manifest(self, request):
        return {
            "candidate_id": "fixture-work",
            "composite_identity": {
                "normalization_profile": NORMALIZATION_PROFILE,
                "normalized_sha256": request["normalized_sha256"],
            },
        }

    def test_signal_measures_weight_separation_without_resolving_tokens(self):
        request = build_sidecar_request("а б в г д")
        response = self._response(
            request,
            [
                [("CONJ", False, 10, 100), ("INT", False, 3, 20)],
                [("P", False, 4, 20), ("PA", False, 4, 21)],
                [("A", False, 0, 11), ("V", False, 0, 12)],
                [("CONJ", True, None, None), ("PARTICLE", True, None, None)],
                [("N", False, 99, 200)],
            ],
        )
        signal = analyze_homonym_weight_signal(request, response)
        self.assertEqual(signal["schema_version"], DIAGNOSTIC_SCHEMA)
        self.assertEqual(signal["direct_cross_bucket_ambiguity_count"], 4)
        self.assertEqual(signal["homonym_weight_complete_count"], 3)
        self.assertEqual(signal["homonym_weight_missing_count"], 1)
        self.assertEqual(signal["unique_max_bucket_count"], 1)
        self.assertEqual(signal["tied_max_bucket_count"], 2)
        self.assertEqual(signal["unique_positive_max_bucket_count"], 1)
        self.assertEqual(signal["all_bucket_max_zero_count"], 1)
        self.assertEqual(signal["rows_with_any_predicted_analysis"], 1)
        self.assertEqual(signal["rows_with_all_predicted_analyses"], 1)
        self.assertEqual(signal["unique_max_nominated_bucket_counts"], {"conjunction": 1})
        self.assertFalse(signal["evidence_boundary"]["production_homonym_selection_changed"])
        self.assertFalse(signal["evidence_boundary"]["m2_parity_admissible"])

    def test_same_bucket_duplicate_is_not_direct_cross_bucket_ambiguity(self):
        request = build_sidecar_request("а")
        response = self._response(
            request,
            [[("CONJ", False, 10, 100), ("CONJ", False, 5, 90)]],
        )
        signal = analyze_homonym_weight_signal(request, response)
        self.assertEqual(signal["direct_cross_bucket_ambiguity_count"], 0)
        self.assertEqual(signal["unique_max_bucket_count"], 0)

    def test_metadata_alignment_and_types_fail_closed(self):
        request = build_sidecar_request("а")
        response = self._response(
            request,
            [[("CONJ", False, 10, 100), ("INT", False, 3, 20)]],
        )
        response["rows"][0]["candidate_metadata"].pop()
        with self.assertRaisesRegex(ValueError, "metadata length mismatch"):
            analyze_homonym_weight_signal(request, response)

        response = self._response(
            request,
            [[("CONJ", False, 10, 100), ("INT", False, 3, 20)]],
        )
        response["rows"][0]["candidate_metadata"][0]["runtime_pos"] = "INT"
        with self.assertRaisesRegex(ValueError, "runtime_pos mismatch"):
            analyze_homonym_weight_signal(request, response)

        response = self._response(
            request,
            [[("CONJ", False, 10, 100), ("INT", False, 3, 20)]],
        )
        response["rows"][0]["candidate_metadata"][0]["homonym_weight"] = True
        with self.assertRaisesRegex(ValueError, "integer or null"):
            analyze_homonym_weight_signal(request, response)

    def test_frozen_artifact_is_source_free_and_manifest_bound(self):
        request = build_sidecar_request("а б")
        response = self._response(
            request,
            [
                [("CONJ", False, 10, 100), ("INT", False, 3, 20)],
                [("N", False, 9, 200)],
            ],
        )
        artifact = build_frozen_homonym_weight_diagnostic(
            request,
            response,
            self._manifest(request),
            scriptorium_revision="deadbeef",
        )
        self.assertFalse(artifact["source_text_included"])
        self.assertEqual(artifact["diagnostic_boundary"]["status"], "diagnostic_only")
        self.assertFalse(artifact["diagnostic_boundary"]["production_resolution_changed"])
        serialized = json.dumps(artifact, ensure_ascii=False)
        self.assertNotIn('"а"', serialized)
        self.assertNotIn('"б"', serialized)

        manifest = self._manifest(request)
        manifest["composite_identity"]["normalized_sha256"] = "0" * 64
        with self.assertRaisesRegex(ValueError, "frozen manifest identity"):
            build_frozen_homonym_weight_diagnostic(
                request,
                response,
                manifest,
                scriptorium_revision="deadbeef",
            )


if __name__ == "__main__":
    unittest.main()
