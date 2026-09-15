#!/usr/bin/env python3
"""Run exact pylem 0.0.18 over an ephemeral Scriptorium token request."""
import argparse
import hashlib
from importlib.metadata import PackageNotFoundError, version
import json
from pathlib import Path

PYLEM_VERSION = "0.0.18"
REQUEST_SCHEMA = "scriptorium-pylem-sidecar-request-v1"
RESPONSE_SCHEMA = "scriptorium-pylem-sidecar-response-v1"
CANDIDATE_METADATA_SCHEMA = "scriptorium-pylem-candidate-metadata-v1"
RUNTIME_PROFILE = "pylem-0.0.18-python39-sidecar-v1"


def _sha256_text(value):
    return hashlib.sha256(value.encode("utf-8")).hexdigest()


def _optional_int(value, field):
    if value is None:
        return None
    if isinstance(value, bool) or not isinstance(value, int):
        raise RuntimeError("pylem returned invalid %s" % field)
    return value


def build_response(request):
    if request.get("schema_version") != REQUEST_SCHEMA:
        raise ValueError("unexpected sidecar request schema")
    normalized_text = request.get("normalized_text")
    if not isinstance(normalized_text, str):
        raise ValueError("request missing normalized_text")
    normalized_sha256 = _sha256_text(normalized_text)
    if request.get("normalized_sha256") != normalized_sha256:
        raise ValueError("request normalized hash mismatch")
    rows = request.get("tokens")
    if not isinstance(rows, list):
        raise ValueError("request tokens must be an array")

    try:
        installed = version("pylem")
    except PackageNotFoundError as exc:
        raise RuntimeError("pylem==0.0.18 is not installed") from exc
    if installed != PYLEM_VERSION:
        raise RuntimeError("expected pylem==0.0.18, found pylem==%s" % installed)

    from pylem import MorphanHolder, MorphLanguage

    holder = MorphanHolder(MorphLanguage.Russian)
    cache = {}
    output_rows = []
    for ordinal, row in enumerate(rows):
        if not isinstance(row, dict) or row.get("ordinal") != ordinal:
            raise ValueError("request token ordinal mismatch")
        token = row.get("text")
        if not isinstance(token, str):
            raise ValueError("request token missing text")
        token_sha256 = _sha256_text(token)
        if row.get("sha256") != token_sha256:
            raise ValueError("request token hash mismatch")

        cached = cache.get(token)
        if cached is None:
            values = []
            metadata = []
            for analysis in holder.lemmatize(token):
                value = getattr(analysis, "part_of_speech", None)
                if not isinstance(value, str) or not value.strip():
                    raise RuntimeError("pylem returned blank/non-string part_of_speech")
                runtime_pos = value.strip()
                predicted = getattr(analysis, "predicted", None)
                if not isinstance(predicted, bool):
                    raise RuntimeError("pylem returned invalid predicted flag")
                values.append(runtime_pos)
                metadata.append(
                    {
                        "runtime_pos": runtime_pos,
                        "predicted": predicted,
                        "homonym_weight": _optional_int(
                            getattr(analysis, "homonym_weight", None), "homonym_weight"
                        ),
                        "word_weight": _optional_int(
                            getattr(analysis, "word_weight", None), "word_weight"
                        ),
                    }
                )
            cached = (tuple(values), tuple(metadata))
            cache[token] = cached
        runtime_pos, candidate_metadata = cached
        output_rows.append(
            {
                "ordinal": ordinal,
                "token_sha256": token_sha256,
                "runtime_pos": list(runtime_pos),
                "candidate_metadata": [dict(item) for item in candidate_metadata],
            }
        )

    return {
        "schema_version": RESPONSE_SCHEMA,
        "candidate_metadata_schema": CANDIDATE_METADATA_SCHEMA,
        "runtime_profile": RUNTIME_PROFILE,
        "provider": {"distribution": "pylem", "version": installed},
        "normalized_sha256": normalized_sha256,
        "token_count": len(rows),
        "distinct_token_count": len(cache),
        "rows": output_rows,
        "source_text_included": False,
        "epistemic_boundary": {
            "fantlab_dictionary_equivalence": "unknown",
            "fantlab_homonym_selection": "unresolved",
            "noun_cardinal_runtime_collision": "unresolved",
            "extra_category_folding": "unresolved",
            "m2_parity_admissible": False,
        },
    }


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--request", type=Path, required=True)
    parser.add_argument("--response", type=Path, required=True)
    args = parser.parse_args()
    request = json.loads(args.request.read_text(encoding="utf-8"))
    if not isinstance(request, dict):
        raise ValueError("sidecar request must be a JSON object")
    response = build_response(request)
    args.response.parent.mkdir(parents=True, exist_ok=True)
    args.response.write_text(
        json.dumps(response, ensure_ascii=False, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
