"""Freeze source-free literary-body identities for the four pinned Klim Samgin parts.

This is a candidate-specific extraction profile, not a generic MediaWiki renderer.
Pinned prose is fetched transiently, transformed under already-frozen source contracts,
and reduced to counts/digests before anything is persisted.
"""
from __future__ import annotations

import argparse
from hashlib import sha256
import json
from pathlib import Path
import re
from typing import Callable, Mapping, Sequence

from .klim_samgin_body_surface import (
    CANDIDATE_ID,
    EXPECTED_DIRECT_POEMX1_COUNTS,
    EXPECTED_PART_REVISION_IDS,
    validate_body_surface_manifest,
)
from .klim_samgin_direct_poemx1_surface import validate_manifest as validate_direct_manifest
from .klim_samgin_freeze import LST_CONTRACT_VERSION
from .mediawiki_part2_resolution import validate_part2_resolution_manifest
from .mediawiki_poemx1_content import _parameter_two_value
from .mediawiki_template_invocation import find_template_invocations
from .mediawiki_transclusion import preprocess_for_transclusion
from .single_page_body import fetch_pinned_wikitext
from .single_page_revision import validate_manifest as validate_revision_manifest
from .text import NORMALIZATION_PROFILE, normalize_text
from .wikisource_freeze import extract_transcription_body

MANIFEST_VERSION = "scriptorium-klim-samgin-literary-body-v1"
PROFILE_VERSION = "scriptorium-klim-samgin-wikisource-body-v1"
COMPOSITION_PROFILE = "scriptorium-klim-samgin-four-part-composite-v1"
COMPOSITION_SEPARATOR = "\n\n"
DEPENDENCY_CANDIDATE_ID = "gorky-klim-samgin-ru-part-2-part2"
EXPECTED_DEPENDENCY_REVISION_ID = 2366546

_HEADING3_RE = re.compile(
    r"(?m)^[ \t]*===(?!=)[ \t]*(?P<text>[^\n=].*?)[ \t]*(?<![=])===(?![=])[ \t]*$"
)
_ANY_HEADING_RE = re.compile(r"(?m)^[ \t]*={2,6}.*?={2,6}[ \t]*$")
_CATEGORY_LINE_RE = re.compile(
    r"(?mi)^[ \t]*\[\[\s*(?:Категория|Category)\s*:[^\]\n]+\]\][ \t]*$"
)
_NOWIKI_PAIR_RE = re.compile(r"<nowiki>(.*?)</nowiki\s*>", re.IGNORECASE | re.DOTALL)
_NOWIKI_ANY_RE = re.compile(r"</?nowiki\b[^>]*>", re.IGNORECASE)
_TABLE_OPEN_RE = re.compile(r"(?m)^[ \t]*\{\|")
_TABLE_ROW_OR_END_RE = re.compile(r"(?m)^[ \t]*\|(?:-|\})")
_LITERAL_LINE_OPENER_RE = re.compile(r"(?m)^(?P<indent>[ \t]*)(?P<mark>[|!])")


def _load_json(path: Path) -> dict[str, object]:
    value = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(value, dict):
        raise ValueError("manifest must be a JSON object")
    return value


def _write_json(path: Path, value: Mapping[str, object]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        json.dumps(value, ensure_ascii=False, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )


def _sha256_text(value: str) -> str:
    return sha256(value.encode("utf-8")).hexdigest()


def _identity(value: str) -> dict[str, object]:
    normalized = normalize_text(value)
    raw = value.encode("utf-8")
    return {
        "character_count_including_spaces": len(value),
        "utf8_byte_count": len(raw),
        "raw_sha256": sha256(raw).hexdigest(),
        "normalization_profile": NORMALIZATION_PROFILE,
        "normalized_character_count_including_spaces": len(normalized),
        "normalized_sha256": sha256(normalized.encode("utf-8")).hexdigest(),
    }


def _verified_wikitext(
    revision_manifest: Mapping[str, object],
    *,
    expected_candidate: str,
    expected_revision_id: int,
    fetcher: Callable[..., dict[str, object]],
) -> tuple[str, Mapping[str, object]]:
    validate_revision_manifest(revision_manifest)
    if revision_manifest.get("candidate_id") != expected_candidate:
        raise ValueError(f"unexpected candidate {revision_manifest.get('candidate_id')!r}")
    identity = revision_manifest.get("source_identity")
    if not isinstance(identity, Mapping) or identity.get("revision_id") != expected_revision_id:
        raise ValueError("unexpected pinned revision identity")
    title = identity.get("title")
    revision_id = identity.get("revision_id")
    if not isinstance(title, str) or not isinstance(revision_id, int):
        raise ValueError("pinned revision locator incomplete")
    observed = fetcher(title=title, revision_id=revision_id)
    wikitext = observed.pop("wikitext", None)
    if not isinstance(wikitext, str):
        raise ValueError("transient pinned wikitext missing")
    if observed != dict(identity):
        differing = sorted(
            key for key in set(observed) | set(identity)
            if observed.get(key) != identity.get(key)
        )
        raise ValueError(f"pinned revision identity drift: {differing}")
    return wikitext, identity


def _replace_spans(source: str, replacements: Sequence[tuple[int, int, str]]) -> str:
    previous_start = len(source) + 1
    out = source
    for start, end, replacement in sorted(replacements, reverse=True):
        if not (0 <= start < end <= len(source)) or end > previous_start:
            raise ValueError("overlapping or invalid frozen replacement span")
        out = out[:start] + replacement + out[end:]
        previous_start = start
    return out


def _literaryize_direct_poemx1(
    source: str,
    *,
    part: int,
    frozen_part: Mapping[str, object],
) -> tuple[str, int]:
    observed = find_template_invocations(source, template_name="poemx1")
    frozen_rows = frozen_part.get("invocations")
    expected_count = EXPECTED_DIRECT_POEMX1_COUNTS[part]
    if not isinstance(frozen_rows, list) or len(frozen_rows) != expected_count:
        raise ValueError(f"Klim part {part} frozen direct poemx1 rows drift")
    if len(observed) != expected_count:
        raise ValueError(f"Klim part {part} direct poemx1 count drift")
    replacements: list[tuple[int, int, str]] = []
    for live, frozen_obj in zip(observed, frozen_rows):
        if not isinstance(frozen_obj, Mapping):
            raise ValueError("invalid frozen direct poemx1 row")
        if live.get("invocation_sha256") != frozen_obj.get("invocation_sha256"):
            raise ValueError("direct poemx1 invocation identity drift")
        if frozen_obj.get("plain_value_literary_replacement_safe") is not True:
            raise ValueError("direct poemx1 is not frozen as plain literary-safe")
        value, identity = _parameter_two_value(source, live)
        if identity != frozen_obj.get("parameter_2_identity"):
            raise ValueError("direct poemx1 parameter-2 identity drift")
        start = live.get("parent_start_offset")
        end = live.get("parent_end_offset")
        if not isinstance(start, int) or not isinstance(end, int):
            raise ValueError("direct poemx1 offsets missing")
        replacements.append((start, end, value))
    return _replace_spans(source, replacements), len(replacements)


def _literaryize_dependency(
    dependency: str,
    part2_resolution: Mapping[str, object],
) -> tuple[str, dict[str, object]]:
    """Apply the already-frozen transclusion controls, then replace six poem calls."""
    validate_part2_resolution_manifest(part2_resolution)
    transclusion_input, control_counts = preprocess_for_transclusion(dependency)
    frozen_controls = part2_resolution.get("transclusion_control_counts")
    if not isinstance(frozen_controls, Mapping) or control_counts != dict(frozen_controls):
        raise ValueError("Part 2 dependency transclusion-control inventory drift")

    rows = part2_resolution.get("poemx1_expansions")
    if not isinstance(rows, list) or len(rows) != 6:
        raise ValueError("Part 2 resolution must freeze six dependency poemx1 calls")
    observed = find_template_invocations(transclusion_input, template_name="poemx1")
    if len(observed) != 6:
        raise ValueError("Part 2 dependency poemx1 inventory drift after transclusion controls")
    replacements: list[tuple[int, int, str]] = []
    for live, frozen_obj in zip(observed, rows):
        if not isinstance(frozen_obj, Mapping):
            raise ValueError("invalid Part 2 resolution row")
        if live.get("invocation_sha256") != frozen_obj.get("invocation_sha256"):
            raise ValueError("dependency poemx1 invocation identity drift")
        value, identity = _parameter_two_value(transclusion_input, live)
        if identity.get("sha256") != frozen_obj.get("parameter_2_sha256"):
            raise ValueError("dependency poemx1 parameter-2 identity drift")
        start = live.get("parent_start_offset")
        end = live.get("parent_end_offset")
        if not isinstance(start, int) or not isinstance(end, int):
            raise ValueError("dependency poemx1 offsets missing")
        replacements.append((start, end, value))
    literary = _replace_spans(transclusion_input, replacements)
    if "{{" in literary or "}}" in literary:
        raise ValueError("literaryized Part 2 dependency retains unsupported brace syntax")
    return literary, {
        "transclusion_control_counts": control_counts,
        "dependency_poemx1_replacement_count": len(replacements),
        "literary_dependency_character_count": len(literary),
        "literary_dependency_utf8_byte_count": len(literary.encode("utf-8")),
        "literary_dependency_sha256": _sha256_text(literary),
    }


def _substitute_part2_dependency(
    parent: str,
    dependency_literary: str,
    lst_contract: Mapping[str, object],
) -> str:
    if lst_contract.get("contract_version") != LST_CONTRACT_VERSION:
        raise ValueError("unexpected Part 2 #lst contract")
    invocation = lst_contract.get("invocation")
    if not isinstance(invocation, Mapping):
        raise ValueError("Part 2 #lst invocation missing")
    start = invocation.get("parent_start_offset")
    end = invocation.get("parent_end_offset")
    if not isinstance(start, int) or not isinstance(end, int):
        raise ValueError("Part 2 #lst offsets missing")
    if _sha256_text(parent[start:end]) != invocation.get("invocation_sha256"):
        raise ValueError("Part 2 #lst placement drift")
    return parent[:start] + dependency_literary + parent[end:]


def _replace_named_template(source: str, name: str, *, expected: int, replacement: str) -> str:
    rows = find_template_invocations(source, template_name=name)
    if len(rows) != expected:
        raise ValueError(f"expected {expected} {name} invocations, observed {len(rows)}")
    spans: list[tuple[int, int, str]] = []
    for row in rows:
        start = row.get("parent_start_offset")
        end = row.get("parent_end_offset")
        if not isinstance(start, int) or not isinstance(end, int):
            raise ValueError(f"{name} offsets missing")
        if name == "Ко" and row.get("argument_count") != 0:
            raise ValueError("Ко invocation acquired unsupported arguments")
        spans.append((start, end, replacement))
    return _replace_spans(source, spans)


def _strip_trailing_category(source: str, *, expected_count: int) -> str:
    matches = tuple(_CATEGORY_LINE_RE.finditer(source))
    if len(matches) != expected_count:
        raise ValueError(f"category inventory drift: expected {expected_count}, got {len(matches)}")
    if not matches:
        return source
    first = matches[0].start()
    suffix = source[first:]
    if _CATEGORY_LINE_RE.sub("", suffix).strip():
        raise ValueError("unsupported content after trailing Klim category block")
    return source[:first].rstrip()


def _plain_heading(match: re.Match[str]) -> str:
    text = match.group("text").strip()
    if not text:
        raise ValueError("empty Klim literary heading")
    return f"\n\n{text}\n\n"


def _protect_nowiki(source: str, *, expected_tag_count: int) -> tuple[str, list[tuple[str, str]]]:
    if expected_tag_count % 2:
        raise ValueError("Klim nowiki tag inventory is not paired")
    protected: list[tuple[str, str]] = []
    marker_prefix = "SCRIPTORIUMKLIMNOWIKITOKEN"
    if marker_prefix in source:
        raise ValueError("nowiki placeholder prefix collides with source")

    def replace(match: re.Match[str]) -> str:
        value = match.group(1)
        if "\n" in value or "\r" in value:
            raise ValueError("multiline nowiki content outside bounded Klim profile")
        token = f"{marker_prefix}{len(protected):04d}END"
        protected.append((token, value))
        return token

    result = _NOWIKI_PAIR_RE.sub(replace, source)
    if _NOWIKI_ANY_RE.search(result):
        raise ValueError("unsupported nowiki shape remains")
    if len(protected) * 2 != expected_tag_count:
        raise ValueError("Klim nowiki pair count drift")
    return result, protected


def _protect_literal_line_openers(source: str) -> tuple[str, list[tuple[str, str]]]:
    """Protect literal line-leading |/! but keep true table delimiters fatal."""
    if _TABLE_OPEN_RE.search(source) or _TABLE_ROW_OR_END_RE.search(source):
        raise ValueError("unsupported Klim table delimiter reached literary extraction")
    marker_prefix = "SCRIPTORIUMKLIMLINEOPENERTOKEN"
    if marker_prefix in source:
        raise ValueError("line-opener placeholder prefix collides with source")
    protected: list[tuple[str, str]] = []

    def replace(match: re.Match[str]) -> str:
        token = f"{marker_prefix}{len(protected):04d}END"
        protected.append((token, match.group("mark")))
        return match.group("indent") + token

    return _LITERAL_LINE_OPENER_RE.sub(replace, source), protected


def _restore_tokens(rendered: str, protected: Sequence[tuple[str, str]], *, label: str) -> str:
    out = rendered
    for token, value in protected:
        if out.count(token) != 1:
            raise ValueError(f"{label} placeholder multiplicity drift")
        out = out.replace(token, value)
    return out


def _extract_part_body(
    source: str,
    *,
    part: int,
    frozen_surface_part: Mapping[str, object],
    direct_poem_part: Mapping[str, object],
) -> tuple[str, dict[str, object]]:
    source, direct_count = _literaryize_direct_poemx1(
        source, part=part, frozen_part=direct_poem_part
    )
    templates = frozen_surface_part.get("template_name_counts")
    tags = frozen_surface_part.get("html_tag_name_counts")
    headings = frozen_surface_part.get("heading_level_counts")
    if not isinstance(templates, Mapping) or not isinstance(tags, Mapping) or not isinstance(headings, Mapping):
        raise ValueError("Klim frozen structural inventories missing")

    source = _replace_named_template(source, "Жизнь Клима Самгина", expected=1, replacement="")
    notes_count = int(templates.get("примечания", 0))
    source = _replace_named_template(source, "примечания", expected=notes_count, replacement="")
    ko_count = int(templates.get("Ко", 0))
    source = _replace_named_template(source, "Ко", expected=ko_count, replacement="Ко")
    if "{{" in source or "}}" in source:
        raise ValueError(f"Klim part {part} retains unsupported template syntax")

    category_count = int(frozen_surface_part.get("category_link_count", 0))
    source = _strip_trailing_category(source, expected_count=category_count)
    level3_count = int(headings.get("3", 0))
    if len(_ANY_HEADING_RE.findall(source)) != level3_count:
        raise ValueError(f"Klim part {part} heading surface drift")
    source = _HEADING3_RE.sub(_plain_heading, source)

    nowiki_tag_count = int(tags.get("nowiki", 0))
    source, protected_nowiki = _protect_nowiki(source, expected_tag_count=nowiki_tag_count)
    source, protected_line_openers = _protect_literal_line_openers(source)
    try:
        rendered = extract_transcription_body(f'<div class="text">{source}</div>')
    except ValueError as exc:
        raise ValueError(f"Klim part {part} conservative renderer rejected prepared source: {exc}") from exc
    rendered = _restore_tokens(rendered, protected_line_openers, label="line-opener")
    body = _restore_tokens(rendered, protected_nowiki, label="nowiki")
    if not body:
        raise ValueError(f"Klim part {part} literary body is empty")
    return body, {
        "direct_parent_poemx1_replacement_count": direct_count,
        "header_template_removal_count": 1,
        "notes_template_removal_count": notes_count,
        "ko_template_plain_replacement_count": ko_count,
        "trailing_category_removal_count": category_count,
        "level_three_heading_plain_replacement_count": level3_count,
        "nowiki_pair_preservation_count": len(protected_nowiki),
        "literal_line_opener_preservation_count": len(protected_line_openers),
    }


def build_manifest(
    revision_manifests: Sequence[Mapping[str, object]],
    dependency_revision_manifest: Mapping[str, object],
    body_surface_manifest: Mapping[str, object],
    direct_poem_manifest: Mapping[str, object],
    lst_contract: Mapping[str, object],
    part2_resolution_manifest: Mapping[str, object],
    *,
    research_date: str,
    fetcher: Callable[..., dict[str, object]] = fetch_pinned_wikitext,
) -> dict[str, object]:
    if len(revision_manifests) != 4:
        raise ValueError("exactly four Klim part revision manifests are required")
    if not research_date:
        raise ValueError("research_date must be non-empty")
    validate_body_surface_manifest(body_surface_manifest)
    validate_direct_manifest(direct_poem_manifest)
    validate_part2_resolution_manifest(part2_resolution_manifest)
    if direct_poem_manifest.get("all_direct_parent_poemx1_plain_value_safe") is not True:
        raise ValueError("all direct parent poemx1 calls must be frozen plain-safe")
    if body_surface_manifest.get("candidate_id") != CANDIDATE_ID:
        raise ValueError("unexpected Klim body-surface candidate")
    if direct_poem_manifest.get("candidate_id") != CANDIDATE_ID:
        raise ValueError("unexpected Klim direct-poem candidate")

    dependency, dependency_identity = _verified_wikitext(
        dependency_revision_manifest,
        expected_candidate=DEPENDENCY_CANDIDATE_ID,
        expected_revision_id=EXPECTED_DEPENDENCY_REVISION_ID,
        fetcher=fetcher,
    )
    source_revisions = part2_resolution_manifest.get("source_revisions")
    if not isinstance(source_revisions, Mapping):
        raise ValueError("Part 2 resolution source revisions missing")
    if dependency_identity.get("wikitext_sha256") != source_revisions.get("dependency_wikitext_sha256"):
        raise ValueError("Part 2 dependency disagrees with frozen resolution graph")
    literary_dependency, dependency_facts = _literaryize_dependency(
        dependency, part2_resolution_manifest
    )

    frozen_surface_parts = body_surface_manifest.get("parts")
    frozen_direct_parts = direct_poem_manifest.get("parts")
    if not isinstance(frozen_surface_parts, list) or not isinstance(frozen_direct_parts, list):
        raise ValueError("Klim frozen per-part surfaces missing")

    part_rows: list[dict[str, object]] = []
    bodies: list[str] = []
    for part, revision_manifest in enumerate(revision_manifests, start=1):
        parent, identity = _verified_wikitext(
            revision_manifest,
            expected_candidate=f"{CANDIDATE_ID}-part-{part}",
            expected_revision_id=EXPECTED_PART_REVISION_IDS[part],
            fetcher=fetcher,
        )
        if part == 2:
            parent = _substitute_part2_dependency(parent, literary_dependency, lst_contract)
        surface_part = frozen_surface_parts[part - 1]
        direct_part = frozen_direct_parts[part - 1]
        if not isinstance(surface_part, Mapping) or not isinstance(direct_part, Mapping):
            raise ValueError("invalid Klim frozen part row")
        body, transforms = _extract_part_body(
            parent,
            part=part,
            frozen_surface_part=surface_part,
            direct_poem_part=direct_part,
        )
        bodies.append(body)
        part_rows.append({
            "part": part,
            "source_revision_id": identity["revision_id"],
            "source_wikitext_sha256": identity["wikitext_sha256"],
            "part2_target_dependency_substituted": part == 2,
            "transforms": transforms,
            "literary_body_identity": _identity(body),
            "source_text_included": False,
        })

    composite = COMPOSITION_SEPARATOR.join(bodies)
    if len(composite) < 300_000:
        raise ValueError("Klim literary composite is below calibration threshold")
    return {
        "manifest_version": MANIFEST_VERSION,
        "candidate_id": CANDIDATE_ID,
        "research_date": research_date,
        "profile": PROFILE_VERSION,
        "evidence_class": "candidate_specific_source_graph_literary_extraction",
        "part2_literary_target_substitution": {
            "dependency_revision_id": dependency_identity["revision_id"],
            "dependency_wikitext_sha256": dependency_identity["wikitext_sha256"],
            **dependency_facts,
            "historical_render_equivalence_proven": False,
        },
        "parts": part_rows,
        "composition": {
            "profile": COMPOSITION_PROFILE,
            "part_order": [1, 2, 3, 4],
            "separator_escape": "\\n\\n",
            "separator_character_count": len(COMPOSITION_SEPARATOR),
            "separator_utf8_byte_count": len(COMPOSITION_SEPARATOR.encode("utf-8")),
            "separator_sha256": _sha256_text(COMPOSITION_SEPARATOR),
            "composite_literary_body_identity": _identity(composite),
        },
        "capture_scope": {
            "four_part_literary_body_extraction_frozen": True,
            "deterministic_four_part_composition_frozen": True,
            "composite_raw_and_normalized_identity_frozen": True,
            "historical_wikisource_mediawiki_core_revision_proven": False,
            "historical_wikisource_poem_deployment_equivalence_proven": False,
            "historical_render_equivalence_proven": False,
            "source_text_committed": False,
        },
        "boundary": (
            "This source-free identity is a deterministic candidate-specific extraction from the "
            "pinned Russian Wikisource/Library Moshkov transcription graph. Frozen poemx1 calls are "
            "replaced by their exact plain parameter-2 values; the Part 2 dependency first receives "
            "the already-frozen noinclude/includeonly/onlyinclude transclusion-control semantics and "
            "is then substituted at the exact frozen #lst span. This does not prove the historical "
            "MediaWiki/Poem deployment or identify FantLab's undisclosed analyzer input."
        ),
        "source_text_included": False,
        "fantlab_source_edition_match": "unknown",
        "diagnostic_ready": True,
        "gate_ready": False,
        "m2_parity_admissible": False,
    }


def _validate_identity(value: object, *, label: str) -> None:
    if not isinstance(value, Mapping):
        raise ValueError(f"{label} identity missing")
    for key in (
        "character_count_including_spaces",
        "utf8_byte_count",
        "normalized_character_count_including_spaces",
    ):
        if not isinstance(value.get(key), int) or int(value[key]) <= 0:
            raise ValueError(f"invalid {label} {key}")
    for key in ("raw_sha256", "normalized_sha256"):
        digest = value.get(key)
        if not isinstance(digest, str) or len(digest) != 64:
            raise ValueError(f"invalid {label} {key}")
    if value.get("normalization_profile") != NORMALIZATION_PROFILE:
        raise ValueError(f"{label} normalization profile drift")


def validate_manifest(manifest: Mapping[str, object]) -> None:
    if manifest.get("manifest_version") != MANIFEST_VERSION:
        raise ValueError("unsupported Klim literary-body manifest")
    if manifest.get("candidate_id") != CANDIDATE_ID or manifest.get("profile") != PROFILE_VERSION:
        raise ValueError("unexpected Klim literary-body identity")
    if manifest.get("evidence_class") != "candidate_specific_source_graph_literary_extraction":
        raise ValueError("Klim literary-body evidence class drift")
    parts = manifest.get("parts")
    if not isinstance(parts, list) or len(parts) != 4:
        raise ValueError("Klim literary-body manifest must contain four parts")
    for part, row_obj in enumerate(parts, start=1):
        if not isinstance(row_obj, Mapping) or row_obj.get("part") != part:
            raise ValueError("Klim literary-body part order drift")
        if row_obj.get("source_revision_id") != EXPECTED_PART_REVISION_IDS[part]:
            raise ValueError(f"Klim part {part} source revision drift")
        _validate_identity(row_obj.get("literary_body_identity"), label=f"part {part}")
        if row_obj.get("source_text_included") is not False:
            raise ValueError("source prose must remain absent")
    composition = manifest.get("composition")
    if not isinstance(composition, Mapping):
        raise ValueError("Klim composition contract missing")
    if composition.get("profile") != COMPOSITION_PROFILE or composition.get("part_order") != [1, 2, 3, 4]:
        raise ValueError("Klim composition order/profile drift")
    if composition.get("separator_escape") != "\\n\\n" or composition.get("separator_sha256") != _sha256_text(COMPOSITION_SEPARATOR):
        raise ValueError("Klim composition separator drift")
    _validate_identity(composition.get("composite_literary_body_identity"), label="composite")
    scope = manifest.get("capture_scope")
    if not isinstance(scope, Mapping):
        raise ValueError("Klim literary-body capture scope missing")
    for key in (
        "four_part_literary_body_extraction_frozen",
        "deterministic_four_part_composition_frozen",
        "composite_raw_and_normalized_identity_frozen",
    ):
        if scope.get(key) is not True:
            raise ValueError(f"{key} must be true")
    for key in (
        "historical_wikisource_mediawiki_core_revision_proven",
        "historical_wikisource_poem_deployment_equivalence_proven",
        "historical_render_equivalence_proven",
        "source_text_committed",
    ):
        if scope.get(key) is not False:
            raise ValueError(f"{key} must remain false")
    if manifest.get("source_text_included") is not False:
        raise ValueError("source prose must remain absent")
    if manifest.get("fantlab_source_edition_match") != "unknown":
        raise ValueError("FantLab source identity must remain unknown")
    if manifest.get("diagnostic_ready") is not True:
        raise ValueError("frozen literary composite should be diagnostic-ready")
    if manifest.get("gate_ready") is not False or manifest.get("m2_parity_admissible") is not False:
        raise ValueError("public-source freeze cannot open M2 gate")
    forbidden = {"wikitext", "content", "body", "text", "source_text"}
    if forbidden.intersection(manifest):
        raise ValueError("source prose key leaked into Klim literary-body manifest")


def replay_manifest(
    revision_manifests: Sequence[Mapping[str, object]],
    dependency_revision_manifest: Mapping[str, object],
    body_surface_manifest: Mapping[str, object],
    direct_poem_manifest: Mapping[str, object],
    lst_contract: Mapping[str, object],
    part2_resolution_manifest: Mapping[str, object],
    manifest: Mapping[str, object],
    *,
    fetcher: Callable[..., dict[str, object]] = fetch_pinned_wikitext,
) -> dict[str, object]:
    validate_manifest(manifest)
    observed = build_manifest(
        revision_manifests,
        dependency_revision_manifest,
        body_surface_manifest,
        direct_poem_manifest,
        lst_contract,
        part2_resolution_manifest,
        research_date=str(manifest["research_date"]),
        fetcher=fetcher,
    )
    if observed != dict(manifest):
        raise ValueError("pinned Klim literary-body identity drift")
    composition = manifest["composition"]
    assert isinstance(composition, Mapping)
    identity = composition["composite_literary_body_identity"]
    assert isinstance(identity, Mapping)
    return {
        "receipt_version": "scriptorium-klim-samgin-literary-body-replay-v1",
        "candidate_id": CANDIDATE_ID,
        "profile": PROFILE_VERSION,
        "raw_sha256": identity["raw_sha256"],
        "normalized_sha256": identity["normalized_sha256"],
        "verified": True,
        "source_text_included": False,
        "fantlab_source_edition_match": "unknown",
        "m2_parity_admissible": False,
    }


def _part_paths(args: argparse.Namespace) -> list[Path]:
    return [getattr(args, f"part{part}_revision_manifest") for part in range(1, 5)]


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Freeze or replay Klim Samgin literary-body identity.")
    sub = parser.add_subparsers(dest="command", required=True)

    def add_sources(command: argparse.ArgumentParser) -> None:
        for part in range(1, 5):
            command.add_argument(f"--part{part}-revision-manifest", type=Path, required=True)
        command.add_argument("--dependency-revision-manifest", type=Path, required=True)
        command.add_argument("--body-surface-manifest", type=Path, required=True)
        command.add_argument("--direct-poemx1-manifest", type=Path, required=True)
        command.add_argument("--lst-contract", type=Path, required=True)
        command.add_argument("--part2-resolution-manifest", type=Path, required=True)

    capture = sub.add_parser("capture")
    add_sources(capture)
    capture.add_argument("--research-date", required=True)
    capture.add_argument("--output", type=Path, required=True)

    replay = sub.add_parser("replay")
    add_sources(replay)
    replay.add_argument("--manifest", type=Path, required=True)
    replay.add_argument("--receipt", type=Path, required=True)

    args = parser.parse_args(argv)
    revisions = [_load_json(path) for path in _part_paths(args)]
    dependency = _load_json(args.dependency_revision_manifest)
    body_surface = _load_json(args.body_surface_manifest)
    direct_poem = _load_json(args.direct_poemx1_manifest)
    lst_contract = _load_json(args.lst_contract)
    part2_resolution = _load_json(args.part2_resolution_manifest)

    if args.command == "capture":
        manifest = build_manifest(
            revisions,
            dependency,
            body_surface,
            direct_poem,
            lst_contract,
            part2_resolution,
            research_date=args.research_date,
        )
        validate_manifest(manifest)
        _write_json(args.output, manifest)
        return 0

    manifest = _load_json(args.manifest)
    receipt = replay_manifest(
        revisions,
        dependency,
        body_surface,
        direct_poem,
        lst_contract,
        part2_resolution,
        manifest,
    )
    _write_json(args.receipt, receipt)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
