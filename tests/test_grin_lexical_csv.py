"""Exact offline replay of the separately reviewed public aggregate CSV."""
from contextlib import redirect_stderr, redirect_stdout
import io
from pathlib import Path
import tempfile
import unittest

from scriptorium.grin_lexical_csv import main, render_reviewed_csv

ROOT = Path(__file__).resolve().parents[1]
JSON = ROOT / "assets/grin-lexical-diagnostic.json"
CSV = ROOT / "assets/grin-lexical-diagnostic.csv"


class GrinLexicalCSVTests(unittest.TestCase):
    def test_exact_replay_and_stdout(self):
        expected = CSV.read_bytes()
        self.assertEqual(render_reviewed_csv(JSON.read_bytes()).encode("utf-8"), expected)
        out = io.StringIO()
        with redirect_stdout(out):
            self.assertEqual(main([str(JSON)]), 0)
        self.assertEqual(out.getvalue().encode("utf-8"), expected)

    def test_projection_mutations_are_refused(self):
        payload = JSON.read_bytes()
        for changed in (payload + b"\n", payload.replace(b"5901", b"5902"),
                        payload.replace(b"Public-domain", b"Private prose"), b"{}"):
            with self.subTest(changed=changed[:10]), self.assertRaises(ValueError):
                render_reviewed_csv(changed)

    def test_create_only_and_exact_check(self):
        with tempfile.TemporaryDirectory() as tmp:
            output = Path(tmp) / "out.csv"
            self.assertEqual(main([str(JSON), "--output", str(output)]), 0)
            self.assertEqual(output.read_bytes(), CSV.read_bytes())
            self.assertEqual(main([str(JSON), "--check", str(output)]), 0)
            output.write_bytes(b"stale")
            for flag in ("--check", "--output"):
                with self.subTest(flag=flag), redirect_stderr(io.StringIO()), self.assertRaises(SystemExit):
                    main([str(JSON), flag, str(output)])
                self.assertEqual(output.read_bytes(), b"stale")

    def test_bad_input_never_creates_output(self):
        with tempfile.TemporaryDirectory() as tmp:
            bad = Path(tmp) / "bad.json"
            bad.write_bytes(b"{}")
            output = Path(tmp) / "out.csv"
            for source in (bad, Path(tmp), Path(tmp) / "absent"):
                with self.subTest(source=source.name), redirect_stderr(io.StringIO()), self.assertRaises(SystemExit):
                    main([str(source), "--output", str(output)])
                self.assertFalse(output.exists())


if __name__ == "__main__":
    unittest.main()
