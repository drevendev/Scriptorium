from __future__ import annotations

import hashlib
import unittest

import scriptorium.mediawiki_poem_history as history
from scriptorium.mediawiki_poem_history import (
    MANIFEST_VERSION,
    PROFILE_VERSION,
    _git_blob_sha1,
    _semantic_inventory,
    build_poem_extension_source_anchor,
)


_FIXTURE = """$parser->setHook( 'poem', [ $this, 'renderPoem' ] );
$newline = isset( $param['compact'] ) ? '' : "\\n";
$tag = $parser->insertStripItem( "<br />" );
'/^(:++)(.+)$/m'
'class' => 'mw-poem-indented'
"margin-inline-start: $indentation;"
'/(?<!^----)\\n/m'
"$tag\\n"
'/^ +/m'
'&#160;'
$parser->recursiveTagParse( $text, $frame );
Sanitizer::validateTagAttributes( $param, 'div' )
$attribs['class'] = 'poem ' . $attribs['class'];
$attribs['class'] = 'poem';
Html::rawElement( 'div', $attribs, $newline . trim( $text ) . $newline )
"""


class MediaWikiPoemHistoryTests(unittest.TestCase):
    def test_git_blob_sha_matches_git_object_formula(self) -> None:
        data = b"hello\n"
        expected = hashlib.sha1(b"blob 6\0hello\n").hexdigest()
        self.assertEqual(_git_blob_sha1(data), expected)

    def test_semantic_inventory_requires_bounded_transformations(self) -> None:
        observed = _semantic_inventory(_FIXTURE)
        self.assertTrue(all(observed.values()))
        self.assertEqual(
            set(observed),
            {
                "poem_parser_hook_registered",
                "compact_parameter_controls_wrapper_newlines",
                "line_break_strip_item_inserted",
                "leading_colons_become_indented_spans",
                "interior_newlines_become_breaks",
                "leading_spaces_become_nbsp_entities",
                "recursive_tag_parse_applied",
                "div_attributes_sanitized",
                "poem_css_class_forced",
                "output_wrapped_in_div",
            },
        )

    def test_manifest_is_source_free_and_keeps_historical_boundary_explicit(self) -> None:
        source = _FIXTURE
        source_bytes = source.encode("utf-8")
        old = (
            history.UPSTREAM_SOURCE_UTF8_BYTE_COUNT,
            history.UPSTREAM_SOURCE_SHA256,
            history.UPSTREAM_GIT_BLOB_SHA1,
        )
        try:
            history.UPSTREAM_SOURCE_UTF8_BYTE_COUNT = len(source_bytes)
            history.UPSTREAM_SOURCE_SHA256 = hashlib.sha256(source_bytes).hexdigest()
            history.UPSTREAM_GIT_BLOB_SHA1 = _git_blob_sha1(source_bytes)
            manifest = build_poem_extension_source_anchor(
                source_text=source, research_date="2026-09-18"
            )
        finally:
            (
                history.UPSTREAM_SOURCE_UTF8_BYTE_COUNT,
                history.UPSTREAM_SOURCE_SHA256,
                history.UPSTREAM_GIT_BLOB_SHA1,
            ) = old

        self.assertEqual(manifest["manifest_version"], MANIFEST_VERSION)
        self.assertEqual(manifest["profile"], PROFILE_VERSION)
        self.assertEqual(manifest["evidence_class"], "inferred_reconstruction_anchor")
        scope = manifest["capture_scope"]
        self.assertIs(scope["upstream_source_identity_frozen"], True)
        self.assertIs(scope["historical_wikisource_deployment_equivalence_proven"], False)
        self.assertIs(scope["poem_extension_rendering_reproduced"], False)
        self.assertIs(scope["resolved_part2_identity_frozen"], False)
        self.assertIs(manifest["m2_parity_admissible"], False)
        self.assertIs(manifest["source_text_included"], False)
        self.assertNotIn("$parser", repr(manifest))
        self.assertNotIn("renderPoem", repr(manifest))

    def test_manifest_fails_closed_on_source_drift(self) -> None:
        with self.assertRaises(ValueError):
            build_poem_extension_source_anchor(
                source_text="not the pinned source", research_date="2026-09-18"
            )


if __name__ == "__main__":
    unittest.main()
