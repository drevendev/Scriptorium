#!/usr/bin/env python3
"""Audit exposed Python fields of native N candidates without emitting source text.

Field presence is not an original AOT source enum or a noun/cardinal decoder.
No raw attribute values or lexical fixture words are serialized.
"""
from __future__ import annotations

import argparse
from hashlib import sha256
from importlib.metadata import PackageNotFoundError, version
import json
from pathlib import Path

from tools.pylem_n_attestation_probe import CONTROLS, PROFILE, SDIST_SHA256

SCHEMA = "scriptorium-aot-n-source-pos-surface-v1"
# Closed allowlist: never serialize dynamic or unknown field names/values.
INSPECTED_FIELDS = (
    "part_of_speech", "predicted", "lemma", "grammems", "grammemes",
    "homonym_weight", "paradigm", "morph_info", "morphInfo",
    "ancode", "ancode_id", "aot_pos", "aot_pos_slot", "source_pos",
    "source_pos_slot", "gramtab_pos", "pos_index",
)
EXPLICIT_SOURCE_FIELDS = frozenset((
    "ancode", "ancode_id", "aot_pos", "aot_pos_slot", "source_pos",
    "source_pos_slot", "gramtab_pos", "pos_index",
))


def _digest(text: str) -> str:
    return sha256(text.encode("utf-8")).hexdigest()


def measure_source_pos_surface(holder) -> dict[str, object]:
    """Inspect field presence on every N analysis for the pinned lexical roles."""
    groups = {}
    manifest = []
    explicit_counts = {name: 0 for name in sorted(EXPLICIT_SOURCE_FIELDS)}
    fields_seen = set()
    n_total = 0
    for role, words in CONTROLS:
        rows = []
        for word in words:
            n_surfaces = []
            candidate_count = 0
            for analysis in holder.lemmatize(word):
                tag = getattr(analysis, "part_of_speech", None)
                if type(tag) is not str or not tag or tag != tag.strip():
                    raise ValueError("invalid native part_of_speech")
                candidate_count += 1
                if tag != "N":
                    continue
                # Presence only; never expose lemma, grammemes or raw morphInfo.
                fields = sorted(field for field in INSPECTED_FIELDS if hasattr(analysis, field))
                n_surfaces.append(fields)
                n_total += 1
                fields_seen.update(fields)
                for field in fields:
                    if field in explicit_counts:
                        explicit_counts[field] += 1
            rows.append({
                "token_sha256": _digest(word),
                "candidate_count": candidate_count,
                "n_candidate_count": len(n_surfaces),
                "n_public_field_names": n_surfaces,
            })
            manifest.append(role + ":" + _digest(word))
        groups[role] = {
            "token_count": len(rows),
            "n_candidate_count": sum(row["n_candidate_count"] for row in rows),
            "tokens": rows,
        }
    negative_rows = groups["unrelated_preposition_controls"]["tokens"]
    clean_negatives = sum(row["candidate_count"] > 0 and row["n_candidate_count"] == 0
                          for row in negative_rows)
    possible = any(explicit_counts.values())
    decision = ("possible_field_needs_semantic_validation" if possible else
                "no_explicit_field_in_examined_n_analyses" if n_total else
                "no_n_analyses_observed")
    return {
        "schema_version": SCHEMA,
        "status": "diagnostic_only",
        "source_text_included": False,
        "m2_parity_admissible": False,
        "provider": {"distribution": "pylem", "version": "0.0.18",
                     "runtime_profile": PROFILE, "sdist_sha256": SDIST_SHA256},
        "fixture_manifest_sha256": _digest("\n".join(manifest)),
        "groups": groups,
        "n_candidate_count": n_total,
        "n_public_field_names_observed": sorted(fields_seen),
        "explicit_source_field_presence_counts": explicit_counts,
        "clean_negative_control_count": clean_negatives,
        "runtime_field_surface_decision": decision,
        "original_aot_enum_verified": False,
        "noun_cardinal_source_pos": "unresolved",
        "fantlab_homonym_selection": "unresolved",
        "production_pos_mapping_changed": False,
        "runtime_fields_are_not_source_pos_proof": True,
        "observation_sha256": _digest(json.dumps(groups, ensure_ascii=False,
                                                  sort_keys=True, separators=(",", ":"))),
    }


def main(argv=None) -> int:
    parser = argparse.ArgumentParser(description="Audit native N fields without source values")
    parser.add_argument("--receipt", type=Path, required=True)
    args = parser.parse_args(argv)
    try:
        installed = version("pylem")
    except PackageNotFoundError as exc:
        raise RuntimeError("native pylem==0.0.18 required") from exc
    if installed != "0.0.18":
        raise RuntimeError("wrong native pylem version")
    from pylem import MorphanHolder, MorphLanguage
    result = measure_source_pos_surface(MorphanHolder(MorphLanguage.Russian))
    args.receipt.parent.mkdir(parents=True, exist_ok=True)
    with args.receipt.open("x", encoding="utf-8") as stream:
        json.dump(result, stream, ensure_ascii=False, indent=2, sort_keys=True)
        stream.write("\n")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
