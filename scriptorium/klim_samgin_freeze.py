"""Source-free source-shape and target-only #lst contract for Klim Samgin.

Part 2 of the retained Russian Wikisource transcription contains exactly one
``#lst`` invocation. Research against the current upstream Wikimedia
LabeledSectionTransclusion implementation established an important edge case:
when ``#lst`` is called with only the target page argument, the extension does
*not* select a labeled section. After resolving the target it returns
``$newFrame->expand($root)`` for the whole target template DOM.

This module freezes only the evidence Scriptorium can reproduce without running
MediaWiki itself: the exact target-only invocation and its parent offsets, the
pinned target revision, the observed absence/presence inventory of section and
transclusion markup, and the upstream semantic branch. It deliberately does
not manufacture an expanded Part 2 byte identity; that remains a later source-
graph/parser-expansion problem.
"""

from __future__ import annotations

import argparse
from collections import Counter
from hashlib import sha256
import json
from pathlib import Path
import re
from typing import Callable, Mapping, Sequence

from .single_page_body import fetch_pinned_wikitext
from .single_page_revision import validate_manifest as validate_revision_manifest


PART2_CANDIDATE_ID = "gorky-klim-samgin-ru-part-2"
DEPENDENCY_CANDIDATE_ID = "gorky-klim-samgin-ru-part-2-part2"
DEPENDENCY_TITLE = "Жизнь Клима Самгина (Горький)/Часть 2/part2"
LST_CONTRACT_VERSION = "scriptorium-klim-samgin-lst-contract-v2"
LST_SELECTION_PROFILE = "scriptorium-klim-samgin-part2-target-only-lst-v1"
UPSTREAM_IMPLEMENTATION = "wikimedia/mediawiki-extensions-LabeledSectionTransclusion"
UPSTREAM_IMPLEMENTATION_PATH = "includes/LabeledSectionTransclusion.php"
UPSTREAM_EVIDENCE_COMMIT = "3e9a44dec6858aeaf3ca547a32ab3162d6887ed6"

_TEMPLATE_NAME_RE = re.compile(r"\{\{\s*([^|{}\n]+)")
_HTML_TAG_NAME_RE = re.compile(r"</?\s*([A-Za-z][A-Za-z0-9]*)\b")
_HEADING_RE = re.compile(r"(?m)^(={2,6})\s*.*?\s*\1\s*$")
_CATEGORY_RE = re.compile(r"(?mi)^\s*\[\[\s*(?:Категория|Category)\s*:")
_LST_PREFIX_RE = re.compile(r"\{\{\s*#lst\s*:", re.IGNORECASE)
_TARGET_ONLY_LST_RE = re.compile(
    r"\{\{\s*#lst\s*:\s*(?P<target>[^|{}\n]+?)\s*\}\}", re.IGNORECASE
)
_ANY_SECTION_TAG_RE = re.compile(r"<section\b", re.IGNORECASE)


def _load_json(path: Path) -> dict[str, object]:
    value = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(value, dict):
        raise ValueError("manifest must be a JSON object")
    return value


def _write_json(path: Path, value: Mapping[str, object]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def _sha256_text(value: str) -> str:
    return sha256(value.encode("utf-8")).hexdigest()


def _verified_wikitext(
    revision_manifest: Mapping[str, object],
    *,
    fetcher: Callable[..., dict[str, object]],
) -> str:
    validate_revision_manifest(revision_manifest)
    source_identity = revision_manifest.get("source_identity")
    assert isinstance(source_identity, dict)
    title = source_identity.get("title")
    revision_id = source_identity.get("revision_id")
    if not isinstance(title, str) or not isinstance(revision_id, int):
        raise ValueError("revision manifest source identity incomplete")
    observed = fetcher(title=title, revision_id=revision_id)
    wikitext = observed.pop("wikitext", None)
    if not isinstance(wikitext, str):
        raise ValueError("transient source prose missing")
    if observed != source_identity:
        differing = sorted(
            key for key in set(observed) | set(source_identity)
            if observed.get(key) != source_identity.get(key)
        )
        raise ValueError(f"pinned revision identity drift before #lst analysis: {differing}")
    return wikitext


def parse_target_only_lst_invocation(wikitext: str) -> dict[str, object]:
    """Require exactly one target-only #lst call and return source-free placement."""
    if not isinstance(wikitext, str):
        raise TypeError("wikitext must be str")
    matches = tuple(_TARGET_ONLY_LST_RE.finditer(wikitext))
    prefix_count = len(tuple(_LST_PREFIX_RE.finditer(wikitext)))
    if prefix_count != 1:
        raise ValueError(f"expected exactly one #lst invocation, observed {prefix_count}")
    if len(matches) != 1:
        raise ValueError("Klim Samgin Part 2 #lst is not the frozen target-only shape")
    match = matches[0]
    target = match.group("target").strip()
    if not target:
        raise ValueError("#lst target must be non-empty")
    raw_call = match.group(0)
    return {
        "argument_count": 1,
        "target_title": target,
        "section_label": None,
        "range_end_label": None,
        "parent_start_offset": match.start(),
        "parent_end_offset": match.end(),
        "invocation_character_count": len(raw_call),
        "invocation_utf8_byte_count": len(raw_call.encode("utf-8")),
        "invocation_sha256": _sha256_text(raw_call),
    }


def _source_revision_projection(manifest: Mapping[str, object]) -> dict[str, object]:
    identity = manifest.get("source_identity")
    assert isinstance(identity, dict)
    return {
        key: identity[key]
        for key in (
            "title", "page_id", "revision_id", "revision_timestamp",
            "mediawiki_sha1", "wikitext_character_count",
            "wikitext_utf8_byte_count", "wikitext_sha256",
        )
    }


def _dependency_shape(wikitext: str) -> dict[str, object]:
    template_names = Counter(m.group(1).strip() for m in _TEMPLATE_NAME_RE.finditer(wikitext))
    lst_count = len(tuple(_LST_PREFIX_RE.finditer(wikitext)))
    return {
        "section_tag_count": len(tuple(_ANY_SECTION_TAG_RE.finditer(wikitext))),
        "lst_invocation_count": lst_count,
        "template_name_counts": dict(sorted(template_names.items())),
    }


def build_lst_contract(
    parent_revision_manifest: Mapping[str, object],
    dependency_revision_manifest: Mapping[str, object],
    *,
    fetcher: Callable[..., dict[str, object]] = fetch_pinned_wikitext,
) -> dict[str, object]:
    """Freeze exact target-only invocation semantics without faking parser output."""
    validate_revision_manifest(parent_revision_manifest)
    validate_revision_manifest(dependency_revision_manifest)
    if parent_revision_manifest.get("candidate_id") != PART2_CANDIDATE_ID:
        raise ValueError("unexpected Klim Samgin Part 2 candidate")
    if dependency_revision_manifest.get("candidate_id") != DEPENDENCY_CANDIDATE_ID:
        raise ValueError("unexpected Klim Samgin dependency candidate")
    dependency_identity = dependency_revision_manifest.get("source_identity")
    assert isinstance(dependency_identity, dict)
    if dependency_identity.get("title") != DEPENDENCY_TITLE:
        raise ValueError("unexpected Klim Samgin #lst dependency title")

    parent_wikitext = _verified_wikitext(parent_revision_manifest, fetcher=fetcher)
    dependency_wikitext = _verified_wikitext(dependency_revision_manifest, fetcher=fetcher)
    invocation = parse_target_only_lst_invocation(parent_wikitext)
    if invocation["target_title"] != DEPENDENCY_TITLE:
        raise ValueError("Part 2 #lst target does not match pinned dependency")

    shape = _dependency_shape(dependency_wikitext)
    return {
        "contract_version": LST_CONTRACT_VERSION,
        "candidate_id": "gorky-klim-samgin-ru",
        "selection_profile": LST_SELECTION_PROFILE,
        "parent_revision": _source_revision_projection(parent_revision_manifest),
        "dependency_revision": _source_revision_projection(dependency_revision_manifest),
        "invocation": invocation,
        "dependency_shape": shape,
        "selection_semantics": {
            "kind": "target_only_full_template_dom_expansion",
            "labeled_section_filtering_applied": False,
            "upstream_behavior": "after target resolution, zero remaining args returns newFrame->expand(root)",
            "upstream_repository": UPSTREAM_IMPLEMENTATION,
            "upstream_path": UPSTREAM_IMPLEMENTATION_PATH,
            "upstream_evidence_commit": UPSTREAM_EVIDENCE_COMMIT,
            "upstream_source_url": (
                "https://github.com/wikimedia/mediawiki-extensions-LabeledSectionTransclusion/"
                f"blob/{UPSTREAM_EVIDENCE_COMMIT}/{UPSTREAM_IMPLEMENTATION_PATH}"
            ),
        },
        "capture_scope": {
            "lst_invocation_shape_frozen": True,
            "lst_target_revision_frozen": True,
            "lst_selection_semantics_frozen": True,
            "lst_parent_placement_frozen": True,
            "mediawiki_template_dom_expansion_reproduced": False,
            "resolved_part2_wikitext_identity_frozen": False,
            "literary_body_extraction_frozen": False,
            "composite_literary_body_identity_frozen": False,
            "source_text_committed": False,
        },
        "boundary": (
            "The invocation selects no label. Upstream LabeledSectionTransclusion delegates the whole "
            "target template DOM to MediaWiki frame expansion when only the target argument is present. "
            "Scriptorium has not yet reproduced that MediaWiki expansion or any transitive template/parser "
            "dependencies, so no resolved Part 2 or literary-body digest is claimed."
        ),
        "fantlab_source_edition_match": "unknown",
        "diagnostic_ready": False,
        "gate_ready": False,
        "m2_parity_admissible": False,
    }


def validate_lst_contract(
    contract: Mapping[str, object],
    *,
    parent_revision_manifest: Mapping[str, object] | None = None,
    dependency_revision_manifest: Mapping[str, object] | None = None,
) -> None:
    if contract.get("contract_version") != LST_CONTRACT_VERSION:
        raise ValueError("unsupported Klim Samgin #lst contract version")
    if contract.get("candidate_id") != "gorky-klim-samgin-ru":
        raise ValueError("unexpected Klim Samgin contract candidate")
    if contract.get("selection_profile") != LST_SELECTION_PROFILE:
        raise ValueError("Klim Samgin selection profile drift")
    invocation = contract.get("invocation")
    if not isinstance(invocation, dict):
        raise ValueError("Klim Samgin invocation missing")
    if invocation.get("argument_count") != 1:
        raise ValueError("Klim Samgin invocation must remain target-only")
    if invocation.get("target_title") != DEPENDENCY_TITLE:
        raise ValueError("Klim Samgin target drift")
    if invocation.get("section_label") is not None or invocation.get("range_end_label") is not None:
        raise ValueError("Klim Samgin target-only invocation acquired section arguments")
    start = invocation.get("parent_start_offset")
    end = invocation.get("parent_end_offset")
    if not isinstance(start, int) or not isinstance(end, int) or start < 0 or end <= start:
        raise ValueError("invalid Klim Samgin #lst parent placement")
    for key in ("invocation_character_count", "invocation_utf8_byte_count"):
        if not isinstance(invocation.get(key), int) or int(invocation[key]) <= 0:
            raise ValueError(f"invalid {key}")
    digest = invocation.get("invocation_sha256")
    if not isinstance(digest, str) or len(digest) != 64:
        raise ValueError("invalid invocation SHA-256")

    semantics = contract.get("selection_semantics")
    if not isinstance(semantics, dict):
        raise ValueError("selection semantics missing")
    if semantics.get("kind") != "target_only_full_template_dom_expansion":
        raise ValueError("Klim Samgin target-only semantics drift")
    if semantics.get("labeled_section_filtering_applied") is not False:
        raise ValueError("target-only #lst must not claim labeled-section filtering")
    if semantics.get("upstream_evidence_commit") != UPSTREAM_EVIDENCE_COMMIT:
        raise ValueError("upstream semantics evidence drift")

    shape = contract.get("dependency_shape")
    if not isinstance(shape, dict):
        raise ValueError("dependency shape missing")
    for key in ("section_tag_count", "lst_invocation_count"):
        if not isinstance(shape.get(key), int) or int(shape[key]) < 0:
            raise ValueError(f"invalid dependency shape {key}")
    if not isinstance(shape.get("template_name_counts"), dict):
        raise ValueError("dependency template inventory missing")

    expected_scope = {
        "lst_invocation_shape_frozen": True,
        "lst_target_revision_frozen": True,
        "lst_selection_semantics_frozen": True,
        "lst_parent_placement_frozen": True,
        "mediawiki_template_dom_expansion_reproduced": False,
        "resolved_part2_wikitext_identity_frozen": False,
        "literary_body_extraction_frozen": False,
        "composite_literary_body_identity_frozen": False,
        "source_text_committed": False,
    }
    if contract.get("capture_scope") != expected_scope:
        raise ValueError("Klim Samgin contract capture scope drift")
    if contract.get("fantlab_source_edition_match") != "unknown":
        raise ValueError("FantLab source identity must remain unknown")
    if contract.get("diagnostic_ready") is not False or contract.get("gate_ready") is not False:
        raise ValueError("Klim Samgin diagnostics/gate must remain disabled")
    if contract.get("m2_parity_admissible") is not False:
        raise ValueError("target-only #lst evidence cannot advance M2")

    forbidden = {"wikitext", "content", "body", "text", "source_text"}
    if forbidden.intersection(contract):
        raise ValueError("source prose leaked into Klim Samgin contract")
    if parent_revision_manifest is not None:
        validate_revision_manifest(parent_revision_manifest)
        if contract.get("parent_revision") != _source_revision_projection(parent_revision_manifest):
            raise ValueError("parent revision identity drift")
    if dependency_revision_manifest is not None:
        validate_revision_manifest(dependency_revision_manifest)
        if contract.get("dependency_revision") != _source_revision_projection(dependency_revision_manifest):
            raise ValueError("dependency revision identity drift")


def replay_lst_contract(
    parent_revision_manifest: Mapping[str, object],
    dependency_revision_manifest: Mapping[str, object],
    contract: Mapping[str, object],
    *,
    fetcher: Callable[..., dict[str, object]] = fetch_pinned_wikitext,
) -> dict[str, object]:
    validate_lst_contract(
        contract,
        parent_revision_manifest=parent_revision_manifest,
        dependency_revision_manifest=dependency_revision_manifest,
    )
    observed = build_lst_contract(parent_revision_manifest, dependency_revision_manifest, fetcher=fetcher)
    if observed != contract:
        raise ValueError("pinned Klim Samgin target-only #lst contract drift")
    invocation = contract["invocation"]
    assert isinstance(invocation, dict)
    return {
        "receipt_version": "scriptorium-klim-samgin-lst-replay-v2",
        "candidate_id": contract["candidate_id"],
        "selection_profile": LST_SELECTION_PROFILE,
        "target_title": invocation["target_title"],
        "invocation_sha256": invocation["invocation_sha256"],
        "verified": True,
        "source_text_included": False,
        "resolved_part2_wikitext_identity_frozen": False,
        "fantlab_source_edition_match": "unknown",
        "m2_parity_admissible": False,
    }


def probe_revision_shape(revision_manifest: Mapping[str, object]) -> dict[str, object]:
    """Return source-free markup/dependency inventory for one pinned revision."""
    wikitext = _verified_wikitext(revision_manifest, fetcher=fetch_pinned_wikitext)
    source_identity = revision_manifest.get("source_identity")
    assert isinstance(source_identity, dict)
    templates = Counter(match.group(1).strip() for match in _TEMPLATE_NAME_RE.finditer(wikitext))
    html_tags = Counter(match.group(1).lower() for match in _HTML_TAG_NAME_RE.finditer(wikitext))
    heading_levels = Counter(len(match.group(1)) for match in _HEADING_RE.finditer(wikitext))
    nonempty_lines = [line.strip() for line in wikitext.splitlines() if line.strip()]

    def line_class(line: str) -> str:
        if line.startswith("{{"):
            return "template"
        if line.startswith("[[") and ":" in line:
            return "wikilink_or_category"
        if re.match(r"^={2,6}", line):
            return "heading"
        if line.startswith("<"):
            return "html"
        return "content_or_markup"

    invocation = None
    if _LST_PREFIX_RE.search(wikitext):
        try:
            invocation = parse_target_only_lst_invocation(wikitext)
        except ValueError:
            invocation = {"shape": "non_target_only_or_multiple", "source_text_included": False}
    return {
        "probe_version": "scriptorium-klim-samgin-shape-probe-v3",
        "candidate_id": revision_manifest["candidate_id"],
        "revision_id": source_identity["revision_id"],
        "wikitext_character_count": len(wikitext),
        "line_count": len(wikitext.splitlines()),
        "nonempty_line_count": len(nonempty_lines),
        "template_names": dict(sorted(templates.items())),
        "lst_invocation_count": len(tuple(_LST_PREFIX_RE.finditer(wikitext))),
        "target_only_lst_invocation": invocation,
        "section_tag_count": len(tuple(_ANY_SECTION_TAG_RE.finditer(wikitext))),
        "html_tag_names": dict(sorted(html_tags.items())),
        "heading_level_counts": {str(level): count for level, count in sorted(heading_levels.items())},
        "category_link_count": len(_CATEGORY_RE.findall(wikitext)),
        "table_start_count": wikitext.count("{|"),
        "table_end_count": wikitext.count("|}"),
        "first_nonempty_line_class": line_class(nonempty_lines[0]) if nonempty_lines else "empty",
        "last_nonempty_line_class": line_class(nonempty_lines[-1]) if nonempty_lines else "empty",
        "source_text_included": False,
    }


def main(argv: Sequence[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Probe or freeze the pinned Klim Samgin #lst source contract.")
    subparsers = parser.add_subparsers(dest="command", required=True)
    probe = subparsers.add_parser("probe")
    probe.add_argument("--revision-manifest", type=Path, required=True)
    capture = subparsers.add_parser("capture-lst")
    capture.add_argument("--parent-revision-manifest", type=Path, required=True)
    capture.add_argument("--dependency-revision-manifest", type=Path, required=True)
    capture.add_argument("--output", type=Path, required=True)
    replay = subparsers.add_parser("replay-lst")
    replay.add_argument("--parent-revision-manifest", type=Path, required=True)
    replay.add_argument("--dependency-revision-manifest", type=Path, required=True)
    replay.add_argument("--contract", type=Path, required=True)
    replay.add_argument("--receipt", type=Path)
    args = parser.parse_args(argv)

    if args.command == "probe":
        result = probe_revision_shape(_load_json(args.revision_manifest))
        print("SCRIPTORIUM_KLIM_SHAPE=" + json.dumps(result, ensure_ascii=False, sort_keys=True, separators=(",", ":")))
        return 0
    parent = _load_json(args.parent_revision_manifest)
    dependency = _load_json(args.dependency_revision_manifest)
    if args.command == "capture-lst":
        contract = build_lst_contract(parent, dependency)
        validate_lst_contract(contract, parent_revision_manifest=parent, dependency_revision_manifest=dependency)
        _write_json(args.output, contract)
        return 0
    contract = _load_json(args.contract)
    receipt = replay_lst_contract(parent, dependency, contract)
    if args.receipt is not None:
        _write_json(args.receipt, receipt)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
