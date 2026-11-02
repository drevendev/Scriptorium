"""Source-free positive/negative coverage for the pinned Trusov Page content."""
import copy
from hashlib import sha256
import json
from pathlib import Path
import unittest

from scriptorium.robinson_trusov_pages import verify_frozen_graph
from scriptorium.robinson_trusov_content import (
    capture, transclusion_input, validate_preflight,
)

BASE = Path(__file__).resolve().parents[1] / "corpus/candidates/source-edition-traces"
GRAPH = BASE / "defoe-robinson-crusoe-trusov-1775-ru.page-graph.json"
RECEIPT = BASE / "defoe-robinson-crusoe-trusov-1775-ru.page-graph-receipt.json"
PRIVATE_SOURCE = "PRIVATE TEST PROSE: исторический текст"


def fixture():
    graph = verify_frozen_graph(GRAPH, RECEIPT)
    return graph, sha256(GRAPH.read_bytes()).hexdigest()


def mock_query(graph, mutate=None):
    records = {row["revision_id"]: row for row in graph["pages"]}
    def query(params):
        ids = [int(r) for r in params["revids"].split("|")]
        assert params["rvprop"] == "ids|timestamp|sha1|content"
        assert params["rvslots"] == "main"
        response = []
        for rid in ids:
            record = records[rid]
            source = ('<noinclude><pagequality level="3"/>HEADER</noinclude>'
                      + PRIVATE_SOURCE + ' {{t}} [[link]]'
                      + '<includeonly> END</includeonly><noinclude>FOOT</noinclude>')
            row = {"pageid": record["page_id"], "title": record["title"],
                   "revisions": [{"revid": rid, "timestamp": record["timestamp_utc"],
                                  "sha1": record["mediawiki_sha1"], "slots": {
                                      "main": {"contentmodel": "wikitext", "content": source}}}]}
            if mutate:
                mutate(row)
            response.append(row)
        return {"query": {"pages": list(reversed(response))}}
    return query


class TrusovContentTests(unittest.TestCase):
    def test_all_pinned_pages_source_free_in_provider_independent_order(self):
        graph, digest = fixture()
        report = capture(graph, graph_sha256=digest, query=mock_query(graph))
        self.assertEqual(report["page_count"], 150)
        self.assertEqual(report["pages"][0]["page_sequence"], 2)
        self.assertEqual(report["pages"][-1]["page_sequence"], 151)
        self.assertEqual(report["pages_with_unresolved_templates"], 150)
        self.assertEqual(report["pages_with_unresolved_links"], 150)
        self.assertFalse(report["literary_coverage_verified"])
        self.assertFalse(report["corpus_threshold_verified"])
        self.assertIsNone(report["literary_body_sha256"])
        self.assertNotIn(PRIVATE_SOURCE, json.dumps(report, ensure_ascii=False))
        validate_preflight(report, graph)

    def test_strip_shell_without_pretending_to_render(self):
        self.assertEqual(transclusion_input("<noinclude>header</noinclude>foo"
                                            "<includeonly>bar</includeonly><noinclude>foot</noinclude>"),
                         "foobar")
        for text in ("<onlyinclude>body</onlyinclude>", "<noinclude>incomplete",
                     "</noinclude>after", "<noinclude/>body",
                     "<includeonly attr='x'>body</includeonly>",
                     "<noinclude></includeonly>"):
            with self.subTest(text=text), self.assertRaises(ValueError):
                transclusion_input(text)
        with self.assertRaisesRegex(ValueError, "empty"):
            transclusion_input("<noinclude>no transclusion</noinclude>")

    def test_proofread_page_content_model_is_supported(self):
        graph, digest = fixture()
        def proofread_model(page):
            page["revisions"][0]["slots"]["main"]["contentmodel"] = "proofread-page"
        report = capture(graph, graph_sha256=digest, query=mock_query(graph, proofread_model))
        self.assertEqual(report["page_count"], 150)

    def test_identity_drift_is_not_a_source_match(self):
        graph, digest = fixture()
        mutations = (
            lambda p: p["revisions"][0].__setitem__("sha1", "f"*40),
            lambda p: p["revisions"][0].__setitem__("revid", -1),
            lambda p: p.__setitem__("title", "Страница:wrong"),
            lambda p: p.__setitem__("pageid", -7),
        )
        for change in mutations:
            with self.subTest(change=change), self.assertRaises(ValueError):
                capture(graph, graph_sha256=digest, query=mock_query(graph, change))

    def test_incomplete_response_wrong_content_model_and_markup_fail(self):
        graph, digest = fixture()
        normal = mock_query(graph)
        def missing(params):
            answer = normal(params)
            answer["query"]["pages"].pop()
            return answer
        with self.assertRaisesRegex(ValueError, "incomplete"):
            capture(graph, graph_sha256=digest, query=missing)
        def bad_model(p):
            p["revisions"][0]["slots"]["main"]["contentmodel"] = "json"
        with self.assertRaisesRegex(ValueError, "content model"):
            capture(graph, graph_sha256=digest, query=mock_query(graph, bad_model))
        def broken(p):
            p["revisions"][0]["slots"]["main"]["content"] = "<noinclude>unclosed"
        with self.assertRaisesRegex(ValueError, "unclosed"):
            capture(graph, graph_sha256=digest, query=mock_query(graph, broken))

    def test_false_science_claim_prose_and_count_tampering_rejected(self):
        graph, digest = fixture()
        good = capture(graph, graph_sha256=digest, query=mock_query(graph))
        bad = copy.deepcopy(good)
        bad["pages"][0]["source_text"] = PRIVATE_SOURCE
        with self.assertRaisesRegex(ValueError, "prose leakage"):
            validate_preflight(bad, graph)
        bad = copy.deepcopy(good)
        bad["m2_parity_admissible"] = True
        with self.assertRaisesRegex(ValueError, "false scientific claim"):
            validate_preflight(bad, graph)
        bad = copy.deepcopy(good)
        bad["pages"][0]["transclusion_input_characters_including_spaces"] += 10
        with self.assertRaisesRegex(ValueError, "character count"):
            validate_preflight(bad, graph)

    def test_invalid_graph_digest_and_api_parameters(self):
        graph, digest = fixture()
        for bad in ("", None, "a"*40):
            with self.assertRaises(ValueError):
                capture(graph, graph_sha256=bad, query=mock_query(graph))
        with self.assertRaisesRegex(ValueError, "unbounded"):
            capture(graph, graph_sha256=digest, query=mock_query(graph), batch_size=500)


if __name__ == "__main__":
    unittest.main()
