import json
from hashlib import sha1
import unittest
from scriptorium import kropotkin_body_preflight as k


def provider(params):
    assert "titles" not in params
    ids = list(map(int, params["revids"].split("|")))
    assert len(ids) <= 4
    pages = []
    for title, rid in k.EXPECTED.items():
        if rid in ids:
            source = '<div class="text">Synthetic words only.</div>'
            pages.append({"title": title, "revisions": [{
                "revid": rid, "timestamp": "2026-01-01T00:00:00Z",
                "sha1": sha1(source.encode()).hexdigest(),
                "slots": {"main": {"content": source}},
            }]})
    return {"query": {"pages": pages[::-1]}}


class KropotkinBodyPreflightTests(unittest.TestCase):
    def test_pinned_order_and_no_source(self):
        result = k.capture(provider)
        self.assertEqual(len(result["routes"]), 29)
        self.assertEqual([r["revision_id"] for r in result["routes"]], list(k.REVISION_IDS))
        self.assertEqual(result["candidate_route_count"], 29)
        self.assertNotIn("Synthetic words only", json.dumps(result))
        self.assertNotIn(3485489, k.REVISION_IDS)
        self.assertIsNone(result["body_characters"])
        self.assertFalse(result["body_frozen"])
        self.assertFalse(result["m2_parity_admissible"])
        self.assertEqual(result, k.capture(provider))

    def test_literal_range_is_not_body(self):
        row = k.observe(f'<div class="text"><pages index="{k.SCAN}" from=5 to="12" /></div>')
        self.assertEqual(row["literal_pages_ranges"], [{"first_page": 5, "last_page": 12}])
        self.assertEqual(row["extraction_status"], "NOT_RUN_DEPENDENCIES")
        self.assertIsNone(row["candidate_body_characters"])

    def test_section_or_wrong_index_unresolved(self):
        for tag in (f'<pages index="{k.SCAN}" from=2 to=3 fromsection="secret" />',
                    '<pages index="different.pdf" from=2 to=3 />',
                    f'<pages index="{k.SCAN}" from=3 to=2 />',
                    f'<pages index="{k.SCAN}" from=2 from=3 to=4 />'):
            with self.subTest(tag=tag):
                row = k.observe(tag)
                self.assertEqual(row["literal_pages_ranges"], [])
                self.assertEqual(row["unresolved_pages_tags"], 1)
                self.assertIsNone(row["candidate_body_characters"])
                self.assertNotIn("secret", json.dumps(row))

    def test_notes_not_claimed_as_verified(self):
        row = k.observe('<div class="text">Synthetic.<ref>Note.</ref></div>')
        self.assertEqual(row["raw_ref_openings"], 1)
        self.assertEqual(row["extraction_status"], "CANDIDATE_ONLY")
        self.assertFalse(k.capture(provider)["notes_boundary_verified"])

    def test_missing_revision_rejected(self):
        def changed(params):
            result = provider(params)
            result["query"]["pages"].pop()
            return result
        with self.assertRaises(ValueError):
            k.capture(changed)

    def test_source_digest_mismatch_rejected(self):
        def changed(params):
            result = provider(params)
            result["query"]["pages"][0]["revisions"][0]["slots"]["main"]["content"] += "drift"
            return result
        with self.assertRaisesRegex(ValueError, "digest mismatch"):
            k.capture(changed)

    def test_unknown_markup_not_counted(self):
        row = k.observe('<div class="text">{{unknown|private}}</div>')
        self.assertEqual(row["extraction_status"], "UNSUPPORTED_TEMPLATE")
        self.assertIsNone(row["candidate_body_characters"])
        self.assertNotIn("private", json.dumps(row))
