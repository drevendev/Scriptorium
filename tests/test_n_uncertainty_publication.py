"""Evidence consistency and scientific-boundary regressions for public native N page."""
import copy
import json
from pathlib import Path
import unittest

from scriptorium.n_uncertainty_publication import validate_n_summary

ROOT = Path(__file__).resolve().parents[1]


def record():
    return json.loads((ROOT / "assets/n-uncertainty-anna.json").read_text(encoding="utf-8"))


class NativeNPublicationTests(unittest.TestCase):
    def test_pinned_real_work_summary_and_readable_static_page(self):
        doc = record()
        result = validate_n_summary(doc)
        self.assertAlmostEqual(result["n_only_percent_of_words"], 20.448993532770512)
        self.assertEqual(doc["counts"]["n_only"], 55081)
        self.assertEqual(doc["bigram_bounds"][1]["max"], 8402)
        self.assertEqual(doc["native_controls"]["cardinal_examples"]["n_only"], 2)
        html = (ROOT / "n-uncertainty.html").read_text(encoding="utf-8")
        index = (ROOT / "index.html").read_text(encoding="utf-8")
        self.assertIn("55 081", html)
        self.assertIn("8 402", html)
        self.assertIn("n-uncertainty-anna.json", html)
        self.assertIn("n-uncertainty.html", index)
        self.assertIn("<table", html)
        self.assertIn("<caption", html)
        self.assertIn("prefers-reduced-motion", html)
        self.assertIn("M2: 0/5", html)
        self.assertNotIn("normalized_text", json.dumps(doc))
        self.assertNotIn("Анна была", json.dumps(doc))

    def test_frozen_native_record_matches_independent_expected_values(self):
        """Detect self-consistent but false edits to the frozen published numbers."""
        doc = record()
        self.assertEqual(
            doc["evidence"]["artifact_json_sha256"],
            "6da40b4723cafc0288fea530a35f8d910b76e7ccffd60f754e6aa899412e5554",
        )
        self.assertEqual(
            doc["evidence"]["normalized_sha256"],
            "1dcf2af815f6288099f77a038d873690fb0dc72edf81d2094fd29f3d5a30c205",
        )
        self.assertEqual(
            doc["evidence"]["runtime_analysis_sha256"],
            "00cb365eeb6e187362cb1cb54acc6718c230791df18013702907dfee6446d69d",
        )
        self.assertEqual(doc["counts"], {
            "word_count": 269358, "sentence_count": 21228,
            "baseline_defined": 117554, "n_only": 55081,
            "n_mixed_excluded": 19670, "conditional_defined": 172635,
        })
        self.assertEqual([row["max"] for row in doc["bigram_bounds"]],
                         [9992, 8402, 8402, 9992])
        self.assertEqual([row["max"] for row in doc["sentence_position_bounds"]],
                         [2787, 3203, 3151, 3451, 3440])

    def test_reader_accessibility_and_readme_separation(self):
        html = (ROOT / "n-uncertainty.html").read_text(encoding="utf-8")
        readme = (ROOT / "README.md").read_text(encoding="utf-8")
        self.assertIn(".n-table:focus-visible", html)
        self.assertIn('class="n-table" role="region" tabindex="0"', html)
        self.assertNotIn(r"\n\n**Russian-first", readme)
        self.assertIn("\n\n**Russian-first", readme)

    def test_tampering_counts_identity_or_parity_fails_closed(self):
        for path, value in [
            (("counts", "conditional_defined"), 172636),
            (("counts", "n_only"), True),
            (("counts", "n_mixed_excluded"), 300000),
            (("bucket_bounds", "cardinal"), [0, 1]),
            (("bigram_bounds", 1, "max"), 9999),
            (("sentence_position_bounds", 0, "max"), 30000),
            (("native_controls", "cardinal_examples", "n_only"), 4),
            (("evidence", "normalized_sha256"), "unknown"),
            (("boundary", "fantlab_homonym_selection"), "reproduced"),
            (("m2_parity_admissible",), True),
            (("source_text_included",), True),
        ]:
            with self.subTest(path=path):
                doc = copy.deepcopy(record())
                current = doc
                for item in path[:-1]:
                    current = current[item]
                current[path[-1]] = value
                with self.assertRaises(ValueError):
                    validate_n_summary(doc)

    def test_unexpected_manuscript_field_rejected(self):
        doc = record()
        doc["normalized_text"] = "private text"
        with self.assertRaisesRegex(ValueError, "keys mismatch"):
            validate_n_summary(doc)


if __name__ == "__main__":
    unittest.main()
