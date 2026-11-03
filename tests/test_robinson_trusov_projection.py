"""Regression coverage for conservative Trusov non-literary projection."""
import copy
import json
import unittest

from test_robinson_trusov_content import fixture, mock_query, PRIVATE_SOURCE
from scriptorium.robinson_trusov_projection import (
    project_page, capture_projection, validate_projection,
)


class TrusovProjectionTests(unittest.TestCase):
    def test_plain_standalone_templates_only_and_no_prose_output(self):
        source = "PRIVATE TEXT\n{{nop}}\n{{heading|4|ГЛАВА I}}\nAFTER\n"
        projected, nop, heading, unresolved, residual = project_page(source)
        self.assertEqual(projected, "PRIVATE TEXT\n\nГЛАВА I\nAFTER\n")
        self.assertEqual((nop, heading, unresolved, residual), (1, 1, 0, 0))

    def test_unsupported_templates_are_kept_not_misrendered(self):
        source = ("inline {{nop}} line\n{{nop|unexpected}}\n"
                  "{{heading|5|{{inner}}}}\n{{heading|5|Title|id=x}}\n"
                  "{{ВАР|дорѣформенный|современный}}\n"
                  "{{#if:yes|TRUE|FALSE}}\n{{{1}}}\n")
        projected, nop, heading, unresolved, residual = project_page(source)
        self.assertEqual(projected, source)
        self.assertEqual((nop, heading), (0, 0))
        self.assertGreaterEqual(unresolved, 6)
        self.assertGreaterEqual(residual, 1)

    def test_exact_150_page_mock_capture_keeps_all_prior_invariants(self):
        graph, digest = fixture()
        def mutate_one(page):
            if page["title"] == graph["pages"][0]["title"]:
                page["revisions"][0]["slots"]["main"]["content"] = (
                    "<noinclude>header</noinclude>" + PRIVATE_SOURCE +
                    "\n{{nop}}\n{{heading|4|Secret heading}}\n" +
                    "<noinclude>footer</noinclude>"
                )
        preflight, shapes = {}, {}
        report = capture_projection(graph, digest, query=mock_query(graph, mutate_one),
                                    delay=0, preflight_output=preflight, shapes_output=shapes)
        self.assertEqual(report["page_count"], 150)
        self.assertEqual(report["handled_nop"], 1)
        self.assertEqual(report["handled_heading"], 1)
        self.assertEqual(report["unresolved_invocations"], 149)
        self.assertEqual(shapes["total_invocations"], 151)
        self.assertFalse(report["corpus_threshold_verified"])
        self.assertIsNone(report["literary_body_sha256"])
        self.assertNotIn(PRIVATE_SOURCE, json.dumps(report, ensure_ascii=False))
        self.assertNotIn("Secret heading", json.dumps(report, ensure_ascii=False))
        validate_projection(report, graph, preflight, shapes)

        altered = copy.deepcopy(report)
        altered["pages"][0]["text"] = PRIVATE_SOURCE
        with self.assertRaisesRegex(ValueError, "leakage"):
            validate_projection(altered, graph, preflight, shapes)
        altered = copy.deepcopy(report)
        altered["m2_parity_admissible"] = True
        with self.assertRaisesRegex(ValueError, "false scientific claim"):
            validate_projection(altered, graph, preflight, shapes)
        altered = copy.deepcopy(report)
        altered["handled_nop"] += 1
        with self.assertRaisesRegex(ValueError, "total mismatch"):
            validate_projection(altered, graph, preflight, shapes)
        altered = copy.deepcopy(report)
        altered["pages"][1]["revision_id"] += 1
        with self.assertRaisesRegex(ValueError, "order drift"):
            validate_projection(altered, graph, preflight, shapes)


if __name__ == "__main__":
    unittest.main()
