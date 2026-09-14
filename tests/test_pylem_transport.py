import ast
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

    def test_round_trip_preserves_conservative_resolution(self):
        request = build_sidecar_request("Красный дом спит.")
        self.assertEqual(request["schema_version"], REQUEST_SCHEMA)
        response = self._response(request, [["A"], ["N"], ["V", "A"]])
        artifact = consume_sidecar_response(request, response)
        self.assertEqual(artifact["metrics"]["defined"]["count"], 1)
        self.assertEqual(artifact["metrics"]["undefined"]["count"], 2)
        self.assertEqual(artifact["metrics"]["buckets"]["adjective"]["count"], 1)

    def test_transport_identity_mismatch_fails_closed(self):
        request = build_sidecar_request("Красный дом.")
        response = self._response(request, [["A"], ["N"]])
        response["rows"][1]["token_sha256"] = "0" * 64
        with self.assertRaisesRegex(ValueError, "token identity mismatch"):
            consume_sidecar_response(request, response)

    def test_unknown_runtime_pos_fails_closed(self):
        request = build_sidecar_request("слово")
        response = self._response(request, [["NEW_POS"]])
        with self.assertRaisesRegex(ValueError, "unknown runtime POS"):
            consume_sidecar_response(request, response)

    def test_frozen_diagnostic_is_source_free_and_non_parity(self):
        request = build_sidecar_request("Красный дом.")
        response = self._response(request, [["A"], ["N"]])
        reference = {
            "expected": {
                "pos": {
                    "adjective": {"count": 10, "percent_of_defined": 5.0},
                    "noun": {"count": 20, "percent_of_defined": 10.0},
                }
            }
        }
        manifest = {"candidate_id": "fixture-work"}
        artifact = build_frozen_pos_diagnostic(
            request,
            response,
            reference,
            manifest,
            scriptorium_revision="deadbeef",
        )
        self.assertEqual(artifact["schema_version"], DIAGNOSTIC_SCHEMA)
        self.assertFalse(artifact["source_text_included"])
        self.assertEqual(artifact["diagnostic_boundary"]["status"], "diagnostic_only")
        self.assertFalse(artifact["diagnostic_boundary"]["m2_parity_admissible"])
        serialized = json.dumps(artifact, ensure_ascii=False)
        self.assertNotIn("Красный", serialized)
        self.assertNotIn("дом", serialized)
        self.assertEqual(
            artifact["fantlab_bucket_comparison"]["adjective"]["result"],
            "diagnostic_only",
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
