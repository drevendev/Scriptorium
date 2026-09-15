from __future__ import annotations

import json
import shutil
import unittest
from pathlib import Path

from scriptorium.site_renderer import build_site


ROOT = Path(__file__).resolve().parents[1]
ARTIFACT_PATH = ROOT / "public-artifacts" / "tolstoy-anna-karenina-ru-morphology-diagnostic.json"
TRACE_PATH = ROOT / "corpus" / "candidates" / "source-edition-traces" / "tolstoy-anna-karenina-ru.json"
MANIFEST_PATH = ROOT / "site" / "publication-manifest.json"
OUTPUT = ROOT / "build" / "test-anna-morphology-showcase"
ENTRY_ID = "tolstoy-anna-karenina-ru-morphology-diagnostic-v1"
MERGED_M005 = "7dab1a6b0fe2a1d9fe44653a17580e3f6f25145b"
MERGED_M006 = "1bc8d9f92f6c8ab4bdce0a49ed45095af4579565"


class AnnaMorphologyPublicShowcaseTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.artifact = json.loads(ARTIFACT_PATH.read_text(encoding="utf-8"))
        cls.trace = json.loads(TRACE_PATH.read_text(encoding="utf-8"))
        cls.manifest = json.loads(MANIFEST_PATH.read_text(encoding="utf-8"))

    @classmethod
    def tearDownClass(cls) -> None:
        if OUTPUT.exists():
            shutil.rmtree(OUTPUT)

    def test_public_artifact_is_bound_to_frozen_candidate_and_fantlab_boundary(self) -> None:
        frozen = self.trace["public_transcription"]["frozen_candidate"]
        public = self.artifact["frozen_identity"]
        for key in (
            "character_count_including_spaces",
            "utf8_byte_count",
            "raw_sha256",
            "normalization_profile",
            "normalized_character_count_including_spaces",
            "normalized_sha256",
        ):
            self.assertEqual(public[key], frozen[key], key)

        fantlab = self.trace["fantlab"]
        boundary = self.artifact["fantlab_boundary"]
        self.assertEqual(boundary["work_id"], fantlab["work_id"])
        self.assertEqual(boundary["analysis_url"], fantlab["analysis_url"])
        self.assertEqual(boundary["analysis_date"], fantlab["analysis_date"])
        self.assertEqual(
            boundary["displayed_character_count"],
            fantlab["observed_counts"]["characters"],
        )
        self.assertEqual(boundary["displayed_word_count"], fantlab["observed_counts"]["words"])
        self.assertEqual(boundary["fantlab_source_edition_match"], "unknown")
        self.assertIs(boundary["m2_parity_admissible"], False)

    def test_morphology_and_methodology_summary_is_explicit_and_non_promotional(self) -> None:
        note = self.artifact["representativeness_note"]
        for value in (
            "269,358",
            "117,554",
            "151,804",
            "59,254",
            "5,972",
            "10.0786%",
            MERGED_M005,
            MERGED_M006,
            "127,909",
            "10,355",
            "7,607 infinitives",
            "1,874 short adjectives",
            "718 short participles",
            "156 phrasal verbs",
            "0 postpositions",
            "work-page relation remains unknown",
            "production POS resolution is unchanged",
            "not recovered FantLab rules, displayed FantLab counts or parity evidence",
        ):
            self.assertIn(value, note)

        self.assertEqual(self.artifact["status"], "diagnostic")
        self.assertEqual(self.artifact["benchmark_admissibility"], "diagnostic_only")
        self.assertEqual(self.artifact["compatibility_claim"], "extension")
        self.assertIs(self.artifact["source_text_committed"], False)

    def test_artifact_contains_no_transport_or_source_text_payload_keys(self) -> None:
        keys: set[str] = set()

        def collect(value):
            if isinstance(value, dict):
                keys.update(value)
                for nested in value.values():
                    collect(nested)
            elif isinstance(value, list):
                for nested in value:
                    collect(nested)

        collect(self.artifact)
        self.assertTrue(
            {
                "normalized_text",
                "tokens",
                "token_rows",
                "candidate_rows",
                "runtime_candidates",
                "runtime_pos_candidates",
                "source_text",
            }.isdisjoint(keys)
        )

    def test_manifest_allow_lists_stable_diagnostic_route(self) -> None:
        entries = {entry["entry_id"]: entry for entry in self.manifest["entries"]}
        entry = entries[ENTRY_ID]
        self.assertEqual(entry["slug"], "tolstoy-anna-karenina-morphology-diagnostic")
        self.assertEqual(
            entry["artifact_path"],
            "public-artifacts/tolstoy-anna-karenina-ru-morphology-diagnostic.json",
        )
        self.assertEqual(entry["artifact_schema"], "scriptorium-work-provenance-showcase-v1")
        self.assertEqual(entry["publication_status"], "diagnostic")
        self.assertEqual(entry["benchmark_admissibility"], "diagnostic_only")
        self.assertEqual(entry["compatibility_claim"], "extension")
        self.assertIs(entry["source_text_included"], False)

    def test_canonical_renderer_exposes_summary_and_fail_closed_labels(self) -> None:
        if OUTPUT.exists():
            shutil.rmtree(OUTPUT)
        record = build_site(ROOT, OUTPUT)
        routes = {row["entry_id"]: row["route"] for row in record["entries"]}
        self.assertEqual(
            routes[ENTRY_ID],
            "works/tolstoy-anna-karenina-morphology-diagnostic/",
        )
        page = OUTPUT / "works" / "tolstoy-anna-karenina-morphology-diagnostic" / "index.html"
        html = page.read_text(encoding="utf-8")
        self.assertIn("Full-work source-free morphology diagnostic", html)
        self.assertIn("269,358", html)
        self.assertIn("59,254", html)
        self.assertIn("5,972", html)
        self.assertIn("127,909", html)
        self.assertIn("10,355", html)
        self.assertIn("7,607 infinitives", html)
        self.assertIn("work-page relation remains unknown", html)
        self.assertIn("Source-edition match", html)
        self.assertIn("unknown", html)
        self.assertIn("M2 parity admissible", html)
        self.assertIn("false", html)
        self.assertIn("Source text is deliberately not included", html)


if __name__ == "__main__":
    unittest.main()
