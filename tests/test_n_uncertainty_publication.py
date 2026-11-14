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
        history = (ROOT / "docs/reader-history.md").read_text(encoding="utf-8")
        # The concise Reader introduction supersedes the old fixed phrase;
        # the native-N evidence and its caveats remain available in history.
        self.assertIn("Russian-first literary analyzer", readme)
        self.assertIn("docs/reader-history.md", readme)
        self.assertIn("n-uncertainty.html", history)
        self.assertIn("M2 parity remains 0/5", readme)
        self.assertIn("not current acceptance or live-deployment evidence", history)


    def test_public_native_n_tables_match_pinned_conditional_units(self):
        """Visible static figures must track the reviewed N witness and its denominators."""
        from scriptorium.native_n_units import normalized_n_bounds

        doc = record()
        units = normalized_n_bounds(doc)
        html = (ROOT / "n-uncertainty.html").read_text(encoding="utf-8")

        def format_int(value):
            return f"{value:,}".replace(",", " ")

        def format_ru(value):
            return f"{value:.6f}".replace(".", ",")

        def assert_rows(markup):
            names = {"noun": "Существительное", "cardinal": "Числительное"}
            for category, bounds in doc["bucket_bounds"].items():
                row = (f'<tr data-native-bucket="{category}"><th scope="row">{names[category]}</th>'
                       f'<td>{format_int(bounds[0])}</td><td>{format_int(bounds[1])}</td>'
                       f'<td>{format_ru(units["bucket_percent_of_conditional_defined"][category][1])}%</td></tr>')
                self.assertIn(row, markup)
            for pair, scaled in zip(doc["bigram_bounds"], units["bigram_per_1000_word_tokens"]):
                first, second = pair["first"], pair["second"]
                row = (f'<tr data-native-pair="{first}-{second}"><th scope="row">'
                       f'{names[first]} → {names[second].lower()}</th>'
                       f'<td>{format_int(pair["min"])}</td><td>{format_int(pair["max"])}</td>'
                       f'<td>{format_int(pair["independent_edge_upper"])}</td>'
                       f'<td>{format_ru(scaled["max"])}</td>'
                       f'<td>{format_ru(scaled["independent_edge_upper"])}</td></tr>')
                self.assertIn(row, markup)
            for position, scaled in zip(doc["sentence_position_bounds"],
                                        units["sentence_position_percent_of_all_sentences"]):
                row = (f'<tr data-native-position="{position["position"]}">'
                       f'<th scope="row">{position["position"]}</th>'
                       f'<td>{format_int(position["min"])}</td><td>{format_int(position["max"])}</td>'
                       f'<td>{format_ru(scaled["max"])}%</td></tr>')
                self.assertIn(row, markup)
            control_labels = {
                "noun_examples": "Примеры существительных",
                "cardinal_examples": "Примеры числительных",
                "other_pos_controls": "Контроль других частей речи",
            }
            for name, group in doc["native_controls"].items():
                rate = units["native_control_n_only_percent_of_annotated_examples"][name]
                display = (f"{rate:.1f}".rstrip("0").rstrip(".").replace(".", ",") + "%"
                           if rate is not None else "NOT_RUN")
                row = (f'<tr data-native-control="{name}"><th scope="row">'
                       f'{control_labels[name]}</th>'
                       f'<td>{format_int(group["n_only"])}</td>'
                       f'<td>{format_int(group["token_count"])}</td>'
                       f'<td>{display}</td></tr>')
                self.assertIn(row, markup)
            for table_id in ("n-buckets-table", "n-bigram-table", "n-position-table",
                             "n-native-controls-table"):
                self.assertIn(f'id="{table_id}"', markup)
            self.assertIn("M2: 0/5", markup)
            self.assertIn("не правило округления FantLab", markup)

        assert_rows(html)
        changed = html.replace("31,192688", "31,192689", 1)
        self.assertNotEqual(changed, html)
        with self.assertRaises(AssertionError):
            assert_rows(changed)
        changed_control = html.replace("66,7%", "66,8%", 1)
        self.assertNotEqual(changed_control, html)
        with self.assertRaises(AssertionError):
            assert_rows(changed_control)

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

    def test_bucket_bounds_require_literal_json_integers(self):
        """False and float count endpoints must not pass Python numeric equality."""
        for label, invalid in (
            ("noun", [False, 55081]),
            ("noun", [0.0, 55081]),
            ("cardinal", [0, 55081.0]),
            ("cardinal", [False, 55081.0]),
        ):
            with self.subTest(label=label, invalid=invalid):
                doc = record()
                doc["bucket_bounds"][label] = invalid
                with self.assertRaisesRegex(ValueError, "JSON integers"):
                    validate_n_summary(doc)

    def test_unexpected_manuscript_field_rejected(self):
        doc = record()
        doc["normalized_text"] = "private text"
        with self.assertRaisesRegex(ValueError, "keys mismatch"):
            validate_n_summary(doc)


if __name__ == "__main__":
    unittest.main()
