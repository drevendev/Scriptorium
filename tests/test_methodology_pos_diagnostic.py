import json
import unittest

from scriptorium.methodology_pos_diagnostic import (
    EXTRA_RUNTIME_TO_METHODOLOGY_BUCKET,
    FROZEN_METHODOLOGY_DIAGNOSTIC_SCHEMA,
    METHODOLOGY_DIAGNOSTIC_SCHEMA,
    analyze_methodology_pos_signal,
    build_frozen_methodology_pos_diagnostic,
    resolve_methodology_runtime_pos,
)
from scriptorium.pylem_provider import PYLEM_RUNTIME_PROFILE
from scriptorium.pylem_transport import RESPONSE_SCHEMA, build_sidecar_request
from scriptorium.text import NORMALIZATION_PROFILE


class MethodologyPosDiagnosticTests(unittest.TestCase):
    def _response(self, request, rows):
        return {
            "schema_version": RESPONSE_SCHEMA,
            "runtime_profile": PYLEM_RUNTIME_PROFILE,
            "provider": {"distribution": "pylem", "version": "0.0.18"},
            "normalized_sha256": request["normalized_sha256"],
            "token_count": len(rows),
            "rows": [
                {
                    "ordinal": ordinal,
                    "token_sha256": request["tokens"][ordinal]["sha256"],
                    "runtime_pos": values,
                }
                for ordinal, values in enumerate(rows)
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

    def test_all_five_methodology_only_runtime_categories_are_source_backed(self):
        self.assertEqual(
            EXTRA_RUNTIME_TO_METHODOLOGY_BUCKET,
            {
                "POSL": "postposition",
                "COLLOC": "phrasal_verb",
                "ADJ_SHORT": "short_adjective",
                "PARTICIPLE_SHORT": "short_participle",
                "INFINITIVE": "infinitive",
            },
        )
        for runtime_pos, bucket in EXTRA_RUNTIME_TO_METHODOLOGY_BUCKET.items():
            self.assertEqual(resolve_methodology_runtime_pos([runtime_pos]), bucket)

    def test_runtime_n_and_cross_category_homonyms_remain_fail_closed(self):
        self.assertIsNone(resolve_methodology_runtime_pos(["N"]))
        self.assertIsNone(resolve_methodology_runtime_pos(["CONJ", "PARTICLE"]))
        self.assertIsNone(resolve_methodology_runtime_pos(["ADJ_SHORT", "INFINITIVE"]))
        self.assertEqual(
            resolve_methodology_runtime_pos(["ADJ_SHORT", "ADJ_SHORT"]),
            "short_adjective",
        )

    def test_signal_adds_methodology_categories_without_changing_work_page_surface(self):
        request = build_sidecar_request(
            "один два три четыре пять шесть семь восемь"
        )
        response = self._response(
            request,
            [
                ["POSL"],
                ["COLLOC"],
                ["ADJ_SHORT"],
                ["PARTICIPLE_SHORT"],
                ["INFINITIVE"],
                ["N"],
                ["CONJ"],
                ["CONJ", "PARTICLE"],
            ],
        )
        signal = analyze_methodology_pos_signal(request, response)
        self.assertEqual(signal["schema_version"], METHODOLOGY_DIAGNOSTIC_SCHEMA)
        self.assertEqual(signal["token_count"], 8)
        self.assertEqual(signal["defined_count"], 6)
        self.assertEqual(signal["undefined_count"], 2)
        self.assertEqual(signal["observed_work_page_surface_defined_count"], 1)
        self.assertEqual(signal["additional_methodology_defined_count"], 5)
        self.assertEqual(
            signal["extra_methodology_bucket_counts"],
            {
                "postposition": 1,
                "phrasal_verb": 1,
                "short_adjective": 1,
                "short_participle": 1,
                "infinitive": 1,
            },
        )
        self.assertIsNone(signal["buckets"]["noun"]["count"])
        self.assertIsNone(signal["buckets"]["cardinal"]["count"])
        self.assertFalse(signal["evidence_boundary"]["production_pos_profile_changed"])
        self.assertFalse(signal["evidence_boundary"]["m2_parity_admissible"])

    def test_frozen_artifact_is_source_free_and_manifest_bound(self):
        request = build_sidecar_request("короток бежать дом")
        response = self._response(request, [["ADJ_SHORT"], ["INFINITIVE"], ["N"]])
        artifact = build_frozen_methodology_pos_diagnostic(
            request,
            response,
            self._manifest(request),
            scriptorium_revision="deadbeef",
        )
        self.assertEqual(
            artifact["schema_version"], FROZEN_METHODOLOGY_DIAGNOSTIC_SCHEMA
        )
        self.assertFalse(artifact["source_text_included"])
        self.assertEqual(artifact["diagnostic_boundary"]["status"], "diagnostic_only")
        self.assertFalse(artifact["diagnostic_boundary"]["production_pos_profile_changed"])
        self.assertFalse(artifact["diagnostic_boundary"]["m2_parity_admissible"])
        serialized = json.dumps(artifact, ensure_ascii=False)
        self.assertNotIn("короток", serialized)
        self.assertNotIn("бежать", serialized)
        self.assertNotIn("дом", serialized)

        manifest = self._manifest(request)
        manifest["composite_identity"]["normalized_sha256"] = "0" * 64
        with self.assertRaisesRegex(ValueError, "frozen manifest identity"):
            build_frozen_methodology_pos_diagnostic(
                request,
                response,
                manifest,
                scriptorium_revision="deadbeef",
            )


if __name__ == "__main__":
    unittest.main()
