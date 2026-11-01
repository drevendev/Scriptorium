"""Eighth measured Russian Reader book: retained source-free Road evidence gates."""
from __future__ import annotations

from copy import deepcopy
from hashlib import sha1
import json
from pathlib import Path
import unittest

ROOT = Path(__file__).resolve().parents[1]
RETAINED_PATH = ROOT / "corpus/candidates/diagnostics/grin-road-nowhere-ru.retained.json"
SNAPSHOT_PATH = ROOT / "assets/evidence-snapshot.json"
BODY_HASH = "e33a28b8dcdb3ac339147c6587b27c182dd910784122b367db41bc93dfc2dbee"
CI_ARCHIVE_HASH = "55c39e7b0c4a69a9c86fe3afc7c1d9c63620c4f9d52eb23be4dd688cda6b39f0"
CI_JSON_HASH = "a0cfc008f9e8580a203e39c83a3e65755143c593038adaa275037bbed7dc1e92"


def assert_retained(artifact, book):
    assert artifact["candidate_id"] == book["candidate_id"] == "grin-road-nowhere-ru"
    assert artifact["source_text_committed"] is False
    assert artifact["body_identity"]["revision_id"] == book["source_revision_id"] == 5585836
    assert artifact["body_identity"]["raw_sha256"] == book["source_sha256"] == BODY_HASH
    assert artifact["body_identity"]["normalized_sha256"] == BODY_HASH
    assert artifact["source_evidence"]["original_ci_archive_sha256"] == CI_ARCHIVE_HASH
    assert artifact["source_evidence"]["original_ci_artifact_json_sha256"] == CI_JSON_HASH
    assert artifact["source_evidence"]["legal_basis"] == "public_domain"
    assert artifact["source_evidence"]["original_ci_head"] == "79c098fb42695af8a91498c21dc64ab4bc6422f2"
    assert artifact["comparison_policy"]["class"] == "diagnostic_unmatched_source"
    assert artifact["comparison_policy"]["reference_rounding_evidence"] == "UNKNOWN"
    assert artifact["gates"]["primary_1965_transcription_body_ready"] is False
    assert artifact["gates"]["m2_parity_admissible"] is False
    assert artifact["gates"]["m2_weight"] == 0
    assert book["edition_id"] == "ru-wikisource-az-lib-oldid-5585836"
    assert book["text_status"] == "measured"
    assert book["measured"] == 24
    assert book["unavailable"] == 5
    rows = artifact["metric_rows"]
    assert len(rows) == len(book["metrics"]) == 29
    assert len({r["metric_id"] for r in rows}) == 29
    assert sum(r["actual"] is not None for r in rows) == 24
    assert sum(r["actual"] is None for r in rows) == 5
    refs = {r["metric_id"] for r in rows if r["fantlab_display"] is not None}
    assert refs == {"fantlab.general.characters", "fantlab.general.words"}
    source = {r["metric_id"]: r for r in rows}
    for m in book["metrics"]:
        row = source[m["id"]]
        assert m["actual"] == row["actual"]
        assert m["reference"] == (None if row["fantlab_display"] is None else int(row["fantlab_display"]))
        assert m["status"] == ("measured" if row["actual"] is not None else "not_run")
        assert m["kind"] == ("extension" if row["compatibility_status"] == "extension" else "candidate")
    assert source["fantlab.general.characters"]["actual_minus_fantlab_display"] == 4217
    assert source["fantlab.general.words"]["actual_minus_fantlab_display"] == 3773


class RoadEighthReaderTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.artifact = json.loads(RETAINED_PATH.read_text(encoding="utf-8"))
        cls.catalog = json.loads(SNAPSHOT_PATH.read_text(encoding="utf-8"))
        cls.book = next(b for b in cls.catalog["books"] if b["key"] == "road")

    def test_frozen_rows_provenance_and_no_source_prose(self):
        assert_retained(self.artifact, self.book)
        raw = RETAINED_PATH.read_bytes()
        expected_blob = sha1(b"blob " + str(len(raw)).encode("ascii") + b"\0" + raw).hexdigest()
        self.assertEqual(self.book["blob_sha1"], expected_blob)
        self.assertNotIn("wikitext", self.artifact)
        self.assertNotIn("literary_body", self.artifact)
        self.assertFalse(self.artifact["source_text_committed"])

    def test_catalogue_consistency_and_non_parity(self):
        self.assertEqual(self.catalog["counts"], {
            "work_count": 13, "measured_works": 11, "awaiting_measurement": 2,
            "metrics_total": 298, "numeric_total": 249, "unavailable_total": 49,
            "m2_source_matched": 0
        })
        self.assertEqual([b["key"] for b in self.catalog["books"] if b["text_status"] != "measured"],
                         ["petersburg", "darwin"])
        self.assertFalse(self.catalog["comparability"]["m2_parity_admissible"])
        html = (ROOT / "index.html").read_text(encoding="utf-8")
        self.assertIn('data-status="measured" data-catalog-key="road"', html)
        self.assertIn('data-book="road"', html)
        self.assertIn('Дорога в никуда</th><td>45.31181857828172</td><td>%</td>', html)
        self.assertIn("не редакция «Правды» 1965 года", html)

    def test_tampering_with_source_hash_reference_or_parity_rejected(self):
        for mutate in (
            lambda a, b: a["gates"].__setitem__("m2_parity_admissible", True),
            lambda a, b: a["body_identity"].__setitem__("raw_sha256", "0" * 64),
            lambda a, b: b["metrics"][4].__setitem__("actual", 1),
            lambda a, b: a["metric_rows"][4].__setitem__("fantlab_display", "442656"),
        ):
            artifact, book = deepcopy(self.artifact), deepcopy(self.book)
            mutate(artifact, book)
            with self.assertRaises(AssertionError):
                assert_retained(artifact, book)


if __name__ == "__main__":
    unittest.main()
