"""Synthetic controls: identical input for every variant; no book prose."""
import json
from pathlib import Path
import tempfile
import unittest

from scriptorium.boundary_probe import analyze_boundary_probe, main, render_boundary_probe


class BoundaryProbeTests(unittest.TestCase):
    def test_independent_one_factor_counts(self):
        sample = "по-русски rock'n'roll l’amour А.Б. слово‐слово 12 и—ты"
        artifact = analyze_boundary_probe(sample)
        rows = {row["id"]: row for row in artifact["variants"]}
        self.assertEqual(rows["current_scriptorium_text_v1"]["word_count"], 10)
        self.assertEqual(rows["split_ascii_hyphen"]["word_count"], 11)
        self.assertEqual(rows["split_straight_apostrophe"]["word_count"], 12)
        self.assertEqual(rows["split_curly_apostrophe"]["word_count"], 11)
        self.assertEqual(rows["join_unicode_hyphens"]["word_count"], 9)
        self.assertEqual(rows["merge_dotted_initialisms"]["word_count"], 9)
        self.assertEqual(rows["exclude_numeric_only"]["word_count"], 9)
        self.assertEqual(artifact["observed_boundaries"]["standalone_dotted_initialisms"], 1)
        self.assertAlmostEqual(rows["split_ascii_hyphen"]["delta_per_1000_current_words"], 100.0)
        self.assertFalse(artifact["source_text_embedded"])
        self.assertFalse(artifact["m2_parity_admissible"])
        self.assertEqual(artifact["source_identity_to_fantlab"], "UNKNOWN")
        self.assertNotIn("l’amour", render_boundary_probe(artifact, "json"))

    def test_empty_invalid_and_same_input_replay(self):
        empty = analyze_boundary_probe("")
        self.assertEqual(empty["variants"][0]["word_count"], 0)
        self.assertIsNone(empty["variants"][0]["delta_per_1000_current_words"])
        self.assertIn("NOT_RUN", render_boundary_probe(empty, "markdown"))
        with self.assertRaises(TypeError):
            analyze_boundary_probe(b"invalid")
        with self.assertRaises(ValueError):
            render_boundary_probe({}, "json")
        self.assertEqual(analyze_boundary_probe("текст"), analyze_boundary_probe("текст"))
        self.assertEqual(
            json.loads(render_boundary_probe(analyze_boundary_probe("текст"), "json"))["status"],
            "DIAGNOSTIC_ONLY",
        )

    def test_cli_is_private_create_only_and_fail_closed(self):
        with tempfile.TemporaryDirectory() as directory:
            source = Path(directory) / "private.txt"
            output = Path(directory) / "probe.json"
            source.write_text("СЕКРЕТНОЕ_СЛОВО по-русски", encoding="utf-8")
            self.assertEqual(main([str(source), "--format", "json", "--output", str(output)]), 0)
            self.assertNotIn("СЕКРЕТНОЕ", output.read_text(encoding="utf-8"))
            with self.assertRaises(SystemExit):
                main([str(source), "--format", "json", "--output", str(output)])
            symlink = Path(directory) / "link.txt"
            symlink.symlink_to(source)
            with self.assertRaises(SystemExit):
                main([str(symlink)])
            source.write_bytes(b"\xff\xfe")
            with self.assertRaises(SystemExit):
                main([str(source)])


if __name__ == "__main__":
    unittest.main()
