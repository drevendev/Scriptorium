import json
from hashlib import sha1
import unittest

from scriptorium import kropotkin_orthography_controls as controls
from scriptorium.kropotkin_body_preflight import EXPECTED, SCAN, observe
from scriptorium.kropotkin_revisions import TITLE


class OrthographyControlTests(unittest.TestCase):
    def test_narrow_case_preserving_rules_and_nonrules(self):
        result, counts = controls.preview("МІРЪ, мѣхъ, Ѳома, подъём, ѵ, ъ, xміръ, міръ2.")
        self.assertEqual(result, "МИР, мех, Фома, подъём, ѵ, ъ, xміръ, міръ2.")
        self.assertEqual(counts, {"yat": 1, "decimal_i": 1, "fita": 1,
                                  "terminal_hard_sign": 2})
        self.assertEqual(controls.preview(result)[0], result)

    def test_control_equality_is_not_inferred_from_length(self):
        equal = controls.summarize("міръ", "мир")
        unequal = controls.summarize("міръ", "мор")
        gap = controls.summarize("міръ")
        self.assertTrue(equal["exact_candidate_equals_modern"])
        self.assertFalse(unequal["exact_candidate_equals_modern"])
        self.assertIsNone(gap["exact_candidate_equals_modern"])
        self.assertIsNone(gap["modern_characters"])
        self.assertNotIn("міръ", json.dumps(gap, ensure_ascii=False))

    def fixture(self):
        sources, by_id, bodies, selectors, rendered = {}, {}, {}, [], []
        for n in (12, 13, 14):
            modern = f"{TITLE}/Приложение/{n}"
            historical = modern + "/ДО"
            mid, hid = EXPECTED[modern], 3485499 if n == 13 else 1000 + n
            source = f'<pages index="{SCAN}" from="335" to="335" onlysection="X"/>'
            for title, revision in ((modern, mid), (historical, hid)):
                sources[title] = source
                by_id[revision] = title
            old_body = "м" * 675 + "ъ" if n == 13 else "міръ"
            new_body = "" if n == 13 else ("мир" if n == 12 else "мор")
            bodies[mid], bodies[hid] = new_body, old_body
            selectors.append({"title": modern,
                              "literal_page_selectors": observe(source)["literal_page_selectors"]})
            rendered.append({"title": modern, "revision_id": mid,
                             "status": "RENDERED_CANDIDATE" if new_body else "EMPTY_BODY",
                             "body_sha256": controls.digest(new_body) if new_body else None})
        gap = {"accepted_page_and_modern_route_replayed": True, "variants": [
            {"revision_id": 3485514, "rendered_status": "EMPTY_BODY",
             "lexical_section": {"raw_span_sha256": controls.GAP_SPAN}},
            {"revision_id": 3485499, "rendered_status": "RENDERED_CANDIDATE",
             "rendered_body_characters": 676,
             "source_sha256": controls.digest(sources[by_id[3485499]]),
             "rendered_body_sha256": controls.digest(bodies[3485499]),
             "lexical_section": {"raw_span_sha256": controls.GAP_SPAN}}]}

        def query(params):
            if params["action"] == "query":
                if "titles" in params:
                    title = params["titles"]
                    rid = next(i for i, t in by_id.items() if t == title)
                else:
                    rid = int(params["revids"])
                    title = by_id[rid]
                source = sources[title]
                return {"query": {"pages": [{"title": title, "ns": 0, "revisions": [
                    {"revid": rid, "timestamp": "2026-01-01T00:00:00Z",
                     "sha1": sha1(source.encode()).hexdigest(),
                     "slots": {"main": {"content": source}}}]}]}}
            rid = int(params["oldid"])
            return {"parse": {"title": by_id[rid], "revid": rid,
                              "text": f'<div class="prp-pages-output">{bodies[rid]}</div>',
                              "templates": [{"ns": 104, "title": f"Страница:{SCAN}/335"}]}}
        return {"routes": selectors}, gap, {"routes": rendered}, query

    def test_capture_keeps_candidate_out_of_composite(self):
        report = controls.capture(*self.fixture())
        self.assertEqual(report["exact_control_matches"], 1)
        self.assertEqual([r["appendix"] for r in report["rows"]], [12, 13, 14])
        self.assertEqual(report["rows"][1]["projection"]["candidate_characters"], 675)
        self.assertIsNone(report["rows"][1]["projection"]["exact_candidate_equals_modern"])
        self.assertFalse(report["composite_constructed"])
        self.assertFalse(report["corpus_normalization_accepted"])
        self.assertFalse(report["m2_parity_admissible"])
        self.assertIsNone(report["body_characters"])
        self.assertNotIn("міръ", json.dumps(report, ensure_ascii=False))

    def test_capture_rejects_gap_and_render_drift(self):
        selectors, gap, rendered, query = self.fixture()
        gap["variants"][1]["rendered_body_characters"] = 675
        with self.assertRaises(ValueError):
            controls.capture(selectors, gap, rendered, query)
        selectors, gap, rendered, query = self.fixture()
        rendered["routes"][0]["body_sha256"] = "0" * 64
        with self.assertRaises(ValueError):
            controls.capture(selectors, gap, rendered, query)

    def test_mismatched_literal_selector_is_not_normalized(self):
        selectors, gap, rendered, query = self.fixture()
        selectors["routes"][0]["literal_page_selectors"][0]["candidate_scan_pages"] = [334]
        report = controls.capture(selectors, gap, rendered, query)
        self.assertEqual(report["rows"][0]["status"], "SELECTOR_MISMATCH")
        self.assertIsNone(report["rows"][0]["projection"])
