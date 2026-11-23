"""Native N attestation probe: positive, mixed, predicted, missing and negative controls."""
import json
from types import SimpleNamespace
import unittest

from tools.pylem_n_attestation_probe import CONTROLS, SCHEMA, measure_attestation


class Holder:
    def __init__(self, rows):
        self.rows = rows

    def lemmatize(self, token):
        return [SimpleNamespace(part_of_speech=tag, predicted=prediction)
                for tag, prediction in self.rows.get(token, ())]


def sample():
    return {
        **{word: (("N", False),) for word in CONTROLS[0][1]},
        **{word: (("N", False),) for word in CONTROLS[1][1]},
        **{word: (("PREP", False),) for word in CONTROLS[2][1]},
    }


class AttestationTests(unittest.TestCase):
    def test_qualified_source_free_attested_cross_role(self):
        doc = measure_attestation(Holder(sample()))
        self.assertEqual(doc, measure_attestation(Holder(sample())))
        self.assertEqual(doc["schema_version"], SCHEMA)
        self.assertTrue(doc["qualified_cross_role_attestation_observed"])
        self.assertEqual(doc["usable_negative_controls"], 3)
        self.assertEqual([doc["groups"][role]["n_only_attested_count"]
                          for role, _ in CONTROLS], [3, 3, 0])
        self.assertFalse(doc["source_text_included"])
        self.assertFalse(doc["m2_parity_admissible"])
        self.assertFalse(doc["production_pos_mapping_changed"])
        self.assertEqual(doc["noun_cardinal_source_pos"], "unresolved")
        serialized = json.dumps(doc, ensure_ascii=False)
        for _, tokens in CONTROLS:
            for token in tokens:
                self.assertNotIn('"' + token + '"', serialized)
        for field in ("fixture_manifest_sha256", "runtime_observations_sha256"):
            self.assertEqual(len(doc[field]), 64)

    def test_predicted_only_mixed_and_unattested_do_not_qualify(self):
        rows = sample()
        rows["двух"] = (("N", True),)
        rows["трёх"] = (("N", True), ("ADV", False))
        rows["пяти"] = ()
        doc = measure_attestation(Holder(rows))
        group = doc["groups"]["cardinal_genitive_annotations"]
        self.assertEqual(group["n_predicted_only_count"], 2)
        self.assertEqual(group["n_attested_count"], 0)
        self.assertEqual(group["n_mixed_count"], 1)
        self.assertEqual(group["n_only_attested_count"], 0)
        self.assertFalse(doc["cross_role_attested_n_only_observed"])
        self.assertFalse(doc["qualified_cross_role_attestation_observed"])
        rows = sample()
        rows["без"] = (("N", False),)
        rows["под"] = ()
        self.assertEqual(measure_attestation(Holder(rows))["usable_negative_controls"], 1)
        self.assertFalse(measure_attestation(Holder(rows))["qualified_cross_role_attestation_observed"])

    def test_attested_mixed_does_not_count_as_only(self):
        rows = sample()
        rows["домов"] = (("N", False), ("A", False))
        doc = measure_attestation(Holder(rows))
        group = doc["groups"]["noun_genitive_annotations"]
        self.assertEqual(group["n_attested_count"], 3)
        self.assertEqual(group["n_only_attested_count"], 2)
        self.assertEqual(group["n_mixed_count"], 1)
        change = measure_attestation(Holder(sample()))
        self.assertEqual(doc["fixture_manifest_sha256"], change["fixture_manifest_sha256"])
        self.assertNotEqual(doc["runtime_observations_sha256"], change["runtime_observations_sha256"])

    def test_invalid_native_labels_and_prediction_flags_fail_closed(self):
        for tag, predicted in (("", False), (" N", False), (None, False),
                               ("N", None), ("N", 0), ("N", "false")):
            with self.subTest(tag=tag, predicted=predicted):
                rows = sample()
                rows["домов"] = ((tag, predicted),)
                with self.assertRaises(ValueError):
                    measure_attestation(Holder(rows))

    def test_empty_native_result_is_not_a_negative_control(self):
        doc = measure_attestation(Holder({}))
        self.assertEqual(doc["usable_negative_controls"], 0)
        self.assertFalse(doc["qualified_cross_role_attestation_observed"])


if __name__ == "__main__":
    unittest.main()
