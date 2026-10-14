"""Readable source-free report for frozen full-work FantLab diagnostics.

This presentation layer consumes the already source-free
``scriptorium-frozen-diagnostic-v1`` artifact. It does not recompute literary metrics,
recover source text, rank incomparable deltas, or upgrade diagnostic evidence to parity.

The current full-work Anna Karenina artifact is source-unmatched by design, so every
published metric remains ``unresolved`` or ``not_run`` here.
"""

from __future__ import annotations

import argparse
import html
import json
import math
import os
import re
from collections.abc import Mapping, Sequence
from pathlib import Path, PurePosixPath
from typing import Any, Final

SCHEMA_VERSION: Final = "scriptorium-frozen-diagnostic-v1"
ALLOWED_RESULTS: Final = frozenset({"unresolved", "not_run"})
HEX64_RE: Final = re.compile(r"^[0-9a-f]{64}$")
GROUPS: Final = (
    ("fantlab.general.", "General"),
    ("fantlab.dialogue.", "Dialogue"),
    ("fantlab.vocabulary.", "Vocabulary"),
    ("fantlab.punctuation.", "Punctuation"),
)


class FrozenDiagnosticReportError(ValueError):
    """Raised when a frozen diagnostic cannot be presented without overclaim."""


def validate_artifact(artifact: Mapping[str, object]) -> Mapping[str, object]:
    value = _mapping(artifact, "artifact")
    expected_top = {
        "artifact_version",
        "benchmark_id",
        "candidate_id",
        "evidence",
        "epistemic_status",
        "metrics",
        "omitted_metric_families",
        "observations",
    }
    if set(value) != expected_top:
        raise FrozenDiagnosticReportError("top-level keys drift from frozen-diagnostic-v1")
    if value.get("artifact_version") != SCHEMA_VERSION:
        raise FrozenDiagnosticReportError("unsupported frozen diagnostic artifact")
    _text(value.get("benchmark_id"), "benchmark_id", 300)
    _text(value.get("candidate_id"), "candidate_id", 300)

    evidence = _mapping(value.get("evidence"), "evidence")
    required_evidence = {
        "hosted_run_id",
        "python_version",
        "scriptorium_revision",
        "reference_path",
        "source_manifest_path",
        "replay_integrity",
        "chapter_count",
        "raw_sha256",
        "normalized_sha256",
        "source_text_committed",
        "source_text_uploaded",
    }
    if set(evidence) != required_evidence:
        raise FrozenDiagnosticReportError("evidence keys drift from reviewed contract")
    if evidence.get("replay_integrity") != "passed":
        raise FrozenDiagnosticReportError("replay_integrity must be passed before presentation")
    _positive_int(evidence.get("hosted_run_id"), "evidence.hosted_run_id")
    _positive_int(evidence.get("chapter_count"), "evidence.chapter_count")
    _text(evidence.get("python_version"), "evidence.python_version", 100)
    _text(evidence.get("scriptorium_revision"), "evidence.scriptorium_revision", 100)
    _repo_json_path(evidence.get("reference_path"), "evidence.reference_path")
    _repo_json_path(evidence.get("source_manifest_path"), "evidence.source_manifest_path")
    _sha256(evidence.get("raw_sha256"), "evidence.raw_sha256")
    _sha256(evidence.get("normalized_sha256"), "evidence.normalized_sha256")
    if evidence.get("source_text_committed") is not False:
        raise FrozenDiagnosticReportError("source_text_committed must remain false")
    if evidence.get("source_text_uploaded") is not False:
        raise FrozenDiagnosticReportError("source_text_uploaded must remain false")

    status = _mapping(value.get("epistemic_status"), "epistemic_status")
    required_status = {
        "status",
        "fantlab_source_edition_match",
        "m2_parity_admissible",
        "m2_source_matched_progress",
        "reason",
    }
    if set(status) != required_status:
        raise FrozenDiagnosticReportError("epistemic_status keys drift from reviewed contract")
    if status.get("status") != "diagnostic_only":
        raise FrozenDiagnosticReportError("artifact must remain diagnostic_only")
    if status.get("fantlab_source_edition_match") != "unknown":
        raise FrozenDiagnosticReportError("FantLab source edition must remain unknown")
    if status.get("m2_parity_admissible") is not False:
        raise FrozenDiagnosticReportError("M2 parity must remain inadmissible")
    if status.get("m2_source_matched_progress") != "0/5":
        raise FrozenDiagnosticReportError("unexpected M2 source-matched progress")
    _text(status.get("reason"), "epistemic_status.reason", 2000)

    metrics = _mapping(value.get("metrics"), "metrics")
    if not metrics:
        raise FrozenDiagnosticReportError("diagnostic metrics must be non-empty")
    for metric_id, raw in metrics.items():
        if not isinstance(metric_id, str) or not metric_id.startswith("fantlab."):
            raise FrozenDiagnosticReportError(f"invalid metric id: {metric_id!r}")
        row = _mapping(raw, f"metrics.{metric_id}")
        if set(row) != {"expected", "actual", "raw_delta", "result"}:
            raise FrozenDiagnosticReportError(f"{metric_id} keys drift from reviewed contract")
        expected = _number(row.get("expected"), f"{metric_id}.expected")
        actual = row.get("actual")
        delta = row.get("raw_delta")
        result = row.get("result")
        if not isinstance(result, str) or result not in ALLOWED_RESULTS:
            raise FrozenDiagnosticReportError(
                f"{metric_id} result {result!r} would overclaim source-unmatched evidence"
            )
        if actual is None:
            if delta is not None:
                raise FrozenDiagnosticReportError(
                    f"{metric_id} cannot have raw_delta without actual"
                )
        else:
            actual_num = _number(actual, f"{metric_id}.actual")
            delta_num = _number(delta, f"{metric_id}.raw_delta")
            calculated = actual_num - expected
            if (
                delta_num != calculated
                if all(isinstance(n, int) for n in (expected, actual_num, delta_num))
                else not math.isclose(delta_num, calculated, rel_tol=0.0, abs_tol=1e-9)
            ):
                raise FrozenDiagnosticReportError(
                    f"{metric_id}.raw_delta is inconsistent with actual - expected"
                )
        if result == "not_run" and actual is not None:
            raise FrozenDiagnosticReportError(
                f"{metric_id} is not_run but contains an actual value"
            )

    omitted = _mapping(value.get("omitted_metric_families"), "omitted_metric_families")
    for family, reason in omitted.items():
        _text(family, "omitted metric family", 100)
        _text(reason, f"omitted_metric_families.{family}", 1000)

    observations = value.get("observations")
    if not isinstance(observations, list):
        raise FrozenDiagnosticReportError("observations must be an array")
    for index, observation in enumerate(observations):
        _text(observation, f"observations[{index}]", 2000)

    return value


def summarize(artifact: Mapping[str, object]) -> dict[str, int]:
    value = validate_artifact(artifact)
    metrics = _mapping(value["metrics"], "metrics")
    actual = 0
    missing = 0
    unresolved = 0
    not_run = 0
    for raw in metrics.values():
        row = _mapping(raw, "metric")
        if row["actual"] is None:
            missing += 1
        else:
            actual += 1
        if row["result"] == "unresolved":
            unresolved += 1
        elif row["result"] == "not_run":
            not_run += 1
    return {
        "metric_count": len(metrics),
        "actual_count": actual,
        "missing_actual_count": missing,
        "unresolved_count": unresolved,
        "not_run_count": not_run,
    }


def render_html(artifact: Mapping[str, object], *, title: str | None = None) -> str:
    value = validate_artifact(artifact)
    title_text = _text(title if title is not None else value["candidate_id"], "title", 300)
    summary = summarize(value)
    evidence = _mapping(value["evidence"], "evidence")
    status = _mapping(value["epistemic_status"], "epistemic_status")
    metrics = _mapping(value["metrics"], "metrics")
    omitted = _mapping(value["omitted_metric_families"], "omitted_metric_families")
    observations = value["observations"]

    grouped: dict[str, list[tuple[str, Mapping[str, object]]]] = {
        label: [] for _, label in GROUPS
    }
    grouped["Other"] = []
    for metric_id in sorted(metrics):
        group = "Other"
        for prefix, label in GROUPS:
            if metric_id.startswith(prefix):
                group = label
                break
        grouped[group].append((metric_id, _mapping(metrics[metric_id], metric_id)))

    sections = []
    for group, rows in grouped.items():
        if not rows:
            continue
        rendered = []
        for metric_id, row in rows:
            result = str(row["result"])
            rendered.append(
                "<tr>"
                f'<th scope="row"><code>{_esc(metric_id)}</code></th>'
                f'<td>{_esc(_unit(metric_id))}</td>'
                f'<td>{_esc(_fmt(row["expected"]))}</td>'
                f'<td>{_esc(_fmt(row["actual"]))}</td>'
                f'<td>{_esc(_signed(row["raw_delta"]))}</td>'
                f'<td><span class="pill">{_esc(result)}</span></td>'
                "</tr>"
            )
        sections.append(
            f'<section><h2>{_esc(group)}</h2>'
            f'<div class="table-wrap" tabindex="0" role="region" aria-label="{_esc(group)} metrics"><table>'
            f'<caption>{_esc(group)}: expected / actual / raw delta</caption>'
            '<thead><tr><th scope="col">Metric</th><th scope="col">Unit</th><th scope="col">FantLab expected</th>'
            '<th scope="col">Scriptorium actual</th><th scope="col">Raw Δ</th><th scope="col">Evidence result</th>'
            f'</tr></thead><tbody>{"".join(rendered)}</tbody></table></div></section>'
        )

    omitted_rows = "".join(
        f"<dt>{_esc(family)}</dt><dd>{_esc(reason)}</dd>"
        for family, reason in sorted(omitted.items())
    )
    observation_items = "".join(
        f"<li>{_esc(item)}</li>" for item in observations
    )

    css = """
:root{color-scheme:light dark;font-family:ui-serif,Georgia,Cambria,"Times New Roman",serif;line-height:1.55}
*{box-sizing:border-box}body{margin:0;background:Canvas;color:CanvasText}
main,footer{max-width:96rem;margin:auto;padding:clamp(1rem,4vw,2.5rem)}
.eyebrow{font:800 .78rem/1.2 system-ui,sans-serif;letter-spacing:.1em;text-transform:uppercase}
h1{font-size:clamp(2.5rem,8vw,5.6rem);line-height:.96;max-width:18ch;margin:.35rem 0 1rem}
h2{margin-top:2.2rem}.lede,.notice,li{font:1rem/1.6 system-ui,sans-serif;max-width:78rem}
.grid{display:grid;grid-template-columns:repeat(auto-fit,minmax(min(11rem,100%),1fr));gap:.75rem;margin:1.4rem 0 2rem}
.card,.notice{border:1px solid currentColor;border-radius:.9rem;padding:1rem}
.card strong{display:block;font-size:1.7rem}.card span{font:.84rem/1.3 system-ui,sans-serif}
.table-wrap{overflow-x:auto;margin-bottom:2rem}table{width:100%;border-collapse:collapse;font:.84rem/1.4 system-ui,sans-serif}
th,td{text-align:left;padding:.62rem;border-bottom:1px solid currentColor;vertical-align:top}
th[scope=row]{min-width:21rem}.pill{display:inline-block;border:1px solid currentColor;border-radius:999px;padding:.15rem .42rem;font-size:.72rem;font-weight:700}
code{overflow-wrap:anywhere}dd{margin-left:0;overflow-wrap:anywhere}dt{font-weight:700;margin-top:.8rem}
*:focus-visible{outline:3px solid currentColor;outline-offset:3px} a{color:inherit;display:inline-block;min-height:44px;padding:.6rem 0} caption{text-align:left;margin:.5rem 0} .skip:not(:focus){position:absolute;clip-path:inset(50%);width:1px;height:1px;overflow:hidden}footer{opacity:.72;font:.85rem/1.45 system-ui,sans-serif}
@media(max-width:44rem){main,footer{padding:1rem}th[scope=row]{min-width:15rem}th,td{padding:.48rem}}
@media(prefers-reduced-motion:reduce){*{scroll-behavior:auto!important}}
"""
    body = (
        '<a class="skip" href="#metrics">Skip to metric tables</a><main>'
        '<p class="eyebrow">Scriptorium · full-work diagnostic</p>'
        f'<h1>{_esc(title_text)}</h1>'
        '<p class="lede">A field-by-field, source-free comparison against FantLab’s '
        'published values. Numeric resemblance is visible, but source identity remains '
        'unknown, so this page does not promote any row to parity.</p>'
        '<section class="grid" aria-label="Diagnostic summary">'
        f'{_card(summary["metric_count"], "published metric rows")}'
        f'{_card(summary["actual_count"], "numeric actuals")}'
        f'{_card(summary["missing_actual_count"], "missing actuals")}'
        f'{_card(summary["unresolved_count"], "unresolved")}'
        f'{_card(summary["not_run_count"], "not run")}'
        '</section>'
        '<section class="notice"><strong>Scientific boundary.</strong> '
        f'{_esc(status["reason"])} '
        '<strong>M2 source-matched progress in this artifact: 0/5.</strong></section>'
        '<p class="notice">Historical snapshot, not a new analyzer run. Display uses up to six '
        'decimal places; small nonzero values use scientific notation. This formatting is '
        'not FantLab display rounding or a parity tolerance. Δ uses the row unit; for '
        'percentage rows it means percentage points. Missing is not zero.</p>'
        '<h2>Reproducibility identity</h2><dl>'
        f'<dt>Benchmark ID</dt><dd><code>{_esc(value["benchmark_id"])}</code></dd>'
        f'<dt>Candidate ID</dt><dd><code>{_esc(value["candidate_id"])}</code></dd>'
        f'<dt>Scriptorium revision</dt><dd><code>{_esc(evidence["scriptorium_revision"])}</code></dd>'
        f'<dt>Python</dt><dd>{_esc(evidence["python_version"])}</dd>'
        f'<dt>Hosted run</dt><dd>{_esc(evidence["hosted_run_id"])}</dd>'
        f'<dt>Frozen chapters</dt><dd>{_esc(evidence["chapter_count"])}</dd>'
        f'<dt>Raw SHA-256</dt><dd><code>{_esc(evidence["raw_sha256"])}</code></dd>'
        f'<dt>Normalized SHA-256</dt><dd><code>{_esc(evidence["normalized_sha256"])}</code></dd>'
        f'<dt>Source-edition match</dt><dd><strong>{_esc(status["fantlab_source_edition_match"])}</strong></dd>'
        '</dl>'
        + '<div id="metrics">' + "".join(sections) + "</div>"
        + '<h2>Omitted metric families (at capture)</h2><dl>'
        + omitted_rows
        + '</dl><h2>Reviewed observations (historical)</h2><ul>'
        + observation_items
        + '</ul><section class="notice"><strong>Privacy.</strong> '
          'This report contains hashes, aggregate metrics and reviewed observations only. '
          'No novel prose or replayed source text is embedded.</section></main>'
    )
    return (
        '<!doctype html><html lang="en"><head><meta charset="utf-8">'
        '<meta name="viewport" content="width=device-width,initial-scale=1">'
        f'<title>{_esc(title_text)} — Scriptorium</title><style>{css}</style>'
        f'</head><body>{body}<footer>Generated from a source-free frozen diagnostic artifact.</footer></body></html>\n'
    )


def main(argv: Sequence[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description="Render a source-free scriptorium-frozen-diagnostic-v1 artifact as HTML."
    )
    parser.add_argument("artifact", type=Path)
    parser.add_argument("--title", help="Display title; defaults to the artifact candidate ID")
    parser.add_argument("--output", type=Path)
    args = parser.parse_args(argv)
    try:
        artifact = json.loads(
            args.artifact.read_text(encoding="utf-8"), object_pairs_hook=_unique_keys
        )
        rendered = render_html(_mapping(artifact, str(args.artifact)), title=args.title)
        if args.output is None:
            print(rendered, end="")
        else:
            _write_new(args.output, rendered)
    except (OSError, UnicodeDecodeError, json.JSONDecodeError, ValueError) as exc:
        parser.error(str(exc))
    return 0


def _unique_keys(pairs: list[tuple[str, object]]) -> dict[str, object]:
    result: dict[str, object] = {}
    for key, value in pairs:
        if key in result:
            raise FrozenDiagnosticReportError(f"duplicate JSON key: {key}")
        result[key] = value
    return result


def _unit(metric_id: str) -> str:
    if metric_id.endswith(".per_1000_words"):
        return "events / 1,000 words"
    if metric_id.endswith("_percent"):
        return "% (delta: percentage points)"
    if metric_id == "fantlab.general.mean_word_length_chars":
        return "characters / word"
    if metric_id in {
        "fantlab.general.mean_sentence_length_chars",
        "fantlab.dialogue.mean_narration_sentence_length_chars",
        "fantlab.dialogue.mean_dialogue_sentence_length_chars",
    }:
        return "characters / sentence"
    if metric_id.endswith("_chars") or metric_id.endswith(".characters"):
        return "characters"
    if ".uasz_" in metric_id:
        return "mean distinct dictionary words / " + metric_id.rsplit("_", 1)[1] + "-word window"
    if metric_id.startswith("fantlab.vocabulary."):
        return "distinct words (definitions differ)"
    if metric_id.endswith(".words"):
        return "word tokens"
    return "unspecified in artifact"


def _mapping(value: object, label: str) -> Mapping[str, Any]:
    if not isinstance(value, Mapping):
        raise FrozenDiagnosticReportError(f"{label} must be an object")
    return value


def _text(value: object, label: str, limit: int) -> str:
    if not isinstance(value, str) or not value.strip():
        raise FrozenDiagnosticReportError(f"{label} must be non-empty text")
    result = value.strip()
    if len(result) > limit:
        raise FrozenDiagnosticReportError(f"{label} is too long")
    return result


def _positive_int(value: object, label: str) -> int:
    if isinstance(value, bool) or not isinstance(value, int) or value <= 0:
        raise FrozenDiagnosticReportError(f"{label} must be a positive integer")
    return value


def _number(value: object, label: str) -> int | float:
    if isinstance(value, bool) or not isinstance(value, (int, float)):
        raise FrozenDiagnosticReportError(f"{label} must be numeric")
    try:
        number = float(value)
    except OverflowError as exc:
        raise FrozenDiagnosticReportError(f"{label} is outside the supported numeric range") from exc
    if not math.isfinite(number):
        raise FrozenDiagnosticReportError(f"{label} must be finite")
    return value


def _sha256(value: object, label: str) -> str:
    if not isinstance(value, str) or HEX64_RE.fullmatch(value) is None:
        raise FrozenDiagnosticReportError(f"{label} must be a lowercase SHA-256")
    return value


def _repo_json_path(value: object, label: str) -> str:
    text = _text(value, label, 500)
    if (
        text != value or "\\" in text or ":" in text
        or PurePosixPath(text).is_absolute()
        or any(part in {"", ".", ".."} for part in text.split("/"))
        or not text.endswith(".json")
    ):
        raise FrozenDiagnosticReportError(f"{label} must be a safe repository JSON path")
    return text


def _fmt(value: object) -> str:
    if value is None:
        return "— (missing)"
    number = _number(value, "display value")
    if isinstance(number, int) or number.is_integer():
        return f"{int(number):,}"
    if number and abs(number) < 0.000001:
        return f"{number:.6g}"
    return f"{number:,.6f}".rstrip("0").rstrip(".")


def _signed(value: object) -> str:
    if value is None:
        return "— (missing)"
    number = _number(value, "display delta")
    if number == 0:
        return "0"
    return ("+" if number > 0 else "") + _fmt(number)


def _esc(value: object) -> str:
    return html.escape(str(value), quote=True)


def _card(value: object, label: str) -> str:
    return (
        '<article class="card"><strong>'
        f'{_esc(value)}</strong><span>{_esc(label)}</span></article>'
    )


def _write_new(path: Path, content: str) -> None:
    try:
        path.parent.mkdir(parents=True, exist_ok=True)
        fd = os.open(path, os.O_WRONLY | os.O_CREAT | os.O_EXCL, 0o666)
    except FileExistsError as exc:
        raise FrozenDiagnosticReportError(f"output already exists: {path}") from exc
    try:
        with os.fdopen(fd, "w", encoding="utf-8", newline="\n") as handle:
            handle.write(content)
            handle.flush()
            os.fsync(handle.fileno())
    except Exception:
        try:
            path.unlink()
        except OSError:
            pass
        raise


if __name__ == "__main__":
    raise SystemExit(main())
