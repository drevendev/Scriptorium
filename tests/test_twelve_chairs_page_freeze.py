import copy
import json
from hashlib import sha256
from pathlib import Path
from tempfile import TemporaryDirectory
import unittest

from scriptorium.twelve_chairs_page_freeze import (
    CANDIDATE_ID,
    EXPECTED_PAGE_COUNT,
    FIELDS,
    INDEX_VERSION,
    NON_TRANSCLUDED_GAPS,
    PAGE_TITLE_PREFIX,
    SHARD_VERSION,
    build_capture_manifest,
    expected_page_sequences,
    expected_pages,
    load_sharded_manifest,
    replay_sharded_manifest,
    validate_capture_manifest,
)


class TwelveChairsPageFreezeTests(unittest.TestCase):
    def _capture(self):
        def fetcher(pages):
            return {
                str(row["title"]): {
                    "revision_id": 2_000_000 + int(row["page_sequence"]),
                    "timestamp": "2026-09-20T00:00:00Z",
                    "mediawiki_sha1": f"sha1-{int(row['page_sequence']):03d}",
                }
                for row in pages
            }

        return build_capture_manifest(fetcher=fetcher, captured_at="2026-09-20T00:00:00Z")

    def _write_sharded(self, root: Path, capture):
        rows = validate_capture_manifest(capture)
        rel_dir = Path("corpus/candidates/source-edition-traces")
        out_dir = root / rel_dir
        out_dir.mkdir(parents=True)
        specs = []
        for index, start in enumerate(range(0, len(rows), 103), start=1):
            batch = rows[start : start + 103]
            payload = {
                "shard_version": SHARD_VERSION,
                "candidate_id": CANDIDATE_ID,
                "fields": FIELDS,
                "page_identities": [
                    [row["page_sequence"], row["revision_id"], row["timestamp"], row["mediawiki_sha1"]]
                    for row in batch
                ],
                "source_text_included": False,
            }
            path = out_dir / f"ilf-petrov-twelve-chairs-zif-1928.page-revisions.{index:02d}.json"
            raw = (json.dumps(payload, ensure_ascii=False, indent=2, sort_keys=True) + "\n").encode()
            path.write_bytes(raw)
            specs.append(
                {
                    "path": str(rel_dir / path.name),
                    "sha256": sha256(raw).hexdigest(),
                    "row_count": len(batch),
                    "first_page_sequence": batch[0]["page_sequence"],
                    "last_page_sequence": batch[-1]["page_sequence"],
                }
            )
        index_payload = {
            "manifest_version": INDEX_VERSION,
            "candidate_id": CANDIDATE_ID,
            "family_id": "wikisource-zif-1928-first-standalone-edition",
            "title_prefix": PAGE_TITLE_PREFIX,
            "page_identity_fields": FIELDS,
            "page_identity_count": EXPECTED_PAGE_COUNT,
            "topology_contract": {
                "ranges": [[8, 149], [152, 313], [316, 421]],
                "non_transcluded_gaps": [[150, 151], [314, 315]],
            },
            "source_text_included": False,
            "literary_body_frozen": False,
            "admitted_for_calibration": False,
            "fantlab_source_edition_match": "unknown",
            "diagnostic_ready": False,
            "m2_parity_admissible": False,
            "shards": specs,
        }
        index_path = out_dir / "ilf-petrov-twelve-chairs-zif-1928.page-revisions.index.json"
        index_path.write_text(json.dumps(index_payload, ensure_ascii=False, indent=2, sort_keys=True) + "\n")
        return index_path

    def test_topology_is_exactly_410_dependencies_and_excludes_gaps(self):
        sequences = expected_page_sequences()
        self.assertEqual(len(sequences), EXPECTED_PAGE_COUNT)
        self.assertEqual(sequences[0], 8)
        self.assertEqual(sequences[-1], 421)
        self.assertEqual(NON_TRANSCLUDED_GAPS, ((150, 151), (314, 315)))
        for page in (150, 151, 314, 315):
            self.assertNotIn(page, sequences)
        self.assertEqual(len(set(sequences)), EXPECTED_PAGE_COUNT)

    def test_capture_is_source_free_and_gate_closed(self):
        capture = self._capture()
        rows = validate_capture_manifest(capture)
        self.assertEqual(capture["candidate_id"], CANDIDATE_ID)
        self.assertFalse(capture["source_text_included"])
        self.assertFalse(capture["literary_body_frozen"])
        self.assertFalse(capture["admitted_for_calibration"])
        self.assertFalse(capture["diagnostic_ready"])
        self.assertFalse(capture["m2_parity_admissible"])
        self.assertEqual(capture["fantlab_source_edition_match"], "unknown")
        self.assertEqual(len(rows), EXPECTED_PAGE_COUNT)

    def test_capture_validation_rejects_payload_drift_and_gate_promotion(self):
        capture = self._capture()
        with_payload = copy.deepcopy(capture)
        with_payload["pages"][0]["wikitext"] = "forbidden"
        with self.assertRaisesRegex(ValueError, "shape drift"):
            validate_capture_manifest(with_payload)
        missing = copy.deepcopy(capture)
        missing["pages"].pop()
        with self.assertRaisesRegex(ValueError, "exactly 410"):
            validate_capture_manifest(missing)
        promoted = copy.deepcopy(capture)
        promoted["diagnostic_ready"] = True
        with self.assertRaisesRegex(ValueError, "must remain false"):
            validate_capture_manifest(promoted)

    def test_sharded_manifest_and_replay_require_exact_identity(self):
        capture = self._capture()
        with TemporaryDirectory() as tmp:
            root = Path(tmp)
            index_path = self._write_sharded(root, capture)
            rows = load_sharded_manifest(index_path)
            self.assertEqual(len(rows), EXPECTED_PAGE_COUNT)
            expected = {
                int(row["revision_id"]): {
                    "title": row["title"],
                    "timestamp": row["timestamp"],
                    "mediawiki_sha1": row["mediawiki_sha1"],
                }
                for row in rows
            }
            receipt = replay_sharded_manifest(index_path, fetcher=lambda revision_ids: expected)
            self.assertTrue(receipt["identity_replay_match"])
            self.assertEqual(receipt["page_revision_count"], EXPECTED_PAGE_COUNT)
            self.assertFalse(receipt["source_text_included"])
            self.assertFalse(receipt["diagnostic_ready"])
            broken = copy.deepcopy(expected)
            broken[next(iter(broken))]["mediawiki_sha1"] = "different"
            with self.assertRaisesRegex(ValueError, "identity mismatch"):
                replay_sharded_manifest(index_path, fetcher=lambda revision_ids: broken)


if __name__ == "__main__":
    unittest.main()
