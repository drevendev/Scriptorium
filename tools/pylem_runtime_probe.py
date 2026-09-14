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
        analyses = tuple(holder.lemmatize(token))
        runtime_pos = []
        for analysis in analyses:
            value = getattr(analysis, "part_of_speech", None)
            if not isinstance(value, str) or not value.strip():
                raise RuntimeError("pylem returned blank/non-string part_of_speech")
            value = value.strip()
            runtime_pos.append(value)
            observed.add(value)
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
