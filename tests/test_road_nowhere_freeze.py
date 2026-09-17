import hashlib
import unittest

from scriptorium.road_nowhere_freeze import (
    CANDIDATE_ID,
    EXTRACTION_PROFILE,
    REVISION_ID,
    TITLE,
    build_body_manifest,
    extract_literary_body,
    replay_body_manifest,
    validate_body_manifest,
)


def _source(literary="Основной текст."):
    headings = "\n\n".join(f"=== Заголовок {index} ===\nАбзац {index}." for index in range(1, 28))
    categories = "\n".join(f"[[Категория:Тест {index}]]" for index in range(1, 6))
    return (
        "{{Отексте\n"
        "<!-- scaffold comment 1 -->\n"
        "|источник=az.lib.ru\n"
        "<!-- scaffold comment 2 -->\n"
        "}}\n"
        f"{literary}\n\n{headings}\n{categories}\n"
    )


def _identity(wikitext):
    raw = wikitext.encode("utf-8")
    return {
        "title": TITLE,
        "page_id": 1003775,
        "revision_id": REVISION_ID,
        "revision_timestamp": "2025-07-30T20:33:01Z",
        "mediawiki_sha1": "1" * 40,
        "wikitext_character_count": len(wikitext),
        "wikitext_utf8_byte_count": len(raw),
        "wikitext_sha256": hashlib.sha256(raw).hexdigest(),
    }


def _revision_manifest(wikitext):
    return {
        "manifest_version": "scriptorium-single-page-source-revision-v1",
        "candidate_id": CANDIDATE_ID,
        "provider": "Russian Wikisource",
        "source_work_url": "https://ru.wikisource.org/wiki/example",
        "permanent_source_url": "https://ru.wikisource.org/w/index.php?oldid=5585836",
        "bibliographic_source": "az.lib.ru single-page transcription; Wikisource publication year 1930",
        "legal_basis": "public_domain",
        "source_identity": _identity(wikitext),
        "capture_scope": {
            "revision_wikitext_identity_frozen": True,
            "literary_body_extraction_frozen": False,
            "composite_identity_frozen": False,
            "source_text_committed": False,
        },
    }


def _fetcher(wikitext):
    def fetcher(**_kwargs):
        return {**_identity(wikitext), "wikitext": wikitext}

    return fetcher


class RoadNowhereFreezeTests(unittest.TestCase):
    def test_extract_accepts_only_observed_direct_page_shape(self):
        body = extract_literary_body(_source("Первый абзац.\n\nВторой абзац."))
        self.assertIn("Первый абзац.", body)
        self.assertIn("Второй абзац.", body)
        self.assertIn("Заголовок 1", body)
        self.assertNotIn("Отексте", body)
        self.assertNotIn("Категория:", body)
        self.assertNotIn("===", body)
        self.assertNotIn("<!--", body)

    def test_extractor_fails_closed_on_shape_drift(self):
        source = _source()
        with self.assertRaisesRegex(ValueError, "heading inventory drift"):
            extract_literary_body(source.replace("=== Заголовок 27 ===", "== Заголовок 27 ==", 1))
        with self.assertRaisesRegex(ValueError, "category inventory drift"):
            extract_literary_body(source.replace("[[Категория:Тест 5]]", "", 1))
        with self.assertRaisesRegex(ValueError, "unsupported template"):
            extract_literary_body(source.replace("Абзац 1.", "{{неизвестно}}", 1))
        with self.assertRaisesRegex(ValueError, "HTML tag"):
            extract_literary_body(source.replace("Абзац 1.", "<span>Абзац 1.</span>", 1))
        with self.assertRaisesRegex(ValueError, "content after"):
            extract_literary_body(source + "unexpected suffix")

    def test_build_and_replay_are_source_free_and_non_parity(self):
        source = _source("а" * 300_001)
        revision_manifest = _revision_manifest(source)
        manifest = build_body_manifest(revision_manifest, fetcher=_fetcher(source))
        validate_body_manifest(manifest, revision_manifest=revision_manifest)
        self.assertEqual(manifest["extraction"]["profile"], EXTRACTION_PROFILE)
        self.assertGreaterEqual(manifest["literary_body_identity"]["character_count_including_spaces"], 300_000)
        self.assertEqual(manifest["fantlab_source_edition_match"], "unknown")
        self.assertTrue(manifest["diagnostic_comparison_admissible"])
        self.assertFalse(manifest["m2_parity_admissible"])
        self.assertNotIn("а" * 100, repr(manifest))

        receipt = replay_body_manifest(revision_manifest, manifest, fetcher=_fetcher(source))
        self.assertTrue(receipt["verified"])
        self.assertFalse(receipt["source_text_included"])
        self.assertEqual(receipt["extraction_profile"], EXTRACTION_PROFILE)
        self.assertFalse(receipt["m2_parity_admissible"])

    def test_revision_drift_preempts_extraction(self):
        source = _source("а" * 300_001)
        revision_manifest = _revision_manifest(source)

        def changed(**_kwargs):
            observed = _fetcher(source)()
            observed["wikitext_sha256"] = "f" * 64
            return observed

        with self.assertRaisesRegex(ValueError, "identity drift before extraction"):
            build_body_manifest(revision_manifest, fetcher=changed)


if __name__ == "__main__":
    unittest.main()
