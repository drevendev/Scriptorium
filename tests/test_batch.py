"""Real in-process Reader batch CLI, disk and privacy regressions (no engine stubs)."""
from __future__ import annotations

import contextlib
from hashlib import sha256
import io
import json
import os
from pathlib import Path
import tempfile
import unittest

from scriptorium import batch, cli


class PrivateBatchTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        self.manifest = self.root / "manifest.json"
        self.output = self.root / "private-results"

    def write_manifest(self, items):
        self.manifest.write_text(json.dumps({
            "schema_version": batch.MANIFEST_SCHEMA, "files": items,
        }), encoding="utf-8")

    def invoke(self):
        return cli.main(["batch", str(self.manifest), "--output-dir", str(self.output)])

    def index(self):
        paths = list(self.output.glob("batch-*.json"))
        self.assertEqual(len(paths), 1)
        return json.loads(paths[0].read_text(encoding="utf-8"))

    def test_real_two_works_duplicate_idempotent_and_private(self):
        self.write_manifest(["alpha.txt", "beta.txt", "alpha.txt"])
        a, b = b"Cat sleeps.", "Кот идёт. Пёс спит.".encode()
        (self.root / "alpha.txt").write_bytes(a)
        (self.root / "beta.txt").write_bytes(b)
        self.assertEqual(self.invoke(), 0)
        result = self.index()
        self.assertEqual((result["completed"], result["failed"]), (3, 0))
        self.assertEqual(result["entries"][0]["reports"], result["entries"][2]["reports"])
        self.assertNotEqual(result["entries"][0]["reports"], result["entries"][1]["reports"])
        self.assertEqual(result["entries"][0]["raw_sha256"], sha256(a).hexdigest())
        self.assertEqual(len(list(self.output.glob("work-*.json"))), 2)
        for row in result["entries"]:
            for route in row["reports"].values():
                self.assertEqual(Path(route).name, route)
                self.assertTrue((self.output / route).is_file())
            real = json.loads((self.output / row["reports"]["json"]).read_text(encoding="utf-8"))
            self.assertEqual(real["schema_version"], "scriptorium-local-analysis-v1")
            self.assertEqual(len(real["metrics"]), 29)
            self.assertFalse(real["source"]["source_text_embedded"])
        self.assertEqual(len(list(self.output.glob("batch-*.csv"))), 1)
        self.assertEqual(len(list(self.output.glob("batch-*.html"))), 1)
        before = {p.name: p.read_bytes() for p in self.output.iterdir()}
        self.assertEqual(self.invoke(), 0)
        self.assertEqual(before, {p.name: p.read_bytes() for p in self.output.iterdir()})
        joined = b"".join(before.values())
        self.assertNotIn(b"Cat sleeps", joined)
        self.assertNotIn(str(self.root).encode(), joined)

    def test_partial_failure_is_explicit_and_retry_is_deterministic(self):
        self.write_manifest(["good.txt", "bad.txt", "missing.txt"])
        (self.root / "good.txt").write_bytes("Один текст.".encode())
        (self.root / "bad.txt").write_bytes(b"\xff")
        self.assertEqual(self.invoke(), 1)
        data = self.index()
        self.assertEqual((data["completed"], data["failed"]), (1, 2))
        self.assertEqual([row["status"] for row in data["entries"]], ["ok", "error", "error"])
        for row in data["entries"][1:]:
            self.assertIsNone(row["reports"])
            self.assertIsNotNone(row["error"])
        old = {p.name: p.read_bytes() for p in self.output.iterdir()}
        self.assertEqual(self.invoke(), 1)
        self.assertEqual(old, {p.name: p.read_bytes() for p in self.output.iterdir()})

    def test_bad_manifest_duplicate_keys_traversal_no_outputs(self):
        for raw in (
            '{"schema_version":"scriptorium-private-batch-manifest-v1","files":["ok"],"files":["evil"]}',
            '{"schema_version":"scriptorium-private-batch-manifest-v1","files":["../secret"]}',
            '{"schema_version":"scriptorium-private-batch-manifest-v1","files":["/secret"]}',
            '{"schema_version":"scriptorium-private-batch-manifest-v1","files":["a//b"]}',
        ):
            self.manifest.write_text(raw, encoding="utf-8")
            with contextlib.redirect_stderr(io.StringIO()), self.assertRaises(SystemExit) as caught:
                self.invoke()
            self.assertEqual(caught.exception.code, 2)
            self.assertFalse(self.output.exists())

    def test_symlink_input_and_huge_input_fail_without_paths(self):
        self.write_manifest(["good.txt", "alias.txt", "huge.txt"])
        (self.root / "good.txt").write_text("Valid.", encoding="utf-8")
        (self.root / "alias.txt").symlink_to(self.root / "good.txt")
        (self.root / "huge.txt").write_bytes(b"x" * 100)
        old_limit = batch.MAX_ANALYSIS_BYTES
        try:
            batch.MAX_ANALYSIS_BYTES = 50
            self.assertEqual(self.invoke(), 1)
        finally:
            batch.MAX_ANALYSIS_BYTES = old_limit
        self.assertEqual(self.index()["failed"], 2)

    def test_conflicting_existing_report_and_index_preserved(self):
        self.write_manifest(["one.txt"])
        (self.root / "one.txt").write_text("Текст.", encoding="utf-8")
        self.assertEqual(self.invoke(), 0)
        index_before = self.index()
        index_file = next(self.output.glob("batch-*.json"))
        old_index_bytes = index_file.read_bytes()
        report_path = self.output / index_before["entries"][0]["reports"]["json"]
        report_path.write_text("preexisting changed report", encoding="utf-8")
        errors = io.StringIO()
        with contextlib.redirect_stderr(errors), self.assertRaises(SystemExit) as caught:
            self.invoke()
        self.assertEqual(caught.exception.code, 2)
        self.assertNotIn(str(self.root), errors.getvalue())
        self.assertEqual(report_path.read_text(), "preexisting changed report")
        self.assertEqual(index_file.read_bytes(), old_index_bytes)

    def test_interrupted_publication_retries_without_replacement(self):
        self.write_manifest(["one.txt"])
        (self.root / "one.txt").write_text("Текст.", encoding="utf-8")
        original = batch._publish
        count = [0]

        def interrupted(*args):
            count[0] += 1
            if count[0] == 2:
                raise OSError("PRIVATE-PATH power loss")
            return original(*args)

        from unittest.mock import patch
        errors = io.StringIO()
        with patch.object(batch, "_publish", side_effect=interrupted), \
             contextlib.redirect_stderr(errors), self.assertRaises(SystemExit):
            self.invoke()
        self.assertNotIn("PRIVATE-PATH", errors.getvalue())
        self.assertFalse(list(self.output.glob("batch-*.json")))
        self.assertEqual(self.invoke(), 0)
        self.assertEqual(self.index()["failed"], 0)

    def test_output_directory_cannot_be_symlink_or_public(self):
        self.write_manifest(["one.txt"])
        (self.root / "one.txt").write_bytes(b"one")
        self.output.symlink_to(self.root, target_is_directory=True)
        with contextlib.redirect_stderr(io.StringIO()), self.assertRaises(SystemExit):
            self.invoke()
        self.output.unlink()
        self.output.mkdir(mode=0o755)
        os.chmod(self.output, 0o755)
        with contextlib.redirect_stderr(io.StringIO()), self.assertRaises(SystemExit):
            self.invoke()
        self.assertEqual(list(self.output.iterdir()), [])


if __name__ == "__main__":
    unittest.main()
