"""Provider-neutral FantLab-shaped POS metrics.

The profile in this module consumes pylem-style runtime POS candidate strings, but it
does not select a homonym or recover information lost by the public pylem adapter.
Every FantLab-shaped value is an explicit inferred candidate until source-matched
benchmarks demonstrate parity.
"""
from __future__ import annotations

from collections import Counter
from collections.abc import Iterable
from hashlib import sha256
import json
from typing import Final

from .text import NORMALIZATION_PROFILE, normalize_text, sentence_spans, word_tokens

POS_PROFILE: Final = "scriptorium-pos-v1"
POS_SCHEMA_VERSION: Final = "scriptorium-pos-metrics-v1"
POS_MAPPING_CONTRACT: Final = "aot-pylem-0.0.18-to-fantlab-2022-v1"
MAX_POSITION: Final = 20
FANTLAB_POS_BUCKETS: Final = (
    "noun", "adjective", "verb", "pronoun_noun", "pronoun_adjective",
    "pronoun_predicative", "cardinal", "ordinal", "adverb", "predicative",
    "preposition", "conjunction", "interjection", "introductory_word", "particle",
    "participle", "gerund",
)
DIRECT_RUNTIME_TO_BUCKET: Final = {
    "A": "adjective", "V": "verb", "P": "pronoun_noun",
    "PA": "pronoun_adjective", "P-PRED": "pronoun_predicative", "NA": "ordinal",
    "ADV": "adverb", "PRED": "predicative", "PREP": "preposition",
    "CONJ": "conjunction", "INT": "interjection", "INP": "introductory_word",
    "PARTICLE": "particle", "PARTICIPLE": "participle", "ADV_PARTICIPLE": "gerund",
}


def resolve_runtime_pos(candidates: Iterable[str]) -> str | None:
    """Resolve a token only when every runtime analysis maps to one direct bucket."""
    values = tuple(candidates)
    if not values:
        return None
    mapped: list[str] = []
    for runtime_pos in values:
        if not isinstance(runtime_pos, str):
            raise TypeError("runtime POS candidates must be strings")
        bucket = DIRECT_RUNTIME_TO_BUCKET.get(runtime_pos)
        if bucket is None:
            return None
        mapped.append(bucket)
    first = mapped[0]
    return first if all(bucket == first for bucket in mapped) else None


def analyze_pos_metrics(
    text: str,
    runtime_pos_candidates: Iterable[Iterable[str]],
    *,
    runtime_profile: str,
) -> dict[str, object]:
    """Build one ``scriptorium-pos-metrics-v1`` artifact.

    ``runtime_pos_candidates`` contains exactly one runtime-analysis sequence per
    ``scriptorium-text-v1`` word token. The aggregation layer stays provider-neutral;
    a future native adapter may supply pinned pylem values without changing these
    metric formulas.
    """
    if not isinstance(runtime_profile, str) or not runtime_profile.strip():
        raise ValueError("runtime_profile must be a non-empty string")

    normalized = normalize_text(text)
    words = word_tokens(normalized)
    sentences = sentence_spans(normalized)
    candidate_rows = tuple(tuple(row) for row in runtime_pos_candidates)
    if len(candidate_rows) != len(words):
        raise ValueError(
            "runtime_pos_candidates must contain exactly one row per Scriptorium word token"
        )

    resolved = tuple(resolve_runtime_pos(row) for row in candidate_rows)
    sentence_rows = _sentence_bucket_rows(words, sentences, resolved)
    word_count = len(words)
    sentence_count = len(sentences)
    defined_count = sum(bucket is not None for bucket in resolved)
    undefined_count = word_count - defined_count
    bucket_counts = Counter(bucket for bucket in resolved if bucket is not None)

    buckets = {
        bucket: {
            "count": bucket_counts[bucket],
            "percent_of_defined": _percent(bucket_counts[bucket], defined_count),
        }
        for bucket in FANTLAB_POS_BUCKETS
    }

    bigram_counts: Counter[tuple[str, str]] = Counter()
    for sentence in sentence_rows:
        for first, second in zip(sentence, sentence[1:]):
            if first is not None and second is not None:
                bigram_counts[(first, second)] += 1
    bigrams = {
        first: {
            second: {
                "raw_count": bigram_counts[(first, second)],
                "per_1000_words": _per_1000(bigram_counts[(first, second)], word_count),
            }
            for second in FANTLAB_POS_BUCKETS
        }
        for first in FANTLAB_POS_BUCKETS
    }

    positions: dict[str, dict[str, dict[str, int | float | None]]] = {}
    for position in range(1, MAX_POSITION + 1):
        counts: Counter[str] = Counter()
        index = position - 1
        for sentence in sentence_rows:
            if index < len(sentence) and sentence[index] is not None:
                counts[sentence[index]] += 1
        positions[str(position)] = {
            bucket: {
                "raw_count": counts[bucket],
                "percent": _percent(counts[bucket], sentence_count),
            }
            for bucket in FANTLAB_POS_BUCKETS
        }

    canonical_candidates = json.dumps(
        candidate_rows,
        ensure_ascii=False,
        separators=(",", ":"),
    ).encode("utf-8")

    return {
        "schema_version": POS_SCHEMA_VERSION,
        "metric_contract_id": "fantlab-2022-v1",
        "profile": POS_PROFILE,
        "text_profile": NORMALIZATION_PROFILE,
        "normalized_sha256": sha256(normalized.encode("utf-8")).hexdigest(),
        "mapping_contract": POS_MAPPING_CONTRACT,
        "runtime_profile": runtime_profile.strip(),
        "runtime_analysis_sha256": sha256(canonical_candidates).hexdigest(),
        "compatibility_status": "inferred",
        "input": {
            "word_count": word_count,
            "sentence_count": sentence_count,
        },
        "metrics": {
            "undefined": {
                "count": undefined_count,
                "percent_of_words": _percent(undefined_count, word_count),
            },
            "defined": {
                "count": defined_count,
                "percent_of_words": _percent(defined_count, word_count),
            },
            "service_words": {
                "count": None,
                "percent_of_defined": None,
                "status": "unresolved",
                "reason": "FantLab's exact POS-to-service aggregation is not established.",
            },
            "buckets": buckets,
            "bigrams": bigrams,
            "positions": positions,
        },
    }


def _sentence_bucket_rows(words, sentences, resolved):
    rows: list[list[str | None]] = [[] for _ in sentences]
    sentence_index = 0
    for token, bucket in zip(words, resolved):
        while sentence_index < len(sentences) and token.start >= sentences[sentence_index].end:
            sentence_index += 1
        if sentence_index >= len(sentences):
            raise ValueError("word token is not covered by a sentence candidate")
        sentence = sentences[sentence_index]
        if token.start < sentence.start or token.end > sentence.end:
            raise ValueError("word token crosses a sentence candidate boundary")
        rows[sentence_index].append(bucket)
    return tuple(tuple(row) for row in rows)


def _percent(part: int, whole: int) -> float | None:
    if whole == 0:
        return None
    return part * 100.0 / whole


def _per_1000(count: int, word_count: int) -> float | None:
    if word_count == 0:
        return None
    return count * 1000.0 / word_count
