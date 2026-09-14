import json
import re
import unittest
from pathlib import Path

from scriptorium.publication import derive_compatibility_claim, validate_compatibility_claim


ROOT = Path(__file__).resolve().parents[1]
MANIFEST_PATH = ROOT / "site" / "publication-manifest.json"
SCHEMA_PATH = ROOT / "schemas" / "scriptorium-publication-manifest-v1.schema.json"
RESURRECTION_TRACE = ROOT / "corpus" / "candidates" / "source-edition-traces" / "tolstoy-resurrection-ru.json"
PROVENANCE_PROFILE = "scriptorium-work-provenance-showcase-v1"


class PublicationManifestContractTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.manifest = json.loads(MANIFEST_PATH.read_text(encoding="utf-8"))
        cls.schema = json.loads(SCHEMA_PATH.read_text(encoding="utf-8"))

    def test_contract_identity_and_deployment_boundary(self):
        self.assertEqual(
            self.manifest["schema_version"],
            "scriptorium-publication-manifest-v1",
        )
        self.assertEqual(
            self.schema["$schema"],
            "https://json-schema.org/draft/2020-12/schema",
        )
        self.assertEqual(
            self.manifest["deployment"],
            {
                "publication_source": "github_actions",
                "generated_output_committed": False,
            },
        )

    def test_seed_entries_are_unique_and_repo_relative(self):
        entry_ids = [entry["entry_id"] for entry in self.manifest["entries"]]
        slugs = [entry["slug"] for entry in self.manifest["entries"]]
        self.assertEqual(len(entry_ids), len(set(entry_ids)))
        self.assertEqual(len(slugs), len(set(slugs)))

        for entry in self.manifest["entries"]:
            artifact = Path(entry["artifact_path"])
            self.assertFalse(artifact.is_absolute())
            self.assertNotIn("..", artifact.parts)
            self.assertTrue((ROOT / artifact).is_file())
            self.assertFalse(entry["source_text_included"])

    def test_seed_manifest_matches_canonical_showcase_safety_labels(self):
        self.assertEqual(len(self.manifest["entries"]), 3)
        for entry in self.manifest["entries"]:
            artifact = json.loads(
                (ROOT / entry["artifact_path"]).read_text(encoding="utf-8")
            )
            self.assertEqual(entry["entry_id"], artifact["showcase_id"])
            self.assertEqual(entry["publication_status"], artifact["status"])
            self.assertEqual(
                entry["benchmark_admissibility"], artifact["benchmark_admissibility"]
            )
            self.assertEqual(entry["corpus_admissibility"], artifact["corpus_admissibility"])

            if entry["artifact_schema"] == PROVENANCE_PROFILE:
                self.assertEqual(artifact["schema_version"], PROVENANCE_PROFILE)
                self.assertIs(artifact["source_text_committed"], False)
                self.assertEqual(entry["compatibility_claim"], "extension")
                self.assertEqual(artifact["compatibility_claim"], "extension")
                self.assertEqual(
                    artifact["fantlab_boundary"]["fantlab_source_edition_match"],
                    "unknown",
                )
                self.assertIs(
                    artifact["fantlab_boundary"]["m2_parity_admissible"], False
                )
                continue

            self.assertEqual(entry["artifact_schema"], artifact["analysis"]["schema_version"])
            self.assertIs(artifact["source"]["source_text_committed"], False)
            self.assertEqual(entry["compatibility_claim"], "mixed")
            self.assertEqual(derive_compatibility_claim(artifact), "mixed")
            self.assertEqual(validate_compatibility_claim(entry, artifact), "mixed")

    def test_resurrection_public_artifact_matches_frozen_canonical_trace(self):
        entry = next(
            row
            for row in self.manifest["entries"]
            if row["artifact_schema"] == PROVENANCE_PROFILE
        )
        artifact = json.loads((ROOT / entry["artifact_path"]).read_text(encoding="utf-8"))
        trace = json.loads(RESURRECTION_TRACE.read_text(encoding="utf-8"))
        frozen = trace["public_transcription"]["frozen_candidate"]
        source = artifact["source"]
        identity = artifact["frozen_identity"]
        fantlab = artifact["fantlab_boundary"]

        self.assertEqual(source["chapter_revision_count"], frozen["chapter_revision_count"])
        self.assertEqual(source["composition_profile"], frozen["composition_profile"])
        self.assertEqual(source["extraction_profile"], frozen["extraction_profile"])
        self.assertEqual(
            source["revision_manifest"], frozen["revision_manifest"]
        )
        for key in (
            "character_count_including_spaces",
            "utf8_byte_count",
            "raw_sha256",
            "normalization_profile",
            "normalized_character_count_including_spaces",
            "normalized_sha256",
        ):
            self.assertEqual(identity[key], frozen[key], key)

        self.assertEqual(fantlab["work_id"], trace["fantlab"]["work_id"])
        self.assertEqual(fantlab["analysis_url"], trace["fantlab"]["analysis_url"])
        self.assertEqual(fantlab["analysis_date"], trace["fantlab"]["analysis_date"])
        self.assertEqual(
            fantlab["displayed_character_count"],
            trace["fantlab"]["observed_counts"]["characters"],
        )
        self.assertEqual(
            fantlab["displayed_word_count"],
            trace["fantlab"]["observed_counts"]["words"],
        )
        self.assertEqual(
            fantlab["fantlab_source_edition_match"],
            trace["admissibility"]["fantlab_source_edition_match"],
        )
        self.assertIs(
            fantlab["m2_parity_admissible"],
            trace["admissibility"]["m2_parity_admissible"],
        )

    def test_compatibility_claim_upgrade_is_rejected(self):
        entry = next(
            row
            for row in self.manifest["entries"]
            if row["artifact_schema"] != PROVENANCE_PROFILE
        )
        entry = dict(entry)
        artifact = json.loads(
            (ROOT / entry["artifact_path"]).read_text(encoding="utf-8")
        )
        entry["compatibility_claim"] = "reproduced"

        with self.assertRaisesRegex(ValueError, "compatibility_claim"):
            validate_compatibility_claim(entry, artifact)

    def test_manifest_contains_no_source_prose_payload_keys(self):
        forbidden_keys = {"text", "source_text", "raw_text", "content"}

        def walk(value):
            if isinstance(value, dict):
                self.assertTrue(forbidden_keys.isdisjoint(value))
                for child in value.values():
                    walk(child)
            elif isinstance(value, list):
                for child in value:
                    walk(child)

        walk(self.manifest)
        provenance_entry = next(
            row
            for row in self.manifest["entries"]
            if row["artifact_schema"] == PROVENANCE_PROFILE
        )
        provenance = json.loads(
            (ROOT / provenance_entry["artifact_path"]).read_text(encoding="utf-8")
        )
        walk(provenance)

    def test_schema_rejects_path_escape_shapes(self):
        pattern = self.schema["properties"]["entries"]["items"]["properties"][
            "artifact_path"
        ]["pattern"]
        self.assertIsNotNone(
            re.fullmatch(pattern, "showcase/anna-karenina-part1-ch1-opening.json")
        )
        self.assertIsNotNone(
            re.fullmatch(pattern, "public-artifacts/tolstoy-resurrection-ru-provenance.json")
        )
        for invalid in (
            "/showcase/example.json",
            "docs/example.json",
            "showcase/../example.json",
            "showcase//example.json",
        ):
            self.assertIsNone(re.fullmatch(pattern, invalid), invalid)

    def test_schema_freezes_fail_closed_source_text_flag(self):
        item_properties = self.schema["properties"]["entries"]["items"]["properties"]
        self.assertEqual(item_properties["source_text_included"], {"const": False})
        self.assertEqual(
            self.schema["properties"]["deployment"]["properties"][
                "generated_output_committed"
            ],
            {"const": False},
        )


if __name__ == "__main__":
    unittest.main()
