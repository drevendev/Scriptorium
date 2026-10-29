"""Road to Nowhere alternate measured diagnostic: source, rights and no-parity tests."""
from __future__ import annotations

from contextlib import ExitStack
from copy import deepcopy
import json
from pathlib import Path
import tempfile
import unittest
from unittest.mock import Mock, patch

from scriptorium import road_nowhere_diagnostic as diag
from scriptorium import road_nowhere_freeze as freeze
from test_road_nowhere_freeze import _source, _revision_manifest, _fetcher


class RoadNowhereDiagnosticTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.source = _source("Фраза с повторами. " * 16_000)
        cls.revision = _revision_manifest(cls.source)
        cls.body = freeze.build_body_manifest(cls.revision, fetcher=_fetcher(cls.source))

    def patched_pins(self):
        body = self.body["literary_body_identity"]
        return (
            patch.object(diag, "FROZEN_BODY_CHARACTERS", body["character_count_including_spaces"]),
            patch.object(diag, "FROZEN_BODY_SHA256", body["raw_sha256"]),
            patch.object(diag, "FROZEN_WIKITEXT_SHA256",
                         self.revision["source_identity"]["wikitext_sha256"]),
        )

    def fixture(self, revision=None, body=None, source=None):
        with ExitStack() as stack:
            for context in self.patched_pins():
                stack.enter_context(context)
            return diag.build_diagnostic(
                self.revision if revision is None else revision,
                self.body if body is None else body,
                fetcher=_fetcher(self.source if source is None else source),
            )

    def test_committed_source_and_body_pins_with_exact_public_counts(self):
        root = Path(__file__).resolve().parents[1] / "corpus/candidates/source-edition-traces"
        revision = json.loads((root / "grin-road-nowhere-ru.alternate-revision.json").read_text(encoding="utf-8"))
        body = json.loads((root / "grin-road-nowhere-ru.alternate-body.json").read_text(encoding="utf-8"))
        self.assertEqual(body["literary_body_identity"]["raw_sha256"], diag.FROZEN_BODY_SHA256)
        self.assertEqual(body["literary_body_identity"]["character_count_including_spaces"], diag.FROZEN_BODY_CHARACTERS)
        self.assertEqual(revision["source_identity"]["wikitext_sha256"], diag.FROZEN_WIKITEXT_SHA256)
        self.assertEqual(diag.FANTLAB_REFERENCES,
                         {"fantlab.general.characters": "438439", "fantlab.general.words": "61299"})
        diag._validate_pins(revision, body)

    def test_measured_rows_are_source_free_and_diagnostic_only(self):
        artifact = self.fixture()
        rows = {row["metric_id"]: row for row in artifact["metric_rows"]}
        self.assertEqual(len(rows), 29)
        self.assertEqual(rows["fantlab.general.characters"]["actual"],
                         self.body["literary_body_identity"]["character_count_including_spaces"])
        self.assertEqual(rows["fantlab.general.characters"]["actual_minus_fantlab_display"],
                         rows["fantlab.general.characters"]["actual"] - 438439)
        self.assertEqual(rows["fantlab.general.words"]["result"], "DIAGNOSTIC_SOURCE_UNMATCHED")
        self.assertIsNone(rows["fantlab.dialogue.share_percent"]["fantlab_display"])
        self.assertIsNone(rows["fantlab.vocabulary.uasz_3000"]["actual"])
        self.assertEqual(rows["fantlab.vocabulary.uasz_3000"]["result"], "NOT_RUN_DICTIONARY_UNBOUND")
        self.assertEqual(artifact["gates"]["m2_weight"], 0)
        self.assertFalse(artifact["gates"]["primary_1965_transcription_body_ready"])
        self.assertEqual(artifact["gates"]["fantlab_source_edition_match"], "unknown")
        text = diag.render_json(artifact)
        self.assertNotIn("Фраза с повторами", text)
        self.assertNotIn('"wikitext"', text)
        self.assertEqual(text, diag.render_json(deepcopy(artifact)))

    def test_body_tamper_rejected_before_network(self):
        changed = deepcopy(self.body)
        changed["literary_body_identity"]["raw_sha256"] = "f" * 64
        fetch = Mock()
        with ExitStack() as stack:
            for context in self.patched_pins():
                stack.enter_context(context)
            with self.assertRaises(ValueError):
                diag.build_diagnostic(self.revision, changed, fetcher=fetch)
        fetch.assert_not_called()

    def test_revision_tamper_rejected_before_network(self):
        changed = deepcopy(self.revision)
        changed["source_identity"]["wikitext_sha256"] = "0" * 64
        fetch = Mock()
        with ExitStack() as stack:
            for context in self.patched_pins():
                stack.enter_context(context)
            with self.assertRaises(ValueError):
                diag.build_diagnostic(changed, self.body, fetcher=fetch)
        fetch.assert_not_called()

    def test_changed_source_rejected_before_metrics(self):
        changed = self.source.replace("Фраза с повторами.", "Другая рукопись.", 1)
        with patch.object(diag, "analyze_deterministic_metrics") as analyzer:
            with self.assertRaisesRegex(ValueError, "identity drift"):
                self.fixture(source=changed)
            analyzer.assert_not_called()

    def test_create_only_output(self):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "observed.json"
            diag.write_new(path, {"source_text_committed": False})
            before = path.read_bytes()
            with self.assertRaises(FileExistsError):
                diag.write_new(path, {"source_text_committed": False})
            self.assertEqual(path.read_bytes(), before)


if __name__ == "__main__":
    unittest.main()
