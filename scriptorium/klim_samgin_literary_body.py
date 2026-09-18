"""Public entry point for the candidate-specific Klim Samgin literary-body extractor.

The Part 2 target is a transcluded Wikisource subpage.  After the six already-frozen
plain ``poemx1`` values are substituted, the dependency still has MediaWiki
``noinclude``/``includeonly`` control tags.  Apply the repository's documented
partial-transclusion layer before handing the result to the literary renderer.
"""
from __future__ import annotations

from typing import Mapping

from . import klim_samgin_literary_body_impl as _impl
from .mediawiki_transclusion import preprocess_for_transclusion


def _resolve_part2_target_to_literary_values(
    parent: str,
    dependency: str,
    *,
    lst_contract: Mapping[str, object],
    part2_resolution_manifest: Mapping[str, object],
) -> tuple[str, dict[str, object]]:
    frozen_rows = part2_resolution_manifest.get("poemx1_expansions")
    observed_rows = _impl.find_template_invocations(dependency, template_name="poemx1")
    if not isinstance(frozen_rows, list) or len(frozen_rows) != 6 or len(observed_rows) != 6:
        raise ValueError("Part 2 dependency poemx1 inventory drift")

    replacements: list[tuple[int, int, str]] = []
    for index, (observed, frozen_obj) in enumerate(zip(observed_rows, frozen_rows), start=1):
        frozen = _impl._require_mapping(frozen_obj, label=f"Part 2 target poemx1 row {index}")
        value = _impl._plain_poem_value(
            dependency,
            observed,
            expected_invocation_sha256=frozen.get("invocation_sha256"),
            expected_parameter_2_sha256=frozen.get("parameter_2_sha256"),
        )
        start = observed.get("parent_start_offset")
        end = observed.get("parent_end_offset")
        if not isinstance(start, int) or not isinstance(end, int):
            raise ValueError("Part 2 dependency poemx1 offsets missing")
        replacements.append((start, end, value))

    pre_transclusion = _impl._replace_spans(dependency, replacements)
    if _impl.find_template_invocations(pre_transclusion, template_name="poemx1"):
        raise ValueError("Part 2 literary dependency retains poemx1")
    if "{{" in pre_transclusion or "}}" in pre_transclusion:
        raise ValueError("Part 2 literary dependency retains unsupported brace expansion syntax")

    literary_dependency, control_counts = preprocess_for_transclusion(pre_transclusion)
    lowered = literary_dependency.casefold()
    if any(tag in lowered for tag in ("<noinclude", "</noinclude", "<includeonly", "</includeonly", "<onlyinclude", "</onlyinclude")):
        raise ValueError("Part 2 dependency retains partial-transclusion control tags")

    invocation = _impl._require_mapping(lst_contract.get("invocation"), label="Part 2 #lst invocation")
    start = invocation.get("parent_start_offset")
    end = invocation.get("parent_end_offset")
    if not isinstance(start, int) or not isinstance(end, int):
        raise ValueError("Part 2 #lst offsets missing")
    if _impl._sha256_text(parent[start:end]) != invocation.get("invocation_sha256"):
        raise ValueError("Part 2 #lst placement drift before literary substitution")

    resolved = parent[:start] + literary_dependency + parent[end:]
    return resolved, {
        "target_poemx1_literary_replacement_count": len(replacements),
        "dependency_partial_transclusion_controls_applied": True,
        "dependency_transclusion_control_counts": control_counts,
        "literary_dependency_pre_transclusion_character_count": len(pre_transclusion),
        "literary_dependency_pre_transclusion_utf8_byte_count": len(pre_transclusion.encode("utf-8")),
        "literary_dependency_character_count": len(literary_dependency),
        "literary_dependency_utf8_byte_count": len(literary_dependency.encode("utf-8")),
        "literary_dependency_sha256": _impl._sha256_text(literary_dependency),
        "target_only_lst_substitution_applied": True,
    }


# ``build_manifest`` resolves this name from the implementation module at runtime.
# Installing the candidate-specific transclusion stage here keeps the generic
# MediaWiki control processor independently testable and makes the public CLI use
# the same exact path as the regression tests.
_impl._resolve_part2_target_to_literary_values = _resolve_part2_target_to_literary_values

COMPOSITE_SEPARATOR = _impl.COMPOSITE_SEPARATOR
COMPOSITION_PROFILE = _impl.COMPOSITION_PROFILE
EXTRACTION_PROFILE = _impl.EXTRACTION_PROFILE
MANIFEST_VERSION = _impl.MANIFEST_VERSION
_extract_part_literary_body = _impl._extract_part_literary_body
_plain_poem_value = _impl._plain_poem_value
_raw_template_spans = _impl._raw_template_spans
build_manifest = _impl.build_manifest
main = _impl.main
replay_manifest = _impl.replay_manifest
validate_manifest = _impl.validate_manifest

__all__ = [
    "COMPOSITE_SEPARATOR",
    "COMPOSITION_PROFILE",
    "EXTRACTION_PROFILE",
    "MANIFEST_VERSION",
    "_extract_part_literary_body",
    "_plain_poem_value",
    "_raw_template_spans",
    "build_manifest",
    "replay_manifest",
    "validate_manifest",
    "main",
]

if __name__ == "__main__":
    raise SystemExit(main())
