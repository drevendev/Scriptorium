"""Privacy-safe local text analysis with JSON and standalone HTML output."""

from __future__ import annotations

import argparse
import csv
from hashlib import sha256
from decimal import Decimal
from html import escape
import io
import json
import math
import os
import stat
import tempfile
from pathlib import Path
from typing import Final, Iterable

from .metrics import analyze_deterministic_metrics
from .metric_labels import METRIC_LABELS
from .csv_safety import safe_csv_text


LOCAL_ANALYSIS_SCHEMA: Final = "scriptorium-local-analysis-v1"
LOCAL_CSV_SCHEMA: Final = "scriptorium-local-analysis-csv-v1"
REPRESENTATIVE_CHARACTERS: Final = 300_000
MAX_ANALYSIS_BYTES: Final = 32 * 1024 * 1024
MAX_DICTIONARY_BYTES: Final = 8 * 1024 * 1024


class LocalInputError(ValueError):
    """An intentionally safe, path-free local file rejection."""


def build_local_analysis(
    source_bytes: bytes,
    *,
    dictionary_words: Iterable[str] | None = None,
    dictionary_profile: str | None = None,
    scriptorium_revision: str | None = None,
) -> dict[str, object]:
    """Analyze UTF-8 source bytes without embedding source text in the result."""

    text = source_bytes.decode("utf-8")
    analysis = analyze_deterministic_metrics(
        text,
        dictionary_words=dictionary_words,
        dictionary_profile=dictionary_profile,
    )
    normalized_characters = analysis["metrics"]["fantlab.general.characters"]["value"]
    if isinstance(normalized_characters, bool) or not isinstance(normalized_characters, int):
        raise ValueError("engine character count must be an integer")
    meets_threshold = normalized_characters >= REPRESENTATIVE_CHARACTERS

    return {
        "schema_version": LOCAL_ANALYSIS_SCHEMA,
        "metric_contract_id": analysis["metric_contract_id"],
        "source": {
            "raw_sha256": sha256(source_bytes).hexdigest(),
            "byte_count": len(source_bytes),
            "normalized_sha256": analysis["normalized_sha256"],
            "normalized_character_count": normalized_characters,
            "source_text_embedded": False,
        },
        "analyzer": {
            "scriptorium_revision": _none_if_blank(scriptorium_revision),
            "profiles": analysis["profiles"],
            "dependencies": analysis["dependencies"],
        },
        "representativeness": {
            "calibration_threshold_characters": REPRESENTATIVE_CHARACTERS,
            "meets_calibration_threshold": meets_threshold,
            "note": (
                "Length meets the standing calibration/profile corpus floor; legal and provenance "
                "admission remain separate gates."
                if meets_threshold
                else "Short input is valid for local analysis but is less representative for "
                "author/profile or parity-corpus use."
            ),
        },
        "metrics": analysis["metrics"],
    }


def render_html(artifact: dict[str, object], *, title: str | None = None, saved_artifact: bool = False) -> str:
    """Render one local-analysis artifact as deterministic standalone HTML."""

    if artifact.get("schema_version") != LOCAL_ANALYSIS_SCHEMA:
        raise ValueError("unsupported local analysis schema")
    source = _mapping(artifact.get("source"), "source")
    analyzer = _mapping(artifact.get("analyzer"), "analyzer")
    representativeness = _mapping(artifact.get("representativeness"), "representativeness")
    metrics = _mapping(artifact.get("metrics"), "metrics")
    if source.get("source_text_embedded") is not False:
        raise ValueError("local analysis must not embed source text")

    display_title = _nonempty_text(title) if title is not None else "Scriptorium local analysis"
    groups = (
        ("General", _rows(metrics, ("fantlab.general.", "scriptorium.general."))),
        ("Dialogue", _rows(metrics, ("fantlab.dialogue.",))),
        ("Vocabulary", _rows(metrics, ("fantlab.vocabulary.",))),
        ("Punctuation", _rows(metrics, ("fantlab.punctuation.",))),
    )
    # Key figures are taken from the *same* current metric artifact as the tables.
    # This is a reader-first summary, not another calculation or a quality score.
    highlight_fields = (
        ("Words", "fantlab.general.words"),
        ("Sentences · Scriptorium", "scriptorium.general.sentences"),
        ("Dialogue share", "fantlab.dialogue.share_percent"),
        ("Distinct surface words", "fantlab.vocabulary.unique_words"),
    )
    overview = '<section aria-labelledby="highlights-heading"><h2 id="highlights-heading">At a glance</h2><dl class="highlights">'
    for label, metric_id in highlight_fields:
        metric = _mapping(metrics.get(metric_id), metric_id)
        value = _format_value(metric.get("value"))
        unit = _human_unit(str(metric.get("unit", "")))
        overview += (
            '<div class="highlight">'
            f'<dt>{escape(label)}</dt>'
            f'<dd>{escape(value)} <span class="highlight-unit">{escape(unit) if value != "Unavailable" else ""}</span></dd>'
            '</div>'
        )
    overview += '</dl></section>'
    included = {metric_id for _, rows in groups for metric_id, _ in rows}
    other = [(metric_id, _mapping(metrics[metric_id], metric_id))
             for metric_id in sorted(metrics) if metric_id not in included]
    groups = (*groups, ("Other", other))
    sections = "".join(_render_metric_group(name, rows) for name, rows in groups if rows)
    profiles = _mapping(analyzer.get("profiles"), "analyzer.profiles")
    profiles_html = "".join(
        f"<dt>{escape(str(key))}</dt><dd><code>{escape(str(value))}</code></dd>"
        for key, value in sorted(profiles.items())
    )
    threshold_state = (
        "Meets the 300,000-character calibration floor"
        if representativeness.get("meets_calibration_threshold") is True
        else "Short input — valid analysis, limited representativeness"
    )
    dependency = _mapping(analyzer.get("dependencies"), "analyzer.dependencies")
    dictionary_dependency = dependency.get("vocabulary_dictionary")
    if dictionary_dependency is None:
        dictionary_html = "<p><strong>Vocabulary dictionary:</strong> not supplied; dictionary-dependent rows are not run.</p>"
    else:
        dep = _mapping(dictionary_dependency, "vocabulary_dictionary")
        dictionary_html = (
            "<p><strong>Vocabulary dictionary:</strong> "
            f"{escape(str(dep.get('profile')))} · {escape(str(dep.get('lexeme_count')))} normalized lexemes · "
            f"<code>{escape(str(dep.get('normalized_lexemes_sha256')))}</code></p>"
        )

    revision = analyzer.get("scriptorium_revision")
    revision_html = "not recorded" if revision is None else f"<code>{escape(str(revision))}</code>"
    note = escape(str(representativeness.get("note", "")))
    saved_note = (
        '<p class="badge"><strong>Imported saved JSON:</strong> hashes, metric values and '
        'algorithm versions are declarations in this file, not authenticated or replay-verified. '
        'To check against your manuscript, rerun the analyzer on the '
        'original text and compare the results. This is not FantLab parity.</p>'
        if saved_artifact else ""
    )
    return f'''<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{escape(display_title)}</title>
<style>
:root {{ color-scheme: light dark; font-family: Georgia, 'Times New Roman', serif; line-height: 1.5; }}
* {{ box-sizing: border-box; }}
body {{ margin: 0; background: Canvas; color: CanvasText; }}
main, footer {{ max-width: 76rem; margin: auto; padding: 1.25rem; }}
h1, h2 {{ line-height: 1.15; }}
.eyebrow {{ font: 700 .8rem/1.2 system-ui, sans-serif; letter-spacing: .08em; text-transform: uppercase; }}
.lead {{ max-width: 62ch; font-size: 1.12rem; }}
.badge {{ display: inline-block; border: 1px solid currentColor; border-radius: 999px; padding: .25rem .6rem; font: 600 .85rem/1.3 system-ui, sans-serif; }}
.meta {{ border-block: 1px solid color-mix(in srgb, CanvasText 20%, Canvas); padding-block: 1rem; }}
.highlights {{ display: grid; grid-template-columns: repeat(auto-fit, minmax(min(100%, 14rem), 1fr)); gap: .85rem; margin: 1rem 0 2rem; }}
.highlight {{ padding: 1rem 1.2rem; border: 1px solid color-mix(in srgb, CanvasText 25%, Canvas); border-radius: .65rem; min-width: 0; }}
.highlight dt {{ font: 600 .88rem/1.4 system-ui, sans-serif; }}
.highlight dd {{ margin: .45rem 0 0; font: 700 clamp(1.25rem, 3vw, 2rem)/1.2 system-ui, sans-serif; overflow-wrap: anywhere; }}
.highlight-unit {{ font: 400 .75rem/1.35 system-ui, sans-serif; }}
.table-wrap {{ overflow-x: auto; margin-block: 1rem 2rem; }}
.metric-label {{ display: block; font-weight: 700; }}
.metric-id {{ display: block; font-size: .78em; font-weight: 400; color: color-mix(in srgb, CanvasText 72%, Canvas); margin-block-start: .2rem; }}
table {{ border-collapse: collapse; width: 100%; min-width: 48rem; font-family: system-ui, sans-serif; }}
th, td {{ padding: .65rem .75rem; border-bottom: 1px solid color-mix(in srgb, CanvasText 18%, Canvas); text-align: left; vertical-align: top; }}
th {{ font-weight: 700; }}
code {{ overflow-wrap: anywhere; }}
.skip-link:not(:focus) {{ position: absolute; clip-path: inset(50%); width: 1px; height: 1px; overflow: hidden; }}
.skip-link:focus {{ position: absolute; z-index: 10; margin: .5rem; padding: .75rem; background: Canvas; }}
*:focus-visible {{ outline: 3px solid currentColor; outline-offset: 3px; }}
@media (prefers-reduced-motion: reduce) {{ * {{ scroll-behavior: auto !important; }} }}
</style>
</head>
<body>
<a class="skip-link" href="#main-content">Skip to analysis</a>
<main id="main-content" tabindex="-1">
<p class="eyebrow">Scriptorium · local-only deterministic analysis</p>
<h1>{escape(display_title)}</h1>
<p class="lead">Explore literary statistics in everyday language, with the exact machine metric IDs beneath each label. FantLab-namespaced rows are inferred compatibility candidates, not parity claims. Source text is not embedded in this report.</p>
<p class="badge">{escape(threshold_state)}</p>
{saved_note}
{overview}
<div class="meta">
<p><strong>Raw SHA-256:</strong> <code>{escape(str(source.get('raw_sha256')))}</code></p>
<p><strong>Normalized SHA-256:</strong> <code>{escape(str(source.get('normalized_sha256')))}</code></p>
<p><strong>Bytes / normalized characters:</strong> {escape(str(source.get('byte_count')))} / {escape(str(source.get('normalized_character_count')))}</p>
<p><strong>Scriptorium revision:</strong> {revision_html}</p>
{dictionary_html}
<p><strong>Representativeness:</strong> {note}</p>
<details><summary>Analysis profiles</summary><dl>{profiles_html}</dl></details>
<p><strong>Unavailable is not zero.</strong> A null metric may need a dictionary, a nonzero
word/sentence denominator, or a complete vocabulary window. No null is a parity pass.</p>
<p><strong>Numeric display:</strong> Floating-point values retain their JSON round-trip decimal representation. Digits describe deterministic output, not measurement accuracy or FantLab parity.</p>
</div>
{sections}
</main>
<footer>Local analysis only. Corpus admission, legal provenance and FantLab source identity are separate gates.</footer>
</body>
</html>
'''


def render_csv(artifact: dict[str, object]) -> str:
    """Render stable, spreadsheet-safe derived rows without manuscript text.

    Metadata is repeated per metric so any filtered CSV subset remains attributable
    to its exact source digest and algorithm profiles. Numeric values retain Python's
    round-trip representation, consistent with JSON and HTML numeric values.
    """

    if artifact.get("schema_version") != LOCAL_ANALYSIS_SCHEMA:
        raise ValueError("unsupported local analysis schema")
    source = _mapping(artifact.get("source"), "source")
    if source.get("source_text_embedded") is not False:
        raise ValueError("local analysis must not embed source text")
    analyzer = _mapping(artifact.get("analyzer"), "analyzer")
    profiles = _mapping(analyzer.get("profiles"), "analyzer.profiles")
    dependencies = _mapping(analyzer.get("dependencies"), "analyzer.dependencies")
    metrics = _mapping(artifact.get("metrics"), "metrics")
    if set(metrics) != set(METRIC_LABELS):
        raise ValueError("local-analysis-csv-v1 requires all 29 current metrics")
    dictionary = dependencies.get("vocabulary_dictionary")
    if dictionary is not None:
        dictionary = _mapping(dictionary, "analyzer.dependencies.vocabulary_dictionary")

    columns = (
        "metric_id", "value", "unit", "status", "definition_evidence", "raw_count",
        "csv_schema_version", "metric_contract_id", "raw_sha256", "normalized_sha256",
        "scriptorium_revision", "normalization_profile", "metrics_profile", "dialogue_profile",
        "vocabulary_profile", "punctuation_profile", "dictionary_profile",
        "dictionary_sha256",
    )
    output = io.StringIO(newline="")
    writer = csv.DictWriter(output, fieldnames=columns, lineterminator="\n")
    writer.writeheader()
    identity = {
        "csv_schema_version": LOCAL_CSV_SCHEMA,
        "scriptorium_revision": _csv_text(analyzer.get("scriptorium_revision")),
        "metric_contract_id": _csv_required_text(artifact.get("metric_contract_id"), "metric_contract_id"),
        "raw_sha256": _csv_required_text(source.get("raw_sha256"), "source.raw_sha256"),
        "normalized_sha256": _csv_required_text(source.get("normalized_sha256"), "source.normalized_sha256"),
        "normalization_profile": _csv_required_text(profiles.get("normalization"), "normalization profile"),
        "metrics_profile": _csv_required_text(profiles.get("metrics"), "metrics profile"),
        "dialogue_profile": _csv_required_text(profiles.get("dialogue"), "dialogue profile"),
        "vocabulary_profile": _csv_required_text(profiles.get("vocabulary"), "vocabulary profile"),
        "punctuation_profile": _csv_required_text(profiles.get("punctuation"), "punctuation profile"),
        "dictionary_profile": _csv_text(dictionary.get("profile") if dictionary else None),
        "dictionary_sha256": _csv_text(dictionary.get("normalized_lexemes_sha256") if dictionary else None),
    }
    for metric_id in sorted(metrics):
        metric = _mapping(metrics[metric_id], metric_id)
        status = metric.get("compatibility_status")
        if status not in ("inferred", "extension"):
            raise ValueError(f"metric {metric_id} has unsupported compatibility status")
        writer.writerow({
            **identity,
            "metric_id": _csv_text(metric_id),
            "value": _csv_number(metric.get("value")),
            "unit": _csv_required_text(metric.get("unit"), "metric unit"),
            "status": status,
            "definition_evidence": _csv_required_text(metric.get("definition_evidence"), "definition evidence"),
            "raw_count": _csv_number(metric.get("raw_count")),
        })
    return output.getvalue()


def _csv_number(value: object) -> str:
    if value is None:
        return ""  # Unknown is a blank cell, never zero.
    if isinstance(value, bool) or not isinstance(value, (int, float, Decimal)):
        raise ValueError("metric numeric value must be int, finite float or null")
    if isinstance(value, (float, Decimal)) and not math.isfinite(value):
        raise ValueError("metric numeric value must be finite")
    return str(value)


def _csv_required_text(value: object, label: str) -> str:
    if not isinstance(value, str) or not value.strip():
        raise ValueError(f"{label} must be a non-empty string")
    return _csv_text(value)


def _csv_text(value: object) -> str:
    if value is None:
        return ""
    if not isinstance(value, str):
        raise ValueError("metric identity field must be text or null")
    return safe_csv_text(value)

def _render_metric_group(name: str, rows: list[tuple[str, dict[str, object]]]) -> str:
    body = []
    for metric_id, row in rows:
        status = row.get("compatibility_status")
        if status not in ("inferred", "extension"):
            raise ValueError("local results must remain inferred or extension")
        value = row.get("value")
        raw_count = row.get("raw_count")
        raw_count_html = "—" if raw_count is None else escape(str(raw_count))
        # Human labels are presentation-only; the canonical metric ID remains
        # visibly inspectable and the machine-readable artifact is unchanged.
        human_label = METRIC_LABELS.get(metric_id, metric_id)
        body.append(
            "<tr>"
            f'<th scope="row" data-label="{escape(human_label, quote=True)}" '
            f'aria-label="{escape(human_label + ", metric ID " + metric_id, quote=True)}">'
            f'<span class="metric-label">{escape(human_label)}</span>'
            f'<code class="metric-id">{escape(metric_id)}</code></th>'
            f"<td>{escape(_format_value(value))}</td>"
            f"<td>{escape(_human_unit(str(row.get('unit', ''))))}</td>"
            f"<td>{escape(str(row.get('compatibility_status', 'unknown')))}</td>"
            f"<td>{raw_count_html}</td>"
            "</tr>"
        )
    label = escape(name)
    return (
        f"<section><h2>{label}</h2><div class=\"table-wrap\" tabindex=\"0\" role=\"region\" aria-label=\"{label} metrics\">"
        f"<table><caption>{label}: local metrics and evidence</caption><thead><tr><th scope=\"col\">Metric</th><th scope=\"col\">Value</th>"
        "<th scope=\"col\">Unit</th><th scope=\"col\">Status</th><th scope=\"col\">Raw count</th>"
        "</tr></thead><tbody>" + "".join(body) + "</tbody></table></div></section>"
    )


def _rows(metrics: dict[str, object], prefixes: tuple[str, ...]) -> list[tuple[str, dict[str, object]]]:
    result: list[tuple[str, dict[str, object]]] = []
    for metric_id in sorted(metrics):
        if not metric_id.startswith(prefixes):
            continue
        row = _mapping(metrics[metric_id], metric_id)
        result.append((metric_id, row))
    return result


def _format_value(value: object) -> str:
    if value is None:
        return "Unavailable"
    if isinstance(value, bool):
        raise ValueError("metric value must not be boolean")
    if isinstance(value, int):
        return f"{value:,}"
    if isinstance(value, Decimal):
        if not value.is_finite():
            raise ValueError("metric value must be finite")
        return str(value)
    if isinstance(value, float):
        if not math.isfinite(value):
            raise ValueError("metric value must be finite")
        # Preserve the float's JSON round-trip decimal in human-readable output.
        # Six significant digits can hide meaningful diagnostic differences.
        return repr(value)
    raise ValueError("metric value must be numeric or null")


def _human_unit(unit: str) -> str:
    return {
        "characters/word": "characters / word",
        "characters/sentence": "characters / sentence",
        "occurrences/1000_words": "occurrences / 1,000 words",
        "unique_dictionary_words/window": "unique dictionary words / window",
    }.get(unit, unit)


def _mapping(value: object, label: str) -> dict[str, object]:
    if not isinstance(value, dict):
        raise ValueError(f"{label} must be an object")
    return value


def _nonempty_text(value: str) -> str:
    stripped = value.strip()
    if not stripped:
        raise ValueError("title must be non-empty")
    return stripped


def _none_if_blank(value: str | None) -> str | None:
    if value is None:
        return None
    stripped = value.strip()
    return stripped or None


def _read_bounded_regular_file(path: Path, limit: int, label: str) -> bytes:
    """Bound local reads even if a file grows after its initial stat.

    On POSIX, O_NOFOLLOW also prevents a symlink-swap race at open time.
    O_NONBLOCK prevents a FIFO from hanging the CLI before fstat rejects it.
    """
    if path.is_symlink():
        raise LocalInputError(f"{label} must be a regular, non-symlink file")
    flags = os.O_RDONLY | getattr(os, "O_NOFOLLOW", 0) | getattr(os, "O_NONBLOCK", 0)
    try:
        fd = os.open(path, flags)
    except OSError as exc:
        raise LocalInputError(f"{label} cannot be opened as a regular file") from exc
    try:
        info = os.fstat(fd)
        if not stat.S_ISREG(info.st_mode):
            raise LocalInputError(f"{label} must be a regular file")
        if info.st_size > limit:
            raise LocalInputError(f"{label} exceeds the {limit}-byte input limit")
        with os.fdopen(fd, "rb") as handle:
            fd = -1
            content = handle.read(limit + 1)
    except OSError as exc:
        raise LocalInputError(f"{label} could not be read") from exc
    finally:
        if fd != -1:
            os.close(fd)
    if len(content) > limit:
        raise LocalInputError(f"{label} exceeds the {limit}-byte input limit")
    return content


def _write_new(path: Path, content: str) -> None:
    # Publish complete derived output with no replacement, including symlink targets.
    # Keep the temporary file on the same filesystem for atomic hard-link creation.
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary = None
    try:
        with tempfile.NamedTemporaryFile(
            mode="w", encoding="utf-8", newline="\n",
            prefix=".scriptorium-", suffix=".tmp", dir=path.parent, delete=False,
        ) as handle:
            temporary = Path(handle.name)
            handle.write(content)
            handle.flush()
            os.fsync(handle.fileno())
        os.link(temporary, path)
    finally:
        if temporary is not None:
            temporary.unlink(missing_ok=True)


def _build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Analyze a local UTF-8 text without publishing source text.")
    parser.add_argument("text", type=Path)
    parser.add_argument("--format", choices=("json", "html", "csv"), default="json")
    parser.add_argument("--title")
    parser.add_argument("--scriptorium-revision")
    parser.add_argument("--dictionary", type=Path)
    parser.add_argument("--dictionary-profile")
    parser.add_argument("--output", type=Path)
    return parser


def main(argv: list[str] | None = None) -> int:
    parser = _build_parser()
    args = parser.parse_args(argv)
    if (args.dictionary is None) != (args.dictionary_profile is None):
        parser.error("--dictionary and --dictionary-profile must be supplied together")

    try:
        source_bytes = _read_bounded_regular_file(args.text, MAX_ANALYSIS_BYTES, "manuscript")
        dictionary_words = None
        if args.dictionary is not None:
            dictionary_bytes = _read_bounded_regular_file(args.dictionary, MAX_DICTIONARY_BYTES, "dictionary")
            try:
                dictionary_words = dictionary_bytes.decode("utf-8").splitlines()
            except UnicodeDecodeError as exc:
                raise LocalInputError("dictionary must be UTF-8") from exc
        artifact = build_local_analysis(
            source_bytes,
            dictionary_words=dictionary_words,
            dictionary_profile=args.dictionary_profile,
            scriptorium_revision=args.scriptorium_revision,
        )
        if args.format == "json":
            rendered = json.dumps(artifact, ensure_ascii=False, indent=2, sort_keys=True, allow_nan=False) + "\n"
        elif args.format == "html":
            rendered = render_html(artifact, title=args.title)
        else:
            rendered = render_csv(artifact)
        if args.output is None:
            print(rendered, end="")
        else:
            _write_new(args.output, rendered)
    except FileExistsError:
        parser.error("report output already exists; choose another destination")
    except LocalInputError as exc:
        parser.error(str(exc))  # This exception contains only controlled, path-free text.
    except UnicodeDecodeError:
        parser.error("manuscript must be UTF-8")
    except (OSError, ValueError, TypeError):
        parser.error("unable to analyze local inputs or create the report")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
