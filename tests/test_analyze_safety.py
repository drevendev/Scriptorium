import contextlib
import copy
from hashlib import sha256
import io
import json
import os
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch

from scriptorium import analyze
from scriptorium.metrics import analyze_deterministic_metrics
from scriptorium.text import normalize_text


class LocalAnalysisSafetyTests(unittest.TestCase):
    def fail_cli(self, argv):
        with contextlib.redirect_stderr(io.StringIO()):
            with self.assertRaises(SystemExit) as error:
                analyze.main(argv)
        self.assertEqual(error.exception.code, 2)

    def test_actual_engine_values_profiles_and_dependencies_are_preserved(self):
        raw = "Е\u0308лка\r\n— Кот? — сказал он.\rКот-пёс!".encode()
        kwargs = dict(dictionary_words=["кот", "ёлка"], dictionary_profile="fixture-v1")
        direct = analyze_deterministic_metrics(raw.decode(), **kwargs)
        result = analyze.build_local_analysis(raw, **kwargs)
        self.assertEqual(result["metrics"], direct["metrics"])
        self.assertEqual(result["analyzer"]["profiles"], direct["profiles"])
        self.assertEqual(result["analyzer"]["dependencies"], direct["dependencies"])
        self.assertEqual(result["source"]["normalized_sha256"], sha256(normalize_text(raw.decode()).encode()).hexdigest())
        self.assertNotEqual(result["source"]["raw_sha256"], result["source"]["normalized_sha256"])

    def test_empty_input_preserves_undefined_mean_and_zero_count(self):
        result = analyze.build_local_analysis(b"")
        self.assertEqual(result["metrics"]["fantlab.general.words"]["value"], 0)
        self.assertIsNone(result["metrics"]["fantlab.general.mean_word_length_chars"]["value"])
        rendered = analyze.render_html(result)
        self.assertIn("Unavailable", rendered)
        self.assertIn("nonzero", rendered)

    def test_supplied_dictionary_does_not_make_incomplete_window_zero(self):
        result = analyze.build_local_analysis("Кот".encode(), dictionary_words=["кот"], dictionary_profile="fixture")
        self.assertEqual(result["metrics"]["fantlab.vocabulary.active_dictionary"]["value"], 1)
        self.assertIsNone(result["metrics"]["fantlab.vocabulary.uasz_3000"]["value"])
        self.assertIn("complete vocabulary window", analyze.render_html(result))

    def test_threshold_is_not_corpus_admission(self):
        for length, meets in ((299999, False), (300000, True)):
            with self.subTest(length=length):
                result = analyze.build_local_analysis(b" " * length)
                self.assertEqual(result["representativeness"]["meets_calibration_threshold"], meets)
        self.assertIn("separate gates", result["representativeness"]["note"])

    def test_html_shows_all_rows_profiles_and_no_remote_assets(self):
        result = analyze.build_local_analysis("Уникальная рукопись".encode())
        rendered = analyze.render_html(result)
        self.assertEqual(rendered.count('scope="row"'), 29)
        self.assertEqual(rendered.count("<caption>"), 4)
        for profile in result["analyzer"]["profiles"].values():
            self.assertIn(profile, rendered)
        self.assertNotIn("<script", rendered)
        self.assertNotIn("<link", rendered)
        self.assertNotIn("Уникальная", rendered)

    def test_other_metric_family_is_not_silently_lost(self):
        result = analyze.build_local_analysis(b"abc")
        result["metrics"]["scriptorium.extra.metric"] = {
            "value": 1, "unit": "events", "compatibility_status": "extension"
        }
        self.assertEqual(analyze.render_html(result).count('scope="row"'), 30)
        self.assertIn("<h2>Other</h2>", analyze.render_html(result))

    def test_render_rejects_nonfinite_or_promoted_result(self):
        original = analyze.build_local_analysis(b"abc")
        for value in (float("inf"), float("nan"), True):
            bad = copy.deepcopy(original)
            bad["metrics"]["fantlab.general.words"]["value"] = value
            with self.assertRaises(ValueError):
                analyze.render_html(bad)
        original["metrics"]["fantlab.general.words"]["compatibility_status"] = "reproduced"
        with self.assertRaises(ValueError):
            analyze.render_html(original)

    def test_cli_real_dictionary_and_private_payload(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            source, dictionary = root / "source.txt", root / "dict.txt"
            source.write_text("Кот пёс дракон", encoding="utf-8")
            dictionary.write_text("кот\nпёс\nSECRET_DICTIONARY_TOKEN\n", encoding="utf-8")
            for fmt in ("json", "html"):
                output = root / f"out.{fmt}"
                self.assertEqual(analyze.main([str(source), "--dictionary", str(dictionary), "--dictionary-profile", "test-v1", "--format", fmt, "--output", str(output)]), 0)
                rendered = output.read_text(encoding="utf-8")
                self.assertNotIn("SECRET_DICTIONARY_TOKEN", rendered)
                self.assertNotIn("дракон", rendered)
                if fmt == "json":
                    result = json.loads(rendered)
                    self.assertEqual(result["metrics"]["fantlab.vocabulary.active_dictionary"]["value"], 2)

    def test_invalid_dictionary_utf8_and_blank_profile_create_no_output(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            source, dictionary, output = root / "in.txt", root / "dict.txt", root / "out.json"
            source.write_bytes(b"abc")
            dictionary.write_bytes(b"\xff")
            self.fail_cli([str(source), "--dictionary", str(dictionary), "--dictionary-profile", "v1", "--output", str(output)])
            dictionary.write_bytes(b"abc")
            self.fail_cli([str(source), "--dictionary", str(dictionary), "--dictionary-profile", " ", "--output", str(output)])
            self.fail_cli([str(source), "--dictionary", str(dictionary), "--output", str(output)])
            self.assertFalse(output.exists())

    def test_output_aliases_cannot_destroy_manuscript_or_dictionary(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            source, dictionary = root / "in.txt", root / "dict.txt"
            source.write_bytes(b"private manuscript")
            dictionary.write_bytes(b"dictionary")
            for target in (source, dictionary):
                before = target.read_bytes()
                self.fail_cli([str(source), "--output", str(target)])
                self.assertEqual(target.read_bytes(), before)
            linked = root / "linked.txt"
            os.link(source, linked)
            self.fail_cli([str(source), "--output", str(linked)])
            self.assertEqual(source.read_bytes(), b"private manuscript")

    def test_dangling_symlink_is_preserved(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            source, target, missing = root / "in.txt", root / "out.json", root / "missing"
            source.write_bytes(b"abc")
            try:
                target.symlink_to(missing)
            except (OSError, NotImplementedError):
                self.skipTest("symlinks unavailable on this platform")
            self.fail_cli([str(source), "--output", str(target)])
            self.assertTrue(target.is_symlink())
            self.assertFalse(missing.exists())

    def test_failed_write_does_not_publish_partial_output(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            output = root / "report.json"
            with patch.object(analyze.os, "fsync", side_effect=OSError("disk failure")):
                with self.assertRaises(OSError):
                    analyze._write_new(output, "derived report")
            self.assertFalse(output.exists())
            self.assertEqual(list(root.iterdir()), [])

    def test_atomic_publish_collision_preserves_existing_report(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            output = root / "report.json"
            output.write_text("last valid report")
            with self.assertRaises(FileExistsError):
                analyze._write_new(output, "new report")
            self.assertEqual(output.read_text(), "last valid report")
            self.assertEqual(list(root.iterdir()), [output])

    def test_output_has_private_permissions_on_posix(self):
        if os.name != "posix":
            self.skipTest("POSIX permission bits")
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "report.json"
            analyze._write_new(path, "derived")
            self.assertEqual(path.stat().st_mode & 0o777, 0o600)


if __name__ == "__main__":
    unittest.main()
