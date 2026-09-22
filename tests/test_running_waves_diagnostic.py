from __future__ import annotations

from copy import deepcopy
import json
from pathlib import Path
import unittest

from scriptorium.running_waves_body import build_manifest as build_body_manifest
from scriptorium.running_waves_diagnostic import (
    DIAGNOSTIC_VERSION,
    FANTLAB_REFERENCES,
    build_diagnostic,
)


ROOT = Path(__file__).resolve().parents[1]
SOURCE_MANIFEST = ROOT / "corpus/candidates/source-edition-traces/grin-running-on-waves-ru.source-revisions.json"


class RunningWavesDiagnosticTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.source = json.loads(SOURCE_MANIFEST.read_text(encoding="utf-8"))
        identities = cls.source["pages"]
        cls.payloads = {
            row["title"]: '<div class="text">' + ("Слово " * 1600) + f"{row['ordinal']}.</div>"
            for row in identities
        }

        def fetcher(rows):
            return {str(row["title"]): cls.payloads[str(row["title"])] for row in rows}

        cls.fetcher = staticmethod(fetcher)
        cls.body = build_body_manifest(cls.source, fetcher=fetcher)

    def test_builds_source_free_diagnostic_with_closed_parity_gate(self) -> None:
        diagnostic = build_diagnostic(
            self.source,
            self.body,
            fetcher=self.fetcher,
            enforce_canonical_body=False,
        )
        self.assertEqual(DIAGNOSTIC_VERSION, diagnostic["diagnostic_version"])
        self.assertFalse(diagnostic["source_text_committed"])
        self.assertEqual("unknown", diagnostic["gates"]["fantlab_source_edition_match"])
        self.assertTrue(diagnostic["gates"]["diagnostic_ready"])
        self.assertFalse(diagnostic["gates"]["gate_ready"])
        self.assertFalse(diagnostic["gates"]["m2_parity_admissible"])
        self.assertEqual(0, diagnostic["gates"]["m2_weight"])
        self.assertEqual(len(FANTLAB_REFERENCES), len(diagnostic["metrics"]))

    def test_dictionary_dependent_rows_remain_not_run(self) -> None:
        diagnostic = build_diagnostic(
            self.source,
            self.body,
            fetcher=self.fetcher,
            enforce_canonical_body=False,
        )
        rows = {row["metric_id"]: row for row in diagnostic["metrics"]}
        for metric_id in (
            "fantlab.vocabulary.active_dictionary",
            "fantlab.vocabulary.active_nondictionary",
            "fantlab.vocabulary.uasz_3000",
            "fantlab.vocabulary.uasz_10000",
        ):
            self.assertEqual("not_run_dependency_unbound", rows[metric_id]["status"])
            self.assertIsNone(rows[metric_id]["scriptorium_raw_value"])
            self.assertIsNone(rows[metric_id]["delta_against_fantlab_display"])

    def test_diagnostic_serialization_contains_no_fixture_prose(self) -> None:
        diagnostic = build_diagnostic(
            self.source,
            self.body,
            fetcher=self.fetcher,
            enforce_canonical_body=False,
        )
        serialized = json.dumps(diagnostic, ensure_ascii=False)
        self.assertNotIn("Слово", serialized)
        self.assertNotIn("wikitext", serialized.lower())
        self.assertNotIn("literary_text", serialized.lower())

    def test_canonical_body_guard_rejects_noncanonical_fixture(self) -> None:
        with self.assertRaisesRegex(ValueError, "frozen character-count constant drift"):
            build_diagnostic(self.source, self.body, fetcher=self.fetcher)

    def test_body_manifest_validation_rejects_identity_drift(self) -> None:
        corrupted = deepcopy(self.body)
        corrupted["composite_identity"]["raw_sha256"] = "0" * 64
        with self.assertRaisesRegex(ValueError, "raw_sha256"):
            build_diagnostic(
                self.source,
                corrupted,
                fetcher=self.fetcher,
                enforce_canonical_body=False,
            )


if __name__ == "__main__":
    unittest.main()
