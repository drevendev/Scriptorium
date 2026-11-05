"""Offline assertions for reviewed Paris Page-identity snapshot; no book text."""
from __future__ import annotations

from contextlib import redirect_stderr, redirect_stdout
from io import StringIO
import unittest
from unittest.mock import patch

from scriptorium import white_guard_paris_manifest as manifest

PRIVATE = "PRIVATE_MANUSCRIPT_DO_NOT_EXPOSE"


class WhiteGuardParisManifestTests(unittest.TestCase):
    def test_real_committed_snapshot_is_complete_and_offline(self):
        rows = manifest.load_rows()
        self.assertEqual(len(rows), 185)
        self.assertEqual([r["page_number"] for r in rows], list(range(5, 190)))
        self.assertEqual(rows[0]["revision_id"], 4412570)
        self.assertEqual(rows[-1]["revision_id"], 4490374)
        self.assertEqual(rows[0]["chapter"], 1)
        self.assertEqual(rows[-1]["chapter"], 11)
        output = manifest.build_receipt()
        self.assertEqual(output["recheck"], "NOT_RUN")
        self.assertFalse(output["m2_parity_admissible"])
        self.assertFalse(output["single_edition_body_frozen"])
        self.assertNotIn(PRIVATE, str(output))

    def test_provider_replays_exact_oldids_without_prose(self):
        rows = manifest.load_rows()
        def replayer(expected):
            self.assertEqual(len(expected), 185)
            self.assertEqual(set(expected[0]), {"title", "page_id", "revision_id", "revision_timestamp", "mediawiki_sha1"})
            return {r["title"]: {key: r[key] for key in (
                "page_id", "revision_id", "revision_timestamp", "mediawiki_sha1")} for r in expected}
        manifest.verify_rows(rows, replayer=replayer)

    def test_rejects_bad_rows_and_duplicate_identities(self):
        raw = manifest.CSV_PATH.read_text(encoding="utf-8")
        for broken in (raw.replace("5,476274", "6,476274", 1),
                       raw.replace("4412570", "0", 1),
                       raw.replace("2022-05-02", "2022-15-02", 1),
                       raw.replace("1af33492", PRIVATE, 1),
                       raw.replace("476275", "476274", 1),
                       raw.replace("page_number,", "page,", 1),
                       raw.rsplit("\n", 2)[0] + "\n"):
            with self.subTest(broken=broken[:80]):
                with self.assertRaises(ValueError):
                    manifest.parse_rows(broken)

    def test_sha_guard_and_provider_drift_abort(self):
        rows = manifest.load_rows()
        with patch.object(manifest, "CSV_SHA256", "0" * 64):
            with self.assertRaises(ValueError):
                manifest.load_rows()
        with self.assertRaises(ValueError):
            manifest.verify_rows(rows, replayer=lambda _: {})
        def drift(expected):
            output = {r["title"]: {key: r[key] for key in (
                "page_id", "revision_id", "revision_timestamp", "mediawiki_sha1")} for r in expected}
            output[expected[0]["title"]]["mediawiki_sha1"] = "f" * 40
            return output
        with self.assertRaises(ValueError):
            manifest.verify_rows(rows, replayer=drift)

    def test_cli_never_leaks_provider_errors_or_partial_receipt(self):
        stdout, stderr = StringIO(), StringIO()
        with patch.object(manifest, "build_receipt", side_effect=RuntimeError(PRIVATE)):
            with redirect_stdout(stdout), redirect_stderr(stderr):
                result = manifest.main(["--verify-provider"])
        self.assertEqual(result, 2)
        self.assertEqual(stdout.getvalue(), "")
        self.assertNotIn(PRIVATE, stderr.getvalue())
        self.assertIn("no receipt issued", stderr.getvalue())


if __name__ == "__main__":
    unittest.main()
