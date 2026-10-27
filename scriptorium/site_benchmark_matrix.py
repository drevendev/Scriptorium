"""Canonical source-free FantLab evidence page for the static Scriptorium site.

This is a diagnostic display of independently retained evidence, never an
assertion of source-matched parity. The underlying matrix validates its inputs.
"""
from __future__ import annotations

import csv
import html
import io
import json
from decimal import Decimal, ROUND_HALF_UP
from pathlib import Path
from urllib.parse import urlsplit

from . import benchmark_metric_matrix as matrix
from . import benchmark_readiness
from .site_metric_filter import FILTER_CONTROLS, WAVE_FILTER_CONTROLS
from .site_shared_metric_filter import CONTROLS as SHARED_CONTROLS
from .benchmark import _reference_specs


EXPECTED_ENTRY = {
    "entry_id": "fantlab-five-work-retained-evidence-v1",
    "kind": "benchmark_matrix",
    "slug": "fantlab-evidence",
    "title": "FantLab evidence — five frozen works",
    "artifact_schema": matrix.SCHEMA_VERSION,
    "publication_status": "diagnostic",
    "benchmark_admissibility": "diagnostic_only",
    "corpus_admissibility": "not_admissible",
    "compatibility_claim": "inferred",
    "source_text_included": False,
}



# Display labels come from the versioned benchmark comparison registry.
# They do not establish FantLab definition equivalence or parity.
_METRIC_PRESENTATION = {
    metric_id: (label, metric_id.split(".")[1].title())
    for metric_id, _path, label, _rule in _reference_specs()
}
# Scriptorium candidate units for the retained comparison registry. These are
# *not* evidence that FantLab uses identical segmentation or denominators.
# New non-punctuation metric families require an explicit reviewed unit decision.
_VALUE_UNITS = {
    "fantlab.general.characters": "characters including spaces",
    "fantlab.general.words": "word tokens",
    "fantlab.general.mean_word_length_chars": "characters / word",
    "fantlab.general.mean_sentence_length_chars": "characters / sentence",
    "fantlab.dialogue.mean_narration_sentence_length_chars": "characters / narration sentence",
    "fantlab.dialogue.mean_dialogue_sentence_length_chars": "characters / dialogue sentence",
    "fantlab.dialogue.share_percent": "%",
    "fantlab.dialogue.author_text_inside_dialogue_percent": "%",
    "fantlab.vocabulary.unique_words": "unique word forms",
    "fantlab.vocabulary.active_dictionary": "dictionary word forms",
    "fantlab.vocabulary.active_nondictionary": "non-dictionary word forms",
    "fantlab.vocabulary.uasz_3000": "mean unique forms / 3,000-token window",
    "fantlab.vocabulary.uasz_10000": "mean unique forms / 10,000-token window",
    "fantlab.vocabulary.uasz_100000": "mean unique forms / 100,000-token window",
    **{
        metric_id: "occurrences / 1,000 word tokens"
        for metric_id in _METRIC_PRESENTATION
        if metric_id.startswith("fantlab.punctuation.")
    },
}
if set(_VALUE_UNITS) != set(_METRIC_PRESENTATION):
    raise ValueError("retained benchmark unit registry changed without review")

_DISPLAY_STATUS = {
    "UNRESOLVED_SOURCE": "Input identity unverified",
    "UNRESOLVED_NO_ACTUAL": "Actual value unavailable",
    "NOT_RUN": "Not run",
    "MEASURED_NO_REFERENCE": "FantLab reference unavailable",
}

def validate_entry(entry: object) -> None:
    """The public report must be explicitly and exactly registered."""
    if not isinstance(entry, dict) or entry != EXPECTED_ENTRY:
        raise ValueError("unrecognized FantLab evidence publication registration")


def _esc(value: object) -> str:
    return html.escape(str(value), quote=True)


def _number(value: object) -> str:
    return "NOT_RUN" if value is None else _esc(value)


def _relative_character_delta(delta: int, displayed: int) -> str:
    """Signed drift against a displayed count, not a FantLab parity metric."""
    if type(delta) is not int or type(displayed) is not int or displayed <= 0:
        raise ValueError("invalid relative character-count diagnostic")
    percent = (Decimal(delta) * 100 / Decimal(displayed)).quantize(
        Decimal("0.01"), rounding=ROUND_HALF_UP
    )
    return f"{percent:+.2f}%" if delta != 0 else "0.00%"


def _shared_normalized_rows(left_rows: list[dict], right_rows: list[dict]) -> list[dict]:
    """Compare only observed, nominally length-normalized Scriptorium metrics.

    This describes two different public transcriptions, not FantLab parity,
    author voice or comparable source identity. Raw totals and vocabulary
    cardinalities are deliberately excluded because work lengths differ.
    """
    left = {row["metric_id"]: row for row in left_rows}
    right = {row["metric_id"]: row for row in right_rows}
    if len(left) != len(left_rows) or len(right) != len(right_rows):
        raise ValueError("duplicate cross-work metric identity")
    pairs = []
    for metric_id, (label, family) in _METRIC_PRESENTATION.items():
        unit = _VALUE_UNITS[metric_id]
        if not (unit == "%" or unit.startswith((
            "characters / ", "occurrences / 1,000 word tokens",
            "mean unique forms / ",
        ))):
            continue
        lrow, rrow = left.get(metric_id), right.get(metric_id)
        if lrow is None or rrow is None:
            continue
        if lrow["actual"] is None or rrow["actual"] is None:
            continue
        if lrow["result"] != "UNRESOLVED_SOURCE" or rrow["result"] != "UNRESOLVED_SOURCE":
            raise ValueError("cross-work values cannot be promoted to parity")
        observed = (lrow["actual"], rrow["actual"])
        if any(type(value) not in (int, float) for value in observed):
            raise ValueError("invalid cross-work numeric observation")
        numbers = tuple(Decimal(str(value)) for value in observed)
        if not all(number.is_finite() for number in numbers):
            raise ValueError("non-finite cross-work numeric observation")
        delta = numbers[1] - numbers[0]
        pairs.append({
            "metric_id": metric_id,
            "label": label,
            "family": family,
            "unit": unit,
            "left": observed[0],
            "right": observed[1],
            "right_minus_left": ("+" if delta > 0 else "") + format(delta, "f") if delta else "0",
            "difference_unit": "percentage points" if unit == "%" else unit,
        })
    return pairs



def _shared_rate_exports(rows: list[dict], anna: dict, wave: dict) -> tuple[str, str]:
    """Portable, source-free 20-rate comparison; source identity remains unknown."""
    if len(rows) != 20 or len({r["metric_id"] for r in rows}) != 20:
        raise ValueError("shared rate export requires twenty distinct measured rows")
    if (anna["candidate_id"], wave["candidate_id"]) != (
        "tolstoy-anna-karenina-ru", "grin-running-on-waves-ru"
    ):
        raise ValueError("shared rate export source order changed")
    works = []
    for item in (anna, wave):
        if item["exact_fantlab_input_identity"] != "UNKNOWN":
            raise ValueError("shared rate export cannot claim proven FantLab input identity")
        works.append({
            "candidate_id": item["candidate_id"],
            "frozen_raw_sha256": item["source_witness_sha256"],
            "fantlab_reference_url": item["reference_url"],
            "fantlab_reference_date": item["reference_date"],
            "fantlab_input_identity": "UNKNOWN",
        })
    document = {
        "schema_version": "scriptorium-shared-rate-comparison-v1",
        "comparison_direction": "running_on_waves_minus_anna_karenina",
        "evidence_class": "diagnostic_source_unmatched",
        "m2_parity_admissible": False,
        "m2_weight": 0,
        "units_note": "Percent-valued differences are percentage points; other differences use the listed candidate unit.",
        "works": works,
        "measurements": rows,
    }
    json_text = json.dumps(document, ensure_ascii=False, indent=2,
                           sort_keys=True, allow_nan=False) + "\n"
    output = io.StringIO(newline="")
    writer = csv.writer(output, lineterminator="\n")
    writer.writerow(("left_candidate_id", "right_candidate_id", "left_source_sha256",
                     "right_source_sha256", "metric_id", "label", "family", "unit",
                     "anna_actual", "waves_actual", "waves_minus_anna_exact_decimal",
                     "difference_unit", "evidence_class", "fantlab_input_identity",
                     "left_fantlab_reference_url", "right_fantlab_reference_url",
                     "left_fantlab_reference_date", "right_fantlab_reference_date",
                     "schema_version", "m2_parity_admissible", "m2_weight"))
    for row in rows:
        writer.writerow((works[0]["candidate_id"], works[1]["candidate_id"],
                         works[0]["frozen_raw_sha256"], works[1]["frozen_raw_sha256"],
                         row["metric_id"], row["label"], row["family"], row["unit"],
                         str(row["left"]), str(row["right"]), row["right_minus_left"],
                         row["difference_unit"], "diagnostic_source_unmatched", "UNKNOWN",
                         works[0]["fantlab_reference_url"], works[1]["fantlab_reference_url"],
                         works[0]["fantlab_reference_date"], works[1]["fantlab_reference_date"],
                         "scriptorium-shared-rate-comparison-v1", "false", "0"))
    return json_text, output.getvalue()


def _reference(url: object) -> str:
    if not isinstance(url, str):
        raise ValueError("missing FantLab reference URL")
    parsed = urlsplit(url)
    if (parsed.scheme != "https" or parsed.netloc not in ("fantlab.ru", "www.fantlab.ru")
            or parsed.username or parsed.password or not parsed.path.startswith("/work")):
        raise ValueError("unsafe FantLab reference URL")
    return '<a href="' + _esc(url) + '" rel="noopener noreferrer">FantLab reference ↗</a>'


def _source_link(url: object) -> str:
    """Only show already-validated Wikisource source/rights links."""
    if not isinstance(url, str):
        raise ValueError("missing public source URL")
    parsed = urlsplit(url)
    if (parsed.scheme != "https" or parsed.netloc != "ru.wikisource.org"
            or parsed.username or parsed.password or not parsed.path.startswith("/wiki/")):
        raise ValueError("unsafe public source URL")
    return '<a href="' + _esc(url) + '" rel="noopener noreferrer">Public-domain source ↗</a>'


def build(root: Path) -> dict[str, str]:
    """Render verified source-free data into a readable offline HTML and downloads."""
    report = matrix.build_metric_matrix(root)
    readiness = benchmark_readiness.build_readiness(root)
    entries = report["entries"]
    sources = readiness["entries"]
    if (readiness["works_reported"] != 5
            or readiness["m2_source_matched_pass_count"] != 0
            or len(sources) != 5
            or len({row["candidate_id"] for row in sources}) != 5
            or {row["candidate_id"] for row in sources} !=
               {row["candidate_id"] for row in entries}):
        raise ValueError("five-work source readiness gate changed")
    sources_by_id = {row["candidate_id"]: row for row in sources}
    if (report["schema_version"] != matrix.SCHEMA_VERSION
            or report["m2_source_matched_pass_count"] != 0
            or report["works_reported"] != 5
            or report["works_with_retained_metric_diagnostics"] != 4
            or report["retained_metric_rows"] != 113
            or len(entries) != 5):
        raise ValueError("FantLab evidence publication gate has changed")

    anna = next(
        (entry for entry in entries if entry["candidate_id"] == "tolstoy-anna-karenina-ru"),
        None,
    )
    if (anna is None or len(anna["metric_rows"]) != 28
            or anna["metric_rows_with_actual"] != 23
            or anna["metric_rows_without_actual"] != 5):
        raise ValueError("retained Anna diagnostic coverage changed")

    wave = next(
        (entry for entry in entries if entry["candidate_id"] == "grin-running-on-waves-ru"),
        None,
    )
    if (wave is None or len(wave["metric_rows"]) != 27
            or wave["metric_rows_with_actual"] != 23
            or wave["metric_rows_without_actual"] != 4
            or {r["metric_id"] for r in wave["metric_rows"]} !=
               set(_METRIC_PRESENTATION) - {"fantlab.vocabulary.uasz_100000"}):
        raise ValueError("retained Running on Waves diagnostic coverage changed")

    silver = next(
        (entry for entry in entries if entry["candidate_id"] == "bely-silver-dove-ru"), None
    )
    if (silver is None or len(silver["metric_rows"]) != 29
            or silver["metric_rows_with_actual"] != 24
            or silver["metric_rows_without_actual"] != 5
            or {r["metric_id"] for r in silver["metric_rows"]}
               != set(_METRIC_PRESENTATION) | {"scriptorium.general.sentences"}):
        raise ValueError("retained Silver Dove diagnostic coverage changed")

    karamazov = next(
        (entry for entry in entries if entry["candidate_id"] == "dostoevsky-brothers-karamazov-ru"),
        None,
    )
    if (karamazov is None or len(karamazov["metric_rows"]) != 29
            or karamazov["metric_rows_with_actual"] != 24
            or karamazov["metric_rows_without_actual"] != 5
            or {r["metric_id"] for r in karamazov["metric_rows"]}
               != set(_METRIC_PRESENTATION) | {"scriptorium.general.sentences"}):
        raise ValueError("retained Brothers Karamazov diagnostic coverage changed")

    works = []
    for item in entries:
        reference_tag = _reference(item["reference_url"])
        witness = sources_by_id[item["candidate_id"]]
        source = witness["source"]
        diagnostic = witness["character_count_diagnostic"]
        if (witness["exact_fantlab_input_identity"] != "UNKNOWN"
                or witness["parity_eligible"] is not False
                or witness["other_metric_comparisons"] != "NOT_RUN"
                or witness["fantlab"]["reference_url"] != item["reference_url"]
                or witness["fantlab"]["analysis_date"] != item["reference_date"]
                or source["raw_sha256"] != item["source_witness_sha256"]):
            raise ValueError("source readiness and metric matrix disagree")
        frozen = diagnostic["actual_frozen_body"]
        displayed = diagnostic["expected_displayed"]
        delta = diagnostic["actual_minus_expected"]
        if (type(frozen) is not int or type(displayed) is not int
                or type(delta) is not int or frozen < 300_000
                or displayed <= 0 or delta != frozen - displayed
                or diagnostic["result"] != "UNRESOLVED_SOURCE"
                or diagnostic["rule"] != "displayed-character-count-diagnostic-only"
                or source["legal_basis"] != "public_domain"
                or not isinstance(source["legal_evidence"], str)
                or not source["legal_evidence"].strip()):
            raise ValueError("invalid source readiness diagnostic")
        status = item["metric_evidence"]
        if item["exact_fantlab_input_identity"] != "UNKNOWN" or status not in (
            "RETAINED_DIAGNOSTIC", "NOT_RUN"
        ):
            raise ValueError("unproven source identity or metric evidence was upgraded")
        if status == "NOT_RUN" and item["metric_rows"]:
            raise ValueError("unreported metric run has fabricated rows")
        measured = str(item["metric_rows_with_actual"]) if item["metric_rows"] else "NOT_RUN"
        edition = source["edition"] or "Edition not established"
        works.append(
            '<tr class="source-row"><th scope="row">' + _esc(item["title"]) +
            '<span class="eyebrow">' + _esc(item["author"]) + '</span><br><small>' +
            'Edition: ' + _esc(edition) + ' · public domain<br>' +
            _source_link(source["url"]) + '</small></th><td>' +
            '<strong>Frozen:</strong> ' + _esc(f"{frozen:,}") +
            '<br><strong>FantLab displayed:</strong> ' + _esc(f"{displayed:,}") +
            '<br><strong>Δ:</strong> ' + _esc(f"{delta:+,}") +
            '<br><strong>Relative drift:</strong> ' +
            _esc(_relative_character_delta(delta, displayed)) +
            '</td><td>' + _esc(status) + '</td><td>' + measured +
            '</td><td>UNKNOWN</td><td>' +
            reference_tag + '<br><small>' +
            _esc(item["reference_date"]) + '</small></td></tr>'
        )

    if {row["metric_id"] for row in anna["metric_rows"]} != set(_METRIC_PRESENTATION):
        raise ValueError("unrecognized FantLab metric ID in evidence page")
    metrics = []
    families = {}
    coverage = {}
    for row in anna["metric_rows"]:
        if row["comparison_kind"] != "DIAGNOSTIC_ONLY" or row["display_rounding_evidence"] != "UNKNOWN":
            raise ValueError("metric evidence was promoted without source/rounding proof")
        status = row["result"]
        if (status not in _DISPLAY_STATUS or
                (row["actual"] is None) != (status != "UNRESOLVED_SOURCE")):
            raise ValueError("invalid diagnostic scientific status")
        label, group = _METRIC_PRESENTATION[row["metric_id"]]
        family_slug = group.lower()
        first_in_family = family_slug not in families
        families[family_slug] = families.get(family_slug, 0) + 1
        tally = coverage.setdefault(family_slug, {"measured": 0, "not_run": 0, "unavailable": 0})
        if status == "UNRESOLVED_SOURCE":
            tally["measured"] += 1
        elif status == "NOT_RUN":
            tally["not_run"] += 1
        else:
            tally["unavailable"] += 1
        anchor = (
            ' id="metric-family-' + _esc(family_slug) + '" tabindex="-1"'
            if first_in_family else ""
        )
        availability = ("measured" if status == "UNRESOLVED_SOURCE" else
                        "not_run" if status == "NOT_RUN" else "unavailable")
        metrics.append(
            '<tr class="metric-row" data-metric-family="' + _esc(family_slug) +
            '" data-metric-state="' + availability + '"' + anchor +
            '><th scope="row"><span class="eyebrow">' +
            _esc(group) + '</span><br><span lang="ru">' + _esc(label) +
            '</span><br><code>' + _esc(row["metric_id"]) +
            '</code></th><td>' + _esc(_VALUE_UNITS[row["metric_id"]]) +
            '</td><td>' + _number(row["expected"]) + '</td><td>' +
            _number(row["actual"]) + '</td><td>' +
            _number(row["actual_minus_expected"]) + '</td><td>' +
            _esc(_DISPLAY_STATUS[status]) + '<br><code>' + _esc(status) +
            '</code></td></tr>'
        )

    family_links = "".join(
        '<a href="#metric-family-' + _esc(slug) + '">' +
        _esc(slug.title()) + ' (' + str(count) + ')</a>'
        for slug, count in families.items()
    )
    # Coverage counts are about measurements, never FantLab parity passes.
    if (sum(c["measured"] for c in coverage.values()) != 23
            or sum(c["not_run"] + c["unavailable"] for c in coverage.values()) != 5
            or sum(families.values()) != 28):
        raise ValueError("metric-family coverage disagrees with retained evidence")
    coverage_rows = "".join(
        '<tr class="coverage-row"><th scope="row"><a href="#metric-family-' +
        _esc(slug) + '">' + _esc(slug.title()) + '</a></th><td>' +
        str(tally["measured"]) + '</td><td>' + str(tally["not_run"]) +
        '</td><td>' + str(tally["unavailable"]) + '</td><td>' +
        str(families[slug]) + '</td></tr>'
        for slug, tally in coverage.items()
    )

    # Running on Waves is independently filterable in the browser. Both complete
    # tables and source-free exports remain available without JavaScript.
    wave_metrics = []
    for row in wave["metric_rows"]:
        if (row["comparison_kind"] != "DIAGNOSTIC_ONLY"
                or row["display_rounding_evidence"] != "UNKNOWN"):
            raise ValueError("Running on Waves metric was promoted without evidence")
        status = row["result"]
        if status not in {"UNRESOLVED_SOURCE", "NOT_RUN"} or (
            (row["actual"] is None) != (status == "NOT_RUN")
        ):
            raise ValueError("Running on Waves metric scientific status drift")
        label, family = _METRIC_PRESENTATION[row["metric_id"]]
        wave_metrics.append(
            '<tr class="wave-metric-row" data-metric-family="' + _esc(family.lower()) +
            '" data-metric-state="' +
            ("measured" if status == "UNRESOLVED_SOURCE" else "not_run") +
            '"><th scope="row"><span class="eyebrow">' +
            _esc(family) + '</span><br><span lang="ru">' + _esc(label) +
            '</span><br><code>' + _esc(row["metric_id"]) +
            '</code></th><td>' + _esc(_VALUE_UNITS[row["metric_id"]]) +
            '</td><td>' + _number(row["expected"]) + '</td><td>' +
            _number(row["actual"]) + '</td><td>' +
            _number(row["actual_minus_expected"]) + '</td><td>' +
            _esc(_DISPLAY_STATUS[status]) + '<br><code>' + _esc(status) +
            '</code></td></tr>'
        )


    # Pinned CI measurements: two displayed reference counts, not 29 invented
    # FantLab expectations. Unknown values remain UNKNOWN (not zero).
    silver_metrics = []
    for row in silver["metric_rows"]:
        metric_id, status = row["metric_id"], row["result"]
        if row["display_rounding_evidence"] != "UNKNOWN" or status not in {
            "UNRESOLVED_SOURCE", "MEASURED_NO_REFERENCE", "NOT_RUN"
        }:
            raise ValueError("Silver Dove reference or rounding upgrade refused")
        extension = metric_id == "scriptorium.general.sentences"
        if row["comparison_kind"] != ("EXTENSION_ONLY" if extension else "DIAGNOSTIC_ONLY"):
            raise ValueError("Silver Dove extension classification drift")
        if extension:
            label, family, unit = "Sentence count (Scriptorium extension)", "Extension", "sentences"
        else:
            label, family = _METRIC_PRESENTATION[metric_id]
            unit = _VALUE_UNITS[metric_id]
        if (row["actual"] is None) != (status == "NOT_RUN"):
            raise ValueError("Silver Dove missing metric was promoted")
        if status == "UNRESOLVED_SOURCE":
            if type(row["expected"]) is not int or type(row["actual_minus_expected"]) is not int:
                raise ValueError("Silver Dove integer FantLab reference missing")
        elif row["expected"] is not None or row["actual_minus_expected"] is not None:
            raise ValueError("Silver Dove unknown FantLab reference was fabricated")
        # A Scriptorium-only metric has no FantLab counterpart, rather than
        # a missing FantLab reference that might be obtained in future.
        expected = ("N/A (extension)" if extension else
                    "UNKNOWN" if row["expected"] is None else str(row["expected"]))
        delta = ("N/A (extension)" if extension else
                 "UNKNOWN" if row["actual_minus_expected"] is None else str(row["actual_minus_expected"]))
        display_status = ("Scriptorium extension; no FantLab counterpart" if extension else
                          _DISPLAY_STATUS[status])
        silver_metrics.append(
            '<tr class="silver-metric-row" data-metric-family="' + _esc(family.lower()) +
            '" data-metric-state="' + ("not_run" if status == "NOT_RUN" else "measured") +
            '"><th scope="row"><span class="eyebrow">' + _esc(family) +
            '</span><br><span lang="ru">' + _esc(label) +
            '</span><br><code>' + _esc(metric_id) +
            '</code></th><td>' + _esc(unit) + '</td><td>' + _esc(expected) +
            '</td><td>' + _number(row["actual"]) + '</td><td>' + _esc(delta) +
            '</td><td>' + _esc(display_status) +
            '<br><code>' + _esc(status) + '</code></td></tr>'
        )
    silver_section = (
        '<section aria-labelledby="silver-title"><h2 id="silver-title">'
        'Silver Dove: 29 retained Scriptorium fields</h2>'
        '<p>Andrei Bely · a verified 563,125-character pinned public source; '
        '24 observed values and five dictionary-dependent NOT_RUN. '
        '<strong>Only two FantLab displayed references are retained</strong> '
        '(characters and words); 26 further FantLab-shaped references are UNKNOWN, never zero. '
        'Sentence count is a separate Scriptorium extension without a FantLab counterpart. '
        'The +14,075 character-count '
        'difference is an unmatched-source diagnostic, not normalization evidence. '
        'Source input identity, FantLab rounding and M2 parity remain unverified.</p>'
        '<p id="silver-scroll">Scroll the table horizontally on mobile; '
        'Tab to its region for keyboard scrolling.</p>'
        '<div class="table-wrap" role="region" tabindex="0" '
        'aria-label="Silver Dove diagnostic fields" aria-describedby="silver-scroll"><table>'
        '<caption>29 source-frozen field observations; only two FantLab reference counts; M2 0/5</caption>'
        '<thead><tr><th scope="col">Metric</th><th scope="col">Candidate unit</th>'
        '<th scope="col">FantLab displayed</th><th scope="col">Scriptorium actual</th>'
        '<th scope="col">Actual − displayed</th><th scope="col">Scientific status</th>'
        '</tr></thead><tbody id="silver-metric-rows">' + ''.join(silver_metrics) +
        '</tbody></table></div></section>'
    )


    # Pinned CI measurements: two displayed reference counts, not 29 invented
    # FantLab expectations. Unknown values remain UNKNOWN (not zero).
    karamazov_metrics = []
    for row in karamazov["metric_rows"]:
        metric_id, status = row["metric_id"], row["result"]
        if row["display_rounding_evidence"] != "UNKNOWN" or status not in {
            "UNRESOLVED_SOURCE", "MEASURED_NO_REFERENCE", "NOT_RUN"
        }:
            raise ValueError("Brothers Karamazov reference or rounding upgrade refused")
        extension = metric_id == "scriptorium.general.sentences"
        if row["comparison_kind"] != ("EXTENSION_ONLY" if extension else "DIAGNOSTIC_ONLY"):
            raise ValueError("Brothers Karamazov extension classification drift")
        if extension:
            label, family, unit = "Sentence count (Scriptorium extension)", "Extension", "sentences"
        else:
            label, family = _METRIC_PRESENTATION[metric_id]
            unit = _VALUE_UNITS[metric_id]
        if (row["actual"] is None) != (status == "NOT_RUN"):
            raise ValueError("Brothers Karamazov missing metric was promoted")
        if status == "UNRESOLVED_SOURCE":
            if type(row["expected"]) is not int or type(row["actual_minus_expected"]) is not int:
                raise ValueError("Brothers Karamazov integer FantLab reference missing")
        elif row["expected"] is not None or row["actual_minus_expected"] is not None:
            raise ValueError("Brothers Karamazov unknown FantLab reference was fabricated")
        # A Scriptorium-only metric has no FantLab counterpart, rather than
        # a missing FantLab reference that might be obtained in future.
        expected = ("N/A (extension)" if extension else
                    "UNKNOWN" if row["expected"] is None else str(row["expected"]))
        delta = ("N/A (extension)" if extension else
                 "UNKNOWN" if row["actual_minus_expected"] is None else str(row["actual_minus_expected"]))
        display_status = ("Scriptorium extension; no FantLab counterpart" if extension else
                          _DISPLAY_STATUS[status])
        karamazov_metrics.append(
            '<tr class="karamazov-metric-row" data-metric-family="' + _esc(family.lower()) +
            '" data-metric-state="' + ("not_run" if status == "NOT_RUN" else "measured") +
            '"><th scope="row"><span class="eyebrow">' + _esc(family) +
            '</span><br><span lang="ru">' + _esc(label) +
            '</span><br><code>' + _esc(metric_id) +
            '</code></th><td>' + _esc(unit) + '</td><td>' + _esc(expected) +
            '</td><td>' + _number(row["actual"]) + '</td><td>' + _esc(delta) +
            '</td><td>' + _esc(display_status) +
            '<br><code>' + _esc(status) + '</code></td></tr>'
        )
    karamazov_section = (
        '<section aria-labelledby="karamazov-title"><h2 id="karamazov-title">'
        'Brothers Karamazov: 29 retained Scriptorium fields</h2>'
        '<p>Fyodor Dostoevsky · a verified 1,810,351-character pinned public source; '
        '24 observed values and five dictionary-dependent NOT_RUN. '
        '<strong>Only two FantLab displayed references are retained</strong> '
        '(characters and words); 26 further FantLab-shaped references are UNKNOWN, never zero. '
        'Sentence count is a separate Scriptorium extension without a FantLab counterpart. '
        'The +3,244 character-count '
        'difference is an unmatched-source diagnostic, not normalization evidence. '
        'Source input identity, FantLab rounding and M2 parity remain unverified.</p>'
        '<p id="karamazov-scroll">Scroll the table horizontally on mobile; '
        'Tab to its region for keyboard scrolling.</p>'
        '<div class="table-wrap" role="region" tabindex="0" '
        'aria-label="Brothers Karamazov diagnostic fields" aria-describedby="karamazov-scroll"><table>'
        '<caption>29 source-frozen field observations; only two FantLab reference counts; M2 0/5</caption>'
        '<thead><tr><th scope="col">Metric</th><th scope="col">Candidate unit</th>'
        '<th scope="col">FantLab displayed</th><th scope="col">Scriptorium actual</th>'
        '<th scope="col">Actual − displayed</th><th scope="col">Scientific status</th>'
        '</tr></thead><tbody id="karamazov-metric-rows">' + ''.join(karamazov_metrics) +
        '</tbody></table></div></section>'
    )

    shared = _shared_normalized_rows(anna["metric_rows"], wave["metric_rows"])
    # Today there are twenty shared measured per-unit observations. Any
    # changed field availability/semantics requires a reviewed new contract.
    if len(shared) != 20:
        raise ValueError("shared normalized diagnostic coverage changed")
    shared_json, shared_csv = _shared_rate_exports(shared, anna, wave)
    shared_rows = [
        '<tr class="cross-metric-row" data-metric-family="' +
        _esc(row["family"].lower()) + '"><th scope="row"><span class="eyebrow">' +
        _esc(row["family"]) + '</span><br><span lang="ru">' +
        _esc(row["label"]) + '</span><br><code>' + _esc(row["metric_id"]) +
        '</code></th><td>' + _esc(row["unit"]) + '</td><td>' +
        _esc(row["left"]) + '</td><td>' + _esc(row["right"]) +
        '</td><td>' + _esc(row["right_minus_left"]) +
        '<br><small>' + _esc(row["difference_unit"]) +
        '</small></td></tr>'
        for row in shared
    ]
    shared_section = (
        '<section aria-labelledby="shared-title"><h2 id="shared-title">'
        'Compare measured rates across two works</h2>'
        '<p>Twenty shared observed length/rate/percentage metrics, shown '
        'side by side using the same named <em>Scriptorium candidate</em> units. '
        'Anna Karenina and Running on Waves are different-length transcriptions; '
        'raw character, token and vocabulary totals are excluded. '
        'The signed difference is <strong>Running on Waves minus Anna Karenina</strong>; '
        'for percentages it is in percentage points, not relative percent. '
        'Missing measurements are omitted here, not replaced with zero. '
        'These are descriptive source-unmatched measurements: FantLab input '
        'identity, denominator compatibility and rounding remain unverified; '
        'no row proves FantLab parity, causal author style or a genre effect. '
        'Use the two full tables or JSON/CSV above for all fields and unknowns.</p>'
        '<p class="actions"><a href="shared-rates.json" download>'
        'Download the 20-rate comparison (JSON)</a> '
        '<a href="shared-rates.csv" download>Download comparison CSV</a></p>'
        + SHARED_CONTROLS +
        '<p id="shared-scroll">On narrow screens scroll this table horizontally; '
        'Tab to the table region for keyboard scrolling.</p>'
        '<div class="table-wrap" role="region" tabindex="0" '
        'aria-label="Two-work normalized diagnostic comparison" '
        'aria-describedby="shared-scroll"><table>'
        '<caption>Twenty source-unmatched observed rates and lengths; '
        'Running on Waves minus Anna Karenina, not FantLab parity</caption>'
        '<thead><tr><th scope="col">Metric</th><th scope="col">Unit</th>'
        '<th scope="col">Anna Karenina</th><th scope="col">Running on Waves</th>'
        '<th scope="col">Waves − Anna</th></tr></thead><tbody id="shared-metric-rows">' +
        ''.join(shared_rows) + '</tbody></table></div></section>'
    )

    body = (
        '<main id="main-content" tabindex="-1">'
        '<nav aria-label="Evidence navigation"><a href="../../">← All analyses</a></nav>'
        '<header class="hero"><p class="eyebrow">Methodology · diagnostic evidence</p>'
        '<h1>How close are the measurements?</h1>'
        '<p class="lede">Inspect retained differences against publicly displayed FantLab '
        'numbers, work by work and metric by metric. No manuscripts are shared.</p>'
        '<p class="notice"><strong>Not FantLab parity. M2: 0/5.</strong> '
        'Exact FantLab analyzer-input text identity is UNKNOWN for every work; '
        'decimal display rounding is UNKNOWN. Count resemblance does not prove source '
        'identity. Missing measurements are NOT_RUN, never zero.</p>'
        '<p class="actions"><a href="#silver-title">Explore Silver Dove’s 29 measured and unknown fields ↓</a> <a href="#karamazov-title">Explore Brothers Karamazov’s 29 fields ↓</a> '
        '<a class="primary-action" href="metrics.json" download>'
        'Download verified JSON</a> <a href="metrics.csv" download>'
        'Download metric CSV</a> <a href="readiness.json" download>'
        'Download source provenance JSON</a> <a href="readiness.csv" download>'
        'Download source provenance CSV</a> <a href="https://github.com/drevendev/Scriptorium/blob/master/'
        'docs/BENCHMARK_METRIC_MATRIX.md">Read the methodology ↗</a></p>'
        '</header>'
        '<section aria-labelledby="works-title"><h2 id="works-title">Five frozen public candidates</h2>'
        '<p>Four works have retained metric observations. The remaining one '
        'has NOT_RUN metric status. Each source row shows public-domain '
        'edition evidence, frozen text characters (including spaces), FantLab '
        'displayed characters, a signed count difference and relative drift '
        '(frozen − FantLab displayed) / FantLab displayed × 100, rounded to '
        'two decimal places. These are display-only diagnostics, not parity '
        'evidence. Numerical proximity does not establish source identity.</p>'
        '<p id="works-scroll">On narrow screens, scroll the table horizontally. '
        'Tab to the table to use keyboard scrolling.</p>'
        '<div class="table-wrap" role="region" aria-label="Five-work evidence status" '
        'tabindex="0" aria-describedby="works-scroll"><table>'
        '<caption>Source-frozen character counts and provenance, not parity benchmarks</caption>'
        '<thead><tr><th scope="col">Work, edition and rights</th>'
        '<th scope="col">Character-count diagnostic</th><th scope="col">Metric evidence</th>'
        '<th scope="col">Observed values</th><th scope="col">FantLab input match</th>'
        '<th scope="col">Dated reference</th></tr></thead><tbody>' +
        ''.join(works) + '</tbody></table></div></section>'
        '<section aria-labelledby="metrics-title"><h2 id="metrics-title">'
        'Anna Karenina: 28 retained diagnostic rows</h2>'
        '<p>23 numeric observations; five missing actual values. '
        'Δ is Scriptorium actual minus FantLab expected; all observed rows '
        'remain unresolved because source identity is unknown. '
        'Names come from the existing benchmark field registry; each row retains '
        'its machine ID. Units describe Scriptorium candidate measurement semantics, '
        'not proven FantLab denominator equivalence. Percentage-value differences '
        'are in percentage points; all other differences use the row unit. '
        'Friendly statuses do not change the exported data.</p>'
        '<section aria-labelledby="coverage-title"><h3 id="coverage-title">'
        'Measurement availability by family</h3>'
        '<p>Measured means a retained Scriptorium numeric observation, '
        '<strong>not</strong> FantLab parity. Not run and unavailable actuals '
        'are separate unknown states, never zero or passed checks.</p>'
        '<div class="table-wrap" role="region" tabindex="0" '
        'aria-label="Metric-family measurement coverage"><table>'
        '<caption>Anna Karenina: measured and missing values by metric family</caption>'
        '<thead><tr><th scope="col">Family</th><th scope="col">Measured</th>'
        '<th scope="col">Not run</th><th scope="col">Actual unavailable</th>'
        '<th scope="col">Total fields</th></tr></thead><tbody>' +
        coverage_rows + '</tbody></table></div></section>'
        '<nav id="metric-families" aria-label="Metric families"><p>Jump to a metric family. '
        'The full table and exports still include all 28 rows.</p>'
        '<div class="actions">' + family_links + '</div></nav>'
        + FILTER_CONTROLS +
        '<p id="metrics-scroll">On narrow screens, scroll the metric table horizontally. '
        'Tab to it for keyboard scrolling.</p>'
        '<div class="table-wrap" role="region" aria-label="Anna Karenina metric differences" '
        'tabindex="0" aria-describedby="metrics-scroll"><table>'
        '<caption>FantLab reference vs Scriptorium retained values, diagnostic only</caption>'
        '<thead><tr><th scope="col">Metric ID</th><th scope="col">Unit</th>'
        '<th scope="col">FantLab expected</th>'
        '<th scope="col">Scriptorium actual</th><th scope="col">Actual − expected</th>'
        '<th scope="col">Scientific status</th></tr></thead><tbody id="retained-metric-rows">' +
        ''.join(metrics) + '</tbody></table></div></section>'
        '<section aria-labelledby="waves-metrics-title"><h2 id="waves-metrics-title">'
        'Running on Waves: 27 retained diagnostic rows</h2>'
        '<p>23 numeric observations and four dictionary-dependent metrics not run. '
        'These are existing source-frozen measurements of a different public '
        'transcription; its FantLab input identity and display-rounding rules '
        'remain UNKNOWN. Each book has independent filters; neither one changes '
        'the other book, downloads or print output. No value is a parity pass.</p>'
        + WAVE_FILTER_CONTROLS +
        '<p id="waves-scroll">On narrow screens, scroll this table horizontally; '
        'Tab to its region for keyboard scrolling.</p>'
        '<div class="table-wrap" role="region" aria-label="Running on Waves metric differences" '
        'tabindex="0" aria-describedby="waves-scroll"><table>'
        '<caption>Frozen Running on Waves values compared with a source-unmatched '
        'FantLab reference — diagnostic only</caption>'
        '<thead><tr><th scope="col">Metric ID</th><th scope="col">Unit</th>'
        '<th scope="col">FantLab expected</th><th scope="col">Scriptorium actual</th>'
        '<th scope="col">Actual − expected</th><th scope="col">Scientific status</th>'
        '</tr></thead><tbody id="wave-metric-rows">' + ''.join(wave_metrics) + '</tbody></table></div></section>'
        + silver_section
        + karamazov_section
        + shared_section +
        '<p class="notice">No parity passes have been established. Reproduction '
        'requires five legally usable ≥300,000-character works with the actual '
        'FantLab analyzer-input identity and published rounding evidence.</p>'
        '<script src="../../assets/metric-filter.js" defer></script>'
        '<script src="../../assets/shared-metric-filter.js" defer></script></main>'
    )
    return {
        "body": body,
        "json": matrix.render_metric_matrix(report, "json"),
        "csv": matrix.render_metric_matrix(report, "csv"),
        "readiness_json": benchmark_readiness.render_report(readiness, "json"),
        "readiness_csv": benchmark_readiness.render_report(readiness, "csv"),
        "shared_json": shared_json,
        "shared_csv": shared_csv,
    }
