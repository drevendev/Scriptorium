import json
from hashlib import sha1, sha256
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

    def test_section_and_header_candidate(self):
        label = "private-section"
        row = k.observe(f'<pages index="{k.SCAN}" from=10 to=13 '
                        f'fromsection="{label}" tosection="end" header=1 '
                        'prev="private-link" />')
        selector = row["literal_page_selectors"][0]
        self.assertEqual(selector["status"], "LITERAL_CANDIDATE")
        self.assertEqual(selector["candidate_scan_pages"], [10, 11, 12, 13])
        self.assertEqual(selector["section_label_sha256"]["fromsection"],
                         sha256(label.encode()).hexdigest())
        self.assertNotIn(label, json.dumps(row))
        self.assertNotIn("private-link", json.dumps(row))
        self.assertEqual(row["unresolved_pages_tags"], 1)
        self.assertEqual(row["extraction_status"], "NOT_RUN_DEPENDENCIES")

    def test_selector_rejections_are_source_free(self):
        examples = (
            ('from=2 from=3 to=4', "DUPLICATE_ATTRIBUTE"),
            ('from=2 to=4 private-attribute="private-value"', "UNKNOWN_ATTRIBUTE"),
            ('from=2 to=4 include="7,9"', "INCLUDE_EXCLUDE_UNSUPPORTED"),
            ('from=2 to=4 exclude="3"', "INCLUDE_EXCLUDE_UNSUPPORTED"),
            ('from=2 to=4 onlysection="x" fromsection="y"', "MIXED_SECTION_SELECTORS"),
            ('from=2 to=4 step=0', "INVALID_RANGE_OR_STEP"),
            ('from=5 to=4', "INVALID_RANGE_OR_STEP"),
            ('from=2 to=4001', "INVALID_RANGE_OR_STEP"),
            ('from=2 to="private-value"', "NON_LITERAL_NUMERIC_RANGE"),
            ('from=2 to=4 fromsection="{{private-value}}"', "NON_LITERAL_SECTION_LABEL"),
        )
        for attrs, reason in examples:
            with self.subTest(reason=reason):
                row = k.observe(f'<pages index="{k.SCAN}" {attrs} />')
                selector = row["literal_page_selectors"][0]
                self.assertEqual(selector["status"], "UNRESOLVED")
                self.assertEqual(selector["reason"], reason)
                self.assertEqual(selector["candidate_scan_pages"], [])
                self.assertNotIn("private-value", json.dumps(row))
                self.assertNotIn("private-attribute", json.dumps(row))

    def test_literal_step_and_exact_label_digest(self):
        row = k.observe(f'<pages index="{k.SCAN}" from=2 to=7 step=2 '
                        'onlysection="A&amp;B" />')
        selector = row["literal_page_selectors"][0]
        self.assertEqual(selector["candidate_scan_pages"], [2, 4, 6])
        self.assertEqual(selector["section_label_sha256"],
                         {"onlysection": sha256(b"A&B").hexdigest()})
        self.assertEqual(k.observe('<pages index="wrong.pdf" from=2 to=7 />')
                         ["literal_page_selectors"][0]["reason"], "INDEX_MISMATCH")

    def test_compact_mediawiki_numeric_terminator(self):
        for first, last in ((5, 5), (11, 22)):
            with self.subTest(first=first, last=last):
                compact = k.observe(f'<pages index="{k.SCAN}" from={first} to={last}/>')
                spaced = k.observe(f'<pages index="{k.SCAN}" from={first} to={last} />')
                self.assertEqual(compact["literal_page_selectors"], spaced["literal_page_selectors"])
                self.assertEqual(compact["literal_pages_ranges"], spaced["literal_pages_ranges"])
                self.assertEqual(compact["literal_page_selectors"][0]["candidate_scan_pages"],
                                 list(range(first, last + 1)))
                self.assertEqual(compact["extraction_status"], "NOT_RUN_DEPENDENCIES")
        row = k.observe(f'<pages index="{k.SCAN}" from=2 to=7 step=2/>')
        self.assertEqual(row["literal_page_selectors"][0]["candidate_scan_pages"], [2, 4, 6])

    def test_compact_correction_does_not_strip_literal_slashes(self):
        for tail in ('to="5/" />', 'to=5&#47;>', 'to=5/ >', 'to=5//>',
                     'to=5/ header=1>', 'to=5&#47;/>'):
            with self.subTest(tail=tail):
                row = k.observe(f'<pages index="{k.SCAN}" from=2 {tail}')
                self.assertEqual(row["literal_page_selectors"][0]["status"], "UNRESOLVED")
        row = k.observe(f'<pages index="{k.SCAN}" from=2 to=5 fromsection="A/"/>')
        self.assertEqual(row["literal_page_selectors"][0]["section_label_sha256"],
                         {"fromsection": sha256(b"A/").hexdigest()})
        duplicate = k.observe(f'<pages index="{k.SCAN}" from=2 to=3 to=5/>')
        self.assertEqual(duplicate["literal_page_selectors"][0]["reason"], "DUPLICATE_ATTRIBUTE")

    def test_capture_reports_candidate_union_not_verified_graph(self):
        def selected(params):
            payload = provider(params)
            for page in payload["query"]["pages"]:
                rev = page["revisions"][0]
                n = list(k.REVISION_IDS).index(rev["revid"])
                source = (f'<pages index="{k.SCAN}" from={n+1} to={n+2} '
                          'fromsection="s" />')
                if n == 28:
                    source += '<!-- <pages hidden /> -->'
                rev["slots"]["main"]["content"] = source
                rev["sha1"] = sha1(source.encode()).hexdigest()
            return payload
        receipt = k.capture(selected)
        self.assertEqual(receipt["schema"], "scriptorium-kropotkin-body-preflight-v3")
        self.assertEqual(receipt["literal_selector_route_count"], 28)
        self.assertEqual(receipt["candidate_scan_page_union"], list(range(1, 30)))
        self.assertFalse(receipt["effective_page_graph_verified"])
        self.assertFalse(receipt["transclusion_dependencies_frozen"])
        self.assertIsNone(receipt["body_characters"])
        self.assertFalse(receipt["m2_parity_admissible"])
