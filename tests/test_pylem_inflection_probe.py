"""Independent oblique form POS controls: boundaries and receipt math."""
import json
from types import SimpleNamespace
import unittest

from tools.pylem_inflection_probe import CONTROL_GROUPS, build_oblique_n_observation


class FakeHolder:
    def __init__(self, labels):
        self.labels = labels

    def lemmatize(self, word):
        return [SimpleNamespace(part_of_speech=tag)
                for tag in self.labels.get(word, ())]


class InflectedNControlsTests(unittest.TestCase):
    def labels(self):
        return {
            **{word: ("N",) for word in CONTROL_GROUPS[0][1]},
            **{word: ("N",) for word in CONTROL_GROUPS[1][1]},
            **{word: ("CONJ",) for word in CONTROL_GROUPS[2][1]},
        }

    def test_source_free_positive_and_replay(self):
        labels = self.labels()
        labels["домами"] = ("N", "A")
        labels["тремя"] = ()
        report = build_oblique_n_observation(FakeHolder(labels))
        self.assertEqual(report, build_oblique_n_observation(FakeHolder(labels)))
        self.assertEqual(report["schema_version"], "scriptorium-aot-n-inflected-controls-v1")
        self.assertEqual([report["groups"][key]["n_only_count"] for key, _ in CONTROL_GROUPS],
                         [2, 2, 0])
        self.assertEqual(report["groups"]["noun_oblique_examples"]["n_mixed_count"], 1)
        self.assertEqual(report["negative_controls_usable"], 3)
        self.assertTrue(report["qualified_cross_role_n_observation"])
        self.assertFalse(report["source_text_included"])
        self.assertFalse(report["m2_parity_admissible"])
        self.assertFalse(report["production_pos_mapping_changed"])
        self.assertEqual(report["noun_cardinal_source_pos"], "unresolved")
        serialized = json.dumps(report, ensure_ascii=False)
        for _, words in CONTROL_GROUPS:
            for word in words:
                self.assertNotIn('"' + word + '"', serialized)
        for name in ("fixture_manifest_sha256", "runtime_observations_sha256"):
            self.assertEqual(len(report[name]), 64)

    def test_negative_and_inconclusive_controls(self):
        labels = self.labels()
        for word in CONTROL_GROUPS[1][1]:
            labels[word] = ("A",)
        self.assertFalse(build_oblique_n_observation(FakeHolder(labels))[
            "qualified_cross_role_n_observation"])
        labels = self.labels()
        for word in CONTROL_GROUPS[2][1]:
            labels[word] = ("N",)
        report = build_oblique_n_observation(FakeHolder(labels))
        self.assertEqual(report["negative_controls_usable"], 0)
        self.assertFalse(report["qualified_cross_role_n_observation"])
        labels = self.labels()
        for word in CONTROL_GROUPS[2][1][:2]:
            labels[word] = ()
        report = build_oblique_n_observation(FakeHolder(labels))
        self.assertEqual(report["negative_controls_usable"], 1)
        self.assertFalse(report["qualified_cross_role_n_observation"])

    def test_missing_analyses_and_bad_tags(self):
        empty = build_oblique_n_observation(FakeHolder({}))
        self.assertFalse(empty["cross_role_n_only_observed"])
        self.assertFalse(empty["qualified_cross_role_n_observation"])
        for wrong in ("", " ", None, True, 3, " N"):
            with self.subTest(tag=wrong):
                labels = self.labels()
                labels["столами"] = (wrong,)
                with self.assertRaises(ValueError):
                    build_oblique_n_observation(FakeHolder(labels))

    def test_group_invariants_and_digests(self):
        report = build_oblique_n_observation(FakeHolder(self.labels()))
        for group in report["groups"].values():
            self.assertEqual(group["n_only_count"] + group["n_mixed_count"],
                             group["n_present_count"])
            self.assertEqual(group["token_count"], len(group["tokens"]))
            for row in group["tokens"]:
                self.assertEqual(row["candidate_count"], len(row["runtime_pos"]))
                self.assertEqual(row["n_mixed"], row["n_present"] and not row["n_only"])
        changed = self.labels()
        changed["столами"] = ("N", "A")
        second = build_oblique_n_observation(FakeHolder(changed))
        self.assertEqual(report["fixture_manifest_sha256"], second["fixture_manifest_sha256"])
        self.assertNotEqual(report["runtime_observations_sha256"],
                            second["runtime_observations_sha256"])


if __name__ == "__main__":
    unittest.main()
