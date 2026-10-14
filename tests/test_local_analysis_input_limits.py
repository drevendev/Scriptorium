"""Bound local manuscript/dictionary reads before parsing large untrusted inputs."""
import contextlib
import io
import json
import os
from pathlib import Path
import stat
import tempfile
import unittest
from unittest.mock import patch

from scriptorium import analyze


class InputBoundsTests(unittest.TestCase):
    def _reject_cli(self, args, *, forbidden=None):
        error = io.StringIO()
        with contextlib.redirect_stderr(error), self.assertRaises(SystemExit) as caught:
            analyze.main(args)
        self.assertEqual(caught.exception.code, 2)
        if forbidden:
            self.assertNotIn(forbidden, error.getvalue())
        return error.getvalue()

    def test_small_manuscript_keeps_actual_json_and_is_deterministic(self):
        with tempfile.TemporaryDirectory() as folder:
            root = Path(folder)
            source = root / "PRIVATE manuscript.txt"
            source.write_text("Кот сидел.\n— Да!", encoding="utf-8")
            a, b = root / "a.json", root / "b.json"
            self.assertEqual(analyze.main([str(source), "--output", str(a)]), 0)
            self.assertEqual(analyze.main([str(source), "--output", str(b)]), 0)
            self.assertEqual(a.read_bytes(), b.read_bytes())
            artifact = json.loads(a.read_text(encoding="utf-8"))
            self.assertEqual(len(artifact["metrics"]), 29)
            self.assertEqual(artifact["source"]["byte_count"], len(source.read_bytes()))
            self.assertNotIn(source.name, a.read_text(encoding="utf-8"))

    def test_precise_byte_limit_is_inclusive(self):
        with tempfile.TemporaryDirectory() as folder:
            source = Path(folder) / "sample"
            source.write_bytes(b"abcd")
            self.assertEqual(analyze._read_bounded_regular_file(source, 4, "manuscript"), b"abcd")
            with self.assertRaisesRegex(ValueError, "exceeds"):
                analyze._read_bounded_regular_file(source, 3, "manuscript")

    def test_sparse_oversized_manuscript_is_rejected_before_read(self):
        with tempfile.TemporaryDirectory() as folder:
            source, output = Path(folder) / "PRIVATE-oversize.txt", Path(folder) / "report.json"
            with source.open("wb") as handle:
                handle.truncate(analyze.MAX_ANALYSIS_BYTES + 1)
            error = self._reject_cli([str(source), "--output", str(output)], forbidden=source.name)
            self.assertIn("byte input limit", error)
            self.assertFalse(output.exists())

    def test_oversized_dictionary_is_rejected_without_output(self):
        with tempfile.TemporaryDirectory() as folder:
            root = Path(folder)
            source, dictionary, output = root / "valid.txt", root / "PRIVATE-lexemes.txt", root / "report.html"
            source.write_text("Книга.", encoding="utf-8")
            with dictionary.open("wb") as handle:
                handle.truncate(analyze.MAX_DICTIONARY_BYTES + 1)
            error = self._reject_cli([str(source), "--dictionary", str(dictionary),
                                      "--dictionary-profile", "fixture", "--format", "html",
                                      "--output", str(output)], forbidden=dictionary.name)
            self.assertIn("byte input limit", error)
            self.assertFalse(output.exists())

    def test_read_guard_detects_file_growth_after_stat(self):
        with tempfile.TemporaryDirectory() as folder:
            source = Path(folder) / "growing.txt"
            source.write_bytes(b"growing")
            real_fstat = os.fstat
            def old_stat(fd):
                current = real_fstat(fd)
                return os.stat_result((current.st_mode, current.st_ino, current.st_dev,
                                       current.st_nlink, current.st_uid, current.st_gid,
                                       3, current.st_atime, current.st_mtime, current.st_ctime))
            with patch.object(analyze.os, "fstat", side_effect=old_stat):
                with self.assertRaisesRegex(ValueError, "exceeds"):
                    analyze._read_bounded_regular_file(source, 4, "manuscript")

    def test_symlink_source_is_rejected_without_following(self):
        with tempfile.TemporaryDirectory() as folder:
            root = Path(folder)
            source, link, output = root / "secret-source.txt", root / "PRIVATE-link.txt", root / "out.csv"
            source.write_text("My secret content", encoding="utf-8")
            try:
                link.symlink_to(source)
            except (OSError, NotImplementedError):
                self.skipTest("symlink unavailable")
            error = self._reject_cli([str(link), "--format", "csv", "--output", str(output)], forbidden=link.name)
            self.assertIn("non-symlink", error)
            self.assertFalse(output.exists())
            self.assertEqual(source.read_text(encoding="utf-8"), "My secret content")

    def test_nonregular_fifo_rejected_without_blocking(self):
        if not hasattr(os, "mkfifo") or not hasattr(os, "O_NONBLOCK"):
            self.skipTest("requires POSIX FIFO and nonblocking open")
        with tempfile.TemporaryDirectory() as folder:
            source = Path(folder) / "input.fifo"
            os.mkfifo(source)
            with self.assertRaisesRegex(ValueError, "regular file"):
                analyze._read_bounded_regular_file(source, 4, "manuscript")

    def test_invalid_dictionary_utf8_rejected_create_only(self):
        with tempfile.TemporaryDirectory() as folder:
            root = Path(folder)
            source, dictionary, output = root / "text", root / "private-lexemes", root / "out.json"
            source.write_bytes(b"hello")
            dictionary.write_bytes(b"\xff")
            error = self._reject_cli([str(source), "--dictionary", str(dictionary),
                                      "--dictionary-profile", "demo", "--output", str(output)],
                                     forbidden=dictionary.name)
            self.assertIn("dictionary must be UTF-8", error)
            self.assertFalse(output.exists())


if __name__ == "__main__":
    unittest.main()
