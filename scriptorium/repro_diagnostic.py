"""Run a diagnostic-only FantLab comparison on a frozen public-domain source."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Mapping, Sequence

from .benchmark import build_comparison
from .wikisource_replay import replay_packed_manifest


def build_frozen_diagnostic(
    reference_json: str,
    manifest: Mapping[str, object],
    *,
    scriptorium_revision: str,
) -> dict[str, object]:
    """Replay a packed source manifest and build a fail-closed comparison artifact."""

    composite = replay_packed_manifest(manifest)
    bibliographic_source = manifest.get("bibliographic_source")
    source_work_url = manifest.get("source_work_url")
    legal_basis = manifest.get("legal_basis")
    if not isinstance(bibliographic_source, str) or not bibliographic_source.strip():
        raise ValueError("packed manifest missing bibliographic_source")
    if not isinstance(source_work_url, str) or not source_work_url.strip():
        raise ValueError("packed manifest missing source_work_url")
    if not isinstance(legal_basis, str) or not legal_basis.strip():
        raise ValueError("packed manifest missing legal_basis")

    artifact = build_comparison(
        reference_json,
        composite.encode("utf-8"),
        scriptorium_revision=scriptorium_revision,
        edition_match="unknown",
        edition_label=bibliographic_source,
        source_reference=source_work_url,
        legal_basis=legal_basis,
    )
    artifact["diagnostic_boundary"] = {
        "status": "diagnostic_only",
        "fantlab_source_edition_match": "unknown",
        "m2_parity_admissible": False,
        "reason": (
            "The replayed public-domain candidate is reproducible, but FantLab does not "
            "disclose the analyzer-input edition or bytes. Numeric deltas cannot establish parity."
        ),
    }
    return artifact


def _build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Replay a frozen Wikisource candidate and run diagnostic FantLab metrics."
    )
    parser.add_argument("--reference", type=Path, required=True)
    parser.add_argument("--manifest", type=Path, required=True)
    parser.add_argument("--scriptorium-revision", required=True)
    parser.add_argument("--output", type=Path, required=True)
    return parser


def main(argv: Sequence[str] | None = None) -> int:
    args = _build_parser().parse_args(argv)
    manifest = json.loads(args.manifest.read_text(encoding="utf-8"))
    if not isinstance(manifest, dict):
        raise ValueError("packed manifest must be a JSON object")
    artifact = build_frozen_diagnostic(
        args.reference.read_text(encoding="utf-8"),
        manifest,
        scriptorium_revision=args.scriptorium_revision,
    )
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(
        json.dumps(artifact, ensure_ascii=False, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
