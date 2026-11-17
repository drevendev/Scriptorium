"""Positive/negative proof of safe source-bound descriptive tag preview."""
from copy import deepcopy
import json
import unittest

from scriptorium.tag_profile import VERSION, build_tag_profiles


def book(key, char_count, source_hash, comma=None, profile="scriptorium-metrics-v4", translator=None):
    rows = [
        {"id": "fantlab.general.characters", "actual": char_count, "status": "measured", "kind": "candidate"},
        {"id": "fantlab.general.mean_word_length_chars", "actual": 4.2 if key == "a" else 5.2, "status": "measured", "kind": "candidate"},
        {"id": "fantlab.punctuation.comma.per_1000_words", "actual": comma, "status": "measured" if comma is not None else "unavailable", "kind": "candidate"},
    ]
    return {"key": key, "candidate_id": "work-" + key, "edition_id": "edition-" + key,
            "source_sha256": source_hash * 64, "language": "ru", "translator": translator,
            "text_status": "measured", "profiles": {"metrics": profile, "normalization": "scriptorium-text-v1"},
            "metrics": rows}


def fixture():
    snap = {"schema": "scriptorium-ru-reader-v2", "scientific_claim": "DIAGNOSTIC_ONLY",
            "fantlab_input_identity": "UNKNOWN", "counts": {"m2_source_matched": 0},
            "comparability": {"m2_parity_admissible": False},
            "books": [book("a", 350000, "a", 10), book("b", 450000, "b", None)]}
    claims = []
    for key in ("a", "b"):
        claims.append({"key": key, "candidate_id": "work-" + key, "edition_id": "edition-" + key,
                       "source_sha256": key * 64, "language": "ru", "translator": None,
                       "rights": {"basis": "public_domain", "evidence_url": "https://example.org/rights/" + key, "reviewed": True},
                       "annotations": [{"tag_id": "historical", "authority": "documented_source",
                                        "certainty": "confirmed", "evidence_url": "https://example.org/tag/" + key}]})
    cur = {"schema": "scriptorium-tag-curation-v1", "taxonomy_version": "curated-tags-v1",
           "tags": [{"id": "historical", "label": "Historical fiction"}, {"id": "science", "label": "Science"}],
           "editions": claims}
    return snap, cur


class TagProfileTests(unittest.TestCase):
    def build(self, snapshot=None, curation=None):
        s, c = fixture()
        return build_tag_profiles(s if snapshot is None else snapshot,
                                  c if curation is None else curation, snapshot_sha256="f" * 64)

    def test_deterministic_aggregate_missingness_and_zero_sample(self):
        data = self.build()
        self.assertEqual(data["schema_version"], VERSION)
        self.assertFalse(data["scientific_boundary"]["public_release_ready"])
        historical, science = data["tags"]
        self.assertEqual(historical["confirmed_work_count"], 2)
        word = next(v for v in historical["metrics"] if v["id"].endswith("mean_word_length_chars"))
        self.assertEqual((word["mean_per_work"], word["population_stddev_between_works"]), (4.7, 0.5))
        comma = next(v for v in historical["metrics"] if v["id"].endswith("comma.per_1000_words"))
        self.assertEqual((comma["observed_count"], comma["missing_count"]), (1, 1))
        self.assertIsNone(comma["population_stddev_between_works"])
        self.assertEqual(science["confirmed_work_count"], 0)
        self.assertTrue(all(v["mean_per_work"] is None for v in science["metrics"]))
        self.assertEqual(json.dumps(data, sort_keys=True), json.dumps(self.build(), sort_keys=True))
        self.assertNotIn("PRIVATE PROSE", json.dumps(data))

    def test_single_work_has_no_dispersion(self):
        s, c = fixture()
        c["editions"][1]["annotations"][0]["certainty"] = "uncertain"
        result = self.build(s, c)["tags"][0]
        self.assertEqual(result["sample_warning"], "SINGLE_WORK")
        self.assertEqual(result["confirmed_work_count"], 1)
        self.assertIsNone(result["metrics"][0]["population_stddev_between_works"])

    def test_inferred_annotations_do_not_promote_corpus(self):
        s, c = fixture()
        for row in c["editions"]:
            row["annotations"][0]["certainty"] = "inferred"
        self.assertEqual(self.build(s, c)["tags"][0]["confirmed_work_count"], 0)

    def test_short_or_unmeasured_work_rejected(self):
        s, c = fixture()
        s["books"][0]["metrics"][0]["actual"] = 299999
        with self.assertRaisesRegex(ValueError, "full-length"):
            self.build(s, c)
        s, c = fixture()
        s["books"][0]["text_status"] = "research_only"
        with self.assertRaisesRegex(ValueError, "not a measured"):
            self.build(s, c)

    def test_unreviewed_or_unknown_rights_rejected(self):
        s, c = fixture()
        c["editions"][0]["rights"]["reviewed"] = False
        with self.assertRaisesRegex(ValueError, "rights"):
            self.build(s, c)
        s, c = fixture()
        c["editions"][0]["rights"]["basis"] = "web_accessible"
        with self.assertRaisesRegex(ValueError, "rights"):
            self.build(s, c)

    def test_source_translator_and_profile_drift_rejected(self):
        s, c = fixture()
        c["editions"][0]["translator"] = "Some other translator"
        with self.assertRaisesRegex(ValueError, "mismatch"):
            self.build(s, c)
        s, c = fixture()
        s["books"][1]["profiles"]["metrics"] = "other-version"
        with self.assertRaisesRegex(ValueError, "incompatible"):
            self.build(s, c)

    def test_duplicates_and_misbound_identity_rejected(self):
        s, c = fixture()
        c["editions"].append(deepcopy(c["editions"][0]))
        with self.assertRaisesRegex(ValueError, "duplicate edition"):
            self.build(s, c)
        s, c = fixture()
        s["books"][1]["source_sha256"] = "a" * 64
        c["editions"][1]["source_sha256"] = "a" * 64
        with self.assertRaisesRegex(ValueError, "duplicate work"):
            self.build(s, c)

    def test_bad_annotation_or_evidence_rejected(self):
        s, c = fixture()
        c["editions"][0]["annotations"][0]["tag_id"] = "fake-tag"
        with self.assertRaisesRegex(ValueError, "unknown"):
            self.build(s, c)
        s, c = fixture()
        c["editions"][0]["rights"]["evidence_url"] = "https://a:p@example.org/x"
        with self.assertRaisesRegex(ValueError, "URL"):
            self.build(s, c)

    def test_unknown_is_not_zero_and_nan_rejected(self):
        s, c = fixture()
        s["books"][0]["metrics"][1]["actual"] = float("nan")
        with self.assertRaisesRegex(ValueError, "invalid observed"):
            self.build(s, c)
        s, c = fixture()
        s["books"][0]["metrics"][1]["actual"] = None
        with self.assertRaisesRegex(ValueError, "invalid observed"):
            self.build(s, c)

    def test_extra_raw_text_field_is_refused(self):
        s, c = fixture()
        c["editions"][0]["source_text"] = "PRIVATE PROSE"
        with self.assertRaisesRegex(ValueError, "malformed edition"):
            self.build(s, c)

    def test_scientific_gate_must_fail_closed(self):
        s, c = fixture()
        s["comparability"]["m2_parity_admissible"] = True
        with self.assertRaisesRegex(ValueError, "scientific"):
            self.build(s, c)


if __name__ == "__main__":
    unittest.main()
