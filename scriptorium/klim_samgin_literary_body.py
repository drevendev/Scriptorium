"""Freeze a source-free four-part literary-body identity for Klim Samgin.

The extractor is deliberately candidate-specific.  It replays the exact four pinned
Russian Wikisource parent revisions plus the already-pinned Part 2 target dependency,
revalidates every prerequisite source-free contract, replaces only the seven proven
plain direct-parent ``poemx1`` calls and the six proven plain dependency calls with
their exact parameter-2 literary values, and applies the frozen target-only ``#lst``
whole-target substitution.

The remaining markup policy is intentionally narrow: the four work-header templates
and notes scaffolding are removed, ``{{Ко}}`` is mapped to its visible plain-text
content, references/categories are excluded, literary headings are preserved, and
``nowiki`` contents are protected from accidental wiki re-interpretation.  The
resulting prose exists only in memory; committed evidence contains counts and SHA-256
identities only.  Historical MediaWiki/Poem deployment equivalence and FantLab input
identity remain unproven.
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
from .klim_samgin_direct_poemx1_surface import (
    _branch_is_plain,
    validate_manifest as validate_direct_poemx1_manifest,
)
from .klim_samgin_freeze import validate_lst_contract
from .mediawiki_part2_resolution import validate_part2_resolution_manifest
from .mediawiki_poem_render_surface import _core_sensitive_surface, _poem_branch_surface
from .mediawiki_poemx1_content import _parameter_two_value
from .mediawiki_template_invocation import _matching_brace_end, find_template_invocations
from .single_page_body import _body_identity, extract_transcription_body, fetch_pinned_wikitext
from .single_page_revision import validate_manifest as validate_revision_manifest
from .text import NORMALIZATION_PROFILE, normalize_text


MANIFEST_VERSION = "scriptorium-klim-samgin-literary-body-v1"
EXTRACTION_PROFILE = "scriptorium-klim-samgin-wikisource-body-v1"
COMPOSITION_PROFILE = "scriptorium-klim-samgin-four-part-composite-v1"
DEPENDENCY_CANDIDATE_ID = "gorky-klim-samgin-ru-part-2-part2"
DEPENDENCY_REVISION_ID = 2366546
COMPOSITE_SEPARATOR = "\n\n"
KO_SEMANTICS_URL = "https://ru.wikisource.org/wiki/Шаблон:Ко"

_EXPECTED_NOTES_COUNTS = {1: 0, 2: 1, 3: 1, 4: 0}
_EXPECTED_KO_COUNTS = {1: 1, 2: 0, 3: 0, 4: 0}
_EXPECTED_HEADING_COUNTS = {1: 5, 2: 0, 3: 0, 4: 0}
_HEADER_TEMPLATE = "Жизнь Клима Самгина"
_NOTES_TEMPLATE = "примечания"
_KO_TEMPLATE = "Ко"
_ALLOWED_HTML_TAGS = {
    "b", "big", "br", "center", "em", "i", "nowiki", "ref", "small", "span",
    "strong", "sub", "sup",
}

_TEMPLATE_PREFIX = r"\{\{\s*"
_CATEGORY_LINE_RE = re.compile(
    r"(?mi)^[ \t]*\[\[\s*(?:Категория|Category)\s*:[^\]\n]+\]\][ \t]*$"
)
_HEADING_RE = re.compile(
    r"(?m)^[ \t]*(?P<marks>={2,6})[ \t]*(?P<text>[^\n]*?)[ \t]*(?P=marks)[ \t]*$"
)
_TAG_RE = re.compile(r"</?\s*(?P<name>[A-Za-z][A-Za-z0-9:-]*)\b[^>]*>")
_NOWIKI_PAIR_RE = re.compile(r"<nowiki>(?P<value>.*?)</nowiki\s*>", re.IGNORECASE | re.DOTALL)
_NOWIKI_OPEN_RE = re.compile(r"</?\s*nowiki\b", re.IGNORECASE)


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


def _require_mapping(value: object, *, label: str) -> Mapping[str, object]:
    if not isinstance(value, Mapping):
        raise ValueError(f"{label} must be a mapping")
    return value


def _verified_wikitext(
    revision_manifest: Mapping[str, object],
    *,
    expected_candidate_id: str,
    expected_revision_id: int,
    fetcher: Callable[..., dict[str, object]],
) -> tuple[str, Mapping[str, object]]:
    validate_revision_manifest(revision_manifest)
    if revision_manifest.get("candidate_id") != expected_candidate_id:
        raise ValueError(f"unexpected candidate {revision_manifest.get('candidate_id')!r}")
    identity = _require_mapping(revision_manifest.get("source_identity"), label="source identity")
    if identity.get("revision_id") != expected_revision_id:
        raise ValueError("unexpected pinned revision")
    title = identity.get("title")
    if not isinstance(title, str):
        raise ValueError("pinned revision title missing")
    observed = fetcher(title=title, revision_id=expected_revision_id)
    wikitext = observed.pop("wikitext", None)
    if not isinstance(wikitext, str):
        raise ValueError("transient pinned wikitext missing")
    if observed != dict(identity):
        differing = sorted(
            key for key in set(observed) | set(identity) if observed.get(key) != identity.get(key)
        )
        raise ValueError(f"pinned revision identity drift before literary extraction: {differing}")
    return wikitext, identity


def _raw_template_spans(source: str, template_name: str) -> list[tuple[int, int]]:
    prefix = re.compile(
        _TEMPLATE_PREFIX + re.escape(template_name) + r"(?=\s*[|}])",
        re.IGNORECASE,
    )
    spans: list[tuple[int, int]] = []
    cursor = 0
    while True:
        match = prefix.search(source, cursor)
        if match is None:
            break
        start = match.start()
        end = _matching_brace_end(source, start)
        spans.append((start, end))
        cursor = end
    return spans


def _replace_spans(source: str, replacements: Sequence[tuple[int, int, str]]) -> str:
    previous_start = len(source) + 1
    out = source
    for start, end, replacement in sorted(replacements, reverse=True):
        if not (0 <= start < end <= len(source)):
            raise ValueError("replacement span outside source")
        if end > previous_start:
            raise ValueError("overlapping replacement spans")
        out = out[:start] + replacement + out[end:]
        previous_start = start
    return out


def _plain_poem_value(
    source: str,
    observed: Mapping[str, object],
    *,
    expected_invocation_sha256: object,
    expected_parameter_2_sha256: object,
) -> str:
    if observed.get("invocation_sha256") != expected_invocation_sha256:
        raise ValueError("poemx1 invocation identity drift")
    value, identity = _parameter_two_value(source, observed)
    if identity.get("sha256") != expected_parameter_2_sha256:
        raise ValueError("poemx1 parameter-2 identity drift")
    if not _branch_is_plain(_core_sensitive_surface(value), _poem_branch_surface(value)):
        raise ValueError("previously plain poemx1 value acquired active render syntax")
    return value


def _replace_direct_parent_poemx1(
    source: str,
    *,
    part: int,
    direct_manifest: Mapping[str, object],
) -> tuple[str, int]:
    parts = direct_manifest.get("parts")
    if not isinstance(parts, list) or len(parts) != 4:
        raise ValueError("direct poemx1 manifest part inventory missing")
    frozen_part = _require_mapping(parts[part - 1], label=f"direct poemx1 part {part}")
    frozen_rows = frozen_part.get("invocations")
    expected_count = EXPECTED_DIRECT_POEMX1_COUNTS[part]
    if not isinstance(frozen_rows, list) or len(frozen_rows) != expected_count:
        raise ValueError("direct poemx1 frozen row count drift")
    observed_rows = find_template_invocations(source, template_name="poemx1")
    if len(observed_rows) != expected_count:
        raise ValueError(
            f"Klim part {part} direct poemx1 count drift: {len(observed_rows)}"
        )

    replacements: list[tuple[int, int, str]] = []
    for index, (observed, frozen_obj) in enumerate(zip(observed_rows, frozen_rows), start=1):
        frozen = _require_mapping(frozen_obj, label=f"direct poemx1 row {index}")
        if frozen.get("plain_value_literary_replacement_safe") is not True:
            raise ValueError("direct poemx1 replacement is not frozen plain-safe")
        expected_identity = _require_mapping(
            frozen.get("parameter_2_identity"), label="direct parameter 2 identity"
        )
        value = _plain_poem_value(
            source,
            observed,
            expected_invocation_sha256=frozen.get("invocation_sha256"),
            expected_parameter_2_sha256=expected_identity.get("sha256"),
        )
        start = observed.get("parent_start_offset")
        end = observed.get("parent_end_offset")
        if not isinstance(start, int) or not isinstance(end, int):
            raise ValueError("direct poemx1 offsets missing")
        replacements.append((start, end, value))
    return _replace_spans(source, replacements), len(replacements)


def _resolve_part2_target_to_literary_values(
    parent: str,
    dependency: str,
    *,
    lst_contract: Mapping[str, object],
    part2_resolution_manifest: Mapping[str, object],
) -> tuple[str, dict[str, object]]:
    rows_obj = part2_resolution_manifest.get("poemx1_expansions")
    if not isinstance(rows_obj, list) or len(rows_obj) != 6:
        raise ValueError("Part 2 resolution must retain six poemx1 expansion rows")
    observed_rows = find_template_invocations(dependency, template_name="poemx1")
    if len(observed_rows) != len(rows_obj):
        raise ValueError("Part 2 dependency poemx1 inventory drift")

    replacements: list[tuple[int, int, str]] = []
    for index, (observed, frozen_obj) in enumerate(zip(observed_rows, rows_obj), start=1):
        frozen = _require_mapping(frozen_obj, label=f"Part 2 target poemx1 row {index}")
        value = _plain_poem_value(
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
    literary_dependency = _replace_spans(dependency, replacements)
    if find_template_invocations(literary_dependency, template_name="poemx1"):
        raise ValueError("Part 2 literary dependency retains poemx1")
    if "{{" in literary_dependency or "}}" in literary_dependency:
        raise ValueError("Part 2 literary dependency retains unsupported brace expansion syntax")

    invocation = _require_mapping(lst_contract.get("invocation"), label="Part 2 #lst invocation")
    start = invocation.get("parent_start_offset")
    end = invocation.get("parent_end_offset")
    if not isinstance(start, int) or not isinstance(end, int):
        raise ValueError("Part 2 #lst offsets missing")
    raw_call = parent[start:end]
    if _sha256_text(raw_call) != invocation.get("invocation_sha256"):
        raise ValueError("Part 2 #lst placement drift before literary substitution")
    resolved = parent[:start] + literary_dependency + parent[end:]
    return resolved, {
        "target_poemx1_literary_replacement_count": len(replacements),
        "literary_dependency_character_count": len(literary_dependency),
        "literary_dependency_utf8_byte_count": len(literary_dependency.encode("utf-8")),
        "literary_dependency_sha256": _sha256_text(literary_dependency),
        "target_only_lst_substitution_applied": True,
    }


def _replace_scaffold_template(source: str, template_name: str, replacement: str, expected: int) -> str:
    spans = _raw_template_spans(source, template_name)
    if len(spans) != expected:
        raise ValueError(
            f"expected {expected} {template_name!r} scaffold invocation(s), observed {len(spans)}"
        )
    return _replace_spans(source, [(start, end, replacement) for start, end in spans])


def _protect_nowiki(source: str) -> tuple[str, dict[str, str]]:
    values: dict[str, str] = {}

    def repl(match: re.Match[str]) -> str:
        value = match.group("value")
        if "\r" in value or "\n" in value:
            raise ValueError("multiline nowiki is outside the Klim literary extraction profile")
        token = f"SCRIPTORIUMNOWIKI{len(values):04d}TOKEN"
        if token in source:
            raise ValueError("nowiki protection token collides with source")
        values[token] = value
        return token

    protected = _NOWIKI_PAIR_RE.sub(repl, source)
    if _NOWIKI_OPEN_RE.search(protected):
        raise ValueError("unpaired or unsupported nowiki tag remains")
    return protected, values


def _plain_heading(match: re.Match[str]) -> str:
    text = match.group("text").strip()
    if not text:
        raise ValueError("empty literary heading")
    return f"\n\n{text}\n\n"


def _extract_part_literary_body(
    source: str,
    *,
    part: int,
    expected_parent_category_count: int,
) -> tuple[str, dict[str, object]]:
    source = _replace_scaffold_template(source, _HEADER_TEMPLATE, "", 1)
    source = _replace_scaffold_template(
        source, _NOTES_TEMPLATE, "", _EXPECTED_NOTES_COUNTS[part]
    )
    source = _replace_scaffold_template(source, _KO_TEMPLATE, "Ко", _EXPECTED_KO_COUNTS[part])
    if "{{" in source or "}}" in source:
        raise ValueError(f"Klim part {part} retains unsupported template syntax after scaffold removal")

    category_matches = tuple(_CATEGORY_LINE_RE.finditer(source))
    if len(category_matches) != expected_parent_category_count:
        raise ValueError(
            f"Klim part {part} category inventory drift after expansion: {len(category_matches)}"
        )
    source = _CATEGORY_LINE_RE.sub("", source)

    headings = tuple(_HEADING_RE.finditer(source))
    if len(headings) != _EXPECTED_HEADING_COUNTS[part]:
        raise ValueError(
            f"Klim part {part} literary heading inventory drift: {len(headings)}"
        )
    source = _HEADING_RE.sub(_plain_heading, source)

    tag_names = [match.group("name").casefold() for match in _TAG_RE.finditer(source)]
    unsupported_tags = sorted(set(tag_names) - _ALLOWED_HTML_TAGS)
    if unsupported_tags:
        raise ValueError(f"unsupported Klim part {part} HTML tags: {unsupported_tags}")
    protected, nowiki_values = _protect_nowiki(source)
    rendered = extract_transcription_body(f'<div class="text">{protected}</div>')
    for token, value in nowiki_values.items():
        if token not in rendered:
            raise ValueError("nowiki protection token was lost during extraction")
        rendered = rendered.replace(token, value)
    if "SCRIPTORIUMNOWIKI" in rendered:
        raise ValueError("nowiki protection token leaked into literary body")
    if not rendered:
        raise ValueError("empty Klim literary part")
    return rendered, {
        "category_count_removed": len(category_matches),
        "heading_count_preserved": len(headings),
        "nowiki_pair_count_preserved": len(nowiki_values),
        "observed_html_tag_name_counts": {
            name: tag_names.count(name) for name in sorted(set(tag_names))
        },
    }


def _source_projection(identity: Mapping[str, object]) -> dict[str, object]:
    return {
        key: identity[key]
        for key in (
            "title", "page_id", "revision_id", "revision_timestamp", "mediawiki_sha1",
            "wikitext_sha256",
        )
    }


def build_manifest(
    revision_manifests: Sequence[Mapping[str, object]],
    dependency_revision_manifest: Mapping[str, object],
    body_surface_manifest: Mapping[str, object],
    direct_poemx1_manifest: Mapping[str, object],
    lst_contract: Mapping[str, object],
    part2_resolution_manifest: Mapping[str, object],
    *,
    research_date: str,
    fetcher: Callable[..., dict[str, object]] = fetch_pinned_wikitext,
) -> dict[str, object]:
    if len(revision_manifests) != 4:
        raise ValueError("exactly four Klim parent revision manifests are required")
    if not isinstance(research_date, str) or not research_date:
        raise ValueError("research_date must be non-empty")
    validate_body_surface_manifest(body_surface_manifest)
    validate_direct_poemx1_manifest(direct_poemx1_manifest)
    validate_part2_resolution_manifest(part2_resolution_manifest)
    validate_revision_manifest(dependency_revision_manifest)
    if dependency_revision_manifest.get("candidate_id") != DEPENDENCY_CANDIDATE_ID:
        raise ValueError("unexpected Part 2 dependency candidate")
    validate_lst_contract(
        lst_contract,
        parent_revision_manifest=revision_manifests[1],
        dependency_revision_manifest=dependency_revision_manifest,
    )

    live_parts: list[str] = []
    identities: list[Mapping[str, object]] = []
    for part, revision_manifest in enumerate(revision_manifests, start=1):
        source, identity = _verified_wikitext(
            revision_manifest,
            expected_candidate_id=f"{CANDIDATE_ID}-part-{part}",
            expected_revision_id=EXPECTED_PART_REVISION_IDS[part],
            fetcher=fetcher,
        )
        live_parts.append(source)
        identities.append(identity)

    dependency, dependency_identity = _verified_wikitext(
        dependency_revision_manifest,
        expected_candidate_id=DEPENDENCY_CANDIDATE_ID,
        expected_revision_id=DEPENDENCY_REVISION_ID,
        fetcher=fetcher,
    )
    source_revisions = _require_mapping(
        part2_resolution_manifest.get("source_revisions"), label="Part 2 resolution revisions"
    )
    if source_revisions.get("dependency_wikitext_sha256") != dependency_identity.get(
        "wikitext_sha256"
    ):
        raise ValueError("Part 2 resolution/dependency revision identity drift")

    resolved_part2, part2_expansion = _resolve_part2_target_to_literary_values(
        live_parts[1],
        dependency,
        lst_contract=lst_contract,
        part2_resolution_manifest=part2_resolution_manifest,
    )
    live_parts[1] = resolved_part2

    body_surface_parts = body_surface_manifest.get("parts")
    if not isinstance(body_surface_parts, list) or len(body_surface_parts) != 4:
        raise ValueError("body surface part inventory missing")

    part_rows: list[dict[str, object]] = []
    bodies: list[str] = []
    for part, (source, identity, surface_obj) in enumerate(
        zip(live_parts, identities, body_surface_parts), start=1
    ):
        surface = _require_mapping(surface_obj, label=f"body surface part {part}")
        source, direct_count = _replace_direct_parent_poemx1(
            source,
            part=part,
            direct_manifest=direct_poemx1_manifest,
        )
        category_count = surface.get("category_link_count")
        if not isinstance(category_count, int):
            raise ValueError("body surface category count missing")
        body, extraction_surface = _extract_part_literary_body(
            source,
            part=part,
            expected_parent_category_count=category_count,
        )
        bodies.append(body)
        part_rows.append(
            {
                "part": part,
                "source_revision": _source_projection(identity),
                "direct_parent_poemx1_literary_replacement_count": direct_count,
                "target_only_part2_literary_substitution_applied": part == 2,
                "extraction_surface": extraction_surface,
                "literary_body_identity": _body_identity(body),
                "source_text_included": False,
            }
        )

    composite = COMPOSITE_SEPARATOR.join(bodies)
    if len(composite) < 300_000:
        raise ValueError("Klim composite literary body is below the corpus threshold")
    composite_identity = _body_identity(composite)
    normalized = normalize_text(composite)
    if composite_identity.get("normalization_profile") != NORMALIZATION_PROFILE:
        raise AssertionError("normalization profile mismatch")
    if composite_identity.get("normalized_sha256") != _sha256_text(normalized):
        raise AssertionError("normalized composite identity mismatch")

    return {
        "manifest_version": MANIFEST_VERSION,
        "candidate_id": CANDIDATE_ID,
        "research_date": research_date,
        "provider": "Russian Wikisource",
        "evidence_class": "candidate_specific_inferred_reconstruction",
        "extraction_profile": EXTRACTION_PROFILE,
        "composition": {
            "profile": COMPOSITION_PROFILE,
            "part_order": [1, 2, 3, 4],
            "separator": "\\n\\n",
            "source_text_committed": False,
        },
        "part2_literary_expansion": part2_expansion,
        "parts": part_rows,
        "composite_identity": composite_identity,
        "semantics_evidence": [
            {
                "url": KO_SEMANTICS_URL,
                "claim": (
                    "Russian Wikisource documents {{Ко}} as the abbreviation for 'и компания'; "
                    "the literary extractor preserves its visible plain-text content as 'Ко' while "
                    "discarding superscript presentation formatting"
                ),
            }
        ],
        "capture_scope": {
            "four_exact_parent_revisions_replayed": True,
            "part2_exact_dependency_revision_replayed": True,
            "target_only_part2_literary_substitution_applied": True,
            "thirteen_poemx1_plain_values_revalidated_and_inserted": True,
            "four_part_literary_body_extraction_frozen": True,
            "four_part_composition_frozen": True,
            "composite_raw_and_normalized_identities_frozen": True,
            "historical_wikisource_mediawiki_core_revision_proven": False,
            "historical_wikisource_poem_deployment_equivalence_proven": False,
            "historical_render_equivalence_proven": False,
            "source_text_committed": False,
        },
        "boundary": (
            "This source-free artifact freezes a candidate-specific literary-body reconstruction "
            "from the exact pinned source graph. The six dependency and seven direct-parent poemx1 "
            "calls are replaced only with their independently frozen plain parameter-2 literary "
            "values; presentation wrappers are intentionally excluded from text analysis. Exact "
            "historical Russian Wikisource MediaWiki/Poem deployment equivalence is not proven. "
            "FantLab analyzer-input identity remains unknown, so this artifact opens only diagnostic "
            "comparison and cannot advance M2 by itself."
        ),
        "source_text_included": False,
        "fantlab_source_edition_match": "unknown",
        "diagnostic_ready": True,
        "gate_ready": False,
        "m2_parity_admissible": False,
    }


def validate_manifest(manifest: Mapping[str, object]) -> None:
    if manifest.get("manifest_version") != MANIFEST_VERSION:
        raise ValueError("unsupported Klim literary-body manifest")
    if manifest.get("candidate_id") != CANDIDATE_ID:
        raise ValueError("unexpected Klim literary-body candidate")
    if manifest.get("evidence_class") != "candidate_specific_inferred_reconstruction":
        raise ValueError("Klim literary-body evidence class drift")
    if manifest.get("extraction_profile") != EXTRACTION_PROFILE:
        raise ValueError("Klim literary-body extraction profile drift")
    composition = _require_mapping(manifest.get("composition"), label="composition")
    if composition != {
        "profile": COMPOSITION_PROFILE,
        "part_order": [1, 2, 3, 4],
        "separator": "\\n\\n",
        "source_text_committed": False,
    }:
        raise ValueError("Klim four-part composition contract drift")

    parts = manifest.get("parts")
    if not isinstance(parts, list) or len(parts) != 4:
        raise ValueError("Klim literary-body manifest must contain four parts")
    for part, row_obj in enumerate(parts, start=1):
        row = _require_mapping(row_obj, label=f"part {part}")
        if row.get("part") != part:
            raise ValueError("Klim literary-body part order drift")
        source = _require_mapping(row.get("source_revision"), label=f"part {part} source")
        if source.get("revision_id") != EXPECTED_PART_REVISION_IDS[part]:
            raise ValueError(f"Klim part {part} source revision drift")
        if row.get("direct_parent_poemx1_literary_replacement_count") != EXPECTED_DIRECT_POEMX1_COUNTS[part]:
            raise ValueError(f"Klim part {part} direct poemx1 replacement count drift")
        if row.get("target_only_part2_literary_substitution_applied") is not (part == 2):
            raise ValueError("Klim Part 2 substitution flag drift")
        identity = _require_mapping(row.get("literary_body_identity"), label=f"part {part} body identity")
        for key in (
            "character_count_including_spaces", "utf8_byte_count",
            "normalized_character_count_including_spaces",
        ):
            if not isinstance(identity.get(key), int) or int(identity[key]) <= 0:
                raise ValueError(f"invalid Klim part {part} {key}")
        for key in ("raw_sha256", "normalized_sha256"):
            digest = identity.get(key)
            if not isinstance(digest, str) or len(digest) != 64:
                raise ValueError(f"invalid Klim part {part} {key}")
        if identity.get("normalization_profile") != NORMALIZATION_PROFILE:
            raise ValueError("Klim part normalization profile drift")
        if row.get("source_text_included") is not False:
            raise ValueError("Klim source text flag must remain false")

    composite = _require_mapping(manifest.get("composite_identity"), label="composite identity")
    if int(composite.get("character_count_including_spaces", 0)) < 300_000:
        raise ValueError("Klim composite body fell below corpus threshold")
    for key in ("raw_sha256", "normalized_sha256"):
        digest = composite.get(key)
        if not isinstance(digest, str) or len(digest) != 64:
            raise ValueError(f"invalid Klim composite {key}")
    if composite.get("normalization_profile") != NORMALIZATION_PROFILE:
        raise ValueError("Klim composite normalization profile drift")

    scope = _require_mapping(manifest.get("capture_scope"), label="capture scope")
    for key in (
        "four_exact_parent_revisions_replayed",
        "part2_exact_dependency_revision_replayed",
        "target_only_part2_literary_substitution_applied",
        "thirteen_poemx1_plain_values_revalidated_and_inserted",
        "four_part_literary_body_extraction_frozen",
        "four_part_composition_frozen",
        "composite_raw_and_normalized_identities_frozen",
    ):
        if scope.get(key) is not True:
            raise ValueError(f"Klim capture scope missing {key}")
    for key in (
        "historical_wikisource_mediawiki_core_revision_proven",
        "historical_wikisource_poem_deployment_equivalence_proven",
        "historical_render_equivalence_proven",
        "source_text_committed",
    ):
        if scope.get(key) is not False:
            raise ValueError(f"Klim capture scope must keep {key}=false")
    if manifest.get("source_text_included") is not False:
        raise ValueError("source text must not be persisted")
    if manifest.get("fantlab_source_edition_match") != "unknown":
        raise ValueError("FantLab source identity must remain unknown")
    if manifest.get("diagnostic_ready") is not True:
        raise ValueError("frozen Klim body should open diagnostic comparison")
    if manifest.get("gate_ready") is not False or manifest.get("m2_parity_admissible") is not False:
        raise ValueError("Klim body freeze cannot advance M2")
    forbidden = {"wikitext", "content", "body", "text", "source_text"}
    if forbidden.intersection(manifest):
        raise ValueError("source prose key leaked into Klim literary-body manifest")


def replay_manifest(
    revision_manifests: Sequence[Mapping[str, object]],
    dependency_revision_manifest: Mapping[str, object],
    body_surface_manifest: Mapping[str, object],
    direct_poemx1_manifest: Mapping[str, object],
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
        direct_poemx1_manifest,
        lst_contract,
        part2_resolution_manifest,
        research_date=str(manifest["research_date"]),
        fetcher=fetcher,
    )
    if observed != dict(manifest):
        raise ValueError("pinned Klim four-part literary-body identity drift")
    composite = _require_mapping(manifest["composite_identity"], label="composite identity")
    return {
        "receipt_version": "scriptorium-klim-samgin-literary-body-replay-v1",
        "candidate_id": CANDIDATE_ID,
        "extraction_profile": EXTRACTION_PROFILE,
        "composition_profile": COMPOSITION_PROFILE,
        "raw_sha256": composite["raw_sha256"],
        "normalized_sha256": composite["normalized_sha256"],
        "verified": True,
        "source_text_included": False,
        "fantlab_source_edition_match": "unknown",
        "m2_parity_admissible": False,
    }


def _revision_args(parser: argparse.ArgumentParser) -> None:
    for part in range(1, 5):
        parser.add_argument(f"--part{part}-revision-manifest", type=Path, required=True)
    parser.add_argument("--dependency-revision-manifest", type=Path, required=True)
    parser.add_argument("--body-surface-manifest", type=Path, required=True)
    parser.add_argument("--direct-poemx1-manifest", type=Path, required=True)
    parser.add_argument("--lst-contract", type=Path, required=True)
    parser.add_argument("--part2-resolution-manifest", type=Path, required=True)


def _inputs(args: argparse.Namespace) -> tuple[list[dict[str, object]], dict[str, object], dict[str, object], dict[str, object], dict[str, object], dict[str, object]]:
    revisions = [
        _load_json(getattr(args, f"part{part}_revision_manifest")) for part in range(1, 5)
    ]
    return (
        revisions,
        _load_json(args.dependency_revision_manifest),
        _load_json(args.body_surface_manifest),
        _load_json(args.direct_poemx1_manifest),
        _load_json(args.lst_contract),
        _load_json(args.part2_resolution_manifest),
    )


def main(argv: Sequence[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Freeze or replay Klim Samgin four-part literary-body identity.")
    subparsers = parser.add_subparsers(dest="command", required=True)
    capture = subparsers.add_parser("capture")
    _revision_args(capture)
    capture.add_argument("--research-date", required=True)
    capture.add_argument("--output", type=Path, required=True)
    replay = subparsers.add_parser("replay")
    _revision_args(replay)
    replay.add_argument("--manifest", type=Path, required=True)
    replay.add_argument("--receipt", type=Path, required=True)
    args = parser.parse_args(argv)
    revisions, dependency, body_surface, direct, lst, part2_resolution = _inputs(args)
    if args.command == "capture":
        manifest = build_manifest(
            revisions, dependency, body_surface, direct, lst, part2_resolution,
            research_date=args.research_date,
        )
        validate_manifest(manifest)
        _write_json(args.output, manifest)
        return 0
    manifest = _load_json(args.manifest)
    receipt = replay_manifest(
        revisions, dependency, body_surface, direct, lst, part2_resolution, manifest
    )
    _write_json(args.receipt, receipt)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
