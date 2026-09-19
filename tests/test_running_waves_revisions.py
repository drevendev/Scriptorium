from __future__ import annotations

import copy
import unittest

from scriptorium.running_waves_revisions import (
    CANDIDATE_ID,
    MANIFEST_VERSION,
    build_manifest,
    expected_pages,
    replay_manifest,
    validate_manifest,
)


class RunningWavesRevisionTests(unittest.TestCase):
    def _records(self):
        return {
            page["title"]: {
                "page_id": 1000 + page["ordinal"],
                "revision_id": 2000 + page["ordinal"],
                "revision_timestamp": f"2026-01-{((page['ordinal'] - 1) % 28) + 1:02d}T00:00:00Z",
                "mediawiki_sha1": f"{page['ordinal']:040x}",
            }
            for page in expected_pages()
        }

    def test_expected_route_is_35_numbered_pages_plus_epilogue(self):
        pages = expected_pages()
        self.assertEqual(36, len(pages))
        self.assertTrue(str(pages[0]["title"]).endswith("/1"))
        self.assertTrue(str(pages[34]["title"]).endswith("/35"))
        self.assertTrue(str(pages[35]["title"]).endswith("/Эпилог"))

    def test_build_and_validate_manifest_is_source_free_and_ordered(self):
        records = self._records()
        manifest = build_manifest(fetcher=lambda pages: records)
        self.assertEqual(MANIFEST_VERSION, manifest["manifest_version"])
        self.assertEqual(CANDIDATE_ID, manifest["candidate_id"])
        self.assertTrue(manifest["capture_scope"]["literary_page_revisions_frozen"])
        self.assertFalse(manifest["capture_scope"]["literary_body_extraction_frozen"])
        self.assertFalse(manifest["capture_scope"]["composite_identity_frozen"])
        identities = validate_manifest(manifest)
        self.assertEqual(36, len(identities))
        self.assertEqual([row["title"] for row in expected_pages()], [row["title"] for row in identities])
        serialized = repr(manifest).lower()
        for forbidden in ("wikitext", "source_text", "literary_body"):
            self.assertNotIn(forbidden + "':", serialized)

    def test_manifest_rejects_route_order_drift(self):
        manifest = build_manifest(fetcher=lambda pages: self._records())
        manifest = copy.deepcopy(manifest)
        manifest["pages"][0], manifest["pages"][1] = manifest["pages"][1], manifest["pages"][0]
        with self.assertRaisesRegex(ValueError, "identity drift"):
            validate_manifest(manifest)

    def test_manifest_rejects_duplicate_revision_identity(self):
        manifest = build_manifest(fetcher=lambda pages: self._records())
        manifest = copy.deepcopy(manifest)
        manifest["pages"][1]["revision_id"] = manifest["pages"][0]["revision_id"]
        with self.assertRaisesRegex(ValueError, "duplicate revision id"):
            validate_manifest(manifest)

    def test_replay_verifies_all_pinned_titles_without_returning_content(self):
        manifest = build_manifest(fetcher=lambda pages: self._records())

        def replay_fetcher(identities):
            return {str(row["title"]): "ephemeral-prose-not-serialized" for row in identities}

        receipt = replay_manifest(manifest, fetcher=replay_fetcher)
        self.assertEqual(36, receipt["verified_literary_page_count"])
        self.assertFalse(receipt["source_text_committed"])
        self.assertFalse(receipt["literary_body_extraction_frozen"])
        self.assertFalse(receipt["composite_identity_frozen"])
        self.assertEqual("unknown", receipt["fantlab_source_edition_match"])


if __name__ == "__main__":
    unittest.main()
