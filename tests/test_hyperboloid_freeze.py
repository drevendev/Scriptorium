import unittest

from scriptorium.hyperboloid_freeze import (
    BODY_MANIFEST_VERSION,
    CANDIDATE_ID,
    EXTRACTION_PROFILE,
    REVISION_ID,
    TITLE,
    build_body_manifest,
    extract_literary_body,
    replay_body_manifest,
    validate_body_manifest,
)


SOURCE_IDENTITY = {
    "title": TITLE,
    "page_id": 1022517,
    "revision_id": REVISION_ID,
    "revision_timestamp": "2023-08-30T20:13:01Z",
    "mediawiki_sha1": "605afeabc38e4f5948371afdf976f586edbf1955",
    "wikitext_character_count": 502280,
    "wikitext_utf8_byte_count": 934455,
    "wikitext_sha256": "fa0b099bba2d0f0e6ce395a16de76317afcd8bec8b23b52e455f97a9726a4de9",
}


def _revision_manifest():
    return {
        "manifest_version": "scriptorium-single-page-source-revision-v1",
        "candidate_id": CANDIDATE_ID,
        "provider": "Russian Wikisource",
        "source_work_url": "https://ru.wikisource.org/wiki/example",
        "permanent_source_url": "https://ru.wikisource.org/w/index.php?oldid=5014458",
        "bibliographic_source": "az.lib.ru single-page transcription; exact print-edition identity unresolved",
        "legal_basis": "public_domain",
        "source_identity": dict(SOURCE_IDENTITY),
        "capture_scope": {
            "revision_wikitext_identity_frozen": True,
            "literary_body_extraction_frozen": False,
            "composite_identity_frozen": False,
            "source_text_committed": False,
        },
    }


def _source_shape(literary="Основной текст."):
    headings = "\n\n".join(f"=== {index} ===\nАбзац {index}." for index in range(1, 133))
    links = " ".join(
        (
            "[[цель-1|метка один]]",
            "[[цель-2|метка два]]",
            "[[цель-3]]",
            "[[цель-4|метка четыре]]",
        )
    )
    italics = " ".join(f"''слово{index}''" for index in range(22))
    breaks = " ".join("<br>" for _ in range(18))
    markers = " ".join(f"<sup><u>[{index % 9}]</u></sup>" for index in range(9))
    categories = "\n".join(f"[[Категория:Тест {index}]]" for index in range(1, 10))
    return (
        "{{Отексте\n|источник=тест\n}}\n"
        "<!-- редакционный комментарий 1 -->\n"
        f"{literary}\n\n{headings}\n\n{links}\n\n{italics}\n\n{breaks}\n\n{markers}\n"
        "<!-- редакционный комментарий 2 -->\n"
        f"{categories}\n"
    )


def _fetcher_for(wikitext):
    def fetcher(**_kwargs):
        return {**SOURCE_IDENTITY, "wikitext": wikitext}

    return fetcher


class HyperboloidFreezeTests(unittest.TestCase):
    def test_extract_literary_body_matches_observed_single_page_contract(self):
        body = extract_literary_body(_source_shape("Первый абзац.\n\nВторой абзац."))
        self.assertIn("Первый абзац.", body)
        self.assertIn("Второй абзац.", body)
        self.assertIn("метка один", body)
        self.assertIn("цель-3", body)
        self.assertIn("[1]", body)
        self.assertNotIn("Категория:", body)
        self.assertNotIn("Отексте", body)
        self.assertNotIn("<!--", body)
        self.assertNotIn("<sup>", body)
        self.assertNotIn("<u>", body)
        self.assertNotIn("[[", body)

    def test_extract_literary_body_fails_closed_on_source_shape_drift(self):
        source = _source_shape()
        with self.assertRaisesRegex(ValueError, "heading inventory drift"):
            extract_literary_body(source.replace("=== 132 ===", "== 132 ==", 1))
        with self.assertRaisesRegex(ValueError, "HTML tag inventory drift"):
            extract_literary_body(source.replace("<br>", "<span>", 1))
        with self.assertRaisesRegex(ValueError, "unsupported content after"):
            extract_literary_body(source + "unexpected suffix")
        with self.assertRaisesRegex(ValueError, "expected leading Отексте template"):
            extract_literary_body(source.replace("{{Отексте", "{{Другое", 1))

    def test_build_body_manifest_is_source_free_and_keeps_fantlab_unknown(self):
        literary = "а" * 300_001
        manifest = build_body_manifest(
            _revision_manifest(),
            fetcher=_fetcher_for(_source_shape(literary)),
        )
        self.assertEqual(manifest["manifest_version"], BODY_MANIFEST_VERSION)
        self.assertEqual(manifest["extraction"]["profile"], EXTRACTION_PROFILE)
        self.assertFalse(manifest["extraction"]["source_text_committed"])
        self.assertGreaterEqual(
            manifest["literary_body_identity"]["character_count_including_spaces"],
            len(literary),
        )
        self.assertEqual(manifest["fantlab_source_edition_match"], "unknown")
        self.assertTrue(manifest["diagnostic_comparison_admissible"])
        self.assertFalse(manifest["m2_parity_admissible"])
        self.assertNotIn(literary[:100], repr(manifest))
        validate_body_manifest(manifest)

    def test_build_rejects_revision_identity_drift_before_extraction(self):
        literary = "а" * 300_001

        def changed(**_kwargs):
            observed = _fetcher_for(_source_shape(literary))()
            observed["wikitext_sha256"] = "f" * 64
            return observed

        with self.assertRaisesRegex(ValueError, "identity drift before extraction"):
            build_body_manifest(_revision_manifest(), fetcher=changed)

    def test_replay_recomputes_the_same_body_identity(self):
        literary = "а" * 300_001
        fetcher = _fetcher_for(_source_shape(literary))
        body_manifest = build_body_manifest(_revision_manifest(), fetcher=fetcher)
        receipt = replay_body_manifest(
            _revision_manifest(),
            body_manifest,
            fetcher=fetcher,
        )
        self.assertTrue(receipt["verified"])
        self.assertFalse(receipt["source_text_included"])
        self.assertEqual(receipt["fantlab_source_edition_match"], "unknown")
        self.assertFalse(receipt["m2_parity_admissible"])
        self.assertNotIn("wikitext", receipt)

        changed_fetcher = _fetcher_for(_source_shape("б" * 300_001))
        with self.assertRaisesRegex(ValueError, "literary-body identity drift"):
            replay_body_manifest(
                _revision_manifest(),
                body_manifest,
                fetcher=changed_fetcher,
            )


if __name__ == "__main__":
    unittest.main()
