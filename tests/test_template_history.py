from __future__ import annotations

from hashlib import sha256
import unittest

from scriptorium.template_history import (
    MANIFEST_VERSION,
    RESOLUTION_POLICY,
    build_manifest,
    replay_manifest,
    resolve_revision_at_or_before,
    validate_manifest,
)


TITLE = "Шаблон:Poemx1"
ANCHOR = "2024-11-26T11:16:35Z"
CONTENT = "<poem>{{{1|}}}</poem>"


def _payload(
    *,
    title: str = TITLE,
    revision_id: int = 77,
    timestamp: str = "2024-10-01T12:00:00Z",
    content: str = CONTENT,
) -> dict[str, object]:
    return {
        "query": {
            "pages": [
                {
                    "pageid": 42,
                    "title": title,
                    "revisions": [
                        {
                            "revid": revision_id,
                            "timestamp": timestamp,
                            "sha1": "a" * 40,
                            "slots": {"main": {"content": content}},
                        }
                    ],
                }
            ]
        }
    }


def _identity(
    *,
    revision_id: int = 77,
    timestamp: str = "2024-10-01T12:00:00Z",
    content: str = CONTENT,
) -> dict[str, object]:
    raw = content.encode("utf-8")
    return {
        "title": TITLE,
        "page_id": 42,
        "revision_id": revision_id,
        "revision_timestamp": timestamp,
        "mediawiki_sha1": "a" * 40,
        "wikitext_character_count": len(content),
        "wikitext_utf8_byte_count": len(raw),
        "wikitext_sha256": sha256(raw).hexdigest(),
    }


class HistoricalTemplateRevisionTests(unittest.TestCase):
    def test_resolver_selects_latest_revision_not_after_anchor(self) -> None:
        seen: dict[str, str] = {}

        def query(params: dict[str, str]) -> dict[str, object]:
            seen.update(params)
            return _payload()

        identity = resolve_revision_at_or_before(
            title=TITLE,
            anchor_timestamp=ANCHOR,
            query=query,
        )

        self.assertEqual(identity, _identity())
        self.assertEqual(seen["titles"], TITLE)
        self.assertEqual(seen["rvstart"], ANCHOR)
        self.assertEqual(seen["rvdir"], "older")
        self.assertEqual(seen["rvlimit"], "1")
        self.assertEqual(seen["rvprop"], "ids|timestamp|sha1|content")
        self.assertEqual(seen["rvslots"], "main")

    def test_resolver_rejects_revision_after_anchor_and_title_drift(self) -> None:
        with self.assertRaisesRegex(ValueError, "after the anchor"):
            resolve_revision_at_or_before(
                title=TITLE,
                anchor_timestamp=ANCHOR,
                query=lambda _params: _payload(timestamp="2024-12-01T00:00:00Z"),
            )
        with self.assertRaisesRegex(ValueError, "title drift"):
            resolve_revision_at_or_before(
                title=TITLE,
                anchor_timestamp=ANCHOR,
                query=lambda _params: _payload(title="Шаблон:Other"),
            )

    def test_manifest_is_source_free_and_keeps_render_equivalence_unproven(self) -> None:
        identity = _identity()
        manifest = build_manifest(
            candidate_id="gorky-klim-samgin-ru-poemx1-template",
            title=TITLE,
            anchor_timestamp=ANCHOR,
            anchor_revision_id=5198033,
            resolver=lambda **_kwargs: dict(identity),
        )
        validate_manifest(manifest)

        self.assertEqual(manifest["manifest_version"], MANIFEST_VERSION)
        policy = manifest["resolution_policy"]
        self.assertEqual(policy["kind"], RESOLUTION_POLICY)
        self.assertEqual(policy["anchor_revision_id"], 5198033)
        self.assertEqual(policy["anchor_timestamp"], ANCHOR)
        self.assertEqual(policy["evidence_class"], "inferred_reconstruction_anchor")
        self.assertIs(policy["historical_render_equivalence_proven"], False)
        self.assertEqual(manifest["source_identity"], identity)
        self.assertIs(manifest["capture_scope"]["template_expansion_reproduced"], False)
        self.assertIs(manifest["capture_scope"]["historical_render_equivalence_proven"], False)
        self.assertIs(manifest["capture_scope"]["source_text_committed"], False)
        forbidden = {"wikitext", "content", "body", "text", "source_text"}
        self.assertFalse(forbidden.intersection(manifest))
        self.assertFalse(forbidden.intersection(manifest["source_identity"]))

    def test_replay_rechecks_selection_and_exact_pinned_revision(self) -> None:
        identity = _identity()
        manifest = build_manifest(
            candidate_id="gorky-klim-samgin-ru-poemx1-template",
            title=TITLE,
            anchor_timestamp=ANCHOR,
            anchor_revision_id=5198033,
            resolver=lambda **_kwargs: dict(identity),
        )

        receipt = replay_manifest(
            manifest,
            resolver=lambda **_kwargs: dict(identity),
            pinned_fetcher=lambda **_kwargs: dict(identity),
        )
        self.assertIs(receipt["verified"], True)
        self.assertEqual(receipt["revision_id"], 77)
        self.assertEqual(receipt["wikitext_sha256"], identity["wikitext_sha256"])
        self.assertIs(receipt["historical_render_equivalence_proven"], False)
        self.assertIs(receipt["template_expansion_reproduced"], False)

        drifted = dict(identity)
        drifted["revision_id"] = 78
        with self.assertRaisesRegex(ValueError, "selection drift"):
            replay_manifest(
                manifest,
                resolver=lambda **_kwargs: dict(drifted),
                pinned_fetcher=lambda **_kwargs: dict(identity),
            )

        with self.assertRaisesRegex(ValueError, "pinned revision identity drift"):
            replay_manifest(
                manifest,
                resolver=lambda **_kwargs: dict(identity),
                pinned_fetcher=lambda **_kwargs: dict(drifted),
            )


if __name__ == "__main__":
    unittest.main()
