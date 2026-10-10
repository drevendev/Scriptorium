import contextlib
from hashlib import sha256
import io
import json
from pathlib import Path
import tempfile
import unittest

from scriptorium.analyze import build_local_analysis, main, render_html


SOURCE = "Кот, кот.\n— Да? — сказал он. — Нет."


class LocalAnalysisTests(unittest.TestCase):
    def test_build_binds_source_without_embedding_text(self):
        source = SOURCE.encode("utf-8")
        artifact = build_local_analysis(source, scriptorium_revision="abc123")
        serialized = json.dumps(artifact, ensure_ascii=False)
        self.assertEqual(artifact["schema_version"], "scriptorium-local-analysis-v1")
        self.assertEqual(artifact["source"]["raw_sha256"], sha256(source).hexdigest())
        self.assertFalse(artifact["source"]["source_text_embedded"])
        self.assertEqual(artifact["analyzer"]["scriptorium_revision"], "abc123")
        self.assertNotIn(SOURCE, serialized)
        self.assertEqual(len(artifact["metrics"]), 29)

    def test_short_input_is_valid_but_marked_less_representative(self):
        artifact = build_local_analysis(b"Short text.")
        status = artifact["representativeness"]
        self.assertFalse(status["meets_calibration_threshold"])
        self.assertEqual(status["calibration_threshold_characters"], 300000)
        self.assertIn("less representative", status["note"])

    def test_dictionary_dependency_is_explicit_and_not_source_text(self):
        artifact = build_local_analysis(
            "Кот пёс дракон".encode("utf-8"),
            dictionary_words=["кот", "пёс"],
            dictionary_profile="demo-v1",
        )
        dependency = artifact["analyzer"]["dependencies"]["vocabulary_dictionary"]
        self.assertEqual(dependency["profile"], "demo-v1")
        self.assertEqual(dependency["lexeme_count"], 2)
        self.assertEqual(artifact["metrics"]["fantlab.vocabulary.active_dictionary"]["value"], 2)
        self.assertEqual(artifact["metrics"]["fantlab.vocabulary.active_nondictionary"]["value"], 1)
        self.assertNotIn("дракон", json.dumps(artifact, ensure_ascii=False))

    def test_html_is_readable_accessible_and_source_free(self):
        artifact = build_local_analysis(SOURCE.encode("utf-8"))
        html = render_html(artifact, title="Demo <report>")
        self.assertIn("Demo &lt;report&gt;", html)
        self.assertIn('href="#main-content"', html)
        self.assertIn('id="main-content" tabindex="-1"', html)
        self.assertIn('tabindex="0" role="region"', html)
        self.assertIn('scope="col"', html)
        self.assertIn("*:focus-visible", html)
        self.assertIn("prefers-reduced-motion: reduce", html)
        self.assertIn("characters / word", html)
        self.assertIn("characters / sentence", html)
        self.assertNotIn(SOURCE, html)

    def test_deterministic_json_and_html(self):
        a = build_local_analysis(SOURCE.encode("utf-8"), scriptorium_revision="abc")
        b = build_local_analysis(SOURCE.encode("utf-8"), scriptorium_revision="abc")
        self.assertEqual(a, b)
        self.assertEqual(render_html(a), render_html(b))

    def test_cli_writes_json_and_html_create_only(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            source = root / "input.txt"
            json_out = root / "analysis.json"
            html_out = root / "analysis.html"
            source.write_text(SOURCE, encoding="utf-8")
            self.assertEqual(main([str(source), "--output", str(json_out)]), 0)
            self.assertEqual(
                main([str(source), "--format", "html", "--title", "Reader report", "--output", str(html_out)]),
                0,
            )
            self.assertEqual(json.loads(json_out.read_text(encoding="utf-8"))["schema_version"], "scriptorium-local-analysis-v1")
            self.assertIn("Reader report", html_out.read_text(encoding="utf-8"))
            before = html_out.read_bytes()
            with contextlib.redirect_stderr(io.StringIO()):
                with self.assertRaises(SystemExit):
                    main([str(source), "--format", "html", "--output", str(html_out)])
            self.assertEqual(html_out.read_bytes(), before)

    def test_cli_dictionary_pair_is_fail_closed(self):
        with tempfile.TemporaryDirectory() as tmp:
            source = Path(tmp) / "input.txt"
            source.write_text(SOURCE, encoding="utf-8")
            with contextlib.redirect_stderr(io.StringIO()):
                with self.assertRaises(SystemExit):
                    main([str(source), "--dictionary-profile", "demo-v1"])

    def test_cli_rejects_invalid_utf8(self):
        with tempfile.TemporaryDirectory() as tmp:
            source = Path(tmp) / "input.txt"
            source.write_bytes(b"\xff\xfe")
            with contextlib.redirect_stderr(io.StringIO()):
                with self.assertRaises(SystemExit):
                    main([str(source)])


if __name__ == "__main__":
    unittest.main()
