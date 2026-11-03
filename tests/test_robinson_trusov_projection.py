"""Regression coverage for conservative Trusov non-literary projection."""
import copy
from hashlib import sha256
import json
import unittest

from test_robinson_trusov_content import fixture, mock_query, PRIVATE_SOURCE
from scriptorium.robinson_trusov_projection import (
    project_page, preview_var_orthographies, var_preview_refusal_reasons, capture_projection, validate_projection, ProjectedPageJoin,
)


class TrusovProjectionTests(unittest.TestCase):
    def test_var_orthography_previews_are_opt_in_and_distinct(self):
        source = "Начало {{ВАР|мѣсто|место}} продолжение\n"
        old, new, flat, multiline = preview_var_orthographies(source)
        self.assertEqual((old, new, flat, multiline), (
            "Начало мѣсто продолжение\n", "Начало место продолжение\n", 1, 0,
        ))
        self.assertEqual(project_page(source)[0], source)
        with self.assertRaises(TypeError):
            preview_var_orthographies(None)

    def test_var_preview_never_expands_nested_named_or_markup_calls(self):
        unsafe = ("{{other|{{ВАР|старое|новое}}}}\n"
                  "{{ВАР|old|new|third}}\n"
                  "{{ВАР|a=b|plain}}\n"
                  "{{ВАР|<b>old</b>|plain}}\n"
                  "{{ВАР||new}}\n"
                  "{{ВАР|old|[link]}}\n"
                  "{{ВАР|old|new}} and {{nop}}\n"
                  "{{#if:yes|{{ВАР|before|after}}|other}}\n"
                  "{{outer\n|{{ВАР|a|b}}\n}}\n"
                  "<!--\n{{ВАР|hidden|visible}}\n-->\n")
        old, new, flat, multiline = preview_var_orthographies(unsafe)
        self.assertEqual((old, new, flat, multiline), (unsafe, unsafe, 0, 0))

    def test_multiline_var_preview_keeps_anonymous_whitespace(self):
        source = "Before {{ВАР|дѣло\nдалѣе|дело\nдалее}} after\n"
        old, new, flat, multiline = preview_var_orthographies(source)
        self.assertEqual((old, new, flat, multiline), (
            "Before дѣло\nдалѣе after\n",
            "Before дело\nдалее after\n", 0, 1,
        ))
        self.assertEqual(sum(var_preview_refusal_reasons(source).values()), 0)
        self.assertEqual(project_page(source)[0], source)
        crlf = "A {{ВАР|old\r\nword|new\r\nword}} Z\r\n"
        self.assertEqual(preview_var_orthographies(crlf), (
            "A old\r\nword Z\r\n", "A new\r\nword Z\r\n", 0, 1,
        ))

    def test_var_preview_bounded_multiline_refusal(self):
        source = "{{ВАР|" + "\n".join(["text"] * 14) + "|modern}}\n"
        old, new, flat, multiline = preview_var_orthographies(source)
        self.assertEqual((old, new, flat, multiline), (source, source, 0, 0))
        self.assertEqual(var_preview_refusal_reasons(source)["multiline"], 1)
        with self.assertRaisesRegex(ValueError, "unclosed"):
            preview_var_orthographies("{{ВАР|old|new")

    def test_var_preview_refusal_categories_do_not_expose_source(self):
        source = ("{{ВАР|дѣло|дело}}\n"
                  "{{ВАР|old|\nmodern}}\n"
                  "{{ВАР|a=b|plain}}\n"
                  "{{other|{{ВАР|a|b}}}}\n"
                  "{{ ВАР|old|new}}\n"
                  "{{ВАР|" + "\n".join(["text"] * 14) + "|modern}}\n")
        old, new, flat, multiline = preview_var_orthographies(source)
        refusals = var_preview_refusal_reasons(source)
        self.assertEqual((flat, multiline), (1, 1))
        self.assertEqual(refusals, {
            "multiline": 1, "multiple_templates_on_line": 1,
            "non_plain_branch": 1, "unsupported_shape": 1,
        })
        self.assertEqual(sum(refusals.values()) + flat + multiline, 6)
        self.assertNotIn("дѣло", json.dumps(refusals, ensure_ascii=False))

    def test_joined_projection_digest_is_source_free_not_body(self):
        join = ProjectedPageJoin()
        with self.assertRaisesRegex(ValueError, "no projected Pages"):
            join.source_free_identity()
        join.add("А")
        join.add("Б\n")
        join.add("\nС")
        expected = "А\nБ\n\n\nС"
        identity = join.source_free_identity()
        self.assertEqual(identity["joined_projected_wikitext_sha256"],
                         sha256(expected.encode("utf-8")).hexdigest())
        self.assertEqual(identity["joined_projected_wikitext_characters_including_spaces"],
                         len(expected))
        self.assertEqual(identity["projected_page_join_seams"], 2)
        self.assertEqual(identity["alphabetic_page_edge_seams"], 1)
        self.assertEqual(identity["projected_page_join_profile"],
                         "one_LF_between_projected_Page_inputs_diagnostic_only")
        self.assertNotIn(expected, json.dumps(identity, ensure_ascii=False))
        with self.assertRaisesRegex(ValueError, "empty or non-text"):
            join.add("")
        with self.assertRaisesRegex(ValueError, "empty or non-text"):
            join.add(None)

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
                    "\n{{nop}}\n{{heading|4|Secret heading}}\n{{ВАР|ѣ|е}}\n" +
                    "{{ВАР|first\nline|second\nline}}\n" +
                    "<noinclude>footer</noinclude>"
                )
        preflight, shapes = {}, {}
        report = capture_projection(graph, digest, query=mock_query(graph, mutate_one),
                                    delay=0, preflight_output=preflight, shapes_output=shapes)
        self.assertEqual(report["page_count"], 150)
        self.assertEqual(report["projected_page_join_seams"], 149)
        self.assertEqual(report["projected_page_join_profile"], ProjectedPageJoin.PROFILE)
        self.assertEqual(report["joined_projected_wikitext_characters_including_spaces"],
                         sum(p["projected_wikitext_characters_including_spaces"] for p in report["pages"]) + 149)
        self.assertEqual(report["handled_nop"], 1)
        self.assertEqual(report["handled_heading"], 1)
        self.assertEqual(report["unresolved_invocations"], 151)
        self.assertEqual(shapes["total_invocations"], 153)
        self.assertEqual(report["flat_var_preview_count"], 1)
        self.assertEqual(report["multiline_var_preview_count"], 1)
        self.assertEqual(sum(report["var_preview_refusal_reasons"].values()), 0)
        self.assertNotEqual(report["joined_pre_reform_var_preview_sha256"],
                            report["joined_modern_var_preview_sha256"])
        self.assertFalse(report["corpus_threshold_verified"])
        self.assertIsNone(report["literary_body_sha256"])
        self.assertNotIn(PRIVATE_SOURCE, json.dumps(report, ensure_ascii=False))
        self.assertNotIn("Secret heading", json.dumps(report, ensure_ascii=False))
        validate_projection(report, graph, preflight, shapes)

        altered = copy.deepcopy(report)
        altered["pages"][0]["var_preview_refusal_reasons"]["multiline"] = 1
        with self.assertRaisesRegex(ValueError, "VAR preview refusal partition"):
            validate_projection(altered, graph, preflight, shapes)
        altered = copy.deepcopy(report)
        altered["flat_var_preview_count"] = 2
        with self.assertRaisesRegex(ValueError, "VAR preview aggregate"):
            validate_projection(altered, graph, preflight, shapes)
        altered = copy.deepcopy(report)
        altered["pages"][0]["flat_var_preview_count"] = 2
        with self.assertRaisesRegex(ValueError, "VAR preview refusal partition"):
            validate_projection(altered, graph, preflight, shapes)
        altered = copy.deepcopy(report)
        altered["pages"][0]["multiline_var_preview_count"] = 2
        with self.assertRaisesRegex(ValueError, "VAR preview refusal partition"):
            validate_projection(altered, graph, preflight, shapes)
        altered = copy.deepcopy(report)
        altered["var_preview_profile"] = "historical_render_verified"
        with self.assertRaisesRegex(ValueError, "VAR preview profile"):
            validate_projection(altered, graph, preflight, shapes)
        altered = copy.deepcopy(report)
        altered["pages"][0]["text"] = PRIVATE_SOURCE
        with self.assertRaisesRegex(ValueError, "leakage"):
            validate_projection(altered, graph, preflight, shapes)
        altered = copy.deepcopy(report)
        altered["m2_parity_admissible"] = True
        with self.assertRaisesRegex(ValueError, "false scientific claim"):
            validate_projection(altered, graph, preflight, shapes)
        altered = copy.deepcopy(report)
        altered["joined_projected_wikitext_characters_including_spaces"] += 1
        with self.assertRaisesRegex(ValueError, "Page join character count mismatch"):
            validate_projection(altered, graph, preflight, shapes)
        altered = copy.deepcopy(report)
        altered["alphabetic_page_edge_seams"] = 150
        with self.assertRaisesRegex(ValueError, "alphabetic Page edge"):
            validate_projection(altered, graph, preflight, shapes)
        altered = copy.deepcopy(report)
        altered["joined_projected_wikitext_sha256"] = PRIVATE_SOURCE
        with self.assertRaisesRegex(ValueError, "Page join identity"):
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
