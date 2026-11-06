"""Exercise opt-in private piped manuscript analysis without source leakage."""
import contextlib
from hashlib import sha256
import io
import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest
from unittest.mock import patch

from scriptorium import analyze


class PrivateStdinTests(unittest.TestCase):
    def test_pipe_equals_file_with_stable_source_hash_and_29_metrics(self):
        source = "Кот идёт. Пёс спит!\n".encode("utf-8")
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            original, by_file, by_pipe = (root / "private.txt", root / "file.json", root / "pipe.json")
            original.write_bytes(source)
            self.assertEqual(analyze.main([str(original), "--output", str(by_file)]), 0)
            run = subprocess.run(
                [sys.executable, "-m", "scriptorium", "analyze", "-", "--output", str(by_pipe)],
                input=source, capture_output=True, timeout=20)
            self.assertEqual(run.returncode, 0, run.stderr.decode("utf-8"))
            self.assertEqual(run.stdout, b"")
            self.assertEqual(by_file.read_bytes(), by_pipe.read_bytes())
            report = json.loads(by_pipe.read_text(encoding="utf-8"))
            self.assertEqual(report["source"]["raw_sha256"], sha256(source).hexdigest())
            self.assertFalse(report["source"]["source_text_embedded"])
            self.assertEqual(len(report["metrics"]), 29)
            self.assertNotIn("Кот идёт", by_pipe.read_text(encoding="utf-8"))

    def test_pipe_preserves_html_markdown_csv_outputs(self):
        source = "Только локальный текст.\n".encode("utf-8")
        for fmt in ("html", "markdown", "csv"):
            with self.subTest(fmt=fmt):
                run = subprocess.run(
                    [sys.executable, "-m", "scriptorium", "analyze", "-", "--format", fmt],
                    input=source, capture_output=True, timeout=20)
                self.assertEqual(run.returncode, 0, run.stderr.decode("utf-8"))
                self.assertTrue(run.stdout)
                self.assertNotIn(source, run.stdout)

    def test_invalid_utf8_and_existing_output_never_echo_or_overwrite(self):
        with tempfile.TemporaryDirectory() as temp:
            target = Path(temp) / "private.json"
            bad = subprocess.run(
                [sys.executable, "-m", "scriptorium", "analyze", "-", "--output", str(target)],
                input=b"PRIVATE\xff", capture_output=True, timeout=20)
            self.assertEqual(bad.returncode, 2)
            self.assertIn(b"UTF-8", bad.stderr)
            self.assertNotIn(b"PRIVATE", bad.stderr)
            self.assertFalse(target.exists())
            target.write_bytes(b"preserved")
            occupied = subprocess.run(
                [sys.executable, "-m", "scriptorium", "analyze", "-", "--output", str(target)],
                input="Рукопись.".encode("utf-8"), capture_output=True, timeout=20)
            self.assertEqual(occupied.returncode, 2)
            self.assertEqual(target.read_bytes(), b"preserved")
            self.assertNotIn(temp.encode(), occupied.stderr)

    def test_limit_is_enforced_without_output_or_private_error_text(self):
        with tempfile.TemporaryDirectory() as temp:
            output = Path(temp) / "secret-output.json"
            input_stream = io.TextIOWrapper(io.BytesIO(b"PRIVATE" * 10), encoding="utf-8")
            errors = io.StringIO()
            with patch.object(analyze.sys, "stdin", input_stream), patch.object(
                analyze, "MAX_ANALYSIS_BYTES", 10
            ), contextlib.redirect_stderr(errors), self.assertRaises(SystemExit) as caught:
                analyze.main(["-", "--output", str(output)])
            self.assertEqual(caught.exception.code, 2)
            self.assertIn("input limit", errors.getvalue())
            self.assertNotIn("PRIVATE", errors.getvalue())
            self.assertNotIn(temp, errors.getvalue())
            self.assertFalse(output.exists())

    def test_tty_is_refused_without_reading(self):
        class Tty:
            def isatty(self):
                return True
            @property
            def buffer(self):
                class NoRead:
                    def read(self, size):
                        raise AssertionError("TTY should not be read")
                return NoRead()
        errors = io.StringIO()
        with patch.object(analyze.sys, "stdin", Tty()), contextlib.redirect_stderr(
            errors
        ), self.assertRaises(SystemExit) as caught:
            analyze.main(["-"])
        self.assertEqual(caught.exception.code, 2)
        self.assertIn("piped or redirected", errors.getvalue())


if __name__ == "__main__":
    unittest.main()
