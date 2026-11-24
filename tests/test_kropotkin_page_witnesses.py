import json
from hashlib import sha1, sha256
import unittest

from scriptorium import kropotkin_page_witnesses as k


def provider(params):
    assert "revids" not in params
    titles = params["titles"].split("|")
    assert 1 <= len(titles) <= 4
    pages = []
    for title in titles:
        scan = int(title.rsplit("/", 1)[1])
        source = '<section begin="private&amp;label" />Private prose.<section end="private&amp;label" />'
        pages.append({"title": title, "ns": 104, "revisions": [{
            "revid": 9000000 + scan, "timestamp": "2026-01-01T00:00:00Z",
            "sha1": sha1(source.encode()).hexdigest(),
            "slots": {"main": {"content": source}},
        }]})
    return {"query": {"pages": pages[::-1]}}


class KropotkinPageWitnessTests(unittest.TestCase):
    def test_partial_inventory_order_and_privacy(self):
        result = k.capture(provider)
        self.assertEqual(result["page_count"], 325)
        self.assertEqual([r["scan_page"] for r in result["pages"]], list(range(23, 348)))
        self.assertEqual(len({r["revision_id"] for r in result["pages"]}), 325)
        self.assertEqual(result, k.capture(provider))
        self.assertEqual(result["unresolved_route_count"], 2)
        for key in ("complete_page_inventory", "effective_page_graph_verified",
                    "transclusion_dependencies_frozen", "notes_boundary_verified",
                    "body_frozen", "source_text_retained", "m2_parity_admissible"):
            self.assertFalse(result[key])
        self.assertIsNone(result["body_characters"])
        self.assertNotIn("Private prose", json.dumps(result))
        self.assertNotIn("private", json.dumps(result))

    def test_marker_digests_and_lexical_limit(self):
        row = k.observe('<section begin="A&amp;B" /><section end="A&amp;B" />'
                        '<!-- <section begin="hidden" /> -->'
                        '<section begin="private" end="also-private" />'
                        '<nowiki>text</nowiki>')
        digest = sha256(b"A&B").hexdigest()
        self.assertEqual(row["literal_section_markers"], [
            {"kind": "begin", "label_sha256": digest},
            {"kind": "end", "label_sha256": digest},
        ])
        self.assertEqual(row["raw_section_openings"], 4)
        self.assertEqual(row["unresolved_section_tags"], 1)
        self.assertEqual(row["raw_nowiki_openings"], 1)
        self.assertNotIn("private", json.dumps(row))
        self.assertNotIn("hidden", json.dumps(row))

    def test_missing_and_unexpected_page_rejected(self):
        for change in ("missing", "wrong_title", "namespace", "redirect"):
            def changed(params):
                result = provider(params)
                pages = result["query"]["pages"]
                if change == "missing":
                    pages.pop()
                elif change == "wrong_title":
                    pages[0]["title"] += "wrong"
                elif change == "namespace":
                    pages[0]["ns"] = 0
                else:
                    pages[0]["redirect"] = True
                return result
            with self.subTest(change=change), self.assertRaises(ValueError):
                k.capture(changed)

    def test_digest_and_missing_source_rejected(self):
        for missing in (False, True):
            def changed(params):
                result = provider(params)
                slot = result["query"]["pages"][0]["revisions"][0]["slots"]["main"]
                if missing:
                    slot.pop("content")
                else:
                    slot["content"] += "drift"
                return result
            with self.subTest(missing=missing), self.assertRaises(ValueError):
                k.capture(changed)

    def test_duplicate_across_batches_rejected(self):
        def changed(params):
            result = provider(params)
            for page in result["query"]["pages"]:
                if page["title"].endswith("/27"):
                    page["revisions"][0]["revid"] = 9000023
            return result
        with self.assertRaisesRegex(ValueError, "duplicate Page revision"):
            k.capture(changed)

    def test_route_identity_collision_rejected(self):
        def changed(params):
            result = provider(params)
            result["query"]["pages"][0]["revisions"][0]["revid"] = k.REVISION_IDS[0]
            return result
        with self.assertRaisesRegex(ValueError, "duplicate Page revision"):
            k.capture(changed)
