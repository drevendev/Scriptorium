"""Synthetic positive/negative source, chapter, privacy and metric regressions."""
from __future__ import annotations

from copy import deepcopy
from hashlib import sha256
import json
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch

from scriptorium import oblomov_diagnostic as diag


def _wikitext() -> str:
    header = (
        "{{Отексте\n| АВТОР = Иван Александрович Гончаров\n"
        "| НАЗВАНИЕ = Обломов\n| ДАТАПУБЛИКАЦИИ = 1859\n"
        "| ИСТОЧНИК = [" + diag.SOURCE_WITNESS + " az.lib.ru]\n"
        "| ЛИЦЕНЗИЯ = PD-old\n| СТИЛЬ = text\n}}\n"
    )
    headings = diag.expected_headings()
    paragraphs = []
    for name in headings:
        paragraphs.append("=== " + name + " ===\n")
        if name == "Обломов":
            paragraphs.append("<center>''Роман в\u00a0четырех частях''</center>\n")
        elif name not in diag._PARTS:
            paragraphs.append(("В Гороховой улице стояла тишина и дул лёгкий ветер.\n" * 155) + "\n")
    paragraphs.append("И он рассказал ему, что здесь написано.\n")
    footer = (
        "''1857 и 1858\u00a0гг.''\n{{---|width=10em}}\n"
        "''Впервые полностью опубликован в 1859.''\n"
        "''Версия 1.0. Сверка произведена по изд. 1954.''\n"
        "[[Категория:Обломов (Гончаров)]]\n"
    )
    return header + "".join(paragraphs) + footer


def _fetcher(wikitext: str):
    raw = wikitext.encode("utf-8")
    identity = {
        "title": diag.TITLE, "revision_id": diag.REVISION_ID, "page_id": 91991,
        "revision_timestamp": "2026-06-22T08:35:00Z",
        "mediawiki_sha1": "a" * 40, "wikitext_sha256": sha256(raw).hexdigest(),
        "wikitext_character_count": len(wikitext), "wikitext_utf8_byte_count": len(raw),
        "wikitext": wikitext,
    }
    return lambda *, title, revision_id: deepcopy(identity)


class OblomovMeasureTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.raw = _wikitext()
        cls.body = diag.extract_literary_body(cls.raw)

    def test_full_four_part_book_and_measured_rows(self):
        self.assertGreaterEqual(len(self.body), 300_000)
        self.assertEqual(len(diag.expected_headings()), 51)
        artifact = diag.build_diagnostic(fetcher=_fetcher(self.raw))
        self.assertEqual(artifact["body"]["characters_including_spaces"], len(self.body))
        self.assertEqual(len(artifact["metric_rows"]), 29)
        self.assertEqual(artifact["gates"]["m2_weight"], 0)
        self.assertFalse(artifact["gates"]["m2_parity_admissible"])
        self.assertEqual(artifact["gates"]["fantlab_input_identity"], "UNKNOWN")
        rows = {row["metric_id"]: row for row in artifact["metric_rows"]}
        self.assertEqual(rows["fantlab.general.characters"]["actual"], len(self.body))
        self.assertEqual(rows["fantlab.vocabulary.uasz_3000"]["result"], "NOT_RUN_DICTIONARY_UNBOUND")
        self.assertIsNone(rows["fantlab.vocabulary.uasz_3000"]["actual"])
        self.assertIsNone(rows["fantlab.general.characters"]["fantlab_display"])
        serialized = diag.render_json(artifact)
        self.assertNotIn("В Гороховой улице стояла", serialized)
        self.assertNotIn('"wikitext":', serialized)
        self.assertNotIn("И он рассказал ему", serialized)
        self.assertEqual(json.loads(serialized), artifact)

    def test_attested_wikisource_heading_break_without_prose_markup(self):
        actual_style = self.raw.replace("=== IX Сон Обломова ===",
                                        "=== IX <br>Сон Обломова ===", 1)
        literary = diag.extract_literary_body(actual_style)
        self.assertEqual(literary, self.body)

    def test_missing_chapter_and_tampered_footer_fail_closed(self):
        changed = self.raw.replace("=== VII ===", "=== VII СТРАНИЦА ПОТЕРЯНА ===", 1)
        with self.assertRaisesRegex(ValueError, "chapter inventory"):
            diag.extract_literary_body(changed)
        changed = self.raw.replace("Сверка произведена по изд. 1954", "Сверка неизвестна")
        with self.assertRaisesRegex(ValueError, "editorial witness"):
            diag.extract_literary_body(changed)

    def test_rights_boundary_and_partial_novel_fail_closed(self):
        changed = self.raw.replace("| ЛИЦЕНЗИЯ = PD-old", "| ЛИЦЕНЗИЯ = unknown")
        with self.assertRaisesRegex(ValueError, "public-domain"):
            diag.extract_literary_body(changed)
        changed = self.raw.replace("И он рассказал ему, что здесь написано.", "Конец оборван.")
        with self.assertRaisesRegex(ValueError, "end of novel"):
            diag.extract_literary_body(changed)

    def test_revision_identity_mutation_rejected_before_metrics(self):
        def changed_fetch(*, title, revision_id):
            response = _fetcher(self.raw)(title=title, revision_id=revision_id)
            response["wikitext_sha256"] = "f" * 64
            return response
        with patch.object(diag, "analyze_deterministic_metrics") as analyzer:
            with self.assertRaisesRegex(ValueError, "identity drift"):
                diag.build_diagnostic(fetcher=changed_fetch)
            analyzer.assert_not_called()

    def test_create_only_json_output_never_overwrites(self):
        artifact = {"body": {"characters_including_spaces": 320000}, "gates": {"source_text_committed": False}}
        with tempfile.TemporaryDirectory() as temporary:
            path = Path(temporary) / "measured.json"
            with patch.object(diag, "build_diagnostic", return_value=artifact):
                self.assertEqual(diag.main(["--output", str(path)]), 0)
                before = path.read_bytes()
                with self.assertRaises(FileExistsError):
                    diag.main(["--output", str(path)])
                self.assertEqual(path.read_bytes(), before)


if __name__ == "__main__":
    unittest.main()
