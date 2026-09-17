from __future__ import annotations

from hashlib import sha256
import unittest

from scriptorium.mediawiki_transclusion import (
    MANIFEST_VERSION,
    PROFILE_VERSION,
    build_transclusion_shape_manifest,
    classify_effective_dependencies,
    preprocess_for_transclusion,
)


class MediaWikiTransclusionTests(unittest.TestCase):
    def test_noinclude_removed_and_includeonly_retained(self) -> None:
        out, counts = preprocess_for_transclusion(
            "a<noinclude>{{doc}}</noinclude>b<includeonly>c</includeonly>d"
        )
        self.assertEqual(out, "abcd")
        self.assertEqual(counts["noinclude_pairs"], 1)
        self.assertEqual(counts["includeonly_pairs"], 1)
        self.assertEqual(counts["onlyinclude_pairs"], 0)

    def test_onlyinclude_precedence_and_multiple_blocks(self) -> None:
        out, _ = preprocess_for_transclusion(
            "a<includeonly>x</includeonly><onlyinclude>b<noinclude>z</noinclude>c</onlyinclude>"
            "d<onlyinclude>e<includeonly>f</includeonly></onlyinclude>g"
        )
        self.assertEqual(out, "bcef")

    def test_self_closing_control_tags_are_removed_without_changing_scope(self) -> None:
        out, counts = preprocess_for_transclusion("a<noinclude />b<includeonly/>c")
        self.assertEqual(out, "abc")
        self.assertEqual(counts["noinclude_self_closing"], 1)
        self.assertEqual(counts["includeonly_self_closing"], 1)

    def test_malformed_and_nowiki_fail_closed(self) -> None:
        with self.assertRaises(ValueError):
            preprocess_for_transclusion("<noinclude>x</includeonly>")
        with self.assertRaisesRegex(ValueError, "nowiki"):
            preprocess_for_transclusion("<nowiki><noinclude>x</noinclude></nowiki>")

    def test_effective_dependency_classifier_separates_classes(self) -> None:
        graph = classify_effective_dependencies(
            "{{foo|x={{{1|}}}}} {{#if:{{{1|}}}|y}} {{#tag:poem|z}} {{PAGENAME}} <div>x</div>"
        )
        self.assertEqual(graph["ordinary_template_counts"], {"foo": 1})
        self.assertEqual(graph["parser_function_counts"], {"#if": 1, "#tag": 1})
        self.assertEqual(graph["magic_word_counts"], {"PAGENAME": 1})
        self.assertEqual(graph["extension_tag_targets"], {"poem": 1})
        self.assertEqual(graph["html_tag_name_counts"], {"div": 2})

    def test_manifest_is_source_free_and_stops_before_parser_expansion(self) -> None:
        text = (
            "<noinclude>{{doc}}</noinclude>{{#if:1|{{PAGENAME}}}}"
            "<includeonly>{{#tag:poem|x}}</includeonly>"
        )
        identity = {
            "title": "Шаблон:Poemx1",
            "revision_id": 5142743,
            "wikitext_sha256": sha256(text.encode()).hexdigest(),
        }
        manifest = build_transclusion_shape_manifest(
            candidate_id="gorky-klim-samgin-ru-poemx1-template",
            revision_identity=identity,
            wikitext=text,
            research_date="2026-09-17",
        )
        self.assertEqual(manifest["manifest_version"], MANIFEST_VERSION)
        self.assertEqual(manifest["preprocessing_profile"], PROFILE_VERSION)
        self.assertEqual(manifest["effective_dependency_graph"]["ordinary_template_counts"], {})
        self.assertEqual(
            manifest["effective_dependency_graph"]["parser_function_counts"],
            {"#if": 1, "#tag": 1},
        )
        self.assertEqual(
            manifest["effective_dependency_graph"]["extension_tag_targets"], {"poem": 1}
        )
        scope = manifest["capture_scope"]
        self.assertIs(scope["partial_transclusion_control_semantics_reproduced"], True)
        self.assertIs(scope["parser_function_expansion_reproduced"], False)
        self.assertIs(scope["extension_tag_expansion_reproduced"], False)
        self.assertIs(scope["historical_render_equivalence_proven"], False)
        self.assertNotIn("wikitext", manifest)


if __name__ == "__main__":
    unittest.main()
