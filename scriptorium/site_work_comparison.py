"""Canonical, source-free comparison route for two exact frozen full works.

A registered page reuses the installed pinned offline gallery; it never reads
manuscripts, discovers artifacts, or promotes diagnostic metrics to parity.
"""
from __future__ import annotations

from decimal import Decimal
from html import escape
import json
from pathlib import Path
from typing import Any

from . import full_work_gallery as gallery

SLUG = "two-full-work-differences"
TITLE = "Running on Waves × The Children of Captain Grant — measured differences"
SOURCE_PATHS = tuple(
    "corpus/candidates/diagnostics/" + candidate + ".json"
    for candidate, *_ in gallery.SOURCES
)
EXPECTED_ENTRY: dict[str, Any] = {
    "entry_id": "grin-verne-frozen-work-comparison-v1",
    "kind": "work_comparison",
    "slug": SLUG,
    "title": TITLE,
    "artifact_paths": list(SOURCE_PATHS),
    "artifact_schema": "scriptorium-full-work-gallery-v1",
    "publication_status": "diagnostic",
    "benchmark_admissibility": "diagnostic_only",
    "corpus_admissibility": "not_admissible",
    "compatibility_claim": "inferred",
    "source_text_included": False,
}


class ComparisonBuildError(ValueError):
    """Refuse unregistered, drifted or unsafe comparative evidence."""


def validate_entry(entry: object) -> None:
    """Only the exact reviewed pair and scientific boundaries may be published."""
    if not isinstance(entry, dict) or entry != EXPECTED_ENTRY:
        raise ComparisonBuildError("unrecognized frozen-work comparison registration")


def _decimal_delta(a: int | float, b: int | float) -> str:
    return format(Decimal(str(b)) - Decimal(str(a)), "f")


def _render_signed_differences(measurements: list[dict[str, Any]]) -> str:
    """Expose only rate/mean deltas from the pinned source-free comparison."""
    rows = []
    for item in measurements:
        if not item["normalized_for_visual_comparison"]:
            continue
        delta = item["right_minus_left_decimal"]
        signed_delta = ("+" if Decimal(delta) > 0 else "") + delta
        rows.append(
            f"<tr data-metric-id='{escape(item['metric_id'], quote=True)}'>"
            f"<th scope='row'>{escape(item['label'])} "
            f"<small>{escape(item['unit'])}</small></th>"
            f"<td>{escape(str(item['left']))}</td>"
            f"<td>{escape(str(item['right']))}</td>"
            f"<td>{escape(signed_delta)} {escape(item['difference_unit'])}</td></tr>"
        )
    if len(rows) != 7:
        raise ComparisonBuildError("unexpected comparable metric count")
    return (
        "<section aria-labelledby='signed-differences'>"
        "<h2 id='signed-differences'>Observed differences</h2>"
        "<p>Verne minus Grin (right minus left), calculated from the exact pinned "
        "measurements. A plus or minus sign gives direction, not literary quality. "
        "Percentages are subtracted in percentage points. The two books differ in "
        "length; these descriptive differences cannot isolate author or translator effects.</p>"
        "<div class='scroll' tabindex='0' role='region' "
        "aria-label='Signed differences across seven rate and mean metrics'>"
        "<table><caption>Seven measured rate/mean comparisons and signed deltas</caption>"
        "<thead><tr><th scope='col'>Metric</th><th scope='col'>Grin</th>"
        "<th scope='col'>Verne · Beketova</th><th scope='col'>Verne − Grin</th>"
        "</tr></thead><tbody>" + "".join(rows) + "</tbody></table></div></section>"
    )


def build(root: Path) -> dict[str, Any]:
    """Generate deterministic HTML/CSV/JSON in memory before site publication."""
    try:
        records = gallery.load_gallery(root)
    except (gallery.GalleryError, OSError, UnicodeError, ValueError,
            TypeError, KeyError, AttributeError) as exc:
        raise ComparisonBuildError("frozen comparison evidence is missing or incompatible") from exc
    if len(records) != 2 or tuple(record["id"] for record in records) != tuple(
        candidate for candidate, *_ in gallery.SOURCES
    ):
        raise ComparisonBuildError("frozen comparison source identity drift")

    measurements = []
    for metric_id, label, unit, normalized in gallery.METRICS:
        left, right = (record["values"][metric_id] for record in records)
        measurements.append({
            "metric_id": metric_id,
            "label": label,
            "unit": unit,
            "left": left,
            "right": right,
            "right_minus_left_decimal": _decimal_delta(left, right),
            "difference_unit": "percentage points" if unit == "%" else unit,
            "normalized_for_visual_comparison": normalized,
            "compatibility_status": "diagnostic_or_inferred_not_parity",
        })

    result = {
        "schema_version": "scriptorium-work-comparison-export-v1",
        "profile": gallery.PROFILE,
        "comparison_direction": "right_minus_left",
        "scientific_boundary": {
            "fantlab_analyzer_input_identity": "unknown",
            "m2_parity_admissible": False,
            "m2_weight": 0,
            "note": "Source-unmatched descriptive comparison; not FantLab parity or an author profile.",
        },
        "works": [
            {
                "candidate_id": record["id"],
                "title": record["title"],
                "author_or_translator": record["author"],
                "characters_including_spaces": record["body"],
                "body_sha256": record["body_hash"],
                "derived_json_sha256": record["json_hash"],
                "evidence": record["evidence"],
            }
            for record in records
        ],
        "measurement_profiles": dict(zip(
            ("metrics", "normalization", "dialogue", "vocabulary", "punctuation"),
            records[0]["profiles"],
        )),
        "measurements": measurements,
    }
    try:
        json_text = json.dumps(result, ensure_ascii=False, indent=2,
                               sort_keys=True, allow_nan=False) + "\n"
        csv_text = gallery.render_csv(records)
        html_text = gallery.render_html(records)
        delta_section = _render_signed_differences(measurements)
    except (gallery.GalleryError, ValueError, TypeError, KeyError, ArithmeticError) as exc:
        raise ComparisonBuildError("frozen comparison export failed validation") from exc
    marker = "<main id='main' class='wrap'>"
    values_marker = "<section aria-labelledby='values'>"
    if (html_text.count(marker) != 1 or html_text.count("</header>") != 1 or
            html_text.count(values_marker) != 1):
        raise ComparisonBuildError("gallery HTML integration markers drifted")
    html_text = html_text.replace(
        marker,
        marker + "<nav aria-label='Reader navigation'>"
        "<a href='../../'>← All published analyses</a></nav>",
        1,
    ).replace(
        "</header>",
        "<p class='actions'><a href='measurements.json' download>"
        "Download verified values (JSON)</a> · "
        "<a href='measurements.csv' download>Download metric table (CSV)"
        "</a></p></header>",
        1,
    ).replace(values_marker, delta_section + values_marker, 1)
    return {
        "html": html_text,
        "json": json_text,
        "csv": csv_text,
        "input_artifacts": [
            {"path": source_path, "sha256": record["json_hash"]}
            for source_path, record in zip(SOURCE_PATHS, records)
        ],
    }
