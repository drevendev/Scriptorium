"""Historical source anchor for the MediaWiki Poem extension used by Klim Samgin.

This module does not claim that Russian Wikisource deployed this exact extension commit
when the pinned Part 2 parent revision was saved. It freezes an explicit inferred
reconstruction anchor: the latest upstream ``includes/Poem.php`` commit observed not
later than that parent timestamp, then verifies the immutable source bytes and records
only source-free behavior evidence needed by the remaining ``#tag:poem`` boundary.
"""
from __future__ import annotations

from hashlib import sha1, sha256

PROFILE_VERSION = "scriptorium-mediawiki-poem-source-anchor-v1"
MANIFEST_VERSION = "scriptorium-poem-extension-source-anchor-v1"

UPSTREAM_REPOSITORY = "wikimedia/mediawiki-extensions-Poem"
UPSTREAM_PATH = "includes/Poem.php"
PARENT_REVISION_ID = 5198033
PARENT_REVISION_TIMESTAMP = "2024-11-26T11:16:35Z"
ANCHOR_POLICY = "latest_path_commit_not_later_than_parent_revision_timestamp"
UPSTREAM_COMMIT = "03b3694613e23efa1254d8bbbb98121efaef2cb0"
UPSTREAM_COMMIT_TIMESTAMP = "2024-10-20T09:15:42Z"
UPSTREAM_GIT_BLOB_SHA1 = "a362a50d6e139b03a6afd5c24ce7a0923d68ee13"
UPSTREAM_SOURCE_SHA256 = "86e853c6c41e94356d57824492f32407b916b890ccdfe31c38a081070fb5313c"
UPSTREAM_SOURCE_UTF8_BYTE_COUNT = 2702

UPSTREAM_SOURCE_URL = (
    "https://github.com/"
    f"{UPSTREAM_REPOSITORY}/blob/{UPSTREAM_COMMIT}/{UPSTREAM_PATH}"
)
UPSTREAM_HISTORY_URL = (
    "https://github.com/"
    f"{UPSTREAM_REPOSITORY}/commits/master/{UPSTREAM_PATH}"
)


def _git_blob_sha1(source_bytes: bytes) -> str:
    header = f"blob {len(source_bytes)}\0".encode("ascii")
    return sha1(header + source_bytes).hexdigest()


def _semantic_inventory(source_text: str) -> dict[str, bool]:
    """Return only the bounded source facts required by the next rendering layer."""
    if not isinstance(source_text, str):
        raise TypeError("source_text must be str")
    checks = {
        "poem_parser_hook_registered": "$parser->setHook( 'poem'," in source_text,
        "compact_parameter_controls_wrapper_newlines": (
            "$newline = isset( $param['compact'] ) ? '' : \"\\n\";" in source_text
        ),
        "line_break_strip_item_inserted": (
            '$parser->insertStripItem( "<br />" )' in source_text
        ),
        "leading_colons_become_indented_spans": (
            "'/^(:++)(.+)$/m'" in source_text
            and "'class' => 'mw-poem-indented'" in source_text
            and "margin-inline-start: $indentation;" in source_text
        ),
        "interior_newlines_become_breaks": (
            "'/(?<!^----)\\n/m'" in source_text
            and '"$tag\\n"' in source_text
        ),
        "leading_spaces_become_nbsp_entities": (
            "'/^ +/m'" in source_text and "'&#160;'" in source_text
        ),
        "recursive_tag_parse_applied": (
            "$parser->recursiveTagParse( $text, $frame )" in source_text
        ),
        "div_attributes_sanitized": (
            "Sanitizer::validateTagAttributes( $param, 'div' )" in source_text
        ),
        "poem_css_class_forced": (
            "$attribs['class'] = 'poem ' . $attribs['class'];" in source_text
            and "$attribs['class'] = 'poem';" in source_text
        ),
        "output_wrapped_in_div": (
            "Html::rawElement( 'div', $attribs, $newline . trim( $text ) . $newline )"
            in source_text
        ),
    }
    return checks


def build_poem_extension_source_anchor(
    *, source_text: str, research_date: str
) -> dict[str, object]:
    """Verify the pinned upstream source and emit a source-free provenance manifest."""
    if not isinstance(source_text, str):
        raise TypeError("source_text must be str")
    if not isinstance(research_date, str) or not research_date:
        raise ValueError("research_date must be non-empty")

    source_bytes = source_text.encode("utf-8")
    if len(source_bytes) != UPSTREAM_SOURCE_UTF8_BYTE_COUNT:
        raise ValueError("Poem source byte-count drift")
    if sha256(source_bytes).hexdigest() != UPSTREAM_SOURCE_SHA256:
        raise ValueError("Poem source SHA-256 drift")
    if _git_blob_sha1(source_bytes) != UPSTREAM_GIT_BLOB_SHA1:
        raise ValueError("Poem source Git blob identity drift")

    semantics = _semantic_inventory(source_text)
    missing = sorted(name for name, present in semantics.items() if not present)
    if missing:
        raise ValueError(f"required Poem source semantics missing: {missing}")

    return {
        "manifest_version": MANIFEST_VERSION,
        "candidate_id": "gorky-klim-samgin-ru-poem-extension-source-anchor",
        "research_date": research_date,
        "profile": PROFILE_VERSION,
        "evidence_class": "inferred_reconstruction_anchor",
        "anchor": {
            "policy": ANCHOR_POLICY,
            "parent_revision_id": PARENT_REVISION_ID,
            "parent_revision_timestamp": PARENT_REVISION_TIMESTAMP,
            "upstream_repository": UPSTREAM_REPOSITORY,
            "upstream_path": UPSTREAM_PATH,
            "upstream_commit": UPSTREAM_COMMIT,
            "upstream_commit_timestamp": UPSTREAM_COMMIT_TIMESTAMP,
            "upstream_git_blob_sha1": UPSTREAM_GIT_BLOB_SHA1,
            "upstream_source_sha256": UPSTREAM_SOURCE_SHA256,
            "upstream_source_utf8_byte_count": UPSTREAM_SOURCE_UTF8_BYTE_COUNT,
            "upstream_source_url": UPSTREAM_SOURCE_URL,
            "upstream_history_url": UPSTREAM_HISTORY_URL,
        },
        "bounded_source_semantics": semantics,
        "capture_scope": {
            "upstream_source_identity_frozen": True,
            "bounded_poem_source_semantics_frozen": True,
            "historical_wikisource_deployment_equivalence_proven": False,
            "tag_invocation_attribute_surface_frozen": False,
            "poem_extension_rendering_reproduced": False,
            "mediawiki_core_recursive_parse_reproduced": False,
            "resolved_part2_identity_frozen": False,
            "historical_render_equivalence_proven": False,
            "source_text_committed": False,
        },
        "boundary": (
            "This artifact freezes an inferred upstream Poem source anchor and the exact "
            "source-level transformations relevant to the live #tag:poem path. It does "
            "not prove which extension commit Russian Wikisource deployed at the parent "
            "save timestamp, does not yet freeze the concrete #tag attribute surface, "
            "does not reproduce MediaWiki recursive parsing, and does not claim resolved "
            "Part 2 bytes or historical render equivalence."
        ),
        "fantlab_source_edition_match": "unknown",
        "m2_parity_admissible": False,
        "source_text_included": False,
    }
