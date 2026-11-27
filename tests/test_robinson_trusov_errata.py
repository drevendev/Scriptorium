"""Synthetic tests: no historical prose fixtures."""
import unittest

from scriptorium.robinson_trusov_errata import classify, digest, CONTROLS, PINS


def witness(s):
    return len(s.split()), digest(" ".join(s.split()))


class ErrataTests(unittest.TestCase):
    def setUp(self):
        self.printed = witness("old phrase")
        self.corrected = witness("new.")

    def status(self, text):
        return classify(text, self.printed, self.corrected)["classification"]

    def test_corrected_unique(self):
        self.assertEqual(self.status("start new. end"), "CORRECTED_READING_PRESENT")

    def test_printed_unique_with_whitespace(self):
        self.assertEqual(self.status("start old\n\tphrase end"), "PRINTED_READING_PRESENT")

    def test_punctuation_case_and_token_edges_matter(self):
        for text in ("new", "New.", "renew.", "new.,", "old phrases"):
            with self.subTest(text=text):
                self.assertEqual(self.status(text), "NEITHER")

    def test_ambiguous_and_duplicate(self):
        for text in ("old phrase new.", "new. new.", "old phrase old phrase"):
            with self.subTest(text=text):
                self.assertEqual(self.status(text), "AMBIGUOUS")

    def test_no_text_in_result(self):
        row = classify("old phrase new.", self.printed, self.corrected)
        self.assertEqual(row, {"printed_matches": 1, "corrected_matches": 1,
                               "classification": "AMBIGUOUS"})

    def test_reject_identical_or_bad_width(self):
        with self.assertRaises(ValueError):
            classify("new.", self.corrected, self.corrected)
        with self.assertRaises(ValueError):
            classify("new.", (0, digest("")), self.corrected)

    def test_fixed_control_pins(self):
        self.assertEqual(PINS, {21: 4958671, 60: 4958715})
        self.assertEqual([row[1] for row in CONTROLS], [21, 60, 60])
        for _, _, printed, corrected in CONTROLS:
            self.assertNotEqual(printed, corrected)
            self.assertRegex(printed[1], r"^[0-9a-f]{64}$")
            self.assertRegex(corrected[1], r"^[0-9a-f]{64}$")


if __name__ == "__main__":
    unittest.main()
