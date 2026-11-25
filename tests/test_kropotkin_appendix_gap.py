import json
import unittest
from hashlib import sha1

from scriptorium import kropotkin_appendix_gap as gap


class AppendixGapTests(unittest.TestCase):
    def test_exact_lexical_span_preserves_empty_and_nonempty(self):
        source = ('<section begin="old"/>Исторический текст<section end="old"/>\n'
                  '<section begin="new"/>\n  <section end="new"/>')
        def selector(label):
            return {"candidate_scan_pages": [335],
                    "section_label_sha256": {"onlysection": gap.digest(label)}}
        old = gap.section_probe(source, selector("old"))
        new = gap.section_probe(source, selector("new"))
        self.assertEqual(old["raw_span_sha256"], gap.digest("Исторический текст"))
        self.assertGreater(old["raw_non_whitespace_characters"], 0)
        self.assertEqual(new["raw_span_characters"], 3)
        self.assertEqual(new["raw_non_whitespace_characters"], 0)

    def test_ambiguous_missing_and_nonlocal_markers(self):
        plan = {"candidate_scan_pages": [335],
                "section_label_sha256": {"onlysection": gap.digest("new")}}
        for source in ('<section begin="new"/>x',
                       '<section end="new"/>x<section begin="new"/>',
                       '<section begin="new"/>x<section begin="new"/>y<section end="new"/>',
                       '<!-- <section begin="new"/>x<section end="new"/> -->'):
            self.assertEqual(gap.section_probe(source, plan)["status"],
                             "AMBIGUOUS_LEXICAL_MARKERS")
        self.assertEqual(gap.section_probe("", dict(plan, candidate_scan_pages=[334, 335]))["status"],
                         "NOT_SINGLE_SECTION")

    def fixture(self):
        def route(label):
            return f'<pages index="{gap.SCAN}" from="335" to="335" onlysection="{label}"/>'
        sources = {gap.MODERN: route("new"), gap.HISTORICAL: route("old"),
                   gap.PAGE: '<section begin="old"/>Private historical prose<section end="old"/>'
                             '<section begin="new"/><section end="new"/>'}
        selectors = {"routes": [{"title": gap.MODERN, "revision_id": gap.PINS[gap.MODERN],
                                 "wikitext_sha256": gap.digest(sources[gap.MODERN])}]}
        witnesses = {"pages": [{"scan_page": 335, "revision_id": gap.PINS[gap.PAGE],
                                "wikitext_sha256": gap.digest(sources[gap.PAGE])}]}
        def query(params):
            if params["action"] == "query":
                self.assertEqual(params["revids"], "3485514|3485499|5800299")
                return {"query": {"pages": [
                    {"title": title, "ns": 104 if title == gap.PAGE else 0,
                     "revisions": [{"revid": gap.PINS[title], "timestamp": "2026-01-01T00:00:00Z",
                                    "sha1": sha1(source.encode()).hexdigest(),
                                    "slots": {"main": {"content": source}}}]}
                    for title, source in reversed(list(sources.items()))]}}
            rid = int(params["oldid"])
            title = next(t for t, r in gap.PINS.items() if r == rid)
            body = "" if title == gap.MODERN else "Private historical prose"
            return {"parse": {"revid": rid, "title": title,
                              "text": f'<div class="prp-pages-output">{body}</div>',
                              "templates": [{"ns": 104, "title": gap.PAGE}]}}
        return selectors, witnesses, query

    def test_capture_keeps_variants_separate_and_no_prose(self):
        report = gap.capture(*self.fixture())
        modern, historical = report["variants"]
        self.assertEqual(modern["rendered_status"], "EMPTY_BODY")
        self.assertEqual(historical["rendered_status"], "RENDERED_CANDIDATE")
        self.assertEqual(modern["lexical_section"]["raw_non_whitespace_characters"], 0)
        self.assertGreater(historical["lexical_section"]["raw_non_whitespace_characters"], 0)
        self.assertNotIn("Private historical prose", json.dumps(report))
        self.assertFalse(report["normalization_performed"])
        self.assertFalse(report["body_frozen"])
        self.assertIsNone(report["body_characters"])
        self.assertFalse(report["m2_parity_admissible"])

    def test_rejects_accepted_digest_and_rendered_identity_drift(self):
        selectors, witnesses, query = self.fixture()
        witnesses["pages"][0]["wikitext_sha256"] = "0" * 64
        with self.assertRaises(ValueError):
            gap.capture(selectors, witnesses, query)
        selectors, witnesses, query = self.fixture()
        def drift(params):
            result = query(params)
            if params["action"] == "parse":
                result["parse"]["revid"] += 1
            return result
        with self.assertRaises(ValueError):
            gap.capture(selectors, witnesses, drift)
