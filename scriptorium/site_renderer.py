"""Deterministic, fail-closed static renderer for Scriptorium publication artifacts.

The renderer consumes only ``site/publication-manifest.json`` and the canonical JSON
artifacts that manifest explicitly names. It never fetches source text or discovers
publishable files by directory scan. Generated output is disposable build state.
"""

from __future__ import annotations

import argparse
import hashlib
import html
import json
import re
import shutil
from collections.abc import Mapping, Sequence
from pathlib import Path, PurePosixPath
from typing import Any
from urllib.parse import urlsplit

from .publication import validate_compatibility_claim

GENERATOR_PROFILE = "scriptorium-static-site-v1"
MANIFEST_PROFILE = "scriptorium-publication-manifest-v1"
_SLUG_RE = re.compile(r"^[a-z0-9][a-z0-9-]*$")
_ALLOWED_ARTIFACT_ROOTS = frozenset({"showcase", "benchmarks", "public-artifacts"})
_ALLOWED_PUBLICATION_STATUSES = frozenset({"illustrative_excerpt", "diagnostic", "published"})
_ALLOWED_BENCHMARK_ADMISSIBILITY = frozenset({"not_admissible", "diagnostic_only", "admissible"})
_ALLOWED_CORPUS_ADMISSIBILITY = frozenset({"not_admissible", "admissible"})


class PublicationBuildError(ValueError):
    """Raised when public output cannot be generated without weakening the contract."""


def _read_json(path: Path) -> tuple[dict[str, Any], bytes]:
    try:
        raw = path.read_bytes()
    except OSError as exc:
        raise PublicationBuildError(f"cannot read publication JSON: {path}") from exc
    try:
        value = json.loads(raw.decode("utf-8"))
    except (UnicodeDecodeError, json.JSONDecodeError) as exc:
        raise PublicationBuildError(f"invalid UTF-8 JSON: {path}") from exc
    if not isinstance(value, dict):
        raise PublicationBuildError(f"expected JSON object: {path}")
    return value, raw


def _required_text(container: Mapping[str, Any], key: str, context: str) -> str:
    value = container.get(key)
    if not isinstance(value, str) or not value.strip():
        raise PublicationBuildError(f"{context}.{key} must be a non-empty string")
    return value


def _require_enum(
    container: Mapping[str, Any], key: str, allowed: frozenset[str], context: str
) -> str:
    value = container.get(key)
    if value not in allowed:
        raise PublicationBuildError(f"{context}.{key} has unsupported value {value!r}")
    return value


def _safe_artifact_path(repo_root: Path, raw_path: Any) -> Path:
    if not isinstance(raw_path, str) or not raw_path or "\\" in raw_path:
        raise PublicationBuildError("artifact_path must be a non-empty POSIX repository path")
    posix_path = PurePosixPath(raw_path)
    parts = posix_path.parts
    if (
        posix_path.is_absolute()
        or len(parts) < 2
        or parts[0] not in _ALLOWED_ARTIFACT_ROOTS
        or any(part in {"", ".", ".."} for part in parts)
        or not raw_path.endswith(".json")
        or "//" in raw_path
    ):
        raise PublicationBuildError(f"unsafe artifact_path {raw_path!r}")

    root = repo_root.resolve()
    lexical_candidate = root / Path(*parts)
    candidate = lexical_candidate.resolve()
    if lexical_candidate.absolute() != candidate:
        raise PublicationBuildError(f"artifact_path must not traverse symlinks: {raw_path!r}")
    if candidate == root or root not in candidate.parents:
        raise PublicationBuildError(f"artifact_path escapes repository: {raw_path!r}")
    if not candidate.is_file():
        raise PublicationBuildError(f"artifact_path does not exist: {raw_path!r}")
    return candidate


def _safe_external_url(value: Any, context: str) -> str:
    if not isinstance(value, str) or not value:
        raise PublicationBuildError(f"{context} must be a non-empty URL")
    parsed = urlsplit(value)
    if parsed.scheme not in {"http", "https"} or not parsed.netloc:
        raise PublicationBuildError(f"{context} must use HTTP(S)")
    if parsed.username is not None or parsed.password is not None:
        raise PublicationBuildError(f"{context} must not contain URL credentials")
    return value


def _validate_manifest_header(manifest: Mapping[str, Any]) -> Sequence[Mapping[str, Any]]:
    if manifest.get("schema_version") != MANIFEST_PROFILE:
        raise PublicationBuildError("unsupported publication manifest profile")
    generated_from = manifest.get("generated_from")
    if generated_from != {"repository": "drevendev/Scriptorium", "branch": "master"}:
        raise PublicationBuildError("publication manifest repository identity is not canonical")
    deployment = manifest.get("deployment")
    if deployment != {"publication_source": "github_actions", "generated_output_committed": False}:
        raise PublicationBuildError("publication manifest deployment boundary is not canonical")
    entries = manifest.get("entries")
    if not isinstance(entries, list) or not entries:
        raise PublicationBuildError("publication manifest entries must be a non-empty array")
    if not all(isinstance(entry, Mapping) for entry in entries):
        raise PublicationBuildError("publication manifest entries must be objects")
    return entries


def _validate_showcase(entry: Mapping[str, Any], artifact: Mapping[str, Any]) -> dict[str, Any]:
    if entry.get("kind") != "work_showcase":
        raise PublicationBuildError(
            f"renderer {GENERATOR_PROFILE} does not yet support kind {entry.get('kind')!r}"
        )
    entry_id = _required_text(entry, "entry_id", "manifest entry")
    slug = _required_text(entry, "slug", f"manifest entry {entry_id}")
    if not _SLUG_RE.fullmatch(entry_id) or not _SLUG_RE.fullmatch(slug):
        raise PublicationBuildError(f"manifest entry {entry_id!r} has unsafe identity or slug")
    if entry.get("source_text_included") is not False:
        raise PublicationBuildError(f"manifest entry {entry_id!r} includes source text")

    publication_status = _require_enum(
        entry, "publication_status", _ALLOWED_PUBLICATION_STATUSES, f"manifest entry {entry_id}"
    )
    benchmark_admissibility = _require_enum(
        entry,
        "benchmark_admissibility",
        _ALLOWED_BENCHMARK_ADMISSIBILITY,
        f"manifest entry {entry_id}",
    )
    corpus_admissibility = _require_enum(
        entry,
        "corpus_admissibility",
        _ALLOWED_CORPUS_ADMISSIBILITY,
        f"manifest entry {entry_id}",
    )

    analysis = artifact.get("analysis")
    source = artifact.get("source")
    work = artifact.get("work")
    if not isinstance(analysis, Mapping) or not isinstance(source, Mapping) or not isinstance(work, Mapping):
        raise PublicationBuildError(f"showcase {entry_id!r} lacks work/source/analysis objects")

    expected_pairs = (
        ("entry_id", entry_id, artifact.get("showcase_id")),
        ("artifact_schema", entry.get("artifact_schema"), analysis.get("schema_version")),
        ("publication_status", publication_status, artifact.get("status")),
        ("benchmark_admissibility", benchmark_admissibility, artifact.get("benchmark_admissibility")),
        ("corpus_admissibility", corpus_admissibility, artifact.get("corpus_admissibility")),
    )
    for label, manifest_value, canonical_value in expected_pairs:
        if manifest_value != canonical_value:
            raise PublicationBuildError(
                f"manifest {label} contradicts showcase {entry_id!r}: "
                f"manifest={manifest_value!r}, canonical={canonical_value!r}"
            )
    if source.get("source_text_committed") is not False:
        raise PublicationBuildError(f"showcase {entry_id!r} commits source text")
    try:
        compatibility_claim = validate_compatibility_claim(entry, artifact)
    except ValueError as exc:
        raise PublicationBuildError(str(exc)) from exc

    metrics = analysis.get("metrics")
    if not isinstance(metrics, Mapping) or not metrics:
        raise PublicationBuildError(f"showcase {entry_id!r} has no publishable metrics")

    revision_url = _safe_external_url(source.get("revision_url"), f"showcase {entry_id}.source.revision_url")
    return {
        "entry_id": entry_id,
        "slug": slug,
        "title": _required_text(entry, "title", f"manifest entry {entry_id}"),
        "publication_status": publication_status,
        "benchmark_admissibility": benchmark_admissibility,
        "corpus_admissibility": corpus_admissibility,
        "compatibility_claim": compatibility_claim,
        "author": _required_text(work, "author", f"showcase {entry_id}.work"),
        "work_title": _required_text(work, "title", f"showcase {entry_id}.work"),
        "language": _required_text(work, "language", f"showcase {entry_id}.work"),
        "representativeness_note": _required_text(artifact, "representativeness_note", f"showcase {entry_id}"),
        "provider": _required_text(source, "provider", f"showcase {entry_id}.source"),
        "page": _required_text(source, "page", f"showcase {entry_id}.source"),
        "revision_url": revision_url,
        "edition_note": _required_text(source, "edition_note", f"showcase {entry_id}.source"),
        "legal_basis": _required_text(source, "legal_basis", f"showcase {entry_id}.source"),
        "metrics": metrics,
    }


def _format_metric_value(value: Any) -> str:
    if value is None:
        return "—"
    if isinstance(value, bool) or not isinstance(value, (int, float)):
        raise PublicationBuildError(f"metric value must be numeric or null, got {value!r}")
    try:
        return json.dumps(value, ensure_ascii=False, allow_nan=False, separators=(",", ":"))
    except ValueError as exc:
        raise PublicationBuildError(f"metric value is not finite JSON: {value!r}") from exc


def _escape(value: Any) -> str:
    return html.escape(str(value), quote=True)


def _page(title: str, stylesheet_href: str, body: str) -> str:
    return (
        "<!doctype html>\n"
        '<html lang="en">\n<head>\n<meta charset="utf-8">\n'
        '<meta name="viewport" content="width=device-width, initial-scale=1">\n'
        f"<title>{_escape(title)}</title>\n"
        f'<link rel="stylesheet" href="{_escape(stylesheet_href)}">\n'
        "</head>\n<body>\n"
        f"{body}\n"
        f'<footer>Generated by {_escape(GENERATOR_PROFILE)} from allow-listed derived artifacts. No source prose is published.</footer>\n'
        "</body>\n</html>\n"
    )


def _render_index(entries: Sequence[Mapping[str, Any]]) -> str:
    cards = []
    for item in entries:
        cards.append(
            '<article class="card">'
            f'<p class="eyebrow">{_escape(item["publication_status"])}</p>'
            f'<h2><a href="works/{_escape(item["slug"])}/">{_escape(item["title"])}</a></h2>'
            f'<p>{_escape(item["author"])} · {_escape(item["work_title"])}</p>'
            f'<p><strong>Compatibility:</strong> {_escape(item["compatibility_claim"])}</p>'
            f'<p><strong>Benchmark:</strong> {_escape(item["benchmark_admissibility"])} · '
            f'<strong>Corpus:</strong> {_escape(item["corpus_admissibility"])}</p>'
            "</article>"
        )
    body = (
        '<main><p class="eyebrow">Scriptorium</p><h1>Evidence-labelled literary analysis</h1>'
        '<p class="lede">Public pages are generated only from repository artifacts explicitly allow-listed by the publication manifest. '
        'Compatibility labels describe evidence, not visual similarity to FantLab.</p>'
        f'<section class="grid">{"".join(cards)}</section></main>'
    )
    return _page("Scriptorium", "assets/site.css", body)


def _render_work(item: Mapping[str, Any]) -> str:
    rows = []
    for metric_id in sorted(item["metrics"]):
        row = item["metrics"][metric_id]
        if not isinstance(row, Mapping):
            raise PublicationBuildError(f"metric {metric_id!r} is not an object")
        status = row.get("compatibility_status")
        if status not in {"inferred", "reproduced", "extension"}:
            raise PublicationBuildError(f"metric {metric_id!r} has unsupported compatibility status")
        unit = row.get("unit")
        if not isinstance(unit, str) or not unit:
            raise PublicationBuildError(f"metric {metric_id!r} has invalid unit")
        rows.append(
            "<tr>"
            f"<th scope=\"row\"><code>{_escape(metric_id)}</code></th>"
            f"<td>{_escape(_format_metric_value(row.get('value')))}</td>"
            f"<td>{_escape(unit)}</td>"
            f'<td><span class="status {_escape(status)}">{_escape(status)}</span></td>'
            "</tr>"
        )
    revision_url = _escape(item["revision_url"])
    body = (
        '<main><nav><a href="../../">← All published analyses</a></nav>'
        f'<p class="eyebrow">{_escape(item["publication_status"])}</p>'
        f'<h1>{_escape(item["title"])}</h1>'
        f'<p class="lede">{_escape(item["author"])} · {_escape(item["work_title"])}</p>'
        '<section class="notice"><strong>Evidence boundary.</strong> '
        f'Compatibility: {_escape(item["compatibility_claim"])}. '
        f'Benchmark: {_escape(item["benchmark_admissibility"])}. '
        f'Corpus: {_escape(item["corpus_admissibility"])}. '
        f'{_escape(item["representativeness_note"])}</section>'
        '<h2>Derived metrics</h2>'
        '<div class="table-wrap"><table><thead><tr><th>Metric</th><th>Value</th><th>Unit</th><th>Evidence</th></tr></thead>'
        f'<tbody>{"".join(rows)}</tbody></table></div>'
        '<h2>Provenance</h2><dl>'
        f'<dt>Provider</dt><dd>{_escape(item["provider"])}</dd>'
        f'<dt>Source page</dt><dd>{_escape(item["page"])}</dd>'
        f'<dt>Edition</dt><dd>{_escape(item["edition_note"])}</dd>'
        f'<dt>Legal basis</dt><dd>{_escape(item["legal_basis"])}</dd>'
        f'<dt>Immutable source reference</dt><dd><a rel="noreferrer" href="{revision_url}">{revision_url}</a></dd>'
        '</dl><p class="notice">Source text is deliberately not included in this site build.</p></main>'
    )
    return _page(item["title"], "../../assets/site.css", body)


_SITE_CSS = """\
:root { color-scheme: light dark; font-family: system-ui, sans-serif; line-height: 1.5; }
body { margin: 0; }
main, footer { max-width: 72rem; margin: auto; padding: 2rem; }
a { color: inherit; }
h1 { font-size: clamp(2rem, 5vw, 4rem); line-height: 1.05; }
.eyebrow { font-size: .8rem; font-weight: 700; letter-spacing: .08em; text-transform: uppercase; }
.lede { font-size: 1.15rem; max-width: 52rem; }
.grid { display: grid; grid-template-columns: repeat(auto-fit, minmax(18rem, 1fr)); gap: 1rem; }
.card, .notice { border: 1px solid currentColor; border-radius: .75rem; padding: 1rem; }
.table-wrap { overflow-x: auto; }
table { border-collapse: collapse; width: 100%; }
th, td { border-bottom: 1px solid currentColor; padding: .65rem; text-align: left; vertical-align: top; }
dt { font-weight: 700; margin-top: 1rem; }
dd { margin-left: 0; }
.status { font-weight: 700; }
footer { opacity: .7; font-size: .9rem; }
"""


def _prepare_output(repo_root: Path, output_dir: Path) -> Path:
    root = repo_root.resolve()
    if output_dir.is_symlink():
        raise PublicationBuildError("output directory must not be a symlink")
    output = output_dir.resolve()
    try:
        relative = output.relative_to(root)
    except ValueError as exc:
        raise PublicationBuildError("output directory must stay inside the repository build/ tree") from exc
    if not relative.parts or relative.parts[0] != "build":
        raise PublicationBuildError("output directory must stay inside the repository build/ tree")
    if output.exists():
        shutil.rmtree(output)
    output.mkdir(parents=True)
    return output


def build_site(
    repo_root: Path | str,
    output_dir: Path | str,
) -> dict[str, Any]:
    """Build deterministic static output from the canonical publication allow-list."""

    root = Path(repo_root).resolve()
    manifest_path = root / "site" / "publication-manifest.json"
    manifest_file = manifest_path.resolve()
    if manifest_path.absolute() != manifest_file:
        raise PublicationBuildError("canonical publication manifest must not traverse symlinks")
    manifest, manifest_raw = _read_json(manifest_file)
    entries = _validate_manifest_header(manifest)

    seen_ids: set[str] = set()
    seen_slugs: set[str] = set()
    render_items: list[dict[str, Any]] = []
    input_rows: list[dict[str, str]] = []
    for entry in entries:
        entry_id = _required_text(entry, "entry_id", "manifest entry")
        slug = _required_text(entry, "slug", f"manifest entry {entry_id}")
        if entry_id in seen_ids or slug in seen_slugs:
            raise PublicationBuildError("publication entry_id and slug values must be unique")
        seen_ids.add(entry_id)
        seen_slugs.add(slug)

        artifact_path = _safe_artifact_path(root, entry.get("artifact_path"))
        artifact, artifact_raw = _read_json(artifact_path)
        item = _validate_showcase(entry, artifact)
        render_items.append(item)
        input_rows.append(
            {
                "entry_id": item["entry_id"],
                "artifact_path": artifact_path.relative_to(root).as_posix(),
                "artifact_sha256": hashlib.sha256(artifact_raw).hexdigest(),
                "route": f"works/{item['slug']}/",
            }
        )

    render_items.sort(key=lambda item: (item["slug"], item["entry_id"]))
    input_rows.sort(key=lambda item: item["entry_id"])

    # Render and validate every page before touching the output tree. A failed build must
    # not leave a partially refreshed site that looks publishable.
    index_html = _render_index(render_items)
    work_pages = {item["slug"]: _render_work(item) for item in render_items}

    build_record = {
        "generator_profile": GENERATOR_PROFILE,
        "manifest_profile": MANIFEST_PROFILE,
        "manifest_sha256": hashlib.sha256(manifest_raw).hexdigest(),
        "entries": input_rows,
    }
    output_path = Path(output_dir)
    if not output_path.is_absolute():
        output_path = root / output_path
    output = _prepare_output(root, output_path)
    (output / "assets").mkdir()
    (output / "assets" / "site.css").write_text(_SITE_CSS, encoding="utf-8", newline="\n")
    (output / "index.html").write_text(index_html, encoding="utf-8", newline="\n")
    for slug, page_html in work_pages.items():
        work_dir = output / "works" / slug
        work_dir.mkdir(parents=True)
        (work_dir / "index.html").write_text(page_html, encoding="utf-8", newline="\n")
    (output / "build.json").write_text(
        json.dumps(build_record, ensure_ascii=False, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
        newline="\n",
    )
    return build_record


def main(argv: Sequence[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--repo-root", default=".", help="repository root (default: current directory)")
    parser.add_argument("--output", default="build/site")
    args = parser.parse_args(argv)
    build_site(args.repo_root, args.output)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
