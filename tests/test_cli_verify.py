"""Positive and adversarial replay checks for private source-free JSON reports."""
import copy
import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest

from scriptorium.analyze import build_local_analysis
from scriptorium.verify import VerificationError, verify_private_report


def encoded(value):
    return json.dumps(value, ensure_ascii=False, sort_keys=True).encode("utf-8")


class PrivateVerificationTests(unittest.TestCase):
    def setUp(self):
        self.source = "Кот идёт. Пёс спит!\n".encode("utf-8")
        self.report = build_local_analysis(self.source)

    def test_full_replay_accepts_original_and_different_json_key_order(self):
        self.assertEqual(len(self.report["metrics"]), 29)
        self.assertIsNone(verify_private_report(self.source, encoded(self.report)))
        self.assertIsNone(verify_private_report(
            self.source, json.dumps(self.report, ensure_ascii=False).encode("utf-8")))

    def test_changed_manuscript_or_metric_must_fail(self):
        with self.assertRaisesRegex(VerificationError, "differs"):
            verify_private_report(self.source + b"!", encoded(self.report))
        tampered = copy.deepcopy(self.report)
        tampered["metrics"]["fantlab.general.characters"]["value"] = None
        with self.assertRaisesRegex(VerificationError, "differs"):
            verify_private_report(self.source, encoded(tampered))
        tampered = copy.deepcopy(self.report)
        tampered["metrics"]["fantlab.general.characters"]["value"] = True
        with self.assertRaisesRegex(VerificationError, "differs"):
            verify_private_report(self.source, encoded(tampered))

    def test_rejects_unknown_payload_private_text_and_revision_authenticity(self):
        tampered = copy.deepcopy(self.report)
        tampered["source"]["source_text"] = "SECRET private manuscript"
        with self.assertRaises(VerificationError):
            verify_private_report(self.source, encoded(tampered))
        with_revision = copy.deepcopy(self.report)
        with_revision["analyzer"]["scriptorium_revision"] = "untrusted-user-declaration"
        # The metadata is reproduced as a *declaration*, never authenticated.
        verify_private_report(self.source, encoded(with_revision))
        with_revision["analyzer"]["scriptorium_revision"] = 123
        with self.assertRaisesRegex(VerificationError, "revision"):
            verify_private_report(self.source, encoded(with_revision))

    def test_malformed_duplicate_nonfinite_and_schema(self):
        for raw in (b'{"schema_version":1,"schema_version":2}',
                    b'{"a":NaN}', b'{"a":1e999}',
                    b'{"schema_version":"other"}', b"\xff"):
            with self.subTest(raw=raw[:20]), self.assertRaises(VerificationError):
                verify_private_report(self.source, raw)

    def test_dictionary_requires_original_inputs_and_exact_profile(self):
        words = "кот\nпёс\n".encode("utf-8")
        with_dictionary = build_local_analysis(
            self.source, dictionary_words=words.decode("utf-8").splitlines(),
            dictionary_profile="local-lexicon-v1")
        with self.assertRaisesRegex(VerificationError, "dictionary"):
            verify_private_report(self.source, encoded(with_dictionary))
        verify_private_report(self.source, encoded(with_dictionary),
                              dictionary_bytes=words, dictionary_profile="local-lexicon-v1")
        with self.assertRaises(VerificationError):
            verify_private_report(self.source, encoded(with_dictionary),
                                  dictionary_bytes=words, dictionary_profile="wrong")
        with self.assertRaisesRegex(VerificationError, "UTF-8"):
            verify_private_report(self.source, encoded(with_dictionary),
                                  dictionary_bytes=b"\xff", dictionary_profile="local-lexicon-v1")

    def test_installed_style_cli_file_and_stdin_success_and_private_failures(self):
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            source = root / "secret-manuscript.txt"
            report = root / "secret-report.json"
            source.write_bytes(self.source)
            report.write_bytes(encoded(self.report))
            command = [sys.executable, "-m", "scriptorium", "verify"]
            file_run = subprocess.run([*command, str(source), str(report)],
                                      capture_output=True, timeout=30)
            self.assertEqual(file_run.returncode, 0, file_run.stderr.decode())
            self.assertIn(b"29 metrics", file_run.stdout)
            pipe_run = subprocess.run([*command, "-", str(report)], input=self.source,
                                      capture_output=True, timeout=30)
            self.assertEqual(pipe_run.returncode, 0, pipe_run.stderr.decode())
            report.write_bytes(encoded({**self.report, "injected_text": "SECRET private manuscript"}))
            bad = subprocess.run([*command, str(source), str(report)],
                                 capture_output=True, timeout=30)
            self.assertEqual(bad.returncode, 2)
            self.assertNotIn(b"secret-manuscript", bad.stderr)
            self.assertNotIn(b"secret-report", bad.stderr)
            self.assertNotIn(b"SECRET private manuscript", bad.stderr)


if __name__ == "__main__":
    unittest.main()
