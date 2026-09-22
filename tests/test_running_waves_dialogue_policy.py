from __future__ import annotations

from copy import deepcopy
import json
from pathlib import Path
import unittest

from scriptorium.running_waves_body import build_manifest as build_body_manifest
from scriptorium.running_waves_dialogue_policy import (
    DIAGNOSTIC_VERSION,
    FANTLAB_AUTHOR_TEXT_INSIDE_DIALOGUE_PERCENT,
    build_diagnostic,
)


ROOT = Path(__file__).resolve().parents[1]
SOURCE_MANIFEST = ROOT / "corpus/candidates/source-edition-traces/grin-running-on-waves-ru.source-revisions.json"


class RunningWavesDialoguePolicyTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.source = json.loads(SOURCE_MANIFEST.read_text(encoding="utf-8"))
        identities = cls.source["pages"]
        cls.payloads = {
            row["title"]: (
                '<div class="text">'
                + ("Нарратив " * 500)
                + f"{row['ordinal']}.\n\n"
                + "— Слово, — сказал он. — Ответ.\n\n"
                + "— Я — человек."
                + "</div>"
            )
            for row in identities
        }

        def fetcher(rows):
            return {str(row["title"]): cls.payloads[str(row["title"])] for row in rows}

        cls.fetcher = staticmethod(fetcher)
        cls.body = build_body_manifest(cls.source, fetcher=fetcher)

    def test_builds_source_free_fail_closed_policy_diagnostic(self) -> None:
        diagnostic = build_diagnostic(
            self.source,
            self.body,
            fetcher=self.fetcher,
            enforce_canonical_body=False,
        )

        self.assertEqual(DIAGNOSTIC_VERSION, diagnostic["diagnostic_version"])
        self.assertFalse(diagnostic["source_text_committed"])
        self.assertFalse(
            diagnostic["interpretation"]["production_dialogue_profile_changed"]
        )
        self.assertTrue(
            diagnostic["interpretation"]["closest_variant_is_not_a_semantics_selection"]
        )
        self.assertEqual("unknown", diagnostic["gates"]["fantlab_source_edition_match"])
        self.assertTrue(diagnostic["gates"]["diagnostic_ready"])
        self.assertFalse(diagnostic["gates"]["gate_ready"])
        self.assertFalse(diagnostic["gates"]["m2_parity_admissible"])
        self.assertEqual(0, diagnostic["gates"]["m2_weight"])

        variants = diagnostic["probe"]["author_text_inside_dialogue_variants"]
        self.assertEqual(4, len(variants))
        ranking = diagnostic["author_text_variant_distance_ranking"]
        self.assertEqual(4, len(ranking))
        distances = [row["absolute_delta_percentage_points"] for row in ranking]
        self.assertEqual(sorted(distances), distances)
        for row in ranking:
            self.assertAlmostEqual(
                row["delta_to_fantlab_display_percentage_points"],
                row["value_percent"] - FANTLAB_AUTHOR_TEXT_INSIDE_DIALOGUE_PERCENT,
            )

    def test_serialization_contains_no_fixture_prose(self) -> None:
        diagnostic = build_diagnostic(
            self.source,
            self.body,
            fetcher=self.fetcher,
            enforce_canonical_body=False,
        )
        serialized = json.dumps(diagnostic, ensure_ascii=False)
        self.assertNotIn("Нарратив", serialized)
        self.assertNotIn("сказал он", serialized)
        self.assertNotIn("source_prose", serialized.lower())
        self.assertNotIn("literary_text", serialized.lower())
        self.assertIn("not recovered FantLab semantics", diagnostic["probe"]["warning"])

    def test_boundary_probe_is_narrower_than_current_v1_on_fixture(self) -> None:
        diagnostic = build_diagnostic(
            self.source,
            self.body,
            fetcher=self.fetcher,
            enforce_canonical_body=False,
        )
        counts = diagnostic["probe"]["character_counts"]
        self.assertLess(
            counts["speech_boundary_author_remark_non_whitespace"],
            counts["current_v1_author_remark_non_whitespace"],
        )

    def test_canonical_body_guard_rejects_noncanonical_fixture(self) -> None:
        with self.assertRaisesRegex(ValueError, "frozen character-count constant drift"):
            build_diagnostic(self.source, self.body, fetcher=self.fetcher)

    def test_body_manifest_validation_rejects_digest_drift(self) -> None:
        corrupted = deepcopy(self.body)
        corrupted["composite_identity"]["raw_sha256"] = "not-a-sha256"
        with self.assertRaisesRegex(ValueError, "raw_sha256"):
            build_diagnostic(
                self.source,
                corrupted,
                fetcher=self.fetcher,
                enforce_canonical_body=False,
            )


if __name__ == "__main__":
    unittest.main()
