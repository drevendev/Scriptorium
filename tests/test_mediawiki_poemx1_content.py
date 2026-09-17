from __future__ import annotations

import hashlib
import unittest

from scriptorium.mediawiki_poemx1_content import (
    MANIFEST_VERSION,
    PROFILE_VERSION,
    _brace_inventory,
    _render_surface,
    build_poemx1_content_surface_manifest,
)
from scriptorium.mediawiki_template_invocation import build_invocation_binding_manifest


def _binding_manifest(source: str) -> dict[str, object]:
    identity = {
        "title": "dependency",
        "revision_id": 2366546,
        "wikitext_sha256": hashlib.sha256(source.encode()).hexdigest(),
    }
    return build_invocation_binding_manifest(
        candidate_id="gorky-klim-samgin-ru-poemx1-invocations",
        dependency_revision_identity=identity,
        dependency_wikitext=source,
        parameter_surface_names=["1", "2", "3", "fixed", "poem", "small", "width"],
        research_date="2026-09-18",
    )


class MediaWikiPoemx1ContentTests(unittest.TestCase):
    def test_brace_inventory_counts_nested_constructs(self) -> None:
        observed = _brace_inventory("a {{outer|{{inner}}|{{{p|x}}}}} z")
        self.assertEqual(observed["template_or_parser_construct_count"], 2)
        self.assertEqual(observed["template_parameter_construct_count"], 1)
        self.assertEqual(observed["brace_expansion_construct_count"], 3)

    def test_brace_inventory_fails_closed_on_malformed_source(self) -> None:
        with self.assertRaises(ValueError):
            _brace_inventory("{{outer|x")
        with self.assertRaises(ValueError):
            _brace_inventory("plain }}")

    def test_render_surface_separates_template_expansion_from_render_markup(self) -> None:
        observed = _render_surface(
            ":line [[Page|label]]\n leading ''emphasis'' <span>text</span>"
        )
        self.assertEqual(observed["brace_expansion_construct_count"], 0)
        self.assertIs(
            observed["template_expansion_identity_for_observed_value"], True
        )
        self.assertEqual(observed["wikilink_open_count"], 1)
        self.assertEqual(observed["apostrophe_markup_run_count"], 2)
        self.assertEqual(observed["xml_like_tag_name_counts"], {"span": 2})
        self.assertEqual(observed["leading_colon_line_count"], 1)
        self.assertEqual(observed["leading_space_line_count"], 1)
        self.assertEqual(observed["newline_count"], 1)

    def test_render_surface_flags_brace_expansion_constructs(self) -> None:
        observed = _render_surface("before {{x|{{{p|d}}}}} after")
        self.assertEqual(observed["brace_expansion_construct_count"], 2)
        self.assertIs(
            observed["template_expansion_identity_for_observed_value"], False
        )

    def test_manifest_revalidates_values_without_persisting_prose(self) -> None:
        values = [
            "one",
            "two [[Page|label]]",
            "three\nfour",
            ":five",
            " six",
            "seven ''eight''",
        ]
        source = "\n".join(f"{{{{poemx1||{value}}}}}" for value in values)
        binding = _binding_manifest(source)

        import scriptorium.mediawiki_poemx1_content as content

        old_digest = content._DEPENDENCY_WIKITEXT_SHA256
        try:
            content._DEPENDENCY_WIKITEXT_SHA256 = hashlib.sha256(source.encode()).hexdigest()
            binding["dependency_revision"]["wikitext_sha256"] = (
                content._DEPENDENCY_WIKITEXT_SHA256
            )
            manifest = build_poemx1_content_surface_manifest(
                dependency_wikitext=source,
                binding_manifest=binding,
                research_date="2026-09-18",
            )
        finally:
            content._DEPENDENCY_WIKITEXT_SHA256 = old_digest

        self.assertEqual(manifest["manifest_version"], MANIFEST_VERSION)
        self.assertEqual(manifest["profile"], PROFILE_VERSION)
        self.assertEqual(manifest["invocation_count"], 6)
        self.assertIs(manifest["observed_parameter_2_template_expansion_identity"], True)
        self.assertIs(manifest["requires_additional_template_dependency_resolution"], False)
        self.assertEqual(
            manifest["aggregate_surface"]["brace_expansion_construct_count"], 0
        )
        self.assertIs(manifest["source_text_included"], False)
        serialized = repr(manifest)
        for value in ("one", "Page", "seven", "eight"):
            self.assertNotIn(value, serialized)

    def test_manifest_detects_binding_value_drift(self) -> None:
        source = "\n".join(f"{{{{poemx1||value-{index}}}}}" for index in range(6))
        binding = _binding_manifest(source)
        import scriptorium.mediawiki_poemx1_content as content

        old_digest = content._DEPENDENCY_WIKITEXT_SHA256
        try:
            content._DEPENDENCY_WIKITEXT_SHA256 = hashlib.sha256(source.encode()).hexdigest()
            binding["dependency_revision"]["wikitext_sha256"] = (
                content._DEPENDENCY_WIKITEXT_SHA256
            )
            binding["invocations"][0]["effective_bindings"]["2"]["sha256"] = "0" * 64
            with self.assertRaises(ValueError):
                build_poemx1_content_surface_manifest(
                    dependency_wikitext=source,
                    binding_manifest=binding,
                    research_date="2026-09-18",
                )
        finally:
            content._DEPENDENCY_WIKITEXT_SHA256 = old_digest


if __name__ == "__main__":
    unittest.main()
