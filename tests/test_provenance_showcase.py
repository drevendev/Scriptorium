import json
import tempfile
import unittest
from pathlib import Path

from scriptorium.site_renderer import PublicationBuildError, build_site


class ProvenanceShowcaseTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.root = Path(self.temp.name) / "repo"
        (self.root / "site").mkdir(parents=True)
        (self.root / "public-artifacts").mkdir()
        self.output = self.root / "build" / "site"
        self.entry = {
            "entry_id": "example-provenance-v1",
            "kind": "work_showcase",
            "slug": "example-provenance",
            "title": "Example frozen provenance",
            "artifact_path": "public-artifacts/example.json",
            "artifact_schema": "scriptorium-work-provenance-showcase-v1",
            "publication_status": "diagnostic",
            "benchmark_admissibility": "diagnostic_only",
            "corpus_admissibility": "admissible",
            "compatibility_claim": "extension",
            "source_text_included": False,
        }
        digest = "a" * 64
        self.artifact = {
            "schema_version": "scriptorium-work-provenance-showcase-v1",
            "showcase_id": "example-provenance-v1",
            "status": "diagnostic",
            "benchmark_admissibility": "diagnostic_only",
            "corpus_admissibility": "admissible",
            "compatibility_claim": "extension",
            "source_text_committed": False,
            "representativeness_note": "Frozen source candidate; source match remains unknown.",
            "work": {"author": "Author", "title": "Work", "language": "ru"},
            "source": {
                "provider": "Example Source",
                "page": "Example page",
                "revision_url": "https://example.test/work?oldid=1",
                "edition_note": "Example edition",
                "legal_basis": "public domain",
                "revision_manifest": "corpus/candidates/source-edition-traces/example.revisions.json",
                "chapter_revision_count": 129,
                "composition_profile": "composite-v1",
                "extraction_profile": "extract-v1",
            },
            "frozen_identity": {
                "character_count_including_spaces": 400000,
                "utf8_byte_count": 700000,
                "raw_sha256": digest,
                "normalization_profile": "scriptorium-text-v1",
                "normalized_character_count_including_spaces": 400000,
                "normalized_sha256": digest,
            },
            "fantlab_boundary": {
                "work_id": 123,
                "analysis_url": "https://fantlab.ru/work123/lp",
                "analysis_date": "2022-09-19",
                "displayed_character_count": 390000,
                "displayed_word_count": 60000,
                "fantlab_source_edition_match": "unknown",
                "m2_parity_admissible": False,
                "note": "Numeric difference is not source-match evidence.",
            },
        }
        self._write()

    def tearDown(self):
        self.temp.cleanup()

    def _write(self):
        manifest = {
            "schema_version": "scriptorium-publication-manifest-v1",
            "generated_from": {"repository": "drevendev/Scriptorium", "branch": "master"},
            "deployment": {
                "publication_source": "github_actions",
                "generated_output_committed": False,
            },
            "entries": [self.entry],
        }
        (self.root / "site" / "publication-manifest.json").write_text(
            json.dumps(manifest), encoding="utf-8"
        )
        (self.root / "public-artifacts" / "example.json").write_text(
            json.dumps(self.artifact), encoding="utf-8"
        )

    def test_renders_source_free_frozen_identity_and_boundary(self):
        record = build_site(self.root, self.output)
        page = self.output / "works" / "example-provenance" / "index.html"
        html = page.read_text(encoding="utf-8")
        self.assertIn("provenance-only", html)
        self.assertIn("Pinned chapter revisions", html)
        self.assertIn("400000", html)
        self.assertIn("a" * 64, html)
        self.assertIn("Source-edition match", html)
        self.assertIn("unknown", html)
        self.assertIn("M2 parity admissible", html)
        self.assertIn("false", html)
        self.assertIn("Source text is deliberately not included", html)
        self.assertEqual(record["entries"][0]["route"], "works/example-provenance/")

    def test_source_match_or_parity_promotion_fails_closed(self):
        self.artifact["fantlab_boundary"]["fantlab_source_edition_match"] = "exact"
        self._write()
        with self.assertRaisesRegex(PublicationBuildError, "source-edition match"):
            build_site(self.root, self.output)

        self.artifact["fantlab_boundary"]["fantlab_source_edition_match"] = "unknown"
        self.artifact["fantlab_boundary"]["m2_parity_admissible"] = True
        self._write()
        with self.assertRaisesRegex(PublicationBuildError, "M2 parity inadmissible"):
            build_site(self.root, self.output)

    def test_compatibility_and_source_text_promotions_fail_closed(self):
        self.entry["compatibility_claim"] = "reproduced"
        self._write()
        with self.assertRaisesRegex(PublicationBuildError, "compatibility_claim"):
            build_site(self.root, self.output)

        self.entry["compatibility_claim"] = "extension"
        self.artifact["source_text_committed"] = True
        self._write()
        with self.assertRaisesRegex(PublicationBuildError, "commits source text"):
            build_site(self.root, self.output)


if __name__ == "__main__":
    unittest.main()
