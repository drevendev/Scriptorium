"""Strict, local-only comparison of two Scriptorium Reader analysis JSON files.

Numbers are compared as exact JSON decimals. This is not a FantLab parity test.
"""
from __future__ import annotations

import argparse
import csv
from decimal import Decimal, InvalidOperation, localcontext
from html import escape
import io
import json
import math
from pathlib import Path
import re

from .analyze import (
    LOCAL_ANALYSIS_SCHEMA, MAX_ANALYSIS_BYTES, REPRESENTATIVE_CHARACTERS,
    LocalInputError, _read_bounded_regular_file, _write_new,
)
from .csv_safety import safe_csv_text
from .metric_labels import METRIC_LABELS
from .metrics import analyze_deterministic_metrics

SCHEMA = "scriptorium-private-comparison-v1"
MAX_REPORT_BYTES = 8 * 1024 * 1024
_HEX = re.compile(r"[0-9a-f]{64}\Z")
_DICTIONARY_METRICS = frozenset((
    "fantlab.vocabulary.active_dictionary", "fantlab.vocabulary.active_nondictionary",
    "fantlab.vocabulary.uasz_3000", "fantlab.vocabulary.uasz_10000",
    "fantlab.vocabulary.uasz_100000",
))


class CompareError(ValueError):
    """A controlled, path-private problem with local derived evidence."""


def _unique_pairs(pairs: list[tuple[str, object]]) -> dict[str, object]:
    result = {}
    for key, value in pairs:
        if key in result:
            raise CompareError("duplicate JSON object key")
        result[key] = value
    return result


def _decimal_token(token: str) -> Decimal:
    # Do not expand unreasonable scientific exponents or unbounded digit strings.
    if len(token) > 72:
        raise CompareError("numeric literal exceeds comparison bounds")
    try:
        value = Decimal(token)
    except InvalidOperation as exc:
        raise CompareError("invalid numeric literal") from exc
    if not value.is_finite() or abs(value.as_tuple().exponent) > 40:
        raise CompareError("numeric literal exceeds comparison bounds")
    return value


def _integer_token(token: str) -> int:
    if len(token) > 16:
        raise CompareError("integer literal exceeds comparison bounds")
    return int(token)


def _reject_constant(_: str):
    raise CompareError("nonfinite numeric literal")


def load_report(path: Path) -> dict[str, object]:
    raw = _read_bounded_regular_file(path, MAX_REPORT_BYTES, "analysis JSON")
    try:
        result = json.loads(raw.decode("utf-8"), object_pairs_hook=_unique_pairs,
                            parse_int=_integer_token, parse_float=_decimal_token,
                            parse_constant=_reject_constant)
    except (UnicodeError, ValueError, RecursionError) as exc:
        raise CompareError("invalid or unsupported analysis JSON") from exc
    validate_report(result)
    return result


def _obj(value: object, keys: set[str], label: str) -> dict[str, object]:
    if type(value) is not dict or set(value) != keys:
        raise CompareError(f"invalid {label} contract")
    return value


def _text(value: object, label: str, max_length: int = 160) -> str:
    if type(value) is not str or not value.strip() or len(value) > max_length:
        raise CompareError(f"invalid {label} identity")
    return value


def _sha(value: object, label: str) -> str:
    if type(value) is not str or _HEX.fullmatch(value) is None:
        raise CompareError(f"invalid {label} digest")
    return value


def _nonnegative_int(value: object, label: str, limit: int = 1_000_000_000) -> int:
    if type(value) is not int or not 0 <= value <= limit:
        raise CompareError(f"invalid {label} count")
    return value


def _number(value: object, label: str) -> Decimal | None:
    if value is None:
        return None
    if type(value) is int:
        _nonnegative_int(value, label)
        return Decimal(value)
    if type(value) is float:
        if not math.isfinite(value):
            raise CompareError(f"invalid {label} numeric value")
        value = Decimal(repr(value))
    if type(value) is not Decimal or not value.is_finite():
        raise CompareError(f"invalid {label} numeric value")
    if value < 0 or value.adjusted() > 12 or value.adjusted() < -40:
        raise CompareError(f"invalid {label} numeric domain")
    return value


def _snapshot() -> dict[str, object]:
    # The actual analyzer owns the 29-ID unit/evidence registry, not this viewer.
    return analyze_deterministic_metrics("")


def validate_report(report: object) -> None:
    doc = _obj(report, {"schema_version", "metric_contract_id", "source", "analyzer",
                        "representativeness", "metrics"}, "top-level")
    canonical = _snapshot()
    if doc["schema_version"] != LOCAL_ANALYSIS_SCHEMA or doc["metric_contract_id"] != canonical["metric_contract_id"]:
        raise CompareError("unsupported local-analysis metric contract")

    source = _obj(doc["source"], {"raw_sha256", "byte_count", "normalized_sha256",
                                  "normalized_character_count", "source_text_embedded"}, "source")
    if source["source_text_embedded"] is not False:
        raise CompareError("source text must not be embedded")
    _sha(source["raw_sha256"], "raw source")
    _sha(source["normalized_sha256"], "normalized source")
    byte_count = _nonnegative_int(source["byte_count"], "source bytes", MAX_ANALYSIS_BYTES)
    length = _nonnegative_int(source["normalized_character_count"], "normalized characters", MAX_ANALYSIS_BYTES)
    if length > byte_count:
        raise CompareError("inconsistent source size")

    analyzer = _obj(doc["analyzer"], {"scriptorium_revision", "profiles", "dependencies"}, "analyzer")
    if analyzer["scriptorium_revision"] is not None:
        _text(analyzer["scriptorium_revision"], "revision")
    profiles = _obj(analyzer["profiles"], set(canonical["profiles"]), "analyzer profiles")
    for key, value in profiles.items():
        _text(value, f"{key} profile")
    dependencies = _obj(analyzer["dependencies"], {"vocabulary_dictionary"}, "dependencies")
    dictionary = dependencies["vocabulary_dictionary"]
    if dictionary is not None:
        dictionary = _obj(dictionary, {"profile", "normalized_lexemes_sha256", "lexeme_count"}, "dictionary")
        _text(dictionary["profile"], "dictionary profile")
        _sha(dictionary["normalized_lexemes_sha256"], "dictionary")
        _nonnegative_int(dictionary["lexeme_count"], "dictionary lexemes")

    representative = _obj(doc["representativeness"], {"calibration_threshold_characters",
                         "meets_calibration_threshold", "note"}, "representativeness")
    if representative["calibration_threshold_characters"] != REPRESENTATIVE_CHARACTERS or type(representative["meets_calibration_threshold"]) is not bool or representative["meets_calibration_threshold"] != (length >= REPRESENTATIVE_CHARACTERS):
        raise CompareError("invalid representativeness status")
    _text(representative["note"], "representativeness note", 1000)

    rows = _obj(doc["metrics"], set(METRIC_LABELS), "29-metric collection")
    baseline = canonical["metrics"]
    if set(baseline) != set(METRIC_LABELS):
        raise CompareError("local metric registry drift")
    for metric_id, standard in baseline.items():
        row = _obj(rows[metric_id], set(standard), "metric row")
        for name in ("unit", "compatibility_status", "definition_evidence"):
            if row[name] != standard[name]:
                raise CompareError("metric unit or evidence contract mismatch")
        value = _number(row["value"], "metric")
        if value is not None:
            if (standard["unit"] == "percent" and value > 100) or (standard["unit"] in ("characters", "words", "sentences") and type(row["value"]) is not int):
                raise CompareError("invalid metric value domain")
        if "raw_count" in row:
            _nonnegative_int(row["raw_count"], "punctuation raw count")
    if rows["fantlab.general.characters"]["value"] != length:
        raise CompareError("character metric contradicts source identity")
    # These measures are emitted unconditionally as exact counts by the
    # canonical deterministic engine.  Treating an imported null as an
    # unavailable *rate* is valid, but treating an obligatory count as null
    # used to reach comparisons below and raise an uncontrolled TypeError.
    required_counts = (
        "fantlab.general.words",
        "scriptorium.general.sentences",
        "fantlab.vocabulary.unique_words",
    )
    for metric_id in required_counts:
        _nonnegative_int(rows[metric_id]["value"], metric_id)
    words = rows["fantlab.general.words"]["value"]
    sentences = rows["scriptorium.general.sentences"]["value"]
    unique = rows["fantlab.vocabulary.unique_words"]["value"]
    if words > length or unique > words or sentences > length:
        raise CompareError("inconsistent source/word/sentence statistics")
    # The canonical deterministic engine computes these means from nonempty,
    # non-overlapping word/sentence spans. An imported null with a positive
    # denominator, or an impossible character budget, is not an unavailable
    # metric: it is a contradictory derived report. Allow one source character
    # of headroom for binary64 division rounding on very large manuscripts.
    for metric_id, denominator in (
        ("fantlab.general.mean_word_length_chars", words),
        ("fantlab.general.mean_sentence_length_chars", sentences),
    ):
        mean = _number(rows[metric_id]["value"], metric_id)
        if denominator == 0:
            if mean is not None:
                raise CompareError("mean exists without its denominator")
        elif (mean is None or mean < 1
              or mean * Decimal(denominator) > Decimal(length + 1)):
            raise CompareError("mean contradicts word/sentence source budget")
    # Punctuation rates are exact deterministic derivatives of the same
    # exported raw event counts and word denominator (metrics-v4).  A valid
    # JSON schema/hash declaration alone does not prove this relationship.
    # Recompute the same binary64 expression used by metrics._per_1000 and
    # compare its shortest round-trip decimal, not an ad-hoc tolerance.
    for metric_id, row in rows.items():
        if not metric_id.startswith("fantlab.punctuation."):
            continue
        raw_count = row["raw_count"]
        if raw_count > length:
            raise CompareError("punctuation count exceeds normalized source")
        expected = None if words == 0 else Decimal(repr(raw_count * 1000.0 / words))
        if _number(row["value"], metric_id) != expected:
            raise CompareError("punctuation rate contradicts raw count or word denominator")

    if dictionary is None:
        if any(rows[mid]["value"] is not None for mid in _DICTIONARY_METRICS):
            raise CompareError("dictionary-dependent value without dictionary")
    else:
        active_dictionary = _nonnegative_int(
            rows["fantlab.vocabulary.active_dictionary"]["value"], "active dictionary"
        )
        active_nondictionary = _nonnegative_int(
            rows["fantlab.vocabulary.active_nondictionary"]["value"], "active nondictionary"
        )
        if active_dictionary > dictionary["lexeme_count"] or active_dictionary + active_nondictionary != unique:
            raise CompareError("dictionary partition contradicts distinct-word counts")
        for window_size in (3000, 10000, 100000):
            metric_id = f"fantlab.vocabulary.uasz_{window_size}"
            derived = _number(rows[metric_id]["value"], metric_id)
            if (derived is None) != (words < window_size):
                raise CompareError("dictionary diversity window contradicts word count")
            if derived is not None and derived > min(window_size, dictionary["lexeme_count"]):
                raise CompareError("dictionary diversity exceeds its maximum possible size")


def _digest_metadata(report: dict[str, object]) -> dict[str, object]:
    source, analyzer = report["source"], report["analyzer"]
    return {
        "raw_sha256": source["raw_sha256"],
        "normalized_sha256": source["normalized_sha256"],
        "bytes": source["byte_count"],
        "normalized_characters": source["normalized_character_count"],
        "meets_calibration_threshold": report["representativeness"]["meets_calibration_threshold"],
        "scriptorium_revision": analyzer["scriptorium_revision"],
        "profiles": dict(analyzer["profiles"]),
        "dictionary": None if analyzer["dependencies"]["vocabulary_dictionary"] is None else dict(analyzer["dependencies"]["vocabulary_dictionary"]),
    }


def _decimal_string(value: object) -> str | None:
    number = _number(value, "metric")
    return None if number is None else str(number)


def _exact_difference(left: Decimal, right: Decimal) -> str:
    """Subtract accepted decimal observations without context-precision rounding.

    JSON admits up to 72-character decimal literals and exponents up to 40.
    The Python Decimal default 28-digit context can silently round their
    difference. Derive sufficient precision from the two exact operands;
    the result is still a decimal string, never converted through float.
    """
    lowest_exponent = min(left.as_tuple().exponent, right.as_tuple().exponent)
    highest_adjusted = max(left.adjusted(), right.adjusted())
    required_digits = max(1, highest_adjusted - lowest_exponent + 1)
    with localcontext() as ctx:
        ctx.prec = max(28, required_digits)
        return str(right - left)


def _validate_cross_report_identity(left: dict[str, object], right: dict[str, object]) -> None:
    """Reject contradictions provable from digest and version identities alone.

    The reports are unauthenticated declarations; these checks do *not* prove
    either digest is truthful. They prevent an imported pair from asserting
    contradictory lengths/normalizations or deterministic values for the
    same declared normalized bytes and exact algorithm/dependency identity.
    """
    a_source, b_source = left["source"], right["source"]
    a_engine, b_engine = left["analyzer"], right["analyzer"]
    same_raw = a_source["raw_sha256"] == b_source["raw_sha256"]
    same_normalized = a_source["normalized_sha256"] == b_source["normalized_sha256"]
    if same_raw:
        if a_source["byte_count"] != b_source["byte_count"]:
            raise CompareError("same raw digest has inconsistent byte counts")
        if (a_engine["profiles"]["normalization"] == b_engine["profiles"]["normalization"]
                and not same_normalized):
            raise CompareError("same raw digest and normalization profile have different normalized digests")
    if same_normalized and a_source["normalized_character_count"] != b_source["normalized_character_count"]:
        raise CompareError("same normalized digest has inconsistent character counts")
    # Declared algorithm profiles and dictionary content determine method
    # identity.  A changed commit/revision label alone is not a declared new
    # metric algorithm: the same normalized input must still be deterministic.
    # Otherwise the comparison would silently report a nonzero difference for
    # one text despite claiming its two declared measurement methods match.
    if same_normalized and a_engine["profiles"] == b_engine["profiles"]:
        # Dictionary identity is a dependency of only five vocabulary metrics.
        # Changing it must not excuse drift in word, sentence, punctuation or
        # dialogue values for the very same normalized bytes and algorithm.
        dictionary_equal = a_engine["dependencies"] == b_engine["dependencies"]
        for metric_id in METRIC_LABELS:
            if metric_id in _DICTIONARY_METRICS and not dictionary_equal:
                continue
            a_row, b_row = left["metrics"][metric_id], right["metrics"][metric_id]
            if (_number(a_row["value"], metric_id) != _number(b_row["value"], metric_id)
                    or a_row.get("raw_count") != b_row.get("raw_count")):
                raise CompareError("same normalized input and method have contradictory measurements")


def build_comparison(left: dict[str, object], right: dict[str, object]) -> dict[str, object]:
    validate_report(left)
    validate_report(right)
    _validate_cross_report_identity(left, right)
    rows = []
    profiles_equal = left["analyzer"]["profiles"] == right["analyzer"]["profiles"]
    dictionaries_equal = left["analyzer"]["dependencies"] == right["analyzer"]["dependencies"]
    canonical_rows = _snapshot()["metrics"]
    for metric_id in sorted(METRIC_LABELS):
        unit = canonical_rows[metric_id]["unit"]
        a, b = left["metrics"][metric_id]["value"], right["metrics"][metric_id]["value"]
        a_value, b_value = _number(a, "metric"), _number(b, "metric")
        if not profiles_equal:
            status, reason = "incomparable", "Algorithm profiles differ"
        elif metric_id in _DICTIONARY_METRICS and not dictionaries_equal:
            status, reason = "incomparable", "Dictionary identities differ"
        elif a_value is None or b_value is None:
            status, reason = "unavailable", "At least one measurement is not run or undefined"
        else:
            status, reason = "comparable", "Both derived values use the same declared method"
        rows.append({
            "metric_id": metric_id,
            "label": METRIC_LABELS[metric_id],
            "unit": unit,
            "definition_evidence": canonical_rows[metric_id]["definition_evidence"],
            "compatibility_status": canonical_rows[metric_id]["compatibility_status"],
            "left": _decimal_string(a),
            "right": _decimal_string(b),
            "difference": _exact_difference(a_value, b_value) if status == "comparable" else None,
            "difference_unit": "percentage_points" if status == "comparable" and unit == "percent" else unit if status == "comparable" else None,
            "comparison_status": status,
            "reason": reason,
        })
    return {
        "schema_version": SCHEMA,
        "metric_contract_id": left["metric_contract_id"],
        "direction": "right_minus_left",
        "scientific_boundary": "Inferred/extension local measurements only; not verified FantLab parity (M2 0/5).",
        "left_source": _digest_metadata(left),
        "right_source": _digest_metadata(right),
        "metrics": rows,
    }


def render_json(comparison: dict[str, object]) -> str:
    return json.dumps(comparison, ensure_ascii=False, sort_keys=True, indent=2, allow_nan=False) + "\n"


def render_csv(comparison: dict[str, object]) -> str:
    out = io.StringIO(newline="")
    writer = csv.writer(out, lineterminator="\n")
    fields = ("metric_id", "label", "unit", "compatibility_status", "definition_evidence",
              "left", "right", "difference", "difference_unit", "comparison_status", "reason",
              "left_sha256", "right_sha256")
    writer.writerow(fields)
    for row in comparison["metrics"]:
        values = [row.get(k) for k in fields[:11]] + [comparison["left_source"]["raw_sha256"], comparison["right_source"]["raw_sha256"]]
        writer.writerow([("" if v is None else str(v) if index in (5, 6, 7) else safe_csv_text(str(v)))
                         for index, v in enumerate(values)])
    return out.getvalue()


def render_html(comparison: dict[str, object], *, title: str = "Two private analyses") -> str:
    name = escape(title)
    rows = []
    for row in comparison["metrics"]:
        def cell(key: str) -> str:
            value = row[key]
            return escape(str(value)) if value is not None else "Not available"
        rows.append(
            "<tr><th scope='row'>" + escape(row["label"]) + "<small><code>" + escape(row["metric_id"]) +
            "</code></small></th><td>" + cell("left") + "</td><td>" + cell("right") +
            "</td><td>" + cell("unit") + "</td><td>" + cell("difference") + "</td><td>" + cell("difference_unit") +
            "</td><td>" + cell("comparison_status") + "<small>" + cell("reason") + "</small></td></tr>"
        )
    def source_card(label: str, source: dict[str, object]) -> str:
        return ("<article class='card'><h2>" + escape(label) + "</h2><p><strong>Normalized characters:</strong> " +
                str(source["normalized_characters"]) + "</p><p><strong>Source SHA-256:</strong> <code>" +
                escape(source["raw_sha256"]) + "</code></p><details><summary>Reproducibility details</summary>" +
                "<p>Normalized SHA-256: <code>" + escape(source["normalized_sha256"]) + "</code></p>" +
                "<p>Declared revision: <code>" + escape(str(source["scriptorium_revision"] or "not recorded")) + "</code></p>" +
                "<p>Dictionary identity: <code>" + escape(json.dumps(source["dictionary"], ensure_ascii=False, sort_keys=True)) + "</code></p>" +
                "<p>Length meets calibration floor: " + str(source["meets_calibration_threshold"]) + "</p>" +
                "<dl>" + "".join("<dt>" + escape(k) + "</dt><dd>" + escape(v) + "</dd>"
                for k, v in sorted(source["profiles"].items())) + "</dl></details></article>")
    css = """*{box-sizing:border-box}body{margin:0;background:#f7f3ea;color:#243b34;font:16px/1.6 system-ui,sans-serif}
main{max-width:75rem;margin:auto;padding:clamp(1rem,4vw,3rem)}h1,h2{font-family:Georgia,serif;line-height:1.16}
h1{font-size:clamp(2.2rem,5vw,4rem)}.eyebrow{font-weight:700;letter-spacing:.12em;text-transform:uppercase;color:#23615b}
.lead{max-width:69ch;font-size:1.12rem}.notice{background:#e3ece7;padding:1rem 1.25rem;border-left:4px solid #35766e}
.cards{display:grid;grid-template-columns:repeat(2,minmax(0,1fr));gap:1rem;margin:2rem 0}.card{background:#fffdfa;padding:1.25rem;border:1px solid #d8d0c0;border-radius:.6rem;min-width:0}
code{overflow-wrap:anywhere}.scroll{overflow:auto;border:1px solid #d8d0c0;background:#fffdfa;border-radius:.5rem}
table{border-collapse:collapse;width:100%;min-width:50rem;font-variant-numeric:tabular-nums}th,td{text-align:left;border-bottom:1px solid #d8d0c0;padding:.75rem;vertical-align:top}caption{text-align:left;padding:1rem;font-weight:600}
small{display:block;font-size:.75rem;font-weight:400;color:#4f635a}details summary{cursor:pointer;padding:.75rem 0;min-height:44px}
.skip{position:absolute;left:-9999px}.skip:focus{left:1rem;top:1rem;background:white;padding:1rem}
:focus-visible{outline:3px solid #a15b1e;outline-offset:3px}@media(max-width:680px){.cards{grid-template-columns:1fr}}
@media(prefers-reduced-motion:reduce){*{scroll-behavior:auto!important}}"""
    return ("<!doctype html><html lang='en'><head><meta charset='utf-8'><meta name='viewport' content='width=device-width,initial-scale=1'>" +
            "<title>" + name + " · Scriptorium</title><style>" + css + "</style></head><body>" +
            "<a class='skip' href='#comparison'>Skip to comparison</a><main><p class='eyebrow'>Scriptorium / Private comparison</p>" +
            "<h1>" + name + "</h1><p class='lead'>Compare two local reports without uploading the books. " +
            "Values are exact JSON decimal observations; difference is right minus left.</p><p class='notice'>" +
            escape(comparison["scientific_boundary"]) + " Unavailable or method-incompatible values have no difference. " +
            "Percent differences are percentage points, never relative percent changes.</p>" +
            "<p>Imported JSON values and hashes are unauthenticated declarations. Rerun the analyzer on your original manuscript to verify them.</p><div class='cards'>" +
            source_card("Left report", comparison["left_source"]) + source_card("Right report", comparison["right_source"]) +
            "</div><section id='comparison' tabindex='-1' aria-labelledby='metrics-heading'><h2 id='metrics-heading'>Measurements</h2>" +
            "<div class='scroll' tabindex='0' role='region' aria-label='Comparison measurements'>" +
            "<table><caption>29 source-free metric comparisons, values and units</caption><thead><tr>" +
            "<th scope='col'>Metric</th><th scope='col'>Left</th><th scope='col'>Right</th>" +
            "<th scope='col'>Unit</th><th scope='col'>Difference</th><th scope='col'>Difference unit</th><th scope='col'>Status</th>" +
            "</tr></thead><tbody>" + "".join(rows) + "</tbody></table></div></section>" +
            "<footer><p>No tracking, server, manuscript text or FantLab parity claim.</p></footer></main></body></html>\n")


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Compare two locally generated Scriptorium Reader JSON reports.")
    parser.add_argument("left", type=Path)
    parser.add_argument("right", type=Path)
    parser.add_argument("--format", choices=("json", "html", "csv"), default="html")
    parser.add_argument("--title", default="Two private analyses")
    parser.add_argument("--output", type=Path)
    args = parser.parse_args(argv)
    try:
        comparison = build_comparison(load_report(args.left), load_report(args.right))
        rendered = {"html": lambda: render_html(comparison, title=args.title),
                    "json": lambda: render_json(comparison),
                    "csv": lambda: render_csv(comparison)}[args.format]()
        if args.output is None:
            print(rendered, end="")
        else:
            _write_new(args.output, rendered)
    except FileExistsError:
        parser.error("comparison output already exists; choose another destination")
    except (LocalInputError, CompareError):
        parser.error("invalid or unsupported local analysis JSON; check the two generated reports")
    except (OSError, UnicodeError, ValueError, TypeError, RecursionError):
        parser.error("unable to compare local analyses or create the report")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
