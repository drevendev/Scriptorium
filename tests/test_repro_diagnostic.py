import json
from hashlib import sha256
import unittest
from unittest.mock import patch

from scriptorium.repro_diagnostic import build_frozen_diagnostic


class ReproDiagnosticTests(unittest.TestCase):
    def test_frozen_diagnostic_remains_fail_closed_for_unknown_fantlab_source(self):
        reference = json.dumps(
            {
                "benchmark_id": "example",
                "reference": {
                    "site": "FantLab",
                    "url": "https://example.invalid/lp",
                    "analysis_date": "2022-09-19",
                    "work_id": 1,
                    "title": "Example",
                    "author": "Example",
                },
                "expected": {
                    "characters": 11,
                    "words": 2,
                    "dialogue_share_percent": 35.12,
                    "author_text_inside_dialogue_percent": 17.02,
                },
            }
        )
        manifest = {
            "bibliographic_source": "Frozen edition",
            "source_work_url": "https://example.invalid/source",
            "legal_basis": "public_domain",
        }

        with patch(
            "scriptorium.repro_diagnostic.replay_packed_manifest",
            return_value="Привет мир.",
        ):
            artifact = build_frozen_diagnostic(
                reference,
                manifest,
                scriptorium_revision="abc123",
            )

        self.assertEqual(artifact["source_text"]["edition_match"], "unknown")
        self.assertEqual(
            artifact["metrics"]["fantlab.general.characters"]["comparison"]["result"],
            "unresolved",
        )
        self.assertEqual(
            artifact["metrics"]["fantlab.general.characters"]["comparison"]["raw_delta"],
            0,
        )
        self.assertEqual(artifact["diagnostic_boundary"]["status"], "diagnostic_only")
        self.assertIs(artifact["diagnostic_boundary"]["m2_parity_admissible"], False)
        self.assertEqual(artifact["policy_sensitivity"]["status"], "diagnostic_only")
        self.assertEqual(
            artifact["policy_sensitivity"]["word_policy"]["variants"][
                "current_scriptorium_text_v1"
            ]["count"],
            2,
        )
        self.assertEqual(
            artifact["policy_sensitivity"]["reference"]["expected_word_count"],
            2,
        )
        self.assertIsNone(
            artifact["policy_sensitivity"]["reference"]["expected_dash_per_1000_words"]
        )

        self.assertEqual(artifact["dialogue_sensitivity"]["status"], "diagnostic_only")
        self.assertEqual(
            artifact["dialogue_sensitivity"]["reference"][
                "expected_dialogue_share_percent"
            ],
            35.12,
        )
        self.assertEqual(
            artifact["dialogue_sensitivity"]["reference"][
                "expected_author_text_inside_dialogue_percent"
            ],
            17.02,
        )
        self.assertEqual(artifact["dialogue_sensitivity"]["dialogue_share"]["value"], 0.0)
        self.assertIsNone(
            artifact["dialogue_sensitivity"]["author_text_inside_dialogue_variants"][
                "current_v1_over_dialogue"
            ]["value"]
        )


    def test_opt_in_full_input_boundary_evidence_is_source_free(self):
        sample = "по-русски А.Б. 12 слово‐слово"
        digest = sha256(sample.encode("utf-8")).hexdigest()
        manifest = {
            "bibliographic_source": "Frozen public-domain edition",
            "source_work_url": "https://example.invalid/source",
            "legal_basis": "public_domain",
            "composite_identity": {
                "normalized_sha256": digest,
                "normalized_character_count_including_spaces": len(sample),
            },
        }
        reference = json.dumps({
            "benchmark_id": "synthetic",
            "reference": {
                "site": "FantLab", "url": "https://example.invalid/lp",
                "analysis_date": "2022-09-19", "work_id": 1,
                "title": "Example", "author": "Example",
            },
            "expected": {"characters": len(sample), "words": 6},
        })
        with patch("scriptorium.repro_diagnostic.replay_packed_manifest", return_value=sample):
            normal = build_frozen_diagnostic(reference, manifest, scriptorium_revision="test")
            self.assertNotIn("word_boundary_sensitivity", normal)
            artifact = build_frozen_diagnostic(
                reference, manifest, scriptorium_revision="test",
                include_boundary_sensitivity=True,
            )
        probe = artifact["word_boundary_sensitivity"]
        rows = {row["id"]: row["word_count"] for row in probe["variants"]}
        self.assertEqual(probe["normalized_sha256"], digest)
        self.assertEqual(rows["split_ascii_hyphen"], rows["current_scriptorium_text_v1"] + 1)
        self.assertEqual(rows["merge_dotted_initialisms"], rows["current_scriptorium_text_v1"] - 1)
        self.assertEqual(rows["join_unicode_hyphens"], rows["current_scriptorium_text_v1"] - 1)
        self.assertFalse(probe["source_text_embedded"])
        self.assertEqual(probe["source_identity_to_fantlab"], "UNKNOWN")
        self.assertNotIn(sample, json.dumps(artifact, ensure_ascii=False))
        self.assertFalse(artifact["diagnostic_boundary"]["m2_parity_admissible"])

        bad_manifest = dict(manifest)
        bad_manifest["composite_identity"] = dict(manifest["composite_identity"], normalized_sha256="0" * 64)
        with patch("scriptorium.repro_diagnostic.replay_packed_manifest", return_value=sample):
            with self.assertRaisesRegex(ValueError, "source identity mismatch"):
                build_frozen_diagnostic(
                    reference, bad_manifest, scriptorium_revision="test",
                    include_boundary_sensitivity=True,
                )

    def test_boundary_probe_rejects_mismatched_policy_count(self):
        sample = "по-русски"
        manifest = {
            "bibliographic_source": "Frozen public-domain edition",
            "source_work_url": "https://example.invalid/source",
            "legal_basis": "public_domain",
            "composite_identity": {
                "normalized_sha256": sha256(sample.encode("utf-8")).hexdigest(),
                "normalized_character_count_including_spaces": len(sample),
            },
        }
        reference = json.dumps({
            "benchmark_id": "synthetic",
            "reference": {
                "site": "FantLab", "url": "https://example.invalid/lp",
                "analysis_date": "2022-09-19", "work_id": 1,
                "title": "Example", "author": "Example",
            },
            "expected": {"characters": len(sample), "words": 1},
        })
        with patch("scriptorium.repro_diagnostic.replay_packed_manifest", return_value=sample):
            with patch("scriptorium.repro_diagnostic.analyze_boundary_probe") as modified:
                from scriptorium.boundary_probe import analyze_boundary_probe
                probe = analyze_boundary_probe(sample)
                probe["variants"][0]["word_count"] += 1
                modified.return_value = probe
                with self.assertRaisesRegex(ValueError, "baseline differs"):
                    build_frozen_diagnostic(
                        reference, manifest, scriptorium_revision="test",
                        include_boundary_sensitivity=True,
                    )


if __name__ == "__main__":
    unittest.main()
