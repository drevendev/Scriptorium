import unittest
from pathlib import Path
from unittest.mock import patch

from scriptorium.darwin_page_freeze import EXPECTED_PAGE_COUNT, expected_page_sequences
from scriptorium.darwin_page_shards import load_sharded_manifest, replay_sharded_manifest


INDEX = (
    Path(__file__).resolve().parents[1]
    / "corpus/candidates/source-edition-traces/"
    "darwin-origin-species-rachinsky-1864-ru.page-revisions.index.json"
)


class DarwinPageShardTests(unittest.TestCase):
    def test_committed_shards_match_frozen_topology_and_remain_source_free(self):
        rows = load_sharded_manifest(INDEX)
        self.assertEqual(len(rows), EXPECTED_PAGE_COUNT)
        self.assertEqual(tuple(row["page_sequence"] for row in rows), expected_page_sequences())
        self.assertEqual(len({row["revision_id"] for row in rows}), EXPECTED_PAGE_COUNT)
        self.assertNotIn(114, {row["page_sequence"] for row in rows})
        self.assertNotIn(411, {row["page_sequence"] for row in rows})
        self.assertEqual(rows[0]["page_sequence"], 8)
        self.assertEqual(rows[-1]["page_sequence"], 427)
        self.assertEqual(
            set(rows[0]),
            {"page_sequence", "title", "revision_id", "timestamp", "mediawiki_sha1"},
        )

    def test_replay_receipt_keeps_all_downstream_gates_closed(self):
        rows = load_sharded_manifest(INDEX)
        fetched = {
            int(row["revision_id"]): {
                "title": row["title"],
                "timestamp": row["timestamp"],
                "mediawiki_sha1": row["mediawiki_sha1"],
            }
            for row in rows
        }
        with patch("scriptorium.darwin_page_shards._pinned_revision_query", return_value=fetched):
            receipt = replay_sharded_manifest(INDEX)
        self.assertEqual(receipt["page_revision_count"], 418)
        self.assertTrue(receipt["identity_replay_match"])
        self.assertFalse(receipt["source_text_included"])
        self.assertFalse(receipt["literary_body_frozen"])
        self.assertFalse(receipt["admitted_for_calibration"])
        self.assertEqual(receipt["fantlab_source_edition_match"], "unknown")
        self.assertFalse(receipt["m2_parity_admissible"])


if __name__ == "__main__":
    unittest.main()
