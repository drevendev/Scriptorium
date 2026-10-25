#!/usr/bin/env python3
"""Execute a tiny source-free native pylem smoke under the legacy provider runtime."""
import argparse
import hashlib
from importlib.metadata import PackageNotFoundError, version
import json
from pathlib import Path
import platform

PYLEM_VERSION = "0.0.18"
SCHEMA_VERSION = "scriptorium-pylem-runtime-receipt-v1"
TOKENS = ("Красный", "быстро", "бежит")


def _sha256_text(value):
    return hashlib.sha256(value.encode("utf-8")).hexdigest()


# Deliberately small, source-free semantic controls. These lexical roles are
# fixture annotations, NOT a native AOT homonym decision.
N_CONTRAST_GROUPS = (
    ("noun_examples", ("дом", "книга", "город")),
    ("cardinal_examples", ("два", "три", "пять")),
    ("other_pos_controls", ("красный", "быстро", "бежит")),
)


def _runtime_candidates(holder, token):
    candidates = []
    for analysis in holder.lemmatize(token):
        value = getattr(analysis, "part_of_speech", None)
        if not isinstance(value, str) or not value.strip():
            raise RuntimeError("pylem returned blank/non-string part_of_speech")
        candidates.append(value.strip())
    return candidates


def build_n_contrast(holder):
    """Record observed native labels by lexical fixture role, never infer true POS."""
    groups = {}
    manifest = []
    for role, tokens in N_CONTRAST_GROUPS:
        rows = []
        for token in tokens:
            labels = _runtime_candidates(holder, token)
            token_hash = _sha256_text(token)
            rows.append({
                "token_sha256": token_hash,
                "candidate_count": len(labels),
                "runtime_pos": labels,
                "n_only": bool(labels) and set(labels) == {"N"},
                "n_present": "N" in labels,
            })
            manifest.append(role + ":" + token_hash)
        groups[role] = {
            "token_count": len(rows),
            "n_only_count": sum(row["n_only"] for row in rows),
            "n_present_count": sum(row["n_present"] for row in rows),
            "tokens": rows,
        }
    return {
        "schema_version": "scriptorium-aot-n-contrast-v1",
        "source_text_included": False,
        "token_manifest_sha256": _sha256_text("\n".join(manifest)),
        "groups": groups,
        "observed_n_only_across_noun_and_cardinal_examples": (
            groups["noun_examples"]["n_only_count"] > 0
            and groups["cardinal_examples"]["n_only_count"] > 0
        ),
        "interpretation": "Fixture lexical roles are annotations, not recovered AOT POS enums.",
        "fantlab_dictionary_equivalence": "unknown",
        "fantlab_homonym_selection": "unresolved",
        "production_pos_mapping_changed": False,
        "m2_parity_admissible": False,
    }


def build_receipt():
    try:
        installed = version("pylem")
    except PackageNotFoundError as exc:
        raise RuntimeError("pylem==0.0.18 is not installed") from exc
    if installed != PYLEM_VERSION:
        raise RuntimeError("expected pylem==0.0.18, found pylem==%s" % installed)

    from pylem import MorphanHolder, MorphLanguage

    holder = MorphanHolder(MorphLanguage.Russian)
    rows = []
    observed = set()
    for ordinal, token in enumerate(TOKENS):
        runtime_pos = _runtime_candidates(holder, token)
        observed.update(runtime_pos)
        rows.append(
            {
                "ordinal": ordinal,
                "token_sha256": _sha256_text(token),
                "candidate_count": len(runtime_pos),
                "runtime_pos": runtime_pos,
            }
        )

    fixture_identity = "\n".join(
        "%d:%s" % (ordinal, _sha256_text(token)) for ordinal, token in enumerate(TOKENS)
    )
    return {
        "schema_version": SCHEMA_VERSION,
        "provider": {
            "distribution": "pylem",
            "version": installed,
            "runtime_profile": "pylem-0.0.18-python39-sidecar-v1",
        },
        "runtime": {
            "python_implementation": platform.python_implementation(),
            "python_version": platform.python_version(),
            "platform": platform.platform(),
        },
        "fixture": {
            "token_count": len(TOKENS),
            "token_manifest_sha256": _sha256_text(fixture_identity),
            "tokens": rows,
            "observed_runtime_pos": sorted(observed),
            "source_text_included": False,
        },
        "n_contrast": build_n_contrast(holder),
        "epistemic_boundary": {
            "fantlab_dictionary_equivalence": "unknown",
            "homonym_selection_policy": "unresolved",
            "noun_cardinal_runtime_collision": "unresolved",
            "m2_parity_admissible": False,
        },
    }


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--receipt", type=Path, required=True)
    args = parser.parse_args()
    receipt = build_receipt()
    args.receipt.parent.mkdir(parents=True, exist_ok=True)
    args.receipt.write_text(
        json.dumps(receipt, ensure_ascii=False, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
