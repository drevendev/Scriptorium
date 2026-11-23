"""Source-POS surface probe: exposed field names are not original AOT slots."""
import json
from types import SimpleNamespace
import unittest

from tools.pylem_n_attestation_probe import CONTROLS
from tools.pylem_n_source_pos_probe import SCHEMA, measure_source_pos_surface


class Holder:
    def __init__(self, rows):
        self.rows = rows

    def lemmatize(self, token):
        return self.rows.get(token, ())


def baseline():
    return {
        **{word: (SimpleNamespace(part_of_speech="N", predicted=False,
                                  lemma="PRIVATE", grammems=["PRIVATE"]),)
           for _, words in CONTROLS[:2] for word in words},
        **{word: (SimpleNamespace(part_of_speech="PREP"),)
           for word in CONTROLS[2][1]},
    }


class SourcePosSurfaceTests(unittest.TestCase):
    def test_runtime_fields_do_not_infer_original_aot_slot(self):
        doc = measure_source_pos_surface(Holder(baseline()))
        self.assertEqual(doc, measure_source_pos_surface(Holder(baseline())))
        self.assertEqual(doc["schema_version"], SCHEMA)
        self.assertEqual(doc["n_candidate_count"], 6)
        self.assertEqual(doc["clean_negative_control_count"], 3)
        self.assertEqual(doc["runtime_field_surface_decision"],
                         "no_explicit_field_in_examined_n_analyses")
        self.assertFalse(doc["original_aot_enum_verified"])
        self.assertEqual(doc["noun_cardinal_source_pos"], "unresolved")
        self.assertFalse(doc["m2_parity_admissible"])
        self.assertFalse(doc["source_text_included"])
        self.assertFalse(doc["production_pos_mapping_changed"])
        self.assertEqual(len(doc["observation_sha256"]), 64)
        serialized = json.dumps(doc, ensure_ascii=False)
        self.assertNotIn("PRIVATE", serialized)
        for _, words in CONTROLS:
            for word in words:
                self.assertNotIn('"' + word + '"', serialized)

    def test_candidate_field_triggers_feasibility_not_a_false_proof(self):
        rows = baseline()
        rows[CONTROLS[1][1][0]] = (SimpleNamespace(part_of_speech="N", source_pos_slot=6),)
        doc = measure_source_pos_surface(Holder(rows))
        self.assertEqual(doc["runtime_field_surface_decision"],
                         "possible_field_needs_semantic_validation")
        self.assertEqual(doc["explicit_source_field_presence_counts"]["source_pos_slot"], 1)
        self.assertFalse(doc["original_aot_enum_verified"])
        self.assertEqual(doc["noun_cardinal_source_pos"], "unresolved")
        self.assertNotIn('"source_pos_slot": 6', json.dumps(doc))

    def test_no_n_analyses_never_claims_absence(self):
        rows = {word: (SimpleNamespace(part_of_speech="PREP"),)
                for _, words in CONTROLS for word in words}
        doc = measure_source_pos_surface(Holder(rows))
        self.assertEqual(doc["n_candidate_count"], 0)
        self.assertEqual(doc["runtime_field_surface_decision"], "no_n_analyses_observed")
        self.assertEqual(doc["n_public_field_names_observed"], [])

    def test_invalid_native_tags_fail_closed(self):
        for bad in (None, "", " N", 123):
            with self.subTest(bad=bad):
                rows = baseline()
                rows[CONTROLS[0][1][0]] = (SimpleNamespace(part_of_speech=bad),)
                with self.assertRaises(ValueError):
                    measure_source_pos_surface(Holder(rows))

    def test_unknown_field_names_not_exported(self):
        rows = baseline()
        rows[CONTROLS[0][1][0]] = (SimpleNamespace(part_of_speech="N",
                                                    manuscript_please_leak="PRIVATE"),)
        doc = measure_source_pos_surface(Holder(rows))
        serialized = json.dumps(doc)
        self.assertNotIn("manuscript_please_leak", serialized)
        self.assertNotIn("PRIVATE", serialized)


if __name__ == "__main__":
    unittest.main()
