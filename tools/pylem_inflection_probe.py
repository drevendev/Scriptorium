#!/usr/bin/env python3
"""Independent inflected-form N control on pinned pylem; emits no lexical source text.

Fixture role labels are researcher annotations, not recovered native AOT source POS.
This neither calibrates a disambiguator nor compares text with FantLab.
"""
from __future__ import annotations

import argparse
from hashlib import sha256
from importlib.metadata import PackageNotFoundError, version
import json
from pathlib import Path

SCHEMA = "scriptorium-aot-n-inflected-controls-v1"
PROFILE = "pylem-0.0.18-python39-sidecar-v1"
SDIST_SHA256 = "66c0d13414006a803f200979540fcee9653738701c14496a418db67542b26515"
# Fresh inflected fixtures distinct from earlier citation-form controls.
CONTROL_GROUPS = (
    ("noun_oblique_examples", ("столами", "домами", "книгами")),
    ("cardinal_oblique_examples", ("двумя", "тремя", "пятью")),
    ("unrelated_conjunction_controls", ("и", "но", "или")),
)


def _digest(text: str) -> str:
    return sha256(text.encode("utf-8")).hexdigest()


def build_oblique_n_observation(holder) -> dict[str, object]:
    """Record every candidate and count disjoint N-only/mixed-N groups."""
    groups = {}
    manifest = []
    for role, words in CONTROL_GROUPS:
        rows = []
        for word in words:
            labels = []
            for analysis in holder.lemmatize(word):
                tag = getattr(analysis, "part_of_speech", None)
                if type(tag) is not str or not tag or tag != tag.strip():
                    raise ValueError("native candidate has invalid POS tag")
                labels.append(tag)
            n_present = "N" in labels
            n_only = bool(labels) and set(labels) == {"N"}
            rows.append({
                "token_sha256": _digest(word),
                "candidate_count": len(labels),
                "runtime_pos": labels,
                "n_only": n_only,
                "n_present": n_present,
                "n_mixed": n_present and not n_only,
            })
            manifest.append(role + ":" + _digest(word))
        groups[role] = {
            "token_count": len(rows),
            "n_only_count": sum(row["n_only"] for row in rows),
            "n_mixed_count": sum(row["n_mixed"] for row in rows),
            "n_present_count": sum(row["n_present"] for row in rows),
            "tokens": rows,
        }
    negatives = groups["unrelated_conjunction_controls"]["tokens"]
    usable_negatives = sum(row["candidate_count"] > 0 and not row["n_present"]
                           for row in negatives)
    positive = (groups["noun_oblique_examples"]["n_only_count"] > 0
                and groups["cardinal_oblique_examples"]["n_only_count"] > 0)
    observations_sha = _digest(json.dumps(groups, ensure_ascii=False, sort_keys=True,
                                         separators=(",", ":")))
    return {
        "schema_version": SCHEMA,
        "status": "diagnostic_only",
        "source_text_included": False,
        "m2_parity_admissible": False,
        "provider": {"distribution": "pylem", "version": "0.0.18",
                     "runtime_profile": PROFILE, "sdist_sha256": SDIST_SHA256},
        "fixture_manifest_sha256": _digest("\n".join(manifest)),
        "runtime_observations_sha256": observations_sha,
        "groups": groups,
        "negative_controls_usable": usable_negatives,
        "negative_controls_required": 2,
        "cross_role_n_only_observed": positive,
        "qualified_cross_role_n_observation": positive and usable_negatives >= 2,
        "noun_cardinal_source_pos": "unresolved",
        "fantlab_homonym_selection": "unresolved",
        "production_pos_mapping_changed": False,
        "interpretation": "Fresh inflected lexical controls only; not a third full-work experiment",
    }


def main(argv=None) -> int:
    parser = argparse.ArgumentParser(description="Run isolated source-free pylem inflection controls")
    parser.add_argument("--receipt", type=Path, required=True)
    args = parser.parse_args(argv)
    try:
        installed = version("pylem")
    except PackageNotFoundError as exc:
        raise RuntimeError("native pylem==0.0.18 is required") from exc
    if installed != "0.0.18":
        raise RuntimeError("wrong pylem native provider version")
    from pylem import MorphanHolder, MorphLanguage
    result = build_oblique_n_observation(MorphanHolder(MorphLanguage.Russian))
    args.receipt.parent.mkdir(parents=True, exist_ok=True)
    with args.receipt.open("x", encoding="utf-8") as stream:
        json.dump(result, stream, ensure_ascii=False, indent=2, sort_keys=True)
        stream.write("\n")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
