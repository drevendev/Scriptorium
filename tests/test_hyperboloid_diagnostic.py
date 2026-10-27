"""Hyperboloid diagnostics: real frozen extraction and negative source gates."""
from __future__ import annotations
from contextlib import ExitStack
from copy import deepcopy
from hashlib import sha256
import json
from pathlib import Path
import tempfile
import unittest
from unittest.mock import Mock, patch
from scriptorium import hyperboloid_diagnostic as diag
from scriptorium import hyperboloid_freeze as freeze
from test_hyperboloid_freeze import SOURCE_IDENTITY, _revision_manifest, _source_shape

class HyperboloidDiagnosticTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.source = _source_shape("Фраза с повторами. " * 17_000)
        cls.identity = dict(SOURCE_IDENTITY)
        cls.identity.update({
            "wikitext_character_count": len(cls.source),
            "wikitext_utf8_byte_count": len(cls.source.encode("utf-8")),
            "wikitext_sha256": sha256(cls.source.encode("utf-8")).hexdigest(),
        })
        cls.revision = _revision_manifest()
        cls.revision["source_identity"] = dict(cls.identity)
        cls.body = freeze.build_body_manifest(
            cls.revision, fetcher=lambda **_: {**cls.identity, "wikitext": cls.source}
        )
    def patched_pins(self):
        body = self.body["literary_body_identity"]
        return (
            patch.object(diag, "FROZEN_BODY_CHARACTERS", body["character_count_including_spaces"]),
            patch.object(diag, "FROZEN_BODY_SHA256", body["raw_sha256"]),
            patch.object(diag, "FROZEN_NORMALIZED_SHA256", body["normalized_sha256"]),
            patch.object(diag, "FROZEN_WIKITEXT_SHA256", self.identity["wikitext_sha256"]),
        )
    def run_fixture(self, revision=None, body=None, source=None):
        with ExitStack() as stack:
            for context in self.patched_pins():
                stack.enter_context(context)
            return diag.build_diagnostic(
                self.revision if revision is None else revision,
                self.body if body is None else body,
                fetcher=lambda **_: {
                    **self.identity, "wikitext": self.source if source is None else source,
                },
            )
    def test_retained_frozen_pins_and_reference_counts(self):
        root = Path(__file__).resolve().parents[1] / "corpus/candidates/source-edition-traces"
        body = json.loads((root / "tolstoy-hyperboloid-garin-wikisource-ru.body.json").read_text(encoding="utf-8"))
        rev = json.loads((root / "tolstoy-hyperboloid-garin-wikisource-ru.revision.json").read_text(encoding="utf-8"))
        self.assertEqual(body["literary_body_identity"]["raw_sha256"], diag.FROZEN_BODY_SHA256)
        self.assertEqual(body["literary_body_identity"]["normalized_sha256"], diag.FROZEN_NORMALIZED_SHA256)
        self.assertEqual(body["literary_body_identity"]["character_count_including_spaces"], diag.FROZEN_BODY_CHARACTERS)
        self.assertEqual(rev["source_identity"]["wikitext_sha256"], diag.FROZEN_WIKITEXT_SHA256)
        self.assertEqual(diag.FANTLAB_REFERENCES, {
            "fantlab.general.characters": "495539",
            "fantlab.general.words": "69126",
        })
        diag._validate_pins(rev, body)
    def test_diagnostic_rows_nulls_and_source_privacy(self):
        data = self.run_fixture()
        rows = {r["metric_id"]: r for r in data["metric_rows"]}
        self.assertEqual(len(rows), 29)
        self.assertGreaterEqual(sum(r["actual"] is not None for r in rows.values()), 21)
        self.assertLessEqual(sum(r["actual"] is not None for r in rows.values()), 24)
        self.assertEqual(rows["fantlab.general.characters"]["actual"], self.body["literary_body_identity"]["character_count_including_spaces"])
        self.assertEqual(rows["fantlab.general.characters"]["result"], "DIAGNOSTIC_SOURCE_UNMATCHED")
        self.assertEqual(rows["fantlab.general.characters"]["actual_minus_fantlab_display"], rows["fantlab.general.characters"]["actual"] - 495539)
        self.assertIsNone(rows["fantlab.dialogue.share_percent"]["fantlab_display"])
        self.assertIsNone(rows["fantlab.vocabulary.uasz_3000"]["actual"])
        self.assertEqual(rows["fantlab.vocabulary.uasz_3000"]["result"], "NOT_RUN_DICTIONARY_UNBOUND")
        self.assertEqual(data["gates"]["m2_weight"], 0)
        self.assertFalse(data["gates"]["m2_parity_admissible"])
        self.assertEqual(data["gates"]["fantlab_source_edition_match"], "unknown")
        self.assertFalse(data["source_text_committed"])
        s = diag.render_json(data)
        self.assertNotIn("Фраза с повторами", s)
        self.assertNotIn("wikitext", s.lower())
        self.assertEqual(s, diag.render_json(deepcopy(data)))
    def test_changed_body_pin_fails_before_fetch(self):
        tampered = deepcopy(self.body)
        tampered["literary_body_identity"]["raw_sha256"] = "0" * 64
        fetch = Mock()
        with ExitStack() as stack:
            for context in self.patched_pins():
                stack.enter_context(context)
            with self.assertRaisesRegex(ValueError, "canonical frozen pins"):
                diag.build_diagnostic(self.revision, tampered, fetcher=fetch)
        fetch.assert_not_called()
    def test_changed_source_fails_before_analysis(self):
        modified = self.source.replace("Фраза с повторами.", "Чужая рукопись.", 1)
        with patch.object(diag, "analyze_deterministic_metrics") as analyzer:
            with self.assertRaisesRegex(ValueError, "identity drift"):
                self.run_fixture(source=modified)
            analyzer.assert_not_called()
    def test_changed_revision_pin_fails_before_fetch(self):
        tampered = deepcopy(self.revision)
        tampered["source_identity"]["wikitext_sha256"] = "f" * 64
        fetch = Mock()
        with ExitStack() as stack:
            for context in self.patched_pins():
                stack.enter_context(context)
            with self.assertRaisesRegex(ValueError, "canonical frozen pins"):
                diag.build_diagnostic(tampered, self.body, fetcher=fetch)
        fetch.assert_not_called()
    def test_create_only_receipt(self):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "data.json"
            diag.write_new(path, {"source_text_committed": False})
            before = path.read_bytes()
            with self.assertRaises(FileExistsError):
                diag.write_new(path, {"source_text_committed": False})
            self.assertEqual(path.read_bytes(), before)

if __name__ == "__main__":
    unittest.main()
