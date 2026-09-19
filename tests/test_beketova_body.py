import hashlib
import unittest

from scriptorium.beketova_body import (
    CANDIDATE_ID,
    EXTRACTION_PROFILE,
    REVISION_ID,
    TITLE,
    build_body_manifest,
    extract_literary_body,
    replay_body_manifest,
    validate_body_manifest,
)


def _source() -> str:
    prefix = ["{{Отексте|meta}}"]
    prefix.extend(f"front-{index}" for index in range(2, 17))
    prefix.append("{{книга|meta}}")
    prefix.extend(f"front-{index}" for index in range(18, 33))
    prefix.append("<center>{{uc|title}}</center>")
    prefix.append("{{h|subtitle}}")
    prefix.append("<center>title</center>")
    prefix.append("<center>subtitle</center>")
    self_test = len(prefix)
    assert self_test == 36

    headings = ["=== PART ONE ===", "=== PART TWO ===", "=== PART THREE ==="]
    headings.extend(f"==== CHAPTER {index} ====" for index in range(1, 141))
    body_line_count = 10_984
    prose_count = body_line_count - len(headings)
    prose = ["а" * 40 for _ in range(prose_count)]
    prose[0] = "[[target|метка]] " + "а" * 30
    body = headings + prose
    assert len(body) == body_line_count

    categories = [f"[[Категория:Test {index}]]" for index in range(1, 9)]
    lines = prefix + body + categories
    assert len(lines) == 11_028
    return "\n".join(lines)


def _identity(source: str) -> dict[str, object]:
    raw = source.encode("utf-8")
    return {
        "title": TITLE,
        "page_id": 1012777,
        "revision_id": REVISION_ID,
        "revision_timestamp": "2025-02-25T02:24:10Z",
        "mediawiki_sha1": "1" * 40,
        "wikitext_character_count": len(source),
        "wikitext_utf8_byte_count": len(raw),
        "wikitext_sha256": hashlib.sha256(raw).hexdigest(),
    }


def _revision_manifest(source: str) -> dict[str, object]:
    return {
        "bibliographic_source": "Detgiz 1955 / az.lib.ru transcription family",
        "candidate_id": CANDIDATE_ID,
        "capture_scope": {
            "composite_identity_frozen": False,
            "literary_body_extraction_frozen": False,
            "revision_wikitext_identity_frozen": True,
            "source_text_committed": False,
        },
        "legal_basis": "public_domain_translation_source_statement",
        "manifest_version": "scriptorium-single-page-source-revision-v1",
        "permanent_source_url": "https://ru.wikisource.org/w/index.php?oldid=5304880",
        "provider": "Russian Wikisource",
        "source_identity": _identity(source),
        "source_work_url": "https://ru.wikisource.org/wiki/example",
    }


def _fetcher(source: str):
    def fetcher(**_kwargs):
        return {**_identity(source), "wikitext": source}

    return fetcher


class BeketovaBodyTests(unittest.TestCase):
    def test_extracts_observed_direct_transcription_shape(self):
        body = extract_literary_body(_source())
        self.assertGreater(len(body), 300_000)
        self.assertIn("PART ONE", body)
        self.assertIn("CHAPTER 140", body)
        self.assertIn("метка", body)
        self.assertNotIn("[[target", body)
        self.assertNotIn("Категория:Test", body)
        self.assertNotIn("front-", body)

    def test_extractor_fails_closed_on_scaffold_or_body_markup_drift(self):
        source = _source()
        with self.assertRaisesRegex(ValueError, "line inventory drift"):
            extract_literary_body(source + "\nextra")

        lines = source.splitlines()
        lines[100] = "{{unsupported|body}}"
        with self.assertRaisesRegex(ValueError, "template inventory drift"):
            extract_literary_body("\n".join(lines))

        lines = source.splitlines()
        lines[-1] = "not-a-category"
        with self.assertRaisesRegex(ValueError, "category boundary drift"):
            extract_literary_body("\n".join(lines))

    def test_build_and_replay_are_source_free_and_non_parity(self):
        source = _source()
        revision = _revision_manifest(source)
        manifest = build_body_manifest(revision, fetcher=_fetcher(source))
        validate_body_manifest(manifest, revision_manifest=revision)
        self.assertEqual(manifest["candidate_id"], CANDIDATE_ID)
        self.assertEqual(manifest["extraction"]["profile"], EXTRACTION_PROFILE)
        self.assertGreaterEqual(manifest["literary_body_identity"]["character_count_including_spaces"], 300_000)
        self.assertEqual(manifest["fantlab_source_edition_match"], "unknown")
        self.assertTrue(manifest["diagnostic_comparison_admissible"])
        self.assertFalse(manifest["m2_parity_admissible"])
        self.assertNotIn("а" * 100, repr(manifest))

        receipt = replay_body_manifest(revision, manifest, fetcher=_fetcher(source))
        self.assertTrue(receipt["verified"])
        self.assertFalse(receipt["source_text_included"])
        self.assertFalse(receipt["m2_parity_admissible"])

    def test_revision_identity_drift_preempts_extraction(self):
        source = _source()
        revision = _revision_manifest(source)

        def changed(**_kwargs):
            observed = _fetcher(source)()
            observed["wikitext_sha256"] = "f" * 64
            return observed

        with self.assertRaisesRegex(ValueError, "identity drift before extraction"):
            build_body_manifest(revision, fetcher=changed)


if __name__ == "__main__":
    unittest.main()
