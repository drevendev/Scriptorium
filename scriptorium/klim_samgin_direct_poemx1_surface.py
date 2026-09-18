"""Classify the seven direct parent ``poemx1`` calls before Klim Samgin body extraction.

SCRIP-CORPUS-020 already froze the structural placement and argument identities for the
five direct Part 1 calls and two direct Part 2 calls.  This module re-opens only those
seven parameter-2 values in process memory, inventories the conservative MediaWiki-core
and Poem branches that can affect their visible text, and records source-free identities.

The result is deliberately a prerequisite, not a literary-body extractor.  If a value is
plain under the already-versioned bounded Poem reconstruction, the artifact records a
post-unstrip fragment identity and marks that invocation safe for a future plain-value
literary replacement.  If active syntax is observed, the artifact records only the
source-free syntax counts and leaves that invocation unresolved instead of guessing.
"""
from __future__ import annotations

import argparse
from collections import Counter
from hashlib import sha256
import json
from pathlib import Path
from typing import Callable, Mapping, Sequence

from .klim_samgin_body_surface import (
    CANDIDATE_ID,
    EXPECTED_DIRECT_POEMX1_COUNTS,
    EXPECTED_PART_REVISION_IDS,
    validate_body_surface_manifest,
)
from .mediawiki_poem_render_surface import (
    _active_construct_total,
    _core_sensitive_surface,
    _poem_branch_surface,
    _render_plain_poem_fragment,
)
from .mediawiki_poemx1_content import _parameter_two_value
from .mediawiki_template_invocation import find_template_invocations
from .single_page_body import fetch_pinned_wikitext
from .single_page_revision import validate_manifest as validate_revision_manifest


MANIFEST_VERSION = "scriptorium-klim-samgin-direct-poemx1-surface-v1"
PROFILE_VERSION = "scriptorium-klim-samgin-direct-poemx1-literary-surface-v1"


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


def _verified_wikitext(
    revision_manifest: Mapping[str, object],
    *,
    expected_part: int,
    fetcher: Callable[..., dict[str, object]],
) -> tuple[str, Mapping[str, object]]:
    validate_revision_manifest(revision_manifest)
    expected_candidate = f"{CANDIDATE_ID}-part-{expected_part}"
    if revision_manifest.get("candidate_id") != expected_candidate:
        raise ValueError(f"unexpected candidate for Klim part {expected_part}")
    identity = revision_manifest.get("source_identity")
    if not isinstance(identity, Mapping):
        raise ValueError("revision source identity missing")
    if identity.get("revision_id") != EXPECTED_PART_REVISION_IDS[expected_part]:
        raise ValueError(f"unexpected revision for Klim part {expected_part}")
    title = identity.get("title")
    revision_id = identity.get("revision_id")
    if not isinstance(title, str) or not isinstance(revision_id, int):
        raise ValueError("revision source identity incomplete")
    observed = fetcher(title=title, revision_id=revision_id)
    wikitext = observed.pop("wikitext", None)
    if not isinstance(wikitext, str):
        raise ValueError("transient pinned wikitext missing")
    if observed != dict(identity):
        differing = sorted(
            key
            for key in set(observed) | set(identity)
            if observed.get(key) != identity.get(key)
        )
        raise ValueError(f"pinned Klim part {expected_part} identity drift: {differing}")
    return wikitext, identity


def _branch_is_plain(core: Mapping[str, object], branch: Mapping[str, object]) -> bool:
    return (
        _active_construct_total(core) == 0
        and int(branch.get("leading_colon_line_count", 0)) == 0
        and int(branch.get("leading_space_line_count", 0)) == 0
        and int(branch.get("horizontal_rule_line_count", 0)) == 0
        and branch.get("edge_whitespace_present") is False
    )


def _classify_invocation(
    *,
    part: int,
    wikitext: str,
    observed: Mapping[str, object],
    frozen: Mapping[str, object],
) -> dict[str, object]:
    if observed != frozen:
        raise ValueError(f"Klim part {part} direct poemx1 structural row drift")
    value, identity = _parameter_two_value(wikitext, observed)
    core = _core_sensitive_surface(value)
    branch = _poem_branch_surface(value)
    safe = _branch_is_plain(core, branch)

    row: dict[str, object] = {
        "invocation_index": observed["invocation_index"],
        "invocation_sha256": observed["invocation_sha256"],
        "parent_start_offset": observed["parent_start_offset"],
        "parent_end_offset": observed["parent_end_offset"],
        "parameter_2_identity": identity,
        "core_sensitive_surface": core,
        "poem_branch_surface": branch,
        "plain_value_literary_replacement_safe": safe,
        "source_text_included": False,
    }
    if safe:
        rendered = _render_plain_poem_fragment(value)
        raw = rendered.encode("utf-8")
        row["bounded_poem_reconstruction"] = {
            "post_unstrip_fragment_character_count": len(rendered),
            "post_unstrip_fragment_utf8_byte_count": len(raw),
            "post_unstrip_fragment_sha256": sha256(raw).hexdigest(),
            "literary_plain_value_sha256": identity["sha256"],
        }
    else:
        row["bounded_poem_reconstruction"] = None
    return row


def build_manifest(
    revision_manifests: Sequence[Mapping[str, object]],
    body_surface_manifest: Mapping[str, object],
    *,
    research_date: str,
    fetcher: Callable[..., dict[str, object]] = fetch_pinned_wikitext,
) -> dict[str, object]:
    if len(revision_manifests) != 4:
        raise ValueError("exactly four Klim part revision manifests are required")
    if not isinstance(research_date, str) or not research_date:
        raise ValueError("research_date must be non-empty")
    validate_body_surface_manifest(body_surface_manifest)
    if body_surface_manifest.get("candidate_id") != CANDIDATE_ID:
        raise ValueError("unexpected Klim body-surface candidate")
    frozen_parts = body_surface_manifest.get("parts")
    if not isinstance(frozen_parts, list) or len(frozen_parts) != 4:
        raise ValueError("body-surface manifest must contain four parts")

    rows: list[dict[str, object]] = []
    aggregate: Counter[str] = Counter()
    unresolved: list[dict[str, object]] = []
    total_invocations = 0

    for part, (revision_manifest, frozen_part_obj) in enumerate(
        zip(revision_manifests, frozen_parts), start=1
    ):
        if not isinstance(frozen_part_obj, Mapping) or frozen_part_obj.get("part") != part:
            raise ValueError("Klim body-surface part order drift")
        wikitext, identity = _verified_wikitext(
            revision_manifest, expected_part=part, fetcher=fetcher
        )
        if _sha256_text(wikitext) != identity.get("wikitext_sha256"):
            raise ValueError(f"Klim part {part} wikitext digest drift")
        observed_invocations = find_template_invocations(wikitext, template_name="poemx1")
        expected_count = EXPECTED_DIRECT_POEMX1_COUNTS[part]
        if len(observed_invocations) != expected_count:
            raise ValueError(
                f"Klim part {part} direct poemx1 inventory drift: {len(observed_invocations)}"
            )
        frozen_invocations = frozen_part_obj.get("direct_poemx1_invocations")
        if not isinstance(frozen_invocations, list) or len(frozen_invocations) != expected_count:
            raise ValueError(f"Klim part {part} frozen poemx1 inventory drift")

        classified: list[dict[str, object]] = []
        for observed, frozen in zip(observed_invocations, frozen_invocations):
            if not isinstance(frozen, Mapping):
                raise ValueError("invalid frozen direct poemx1 row")
            classified_row = _classify_invocation(
                part=part,
                wikitext=wikitext,
                observed=observed,
                frozen=frozen,
            )
            classified.append(classified_row)
            total_invocations += 1
            core = classified_row["core_sensitive_surface"]
            branch = classified_row["poem_branch_surface"]
            assert isinstance(core, Mapping) and isinstance(branch, Mapping)
            aggregate["core_active_construct_count"] += _active_construct_total(core)
            aggregate["newline_count"] += int(branch["newline_count"])
            aggregate["input_character_count"] += int(
                classified_row["parameter_2_identity"]["character_count"]  # type: ignore[index]
            )
            aggregate["input_utf8_byte_count"] += int(
                classified_row["parameter_2_identity"]["utf8_byte_count"]  # type: ignore[index]
            )
            if classified_row["plain_value_literary_replacement_safe"] is True:
                aggregate["plain_safe_invocation_count"] += 1
            else:
                unresolved.append(
                    {
                        "part": part,
                        "invocation_index": classified_row["invocation_index"],
                        "invocation_sha256": classified_row["invocation_sha256"],
                        "core_sensitive_surface": core,
                        "poem_branch_surface": branch,
                    }
                )

        rows.append(
            {
                "part": part,
                "source_revision_id": identity["revision_id"],
                "source_wikitext_sha256": identity["wikitext_sha256"],
                "direct_poemx1_invocation_count": len(classified),
                "invocations": classified,
                "source_text_included": False,
            }
        )

    if total_invocations != 7:
        raise ValueError(f"expected seven direct parent poemx1 calls, observed {total_invocations}")
    all_plain = len(unresolved) == 0
    aggregate["invocation_count"] = total_invocations
    aggregate["unresolved_invocation_count"] = len(unresolved)

    return {
        "manifest_version": MANIFEST_VERSION,
        "candidate_id": CANDIDATE_ID,
        "research_date": research_date,
        "profile": PROFILE_VERSION,
        "evidence_class": "candidate_specific_inferred_reconstruction",
        "parts": rows,
        "aggregate": dict(sorted(aggregate.items())),
        "all_direct_parent_poemx1_plain_value_safe": all_plain,
        "unresolved_invocations": unresolved,
        "capture_scope": {
            "direct_parent_poemx1_structural_surface_replayed": True,
            "direct_parent_poemx1_core_and_poem_surface_classified": True,
            "all_direct_parent_poemx1_plain_value_safe": all_plain,
            "literary_body_extraction_frozen": False,
            "literary_composition_frozen": False,
            "composite_literary_body_identity_frozen": False,
            "historical_render_equivalence_proven": False,
            "source_text_committed": False,
        },
        "boundary": (
            "This artifact classifies only the seven direct parent-level poemx1 values against the "
            "already-versioned conservative MediaWiki-core and inferred Poem reconstruction surface. "
            "It does not extract the four literary bodies, prove historical Russian Wikisource "
            "MediaWiki/Poem deployment equivalence, identify FantLab input bytes, or advance M2."
        ),
        "source_text_included": False,
        "fantlab_source_edition_match": "unknown",
        "diagnostic_ready": False,
        "gate_ready": False,
        "m2_parity_admissible": False,
    }


def validate_manifest(manifest: Mapping[str, object]) -> None:
    if manifest.get("manifest_version") != MANIFEST_VERSION:
        raise ValueError("unsupported Klim direct poemx1 surface manifest")
    if manifest.get("candidate_id") != CANDIDATE_ID or manifest.get("profile") != PROFILE_VERSION:
        raise ValueError("unexpected Klim direct poemx1 manifest identity")
    if manifest.get("evidence_class") != "candidate_specific_inferred_reconstruction":
        raise ValueError("direct poemx1 evidence class drift")
    parts = manifest.get("parts")
    if not isinstance(parts, list) or len(parts) != 4:
        raise ValueError("direct poemx1 manifest must contain four parts")
    observed_total = 0
    observed_plain = 0
    for part, row_obj in enumerate(parts, start=1):
        if not isinstance(row_obj, Mapping) or row_obj.get("part") != part:
            raise ValueError("direct poemx1 part order drift")
        if row_obj.get("source_revision_id") != EXPECTED_PART_REVISION_IDS[part]:
            raise ValueError(f"Klim part {part} revision drift")
        rows = row_obj.get("invocations")
        expected_count = EXPECTED_DIRECT_POEMX1_COUNTS[part]
        if not isinstance(rows, list) or len(rows) != expected_count:
            raise ValueError(f"Klim part {part} direct poemx1 row count drift")
        observed_total += len(rows)
        for index, invocation_obj in enumerate(rows, start=1):
            if not isinstance(invocation_obj, Mapping):
                raise ValueError("invalid direct poemx1 invocation row")
            if invocation_obj.get("invocation_index") != index:
                raise ValueError("direct poemx1 invocation order drift")
            identity = invocation_obj.get("parameter_2_identity")
            if not isinstance(identity, Mapping):
                raise ValueError("parameter-2 identity missing")
            if not isinstance(identity.get("character_count"), int) or int(identity["character_count"]) <= 0:
                raise ValueError("invalid parameter-2 character count")
            digest = identity.get("sha256")
            if not isinstance(digest, str) or len(digest) != 64:
                raise ValueError("invalid parameter-2 digest")
            safe = invocation_obj.get("plain_value_literary_replacement_safe")
            if not isinstance(safe, bool):
                raise ValueError("plain-value safety classification missing")
            if safe:
                observed_plain += 1
                reconstruction = invocation_obj.get("bounded_poem_reconstruction")
                if not isinstance(reconstruction, Mapping):
                    raise ValueError("plain-safe invocation missing reconstruction identity")
                if reconstruction.get("literary_plain_value_sha256") != digest:
                    raise ValueError("plain literary replacement identity drift")
            elif invocation_obj.get("bounded_poem_reconstruction") is not None:
                raise ValueError("unresolved invocation must not claim bounded reconstruction")
            if invocation_obj.get("source_text_included") is not False:
                raise ValueError("source text flag must remain false")
        if row_obj.get("source_text_included") is not False:
            raise ValueError("source text flag must remain false")

    if observed_total != 7:
        raise ValueError("direct poemx1 aggregate count drift")
    unresolved = manifest.get("unresolved_invocations")
    if not isinstance(unresolved, list) or len(unresolved) != observed_total - observed_plain:
        raise ValueError("direct poemx1 unresolved inventory drift")
    all_plain = manifest.get("all_direct_parent_poemx1_plain_value_safe")
    if all_plain is not (observed_plain == observed_total):
        raise ValueError("direct poemx1 aggregate safety flag drift")

    scope = manifest.get("capture_scope")
    if not isinstance(scope, Mapping):
        raise ValueError("direct poemx1 capture scope missing")
    if scope.get("direct_parent_poemx1_structural_surface_replayed") is not True:
        raise ValueError("structural surface replay flag missing")
    if scope.get("direct_parent_poemx1_core_and_poem_surface_classified") is not True:
        raise ValueError("classification flag missing")
    if scope.get("all_direct_parent_poemx1_plain_value_safe") is not all_plain:
        raise ValueError("capture-scope safety flag drift")
    for key in (
        "literary_body_extraction_frozen",
        "literary_composition_frozen",
        "composite_literary_body_identity_frozen",
        "historical_render_equivalence_proven",
        "source_text_committed",
    ):
        if scope.get(key) is not False:
            raise ValueError(f"{key} must remain false in prerequisite artifact")
    if manifest.get("source_text_included") is not False:
        raise ValueError("source prose must not be persisted")
    if manifest.get("fantlab_source_edition_match") != "unknown":
        raise ValueError("FantLab source identity must remain unknown")
    if manifest.get("diagnostic_ready") is not False or manifest.get("gate_ready") is not False:
        raise ValueError("direct poemx1 surface alone cannot open diagnostic/gate")
    if manifest.get("m2_parity_admissible") is not False:
        raise ValueError("direct poemx1 surface alone cannot advance M2")

    forbidden = {"wikitext", "content", "body", "text", "source_text"}
    if forbidden.intersection(manifest):
        raise ValueError("source prose key leaked into direct poemx1 manifest")


def replay_manifest(
    revision_manifests: Sequence[Mapping[str, object]],
    body_surface_manifest: Mapping[str, object],
    manifest: Mapping[str, object],
    *,
    fetcher: Callable[..., dict[str, object]] = fetch_pinned_wikitext,
) -> dict[str, object]:
    validate_manifest(manifest)
    observed = build_manifest(
        revision_manifests,
        body_surface_manifest,
        research_date=str(manifest["research_date"]),
        fetcher=fetcher,
    )
    if observed != dict(manifest):
        raise ValueError("pinned Klim direct parent poemx1 surface drift")
    return {
        "receipt_version": "scriptorium-klim-samgin-direct-poemx1-replay-v1",
        "candidate_id": CANDIDATE_ID,
        "manifest_version": MANIFEST_VERSION,
        "all_direct_parent_poemx1_plain_value_safe": manifest[
            "all_direct_parent_poemx1_plain_value_safe"
        ],
        "verified": True,
        "source_text_included": False,
        "fantlab_source_edition_match": "unknown",
        "m2_parity_admissible": False,
    }


def _part_manifest_paths(args: argparse.Namespace) -> list[Path]:
    return [
        args.part1_revision_manifest,
        args.part2_revision_manifest,
        args.part3_revision_manifest,
        args.part4_revision_manifest,
    ]


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description="Classify direct parent poemx1 values for Klim Samgin body extraction."
    )
    sub = parser.add_subparsers(dest="command", required=True)

    def add_sources(command: argparse.ArgumentParser) -> None:
        for part in range(1, 5):
            command.add_argument(
                f"--part{part}-revision-manifest",
                type=Path,
                required=True,
            )
        command.add_argument("--body-surface-manifest", type=Path, required=True)

    capture = sub.add_parser("capture")
    add_sources(capture)
    capture.add_argument("--research-date", required=True)
    capture.add_argument("--output", type=Path, required=True)

    replay = sub.add_parser("replay")
    add_sources(replay)
    replay.add_argument("--manifest", type=Path, required=True)
    replay.add_argument("--receipt", type=Path, required=True)

    args = parser.parse_args(argv)
    revision_manifests = [_load_json(path) for path in _part_manifest_paths(args)]
    body_surface = _load_json(args.body_surface_manifest)

    if args.command == "capture":
        manifest = build_manifest(
            revision_manifests,
            body_surface,
            research_date=args.research_date,
        )
        validate_manifest(manifest)
        _write_json(args.output, manifest)
        return 0

    manifest = _load_json(args.manifest)
    receipt = replay_manifest(revision_manifests, body_surface, manifest)
    _write_json(args.receipt, receipt)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
