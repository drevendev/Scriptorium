"""Private, source-free CSV replay of curator-declared tag profiles.

The HTML report validator is the acceptance gate. This flat four-column export
does not authenticate rights claims or enable public publication.
"""
from __future__ import annotations

import csv
from io import StringIO
from math import isfinite
import re

from .csv_safety import safe_csv_text
from .tag_profile import FEATURES
from .tag_profile_html import _validated

_PROFILE_ID = re.compile(r"[A-Za-z0-9_.:+/-]{1,120}\Z")


def _cell(value: object) -> str:
    if value is None:
        return "NOT_RUN"
    if type(value) is bool:
        return "true" if value else "false"
    if type(value) in (int, float) and isfinite(value):
        return str(value)
    if type(value) is str:
        return safe_csv_text(value)
    raise ValueError("invalid private tag CSV value")


def render_tag_profiles_csv(report: dict) -> str:
    """Export one deterministic row per field with explicit metric units.

    Sections are report, scientific_boundary, source_profile, tag/<id>,
    metric/<tag>/<metric-id> and edition/<tag>/<1-based-index>. All text is
    spreadsheet-formula neutralized; no book text, word forms or tokens appear.
    """
    tags = _validated(report)
    profiles = report["source_metric_profiles"]
    if profiles is not None and any(
        not _PROFILE_ID.fullmatch(key) or not _PROFILE_ID.fullmatch(value)
        for key, value in profiles.items()
    ):
        raise ValueError("unsafe source profile identity for CSV")

    out = StringIO(newline="")
    writer = csv.writer(out, lineterminator="\n")
    writer.writerow(("section", "field", "value", "unit"))

    def add(section: str, field: str, value: object, unit: str = "") -> None:
        writer.writerow((section, field, _cell(value), unit))

    add("report", "csv_schema", "scriptorium-private-tag-csv-v1")
    for field in ("schema_version", "taxonomy_version", "source_snapshot_sha256",
                  "aggregation"):
        add("report", field, report[field])
    for field in sorted(report["scientific_boundary"]):
        add("scientific_boundary", field, report["scientific_boundary"][field])
    if profiles is None:
        add("source_profile", "status", "NOT_RUN")
    else:
        for field in sorted(profiles):
            add("source_profile", field, profiles[field])

    for tag in sorted(tags, key=lambda item: item["tag_id"]):
        prefix = tag["tag_id"]
        for field in ("tag_id", "label", "confirmed_work_count", "sample_warning"):
            add("tag/" + prefix, field, tag[field])
        metric_rows = {row["id"]: row for row in tag["metrics"]}
        for metric_id, unit in FEATURES.items():
            metric = metric_rows[metric_id]
            section = "metric/" + prefix + "/" + metric_id
            for field in ("observed_count", "missing_count", "mean_per_work",
                          "population_stddev_between_works", "minimum", "maximum"):
                add(section, field, metric[field], unit if field not in (
                    "observed_count", "missing_count") else "editions")
        for number, work in enumerate(sorted(tag["works"], key=lambda item: item["key"]), 1):
            section = f"edition/{prefix}/{number}"
            for field in ("key", "candidate_id", "edition_id", "source_sha256",
                          "rights_basis", "rights_evidence_url", "tag_authority",
                          "tag_evidence_url"):
                add(section, field, work[field])
    return out.getvalue()
