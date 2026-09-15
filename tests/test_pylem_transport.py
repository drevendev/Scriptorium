import ast
from hashlib import sha256
import json
import unittest
from pathlib import Path

from scriptorium.pylem_transport import (
    DIAGNOSTIC_SCHEMA,
    REQUEST_SCHEMA,
    RESPONSE_SCHEMA,
    build_frozen_pos_diagnostic,
    build_sidecar_request,
    consume_sidecar_response,
)
from scriptorium.pylem_provider import PYLEM_RUNTIME_PROFILE
from scriptorium.text import NORMALIZATION_PROFILE


class PylemTransportTests(unittest.TestCase):
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

    def _manifest(self, request, *, candidate_id="fixture-work"):
        return {
            "candidate_id": candidate_id,
            "composite_identity": {
                "normalization_profile": NORMALIZATION_PROFILE,
                "normalized_sha256": request["normalized_sha256"],
            },
        }

    def test_round_trip_preserves_conservative_resolution(self):
        request = build_sidecar_request("Красный дом спит.")
        self.assertEqual(request["schema_version"], REQUEST_SCHEMA)
        response = self._response(request, [["A"], ["N"], ["V", "A"]])
        artifact = consume_sidecar_response(request, response)
        self.assertEqual(artifact["runtime_profile"], PYLEM_RUNTIME_PROFILE)
        self.assertEqual(artifact["metrics"]["defined"]["count"], 1)
        self.assertEqual(artifact["metrics"]["undefined"]["count"], 2)
        self.assertEqual(artifact["metrics"]["buckets"]["adjective"]["count"], 1)

    def test_transport_identity_mismatch_fails_closed(self):
        request = build_sidecar_request("Красный дом.")
        response = self._response(request, [["A"], ["N"]])
        response["rows"][1]["token_sha256"] = "0" * 64
        with self.assertRaisesRegex(ValueError, "token identity mismatch"):
            consume_sidecar_response(request, response)

    def test_request_token_must_match_canonical_tokenization(self):
        request = build_sidecar_request("Красный дом.")
        request["tokens"][1]["text"] = "кот"
        request["tokens"][1]["sha256"] = sha256("кот".encode("utf-8")).hexdigest()
        response = self._response(request, [["A"], ["N"]])
        with self.assertRaisesRegex(ValueError, "canonical tokenization"):
            consume_sidecar_response(request, response)

    def test_unknown_runtime_pos_fails_closed(self):
        request = build_sidecar_request("слово")
        response = self._response(request, [["NEW_POS"]])
        with self.assertRaisesRegex(ValueError, "unknown runtime POS"):
            consume_sidecar_response(request, response)

    def test_provider_identity_mismatch_fails_closed(self):
        request = build_sidecar_request("слово")
        response = self._response(request, [["N"]])
        response["provider"] = {"distribution": "other", "version": "0.0.18"}
        with self.assertRaisesRegex(ValueError, "provider identity"):
            consume_sidecar_response(request, response)

    def test_noncanonical_or_wrong_profile_request_fails_closed(self):
        request = build_sidecar_request("Красный дом.")
        response = self._response(request, [["A"], ["N"]])
        request["text_profile"] = "different-profile"
        with self.assertRaisesRegex(ValueError, "text profile"):
            consume_sidecar_response(request, response)

        request = build_sidecar_request("Красный дом.")
        request["normalized_text"] = "Красный\r\nдом."
        request["normalized_sha256"] = sha256(
            request["normalized_text"].encode("utf-8")
        ).hexdigest()
        response = self._response(request, [["A"], ["N"]])
        with self.assertRaisesRegex(ValueError, "not canonical"):
            consume_sidecar_response(request, response)

    def test_frozen_diagnostic_is_bound_to_manifest_and_non_parity(self):
        request = build_sidecar_request("Красный дом.")
        response = self._response(request, [["A"], ["N"]])
        reference = {
            "expected": {
                "words": 2,
                "defined_pos_words": 1,
                "undefined_pos_words": 1,
                "pos": {
                    "adjective": {"count": 10, "percent_of_defined": 5.0},
                    "noun": {"count": 20, "percent_of_defined": 10.0},
                },
            }
        }
        artifact = build_frozen_pos_diagnostic(
            request,
            response,
            reference,
            self._manifest(request),
            scriptorium_revision="deadbeef",
        )
        self.assertEqual(artifact["schema_version"], DIAGNOSTIC_SCHEMA)
        self.assertFalse(artifact["source_text_included"])
        self.assertEqual(artifact["diagnostic_boundary"]["status"], "diagnostic_only")
        self.assertFalse(artifact["diagnostic_boundary"]["m2_parity_admissible"])
        self.assertEqual(
            artifact["undefined_decomposition"]["undefined_reason_counts"]["runtime_n_only"],
            1,
        )
        self.assertEqual(artifact["fantlab_pos_accounting"]["undefined_pos_words"]["delta"], 0)
        serialized = json.dumps(artifact, ensure_ascii=False)
        self.assertNotIn("Красный", serialized)
        self.assertNotIn("дом", serialized)
        self.assertEqual(
            artifact["fantlab_bucket_comparison"]["adjective"]["result"],
            "diagnostic_only",
        )
        self.assertEqual(
            artifact["fantlab_bucket_comparison"]["adjective"]["actual_scope"],
            "scriptorium_conservatively_defined_tokens_only",
        )

        mismatched_manifest = self._manifest(request, candidate_id="wrong-work")
        mismatched_manifest["composite_identity"]["normalized_sha256"] = "0" * 64
        with self.assertRaisesRegex(ValueError, "frozen manifest identity"):
            build_frozen_pos_diagnostic(
                request,
                response,
                reference,
                mismatched_manifest,
                scriptorium_revision="deadbeef",
            )

    def test_invalid_expected_count_fails_closed(self):
        request = build_sidecar_request("Красный дом.")
        response = self._response(request, [["A"], ["N"]])
        reference = {
            "expected": {
                "words": 2,
                "defined_pos_words": 1,
                "undefined_pos_words": 1,
                "pos": {
                    "adjective": {"count": None, "percent_of_defined": 5.0},
                },
            }
        }
        with self.assertRaisesRegex(ValueError, "must be an integer"):
            build_frozen_pos_diagnostic(
                request,
                response,
                reference,
                self._manifest(request),
                scriptorium_revision="deadbeef",
            )

    def test_sidecar_tool_has_no_scriptorium_import(self):
        root = Path(__file__).resolve().parents[1]
        source = (root / "tools/pylem_sidecar.py").read_text(encoding="utf-8")
        tree = ast.parse(source)
        roots = set()
        for node in ast.walk(tree):
            if isinstance(node, ast.Import):
                roots.update(alias.name.split(".", 1)[0] for alias in node.names)
            elif isinstance(node, ast.ImportFrom) and node.module:
                roots.add(node.module.split(".", 1)[0])
        self.assertNotIn("scriptorium", roots)
        self.assertIn('"source_text_included": False', source)


if __name__ == "__main__":
    unittest.main()
