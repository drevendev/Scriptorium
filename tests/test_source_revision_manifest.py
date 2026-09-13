import json
from pathlib import Path
import unittest

from scriptorium.source_revision_manifest import (
    EXPANDED_RECEIPT_VERSION,
    PACKED_MANIFEST_VERSION,
    canonical_json_text,
    chapter_identity_sha256,
    decode_chapter_identities,
    pack_revision_manifest,
)
from scriptorium.wikisource_freeze import expected_chapters


REPO_ROOT = Path(__file__).resolve().parents[1]
PACKED_MANIFEST = (
    REPO_ROOT
    / "corpus"
    / "candidates"
    / "source-edition-traces"
    / "tolstoy-anna-karenina-ru.revisions.json"
)
CAPTURED_IDENTITY_SHA256 = "fea96e084c769dfdec3a5fd55cbce34b061336441ba6edec70ebc830f5f83779"


class SourceRevisionManifestTests(unittest.TestCase):
    def setUp(self):
        self.manifest = json.loads(PACKED_MANIFEST.read_text(encoding="utf-8"))

    def test_packed_manifest_has_distinct_version_and_canonical_bytes(self):
        self.assertEqual(self.manifest["manifest_version"], PACKED_MANIFEST_VERSION)
        self.assertNotEqual(PACKED_MANIFEST_VERSION, EXPANDED_RECEIPT_VERSION)
        self.assertNotIn("chapters", self.manifest)
        self.assertIn("chapter_identity_encoding", self.manifest)
        self.assertEqual(
            PACKED_MANIFEST.read_text(encoding="utf-8"),
            canonical_json_text(self.manifest),
        )

    def test_all_239_captured_chapter_identities_decode_with_expected_title_order(self):
        decoded = decode_chapter_identities(self.manifest)
        expected = expected_chapters()
        self.assertEqual(len(decoded), 239)
        self.assertEqual(len(expected), 239)
        for expected_chapter, decoded_row in zip(expected, decoded, strict=True):
            for key in ("ordinal", "part", "chapter", "title"):
                self.assertEqual(decoded_row[key], expected_chapter[key])
        self.assertEqual(chapter_identity_sha256(decoded), CAPTURED_IDENTITY_SHA256)
        self.assertEqual(
            self.manifest["chapter_identity_encoding"]["captured_identity_sha256"],
            CAPTURED_IDENTITY_SHA256,
        )

    def test_source_free_expanded_identity_projection_repacks_exactly(self):
        decoded = decode_chapter_identities(self.manifest)
        expanded = {
            key: self.manifest[key]
            for key in (
                "bibliographic_source",
                "candidate_id",
                "composite_identity",
                "composition",
                "legal_basis",
                "provider",
                "source_work_index_revision_id",
                "source_work_url",
            )
        }
        expanded["manifest_version"] = EXPANDED_RECEIPT_VERSION
        expanded["chapters"] = [dict(row) for row in decoded]
        self.assertEqual(pack_revision_manifest(expanded), self.manifest)

    def test_packed_manifest_stores_no_source_prose(self):
        forbidden_exact_keys = {
            "body",
            "content",
            "prose",
            "source_text",
            "text",
            "wikitext",
        }

        def visit(value):
            if isinstance(value, dict):
                self.assertTrue(forbidden_exact_keys.isdisjoint(value))
                for child in value.values():
                    visit(child)
            elif isinstance(value, list):
                for child in value:
                    visit(child)

        visit(self.manifest)

    def test_decoder_fails_closed_on_identity_payload_length_drift(self):
        broken = json.loads(json.dumps(self.manifest))
        broken["chapter_identity_encoding"]["revision_ids"] = broken[
            "chapter_identity_encoding"
        ]["revision_ids"][:-1]
        with self.assertRaisesRegex(ValueError, "revision_id count mismatch"):
            decode_chapter_identities(broken)

    def test_decoder_fails_closed_on_capture_digest_drift(self):
        broken = json.loads(json.dumps(self.manifest))
        broken["chapter_identity_encoding"]["captured_identity_sha256"] = "0" * 64
        with self.assertRaisesRegex(ValueError, "captured identity digest mismatch"):
            decode_chapter_identities(broken)


if __name__ == "__main__":
    unittest.main()
