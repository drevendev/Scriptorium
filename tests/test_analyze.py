import contextlib
import copy
from decimal import Decimal
from hashlib import sha256
import io
import json
from pathlib import Path
import tempfile
import unittest

from scriptorium.analyze import build_local_analysis, main, render_html, render_markdown
from scriptorium.metric_labels import METRIC_LABELS, METRIC_LABELS_RU


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



    def test_html_shows_all_29_source_bound_russian_labels_with_english_and_ids(self):
        self.assertEqual(set(METRIC_LABELS_RU), set(METRIC_LABELS))
        artifact = build_local_analysis(SOURCE.encode("utf-8"))
        html = render_html(artifact, title="Русский <отчёт>")
        self.assertIn("<html lang=\"en\">", html)
        self.assertIn("Русский &lt;отчёт&gt;", html)
        for metric_id, russian_label in METRIC_LABELS_RU.items():
            with self.subTest(metric_id=metric_id):
                self.assertIn(
                    f'<span class="metric-label">{METRIC_LABELS[metric_id]}</span>'
                    f'<span class="metric-label-ru" lang="ru">{russian_label}</span>'
                    f'<code class="metric-id">{metric_id}</code>',
                    html,
                )
                self.assertIn(
                    f'{METRIC_LABELS[metric_id]}, {russian_label}, metric ID {metric_id}',
                    html,
                )
        self.assertIn('lang="ru">Запятые</span>', html)
        self.assertIn('lang="ru">Доля диалогов</span>', html)
        self.assertNotIn(SOURCE, html)
        self.assertNotIn("<script", html)

    def test_html_bilingual_labels_do_not_bypass_metric_contract(self):
        artifact = build_local_analysis(SOURCE.encode("utf-8"))
        altered = copy.deepcopy(artifact)
        altered["metrics"]["fantlab.general.words"]["compatibility_status"] = "extension"
        with self.assertRaisesRegex(ValueError, "metric evidence status changed"):
            render_html(altered)

    def test_dialogue_share_chart_is_fixed_scale_and_source_bound(self):
        original = build_local_analysis(SOURCE.encode("utf-8"))
        self.assertIn('id="dialogue-chart-heading"', render_html(original))
        metric_id = "fantlab.dialogue.share_percent"
        for share in (0, 23.25, 100, Decimal("0.000001")):
            with self.subTest(share=share):
                artifact = copy.deepcopy(original)
                artifact["metrics"][metric_id]["value"] = share
                html = render_html(artifact)
                chart = html.split('id="dialogue-chart-heading"', 1)[1].split("</section>", 1)[0]
                self.assertIn(f'width: {Decimal(str(share)):.2f}%', chart)
                self.assertIn(f'<strong>{share}%</strong>', chart)
                self.assertIn("absolute 0–100% scale", chart)
                self.assertIn("not necessarily narration", chart)
                if share > 0:
                    self.assertIn('data-nonzero="true"', chart)
                else:
                    self.assertNotIn('data-nonzero="true"', chart)
                self.assertNotIn("<script", html)

    def test_dialogue_share_chart_unavailable_and_bad_input(self):
        original = build_local_analysis(SOURCE.encode("utf-8"))
        metric_id = "fantlab.dialogue.share_percent"
        absent = copy.deepcopy(original)
        absent["metrics"][metric_id]["value"] = None
        html = render_html(absent)
        chart = html.split('id="dialogue-chart-heading"', 1)[1].split("</section>", 1)[0]
        self.assertIn("Dialogue share unavailable — not zero", chart)
        self.assertNotIn('class="dialogue-fill"', chart)
        for share in (-0.01, 100.01, True, float("nan"), float("inf"), "25"):
            with self.subTest(share=share):
                altered = copy.deepcopy(original)
                altered["metrics"][metric_id]["value"] = share
                with self.assertRaises(ValueError):
                    render_html(altered)
        wrong_unit = copy.deepcopy(original)
        wrong_unit["metrics"][metric_id]["unit"] = "characters"
        # Unit mismatch is rejected by the shared registered metric contract,
        # before chart-specific rendering can label a false percentage.
        with self.assertRaisesRegex(ValueError, "registered metric contract mismatch"):
            render_html(wrong_unit)

    def test_punctuation_chart_is_source_bound_exact_and_accessible(self):
        artifact = build_local_analysis(SOURCE.encode("utf-8"))
        html = render_html(artifact)
        rows = {name: row for name, row in artifact["metrics"].items()
                if name.startswith("fantlab.punctuation.")}
        self.assertEqual(len(rows), 14)
        self.assertEqual(html.count('class="punctuation-item"'), len(rows))
        self.assertIn('aria-labelledby="punctuation-chart-heading"', html)
        self.assertIn('aria-hidden="true"', html)
        self.assertIn('Tiny nonzero rates retain a visible tick', html)
        self.assertIn('print-color-adjust: exact', html)
        self.assertNotIn("<script", html)
        rates = [Decimal(str(row["value"])) for row in rows.values() if row["value"] is not None]
        maximum = max(rates, default=Decimal(0))
        for metric_id, row in rows.items():
            with self.subTest(metric_id=metric_id):
                part = html.split(f'data-metric-id="{metric_id}"', 1)[1].split("</li>", 1)[0]
                if row["value"] is None:
                    self.assertIn("Unavailable — not zero", part)
                    self.assertNotIn('class="punctuation-fill"', part)
                else:
                    rate = Decimal(str(row["value"]))
                    width = (rate / maximum * 100) if maximum else Decimal(0)
                    self.assertIn(f'width: {width:.2f}%', part)
                    self.assertIn(f'{row["value"]} occurrences / 1,000 words', part)
                    if rate > 0:
                        self.assertIn('data-nonzero="true"', part)
        self.assertIn('Punctuation: local metrics and evidence', html)

    def test_punctuation_chart_keeps_unknown_and_rejects_impossible_values(self):
        empty = build_local_analysis(b"")
        html = render_html(empty)
        self.assertIn("All punctuation rates are unavailable", html)
        self.assertIn("Unavailable — not zero", html)
        metric_id = "fantlab.punctuation.dash.per_1000_words"
        original = build_local_analysis(SOURCE.encode("utf-8"))
        for value in (-1, True, float("nan"), float("inf"), "6"):
            with self.subTest(value=value):
                altered = copy.deepcopy(original)
                altered["metrics"][metric_id]["value"] = value
                with self.assertRaises(ValueError):
                    render_html(altered)
        zero = copy.deepcopy(original)
        zero["metrics"][metric_id]["value"] = 0
        zero_html = render_html(zero)
        part = zero_html.split(f'data-metric-id="{metric_id}"', 1)[1].split("</li>", 1)[0]
        self.assertIn('style="width: 0.00%"', part)
        self.assertNotIn('data-nonzero="true"', part)
        tiny = copy.deepcopy(original)
        tiny["metrics"][metric_id]["value"] = Decimal("1E-30")
        tiny_html = render_html(tiny)
        tiny_part = tiny_html.split(f'data-metric-id="{metric_id}"', 1)[1].split("</li>", 1)[0]
        self.assertIn('data-nonzero="true"', tiny_part)
        self.assertIn('1E-30 occurrences / 1,000 words', tiny_part)

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


    def test_markdown_report_has_all_metrics_and_source_provenance(self):
        artifact = build_local_analysis(SOURCE.encode("utf-8"), scriptorium_revision="abc")
        report = render_markdown(artifact, title="Demo | <script>alert(1)</script>")
        self.assertIn("# Demo \\| &lt;script&gt;alert(1)&lt;/script&gt;", report)
        self.assertNotIn("<script>", report)
        self.assertIn(artifact["source"]["raw_sha256"], report)
        self.assertIn(artifact["source"]["normalized_sha256"], report)
        self.assertIn("Short input: valid local analysis", report)
        self.assertIn("NOT** verified FantLab parity", report)
        metric_lines = [
            line for line in report.splitlines()
            if line.startswith("| ") and (
                "| fantlab." in line or "| scriptorium." in line
            )
        ]
        self.assertEqual(len(metric_lines), 29)
        self.assertIn("| Words | fantlab.general.words |", report)
        self.assertIn("inferred", report)
        self.assertIn("extension", report)
        self.assertNotIn(SOURCE, report)
        self.assertEqual(report, render_markdown(artifact, title="Demo | <script>alert(1)</script>"))

    def test_markdown_unknown_is_not_zero_and_profiles_are_bound(self):
        empty = build_local_analysis(b"")
        report = render_markdown(empty)
        self.assertIn("| Words | fantlab.general.words | 0 |", report)
        self.assertIn(
            "| Dictionary variety · 3,000-word window | "
            "fantlab.vocabulary.uasz_3000 | Unavailable |", report
        )
        self.assertIn("Dictionary: not supplied", report)
        self.assertIn(empty["analyzer"]["profiles"]["metrics"], report)

    def test_markdown_rejects_tampered_or_untrustworthy_evidence(self):
        original = build_local_analysis(SOURCE.encode("utf-8"))
        changes = [
            lambda a: a["source"].update(source_text_embedded=True),
            lambda a: a["source"].update(raw_sha256="not-a-hash"),
            lambda a: a["metrics"]["fantlab.general.words"].update(value=float("nan")),
            lambda a: a["metrics"]["fantlab.general.words"].update(value=True),
            lambda a: a["metrics"]["fantlab.general.words"].update(compatibility_status="reproduced"),
            lambda a: a["analyzer"]["profiles"].update(metrics=None),
        ]
        for change in changes:
            with self.subTest(change=changes.index(change)):
                artifact = copy.deepcopy(original)
                change(artifact)
                with self.assertRaises(ValueError):
                    render_markdown(artifact)

    def test_markdown_cli_stdout_and_create_only_are_reproducible(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            source = root / "private.txt"
            target = root / "report.md"
            source.write_text(SOURCE, encoding="utf-8")
            expected = render_markdown(build_local_analysis(source.read_bytes()))
            with contextlib.redirect_stdout(io.StringIO()) as stream:
                self.assertEqual(main([str(source), "--format", "markdown"]), 0)
            self.assertEqual(stream.getvalue(), expected)
            self.assertEqual(main([str(source), "--format", "markdown",
                                   "--output", str(target)]), 0)
            self.assertEqual(target.read_text(encoding="utf-8"), expected)
            before = target.read_bytes()
            with contextlib.redirect_stderr(io.StringIO()), self.assertRaises(SystemExit):
                main([str(source), "--format", "markdown", "--output", str(target)])
            self.assertEqual(target.read_bytes(), before)
            with contextlib.redirect_stderr(io.StringIO()), self.assertRaises(SystemExit):
                main([str(source), "--format", "markdown", "--output", str(source)])
            self.assertEqual(source.read_bytes(), SOURCE.encode("utf-8"))


if __name__ == "__main__":
    unittest.main()
