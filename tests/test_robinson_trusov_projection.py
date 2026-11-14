"""Regression coverage for conservative Trusov non-literary projection."""
import copy
from hashlib import sha256
import json
import unittest

from test_robinson_trusov_content import fixture, mock_query, PRIVATE_SOURCE
from scriptorium.robinson_trusov_projection import (
    project_page, preview_var_orthographies, var_preview_refusal_reasons, var_preview_call_partition, capture_projection, validate_projection, ProjectedPageJoin,
)


class TrusovProjectionTests(unittest.TestCase):
    def test_literal_nowiki_pre_regions_never_project_or_preview_templates(self):
        # MediaWiki XML-style nowiki/pre strip blocks render brace markup
        # literally. A stand-alone-looking call inside one is not active.
        for name in ("nowiki", "pre"):
            with self.subTest(tag=name):
                source = (f"<{name}>\\n{{{{nop}}}}\\n"
                          "{{heading|h|Hidden}}\\n"
                          "{{ВАР|old|new}}\\n"
                          f"</{name}>\\n{{{{nop}}}}\\n"
                          "{{ВАР|мѣсто|место}}\\n")
                projected = project_page(source)[0]
                self.assertEqual(
                    projected, source.replace(f"</{name}>\\n{{{{nop}}}}",
                                              f"</{name}>\\n"),
                )
                self.assertIn("{{nop}}\\n{{heading|h|Hidden}}", projected)
                old, modern, flat, multiline = preview_var_orthographies(source)
                self.assertEqual((flat, multiline), (1, 0))
                self.assertIn("{{ВАР|old|new}}", old)
                self.assertIn("{{ВАР|old|new}}", modern)
                self.assertIn("мѣсто\\n", old)
                self.assertIn("место\\n", modern)
                self.assertEqual(
                    var_preview_refusal_reasons(source)["multiple_templates_on_line"], 1,
                )

    def test_protected_tag_comment_self_closing_and_unclosed_boundaries(self):
        # Literal examples inside comments must not poison later live calls.
        commented = "<!-- <nowiki> -->\\n{{nop}}\\n"
        self.assertEqual(project_page(commented)[0], "<!-- <nowiki> -->\\n\\n")
        self.assertEqual(project_page("<nowiki />\\n{{nop}}\\n")[0],
                         "<nowiki />\\n\\n")
        # An open literal region or a stray close tag is ambiguous: retain it.
        for prefix in ("<nowiki>", "<pre class='listing'>", "</pre>"):
            with self.subTest(prefix=prefix):
                source = prefix + "\\n{{nop}}\\n{{ВАР|old|new}}\\n"
                self.assertEqual(project_page(source)[0], source)
                self.assertEqual(preview_var_orthographies(source),
                                 (source, source, 0, 0))

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
        self.assertEqual(var_preview_refusal_reasons(source)["too_many_line_breaks"], 1)
        unclosed = "{{ВАР|old|new"
        self.assertEqual(preview_var_orthographies(unclosed), (unclosed, unclosed, 0, 0))
        self.assertEqual(var_preview_refusal_reasons(unclosed)["unbalanced_braces"], 1)

    def test_var_preview_counts_logical_newlines_including_bare_cr(self):
        # Historical Page source may preserve any newline convention; the
        # twelve-break bound must not be bypassed with carriage returns.
        for ending in ("\n", "\r\n", "\r"):
            with self.subTest(ending=repr(ending)):
                admissible = "{{ВАР|" + ending.join(["old"] * 13) + "|new}}"
                old, new, flat, multiline = preview_var_orthographies(admissible)
                self.assertEqual((old, new, flat, multiline),
                                 (ending.join(["old"] * 13), "new", 0, 1))
                self.assertEqual(sum(var_preview_refusal_reasons(admissible).values()), 0)

                rejected = "{{ВАР|" + ending.join(["old"] * 14) + "|new}}"
                self.assertEqual(preview_var_orthographies(rejected),
                                 (rejected, rejected, 0, 0))
                self.assertEqual(var_preview_refusal_reasons(rejected)["too_many_line_breaks"], 1)
                decisions = var_preview_call_partition(rejected)
                self.assertEqual(len(decisions), 1)
                self.assertEqual(decisions[0]["decision"], "too_many_line_breaks")
                self.assertNotIn("old", json.dumps(decisions))

    def test_var_same_line_boundary_recognizes_all_newline_conventions(self):
        # Separate CR-only historical lines must not masquerade as one
        # line containing multiple templates; inline and comment guards stay.
        for ending in ("\n", "\r\n", "\r"):
            with self.subTest(ending=repr(ending)):
                page = ("{{ВАР|мѣсто|место}}" + ending +
                        "{{ВАР|дѣло|дело}}" + ending)
                self.assertEqual(
                    preview_var_orthographies(page),
                    ("мѣсто" + ending + "дѣло" + ending,
                     "место" + ending + "дело" + ending, 2, 0),
                )
                self.assertEqual(
                    [row["decision"] for row in var_preview_call_partition(page)],
                    ["flat_preview", "flat_preview"],
                )
                inline = "{{ВАР|old|new}} {{nop}}" + ending
                self.assertEqual(preview_var_orthographies(inline),
                                 (inline, inline, 0, 0))
                self.assertEqual(
                    var_preview_refusal_reasons(inline)["multiple_templates_on_line"], 1
                )
                hidden = "<!--" + ending + "{{ВАР|old|new}}" + ending + "-->"
                self.assertEqual(preview_var_orthographies(hidden),
                                 (hidden, hidden, 0, 0))
                self.assertEqual(
                    var_preview_refusal_reasons(hidden)["multiple_templates_on_line"], 1
                )

    def test_var_preview_refusal_categories_do_not_expose_source(self):
        source = ("{{ВАР|дѣло|дело}}\n"
                  "{{ВАР|old|\nmodern}}\n"
                  "{{ВАР|a=b|plain}}\n"
                  "{{other|{{ВАР|a|b}}}}\n"
                  "{{ ВАР|old|new}}\n"
                  "{{ВАР|old|new|third}}\n"
                  "{{ВАР|" + "\n".join(["text"] * 14) + "|modern}}\n")
        old, new, flat, multiline = preview_var_orthographies(source)
        refusals = var_preview_refusal_reasons(source)
        self.assertEqual((flat, multiline), (1, 1))
        self.assertEqual(refusals, {
            "call_too_large": 0, "too_many_line_breaks": 1,
            "nested_braces": 0, "unbalanced_braces": 0,
            "extra_arguments": 1, "unsupported_shape": 1,
            "multiple_templates_on_line": 1, "non_plain_branch": 1,
        })
        self.assertEqual(sum(refusals.values()) + flat + multiline, 7)
        self.assertNotIn("дѣло", json.dumps(refusals, ensure_ascii=False))

    def test_refusal_diagnostics_partition_distinct_limits_and_nested_calls(self):
        source = ("{{ВАР|" + "x" * 4097 + "|new}}\n"
                  "{{ВАР|" + "\n".join(["old"] * 14) + "|new}}\n"
                  "{{ВАР|old{{nested}}|new}}\n"
                  "{{ВАР|a|b|c}}\n")
        reasons = var_preview_refusal_reasons(source)
        self.assertEqual(reasons["call_too_large"], 1)
        self.assertEqual(reasons["too_many_line_breaks"], 1)
        self.assertEqual(reasons["nested_braces"], 1)
        self.assertEqual(reasons["extra_arguments"], 1)
        self.assertEqual(sum(reasons.values()), 4)
        decisions = var_preview_call_partition(source)
        self.assertEqual(len(decisions), 4)
        self.assertEqual({d["decision"] for d in decisions},
                         {"call_too_large", "too_many_line_breaks",
                          "nested_braces", "extra_arguments"})
        self.assertTrue(all(len(d["invocation_sha256"]) == 64 for d in decisions))
        self.assertNotIn("old", json.dumps(decisions))

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

    def test_standalone_projection_keeps_exact_source_line_endings(self):
        # A Page's final line is not the synthetic LF between Pages.
        for ending in ("\n", "\r\n", "\r", ""):
            with self.subTest(ending=repr(ending)):
                self.assertEqual(
                    project_page("{{heading|4|Финал}}" + ending)[0],
                    "Финал" + ending,
                )
                self.assertEqual(project_page("{{nop}}" + ending)[0], ending)
                inline = "Before {{heading|4|Финал}}" + ending
                self.assertEqual(project_page(inline)[0], inline)
                prose = "Обычная проза" + ending
                self.assertEqual(project_page(prose)[0], prose)
                if ending:
                    source = "Обычная проза" + ending + "{{heading|4|Финал}}" + ending
                    self.assertEqual(
                        project_page(source)[0], "Обычная проза" + ending + "Финал" + ending
                    )

        # A nop-only Page with no newline is empty and must fail closed at join.
        projected, nop, heading, unresolved, residual = project_page("{{nop}}")
        self.assertEqual((projected, nop, heading, unresolved, residual),
                         ("", 1, 0, 0, 0))
        with self.assertRaisesRegex(ValueError, "empty or non-text"):
            ProjectedPageJoin().add(projected)

    def test_standalone_projection_refuses_enclosing_markup_not_literal_lines(self):
        # A standalone-looking invocation inside a multiline comment, wikilink
        # or outer template must remain unresolved, even on CR-only Pages.
        for ending in ("\n", "\r\n", "\r"):
            with self.subTest(ending=repr(ending)):
                comment = ("<!--" + ending + "{{nop}}" + ending +
                           "{{heading|4|Hidden}}" + ending + "-->" + ending +
                           "{{nop}}" + ending + "{{heading|4|Visible}}" + ending)
                expected = ("<!--" + ending + "{{nop}}" + ending +
                            "{{heading|4|Hidden}}" + ending + "-->" + ending +
                            ending + "Visible" + ending)
                self.assertEqual(project_page(comment),
                                 (expected, 1, 1, 2, 0))

                wikilink = ("[[Link|" + ending + "{{heading|4|Hidden}}" +
                            ending + "]]" + ending +
                            "{{heading|4|Visible}}" + ending)
                expected_link = ("[[Link|" + ending + "{{heading|4|Hidden}}" +
                                 ending + "]]" + ending + "Visible" + ending)
                self.assertEqual(project_page(wikilink),
                                 (expected_link, 0, 1, 1, 0))

                enclosing_template = ("{{outer|" + ending + "{{nop}}" +
                                      ending + "}}" + ending + "{{nop}}" + ending)
                expected_outer = ("{{outer|" + ending + "{{nop}}" +
                                  ending + "}}" + ending + ending)
                self.assertEqual(project_page(enclosing_template),
                                 (expected_outer, 1, 0, 2, 0))

                unclosed_comment = "<!--" + ending + "{{nop}}" + ending
                self.assertEqual(project_page(unclosed_comment),
                                 (unclosed_comment, 0, 0, 1, 0))

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
        self.assertEqual(report["pages"][0]["source_mediawiki_sha1"],
                         graph["pages"][0]["mediawiki_sha1"])
        self.assertEqual([d["decision"] for d in report["pages"][0]["var_call_partition"]],
                         ["flat_preview", "multiline_preview"])
        validate_projection(report, graph, preflight, shapes)

        altered = copy.deepcopy(report)
        altered["pages"][0]["var_preview_refusal_reasons"]["too_many_line_breaks"] = 1
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
        with self.assertRaisesRegex(ValueError, "revision/source SHA-1 drift"):
            validate_projection(altered, graph, preflight, shapes)
        altered = copy.deepcopy(report)
        altered["pages"][0]["source_mediawiki_sha1"] = "0" * 40
        with self.assertRaisesRegex(ValueError, "revision/source SHA-1 drift"):
            validate_projection(altered, graph, preflight, shapes)
        altered = copy.deepcopy(report)
        altered["pages"][0]["var_call_partition"][0]["invocation_sha256"] = "0" * 64
        with self.assertRaisesRegex(ValueError, "VAR invocation identity"):
            validate_projection(altered, graph, preflight, shapes)
        altered = copy.deepcopy(report)
        altered["pages"][0]["var_call_partition"][0]["decision"] = "non_plain_branch"
        with self.assertRaisesRegex(ValueError, "VAR decision histogram"):
            validate_projection(altered, graph, preflight, shapes)


if __name__ == "__main__":
    unittest.main()
