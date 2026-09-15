"""Diagnostic-only POS view for FantLab's documented full methodology inventory.

FantLab article 374 documents five POS statistics that are absent from the observed
17-bucket work-page surface but exist as standalone categories in pinned AOT/pylem:
postpositions, phrasal verbs/collocations, short adjectives, short participles and
infinitives.  This module measures those source-backed categories without changing the
existing work-page-compatible ``scriptorium-pos-v1`` contract.

Runtime ``N`` remains unresolved because pinned AOT renders both noun and cardinal
numeral to the same Latin string.  Cross-category homonyms also remain fail-closed.
"""
from __future__ import annotations

import argparse
from collections import Counter
import json
from pathlib import Path
from typing import Final, Iterable, Mapping, Sequence

from .morphology import DIRECT_RUNTIME_TO_BUCKET, FANTLAB_POS_BUCKETS, resolve_runtime_pos
from .pylem_transport import consume_sidecar_response
from .text import NORMALIZATION_PROFILE

METHODOLOGY_DIAGNOSTIC_SCHEMA: Final = "scriptorium-fantlab-methodology-pos-diagnostic-v1"
FROZEN_METHODOLOGY_DIAGNOSTIC_SCHEMA: Final = (
    "scriptorium-frozen-fantlab-methodology-pos-diagnostic-v1"
)
FANTLAB_METHODOLOGY_SOURCE: Final = "https://fantlab.ru/article374"

EXTRA_RUNTIME_TO_METHODOLOGY_BUCKET: Final = {
    "POSL": "postposition",
    "COLLOC": "phrasal_verb",
    "ADJ_SHORT": "short_adjective",
    "PARTICIPLE_SHORT": "short_participle",
    "INFINITIVE": "infinitive",
}

METHODOLOGY_RUNTIME_TO_BUCKET: Final = {
    **DIRECT_RUNTIME_TO_BUCKET,
    **EXTRA_RUNTIME_TO_METHODOLOGY_BUCKET,
}

METHODOLOGY_POS_BUCKETS: Final = (
    "noun",
    "adjective",
    "verb",
    "pronoun_noun",
    "pronoun_adjective",
    "pronoun_predicative",
    "cardinal",
    "ordinal",
    "adverb",
    "predicative",
    "preposition",
    "postposition",
    "conjunction",
    "interjection",
    "introductory_word",
    "phrasal_verb",
    "particle",
    "short_adjective",
    "participle",
    "gerund",
    "short_participle",
    "infinitive",
)


def resolve_methodology_runtime_pos(candidates: Iterable[str]) -> str | None:
    """Resolve only unanimous candidates on the documented full methodology surface."""
    values = tuple(candidates)
    if not values:
        return None
    mapped: list[str] = []
    for runtime_pos in values:
        if not isinstance(runtime_pos, str):
            raise TypeError("runtime POS candidates must be strings")
        bucket = METHODOLOGY_RUNTIME_TO_BUCKET.get(runtime_pos)
        if bucket is None:
            return None
        mapped.append(bucket)
    first = mapped[0]
    return first if all(bucket == first for bucket in mapped) else None


def analyze_methodology_pos_signal(
    request: Mapping[str, object],
    response: Mapping[str, object],
) -> dict[str, object]:
    """Measure the source-backed full methodology view without altering production POS."""
    observed_surface = consume_sidecar_response(request, response)
    rows = response.get("rows")
    if not isinstance(rows, list):
        raise ValueError("sidecar response token rows must be an array")

    runtime_rows: list[tuple[str, ...]] = []
    for row in rows:
        if not isinstance(row, Mapping):
            raise ValueError("sidecar response token row must be an object")
        values = row.get("runtime_pos")
        if not isinstance(values, list):
            raise ValueError("sidecar response runtime_pos must be an array")
        runtime_rows.append(tuple(str(value) for value in values))

    methodology_resolved = tuple(
        resolve_methodology_runtime_pos(row) for row in runtime_rows
    )
    observed_resolved = tuple(resolve_runtime_pos(row) for row in runtime_rows)
    methodology_counts = Counter(
        bucket for bucket in methodology_resolved if bucket is not None
    )
    defined_count = sum(bucket is not None for bucket in methodology_resolved)
    token_count = len(methodology_resolved)
    undefined_count = token_count - defined_count
    observed_defined_count = int(observed_surface["metrics"]["defined"]["count"])
    additional_defined_count = sum(
        methodology is not None and observed is None
        for methodology, observed in zip(methodology_resolved, observed_resolved)
    )

    if defined_count < observed_defined_count:
        raise AssertionError("full methodology view cannot define fewer rows than observed surface")
    if defined_count - observed_defined_count != additional_defined_count:
        raise AssertionError("methodology additional-defined accounting mismatch")

    buckets: dict[str, dict[str, object]] = {}
    for bucket in METHODOLOGY_POS_BUCKETS:
        if bucket in {"noun", "cardinal"}:
            buckets[bucket] = {
                "count": None,
                "status": "unresolved_runtime_n_collision",
            }
        else:
            buckets[bucket] = {
                "count": methodology_counts[bucket],
                "status": "diagnostic_resolved",
            }

    extra_counts = {
        bucket: methodology_counts[bucket]
        for bucket in EXTRA_RUNTIME_TO_METHODOLOGY_BUCKET.values()
    }
    return {
        "schema_version": METHODOLOGY_DIAGNOSTIC_SCHEMA,
        "status": "diagnostic_only",
        "fantlab_methodology_source": FANTLAB_METHODOLOGY_SOURCE,
        "token_count": token_count,
        "defined_count": defined_count,
        "undefined_count": undefined_count,
        "observed_work_page_surface_defined_count": observed_defined_count,
        "additional_methodology_defined_count": additional_defined_count,
        "extra_methodology_bucket_counts": extra_counts,
        "buckets": buckets,
        "evidence_boundary": {
            "methodology_category_names": "source_backed",
            "current_work_page_surface_relation": "unknown",
            "production_pos_profile_changed": False,
            "runtime_n_resolution": "unresolved",
            "fantlab_homonym_selection": "unresolved",
            "fantlab_dictionary_equivalence": "unknown",
            "m2_parity_admissible": False,
        },
    }


def build_frozen_methodology_pos_diagnostic(
    request: Mapping[str, object],
    response: Mapping[str, object],
    manifest: Mapping[str, object],
    *,
    scriptorium_revision: str,
) -> dict[str, object]:
    composite_identity = manifest.get("composite_identity")
    candidate_id = manifest.get("candidate_id")
    if not isinstance(composite_identity, Mapping):
        raise ValueError("packed manifest missing composite_identity")
    if not isinstance(candidate_id, str) or not candidate_id:
        raise ValueError("packed manifest missing candidate_id")
    if composite_identity.get("normalization_profile") != NORMALIZATION_PROFILE:
        raise ValueError("packed manifest normalization profile mismatch")
    if request.get("normalized_sha256") != composite_identity.get("normalized_sha256"):
        raise ValueError("methodology POS request is not bound to frozen manifest identity")

    return {
        "schema_version": FROZEN_METHODOLOGY_DIAGNOSTIC_SCHEMA,
        "candidate_id": candidate_id,
        "scriptorium_revision": scriptorium_revision,
        "normalized_sha256": request["normalized_sha256"],
        "source_text_included": False,
        "methodology_pos": analyze_methodology_pos_signal(request, response),
        "diagnostic_boundary": {
            "status": "diagnostic_only",
            "fantlab_source_edition_match": "unknown",
            "current_work_page_surface_relation": "unknown",
            "production_pos_profile_changed": False,
            "m2_parity_admissible": False,
        },
    }


def _load_object(path: Path) -> dict[str, object]:
    value = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(value, dict):
        raise ValueError(f"{path} must contain a JSON object")
    return value


def main(argv: Sequence[str] | None = None) -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--manifest", type=Path, required=True)
    parser.add_argument("--request", type=Path, required=True)
    parser.add_argument("--response", type=Path, required=True)
    parser.add_argument("--scriptorium-revision", required=True)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args(argv)
    artifact = build_frozen_methodology_pos_diagnostic(
        _load_object(args.request),
        _load_object(args.response),
        _load_object(args.manifest),
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
