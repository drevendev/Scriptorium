"""Offline regressions for the independent Bely/Tolstoy lexical bridge."""
import hashlib
import json
from pathlib import Path
import unittest
from unittest.mock import Mock, patch

from scriptorium import bely_tolstoy_lexical_pair as target

TRACES = Path(__file__).resolve().parents[1] / "corpus/candidates/source-edition-traces"


def read(name):
    return json.loads((TRACES / name).read_text(encoding="utf-8"))


def identity(text):
    raw = text.encode("utf-8")
    return {"character_count_including_spaces": len(text),
            "utf8_byte_count": len(raw), "raw_sha256": hashlib.sha256(raw).hexdigest(),
            "normalized_sha256": hashlib.sha256(raw).hexdigest()}


class CrossAuthorPairTests(unittest.TestCase):
    def setUp(self):
        self.left = "берёза " * 8 + "снег " * 2
        self.right = "луч " * 7 + "снег " * 3
        self.a, self.b = identity(self.left), identity(self.right)
        self.dove = read("bely-silver-dove-ru.revisions.json")
        self.rev = read("tolstoy-hyperboloid-garin-wikisource-ru.revision.json")
        self.body = read("tolstoy-hyperboloid-garin-wikisource-ru.body.json")

    def test_numeric_only_deterministic_result(self):
        result = target._assemble(self.left, self.right, self.a, self.b)
        self.assertEqual(result, target._assemble(self.left, self.right, self.a, self.b))
        self.assertEqual(result["schema_version"], target.SCHEMA)
        self.assertFalse(result["source_text_included"])
        self.assertFalse(result["m2_parity_admissible"])
        self.assertEqual(result["public_reader_release"], "REQUIRES_SEPARATE_REVIEW")
        report = result["lexical_contrast"]
        self.assertEqual(report["status"], "COMPARABLE")
        self.assertFalse(report["public_release_ready"])
        self.assertEqual(report["corpus_admission"], "NOT_VERIFIED")
        self.assertEqual(result["source_evidence"]["left"]["revision_id"], 5588003)
        self.assertEqual(result["source_evidence"]["right"]["revision_id"], 5014458)
        for word in ("берёза", "снег", "луч"):
            self.assertNotIn(word, json.dumps(result, ensure_ascii=False))

    def test_body_drift_and_identical_text(self):
        with self.assertRaisesRegex(ValueError, "identity drift"):
            target._assemble(self.left, self.right + "!", self.a, self.b)
        with self.assertRaisesRegex(ValueError, "not comparable"):
            target._assemble(self.left, self.left, self.a, self.a)
        with self.assertRaisesRegex(ValueError, "not comparable"):
            target._assemble(self.left, self.right, self.a,
                             {**self.b, "normalized_sha256": "0" * 64})

    def test_both_canonical_pins_checked_before_network(self):
        for left, right, body in (
            ({**self.dove, "legal_basis": "unknown"}, self.rev, self.body),
            (self.dove, {**self.rev, "legal_basis": "unknown"}, self.body),
            (self.dove, self.rev, {**self.body, "literary_body_identity": {
                **self.body["literary_body_identity"], "raw_sha256": "0" * 64}}),
        ):
            with self.subTest(left=left["legal_basis"], right=right["legal_basis"]):
                a, b = Mock(), Mock()
                with self.assertRaises(ValueError):
                    target.build_pinned_pair(left, right, body, dove_fetcher=a, garin_fetcher=b)
                a.assert_not_called()
                b.assert_not_called()

    def test_failed_left_replay_prevents_right_fetch(self):
        a, b = Mock(return_value={}), Mock()
        with self.assertRaisesRegex(ValueError, "source inventory"):
            target.build_pinned_pair(self.dove, self.rev, self.body,
                                     dove_fetcher=a, garin_fetcher=b)
        a.assert_called_once()
        b.assert_not_called()

    def test_unverified_receipt_prevents_analysis(self):
        with patch.object(target.dove.freeze, "replay_manifest", return_value={}), \
                patch.object(target, "_assemble") as assemble:
            b = Mock()
            with self.assertRaisesRegex(ValueError, "replay evidence drift"):
                target.build_pinned_pair(self.dove, self.rev, self.body, garin_fetcher=b)
            b.assert_not_called()
            assemble.assert_not_called()


if __name__ == "__main__":
    unittest.main()
