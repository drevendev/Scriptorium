"""Exact CI-artifact retention for a real tenth Russian work; no source prose."""
from __future__ import annotations
import copy
import hashlib
import json
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PATH = ROOT / "corpus/candidates/diagnostics/dostoevsky-humiliated-and-insulted-ru.retained.json"
EXPECTED_JSON_SHA256 = "bcd4e9cde2aa75364ef458749c9b1f26b72b75e1ab8df0d70c4fc6f3f018a634"
BODY_SHA = "ffc6825db7f442c7df93136e8ddf90ce44be8801cdbaa727d5fe642db3fad8fa"
WIKITEXT_SHA = "c8e46b8a1948d34b5fc0fb6db8091c990701eeae0c09a8ef83d941dce6131d68"


def validate(d):
    assert d["version"] == "scriptorium-humiliated-azlib-literary-measurement-v1"
    assert d["candidate_id"] == "dostoevsky-humiliated-and-insulted-azlib-ru"
    assert d["analysis_language"] == d["original_language"] == "ru"
    assert d["translator"] is None
    assert d["gates"]["comparison_class"] == "DIAGNOSTIC_ONLY"
    assert d["gates"]["fantlab_input_identity"] == "UNKNOWN"
    assert d["gates"]["m2_weight"] == 0
    assert d["gates"]["m2_parity_admissible"] is False
    assert d["gates"]["complete_chapter_inventory"] is True
    assert d["gates"]["minimum_300000_characters"] is True
    assert d["gates"]["source_text_committed"] is False
    assert d["gates"]["source_edition_print_collation"] == "NOT_RUN"
    assert d["source"]["revision_id"] == 5611473
    assert d["source"]["page_id"] == 1016220
    assert d["source"]["legal_basis"] == "public_domain_original_author_died_1881"
    assert d["source"]["wikitext_sha256"] == WIKITEXT_SHA
    assert d["source"]["edition_identity_independently_matched"] is False
    assert d["body"]["characters_including_spaces"] == 713925
    assert d["body"]["raw_sha256"] == d["body"]["normalized_sha256"] == BODY_SHA
    rows = d["metric_rows"]
    assert len(rows) == len({r["metric_id"] for r in rows}) == 29
    assert sum(isinstance(r["actual"], (float, int)) for r in rows) == 24
    assert sum(r["actual"] is None for r in rows) == 5
    assert all(r["fantlab_display"] is None for r in rows)
    for r in rows:
        assert r["result"] == ("NOT_RUN_DICTIONARY_UNBOUND" if r["actual"] is None else
                              "MEASURED_REFERENCE_UNAVAILABLE")
        assert r["compatibility_status"] in ("inferred", "extension")
    fields = {r["metric_id"]: r["actual"] for r in rows}
    assert fields["fantlab.general.characters"] == 713925
    assert fields["fantlab.general.words"] == 118157
    assert fields["fantlab.vocabulary.unique_words"] == 17066
    assert fields["scriptorium.general.sentences"] == 10381
    assert abs(fields["fantlab.dialogue.share_percent"] - 56.66327827623132) < 1e-12


class RetainedDostoevskyEvidenceTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.raw = PATH.read_bytes()
        cls.data = json.loads(cls.raw)

    def test_exact_archived_ci_bytes_and_record(self):
        self.assertEqual(hashlib.sha256(self.raw).hexdigest(), EXPECTED_JSON_SHA256)
        validate(self.data)

    def test_no_literary_body_in_public_artifact(self):
        self.assertNotIn("chapters", self.data)
        self.assertNotIn("literary_text", self.data)
        self.assertNotIn("wikitext", self.data)
        self.assertNotIn("raw_text", self.data)

    def test_tampered_identity_and_m2_claim_rejected(self):
        for mutate in (
            lambda d: d["source"].__setitem__("revision_id", 5611474),
            lambda d: d["body"].__setitem__("raw_sha256", "0"*64),
            lambda d: d["gates"].__setitem__("m2_weight", 1),
            lambda d: d["metric_rows"][4].__setitem__("actual", 713926),
            lambda d: d["metric_rows"][-1].__setitem__("metric_id", "fantlab.general.characters"),
        ):
            altered = copy.deepcopy(self.data)
            mutate(altered)
            with self.assertRaises(AssertionError):
                validate(altered)


if __name__ == "__main__":
    unittest.main()
