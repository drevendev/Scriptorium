"""Transport pinned pylem sidecar output into Scriptorium POS diagnostics."""
from __future__ import annotations

import argparse
from hashlib import sha256
import json
from pathlib import Path
from typing import Mapping, Sequence

from .morphology import analyze_pos_metrics
from .pylem_provider import KNOWN_RUNTIME_POS, PYLEM_RUNTIME_PROFILE
from .text import NORMALIZATION_PROFILE, normalize_text, word_tokens
from .wikisource_replay import replay_packed_manifest

REQUEST_SCHEMA = "scriptorium-pylem-sidecar-request-v1"
RESPONSE_SCHEMA = "scriptorium-pylem-sidecar-response-v1"
DIAGNOSTIC_SCHEMA = "scriptorium-frozen-pos-diagnostic-v1"


def _sha256_text(value: str) -> str:
    return sha256(value.encode("utf-8")).hexdigest()


def build_sidecar_request(text: str) -> dict[str, object]:
    """Build an ephemeral request containing normalized text and exact word tokens."""
    normalized = normalize_text(text)
    tokens = word_tokens(normalized)
    return {
        "schema_version": REQUEST_SCHEMA,
        "text_profile": NORMALIZATION_PROFILE,
        "normalized_sha256": _sha256_text(normalized),
        "normalized_text": normalized,
        "tokens": [
            {
                "ordinal": ordinal,
                "text": token.text,
                "sha256": _sha256_text(token.text),
            }
            for ordinal, token in enumerate(tokens)
        ],
    }


def consume_sidecar_response(
    request: Mapping[str, object],
    response: Mapping[str, object],
) -> dict[str, object]:
    """Validate an isolated sidecar response and aggregate conservative POS metrics."""
    if request.get("schema_version") != REQUEST_SCHEMA:
        raise ValueError("unexpected pylem sidecar request schema")
    if response.get("schema_version") != RESPONSE_SCHEMA:
        raise ValueError("unexpected pylem sidecar response schema")
    if response.get("runtime_profile") != PYLEM_RUNTIME_PROFILE:
        raise ValueError("unexpected pylem runtime profile")
    normalized = request.get("normalized_text")
    if not isinstance(normalized, str):
        raise ValueError("sidecar request missing normalized_text")
    normalized_sha256 = _sha256_text(normalized)
    if request.get("normalized_sha256") != normalized_sha256:
        raise ValueError("sidecar request normalized text hash mismatch")
    if response.get("normalized_sha256") != normalized_sha256:
        raise ValueError("sidecar response normalized text hash mismatch")

    request_tokens = request.get("tokens")
    rows = response.get("rows")
    if not isinstance(request_tokens, list) or not isinstance(rows, list):
        raise ValueError("sidecar transport token rows must be arrays")
    if response.get("token_count") != len(request_tokens) or len(rows) != len(request_tokens):
        raise ValueError("sidecar response token count mismatch")

    candidates: list[tuple[str, ...]] = []
    for ordinal, (request_row, response_row) in enumerate(zip(request_tokens, rows)):
        if not isinstance(request_row, Mapping) or not isinstance(response_row, Mapping):
            raise ValueError("sidecar token row must be an object")
        token = request_row.get("text")
        if not isinstance(token, str):
            raise ValueError("sidecar request token missing text")
        expected_hash = _sha256_text(token)
        if request_row.get("ordinal") != ordinal or response_row.get("ordinal") != ordinal:
            raise ValueError("sidecar token ordinal mismatch")
        if request_row.get("sha256") != expected_hash or response_row.get("token_sha256") != expected_hash:
            raise ValueError("sidecar token identity mismatch")
        runtime_pos = response_row.get("runtime_pos")
        if not isinstance(runtime_pos, list):
            raise ValueError("sidecar runtime_pos must be an array")
        validated: list[str] = []
        for value in runtime_pos:
            if not isinstance(value, str) or not value.strip():
                raise ValueError("sidecar returned blank/non-string runtime POS")
            value = value.strip()
            if value not in KNOWN_RUNTIME_POS:
                raise ValueError(f"sidecar returned unknown runtime POS value: {value!r}")
            validated.append(value)
        candidates.append(tuple(validated))

    return analyze_pos_metrics(
        normalized,
        candidates,
        runtime_profile=PYLEM_RUNTIME_PROFILE,
    )


def build_frozen_pos_diagnostic(
    request: Mapping[str, object],
    response: Mapping[str, object],
    reference: Mapping[str, object],
    manifest: Mapping[str, object],
    *,
    scriptorium_revision: str,
) -> dict[str, object]:
    pos = consume_sidecar_response(request, response)
    expected = reference.get("expected")
    expected_pos = expected.get("pos") if isinstance(expected, Mapping) else None
    comparisons: dict[str, object] = {}
    if isinstance(expected_pos, Mapping):
        for bucket, actual_row in pos["metrics"]["buckets"].items():
            expected_row = expected_pos.get(bucket)
            if not isinstance(expected_row, Mapping):
                continue
            comparisons[bucket] = {
                "expected_count": expected_row.get("count"),
                "actual_count": actual_row["count"],
                "count_delta": actual_row["count"] - expected_row.get("count", 0),
                "expected_percent_of_defined": expected_row.get("percent_of_defined"),
                "actual_percent_of_defined": actual_row["percent_of_defined"],
                "result": "diagnostic_only",
            }
    candidate_id = manifest.get("candidate_id")
    if not isinstance(candidate_id, str) or not candidate_id:
        raise ValueError("packed manifest missing candidate_id")
    return {
        "schema_version": DIAGNOSTIC_SCHEMA,
        "candidate_id": candidate_id,
        "scriptorium_revision": scriptorium_revision,
        "source_text_included": False,
        "transport": {
            "request_schema": REQUEST_SCHEMA,
            "response_schema": RESPONSE_SCHEMA,
            "runtime_profile": PYLEM_RUNTIME_PROFILE,
            "normalized_sha256": pos["normalized_sha256"],
            "runtime_analysis_sha256": pos["runtime_analysis_sha256"],
        },
        "diagnostic_boundary": {
            "status": "diagnostic_only",
            "fantlab_source_edition_match": "unknown",
            "fantlab_dictionary_equivalence": "unknown",
            "fantlab_homonym_selection": "unresolved",
            "noun_cardinal_runtime_collision": "unresolved",
            "extra_category_folding": "unresolved",
            "m2_parity_admissible": False,
        },
        "pos": pos,
        "fantlab_bucket_comparison": comparisons,
    }


def prepare_frozen_request(manifest: Mapping[str, object]) -> dict[str, object]:
    return build_sidecar_request(replay_packed_manifest(manifest))


def _load_object(path: Path) -> dict[str, object]:
    value = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(value, dict):
        raise ValueError(f"{path} must contain a JSON object")
    return value


def _write_json(path: Path, value: Mapping[str, object]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def main(argv: Sequence[str] | None = None) -> int:
    parser = argparse.ArgumentParser()
    sub = parser.add_subparsers(dest="command", required=True)
    prepare = sub.add_parser("prepare")
    prepare.add_argument("--manifest", type=Path, required=True)
    prepare.add_argument("--request", type=Path, required=True)
    finalize = sub.add_parser("finalize")
    finalize.add_argument("--manifest", type=Path, required=True)
    finalize.add_argument("--reference", type=Path, required=True)
    finalize.add_argument("--request", type=Path, required=True)
    finalize.add_argument("--response", type=Path, required=True)
    finalize.add_argument("--scriptorium-revision", required=True)
    finalize.add_argument("--output", type=Path, required=True)
    args = parser.parse_args(argv)
    if args.command == "prepare":
        _write_json(args.request, prepare_frozen_request(_load_object(args.manifest)))
        return 0
    artifact = build_frozen_pos_diagnostic(
        _load_object(args.request),
        _load_object(args.response),
        _load_object(args.reference),
        _load_object(args.manifest),
        scriptorium_revision=args.scriptorium_revision,
    )
    _write_json(args.output, artifact)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
