"""New fourth-work native N path: rights, source identity, transport and privacy."""
from __future__ import annotations

from contextlib import ExitStack
from copy import deepcopy
import json
from pathlib import Path
from tempfile import TemporaryDirectory
import unittest
from unittest.mock import Mock, patch

from scriptorium import road_nowhere_freeze as freeze
from scriptorium import road_nowhere_diagnostic as pinned
from scriptorium import road_nowhere_native_n as native
from scriptorium.pylem_transport import build_sidecar_request
from scriptorium.pylem_provider import PYLEM_RUNTIME_PROFILE
from test_road_nowhere_freeze import _source, _revision_manifest, _fetcher

ROOT = Path(__file__).resolve().parents[1]


class FourthFullWorkNTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.source = _source("Книга один два. " * 22_000)
        cls.revision = _revision_manifest(cls.source)
        cls.body = freeze.build_body_manifest(cls.revision, fetcher=_fetcher(cls.source))

    def pinned_fixture(self):
        identity = self.body["literary_body_identity"]
        return (
            patch.object(pinned, "FROZEN_BODY_CHARACTERS", identity["character_count_including_spaces"]),
            patch.object(pinned, "FROZEN_BODY_SHA256", identity["raw_sha256"]),
            patch.object(pinned, "FROZEN_WIKITEXT_SHA256", self.revision["source_identity"]["wikitext_sha256"]),
            # _validate_pins was imported into the native module; patch its globals too.
            patch.object(native._validate_pins.__globals__["__builtins__"] if False else pinned,
                         "FANTLAB_REFERENCES", pinned.FANTLAB_REFERENCES),
        )

    def test_real_pins_are_still_source_matched_only_for_diagnostics(self):
        revision = json.loads((ROOT / native.SOURCE_PATH).read_text(encoding="utf-8"))
        body = json.loads((ROOT / native.BODY_PATH).read_text(encoding="utf-8"))
        pinned._validate_pins(revision, body)
        self.assertEqual(body["literary_body_identity"]["normalized_sha256"],
                         pinned.FROZEN_BODY_SHA256)
        self.assertEqual(revision["legal_basis"], "public_domain")
        self.assertEqual(body["fantlab_source_edition_match"], "unknown")
        self.assertFalse(body["m2_parity_admissible"])

    def test_verified_source_replayed_once_into_ephemeral_request(self):
        with ExitStack() as stack:
            for context in self.pinned_fixture()[:3]:
                stack.enter_context(context)
            request = native.prepare_request(
                self.revision, self.body, fetcher=_fetcher(self.source)
            )
        self.assertEqual(request["normalized_sha256"],
                         self.body["literary_body_identity"]["normalized_sha256"])
        self.assertEqual(len(request["normalized_text"]),
                         self.body["literary_body_identity"]["character_count_including_spaces"])
        self.assertGreater(len(request["tokens"]), 1000)

    def test_tampering_preempts_fetch_and_native_provider(self):
        changed = deepcopy(self.body)
        changed["literary_body_identity"]["normalized_sha256"] = "0" * 64
        fetch = Mock()
        with self.assertRaises(ValueError):
            native.prepare_request(self.revision, changed, fetcher=fetch)
        fetch.assert_not_called()
        changed = deepcopy(self.revision)
        changed["legal_basis"] = "unknown"
        with self.assertRaises(ValueError):
            native.prepare_request(changed, self.body, fetcher=fetch)
        fetch.assert_not_called()

    def test_mutated_replay_is_rejected(self):
        mutated = self.source.replace("Книга", "Порча", 1)
        with ExitStack() as stack:
            for context in self.pinned_fixture()[:3]:
                stack.enter_context(context)
            with self.assertRaisesRegex(ValueError, "identity drift"):
                native.prepare_request(
                    self.revision, self.body, fetcher=_fetcher(mutated)
                )

    def test_native_transport_and_n_bounds_only_publish_counts(self):
        request = build_sidecar_request("Три дома стоят. Дом и два.")
        rows = (("N",), ("N", "V"), ("V",), ("N",), ("CONJ",), ("N",))
        response = {
            "schema_version": "scriptorium-pylem-sidecar-response-v1",
            "runtime_profile": PYLEM_RUNTIME_PROFILE,
            "provider": {"distribution": "pylem", "version": "0.0.18"},
            "source_text_included": False,
            "normalized_sha256": request["normalized_sha256"],
            "token_count": len(rows),
            "rows": [
                {"ordinal": i, "token_sha256": token["sha256"], "runtime_pos": list(rows[i])}
                for i, token in enumerate(request["tokens"])
            ],
        }
        identity = {
            "normalized_sha256": request["normalized_sha256"],
            "normalized_character_count_including_spaces": len(request["normalized_text"]),
        }
        with patch.object(native, "_validate_pins", return_value=identity):
            result = native.finalize(
                self.revision, self.body, request, response,
                scriptorium_revision="local-fixture",
            )
            self.assertEqual(result["impact"]["n_only_token_count"], 3)
            self.assertEqual(result["impact"]["n_mixed_token_count_excluded"], 1)
            self.assertEqual(result["impact"]["word_count"], 6)
            self.assertFalse(result["source_text_included"])
            self.assertFalse(result["impact"]["boundary"]["m2_parity_admissible"])
            self.assertNotIn("дома", json.dumps(result, ensure_ascii=False))
            self.assertNotIn("normalized_text", json.dumps(result, ensure_ascii=False))
            response["rows"][0]["token_sha256"] = "0" * 64
            with self.assertRaises(ValueError):
                native.finalize(
                    self.revision, self.body, request, response,
                    scriptorium_revision="local-fixture",
                )

    def test_create_only_native_receipt_and_workflow_privacy(self):
        with TemporaryDirectory() as folder:
            destination = Path(folder) / "evidence.json"
            native._write_new(destination, '{"evidence": true}\n')
            saved = destination.read_bytes()
            with self.assertRaises(FileExistsError):
                native._write_new(destination, "different")
            self.assertEqual(destination.read_bytes(), saved)
        workflow = (ROOT / ".github/workflows/morphology-provider.yml").read_text(encoding="utf-8")
        self.assertIn("fourth-road-nowhere-native-n:", workflow)
        job = workflow.split("  fourth-road-nowhere-native-n:", 1)[1]
        self.assertIn("scriptorium.road_nowhere_native_n prepare", job)
        self.assertIn("scriptorium.road_nowhere_native_n finalize", job)
        self.assertIn("if: always()", job)
        self.assertIn("rm -f build/morph/road-pylem-request.json", job)
        self.assertIn("scriptorium-road-pylem-n-only-impact", job)
        self.assertNotIn("build/morph/road-pylem-request.json\n          if-no-files-found", job)


if __name__ == "__main__":
    unittest.main()
