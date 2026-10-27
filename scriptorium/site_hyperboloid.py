"""Verified, source-free Hyperboloid measurements for the generated full Reader.

This is a separately pinned diagnostic, not another FantLab-parity work in the
five-source benchmark matrix. Only the reviewed CI-derived JSON is published.
"""
from __future__ import annotations

import csv
from decimal import Decimal
from hashlib import sha1, sha256
from html import escape
import io
import json
import math
from pathlib import Path

from .site_benchmark_matrix import _METRIC_PRESENTATION, _VALUE_UNITS

ARTIFACT_PATH = (
    "corpus/candidates/diagnostics/"
    "tolstoy-hyperboloid-garin-wikisource-ru.retained.json"
)
# Git's blob object ID of the independently reviewed, source-free retained JSON.
# A mutated artefact requires a new reviewed receipt, not silent site publication.
ARTIFACT_GIT_BLOB_SHA1 = "c1278e87b08b6668073ef732f4841bf96d06cfe0"
CANDIDATE_ID = "tolstoy-hyperboloid-garin-wikisource-ru"
SLUG = "hyperboloid-garin-measured"
TITLE = "Гиперболоид инженера Гарина — 29 измерений"
CI_HEAD = "1b6f3867e407806102d4acd8758c5b2df4c89229"
CI_JSON_SHA256 = "95245fd09caea8b9150a6e7c1215c6f3c52fbaa54aa83d898a81a247192cf56d"
CI_ZIP_SHA256 = "4b5eca834a343cbe2c8bfa167942972ad652a1b64c25a97430a17dcf07ec698c"
BODY_SHA256 = "a01c5eadef53b2437eff3abe6052bb7f7bf6f95737641558343363628da7f513"
_UNBOUND = frozenset({
    "fantlab.vocabulary.active_dictionary",
    "fantlab.vocabulary.active_nondictionary",
    "fantlab.vocabulary.uasz_3000",
    "fantlab.vocabulary.uasz_10000",
    "fantlab.vocabulary.uasz_100000",
})
_REFERENCES = {
    "fantlab.general.characters": 495539,
    "fantlab.general.words": 69126,
}
EXPECTED_ENTRY = {
    "entry_id": "tolstoy-hyperboloid-retained-reader-v1",
    "kind": "measured_diagnostic",
    "slug": SLUG,
    "title": TITLE,
    "artifact_paths": [ARTIFACT_PATH],
    "artifact_schema": "scriptorium-hyperboloid-retained-ci-v1",
    "publication_status": "diagnostic",
    "benchmark_admissibility": "diagnostic_only",
    "corpus_admissibility": "not_admissible",
    "compatibility_claim": "inferred",
    "source_text_included": False,
}


class HyperboloidBuildError(ValueError):
    """The source-free published measurement evidence is not valid."""


def validate_entry(entry: object) -> None:
    if type(entry) is not dict or entry != EXPECTED_ENTRY:
        raise HyperboloidBuildError("unrecognized Hyperboloid diagnostic registration")


def _read_pinned(root: Path) -> tuple[dict, bytes]:
    path = root / ARTIFACT_PATH
    if path.absolute() != path.resolve():
        raise HyperboloidBuildError("Hyperboloid artifact path traverses a symlink")
    try:
        raw = path.read_bytes()
    except OSError as exc:
        raise HyperboloidBuildError("pinned Hyperboloid derived evidence unavailable") from exc
    if not raw or len(raw) > 100_000:
        raise HyperboloidBuildError("unexpected Hyperboloid artifact size")
    blob = b"blob " + str(len(raw)).encode("ascii") + b"\0" + raw
    if sha1(blob).hexdigest() != ARTIFACT_GIT_BLOB_SHA1:
        raise HyperboloidBuildError("Hyperboloid retained evidence blob digest changed")
    try:
        data = json.loads(raw)
    except (ValueError, UnicodeError) as exc:
        raise HyperboloidBuildError("invalid pinned Hyperboloid JSON") from exc
    return data, raw


def _validate(data: object) -> list[dict]:
    if type(data) is not dict or set(data) != {
        "schema_version", "candidate_id", "source_text_committed", "ci_run_id",
        "ci_head", "original_ci_artifact_json_sha256", "original_ci_archive_sha256",
        "source_revision_id", "source_body_characters", "source_body_sha256",
        "source_input_identity_with_fantlab", "m2_parity_admissible",
        "schema_profile", "metric_rows",
    }:
        raise HyperboloidBuildError("Hyperboloid receipt has invalid shape")
    exact = {
        "schema_version": "scriptorium-hyperboloid-retained-ci-v1",
        "candidate_id": CANDIDATE_ID,
        "source_text_committed": False,
        "ci_run_id": 40469834658,
        "ci_head": CI_HEAD,
        "original_ci_artifact_json_sha256": CI_JSON_SHA256,
        "original_ci_archive_sha256": CI_ZIP_SHA256,
        "source_revision_id": 5014458,
        "source_body_characters": 499066,
        "source_body_sha256": BODY_SHA256,
        "source_input_identity_with_fantlab": "unknown",
        "m2_parity_admissible": False,
        "schema_profile": "scriptorium-deterministic-metrics-v4",
    }
    if any(type(data.get(key)) is not type(value) or data[key] != value
           for key, value in exact.items()):
        raise HyperboloidBuildError("Hyperboloid measurement source/CI/parity gate changed")
    rows = data["metric_rows"]
    expected_ids = set(_METRIC_PRESENTATION) | {"scriptorium.general.sentences"}
    if type(rows) is not list or len(rows) != 29:
        raise HyperboloidBuildError("Hyperboloid must retain exactly 29 rows")
    ids = [row.get("id") if type(row) is dict else None for row in rows]
    if set(ids) != expected_ids or len(set(ids)) != 29:
        raise HyperboloidBuildError("Hyperboloid metric registry or uniqueness changed")
    measured = missing = 0
    for row in rows:
        if type(row) is not dict or set(row) != {"id", "actual", "reference", "status", "kind"}:
            raise HyperboloidBuildError("invalid Hyperboloid metric row")
        metric_id = row["id"]
        if type(metric_id) is not str:
            raise HyperboloidBuildError("invalid Hyperboloid metric ID")
        extension = metric_id == "scriptorium.general.sentences"
        if row["kind"] != ("extension" if extension else "candidate"):
            raise HyperboloidBuildError("metric compatibility class changed")
        if row["reference"] != _REFERENCES.get(metric_id):
            raise HyperboloidBuildError("unverified FantLab reference inserted")
        if metric_id in _UNBOUND:
            if row["status"] != "not_run" or row["actual"] is not None:
                raise HyperboloidBuildError("dictionary-unbound fields cannot be measured")
            missing += 1
        else:
            val = row["actual"]
            if (row["status"] != "measured" or type(val) not in (int, float)
                    or not math.isfinite(val) or val < 0):
                raise HyperboloidBuildError("non-numeric or fabricated metric measurement")
            if metric_id in ("fantlab.general.characters", "fantlab.general.words",
                             "scriptorium.general.sentences") and type(val) is not int:
                raise HyperboloidBuildError("integer count was altered")
            measured += 1
    if measured != 24 or missing != 5:
        raise HyperboloidBuildError("Hyperboloid evidence availability changed")
    numbers = {row["id"]: row["actual"] for row in rows}
    if numbers["fantlab.general.characters"] != 499066 or numbers["fantlab.general.words"] != 71921:
        raise HyperboloidBuildError("pinned count measurements drifted")
    return rows


def build(root: Path) -> dict[str, str]:
    """Prepare a deterministic document and portable exports without source prose."""
    data, raw = _read_pinned(root)
    rows = _validate(data)
    table = []
    output = io.StringIO(newline="")
    writer = csv.writer(output, lineterminator="\n")
    writer.writerow(("metric_id", "actual", "unit", "FantLab_display_reference",
                     "actual_minus_reference", "status", "evidence_class"))
    for row in rows:
        metric_id = row["id"]
        actual = row["actual"]
        reference = row["reference"]
        unit = ("sentences" if metric_id == "scriptorium.general.sentences"
                else _VALUE_UNITS[metric_id])
        if actual is None:
            value = "NOT_RUN"
        else:
            value = str(actual)
        delta = (format(Decimal(str(actual)) - Decimal(str(reference)), "f")
                 if reference is not None else "UNKNOWN")
        ref = str(reference) if reference is not None else "UNKNOWN"
        cls = "extension" if row["kind"] == "extension" else "inferred candidate"
        writer.writerow((metric_id, value, unit, ref, delta, row["status"],
                         "diagnostic_source_unmatched"))
        table.append(
            '<tr><th scope="row"><code>' + escape(metric_id) + '</code></th>'
            '<td>' + escape(value) + '</td><td>' + escape(unit) + '</td>'
            '<td>' + escape(ref) + '</td><td>' + escape(delta) + '</td>'
            '<td>' + escape(row["status"]) + " · " + escape(cls) + '</td></tr>'
        )
    body = (
        '<main id="main-content" tabindex="-1"><nav aria-label="Breadcrumb">'
        '<a href="../../">← All published analyses</a></nav>'
        '<p class="eyebrow">Source-pinned · diagnostic, not FantLab parity</p>'
        '<h1 lang="ru">Гиперболоид инженера Гарина</h1>'
        '<p class="lede" lang="ru">Алексей Толстой · 24 измеренных показателя, '
        '5 показателей NOT_RUN</p>'
        '<p class="notice"><strong>Evidence boundary:</strong> 499,066 characters '
        'and 71,921 words were measured from the pinned Russian Wikisource body. '
        'FantLab displays 495,539 characters and 69,126 words (diagnostic '
        'differences +3,527 and +2,795). Its analyzer-input edition is unknown. '
        '<strong>M2 parity: 0/5.</strong> Missing values are not zeros. '
        'No full text or translation is published here.</p>'
        '<p class="actions"><a href="measurements.json" download>Download 29 measurements (JSON)</a>'
        ' · <a href="measurements.csv" download>Download table (CSV)</a></p>'
        '<div class="table-wrap" tabindex="0" role="region" '
        'aria-label="Hyperboloid exact diagnostic measurements">'
        '<table><caption>29 source-free candidate and extension rows; unknown FantLab '
        'references explicitly marked UNKNOWN</caption>'
        '<thead><tr><th scope="col">Metric ID</th><th scope="col">Actual</th>'
        '<th scope="col">Candidate unit</th><th scope="col">FantLab reference</th>'
        '<th scope="col">Difference</th><th scope="col">Scientific status</th></tr>'
        '</thead><tbody>' + "".join(table) + '</tbody></table></div>'
        '<h2>Source and reproducibility</h2><dl>'
        '<dt>Pinned revision</dt><dd><a rel="noopener noreferrer" '
        'href="https://ru.wikisource.org/w/index.php?oldid=5014458">'
        'Wikisource revision 5014458</a> (public-domain candidate)</dd>'
        '<dt>Frozen body SHA-256</dt><dd><code>' + BODY_SHA256 + '</code></dd>'
        '<dt>CI measurement</dt><dd><a rel="noopener noreferrer" '
        'href="https://github.com/drevendev/Scriptorium/actions/runs/40469834658">'
        'Successful pinned diagnostic run 40469834658</a></dd>'
        '<dt>Original derived JSON SHA-256</dt><dd><code>' + CI_JSON_SHA256 + '</code></dd>'
        '<dt>FantLab reference</dt><dd><a rel="noopener noreferrer" '
        'href="https://fantlab.ru/work44824/lp">2022-09-18 work44824</a>; '
        'only two integer counts retained</dd>'
        '</dl><p class="notice">Published results are descriptive measurements '
        'on a source-unmatched transcription, not evidence of exact FantLab reproduction.</p>'
        '</main>'
    )
    return {
        "body": body,
        "json": json.dumps(data, ensure_ascii=False, indent=2, sort_keys=True,
                           allow_nan=False) + "\n",
        "csv": output.getvalue(),
        "artifact_sha256": sha256(raw).hexdigest(),
    }
