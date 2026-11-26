import json
import unittest

from scriptorium.robinson_trusov_boundary_render import (
    capture, compare_control, digest, nonspace_edit_summary, observe, SELECTED,
)


class BoundaryRenderTests(unittest.TestCase):
    def test_unique_candidate_excludes_chrome_and_notes(self):
        result = observe('<div>header</div><div class="pagetext">'
                         '<p>Alpha &amp; beta</p><sup class="reference">1</sup>'
                         '<span hidden>secret</span><style>css</style><p>Gamma</p>'
                         '</div>')
        self.assertEqual(result["status"], "PAGE_VIEW_CANDIDATE")
        self.assertEqual(result["candidate_sha256"], digest("Alpha & beta Gamma"))
        self.assertEqual(result["candidate_characters"], 18)
        self.assertNotIn("Alpha", json.dumps(result))

    def test_unsafe_candidates_have_no_body_identity(self):
        for html, expected in [
            ("<div>text</div>", "BODY_CONTAINER_COUNT"),
            ('<div class="pagetext">A</div><div class="pagetext">B</div>',
             "BODY_CONTAINER_COUNT"),
            ('<div class="pagetext"><p>A</div>', "UNBALANCED_HTML"),
            ('<div class="pagetext"><span class="error">A</span></div>',
             "PARSER_ERROR_ELEMENT"),
            ('<div class="pagetext">  </div>', "EMPTY_CANDIDATE"),
            ('<div class="pagetext">{{VAR}}</div>', "UNEXPANDED_BRACES"),
        ]:
            with self.subTest(expected=expected):
                row = observe(html)
                self.assertEqual(row["status"], expected)
                self.assertIsNone(row["candidate_sha256"])
                self.assertIsNone(row["candidate_characters"])

    def setUp(self):
        self.graph = {"pages": [
            {"page_sequence": n, "revision_id": n + 1000, "page_id": n + 2000,
             "title": f"Page:{n}", "mediawiki_sha1": "a" * 40}
            for n in range(2, 152)
        ]}
        self.projection = {"source_page_graph_sha256": "b" * 64, "pages": [
            {"page_sequence": p["page_sequence"], "revision_id": p["revision_id"],
             "source_mediawiki_sha1": p["mediawiki_sha1"]} for p in self.graph["pages"]
        ]}
        self.calls = []

    def query(self, params):
        self.calls.append(params)
        n = int(params["oldid"]) - 1000
        return {"parse": {"revid": n + 1000, "title": f"Page:{n}",
                          "pageid": n + 2000, "text": '<div class="pagetext">private</div>',
                          "templates": [{"ns": 10, "title": "Template:secret"}]}}

    def run_capture(self, query=None):
        return capture(self.graph, self.projection, graph_sha256="b" * 64,
                       query=query or self.query)

    def test_exact_seven_requests_and_no_prose(self):
        result = self.run_capture()
        self.assertEqual([int(p["oldid"]) - 1000 for p in self.calls], list(SELECTED))
        self.assertEqual([p["page_sequence"] for p in result["pages"]], list(SELECTED))
        self.assertEqual(sum(p["role"] == "INTERIOR_CONTROL" for p in result["pages"]), 2)
        self.assertFalse(result["historical_dependencies_pinned"])
        self.assertFalse(result["corpus_admitted"])
        self.assertNotIn("private", json.dumps(result))
        self.assertNotIn("Template:secret", json.dumps(result))
        self.assertEqual(result["full_literary_body"], "NOT_VERIFIED")

    def test_whitespace_control_distinguishes_three_cases_and_refusal(self):
        projected = "Alpha\n beta"
        prior = {"projected_wikitext_sha256": digest(projected),
                 "projected_wikitext_characters_including_spaces": len(projected),
                 "unresolved_invocations": 0, "unclassified_openers": 0}
        for candidate, expected in [
            ("Alpha beta", "COLLAPSED_EQUAL"),
            ("Alphabeta", "NONSPACE_EQUAL_ONLY"),
            ("AlphA beta", "NONSPACE_DIFFERS"),
            (None, "RENDER_REFUSED"),
        ]:
            with self.subTest(expected=expected):
                row = compare_control(projected, prior, candidate)
                self.assertEqual(row["classification"], expected)
                self.assertNotIn("Alpha", json.dumps(row))
        for key, value in [("projected_wikitext_sha256", "0"*64),
                           ("projected_wikitext_characters_including_spaces", 1),
                           ("unresolved_invocations", 1), ("unclassified_openers", 1)]:
            with self.subTest(key=key), self.assertRaises(ValueError):
                compare_control(projected, {**prior, key: value}, "Alpha beta")

    def test_nonspace_edit_summary_is_aggregate_and_bounded(self):
        row = nonspace_edit_summary("Alpha''Beta''", "AlphaBeta")
        self.assertEqual(row["matching_characters"], 9)
        self.assertEqual(row["projected_changed_unicode_categories"]["P"], 4)
        self.assertEqual(row["projected_changed_ascii_apostrophes"], 4)
        self.assertEqual(row["rendered_changed_unicode_categories"]["L"], 0)
        self.assertNotIn("Alpha", json.dumps(row))
        lexical = nonspace_edit_summary("abc", "axc")
        self.assertEqual(lexical["edit_runs"]["replace"], 1)
        self.assertEqual(lexical["projected_changed_unicode_categories"]["L"], 1)
        self.assertEqual(lexical["rendered_changed_unicode_categories"]["L"], 1)
        self.assertEqual(nonspace_edit_summary("a"*8193, "a"), {"status": "SIZE_LIMIT"})
        same = nonspace_edit_summary("a b", "ab")
        self.assertEqual(sum(same["edit_runs"].values()), 0)

    def test_control_capture_keeps_source_free_v3_separate(self):
        for row in self.projection["pages"]:
            row.update(projected_wikitext_sha256=digest("private"),
                       projected_wikitext_characters_including_spaces=7,
                       unresolved_invocations=0, unclassified_openers=0)
        result = capture(self.graph, self.projection, graph_sha256="b"*64,
                         query=self.query, projected_controls={3: "private", 147: "private"})
        self.assertEqual(result["schema_version"], "scriptorium-trusov-boundary-render-v3")
        rows = [p for p in result["pages"] if "whitespace_control" in p]
        self.assertEqual([p["page_sequence"] for p in rows], [3, 147])
        self.assertTrue(all(p["whitespace_control"]["classification"] ==
                            "COLLAPSED_EQUAL" for p in rows))
        self.assertNotIn("private", json.dumps(result))
        self.assertTrue(all(p["skipped_body_nonspace_characters"] == 0 for p in rows))
        self.assertTrue(all(p["whitespace_control"]["nonspace_edit_summary"]["matching_characters"] == 7 for p in rows))
        self.assertFalse(result["historical_dependencies_pinned"])
        with self.assertRaises(ValueError):
            capture(self.graph, self.projection, graph_sha256="b"*64,
                    query=self.query, projected_controls={3: "private"})

    def test_skipped_scope_is_counted_only_in_control_receipt(self):
        for row in self.projection["pages"]:
            row.update(projected_wikitext_sha256=digest("private"),
                       projected_wikitext_characters_including_spaces=7,
                       unresolved_invocations=0, unclassified_openers=0)
        def query(params):
            result = self.query(params)
            result["parse"]["text"] = '<div class="pagetext">private<span hidden>secret note</span></div>'
            return result
        result = capture(self.graph, self.projection, graph_sha256="b"*64,
                         query=query, projected_controls={3: "private", 147: "private"})
        for row in result["pages"]:
            if row["page_sequence"] in (3, 147):
                self.assertEqual(row["skipped_body_nonspace_characters"], 10)
            else:
                self.assertNotIn("skipped_body_nonspace_characters", row)
        self.assertNotIn("secret note", json.dumps(result))

    def test_projection_drift_fails_before_request(self):
        self.projection["pages"][-1]["revision_id"] += 1
        with self.assertRaisesRegex(ValueError, "projection Page identity drift"):
            self.run_capture()
        self.assertEqual(self.calls, [])

    def test_render_identity_and_dependency_drift(self):
        for key, value in [("revid", 1), ("pageid", 1), ("title", "other"),
                           ("templates", [{"ns": True, "title": "bad"}])]:
            with self.subTest(key=key):
                def bad(params):
                    response = self.query(params)
                    response["parse"][key] = value
                    return response
                with self.assertRaises(ValueError):
                    self.run_capture(bad)


if __name__ == "__main__":
    unittest.main()
