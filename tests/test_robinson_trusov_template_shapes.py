"""Regression tests for one-request, source-free Trusov template-shape inventory."""
import copy
from hashlib import sha256
import json
import unittest

from test_robinson_trusov_content import fixture, mock_query, PRIVATE_SOURCE
from scriptorium.robinson_trusov_template_shapes import (
    capture_shapes, invocation_shapes, validate_shapes,
)


class TrusovTemplateShapesTests(unittest.TestCase):
    def test_balanced_nested_bindings_without_values_or_prose(self):
        text = "PRIVATE {{Set|value={{t|x=y}}|n= 4 }} text {{#if:1|SECRET|other}} {{{unknown}}}"
        calls, residual = invocation_shapes(text)
        self.assertEqual(len(calls), 3)
        self.assertEqual(residual, 1)  # triple-brace parameter is NOT a template
        self.assertEqual(calls[0]["template_title"], "Set")
        self.assertEqual(calls[0]["named_argument_count"], 2)
        self.assertEqual(calls[1]["template_title"], "t")
        self.assertEqual(calls[2]["template_title"], None)
        self.assertEqual(calls[2]["classification"], "parser_or_dynamic_template")
        self.assertNotIn("SECRET", json.dumps(calls))
        self.assertNotIn("PRIVATE", json.dumps(calls))

    def test_malformed_invocation_and_unsupported_titles(self):
        with self.assertRaisesRegex(ValueError, "unclosed"):
            invocation_shapes("Intro {{broken|value")
        calls, missing = invocation_shapes("{{a\nPRIVATE PROSE|hidden}}")
        self.assertEqual(len(calls), 1)
        self.assertIsNone(calls[0]["template_title"])
        self.assertEqual(missing, 0)
        self.assertNotIn("PRIVATE PROSE", str(calls))

    def test_all_historical_pages_reuse_verified_identities_and_do_not_persist_text(self):
        graph, digest = fixture()
        prior = {}
        report = capture_shapes(graph, digest, query=mock_query(graph),
                                delay=0, preflight_output=prior)
        self.assertEqual(report["page_count"], 150)
        self.assertEqual(report["total_invocations"], 150)
        self.assertEqual(report["unclassified_openers"], 0)
        self.assertEqual(report["pages_with_invocations"], 150)
        self.assertEqual(prior["page_count"], 150)
        self.assertEqual(report["transclusion_input_candidate_sha256"],
                         prior["transclusion_input_candidate_sha256"])
        self.assertNotIn(PRIVATE_SOURCE, json.dumps(report, ensure_ascii=False))
        validate_shapes(report, graph, prior)

    def test_invalid_identity_and_false_scientific_claim_rejected(self):
        graph, digest = fixture()
        def identity_drift(page):
            page["revisions"][0]["revid"] = -1
        with self.assertRaisesRegex(ValueError, "unexpected/duplicate"):
            capture_shapes(graph, digest, query=mock_query(graph, identity_drift))
        prior = {}
        report = capture_shapes(graph, digest, query=mock_query(graph),
                                preflight_output=prior)
        bad = copy.deepcopy(report)
        bad["literary_body_sha256"] = "a" * 64
        with self.assertRaisesRegex(ValueError, "false scientific claim"):
            validate_shapes(bad, graph, prior)
        bad = copy.deepcopy(report)
        bad["pages"][0]["invocations"][0]["template_title"] = "changed"
        with self.assertRaisesRegex(ValueError, "unsafe template title"):
            validate_shapes(bad, graph, prior)
        bad = copy.deepcopy(report)
        bad["pages"][0]["invocations"].append(bad["pages"][0]["invocations"][0])
        with self.assertRaisesRegex(ValueError, "counts differ"):
            validate_shapes(bad, graph, prior)
        bad = copy.deepcopy(report)
        bad["pages"][0]["raw_source_text"] = "secret"
        with self.assertRaisesRegex(ValueError, "unexpected Page shape"):
            validate_shapes(bad, graph, prior)


if __name__ == "__main__":
    unittest.main()
