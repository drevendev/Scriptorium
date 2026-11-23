#!/usr/bin/env python3
"""Measure whether curated native N collisions are dictionary-attested or predicted.

Fixture grammar roles are human annotations; neither these roles nor dictionary
attestation recover AOT source POS or FantLab's homonym-selection policy.
Only hashes of fixture words and POS/prediction summaries enter the receipt.
"""
from __future__ import annotations

import argparse
from hashlib import sha256
from importlib.metadata import PackageNotFoundError, version
import json
from pathlib import Path

SCHEMA = "scriptorium-aot-n-dictionary-attestation-v1"
PROFILE = "pylem-0.0.18-python39-sidecar-v1"
SDIST_SHA256 = "66c0d13414006a803f200979540fcee9653738701c14496a418db67542b26515"
CONTROLS = (
    ("noun_genitive_annotations", ("домов", "столов", "книг")),
    ("cardinal_genitive_annotations", ("двух", "трёх", "пяти")),
    ("unrelated_preposition_controls", ("в", "под", "без")),
)


def _digest(value: str) -> str:
    return sha256(value.encode("utf-8")).hexdigest()


def measure_attestation(holder) -> dict[str, object]:
    groups = {}
    manifest = []
    for role, words in CONTROLS:
        rows = []
        for word in words:
            candidates = []
            for candidate in holder.lemmatize(word):
                tag = getattr(candidate, "part_of_speech", None)
                predicted = getattr(candidate, "predicted", None)
                if type(tag) is not str or not tag or tag != tag.strip():
                    raise ValueError("invalid native part_of_speech")
                if type(predicted) is not bool:
                    raise ValueError("native prediction flag must be boolean")
                candidates.append((tag, predicted))
            n_rows = [predicted for tag, predicted in candidates if tag == "N"]
            n_only = bool(candidates) and all(tag == "N" for tag, _ in candidates)
            n_attested = any(not predicted for predicted in n_rows)
            n_predicted_only = bool(n_rows) and all(n_rows)
            rows.append({
                "token_sha256": _digest(word),
                "candidate_count": len(candidates),
                "runtime_pos": [tag for tag, _ in candidates],
                "prediction_flags": [predicted for _, predicted in candidates],
                "n_only": n_only,
                "n_mixed": bool(n_rows) and not n_only,
                "n_attested": n_attested,
                "n_predicted_only": n_predicted_only,
                "n_only_attested": n_only and n_attested,
            })
            manifest.append(role + ":" + _digest(word))
        groups[role] = {
            "token_count": len(rows),
            "n_only_attested_count": sum(r["n_only_attested"] for r in rows),
            "n_attested_count": sum(r["n_attested"] for r in rows),
            "n_predicted_only_count": sum(r["n_predicted_only"] for r in rows),
            "n_mixed_count": sum(r["n_mixed"] for r in rows),
            "tokens": rows,
        }
    negative_rows = groups["unrelated_preposition_controls"]["tokens"]
    usable_negatives = sum(r["candidate_count"] > 0 and "N" not in r["runtime_pos"]
                           for r in negative_rows)
    cross_role = (groups["noun_genitive_annotations"]["n_only_attested_count"] > 0
                  and groups["cardinal_genitive_annotations"]["n_only_attested_count"] > 0)
    return {
        "schema_version": SCHEMA,
        "status": "diagnostic_only",
        "source_text_included": False,
        "m2_parity_admissible": False,
        "provider": {"distribution": "pylem", "version": "0.0.18",
                     "runtime_profile": PROFILE, "sdist_sha256": SDIST_SHA256},
        "fixture_manifest_sha256": _digest("\n".join(manifest)),
        "runtime_observations_sha256": _digest(json.dumps(groups, sort_keys=True,
                                                         ensure_ascii=False, separators=(",", ":"))),
        "groups": groups,
        "usable_negative_controls": usable_negatives,
        "required_negative_controls": 2,
        "cross_role_attested_n_only_observed": cross_role,
        "qualified_cross_role_attestation_observed": cross_role and usable_negatives >= 2,
        "dictionary_attested_is_not_source_pos": True,
        "noun_cardinal_source_pos": "unresolved",
        "fantlab_homonym_selection": "unresolved",
        "production_pos_mapping_changed": False,
        "interpretation": "New genitive-form fixture evidence only, not a noun/cardinal discriminator or corpus statistic",
    }


def main(argv=None) -> int:
    parser = argparse.ArgumentParser(description="Measure native pylem N dictionary attestation, source-free")
    parser.add_argument("--receipt", type=Path, required=True)
    args = parser.parse_args(argv)
    try:
        installed = version("pylem")
    except PackageNotFoundError as exc:
        raise RuntimeError("native pylem==0.0.18 required") from exc
    if installed != "0.0.18":
        raise RuntimeError("wrong native pylem version")
    from pylem import MorphanHolder, MorphLanguage
    result = measure_attestation(MorphanHolder(MorphLanguage.Russian))
    args.receipt.parent.mkdir(parents=True, exist_ok=True)
    with args.receipt.open("x", encoding="utf-8") as file:
        json.dump(result, file, ensure_ascii=False, indent=2, sort_keys=True)
        file.write("\n")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
