import json
import unittest

from scriptorium.robinson_trusov_boundary_render import (
    capture, digest, observe, SELECTED,
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
