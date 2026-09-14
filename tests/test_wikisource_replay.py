import copy
from hashlib import sha256
import json
from pathlib import Path
import unittest

from scriptorium.source_revision_manifest import decode_chapter_identities
from scriptorium.text import NORMALIZATION_PROFILE, normalize_text
from scriptorium.wikisource_replay import (
    fetch_pinned_chapter_revisions,
    replay_packed_manifest,
)


REPO_ROOT = Path(__file__).resolve().parents[1]
REVISION_MANIFEST = (
    REPO_ROOT
    / "corpus"
    / "candidates"
    / "source-edition-traces"
    / "tolstoy-anna-karenina-ru.revisions.json"
)


class WikisourceReplayTests(unittest.TestCase):
    def test_fetch_pinned_revisions_requires_exact_identity(self):
        identities = (
            {
                "title": "A",
                "revision_id": 11,
                "revision_timestamp": "2024-01-01T00:00:00Z",
                "mediawiki_sha1": "a" * 40,
            },
            {
                "title": "B",
                "revision_id": 12,
                "revision_timestamp": "2024-01-01T00:00:01Z",
                "mediawiki_sha1": "b" * 40,
            },
        )
        calls = []

        def query(params):
            calls.append(params)
            return {
                "query": {
                    "pages": [
                        {
                            "title": "B",
                            "revisions": [
                                {
                                    "revid": 12,
                                    "timestamp": "2024-01-01T00:00:01Z",
                                    "sha1": "b" * 40,
                                    "slots": {"main": {"content": "<div class=\"text\">B.</div>"}},
                                }
                            ],
                        },
                        {
                            "title": "A",
                            "revisions": [
                                {
                                    "revid": 11,
                                    "timestamp": "2024-01-01T00:00:00Z",
                                    "sha1": "a" * 40,
                                    "slots": {"main": {"content": "<div class=\"text\">A.</div>"}},
                                }
                            ],
                        },
                    ]
                }
            }

        records = fetch_pinned_chapter_revisions(identities, query=query)
        self.assertEqual(set(records), {"A", "B"})
        self.assertEqual(calls[0]["revids"], "11|12")
        self.assertEqual(calls[0]["rvprop"], "ids|timestamp|sha1|content")

        def bad_query(params):
            payload = query(params)
            payload["query"]["pages"][0]["revisions"][0]["sha1"] = "c" * 40
            return payload

        with self.assertRaisesRegex(ValueError, "SHA-1 drift"):
            fetch_pinned_chapter_revisions(identities, query=bad_query)

    def test_replay_preserves_manifest_order_and_verifies_composite_identity(self):
        manifest = json.loads(REVISION_MANIFEST.read_text(encoding="utf-8"))
        identities = decode_chapter_identities(manifest)
        synthetic = {
            row["title"]: f'<div class="text">Глава {row["ordinal"]}.</div>'
            for row in identities
        }
        expected = "\n\n".join(f"Глава {row['ordinal']}." for row in identities)
        raw = expected.encode("utf-8")
        normalized = normalize_text(expected)
        adjusted = copy.deepcopy(manifest)
        adjusted["composite_identity"] = {
            "chapter_count": 239,
            "character_count_including_spaces": len(expected),
            "utf8_byte_count": len(raw),
            "raw_sha256": sha256(raw).hexdigest(),
            "normalization_profile": NORMALIZATION_PROFILE,
            "normalized_character_count_including_spaces": len(normalized),
            "normalized_sha256": sha256(normalized.encode("utf-8")).hexdigest(),
        }

        actual = replay_packed_manifest(adjusted, fetcher=lambda rows: synthetic)
        self.assertEqual(actual, expected)

        bad_hash = copy.deepcopy(adjusted)
        bad_hash["composite_identity"]["raw_sha256"] = "0" * 64
        with self.assertRaisesRegex(ValueError, "raw_sha256"):
            replay_packed_manifest(bad_hash, fetcher=lambda rows: synthetic)

        bad_profile = copy.deepcopy(adjusted)
        bad_profile["composite_identity"]["normalization_profile"] = "future-profile-v999"
        with self.assertRaisesRegex(ValueError, "normalization_profile"):
            replay_packed_manifest(bad_profile, fetcher=lambda rows: synthetic)


if __name__ == "__main__":
    unittest.main()
