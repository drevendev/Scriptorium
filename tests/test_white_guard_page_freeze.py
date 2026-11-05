"""Synthetic, source-free regression tests for Paris ProofreadPage identity capture."""
from __future__ import annotations

import copy
from datetime import datetime
import io
import json
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch

from scriptorium import white_guard_page_freeze as freeze

SENTINEL = "DO_NOT_SERIALIZE_PRIVATE_PROSE"


class WhiteGuardParisPageFreezeTests(unittest.TestCase):
    def records(self):
        return {
            row["title"]: {
                "revision_id": 900_000 + row["page_sequence"],
                "timestamp": "2026-11-05T02:00:00Z",
                "mediawiki_sha1": f"{row['page_sequence']:040x}",
            }
            for row in freeze.expected_pages()
        }

    def manifest(self):
        return freeze.build_manifest(
            fetcher=lambda _pages: self.records(),
            captured_at="2026-11-05T02:01:00Z",
        )

    def test_complete_topology_and_chapter_boundaries(self):
        rows = freeze.expected_pages()
        self.assertEqual(len(rows), 185)
        self.assertEqual([r["page_sequence"] for r in rows], list(range(5, 190)))
        self.assertEqual(rows[0]["chapter"], 1)
        self.assertEqual(rows[4]["chapter"], 1)
        self.assertEqual(rows[5]["chapter"], 2)
        self.assertEqual(rows[-1]["chapter"], 11)
        self.assertTrue(all(r["title"].startswith("Страница:") for r in rows))
        self.assertEqual(len(set(r["title"] for r in rows)), 185)

    def test_capture_and_replay_are_exact_and_never_publish_text(self):
        manifest = self.manifest()
        rows = freeze.validate_manifest(manifest)
        self.assertEqual(len(rows), 185)
        self.assertFalse(manifest["literary_body_frozen"])
        self.assertFalse(manifest["m2_parity_admissible"])
        self.assertEqual(manifest["capture_basis"], "CURRENT_PAGE_REVISIONS")
        identities = {
            int(row["revision_id"]): {
                "title": row["title"],
                "timestamp": row["timestamp"],
                "mediawiki_sha1": row["mediawiki_sha1"],
            }
            for row in rows
        }
        receipt = freeze.replay_manifest(manifest, fetcher=lambda _ids: identities)
        self.assertEqual(receipt["page_revision_count"], 185)
        self.assertTrue(receipt["identity_replay_match"])
        self.assertFalse(receipt["source_text_included"])
        self.assertNotIn(SENTINEL, json.dumps(manifest) + json.dumps(receipt))
        self.assertEqual(len(receipt["manifest_sha256"]), 64)

    def test_missing_extra_and_untrusted_provider_rows_fail_closed(self):
        original = self.records()
        for change in ("missing", "extra", "prose", "badsha", "boolrevid"):
            with self.subTest(change=change):
                records = copy.deepcopy(original)
                title = freeze.expected_pages()[0]["title"]
                if change == "missing":
                    del records[title]
                elif change == "extra":
                    records["Страница:unapproved.djvu/1"] = records[title]
                elif change == "prose":
                    records[title]["wikitext"] = SENTINEL
                elif change == "badsha":
                    records[title]["mediawiki_sha1"] = "not-a-sha"
                else:
                    records[title]["revision_id"] = True
                with self.assertRaises(ValueError):
                    freeze.build_manifest(
                        fetcher=lambda _pages: records,
                        captured_at="2026-11-05T02:01:00Z",
                    )

    def test_manifest_rejects_prose_reordering_duplicate_revision_and_invalid_gate(self):
        base = self.manifest()
        for change in ("prose", "order", "duplicate", "gate", "wrongurl", "timestamp"):
            with self.subTest(change=change):
                manifest = copy.deepcopy(base)
                if change == "prose":
                    manifest["pages"][0]["text"] = SENTINEL
                elif change == "order":
                    manifest["pages"][0], manifest["pages"][1] = (
                        manifest["pages"][1], manifest["pages"][0]
                    )
                elif change == "duplicate":
                    manifest["pages"][1]["revision_id"] = manifest["pages"][0]["revision_id"]
                elif change == "gate":
                    manifest["literary_body_frozen"] = True
                elif change == "wrongurl":
                    manifest["pages"][0]["permanent_url"] = "https://invalid.example/"
                else:
                    manifest["captured_at_utc"] = "not a timestamp"
                with self.assertRaises(ValueError):
                    freeze.validate_manifest(manifest)

    def test_replay_rejects_drift_and_partial_inventory(self):
        manifest = self.manifest()
        identities = {
            int(row["revision_id"]): {
                "title": row["title"],
                "timestamp": row["timestamp"],
                "mediawiki_sha1": row["mediawiki_sha1"],
            }
            for row in manifest["pages"]
        }
        for change in ("missing", "hash", "title", "extra"):
            with self.subTest(change=change):
                records = copy.deepcopy(identities)
                first = manifest["pages"][0]["revision_id"]
                if change == "missing":
                    del records[first]
                elif change == "hash":
                    records[first]["mediawiki_sha1"] = "0" * 40
                elif change == "title":
                    records[first]["title"] = "Страница:other"
                else:
                    records[123456] = records[first]
                with self.assertRaises(ValueError):
                    freeze.replay_manifest(manifest, fetcher=lambda _ids: records)

    def test_cli_does_not_log_provider_private_exception(self):
        class PrivateFailure(Exception):
            pass

        with tempfile.TemporaryDirectory() as directory:
            target = Path(directory) / "capture.json"
            with patch.object(freeze, "build_manifest", side_effect=PrivateFailure(SENTINEL)):
                with patch("sys.stderr", new_callable=io.StringIO) as stderr:
                    code = freeze.main(["capture", "--manifest", str(target)])
            self.assertEqual(code, 2)
            self.assertFalse(target.exists())
            self.assertNotIn(SENTINEL, stderr.getvalue())
            self.assertNotIn("Traceback", stderr.getvalue())


if __name__ == "__main__":
    unittest.main()
