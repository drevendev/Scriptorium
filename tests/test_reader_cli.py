"""Integration of the installed entry point with real canonical reader modules."""
import contextlib
import copy
import csv
import io
import json
import os
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest
from unittest.mock import patch

from scriptorium import analyze, cli

ROOT = Path(__file__).resolve().parents[1]
DIAGNOSTIC = ROOT / "benchmarks/fantlab/work270306-wikisource-diagnostic.json"


class ReaderCliTests(unittest.TestCase):
    def test_help_lists_real_commands(self):
        text = io.StringIO()
        with contextlib.redirect_stdout(text):
            self.assertEqual(cli.main(["--help"]), 0)
        for command in ["analyze", "diagnostic", "site"]:
            self.assertIn(command, text.getvalue())

    def test_unknown_command_does_not_echo_private_input(self):
        text = io.StringIO()
        with contextlib.redirect_stderr(text):
            self.assertEqual(cli.main(["PRIVATE-PATH"]), 2)
        self.assertNotIn("PRIVATE-PATH", text.getvalue())

    def test_real_analyzer_dispatch_three_formats(self):
        with tempfile.TemporaryDirectory() as d:
            root = Path(d)
            source = root / "private.txt"
            source.write_text("Кот идёт. Пёс спит!", encoding="utf-8")
            for kind in ["json", "html", "csv"]:
                out = root / f"report.{kind}"
                self.assertEqual(cli.main(["analyze", str(source), "--format", kind, "--output", str(out)]), 0)
                text = out.read_text(encoding="utf-8")
                self.assertNotIn("Кот идёт", text)
                if kind == "csv":
                    self.assertEqual(len(list(csv.DictReader(io.StringIO(text)))), 29)

    def test_frozen_diagnostic_matches_canonical_renderer(self):
        from scriptorium.frozen_diagnostic_report import render_html
        with tempfile.TemporaryDirectory() as d:
            out = Path(d) / "report.html"
            self.assertEqual(cli.main(["diagnostic", str(DIAGNOSTIC), "--output", str(out)]), 0)
            self.assertEqual(out.read_text(encoding="utf-8"), render_html(json.loads(DIAGNOSTIC.read_text(encoding="utf-8"))))

    def test_diagnostic_errors_are_private_and_preserve_output(self):
        with tempfile.TemporaryDirectory() as d:
            out = Path(d) / "PRIVATE-REPORT.html"
            out.write_bytes(b"preserved")
            errors = io.StringIO()
            with contextlib.redirect_stderr(errors), self.assertRaises(SystemExit) as exc:
                cli.main(["diagnostic", str(DIAGNOSTIC), "--output", str(out)])
            self.assertEqual(exc.exception.code, 2)
            self.assertNotIn(d, errors.getvalue())
            self.assertNotIn(out.name, errors.getvalue())
            self.assertEqual(out.read_bytes(), b"preserved")

    def test_diagnostic_rejects_duplicate_keys_before_output(self):
        with tempfile.TemporaryDirectory() as d:
            source, out = Path(d) / "bad.json", Path(d) / "out.html"
            source.write_text('{"artifact_version":1,"artifact_version":2}', encoding="utf-8")
            with contextlib.redirect_stderr(io.StringIO()), self.assertRaises(SystemExit):
                cli.main(["diagnostic", str(source), "--output", str(out)])
            self.assertFalse(out.exists())

    @unittest.skipUnless(hasattr(os, "mkfifo"), "FIFO is POSIX-specific")
    def test_diagnostic_fifo_rejected_without_hanging(self):
        with tempfile.TemporaryDirectory() as d:
            source = Path(d) / "PRIVATE-FIFO"
            os.mkfifo(source)
            result = subprocess.run([sys.executable, "-m", "scriptorium", "diagnostic", str(source)],
                                    cwd=ROOT, capture_output=True, text=True, timeout=10)
            self.assertEqual(result.returncode, 2)
            self.assertNotIn(d, result.stderr)

    def test_csv_rejects_missing_metrics_and_unit_evidence(self):
        original = analyze.build_local_analysis(b"A short example.")
        bad = copy.deepcopy(original)
        bad["metrics"].pop("fantlab.general.words")
        with self.assertRaises(ValueError):
            analyze.render_csv(bad)
        for key in ["unit", "definition_evidence"]:
            bad = copy.deepcopy(original)
            bad["metrics"]["fantlab.general.words"][key] = ""
            with self.assertRaises(ValueError):
                analyze.render_csv(bad)

    def test_site_dispatch_preserves_arguments(self):
        from types import SimpleNamespace
        received = []
        module = SimpleNamespace(main=lambda args: received.append(args) or 0)
        with patch.object(cli.importlib, "import_module", return_value=module) as loader:
            self.assertEqual(cli.main(["site", "--repo-root", ".", "--output", "build/site"]), 0)
        loader.assert_called_once_with("scriptorium.site_renderer")
        self.assertEqual(received, [["--repo-root", ".", "--output", "build/site"]])


if __name__ == "__main__":
    unittest.main()
