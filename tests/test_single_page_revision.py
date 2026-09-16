import unittest

from scriptorium.single_page_revision import (
    MANIFEST_VERSION,
    build_manifest,
    fetch_pinned_revision,
    replay_manifest,
    validate_manifest,
)


TITLE = "Дорога в никуда (Грин)"
REVISION_ID = 5_585_836


def _payload(*, title=TITLE, revision_id=REVISION_ID, content="Тестовый текст"):
    return {
        "query": {
            "pages": [
                {
                    "pageid": 12345,
                    "title": title,
                    "revisions": [
                        {
                            "revid": revision_id,
                            "timestamp": "2025-07-30T20:33:47Z",
                            "sha1": "0123456789abcdef0123456789abcdef01234567",
                            "slots": {"main": {"content": content}},
                        }
                    ],
                }
            ]
        }
    }


class SinglePageRevisionTests(unittest.TestCase):
    def test_fetch_pinned_revision_returns_source_free_identity(self):
        observed = fetch_pinned_revision(
            title=TITLE,
            revision_id=REVISION_ID,
            query=lambda _params: _payload(),
        )
        self.assertEqual(observed["title"], TITLE)
        self.assertEqual(observed["revision_id"], REVISION_ID)
        self.assertEqual(observed["page_id"], 12345)
        self.assertEqual(observed["revision_timestamp"], "2025-07-30T20:33:47Z")
        self.assertEqual(observed["mediawiki_sha1"], "0123456789abcdef0123456789abcdef01234567")
        self.assertEqual(observed["wikitext_character_count"], len("Тестовый текст"))
        self.assertEqual(
            observed["wikitext_utf8_byte_count"], len("Тестовый текст".encode("utf-8"))
        )
        self.assertEqual(len(observed["wikitext_sha256"]), 64)
        self.assertNotIn("wikitext", observed)
        self.assertNotIn("content", observed)

    def test_fetch_fails_closed_on_title_or_revision_drift(self):
        with self.assertRaisesRegex(ValueError, "title drift"):
            fetch_pinned_revision(
                title=TITLE,
                revision_id=REVISION_ID,
                query=lambda _params: _payload(title="Другой заголовок"),
            )
        with self.assertRaisesRegex(ValueError, "revision id drift"):
            fetch_pinned_revision(
                title=TITLE,
                revision_id=REVISION_ID,
                query=lambda _params: _payload(revision_id=REVISION_ID + 1),
            )

    def test_build_manifest_marks_only_revision_identity_frozen(self):
        manifest = build_manifest(
            candidate_id="grin-road-nowhere-ru",
            title=TITLE,
            revision_id=REVISION_ID,
            source_work_url="https://ru.wikisource.org/wiki/example",
            permanent_source_url="https://ru.wikisource.org/w/index.php?oldid=5585836",
            bibliographic_source="az.lib.ru",
            legal_basis="public_domain",
            fetcher=lambda **_kwargs: fetch_pinned_revision(
                title=TITLE,
                revision_id=REVISION_ID,
                query=lambda _params: _payload(),
            ),
        )
        self.assertEqual(manifest["manifest_version"], MANIFEST_VERSION)
        self.assertEqual(
            manifest["capture_scope"],
            {
                "revision_wikitext_identity_frozen": True,
                "literary_body_extraction_frozen": False,
                "composite_identity_frozen": False,
                "source_text_committed": False,
            },
        )
        validate_manifest(manifest)

    def test_replay_detects_identity_drift_without_returning_prose(self):
        manifest = build_manifest(
            candidate_id="grin-road-nowhere-ru",
            title=TITLE,
            revision_id=REVISION_ID,
            source_work_url="https://ru.wikisource.org/wiki/example",
            permanent_source_url="https://ru.wikisource.org/w/index.php?oldid=5585836",
            bibliographic_source="az.lib.ru",
            legal_basis="public_domain",
            fetcher=lambda **_kwargs: fetch_pinned_revision(
                title=TITLE,
                revision_id=REVISION_ID,
                query=lambda _params: _payload(),
            ),
        )
        receipt = replay_manifest(
            manifest,
            fetcher=lambda **_kwargs: dict(manifest["source_identity"]),
        )
        self.assertTrue(receipt["verified"])
        self.assertFalse(receipt["source_text_committed"])
        self.assertNotIn("wikitext", receipt)

        def changed(**_kwargs):
            identity = dict(manifest["source_identity"])
            identity["wikitext_sha256"] = "f" * 64
            return identity

        with self.assertRaisesRegex(ValueError, "identity drift"):
            replay_manifest(manifest, fetcher=changed)


if __name__ == "__main__":
    unittest.main()
