"""Source-free, pinned-provider lexical N contrast controls (no native dependency here)."""
import json
import unittest
from types import SimpleNamespace

from tools.pylem_runtime_probe import N_CONTRAST_GROUPS, build_n_contrast


class _Holder:
    def __init__(self, tags):
        self.tags = tags

    def lemmatize(self, word):
        return tuple(SimpleNamespace(part_of_speech=value)
                     for value in self.tags.get(word, ()))


class NativeNContrastTests(unittest.TestCase):
    def test_cross_role_n_collision_is_observation_not_disambiguation(self):
        mapping = {
            "дом": ("N",), "книга": ("N", "N"), "город": ("N", "V"),
            "два": ("N",), "три": ("N", "A"), "пять": (),
            "красный": ("A",), "быстро": ("ADV",), "бежит": ("V",),
        }
        result = build_n_contrast(_Holder(mapping))
        self.assertEqual(result["schema_version"], "scriptorium-aot-n-contrast-v1")
        self.assertTrue(result["observed_n_only_across_noun_and_cardinal_examples"])
        groups = result["groups"]
        self.assertEqual([name for name, _ in N_CONTRAST_GROUPS], list(groups))
        self.assertEqual((groups["noun_examples"]["n_only_count"],
                          groups["noun_examples"]["n_present_count"]), (2, 3))
        self.assertEqual((groups["cardinal_examples"]["n_only_count"],
                          groups["cardinal_examples"]["n_present_count"]), (1, 2))
        self.assertEqual(groups["other_pos_controls"]["n_present_count"], 0)
        self.assertEqual(groups["cardinal_examples"]["tokens"][2]["candidate_count"], 0)
        self.assertFalse(groups["cardinal_examples"]["tokens"][2]["n_only"])
        self.assertFalse(result["m2_parity_admissible"])
        self.assertFalse(result["production_pos_mapping_changed"])
        self.assertEqual(result["fantlab_homonym_selection"], "unresolved")
        serialized = json.dumps(result, ensure_ascii=False)
        for original in ("дом", "книга", "город", "два", "три", "пять",
                         "красный", "быстро", "бежит"):
            self.assertNotIn(original, serialized)
        self.assertNotIn("normalized_text", serialized)

    def test_no_collision_observation_remains_false(self):
        mapping = {word: ("A",) for _, words in N_CONTRAST_GROUPS for word in words}
        result = build_n_contrast(_Holder(mapping))
        self.assertFalse(result["observed_n_only_across_noun_and_cardinal_examples"])
        self.assertTrue(all(group["n_only_count"] == 0
                            for group in result["groups"].values()))
        self.assertEqual(sum(group["token_count"]
                             for group in result["groups"].values()), 9)

    def test_missing_analysis_and_bad_native_values_fail_closed(self):
        empty = build_n_contrast(_Holder({}))
        self.assertEqual(empty["groups"]["noun_examples"]["n_present_count"], 0)
        self.assertFalse(empty["observed_n_only_across_noun_and_cardinal_examples"])
        for bad in ("", " ", None, 123):
            with self.subTest(bad=bad):
                with self.assertRaisesRegex(RuntimeError, "blank/non-string"):
                    build_n_contrast(_Holder({"дом": (bad,)}))

    def test_replay_is_deterministic_and_hashes_are_valid(self):
        import re
        tags = {word: ("N",) for _, words in N_CONTRAST_GROUPS for word in words}
        first = build_n_contrast(_Holder(tags))
        self.assertEqual(first, build_n_contrast(_Holder(tags)))
        self.assertRegex(first["token_manifest_sha256"], r"^[0-9a-f]{64}$")
        for group in first["groups"].values():
            self.assertEqual(group["token_count"], 3)
            self.assertEqual(group["n_present_count"], 3)
            for row in group["tokens"]:
                self.assertTrue(re.fullmatch("[0-9a-f]{64}", row["token_sha256"]))
                self.assertEqual(row["runtime_pos"], ["N"])


if __name__ == "__main__":
    unittest.main()
