"""Installed author-rhythm preview: evidence-bound CLI and non-destructive exports."""
from __future__ import annotations

from contextlib import redirect_stderr, redirect_stdout
from io import StringIO
import json
import os
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch

from scriptorium import cli, voice_profile

ROOT = Path(__file__).resolve().parents[1]
SNAPSHOT = ROOT / "assets/evidence-snapshot.json"
DERIVED = ROOT / "assets/voice-preview.json"


class InstalledVoiceCliTests(unittest.TestCase):
    def test_help_exposes_actual_preview_not_accepted_profile(self):
        output = StringIO()
        with redirect_stdout(output):
            self.assertEqual(cli.main(["--help"]), 0)
        self.assertIn("voice", output.getvalue())
        self.assertIn("M3 preview", output.getvalue())

    def test_default_source_is_bundled_byte_for_byte(self):
        packaged = ROOT / "scriptorium" / "data" / "evidence-snapshot.json"
        self.assertEqual(packaged.read_bytes(), SNAPSHOT.read_bytes())
        self.assertEqual(voice_profile._git_blob_sha(packaged.read_bytes()),
                         voice_profile._PACKAGED_SOURCE_BLOB_SHA1)
        package_config = (ROOT / "pyproject.toml").read_text(encoding="utf-8")
        self.assertIn('"data/evidence-snapshot.json"', package_config)

    def test_default_voice_report_works_outside_checkout(self):
        with tempfile.TemporaryDirectory() as directory:
            cwd = Path.cwd()
            try:
                os.chdir(directory)
                output = StringIO()
                with redirect_stdout(output):
                    self.assertEqual(cli.main(["voice"]), 0)
            finally:
                os.chdir(cwd)
        self.assertEqual(json.loads(output.getvalue()),
                         json.loads(DERIVED.read_text(encoding="utf-8")))

    def test_modified_bundled_identity_fails_closed_without_path_leak(self):
        stderr, stdout = StringIO(), StringIO()
        with patch.object(voice_profile, "_PACKAGED_SOURCE_BLOB_SHA1", "0" * 40):
            with redirect_stdout(stdout), redirect_stderr(stderr):
                with self.assertRaises(SystemExit) as rejected:
                    cli.main(["voice"])
        self.assertEqual(rejected.exception.code, 2)
        self.assertEqual(stdout.getvalue(), "")
        self.assertNotIn(str(ROOT), stderr.getvalue())
        self.assertIn("unable to verify", stderr.getvalue())

    def test_json_stdout_is_exact_reproduced_artifact_without_status_prefix(self):
        output = StringIO()
        with redirect_stdout(output):
            self.assertEqual(cli.main(["voice", "--snapshot", str(SNAPSHOT)]), 0)
        self.assertEqual(json.loads(output.getvalue()),
                         json.loads(DERIVED.read_text(encoding="utf-8")))
        self.assertEqual(output.getvalue(),
                         voice_profile.render_json(json.loads(DERIVED.read_text(encoding="utf-8"))))

    def test_markdown_shows_real_book_values_weighting_and_limits(self):
        output = StringIO()
        with redirect_stdout(output):
            self.assertEqual(cli.main(["voice", "--format", "markdown",
                                       "--snapshot", str(SNAPSHOT)]), 0)
        report = output.getvalue()
        self.assertIn("Александр Грин", report)
        self.assertIn("Лев Толстой", report)
        self.assertIn("M2: 0/5; M3: открыт", report)
        self.assertIn("между двумя книгами", report)
        self.assertIn("Среднее по словам", report)
        self.assertIn("разброс", report.lower())
        self.assertEqual(report.count("| Метрика |"), 2)
        self.assertEqual(report.count("| fantlab."), 0)
        self.assertEqual(report.count("| --- |"), 2)
        artifact = json.loads(DERIVED.read_text(encoding="utf-8"))
        for author in artifact["authors"]:
            for metric in author["metrics"]:
                self.assertIn(f'{metric["weighted_mean"]:.6f}', report)
                self.assertIn(f'{metric["weighted_population_stddev"]:.6f}', report)
                for observation in metric["per_work"]:
                    self.assertIn(f'{observation["value"]:.6f}', report)
        self.assertEqual(report, voice_profile.render_markdown(artifact))
        self.assertNotIn("Авторский отпечаток подтверждён", report)

    def test_check_preserves_stable_existing_ci_entrypoint(self):
        output = StringIO()
        with redirect_stdout(output):
            self.assertEqual(cli.main(["voice", "--check", str(DERIVED)]), 0)
        self.assertIn("VOICE_PREVIEW=VERIFIED", output.getvalue())

    def test_output_is_non_overwriting_and_does_not_leak_paths(self):
        with tempfile.TemporaryDirectory() as directory:
            target = Path(directory) / "PRIVATE-author-report.md"
            target.write_text("KEEP", encoding="utf-8")
            stderr = StringIO()
            with redirect_stderr(stderr), self.assertRaises(SystemExit) as rejected:
                cli.main(["voice", "--format", "markdown", "--output", str(target)])
            self.assertEqual(rejected.exception.code, 2)
            self.assertEqual(target.read_text(encoding="utf-8"), "KEEP")
            self.assertIn("already exists", stderr.getvalue())
            self.assertNotIn(directory, stderr.getvalue())
            self.assertNotIn(target.name, stderr.getvalue())
            target.unlink()
            with redirect_stdout(StringIO()):
                self.assertEqual(cli.main(["voice", "--format", "markdown",
                                           "--output", str(target)]), 0)
            self.assertIn("M2: 0/5", target.read_text(encoding="utf-8"))

    def test_rejects_untrusted_or_malformed_evidence_without_output(self):
        with tempfile.TemporaryDirectory() as directory:
            source = Path(directory) / "PRIVATE-source.json"
            target = Path(directory) / "report.json"
            for invalid in ('{"schema":"A","schema":"B"}', '{"schema":"wrong"}', "not json"):
                with self.subTest(invalid=invalid):
                    source.write_text(invalid, encoding="utf-8")
                    stderr = StringIO()
                    with redirect_stderr(stderr), self.assertRaises(SystemExit) as rejected:
                        cli.main(["voice", "--snapshot", str(source), "--output", str(target)])
                    self.assertEqual(rejected.exception.code, 2)
                    self.assertFalse(target.exists())
                    self.assertNotIn(directory, stderr.getvalue())
            stderr = StringIO()
            with redirect_stderr(stderr), self.assertRaises(SystemExit):
                cli.main(["voice", "--check", str(DERIVED), "--format", "markdown"])
            self.assertIn("requires JSON", stderr.getvalue())

    def test_three_author_opt_in_cli_and_four_work_holdout_isolation(self):
        out = StringIO()
        with redirect_stdout(out):
            self.assertEqual(cli.main(["voice", "--include-dostoevsky"]), 0)
        value = json.loads(out.getvalue())
        self.assertEqual(value["schema_version"], voice_profile.EXTENDED_VERSION)
        self.assertEqual(len(value["authors"]), 3)
        self.assertEqual(value["authors"][-1]["author_id"], "dostoevsky")
        self.assertIs(value["scientific_boundary"]["m3_accepted"], False)
        with tempfile.TemporaryDirectory() as directory:
            target = Path(directory) / "preview.json"
            with redirect_stdout(StringIO()):
                self.assertEqual(cli.main(["voice", "--include-dostoevsky",
                                           "--output", str(target)]), 0)
                self.assertEqual(cli.main(["voice", "--include-dostoevsky",
                                           "--check", str(target)]), 0)
            self.assertEqual(json.loads(target.read_text(encoding="utf-8")), value)
            with redirect_stderr(StringIO()), self.assertRaises(SystemExit):
                cli.main(["voice", "--include-dostoevsky", "--output", str(target)])
        with redirect_stdout(out := StringIO()):
            self.assertEqual(cli.main(["voice", "--include-dostoevsky",
                                       "--format", "markdown"]), 0)
        self.assertIn("Фёдор Достоевский", out.getvalue())
        for mode in ("--holdout", "--ablate"):
            with self.subTest(mode=mode):
                with redirect_stderr(StringIO()), self.assertRaises(SystemExit) as ex:
                    cli.main(["voice", "--include-dostoevsky", mode])
                self.assertEqual(ex.exception.code, 2)


if __name__ == "__main__":
    unittest.main()
