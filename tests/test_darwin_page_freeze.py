import copy
import unittest

from scriptorium.darwin_page_freeze import (
    CANDIDATE_ID,
    EXPECTED_PAGE_COUNT,
    EXPLICIT_NO_TEXT_NON_DEPENDENCIES,
    build_manifest,
    expected_page_sequences,
    expected_pages,
    replay_manifest,
    validate_manifest,
)


class DarwinPageFreezeTests(unittest.TestCase):
    def _manifest(self):
        inventory = expected_pages()

        def fetcher(pages):
            return {
                str(row["title"]): {
                    "revision_id": 1_000_000 + int(row["page_sequence"]),
                    "timestamp": "2026-09-19T00:00:00Z",
                    "mediawiki_sha1": f"sha1-{int(row['page_sequence']):03d}",
                }
                for row in pages
            }

        return build_manifest(fetcher=fetcher, captured_at="2026-09-19T00:00:00Z")

    def test_expected_topology_is_exactly_418_included_pages(self):
        sequences = expected_page_sequences()
        self.assertEqual(len(sequences), EXPECTED_PAGE_COUNT)
        self.assertEqual(sequences[0], 8)
        self.assertEqual(sequences[-1], 427)
        self.assertNotIn(114, sequences)
        self.assertNotIn(411, sequences)
        self.assertEqual(EXPLICIT_NO_TEXT_NON_DEPENDENCIES, (114, 411))
        self.assertEqual(len(set(sequences)), EXPECTED_PAGE_COUNT)

    def test_build_manifest_is_source_free_and_gate_closed(self):
        manifest = self._manifest()
        rows = validate_manifest(manifest)
        self.assertEqual(manifest["candidate_id"], CANDIDATE_ID)
        self.assertFalse(manifest["source_text_included"])
        self.assertFalse(manifest["literary_body_frozen"])
        self.assertFalse(manifest["admitted_for_calibration"])
        self.assertEqual(manifest["fantlab_source_edition_match"], "unknown")
        self.assertFalse(manifest["m2_parity_admissible"])
        self.assertEqual(len(rows), EXPECTED_PAGE_COUNT)
        self.assertEqual(
            set(rows[0]),
            {
                "ordinal",
                "page_sequence",
                "title",
                "revision_id",
                "timestamp",
                "mediawiki_sha1",
                "permanent_url",
            },
        )

    def test_validation_fails_closed_on_source_payload_or_inventory_drift(self):
        manifest = self._manifest()
        with_payload = copy.deepcopy(manifest)
        with_payload["pages"][0]["wikitext"] = "must never be committed"
        with self.assertRaisesRegex(ValueError, "shape drift"):
            validate_manifest(with_payload)

        missing = copy.deepcopy(manifest)
        missing["pages"].pop()
        with self.assertRaisesRegex(ValueError, "exactly 418"):
            validate_manifest(missing)

        promoted = copy.deepcopy(manifest)
        promoted["admitted_for_calibration"] = True
        with self.assertRaisesRegex(ValueError, "must remain false"):
            validate_manifest(promoted)

    def test_replay_requires_exact_pinned_identity_match(self):
        manifest = self._manifest()
        expected = {
            int(row["revision_id"]): {
                "title": row["title"],
                "timestamp": row["timestamp"],
                "mediawiki_sha1": row["mediawiki_sha1"],
            }
            for row in manifest["pages"]
        }

        receipt = replay_manifest(manifest, fetcher=lambda revision_ids: expected)
        self.assertTrue(receipt["identity_replay_match"])
        self.assertEqual(receipt["page_revision_count"], EXPECTED_PAGE_COUNT)
        self.assertFalse(receipt["source_text_included"])
        self.assertFalse(receipt["admitted_for_calibration"])
        self.assertFalse(receipt["m2_parity_admissible"])

        broken = copy.deepcopy(expected)
        first_revision = next(iter(broken))
        broken[first_revision]["mediawiki_sha1"] = "different"
        with self.assertRaisesRegex(ValueError, "identity mismatch"):
            replay_manifest(manifest, fetcher=lambda revision_ids: broken)


if __name__ == "__main__":
    unittest.main()
