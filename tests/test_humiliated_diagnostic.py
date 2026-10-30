"""Synthetic positive/negative source, rights, completeness, metric and privacy tests."""
from __future__ import annotations

from copy import deepcopy
from hashlib import sha256
import json
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch

from scriptorium import humiliated_diagnostic as diag


def _wikitext() -> str:
    header = (
        "{{Отексте\n| АВТОР = Федор Михайлович Достоевский\n"
        "| НАЗВАНИЕ = Униженные и оскорбленные\n| ДАТАПУБЛИКАЦИИ = 1861\n"
        "| ИСТОЧНИК = [https://az.lib.ru/d/dostoewskij_f_m/ az.lib.ru]\n"
        "| ЛИЦЕНЗИЯ = PD-old\n}}\n=== Униженные и оскорбленные ===\n"
        "<center>''Роман в четырех частях с эпилогом''</center>\n"
    )
    parts = []
    for heading in diag.expected_headings()[1:]:
        parts.append("=== " + heading + " ===\n")
        if heading == "Глава I" and len(parts) == 2:
            parts.append("Прошлого года, двадцать второго марта, вечером.\n")
        if heading.startswith("Глава "):
            parts.append("Читатель слышит историю в городе и молчаливом доме.\n" * 160)
    parts.append("Мы бы могли быть навеки счастливы вместе!\n")
    footer = ("=== Комментарии ===\n(N. Ф. Буданова)\nБуданова. "
              "Впервые опубликовано в журнале Время.\n")
    return header + "".join(parts) + footer


def _fetcher(wikitext: str):
    encoded = wikitext.encode("utf-8")
    source = {
        "title": diag.TITLE,
        "revision_id": diag.REVISION_ID,
        "page_id": 91992,
        "revision_timestamp": "2025-08-29T08:05:00Z",
        "mediawiki_sha1": "a" * 40,
        "wikitext_character_count": len(wikitext),
        "wikitext_utf8_byte_count": len(encoded),
        "wikitext_sha256": sha256(encoded).hexdigest(),
        "wikitext": wikitext,
    }
    return lambda *, title, revision_id: deepcopy(source)


class HumiliatedMeasureTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.source = _wikitext()
        cls.body = diag.extract_literary_body(cls.source)

    def test_four_parts_45_chapters_and_epilogue_with_real_metrics(self):
        self.assertEqual(len(diag.expected_headings()), 52)
        self.assertGreaterEqual(len(self.body), 300_000)
        artifact = diag.build_diagnostic(fetcher=_fetcher(self.source))
        self.assertEqual(len(artifact["metric_rows"]), 29)
        self.assertEqual(artifact["body"]["characters_including_spaces"], len(self.body))
        self.assertEqual(artifact["gates"]["m2_weight"], 0)
        self.assertFalse(artifact["gates"]["m2_parity_admissible"])
        self.assertEqual(artifact["gates"]["fantlab_input_identity"], "UNKNOWN")
        rows = {row["metric_id"]: row for row in artifact["metric_rows"]}
        self.assertEqual(rows["fantlab.general.characters"]["actual"], len(self.body))
        self.assertIsNone(rows["fantlab.vocabulary.uasz_10000"]["actual"])
        self.assertEqual(rows["fantlab.vocabulary.uasz_10000"]["result"],
                         "NOT_RUN_DICTIONARY_UNBOUND")
        serialized = diag.render_json(artifact)
        self.assertNotIn("Читатель слышит историю", serialized)
        self.assertNotIn("Впервые опубликовано", serialized)
        self.assertNotIn('"wikitext":', serialized)
        self.assertEqual(json.loads(serialized), artifact)

    def test_pinned_title_nbsp_variant_is_source_bound(self):
        """The exact Wiki revision uses a non-breaking space in the title heading."""
        nbsp = self.source.replace(
            "=== Униженные и оскорбленные ===",
            "=== Униженные и\u00a0оскорбленные ===",
            1,
        )
        self.assertEqual(diag.extract_literary_body(nbsp), self.body)
        artifact = diag.build_diagnostic(fetcher=_fetcher(nbsp))
        self.assertEqual(artifact["body"]["raw_sha256"], sha256(self.body.encode("utf-8")).hexdigest())
        self.assertNotEqual(
            artifact["source"]["wikitext_sha256"],
            sha256(self.source.encode("utf-8")).hexdigest(),
        )
        duplicated = nbsp.replace(
            "=== Униженные и\u00a0оскорбленные ===",
            "=== Униженные и\u00a0оскорбленные ===\n=== Униженные и оскорбленные ===",
            1,
        )
        with self.assertRaisesRegex(ValueError, "heading inventory"):
            diag.extract_literary_body(duplicated)

    def test_commentary_not_in_body(self):
        self.assertNotIn("Буданова", self.body)
        self.assertNotIn("Впервые опубликовано", self.body)

    def test_wrong_chapter_sequence_and_partial_epilogue_fail(self):
        bad = self.source.replace("=== Глава XV ===", "=== Глава XIV ===", 1)
        with self.assertRaisesRegex(ValueError, "heading inventory"):
            diag.extract_literary_body(bad)
        bad = self.source.replace("навеки счастливы вместе", "неизвестный конец")
        with self.assertRaisesRegex(ValueError, "ending of epilogue"):
            diag.extract_literary_body(bad)

    def test_rights_and_editorial_comment_boundary_fail(self):
        bad = self.source.replace("| ЛИЦЕНЗИЯ = PD-old", "| ЛИЦЕНЗИЯ = unknown")
        with self.assertRaisesRegex(ValueError, "public-domain"):
            diag.extract_literary_body(bad)
        bad = self.source.replace("=== Комментарии ===", "=== ЭПИЛОГ ===")
        with self.assertRaisesRegex(ValueError, "editorial-commentary boundary"):
            diag.extract_literary_body(bad)

    def test_unexpanded_markup_is_rejected(self):
        bad = self.source.replace("Читатель слышит историю", "{{ИСКАЖЕНО}} Читатель слышит историю", 1)
        with self.assertRaisesRegex(ValueError, "markup"):
            diag.extract_literary_body(bad)

    def test_revision_identity_drift_rejected_before_metrics(self):
        def bad_fetch(*, title, revision_id):
            source = _fetcher(self.source)(title=title, revision_id=revision_id)
            source["wikitext_sha256"] = "0" * 64
            return source
        with patch.object(diag, "analyze_deterministic_metrics") as analyzer:
            with self.assertRaisesRegex(ValueError, "identity drift"):
                diag.build_diagnostic(fetcher=bad_fetch)
            analyzer.assert_not_called()

    def test_create_only_output_cannot_overwrite(self):
        artifact = {"gates": {"source_text_committed": False},
                    "body": {"characters_including_spaces": 345678}}
        with tempfile.TemporaryDirectory() as directory:
            out = Path(directory) / "source-free.json"
            with patch.object(diag, "build_diagnostic", return_value=artifact):
                self.assertEqual(diag.main(["--output", str(out)]), 0)
                before = out.read_bytes()
                with self.assertRaises(FileExistsError):
                    diag.main(["--output", str(out)])
                self.assertEqual(out.read_bytes(), before)


if __name__ == "__main__":
    unittest.main()
