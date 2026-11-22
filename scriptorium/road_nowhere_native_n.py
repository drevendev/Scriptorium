"""Fourth independent full-work N-only diagnostic: frozen Grin Road to Nowhere.

The one-page alternate transcription is fetched by immutable oldid, replayed
against its raw/body digests, and passed transiently to pinned pylem. Only
source-free counts, uncertainty bounds and witness IDs may be retained.
"""
from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Callable, Mapping, Sequence

from .analyze import _write_new
from . import road_nowhere_freeze as freeze
from .road_nowhere_diagnostic import _validate_pins
from .n_collision_diagnostic import (
    SCHEMA, SDIST_SHA256, measure_n_only_impact,
)
from .pylem_provider import PYLEM_VERSION, PYLEM_RUNTIME_PROFILE
from .pylem_transport import (
    _validated_candidate_rows, build_sidecar_request, consume_sidecar_response,
)

SOURCE_PATH = "corpus/candidates/source-edition-traces/grin-road-nowhere-ru.alternate-revision.json"
BODY_PATH = "corpus/candidates/source-edition-traces/grin-road-nowhere-ru.alternate-body.json"


def _bind_request(request: Mapping[str, object], identity: Mapping[str, object]) -> None:
    if (request.get("normalized_sha256") != identity.get("normalized_sha256")
            or not isinstance(request.get("normalized_text"), str)
            or len(request["normalized_text"]) != identity.get("normalized_character_count_including_spaces")
            or not isinstance(request.get("tokens"), list) or not request["tokens"]):
        raise ValueError("Road to Nowhere native input does not match the frozen literary body")


def prepare_request(
    revision: Mapping[str, object],
    body: Mapping[str, object],
    *,
    fetcher: Callable[..., dict[str, object]] = freeze.fetch_pinned_wikitext,
) -> dict[str, object]:
    """Replay once, check source/body identity before any native request exists."""
    identity = _validate_pins(revision, body)
    captured: str | None = None

    def capture(*, title: str, revision_id: int) -> dict[str, object]:
        nonlocal captured
        if captured is not None:
            raise ValueError("unexpected second Road to Nowhere fetch")
        observed = fetcher(title=title, revision_id=revision_id)
        if not isinstance(observed, dict) or not isinstance(observed.get("wikitext"), str):
            raise ValueError("pinned Road to Nowhere source text missing")
        captured = observed["wikitext"]
        return dict(observed)

    receipt = freeze.replay_body_manifest(revision, body, fetcher=capture)
    if (receipt.get("verified") is not True or captured is None
            or receipt.get("source_text_included") is not False
            or receipt.get("m2_parity_admissible") is not False):
        raise ValueError("Road to Nowhere frozen replay not accepted")
    request = build_sidecar_request(freeze.extract_literary_body(captured))
    _bind_request(request, identity)
    return request


def finalize(
    revision: Mapping[str, object],
    body: Mapping[str, object],
    request: Mapping[str, object],
    response: Mapping[str, object],
    *,
    scriptorium_revision: str,
) -> dict[str, object]:
    """Enforce witness/transport identity and keep only conditional aggregates."""
    identity = _validate_pins(revision, body)
    if not isinstance(scriptorium_revision, str) or not scriptorium_revision.strip():
        raise ValueError("scriptorium_revision is required")
    _bind_request(request, identity)
    pos = consume_sidecar_response(request, response)
    impact = measure_n_only_impact(
        request["normalized_text"], _validated_candidate_rows(response)
    )
    if impact["baseline_defined_token_count"] != pos["metrics"]["defined"]["count"]:
        raise ValueError("N-only baseline defined count drift")
    return {
        "schema_version": SCHEMA,
        "candidate_id": freeze.CANDIDATE_ID,
        "scriptorium_revision": scriptorium_revision,
        "source_text_included": False,
        "source_identity": {
            "revision_id": freeze.REVISION_ID,
            "wikitext_sha256": revision["source_identity"]["wikitext_sha256"],
            "extraction_profile": freeze.EXTRACTION_PROFILE,
            "fantlab_source_edition_match": "unknown",
        },
        "provider": {
            "distribution": "pylem", "version": PYLEM_VERSION,
            "runtime_profile": PYLEM_RUNTIME_PROFILE, "sdist_sha256": SDIST_SHA256,
        },
        "normalized_sha256": pos["normalized_sha256"],
        "runtime_analysis_sha256": pos["runtime_analysis_sha256"],
        "impact": impact,
    }


def _load(path: Path) -> dict[str, object]:
    value = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(value, dict):
        raise ValueError("native N input must be a JSON object")
    return value


def main(argv: Sequence[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    sub = parser.add_subparsers(dest="command", required=True)
    prepare = sub.add_parser("prepare")
    prepare.add_argument("--revision", type=Path, required=True)
    prepare.add_argument("--body", type=Path, required=True)
    prepare.add_argument("--request", type=Path, required=True)
    finish = sub.add_parser("finalize")
    finish.add_argument("--revision", type=Path, required=True)
    finish.add_argument("--body", type=Path, required=True)
    finish.add_argument("--request", type=Path, required=True)
    finish.add_argument("--response", type=Path, required=True)
    finish.add_argument("--scriptorium-revision", required=True)
    finish.add_argument("--output", type=Path, required=True)
    args = parser.parse_args(argv)
    revision, body = _load(args.revision), _load(args.body)
    if args.command == "prepare":
        payload = prepare_request(revision, body)
        destination = args.request
    else:
        payload = finalize(
            revision, body, _load(args.request), _load(args.response),
            scriptorium_revision=args.scriptorium_revision,
        )
        destination = args.output
    rendered = json.dumps(payload, ensure_ascii=False, sort_keys=True, indent=2, allow_nan=False) + "\n"
    try:
        _write_new(destination, rendered)
    except FileExistsError:
        parser.error("native evidence file already exists; never overwrite prior evidence")
    except OSError:
        parser.error("native evidence destination unavailable")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
