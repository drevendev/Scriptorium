"""Privacy-safe local text analysis with JSON and standalone HTML output."""

from __future__ import annotations

import argparse
from hashlib import sha256
from html import escape
import json
import math
import os
import tempfile
from pathlib import Path
from typing import Final, Iterable

from .metrics import analyze_deterministic_metrics


LOCAL_ANALYSIS_SCHEMA: Final = "scriptorium-local-analysis-v1"
REPRESENTATIVE_CHARACTERS: Final = 300_000


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


def render_html(artifact: dict[str, object], *, title: str | None = None) -> str:
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
    return f'''<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{escape(display_title)}</title>
<style>
:root {{ color-scheme: light dark; font-family: Georgia, 'Times New Roman', serif; line-height: 1.5; }}
body {{ margin: 0; background: Canvas; color: CanvasText; }}
main, footer {{ max-width: 76rem; margin: auto; padding: 1.25rem; }}
h1, h2 {{ line-height: 1.15; }}
.eyebrow {{ font: 700 .8rem/1.2 system-ui, sans-serif; letter-spacing: .08em; text-transform: uppercase; }}
.lead {{ max-width: 62ch; font-size: 1.12rem; }}
.badge {{ display: inline-block; border: 1px solid currentColor; border-radius: 999px; padding: .25rem .6rem; font: 600 .85rem/1.3 system-ui, sans-serif; }}
.meta {{ border-block: 1px solid color-mix(in srgb, CanvasText 20%, Canvas); padding-block: 1rem; }}
.table-wrap {{ overflow-x: auto; margin-block: 1rem 2rem; }}
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
<p class="lead">Readable derived metrics from a local UTF-8 text. FantLab-namespaced rows are inferred compatibility candidates, not parity claims. Source text is not embedded in this report.</p>
<p class="badge">{escape(threshold_state)}</p>
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
</div>
{sections}
</main>
<footer>Local analysis only. Corpus admission, legal provenance and FantLab source identity are separate gates.</footer>
</body>
</html>
'''


def _render_metric_group(name: str, rows: list[tuple[str, dict[str, object]]]) -> str:
    body = []
    for metric_id, row in rows:
        status = row.get("compatibility_status")
        if status not in ("inferred", "extension"):
            raise ValueError("local results must remain inferred or extension")
        value = row.get("value")
        raw_count = row.get("raw_count")
        raw_count_html = "—" if raw_count is None else escape(str(raw_count))
        body.append(
            "<tr>"
            f"<th scope=\"row\"><code>{escape(metric_id)}</code></th>"
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
    if isinstance(value, float):
        if not math.isfinite(value):
            raise ValueError("metric value must be finite")
        return format(value, ".6g")
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
    parser.add_argument("--format", choices=("json", "html"), default="json")
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
        source_bytes = args.text.read_bytes()
        dictionary_words = None
        if args.dictionary is not None:
            dictionary_words = args.dictionary.read_text(encoding="utf-8").splitlines()
        artifact = build_local_analysis(
            source_bytes,
            dictionary_words=dictionary_words,
            dictionary_profile=args.dictionary_profile,
            scriptorium_revision=args.scriptorium_revision,
        )
        if args.format == "json":
            rendered = json.dumps(artifact, ensure_ascii=False, indent=2, sort_keys=True, allow_nan=False) + "\n"
        else:
            rendered = render_html(artifact, title=args.title)
        if args.output is None:
            print(rendered, end="")
        else:
            _write_new(args.output, rendered)
    except (OSError, UnicodeDecodeError, ValueError, TypeError) as exc:
        parser.error(str(exc))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
