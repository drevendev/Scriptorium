import hashlib
import unittest

from scriptorium.single_page_body import (
    BODY_MANIFEST_VERSION,
    build_body_manifest,
    replay_body_manifest,
    validate_body_manifest,
)
from scriptorium.wikisource_freeze import EXTRACTION_PROFILE


TITLE = "Дорога в никуда (Грин)"
REVISION_ID = 5585836


def _source(literary: str) -> str:
    return (
        "<noinclude>{{Отексте|тест}}</noinclude>\n"
        '<div class="text">\n'
        "<!-- editorial -->\n"
        f"{literary}\n\n"
        "''Курсив'' и [[цель|метка]].\n"
        "</div>\n"
        "<noinclude>[[Категория:Тест]]</noinclude>\n"
    )


def _identity(wikitext: str) -> dict[str, object]:
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


def _revision_manifest(wikitext: str) -> dict[str, object]:
    return {
        "manifest_version": "scriptorium-single-page-source-revision-v1",
        "candidate_id": "grin-road-nowhere-ru",
        "provider": "Russian Wikisource",
        "source_work_url": "https://ru.wikisource.org/wiki/example",
        "permanent_source_url": "https://ru.wikisource.org/w/index.php?oldid=5585836",
        "bibliographic_source": "az.lib.ru single-page transcription",
        "legal_basis": "public_domain",
        "source_identity": _identity(wikitext),
        "capture_scope": {
            "revision_wikitext_identity_frozen": True,
            "literary_body_extraction_frozen": False,
            "composite_identity_frozen": False,
            "source_text_committed": False,
        },
    }


def _fetcher(wikitext: str):
    def fetcher(**_kwargs):
        return {**_identity(wikitext), "wikitext": wikitext}

    return fetcher


class SinglePageBodyTests(unittest.TestCase):
    def test_build_is_source_free_and_fantlab_unknown(self):
        literary = "а" * 300_001
        source = _source(literary)
        manifest = build_body_manifest(
            _revision_manifest(source),
            fetcher=_fetcher(source),
        )
        self.assertEqual(manifest["manifest_version"], BODY_MANIFEST_VERSION)
        self.assertEqual(manifest["extraction"]["profile"], EXTRACTION_PROFILE)
        self.assertFalse(manifest["extraction"]["source_text_committed"])
        self.assertGreaterEqual(
            manifest["literary_body_identity"]["character_count_including_spaces"],
            300_000,
        )
        self.assertEqual(manifest["fantlab_source_edition_match"], "unknown")
        self.assertTrue(manifest["diagnostic_comparison_admissible"])
        self.assertFalse(manifest["m2_parity_admissible"])
        self.assertNotIn(literary[:100], repr(manifest))
        validate_body_manifest(manifest, revision_manifest=_revision_manifest(source))

    def test_generic_extractor_fails_closed_on_unsupported_markup(self):
        literary = "а" * 300_001
        source = _source(literary).replace("''Курсив''", "{{unsupported|Курсив}}")
        with self.assertRaisesRegex(ValueError, "unsupported template"):
            build_body_manifest(
                _revision_manifest(source),
                fetcher=_fetcher(source),
            )

    def test_build_rejects_revision_identity_drift_before_extraction(self):
        source = _source("а" * 300_001)
        manifest = _revision_manifest(source)

        def changed(**_kwargs):
            observed = _fetcher(source)()
            observed["wikitext_sha256"] = "f" * 64
            return observed

        with self.assertRaisesRegex(ValueError, "identity drift before extraction"):
            build_body_manifest(manifest, fetcher=changed)

    def test_replay_recomputes_same_identity(self):
        source = _source("а" * 300_001)
        revision_manifest = _revision_manifest(source)
        fetcher = _fetcher(source)
        body_manifest = build_body_manifest(revision_manifest, fetcher=fetcher)
        receipt = replay_body_manifest(
            revision_manifest,
            body_manifest,
            fetcher=fetcher,
        )
        self.assertTrue(receipt["verified"])
        self.assertFalse(receipt["source_text_included"])
        self.assertEqual(receipt["revision_id"], REVISION_ID)
        self.assertFalse(receipt["m2_parity_admissible"])

        # A changed source must fail on the already-frozen revision identity before
        # extraction is even attempted; body-drift checks apply only after source
        # identity has been proven unchanged.
        changed = _source("б" * 300_001)
        with self.assertRaisesRegex(ValueError, "identity drift before extraction"):
            replay_body_manifest(
                revision_manifest,
                body_manifest,
                fetcher=_fetcher(changed),
            )

    def test_validate_rejects_body_source_mismatch(self):
        source = _source("а" * 300_001)
        revision_manifest = _revision_manifest(source)
        body_manifest = build_body_manifest(
            revision_manifest,
            fetcher=_fetcher(source),
        )
        changed = _revision_manifest(source)
        changed["source_identity"]["page_id"] = 42
        with self.assertRaisesRegex(ValueError, "page_id"):
            validate_body_manifest(body_manifest, revision_manifest=changed)


if __name__ == "__main__":
    unittest.main()
