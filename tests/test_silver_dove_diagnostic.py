"""Source-free pinned Silver Dove field diagnostics, including drift rejection."""
from __future__ import annotations

from copy import deepcopy
from hashlib import sha256
import json
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch

from scriptorium import silver_dove_diagnostic as diag
from scriptorium import silver_dove_freeze as freeze


def fixture_source() -> str:
    categories = " ".join(f"[[Категория:{name}]]" for name in freeze._EXPECTED_CATEGORIES)
    return (
        "{{Отексте|АВТОР=Андрей Белый|ЛИЦЕНЗИЯ=PD-old}}\n"
        f"{freeze._EXPECTED_SCAFFOLD}\n"
        "<center>ВМЕСТО ПРЕДИСЛОВИЯ</center>\n"
        + ("Текст повести. " * 25000)
        + "\n" + freeze._EXPECTED_EDITORIAL_NOTE + " " + categories
    )


class SilverDoveDiagnosticTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.source = fixture_source()
        def fetch(_rows):
            return {freeze.WORK_TITLE: {
                "revision_id": freeze.SOURCE_REVISION_ID,
                "timestamp": "2025-07-30T21:54:23Z",
                "mediawiki_sha1": "a" * 40,
                "wikitext": cls.source,
            }}
        cls.manifest = freeze.build_manifest(fetcher=fetch)
        cls.body = freeze.extract_silver_dove_body(cls.source)

    def patched_pins(self):
        return (
            patch.object(diag, "FROZEN_BODY_CHARACTERS", len(self.body)),
            patch.object(diag, "FROZEN_BODY_SHA256", sha256(self.body.encode("utf-8")).hexdigest()),
            patch.object(diag, "FROZEN_WIKITEXT_SHA256", sha256(self.source.encode("utf-8")).hexdigest()),
        )

    def run_fixture(self, source=None):
        from contextlib import ExitStack
        with ExitStack() as stack:
            for context in self.patched_pins():
                stack.enter_context(context)
            return diag.build_diagnostic(
                self.manifest,
                fetcher=lambda _rows: {freeze.WORK_TITLE: source if source is not None else self.source},
            )

    def test_canonical_manifest_pin_and_public_reference_are_explicit(self):
        path = Path(__file__).resolve().parents[1] / "corpus/candidates/source-edition-traces/bely-silver-dove-ru.revisions.json"
        frozen = json.loads(path.read_text(encoding="utf-8"))
        self.assertEqual(frozen["composite_identity"]["raw_sha256"], diag.FROZEN_BODY_SHA256)
        self.assertEqual(frozen["composite_identity"]["character_count_including_spaces"], diag.FROZEN_BODY_CHARACTERS)
        self.assertEqual(frozen["source_identity"]["wikitext_sha256"], diag.FROZEN_WIKITEXT_SHA256)
        self.assertEqual(diag.FANTLAB_REFERENCES, {
            "fantlab.general.characters": "549050",
            "fantlab.general.words": "83369",
        })

    def test_source_free_fields_and_scientific_boundaries(self):
        artifact = self.run_fixture()
        rows = {row["metric_id"]: row for row in artifact["metric_rows"]}
        self.assertEqual(len(rows), 29)
        self.assertEqual(sum(row["actual"] is not None for row in rows.values()), 24)
        self.assertEqual(artifact["gates"]["m2_weight"], 0)
        self.assertFalse(artifact["gates"]["m2_parity_admissible"])
        self.assertEqual(artifact["gates"]["fantlab_source_edition_match"], "unknown")
        self.assertEqual(rows["fantlab.general.characters"]["actual"], len(self.body))
        self.assertEqual(
            rows["fantlab.general.characters"]["actual_minus_fantlab_display"],
            len(self.body) - 549050,
        )
        self.assertIsNone(rows["fantlab.dialogue.share_percent"]["fantlab_display"])
        self.assertEqual(rows["fantlab.dialogue.share_percent"]["result"], "MEASURED_REFERENCE_UNAVAILABLE")
        self.assertIsNone(rows["fantlab.vocabulary.uasz_3000"]["actual"])
        self.assertEqual(rows["fantlab.vocabulary.uasz_3000"]["result"], "NOT_RUN_DICTIONARY_UNBOUND")
        serialized = diag.render_json(artifact)
        self.assertNotIn("Текст повести", serialized)
        self.assertNotIn("wikitext", serialized.lower())
        self.assertEqual(serialized, diag.render_json(deepcopy(artifact)))
        self.assertEqual(json.loads(serialized), artifact)

    def test_source_drift_rejected_before_any_metrics(self):
        changed = self.source.replace("Текст повести", "Чужой текст", 1)
        with patch.object(diag, "analyze_deterministic_metrics") as analyzer:
            with self.assertRaisesRegex(ValueError, "wikitext|composite"):
                self.run_fixture(changed)
            analyzer.assert_not_called()

    def test_manifest_pin_drift_rejected_before_network_fetch(self):
        tampered = deepcopy(self.manifest)
        tampered["composite_identity"]["raw_sha256"] = "0" * 64
        fetcher = unittest.mock.Mock()
        with self.assertRaisesRegex(ValueError, "canonical pins"):
            diag.build_diagnostic(tampered, fetcher=fetcher)
        fetcher.assert_not_called()

    def test_create_only_source_free_receipt(self):
        artifact = {"candidate_id": freeze.CANDIDATE_ID, "source_text_committed": False}
        with tempfile.TemporaryDirectory() as directory:
            target = Path(directory) / "receipt.json"
            diag.write_new(target, artifact)
            expected = target.read_bytes()
            with self.assertRaises(FileExistsError):
                diag.write_new(target, artifact)
            self.assertEqual(target.read_bytes(), expected)


if __name__ == "__main__":
    unittest.main()
