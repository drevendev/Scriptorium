"""Deterministic, source-only CSV export of the *incomplete* 1775 Trusov sample.

Only verified derived metrics are exported; no historical Page prose is read.
A frozen Git blob identity prevents silent changes in the scientific sample.
This is NOT a book, a translator comparison, or a FantLab parity benchmark.
"""
from __future__ import annotations

import csv
from hashlib import sha1
from io import StringIO
import json
from math import isfinite
from pathlib import Path
import re
from typing import Mapping

SOURCE_RELATIVE = (
    "corpus/candidates/diagnostics/"
    "defoe-robinson-crusoe-trusov-1775-ru.interior-measured.json"
)
SOURCE_BLOB_SHA1 = "04f0ec0974a705f00c9ac5c4e02a2003d4d38b58"
SOURCE_GRAPH_SHA256 = "d2104ad33fc15ddb8479c13b9fdbe0abf94f8418e76c02261a803b79130ebaa4"
NORMALIZED_SHA256 = "e8e6b6f9d583e5b70c9b05b54aa4f441acc34aaa03a4da6e9011d512680c3eeb"
COVERAGE = "INCOMPLETE_INTERIOR_EXCERPT_NOT_CORPUS_OR_PARITY"
FIELDS = (
    "metric_id", "actual", "unit", "compatibility_status", "result",
    "coverage", "page_from", "page_to",
    "source_page_graph_sha256", "normalized_sha256",
)
GATES = {
    "pinned_150_page_source_replay": True,
    "full_literary_body": "NOT_RUN",
    "historical_proofreadpage_rendering": "NOT_VERIFIED",
    "page_join_historical_identity": "UNKNOWN",
    "aligned_translation_coverage": "NOT_RUN",
    "print_edition_collation": "NOT_RUN",
    "fantlab_analyzer_input_identity": "UNKNOWN",
    "corpus_admitted_for_calibration": False,
    "author_profile_admissible": False,
    "m2_parity_admissible": False,
    "source_text_committed": False,
}
_IDS = re.compile(r"(?:fantlab|scriptorium)\.[a-z0-9_.]+\Z")
_UNIT = re.compile(r"[a-zA-Z0-9_/.-]{1,70}\Z")
_RESULTS = {
    "MEASURED_INTERIOR_EXCERPT_ONLY",
    "NOT_RUN_DICTIONARY_UNBOUND",
    "UNAVAILABLE_NO_OBSERVATIONS",
}


def load_frozen_report(path: Path) -> dict:
    """Read only the exact source-free published receipt, never mutable page text."""
    if path.is_symlink() or not path.is_file():
        raise ValueError("Trusov export input must be a regular file")
    raw = path.read_bytes()
    if not 1000 <= len(raw) <= 16000:
        raise ValueError("unexpected Trusov receipt size")
    blob = sha1(b"blob " + str(len(raw)).encode("ascii") + b"\0" + raw).hexdigest()
    if blob != SOURCE_BLOB_SHA1:
        raise ValueError("Trusov excerpt receipt Git blob SHA-1 mismatch")
    report = json.loads(raw)
    if not isinstance(report, dict):
        raise ValueError("invalid Trusov receipt")
    return report


def render_csv(report: Mapping[str, object]) -> str:
    """Build a spreadsheet-safe, traceable 29-row CSV with unavailable values blank."""
    if (
        not isinstance(report, dict)
        or report.get("schema_version") != "scriptorium-trusov-interior-measurement-v1"
        or report.get("version") != "inferred_projected_Page_3_to_147_excerpt_v1"
        or report.get("candidate_id") != "defoe-robinson-trusov-1775-vol1-ru"
        or report.get("status") != COVERAGE
        or report.get("source_page_graph_sha256") != SOURCE_GRAPH_SHA256
        or report.get("normalized_sha256") != NORMALIZED_SHA256
        or report.get("normalized_characters_including_spaces") != 303882
        or report.get("page_interval") != {
            "from": 3, "to": 147, "count": 145, "excluded_pages": [2, 148, 149, 150, 151],
            "opening_truncated": True, "ending_truncated": True,
        }
        or report.get("gates") != GATES
        or report.get("numeric_metric_count") != 22
        or report.get("unavailable_metric_count") != 7
    ):
        raise ValueError("scientific scope or frozen Trusov identity changed")
    metric_rows = report.get("metric_rows")
    if not isinstance(metric_rows, list) or len(metric_rows) != 29:
        raise ValueError("incomplete Trusov metric export")
    seen: set[str] = set()
    values: list[list[str]] = []
    for row in metric_rows:
        if not isinstance(row, dict) or set(row) != {
            "metric_id", "actual", "unit", "compatibility_status", "result", "fantlab_display"
        }:
            raise ValueError("unexpected metric row")
        metric_id, actual = row["metric_id"], row["actual"]
        unit, result = row["unit"], row["result"]
        if (
            not isinstance(metric_id, str) or not _IDS.fullmatch(metric_id)
            or metric_id in seen
            or not isinstance(unit, str) or not _UNIT.fullmatch(unit)
            or row["compatibility_status"] not in ("inferred", "extension")
            or result not in _RESULTS
            or row["fantlab_display"] is not None
        ):
            raise ValueError("unknown metric, duplicate or unsafe CSV content")
        seen.add(metric_id)
        if actual is None:
            if result == "MEASURED_INTERIOR_EXCERPT_ONLY":
                raise ValueError("unknown excerpt value marked measured")
            cell = ""
        else:
            if (type(actual) not in (float, int)
                    or not isfinite(actual)
                    or result != "MEASURED_INTERIOR_EXCERPT_ONLY"):
                raise ValueError("non-numeric or unverified excerpt value")
            cell = str(int(actual)) if type(actual) is float and actual.is_integer() else str(actual)
        values.append([
            metric_id, cell, unit, row["compatibility_status"], result,
            COVERAGE, "3", "147", SOURCE_GRAPH_SHA256, NORMALIZED_SHA256,
        ])
    if (
        sorted(seen) != [row["metric_id"] for row in metric_rows]
        or sum(row[1] != "" for row in values) != 22
        or sum(row[1] == "" for row in values) != 7
    ):
        raise ValueError("unordered or incomplete 29-field export")
    handle = StringIO(newline="")
    writer = csv.writer(handle, lineterminator="\n")
    writer.writerow(FIELDS)
    writer.writerows(values)
    return handle.getvalue()
