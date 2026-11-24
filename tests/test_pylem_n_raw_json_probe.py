import json
from types import SimpleNamespace
import unittest

from tools.pylem_n_attestation_probe import CONTROLS
from tools.pylem_n_raw_json_probe import measure


class Holder:
    def __init__(self):
        self.rows = {w: [{"morphInfo": "N PRIVATE", "wordForm": "PRIVATE"}]
                     for _, words in CONTROLS[:2] for w in words}
        self.rows.update({w: [{"morphInfo": "PREP"}] for w in CONTROLS[2][1]})

    def lemmatize_json(self, word, all_forms):
        assert all_forms is False
        return self.rows.get(word, [])

    def lemmatize(self, word):
        return [SimpleNamespace(part_of_speech=r["morphInfo"].partition(" ")[0])
                for r in self.rows.get(word, [])]


class RawJsonProbeTests(unittest.TestCase):
    def test_baseline_and_privacy(self):
        doc = measure(Holder())
        self.assertEqual(doc, measure(Holder()))
        self.assertEqual(doc["n_candidate_count"], 6)
        self.assertEqual(doc["clean_negative_control_count"], 3)
        self.assertEqual(doc["decision"], "no_explicit_source_key_in_examined_raw_n_rows")
        self.assertNotIn("PRIVATE", json.dumps(doc))
        self.assertFalse(doc["original_aot_enum_verified"])
        self.assertFalse(doc["m2_parity_admissible"])

    def test_possible_source_key_is_not_proof(self):
        holder = Holder()
        holder.rows[CONTROLS[1][1][0]][0]["sourcePosSlot"] = 987654
        doc = measure(holder)
        self.assertEqual(doc["explicit_source_key_counts"]["sourcePosSlot"], 1)
        self.assertEqual(doc["decision"], "possible_source_key_needs_semantic_validation")
        self.assertNotIn("987654", json.dumps(doc))
        self.assertFalse(doc["original_aot_enum_verified"])

    def test_unknown_key_is_counted_not_exported(self):
        holder = Holder()
        holder.rows[CONTROLS[0][1][0]][0]["PRIVATE_KEY"] = "PRIVATE_VALUE"
        doc = measure(holder)
        self.assertEqual(doc["decision"], "unrecognized_keys_need_source_review")
        self.assertEqual(doc["unrecognized_n_key_count"], 1)
        self.assertNotIn("PRIVATE", json.dumps(doc))

    def test_empty_is_not_absence_evidence(self):
        holder = Holder()
        holder.rows.clear()
        self.assertEqual(measure(holder)["decision"], "no_n_observed")
        self.assertEqual(measure(holder)["clean_negative_control_count"], 0)

    def test_mismatch_and_malformed_fail_closed(self):
        holder = Holder()
        holder.lemmatize = lambda word: []
        with self.assertRaisesRegex(ValueError, "sequence differ"):
            measure(holder)
        holder = Holder()
        holder.rows[CONTROLS[0][1][0]] = [{"morphInfo": None}]
        with self.assertRaisesRegex(ValueError, "invalid native JSON analysis"):
            measure(holder)


if __name__ == "__main__":
    unittest.main()
