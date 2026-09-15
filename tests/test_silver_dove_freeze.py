from __future__ import annotations

from copy import deepcopy
import unittest

from scriptorium.silver_dove_freeze import (
    CANDIDATE_ID,
    SOURCE_REVISION_ID,
    SOURCE_REVISION_TIMESTAMP,
    WORK_TITLE,
    _EXPECTED_CATEGORIES,
    _EXPECTED_EDITORIAL_NOTE,
    _EXPECTED_SCAFFOLD,
    build_manifest,
    extract_silver_dove_body,
    replay_manifest,
)


def _source(literary: str) -> str:
    categories = " ".join(f"[[Категория:{name}]]" for name in _EXPECTED_CATEGORIES)
    return (
        "{{Отексте|АВТОР=Андрей Белый|ЛИЦЕНЗИЯ=PD-old}}\n"
        f"{_EXPECTED_SCAFFOLD}\n"
        "<center>ВМЕСТО ПРЕДИСЛОВИЯ</center>\n"
        f"{literary}\n"
        f"{_EXPECTED_EDITORIAL_NOTE} {categories}"
    )


class SilverDoveExtractionTests(unittest.TestCase):
    def test_extracts_authorial_front_matter_and_headings_only(self) -> None:
        body = extract_silver_dove_body(
            _source(
                "Авторский текст.\n"
                "{{right|''А. Белый''}}\n"
                "=== Глава первая. СЕЛО ЦЕЛЕБЕЕВО ===\n"
                "<center>'''''НАШЕ СЕЛО'''''</center>\n"
                "Продолжение <sup>1</sup>."
            )
        )
        self.assertIn("ВМЕСТО ПРЕДИСЛОВИЯ", body)
        self.assertIn("А. Белый", body)
        self.assertIn("Глава первая. СЕЛО ЦЕЛЕБЕЕВО", body)
        self.assertIn("НАШЕ СЕЛО", body)
        self.assertIn("Продолжение 1.", body)
        self.assertNotIn("Источник:", body)
        self.assertNotIn("Роман был опубликован впервые", body)
        self.assertNotIn("Категория:", body)

    def test_rejects_unknown_body_template(self) -> None:
        with self.assertRaisesRegex(ValueError, "unsupported template"):
            extract_silver_dove_body(_source("Литература. {{mystery|x}}"))

    def test_rejects_scaffold_drift(self) -> None:
        source = _source("Литература.").replace("Эл. версия:", "Электронная версия:", 1)
        with self.assertRaisesRegex(ValueError, "scaffolding drift"):
            extract_silver_dove_body(source)

    def test_rejects_editorial_category_drift(self) -> None:
        source = _source("Литература.").replace("[[Категория:Романы]]", "", 1)
        with self.assertRaisesRegex(ValueError, "category inventory drift"):
            extract_silver_dove_body(source)


class SilverDoveManifestTests(unittest.TestCase):
    def _fetcher(self, literary: str):
        source = _source(literary)

        def fetcher(_rows):
            return {
                WORK_TITLE: {
                    "revision_id": SOURCE_REVISION_ID,
                    "timestamp": SOURCE_REVISION_TIMESTAMP,
                    "mediawiki_sha1": "a" * 40,
                    "wikitext": source,
                }
            }

        return source, fetcher

    def test_capture_and_replay_are_source_free_and_fail_closed(self) -> None:
        source, capture_fetcher = self._fetcher("Текст повести. " * 26000)
        manifest = build_manifest(fetcher=capture_fetcher)
        self.assertEqual(manifest["candidate_id"], CANDIDATE_ID)
        self.assertGreaterEqual(
            manifest["composite_identity"]["character_count_including_spaces"], 300_000
        )
        serialized = repr(manifest)
        self.assertNotIn("Текст повести", serialized)
        self.assertIs(manifest["diagnostic_comparison_admissible"], False)
        self.assertIs(manifest["m2_parity_admissible"], False)

        def replay_fetcher(rows):
            rows = tuple(rows)
            self.assertEqual(len(rows), 1)
            self.assertEqual(rows[0]["revision_id"], SOURCE_REVISION_ID)
            return {WORK_TITLE: source}

        receipt = replay_manifest(manifest, fetcher=replay_fetcher)
        self.assertEqual(receipt["composite_identity"], manifest["composite_identity"])
        self.assertIs(receipt["source_text_included"], False)
        self.assertNotIn("Текст повести", repr(receipt))

    def test_capture_rejects_revision_drift(self) -> None:
        _source_text, fetcher = self._fetcher("Текст повести. " * 26000)

        def drifted(rows):
            result = fetcher(rows)
            result[WORK_TITLE]["revision_id"] = SOURCE_REVISION_ID + 1
            return result

        with self.assertRaisesRegex(ValueError, "current revision drift"):
            build_manifest(fetcher=drifted)

    def test_replay_rejects_identity_drift(self) -> None:
        source, fetcher = self._fetcher("Текст повести. " * 26000)
        manifest = build_manifest(fetcher=fetcher)
        drifted = deepcopy(manifest)
        drifted["composite_identity"]["raw_sha256"] = "0" * 64

        with self.assertRaisesRegex(ValueError, "composite identity drift"):
            replay_manifest(drifted, fetcher=lambda _rows: {WORK_TITLE: source})


if __name__ == "__main__":
    unittest.main()
