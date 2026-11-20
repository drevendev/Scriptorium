"""Private, source-free lexical contrasts; an extension, never FantLab parity.

This module deliberately never returns lexemes, top words, or per-word hashes.
A numerical distribution summary is not a substitute for a rights-cleared corpus.
"""
from __future__ import annotations

import argparse
from collections import Counter
from hashlib import sha256
import json
import math
from pathlib import Path
import re

from .analyze import MAX_ANALYSIS_BYTES, REPRESENTATIVE_CHARACTERS, _read_bounded_regular_file
from .text import NORMALIZATION_PROFILE, normalize_text
from .vocabulary import VOCABULARY_PROFILE, vocabulary_lexemes

PROFILE = "scriptorium-lexical-aggregate-contrast-v1"
TYPE_OVERLAP_PROFILE = "scriptorium-lexical-type-overlap-v1"
TOKEN_OVERLAP_PROFILE = "scriptorium-lexical-token-overlap-v1"
SCIENTIFIC_BOUNDARY = (
    "Local descriptive extension only; neither edition, translation lineage nor "
    "reuse rights are independently verified. No author fingerprint or FantLab "
    "parity (M2 0/5). Short texts remain nonrepresentative for corpus profiles."
)
SCHEMA = "scriptorium-private-lexical-contrast-v1"
MIN_POOLED_OCCURRENCES = 5
PSEUDOCOUNT = 0.5
DOMINANCE_RATIO = 2.0
_ID = re.compile(r"[A-Za-z0-9][A-Za-z0-9_./:-]{0,159}\Z")
_LANG = re.compile(r"[a-z]{2,3}\Z")


_METHOD: dict[str, object] = {
    "lexical_identity": "NFC + casefold; surface word tokens; no lemmatization or yo/e fold",
    "denominator": "all word tokens in each normalized text",
    "min_pooled_occurrences": MIN_POOLED_OCCURRENCES,
    "smoothing": "Jeffreys +0.5 per pooled type for dominance only",
    "dominance_cutoff": ">=2x normalized smoothed relative frequency",
    "divergence": "empirical Jensen-Shannon; base-2 bits, no smoothing",
    "dictionary_dependency": None,
    "type_overlap_profile": TYPE_OVERLAP_PROFILE,
    "type_overlap": "intersection / union of distinct casefolded surface forms; no rarity filter or smoothing",
    "token_overlap_profile": TOKEN_OVERLAP_PROFILE,
    "token_overlap": "sum of minima of unsmoothed per-text token shares; all surface forms, including rare",
}


def _id(value: str | None, name: str, *, required: bool = True) -> str | None:
    if value is None and not required:
        return None
    if type(value) is not str or _ID.fullmatch(value) is None:
        raise ValueError(f"{name} must be a nonempty stable ASCII identifier")
    return value


def _translator(value: str | None) -> str | None:
    if value is None:
        return None
    if type(value) is not str or not 1 <= len(value.strip()) <= 160 or any(
        ord(char) < 32 or ord(char) == 127 for char in value
    ):
        raise ValueError("invalid translator attribution")
    return value.strip()


def _witness(text: str, edition: str, original: str | None, language: str,
             translator: str | None) -> tuple[dict[str, object], Counter[str]]:
    if type(text) is not str or len(text.encode("utf-8")) > MAX_ANALYSIS_BYTES:
        raise ValueError("input must be bounded UTF-8 text")
    _id(edition, "edition")
    _id(original, "original work", required=False)
    if type(language) is not str or _LANG.fullmatch(language) is None:
        raise ValueError("invalid language identity")
    translator = _translator(translator)
    normalized = normalize_text(text)
    counts = Counter(vocabulary_lexemes(text))
    return ({
        "edition_id": edition,
        "original_work_id": original,
        "translator": translator,
        "language": language,
        "normalization_profile": NORMALIZATION_PROFILE,
        "vocabulary_profile": VOCABULARY_PROFILE,
        "normalized_sha256": sha256(normalized.encode("utf-8")).hexdigest(),
        "characters_including_spaces": len(normalized),
        "word_tokens": sum(counts.values()),
        "distinct_forms": len(counts),
        "meets_300000_character_floor": len(normalized) >= REPRESENTATIVE_CHARACTERS,
        "source_text_embedded": False,
        "metadata_verified": False,
    }, counts)


def _js_bits(a: Counter[str], b: Counter[str], na: int, nb: int,
             words: set[str]) -> float:
    contributions = []
    for word in sorted(words):
        p, q = a[word] / na, b[word] / nb
        m = (p + q) / 2
        if p:
            contributions.append(p * math.log2(p / m) / 2)
        if q:
            contributions.append(q * math.log2(q / m) / 2)
    return round(max(0.0, math.fsum(contributions)), 6)


def build_lexical_contrast(
    left_text: str, right_text: str, *,
    left_edition_id: str, right_edition_id: str,
    left_original_work_id: str | None = None,
    right_original_work_id: str | None = None,
    left_language: str = "ru", right_language: str = "ru",
    left_translator: str | None = None,
    right_translator: str | None = None,
    translation_pair: bool = False,
) -> dict[str, object]:
    """Compare locally supplied text distributions, returning aggregate counts only.

    Translation-pair mode requires independently specified matching original IDs.
    It does not prove that either edition/rights claim is authentic.
    """
    if type(translation_pair) is not bool:
        raise ValueError("translation_pair must be boolean")
    left, a = _witness(left_text, left_edition_id, left_original_work_id,
                       left_language, left_translator)
    right, b = _witness(right_text, right_edition_id, right_original_work_id,
                        right_language, right_translator)
    if left_edition_id == right_edition_id:
        if left["normalized_sha256"] != right["normalized_sha256"]:
            raise ValueError("one edition ID cannot identify two different normalized texts")
        # A stable edition ID cannot refer to contradictory declared identities,
        # even when two files happen to contain the same normalized bytes.
        if any(left[key] != right[key] for key in (
            "original_work_id", "language", "translator"
        )):
            raise ValueError("one edition ID cannot identify conflicting provenance")
        if translation_pair:
            raise ValueError("a translation pair requires two distinct edition IDs")
    na, nb = left["word_tokens"], right["word_tokens"]
    lengths = (left["characters_including_spaces"], right["characters_including_spaces"])
    ratio = round(max(lengths) / min(lengths), 6) if min(lengths) > 0 else None
    # Lexical frequencies use word-token denominators, which can diverge even
    # when the two texts have identical normalized character lengths.
    token_ratio = round(max(na, nb) / min(na, nb), 6) if min(na, nb) > 0 else None
    stats = None
    if not na or not nb:
        status = "NOT_RUN_EMPTY"
    elif left_language != right_language:
        status = "INCOMPARABLE_LANGUAGE"
    elif translation_pair and (
        left_original_work_id is None or left_original_work_id != right_original_work_id
    ):
        status = "INCOMPARABLE_TRANSLATION_LINEAGE"
    else:
        status = ("IDENTICAL_NORMALIZED_TEXT" if
                  left["normalized_sha256"] == right["normalized_sha256"]
                  else "COMPARABLE")
        vocabulary = set(a) | set(b)
        # Overlap includes rare surface forms excluded from dominance only.
        shared_forms = len(a.keys() & b.keys())
        left_only_forms = len(a) - shared_forms
        right_only_forms = len(b) - shared_forms
        type_jaccard = round(100 * shared_forms / len(vocabulary), 6)
        # The unsmoothed probability mass shared by both word-frequency
        # distributions, including forms excluded from dominance reporting.
        token_overlap = round(100 * min(1.0, math.fsum(
            min(a[word] / na, b[word] / nb) for word in sorted(vocabulary)
        )), 6)
        eligible = [w for w in vocabulary if a[w] + b[w] >= MIN_POOLED_OCCURRENCES]
        left_favored = right_favored = balanced = 0
        left_favored_tokens = right_favored_tokens = 0
        # The *same* pooled vocabulary and Jeffreys pseudocount define both
        # denominators. No per-word value or dictionary key leaves this scope.
        da = na + PSEUDOCOUNT * len(vocabulary)
        db = nb + PSEUDOCOUNT * len(vocabulary)
        for word in eligible:
            ratio_word = ((a[word] + PSEUDOCOUNT) / da) / (
                (b[word] + PSEUDOCOUNT) / db
            )
            if ratio_word >= DOMINANCE_RATIO:
                left_favored += 1
                left_favored_tokens += a[word]
            elif ratio_word <= 1 / DOMINANCE_RATIO:
                right_favored += 1
                right_favored_tokens += b[word]
            else:
                balanced += 1
        stats = {
            "eligible_form_count": len(eligible),
            "excluded_rare_form_count": len(vocabulary) - len(eligible),
            "shared_form_count": shared_forms,
            "left_only_form_count": left_only_forms,
            "right_only_form_count": right_only_forms,
            "type_jaccard_percent": type_jaccard,
            "token_distribution_overlap_percent": token_overlap,
            "left_dominant_form_count": left_favored,
            "right_dominant_form_count": right_favored,
            "balanced_form_count": balanced,
            "left_dominant_token_share_percent": round(100 * left_favored_tokens / na, 6),
            "right_dominant_token_share_percent": round(100 * right_favored_tokens / nb, 6),
            "jensen_shannon_divergence_bits": _js_bits(a, b, na, nb, vocabulary),
        }
    return {
        "schema_version": SCHEMA, "profile": PROFILE,
        "compatibility_status": "extension",
        "left": left, "right": right,
        "status": status,
        "method": dict(_METHOD),
        "length_ratio_max_over_min": ratio,
        "length_imbalance_warning": ratio is not None and ratio >= 2,
        "word_token_ratio_max_over_min": token_ratio,
        "word_token_imbalance_warning": token_ratio is not None and token_ratio >= 2,
        "corpus_admission": "NOT_VERIFIED",
        "public_release_ready": False,
        "scientific_boundary": SCIENTIFIC_BOUNDARY,
        "aggregate": stats,
    }


def render_lexical_contrast(report: dict[str, object], kind: str = "json") -> str:
    if report.get("schema_version") != SCHEMA:
        raise ValueError("unsupported lexical contrast schema")
    if kind == "json":
        return json.dumps(report, ensure_ascii=False, sort_keys=True,
                          indent=2, allow_nan=False) + "\n"
    if kind == "csv":
        from .lexical_contrast_csv import render_lexical_contrast_csv
        return render_lexical_contrast_csv(report)
    if kind in ("html", "markdown"):
        # Private reports may be re-rendered from stored JSON instead of built
        # locally. Validate all numeric aggregates, method tags and witnesses
        # before a human-readable formatter can emit untrusted field values.
        from .lexical_contrast_csv import render_lexical_contrast_csv
        render_lexical_contrast_csv(report)
    if kind == "html":
        from .lexical_contrast_html import render_lexical_contrast_html
        return render_lexical_contrast_html(report)
    if kind != "markdown":
        raise ValueError("unsupported lexical contrast format")
    token_ratio = report.get("word_token_ratio_max_over_min")
    token_ratio_label = "UNKNOWN" if token_ratio is None else str(token_ratio)
    token_note = (
        "**Caution:** Word-token counts differ by at least 2×."
        if report.get("word_token_imbalance_warning") is True else
        ("Word-token count imbalance: UNKNOWN (one or both inputs have no words)."
         if token_ratio is None else "Word-token count imbalance below 2×.")
    )
    lines = [
        "# Scriptorium · local lexical contrast", "",
        "**Extension preview — not FantLab parity, a copyright clearance, or an author fingerprint.**",
        "", f"Status: **{report['status']}**. Comparison inputs are user-declared, not verified.",
        "", f"Word-token count ratio (larger/smaller): **{token_ratio_label}**.",
        token_note,
        "", "| Observation | Value | Unit |", "| --- | ---: | --- |",
    ]
    a = report["aggregate"]
    if a is None:
        lines.append("| Lexical comparison | NOT_RUN / INCOMPARABLE | — |")
    else:
        overlap_fields = {"shared_form_count", "left_only_form_count",
                          "right_only_form_count", "type_jaccard_percent"}
        present = overlap_fields.intersection(a)
        if present and present != overlap_fields:
            raise ValueError("incomplete type-overlap measurements")
        has_token_overlap = "token_overlap_profile" in report.get("method", {})
        if ("token_distribution_overlap_percent" in a) != has_token_overlap:
            raise ValueError("incomplete token-overlap measurements")
        for label, key, unit in (
            ("Eligible shared-pool types", "eligible_form_count", "forms"),
            ("Shared surface forms", "shared_form_count", "forms"),
            ("Left-only surface forms", "left_only_form_count", "forms"),
            ("Right-only surface forms", "right_only_form_count", "forms"),
            ("Type Jaccard similarity", "type_jaccard_percent", "% of pooled types"),
            ("Token-distribution overlap", "token_distribution_overlap_percent", "% of token mass"),
            ("Excluded rare types", "excluded_rare_form_count", "forms"),
            ("Left-dominant types", "left_dominant_form_count", "forms"),
            ("Right-dominant types", "right_dominant_form_count", "forms"),
            ("Balanced types", "balanced_form_count", "forms"),
            ("Left-dominant token share", "left_dominant_token_share_percent", "% of left tokens"),
            ("Right-dominant token share", "right_dominant_token_share_percent", "% of right tokens"),
            ("Jensen–Shannon divergence", "jensen_shannon_divergence_bits", "bits (0–1)"),
        ):
            if key in overlap_fields and not present:
                continue  # Existing v1 reports without this additive extension.
            if key == "token_distribution_overlap_percent" and not has_token_overlap:
                continue  # Older v1 reports without token-overlap measurements.
            lines.append(f"| {label} | {a[key]} | {unit} |")
    lines.extend(["", report["scientific_boundary"],
                  "No word forms, rare-word hashes or source text are included.", ""])
    return "\n".join(lines)


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description="Compare local lexical aggregates without emitting any source words"
    )
    parser.add_argument("left", type=Path)
    parser.add_argument("right", type=Path)
    parser.add_argument("--left-edition", required=True)
    parser.add_argument("--right-edition", required=True)
    parser.add_argument("--left-original")
    parser.add_argument("--right-original")
    parser.add_argument("--left-translator")
    parser.add_argument("--right-translator")
    parser.add_argument("--left-language", default="ru")
    parser.add_argument("--right-language", default="ru")
    parser.add_argument("--translation-pair", action="store_true")
    parser.add_argument("--format", choices=("json", "markdown", "html", "csv"), default="json")
    parser.add_argument("--output", type=Path, help="New local output file; never overwrite")
    args = parser.parse_args(argv)
    try:
        left = _read_bounded_regular_file(args.left, MAX_ANALYSIS_BYTES, "left text").decode("utf-8")
        right = _read_bounded_regular_file(args.right, MAX_ANALYSIS_BYTES, "right text").decode("utf-8")
        result = build_lexical_contrast(
            left, right, left_edition_id=args.left_edition,
            right_edition_id=args.right_edition,
            left_original_work_id=args.left_original,
            right_original_work_id=args.right_original,
            left_translator=args.left_translator,
            right_translator=args.right_translator,
            left_language=args.left_language, right_language=args.right_language,
            translation_pair=args.translation_pair,
        )
        rendered = render_lexical_contrast(result, args.format)
        if args.output is None:
            print(rendered, end="")
        else:
            with args.output.open("x", encoding="utf-8", newline="") as destination:
                destination.write(rendered)
    except FileExistsError:
        parser.error("output already exists; choose another filename")
    except (OSError, UnicodeError, ValueError, TypeError, OverflowError):
        parser.error("local text, identity or destination invalid; no source text uploaded")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
