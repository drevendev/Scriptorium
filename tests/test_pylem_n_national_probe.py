from types import SimpleNamespace
import unittest

from tools.pylem_n_attestation_probe import CONTROLS
from tools.pylem_n_national_probe import OLD, NEW, patch_binding, capture, compare


class NationalProbeTests(unittest.TestCase):
    mapping = {"С": "N", "ЧИСЛ": "N", "ПРЕДЛ": "PREP"}

    def rows(self, national=False):
        tags = ("С", "ЧИСЛ", "ПРЕДЛ") if national else ("N", "N", "PREP")
        lookup = {word: tag for (_, words), tag in zip(CONTROLS, tags) for word in words}
        holder = SimpleNamespace(lemmatize=lambda word: [SimpleNamespace(part_of_speech=lookup[word])])
        return capture(holder, set(tags))

    def test_patch_is_single_exact_change(self):
        self.assertEqual(patch_binding(b"before" + OLD + b"after"), b"before" + NEW + b"after")
        for bad in (b"", OLD + OLD, OLD + NEW):
            with self.assertRaises(ValueError):
                patch_binding(bad)

    def test_recovery_is_diagnostic_only(self):
        doc = compare(self.rows(), self.rows(True), self.mapping)
        self.assertTrue(doc["distinct_labels_observed"])
        self.assertEqual(doc["clean_negative_controls"], 3)
        self.assertFalse(doc["source_enum_verified"])
        self.assertFalse(doc["m2_parity_admissible"])

    def test_multiplicity_and_identity_fail_closed(self):
        before, after = self.rows(), self.rows(True)
        after[0]["tags"].append("С")
        with self.assertRaisesRegex(ValueError, "multiplicity"):
            compare(before, after, self.mapping)
        after = self.rows(True)
        after[0]["token_sha256"] = "wrong"
        with self.assertRaisesRegex(ValueError, "identity"):
            compare(before, after, self.mapping)

    def test_same_label_cannot_claim_recovery(self):
        before, after = self.rows(), self.rows(True)
        for row in after[3:6]:
            row["tags"] = ["С"]
        self.assertFalse(compare(before, after, self.mapping)["distinct_labels_observed"])

    def test_unknown_label_rejected(self):
        holder = SimpleNamespace(lemmatize=lambda word: [SimpleNamespace(part_of_speech="private")])
        with self.assertRaisesRegex(ValueError, "unexpected native"):
            capture(holder, self.mapping)


if __name__ == "__main__":
    unittest.main()
