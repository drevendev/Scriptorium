"""Run a diagnostic-only FantLab comparison on a frozen public-domain source."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Mapping, Sequence

from .benchmark import build_comparison
from .boundary_probe import analyze_boundary_probe
from .dialogue_diagnostic import analyze_dialogue_policy
from .policy_diagnostic import analyze_word_dash_policy
from .wikisource_replay import replay_packed_manifest


def build_frozen_diagnostic(
    reference_json: str,
    manifest: Mapping[str, object],
    *,
    scriptorium_revision: str,
    include_boundary_sensitivity: bool = False,
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

    expected_words = _expected_numeric(artifact, "fantlab.general.words")
    expected_dash_rate = _expected_numeric(
        artifact, "fantlab.punctuation.dash.per_1000_words"
    )
    artifact["policy_sensitivity"] = analyze_word_dash_policy(
        composite,
        expected_word_count=(expected_words if isinstance(expected_words, int) else None),
        expected_dash_per_1000_words=(
            float(expected_dash_rate) if expected_dash_rate is not None else None
        ),
    )

    if include_boundary_sensitivity:
        # Reuse the exact already-fetched, identity-verified composite. A second
        # 239-revision provider replay would add load and risk source drift.
        source_identity = manifest.get("composite_identity")
        if not isinstance(source_identity, Mapping):
            raise ValueError("frozen boundary evidence requires a source identity")
        probe = analyze_boundary_probe(composite)
        if (
            probe["normalized_sha256"] != source_identity.get("normalized_sha256")
            or probe["normalized_characters_including_spaces"]
            != source_identity.get("normalized_character_count_including_spaces")
        ):
            raise ValueError("frozen boundary source identity mismatch")
        previous = artifact["policy_sensitivity"]["word_policy"]["variants"]
        observed = {row["id"]: row["word_count"] for row in probe["variants"]}
        for probe_key, policy_key in (
            ("current_scriptorium_text_v1", "current_scriptorium_text_v1"),
            ("exclude_numeric_only", "exclude_numeric_only_tokens"),
            ("join_unicode_hyphens", "join_unicode_hyphen_connectors"),
        ):
            if observed[probe_key] != previous[policy_key]["count"]:
                raise ValueError("frozen boundary baseline differs from policy diagnostic")
        artifact["word_boundary_sensitivity"] = probe

    expected_dialogue_share = _expected_numeric(
        artifact, "fantlab.dialogue.share_percent"
    )
    expected_author_text_inside_dialogue = _expected_numeric(
        artifact, "fantlab.dialogue.author_text_inside_dialogue_percent"
    )
    artifact["dialogue_sensitivity"] = analyze_dialogue_policy(
        composite,
        expected_dialogue_share_percent=(
            float(expected_dialogue_share)
            if expected_dialogue_share is not None
            else None
        ),
        expected_author_text_inside_dialogue_percent=(
            float(expected_author_text_inside_dialogue)
            if expected_author_text_inside_dialogue is not None
            else None
        ),
    )
    return artifact


def _expected_numeric(artifact: Mapping[str, object], metric_id: str) -> int | float | None:
    metrics = artifact.get("metrics")
    if not isinstance(metrics, Mapping):
        return None
    row = metrics.get(metric_id)
    if not isinstance(row, Mapping):
        return None
    expected = row.get("expected")
    if not isinstance(expected, Mapping):
        return None
    value = expected.get("numeric_value")
    if isinstance(value, bool) or not isinstance(value, (int, float)):
        return None
    return value


def _build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Replay a frozen Wikisource candidate and run diagnostic FantLab metrics."
    )
    parser.add_argument("--reference", type=Path, required=True)
    parser.add_argument("--manifest", type=Path, required=True)
    parser.add_argument("--scriptorium-revision", required=True)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--with-boundary-probe", action="store_true", help="append source-free same-input word-boundary sensitivity to the verified replay")
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
        include_boundary_sensitivity=args.with_boundary_probe,
    )
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(
        json.dumps(artifact, ensure_ascii=False, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
