"""Source-free conditional impact of pylem 0.0.18's collapsed noun/cardinal N.

Only rows containing exclusively N are varied. Mixed N and other undefined
analyses remain unknown; reported cell bounds are not jointly realizable.
"""
from __future__ import annotations

import argparse
from collections import Counter
from collections.abc import Iterable, Mapping, Sequence
import json
from pathlib import Path

from .morphology import FANTLAB_POS_BUCKETS, MAX_POSITION, _sentence_bucket_rows, resolve_runtime_pos
from .morphology_diagnostic import classify_runtime_candidates
from .pylem_provider import PYLEM_VERSION, PYLEM_RUNTIME_PROFILE
from .pylem_transport import _bind_frozen_manifest_identity, _validated_candidate_rows, consume_sidecar_response
from .text import normalize_text, sentence_spans, word_tokens

SCHEMA = "scriptorium-pylem-n-only-impact-v3"
MARKER = "<N-only>"
BUCKETS = ("noun", "cardinal")
SDIST_SHA256 = "66c0d13414006a803f200979540fcee9653738701c14496a418db67542b26515"


def rate(numerator: int, denominator: int, multiplier: int) -> float | None:
    return numerator * multiplier / denominator if denominator else None


def _max_ambiguous_pair_gain(
    sentence: Sequence[str | None], first: str, second: str,
) -> int:
    """Exact per-cell gain from N-only choices, respecting shared neighbors.

    An edge contributes only if it touches an N-only token. Fixed-fixed edges
    are already accounted for in the baseline. Dynamic programming enforces
    one noun/cardinal assignment per token across both adjacent edges.
    """
    if len(sentence) < 2 or MARKER not in sentence:
        return 0

    def choices(slot: str | None) -> tuple[str | None, ...]:
        return BUCKETS if slot == MARKER else (slot,)

    scores = {option: 0 for option in choices(sentence[0])}
    for index, current in enumerate(sentence[1:], start=1):
        variable_edge = sentence[index - 1] == MARKER or current == MARKER
        scores = {
            option: max(
                count + int(variable_edge and previous == first and option == second)
                for previous, count in scores.items()
            )
            for option in choices(current)
        }
    return max(scores.values())


def _min_ambiguous_pair_gain(
    sentence: Sequence[str | None], first: str, second: str,
) -> int:
    """Exact per-cell minimum gain from N-only choices, respecting shared neighbors.

    An edge contributes only if it touches an N-only token. Fixed-fixed edges
    are already accounted for in the baseline. Dynamic programming enforces
    one noun/cardinal assignment per token across both adjacent edges.
    """
    if len(sentence) < 2 or MARKER not in sentence:
        return 0

    def choices(slot: str | None) -> tuple[str | None, ...]:
        return BUCKETS if slot == MARKER else (slot,)

    scores = {option: 0 for option in choices(sentence[0])}
    for index, current in enumerate(sentence[1:], start=1):
        variable_edge = sentence[index - 1] == MARKER or current == MARKER
        scores = {
            option: min(
                count + int(variable_edge and previous == first and option == second)
                for previous, count in scores.items()
            )
            for option in choices(current)
        }
    return min(scores.values())


def measure_n_only_impact(
    text: str, candidate_rows: Iterable[Iterable[str]],
) -> dict[str, object]:
    normalized = normalize_text(text)
    words, sentences = word_tokens(normalized), sentence_spans(normalized)
    candidates = tuple(tuple(row) for row in candidate_rows)
    if len(candidates) != len(words):
        raise ValueError("N-only candidate count differs from word count")
    slots: list[str | None] = []
    n_only = n_mixed = 0
    for row in candidates:
        reason = classify_runtime_candidates(row)
        if reason == "runtime_n_only":
            slots.append(MARKER)
            n_only += 1
        else:
            slots.append(resolve_runtime_pos(row))
            if reason == "runtime_n_mixed":
                n_mixed += 1
    sentence_rows = _sentence_bucket_rows(words, sentences, slots)
    base_defined = sum(slot not in (None, MARKER) for slot in slots)
    assumed_defined = base_defined + n_only
    totals = Counter(slot for slot in slots if slot not in (None, MARKER))
    bucket_rows = {}
    for bucket in BUCKETS:
        fixed = totals[bucket]
        bucket_rows[bucket] = {
            "baseline_count": fixed,
            "conditional_min_count": fixed,
            "conditional_max_count": fixed + n_only,
            "baseline_percent_of_defined": rate(fixed, base_defined, 100),
            "conditional_min_percent_of_defined": rate(fixed, assumed_defined, 100),
            "conditional_max_percent_of_defined": rate(fixed + n_only, assumed_defined, 100),
        }

    def possibilities(slot: str | None) -> tuple[str, ...]:
        return BUCKETS if slot == MARKER else (() if slot is None else (slot,))

    pairs_base: Counter[tuple[str, str]] = Counter()
    pairs_possible: Counter[tuple[str, str]] = Counter()
    pos_base: Counter[tuple[int, str]] = Counter()
    pos_possible: Counter[tuple[int, str]] = Counter()
    for sentence in sentence_rows:
        for index, slot in enumerate(sentence[:MAX_POSITION], start=1):
            if slot in BUCKETS:
                pos_base[(index, slot)] += 1
            for bucket in possibilities(slot):
                if bucket in BUCKETS:
                    pos_possible[(index, bucket)] += 1
        for first, second in zip(sentence, sentence[1:]):
            if first not in (None, MARKER) and second not in (None, MARKER):
                pairs_base[(first, second)] += 1
            for left in possibilities(first):
                for right in possibilities(second):
                    pairs_possible[(left, right)] += 1
    # The v1 independent-edge sum can overestimate even one cell's maximum:
    # N N N permits at most one noun->cardinal edge, not two. Compute exact
    # per-cell maxima by selecting consistent N-only assignments per sentence.
    ambiguous_sentences = tuple(sentence for sentence in sentence_rows if MARKER in sentence)
    exact_pair_max = {
        (first, second): pairs_base[(first, second)] + sum(
            _max_ambiguous_pair_gain(sentence, first, second)
            for sentence in ambiguous_sentences
        )
        for first in FANTLAB_POS_BUCKETS for second in FANTLAB_POS_BUCKETS
        if pairs_possible[(first, second)] > pairs_base[(first, second)]
    }
    # Like maxima, minima must respect the choice shared by neighboring
    # ambiguous edges. Fixed-only counts are conservative, not always attainable.
    exact_pair_min = {
        (first, second): pairs_base[(first, second)] + sum(
            _min_ambiguous_pair_gain(sentence, first, second)
            for sentence in ambiguous_sentences
        )
        for (first, second) in exact_pair_max
    }
    bigram_rows = [
        {
            "first": first, "second": second,
            "conditional_min_raw_count": exact_pair_min[(first, second)],
            "fixed_edge_lower_bound_raw_count": pairs_base[(first, second)],
            "conditional_max_raw_count": exact_max,
            "independent_edge_upper_bound_raw_count": pairs_possible[(first, second)],
            "conditional_min_per_1000_words": rate(exact_pair_min[(first, second)], len(words), 1000),
            "conditional_max_per_1000_words": rate(exact_max, len(words), 1000),
        }
        for (first, second), exact_max in exact_pair_max.items()
    ]
    position_rows = [
        {
            "position": index, "bucket": bucket,
            "conditional_min_raw_count": pos_base[(index, bucket)],
            "conditional_max_raw_count": pos_possible[(index, bucket)],
            "conditional_min_percent_of_sentences": rate(pos_base[(index, bucket)], len(sentences), 100),
            "conditional_max_percent_of_sentences": rate(pos_possible[(index, bucket)], len(sentences), 100),
        }
        for index in range(1, MAX_POSITION + 1) for bucket in BUCKETS
        if pos_possible[(index, bucket)] > pos_base[(index, bucket)]
    ]
    return {
        "status": "diagnostic_only",
        "word_count": len(words), "sentence_count": len(sentences),
        "baseline_defined_token_count": base_defined,
        "n_only_token_count": n_only,
        "n_mixed_token_count_excluded": n_mixed,
        "n_only_percent_of_words": rate(n_only, len(words), 100),
        "conditional_defined_token_count": assumed_defined,
        "bucket_conditional_envelopes": bucket_rows,
        "bigram_conditional_envelopes": bigram_rows,
        "position_conditional_envelopes": position_rows,
        "boundary": {
            "assumption": "Only N-only rows may become noun or cardinal; other undefined rows stay unknown.",
            "cell_bounds_jointly_attainable": False,
            "bigram_max_method": "exact_per_cell_n_only_dynamic_programming",
            "bigram_min_method": "exact_per_cell_n_only_dynamic_programming",
            "independent_edge_upper_bound_retained": True,
            "n_mixed_recovered": False,
            "production_pos_mapping_changed": False,
            "fantlab_dictionary_equivalence": "unknown",
            "fantlab_homonym_selection": "unresolved",
            "m2_parity_admissible": False,
        },
    }


def build_frozen_n_only_diagnostic(
    request: Mapping[str, object], response: Mapping[str, object],
    manifest: Mapping[str, object], *, scriptorium_revision: str,
) -> dict[str, object]:
    if not isinstance(scriptorium_revision, str) or not scriptorium_revision.strip():
        raise ValueError("scriptorium_revision is required")
    _bind_frozen_manifest_identity(request, manifest)
    pos = consume_sidecar_response(request, response)
    rows = _validated_candidate_rows(response)
    measured = measure_n_only_impact(request["normalized_text"], rows)
    if measured["baseline_defined_token_count"] != pos["metrics"]["defined"]["count"]:
        raise ValueError("N-only baseline defined count drift")
    candidate_id = manifest.get("candidate_id")
    if not isinstance(candidate_id, str) or not candidate_id:
        raise ValueError("frozen manifest missing candidate_id")
    return {
        "schema_version": SCHEMA, "candidate_id": candidate_id,
        "scriptorium_revision": scriptorium_revision,
        "source_text_included": False,
        "provider": {
            "distribution": "pylem", "version": PYLEM_VERSION,
            "runtime_profile": PYLEM_RUNTIME_PROFILE, "sdist_sha256": SDIST_SHA256,
        },
        "normalized_sha256": pos["normalized_sha256"],
        "runtime_analysis_sha256": pos["runtime_analysis_sha256"],
        "impact": measured,
    }


def main(argv: Sequence[str] | None = None) -> int:
    parser = argparse.ArgumentParser()
    for flag in ("manifest", "request", "response", "output"):
        parser.add_argument("--" + flag, type=Path, required=True)
    parser.add_argument("--scriptorium-revision", required=True)
    args = parser.parse_args(argv)

    def load(path: Path) -> dict[str, object]:
        document = json.loads(path.read_text(encoding="utf-8"))
        if not isinstance(document, dict):
            raise ValueError("N-only input must be a JSON object")
        return document

    artifact = build_frozen_n_only_diagnostic(
        load(args.request), load(args.response), load(args.manifest),
        scriptorium_revision=args.scriptorium_revision,
    )
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(
        json.dumps(artifact, ensure_ascii=False, sort_keys=True, indent=2) + "\n",
        encoding="utf-8",
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
