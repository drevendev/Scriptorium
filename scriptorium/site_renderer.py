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
from collections.abc import Mapping, Sequence
from pathlib import Path, PurePosixPath
from typing import Any
from urllib.parse import urlsplit

from .site_publish import staged_site
from .publication import validate_compatibility_claim
from .site_gallery_filter import evidence_kind, FILTER_CONTROLS, FILTER_JS, FILTER_CSS
from . import site_frozen_diagnostic
from . import site_work_comparison

GENERATOR_PROFILE = "scriptorium-static-site-v2"
MANIFEST_PROFILE = "scriptorium-publication-manifest-v1"
PROVENANCE_SHOWCASE_PROFILE = "scriptorium-work-provenance-showcase-v1"
_SLUG_RE = re.compile(r"^[a-z0-9][a-z0-9-]*$")
_HEX64_RE = re.compile(r"^[0-9a-f]{64}$")
_ALLOWED_ARTIFACT_ROOTS = frozenset({"showcase", "benchmarks", "public-artifacts"})
_ALLOWED_PUBLICATION_STATUSES = frozenset({"illustrative_excerpt", "diagnostic", "published"})
_ALLOWED_BENCHMARK_ADMISSIBILITY = frozenset({"not_admissible", "diagnostic_only", "admissible"})
_ALLOWED_CORPUS_ADMISSIBILITY = frozenset({"not_admissible", "admissible"})
_MANIFEST_KEYS = frozenset({"schema_version", "generated_from", "deployment", "entries"})
_WORK_SHOWCASE_ENTRY_KEYS = frozenset(
    {
        "entry_id",
        "kind",
        "slug",
        "title",
        "artifact_path",
        "artifact_schema",
        "publication_status",
        "benchmark_admissibility",
        "corpus_admissibility",
        "compatibility_claim",
        "source_text_included",
    }
)
_SUPPORTED_SHOWCASE_ARTIFACT_SCHEMAS = frozenset(
    {
        "scriptorium-deterministic-metrics-v1",
        "scriptorium-deterministic-metrics-v2",
        PROVENANCE_SHOWCASE_PROFILE,
        site_frozen_diagnostic.FROZEN_PROFILE,
    }
)
_PROVENANCE_TOP_LEVEL_KEYS = frozenset(
    {
        "schema_version",
        "showcase_id",
        "status",
        "benchmark_admissibility",
        "corpus_admissibility",
        "compatibility_claim",
        "source_text_committed",
        "representativeness_note",
        "work",
        "source",
        "frozen_identity",
        "fantlab_boundary",
    }
)
_PROVENANCE_SOURCE_KEYS = frozenset(
    {
        "provider",
        "page",
        "revision_url",
        "edition_note",
        "legal_basis",
        "revision_manifest",
        "chapter_revision_count",
        "composition_profile",
        "extraction_profile",
    }
)
_PROVENANCE_IDENTITY_KEYS = frozenset(
    {
        "character_count_including_spaces",
        "utf8_byte_count",
        "raw_sha256",
        "normalization_profile",
        "normalized_character_count_including_spaces",
        "normalized_sha256",
    }
)
_PROVENANCE_FANTLAB_KEYS = frozenset(
    {
        "work_id",
        "analysis_url",
        "analysis_date",
        "displayed_character_count",
        "displayed_word_count",
        "fantlab_source_edition_match",
        "m2_parity_admissible",
        "note",
    }
)


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


def _require_exact_keys(
    container: Mapping[str, Any], allowed: frozenset[str], context: str
) -> None:
    actual = set(container)
    if actual == allowed:
        return
    details: list[str] = []
    missing = sorted(allowed - actual)
    unexpected = sorted(actual - allowed)
    if missing:
        details.append(f"missing={missing!r}")
    if unexpected:
        details.append(f"unexpected={unexpected!r}")
    raise PublicationBuildError(f"{context} has invalid keys: {', '.join(details)}")


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
    _require_exact_keys(manifest, _MANIFEST_KEYS, "publication manifest")
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


def _validate_common_entry(entry: Mapping[str, Any]) -> tuple[str, str, str, str, str, str]:
    if entry.get("kind") != "work_showcase":
        raise PublicationBuildError(
            f"renderer {GENERATOR_PROFILE} does not yet support kind {entry.get('kind')!r}"
        )
    entry_id = _required_text(entry, "entry_id", "manifest entry")
    _require_exact_keys(entry, _WORK_SHOWCASE_ENTRY_KEYS, f"manifest entry {entry_id}")
    slug = _required_text(entry, "slug", f"manifest entry {entry_id}")
    if not _SLUG_RE.fullmatch(entry_id) or not _SLUG_RE.fullmatch(slug):
        raise PublicationBuildError(f"manifest entry {entry_id!r} has unsafe identity or slug")
    if entry.get("source_text_included") is not False:
        raise PublicationBuildError(f"manifest entry {entry_id!r} includes source text")

    artifact_schema = _require_enum(
        entry,
        "artifact_schema",
        _SUPPORTED_SHOWCASE_ARTIFACT_SCHEMAS,
        f"manifest entry {entry_id}",
    )
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
    return (
        entry_id,
        slug,
        artifact_schema,
        publication_status,
        benchmark_admissibility,
        corpus_admissibility,
    )


def _validate_metric_showcase(
    entry: Mapping[str, Any], artifact: Mapping[str, Any], common: tuple[str, str, str, str, str, str]
) -> dict[str, Any]:
    entry_id, slug, artifact_schema, publication_status, benchmark_admissibility, corpus_admissibility = common
    analysis = artifact.get("analysis")
    source = artifact.get("source")
    work = artifact.get("work")
    if not isinstance(analysis, Mapping) or not isinstance(source, Mapping) or not isinstance(work, Mapping):
        raise PublicationBuildError(f"showcase {entry_id!r} lacks work/source/analysis objects")

    expected_pairs = (
        ("entry_id", entry_id, artifact.get("showcase_id")),
        ("artifact_schema", artifact_schema, analysis.get("schema_version")),
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
        "render_mode": "metrics",
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


def _positive_int(container: Mapping[str, Any], key: str, context: str) -> int:
    value = container.get(key)
    if isinstance(value, bool) or not isinstance(value, int) or value <= 0:
        raise PublicationBuildError(f"{context}.{key} must be a positive integer")
    return value


def _sha256_text(container: Mapping[str, Any], key: str, context: str) -> str:
    value = container.get(key)
    if not isinstance(value, str) or not _HEX64_RE.fullmatch(value):
        raise PublicationBuildError(f"{context}.{key} must be a lowercase SHA-256")
    return value


def _safe_revision_manifest(value: Any, context: str) -> str:
    if not isinstance(value, str) or not value.endswith(".json") or "\\" in value:
        raise PublicationBuildError(f"{context} must be a repository JSON path")
    path = PurePosixPath(value)
    if path.is_absolute() or any(part in {"", ".", ".."} for part in path.parts):
        raise PublicationBuildError(f"{context} must be a safe repository JSON path")
    if path.parts[:3] != ("corpus", "candidates", "source-edition-traces"):
        raise PublicationBuildError(f"{context} must point into the canonical source-edition trace tree")
    return value


def _validate_provenance_showcase(
    entry: Mapping[str, Any], artifact: Mapping[str, Any], common: tuple[str, str, str, str, str, str]
) -> dict[str, Any]:
    entry_id, slug, artifact_schema, publication_status, benchmark_admissibility, corpus_admissibility = common
    _require_exact_keys(artifact, _PROVENANCE_TOP_LEVEL_KEYS, f"provenance showcase {entry_id}")
    if artifact.get("schema_version") != PROVENANCE_SHOWCASE_PROFILE or artifact_schema != PROVENANCE_SHOWCASE_PROFILE:
        raise PublicationBuildError(f"provenance showcase {entry_id!r} has unsupported schema identity")

    expected_pairs = (
        ("entry_id", entry_id, artifact.get("showcase_id")),
        ("publication_status", publication_status, artifact.get("status")),
        ("benchmark_admissibility", benchmark_admissibility, artifact.get("benchmark_admissibility")),
        ("corpus_admissibility", corpus_admissibility, artifact.get("corpus_admissibility")),
        ("compatibility_claim", entry.get("compatibility_claim"), artifact.get("compatibility_claim")),
    )
    for label, manifest_value, canonical_value in expected_pairs:
        if manifest_value != canonical_value:
            raise PublicationBuildError(
                f"manifest {label} contradicts showcase {entry_id!r}: "
                f"manifest={manifest_value!r}, canonical={canonical_value!r}"
            )
    if artifact.get("compatibility_claim") != "extension":
        raise PublicationBuildError(
            f"provenance showcase {entry_id!r} must use extension compatibility to avoid a FantLab parity claim"
        )
    if artifact.get("source_text_committed") is not False:
        raise PublicationBuildError(f"showcase {entry_id!r} commits source text")

    work = artifact.get("work")
    source = artifact.get("source")
    frozen = artifact.get("frozen_identity")
    fantlab = artifact.get("fantlab_boundary")
    if not all(isinstance(value, Mapping) for value in (work, source, frozen, fantlab)):
        raise PublicationBuildError(f"provenance showcase {entry_id!r} lacks required objects")
    assert isinstance(work, Mapping) and isinstance(source, Mapping)
    assert isinstance(frozen, Mapping) and isinstance(fantlab, Mapping)
    _require_exact_keys(source, _PROVENANCE_SOURCE_KEYS, f"provenance showcase {entry_id}.source")
    _require_exact_keys(frozen, _PROVENANCE_IDENTITY_KEYS, f"provenance showcase {entry_id}.frozen_identity")
    _require_exact_keys(fantlab, _PROVENANCE_FANTLAB_KEYS, f"provenance showcase {entry_id}.fantlab_boundary")

    revision_url = _safe_external_url(source.get("revision_url"), f"showcase {entry_id}.source.revision_url")
    revision_manifest = _safe_revision_manifest(
        source.get("revision_manifest"), f"showcase {entry_id}.source.revision_manifest"
    )
    chapter_revision_count = _positive_int(source, "chapter_revision_count", f"showcase {entry_id}.source")
    character_count = _positive_int(frozen, "character_count_including_spaces", f"showcase {entry_id}.frozen_identity")
    normalized_character_count = _positive_int(
        frozen, "normalized_character_count_including_spaces", f"showcase {entry_id}.frozen_identity"
    )
    utf8_byte_count = _positive_int(frozen, "utf8_byte_count", f"showcase {entry_id}.frozen_identity")
    raw_sha256 = _sha256_text(frozen, "raw_sha256", f"showcase {entry_id}.frozen_identity")
    normalized_sha256 = _sha256_text(frozen, "normalized_sha256", f"showcase {entry_id}.frozen_identity")

    work_id = _positive_int(fantlab, "work_id", f"showcase {entry_id}.fantlab_boundary")
    fantlab_url = _safe_external_url(
        fantlab.get("analysis_url"), f"showcase {entry_id}.fantlab_boundary.analysis_url"
    )
    displayed_character_count = _positive_int(
        fantlab, "displayed_character_count", f"showcase {entry_id}.fantlab_boundary"
    )
    displayed_word_count = _positive_int(
        fantlab, "displayed_word_count", f"showcase {entry_id}.fantlab_boundary"
    )
    if fantlab.get("fantlab_source_edition_match") != "unknown":
        raise PublicationBuildError(
            f"provenance showcase {entry_id!r} must preserve unknown FantLab source-edition match"
        )
    if fantlab.get("m2_parity_admissible") is not False:
        raise PublicationBuildError(
            f"provenance showcase {entry_id!r} must remain M2 parity inadmissible"
        )
    if benchmark_admissibility != "diagnostic_only":
        raise PublicationBuildError(
            f"provenance showcase {entry_id!r} must remain diagnostic-only for benchmark use"
        )

    return {
        "render_mode": "provenance",
        "entry_id": entry_id,
        "slug": slug,
        "title": _required_text(entry, "title", f"manifest entry {entry_id}"),
        "publication_status": publication_status,
        "benchmark_admissibility": benchmark_admissibility,
        "corpus_admissibility": corpus_admissibility,
        "compatibility_claim": "extension",
        "author": _required_text(work, "author", f"showcase {entry_id}.work"),
        "work_title": _required_text(work, "title", f"showcase {entry_id}.work"),
        "language": _required_text(work, "language", f"showcase {entry_id}.work"),
        "representativeness_note": _required_text(artifact, "representativeness_note", f"showcase {entry_id}"),
        "provider": _required_text(source, "provider", f"showcase {entry_id}.source"),
        "page": _required_text(source, "page", f"showcase {entry_id}.source"),
        "revision_url": revision_url,
        "edition_note": _required_text(source, "edition_note", f"showcase {entry_id}.source"),
        "legal_basis": _required_text(source, "legal_basis", f"showcase {entry_id}.source"),
        "revision_manifest": revision_manifest,
        "chapter_revision_count": chapter_revision_count,
        "composition_profile": _required_text(source, "composition_profile", f"showcase {entry_id}.source"),
        "extraction_profile": _required_text(source, "extraction_profile", f"showcase {entry_id}.source"),
        "character_count": character_count,
        "normalized_character_count": normalized_character_count,
        "utf8_byte_count": utf8_byte_count,
        "raw_sha256": raw_sha256,
        "normalized_sha256": normalized_sha256,
        "normalization_profile": _required_text(frozen, "normalization_profile", f"showcase {entry_id}.frozen_identity"),
        "fantlab_work_id": work_id,
        "fantlab_url": fantlab_url,
        "fantlab_analysis_date": _required_text(fantlab, "analysis_date", f"showcase {entry_id}.fantlab_boundary"),
        "fantlab_displayed_character_count": displayed_character_count,
        "fantlab_displayed_word_count": displayed_word_count,
        "fantlab_note": _required_text(fantlab, "note", f"showcase {entry_id}.fantlab_boundary"),
    }


def _validate_showcase(
    entry: Mapping[str, Any], artifact: Mapping[str, Any], artifact_raw: bytes | None = None
) -> dict[str, Any]:
    common = _validate_common_entry(entry)
    if common[2] == site_frozen_diagnostic.FROZEN_PROFILE:
        try:
            return site_frozen_diagnostic.prepare(entry, artifact, artifact_raw)
        except ValueError as exc:
            raise PublicationBuildError(str(exc)) from exc
    if common[2] == PROVENANCE_SHOWCASE_PROFILE:
        return _validate_provenance_showcase(entry, artifact, common)
    return _validate_metric_showcase(entry, artifact, common)


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
        '<a class="skip-link" href="#main-content">Skip to main content</a>\n'
        f"{body}\n"
        f'<footer>Generated by {_escape(GENERATOR_PROFILE)} from allow-listed derived artifacts. No source prose is published.</footer>\n'
        "</body>\n</html>\n"
    )


def _render_index(entries: Sequence[Mapping[str, Any]]) -> str:
    cards = []
    for item in entries:
        mode_note = {
            "provenance": " · provenance-only",
            "frozen_diagnostic": " · full-work metrics",
        }.get(item.get("render_mode"), "")
        kind = evidence_kind(item)
        cards.append(
            f'<article class="card" data-evidence-kind="{kind}">'
            f'<p class="eyebrow">{_escape(item["publication_status"])}{_escape(mode_note)}</p>'
            f'<h2><a href="works/{_escape(item["slug"])}/">{_escape(item["title"])}</a></h2>'
            f'<p>{_escape(item["author"])} · {_escape(item["work_title"])}</p>'
            f'<p><strong>Compatibility:</strong> {_escape(item["compatibility_claim"])}</p>'
            f'<p><strong>Benchmark:</strong> {_escape(item["benchmark_admissibility"])} · '
            f'<strong>Corpus:</strong> {_escape(item["corpus_admissibility"])}</p>'
            "</article>"
        )
    featured = next((item for item in entries if item.get("render_mode") == "frozen_diagnostic"), None)
    action = ""
    if featured is not None:
        action = (
            '<p class="actions">'
            f'<a class="primary-action" href="works/{_escape(featured["slug"])}/">'
            f'Explore the {_escape(featured["metric_count"])}-metric full-work report →</a> '
            '<a href="#works">Browse all evidence pages</a></p>'
        )
    comparison = next((item for item in entries if item.get("render_mode") == "comparison"), None)
    if comparison is not None:
        action += (
            '<p class="actions"><a class="primary-action" href="works/'
            + _escape(comparison["slug"])
            + '/">Compare Grin and Verne — two full-length works →</a></p>'
        )
    cards_html = "".join(cards) if cards else '<p class="empty-state">No public analyses are available in this build.</p>'
    body = (
        '<main id="main-content" tabindex="-1"><header class="hero"><p class="eyebrow">Scriptorium · literary analysis</p>'
        '<h1>Explore the language behind a story.</h1>'
        '<p class="lede">Inspect vocabulary, sentence rhythm, dialogue and punctuation in real literary texts. '
        'Each result shows its measurements, source identity and limits.</p>'
        + action
        + '</header><section class="reading-guide" aria-labelledby="reading-guide-title">'
        '<h2 id="reading-guide-title">Read the evidence, not a mystery score</h2>'
        '<ol><li><strong>Choose a work.</strong> Open a measured report and inspect exact units.</li>'
        '<li><strong>Check its limits.</strong> An inferred measurement is not verified FantLab parity.</li>'
        '<li><strong>Compare carefully.</strong> Different source editions and translations remain distinct.</li></ol>'
        '<p>Have your own manuscript? <a href="https://github.com/drevendev/Scriptorium/blob/master/docs/READER_PREVIEW.md">Analyze a text privately with the Reader CLI →</a> No upload is required.</p>'
        '</section>'
        + '<p class="notice">Full-work metrics, illustrative excerpts and provenance-only pages are labelled separately. '
        'FantLab source identity remains unknown for the frozen full-work report: diagnostic evidence is not parity.</p>'
        + '<h2 class="section-title">Published work and evidence</h2>'
        + FILTER_CONTROLS
        + f'<section id="works" aria-label="Published evidence pages" class="grid">{cards_html}</section>'
        + '<script src="assets/evidence-filter.js" defer></script></main>'
    )
    return _page("Scriptorium", "assets/site.css", body)


def _render_metric_work(item: Mapping[str, Any]) -> str:
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
        '<main id="main-content" tabindex="-1"><nav aria-label="Breadcrumb"><a href="../../">← All published analyses</a></nav>'
        f'<p class="eyebrow">{_escape(item["publication_status"])}</p>'
        f'<h1>{_escape(item["title"])}</h1>'
        f'<p class="lede">{_escape(item["author"])} · {_escape(item["work_title"])}</p>'
        '<section class="notice"><strong>Evidence boundary.</strong> '
        f'Compatibility: {_escape(item["compatibility_claim"])}. '
        f'Benchmark: {_escape(item["benchmark_admissibility"])}. '
        f'Corpus: {_escape(item["corpus_admissibility"])}. '
        f'{_escape(item["representativeness_note"])}</section>'
        '<h2>Derived metrics</h2>'
        '<div class="table-wrap" tabindex="0" role="region" aria-label="Derived metrics"><table>'
        '<caption>Derived metrics and their evidence labels</caption><thead><tr>'
        '<th scope="col">Metric</th><th scope="col">Value</th><th scope="col">Unit</th><th scope="col">Evidence</th></tr></thead>'
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


def _render_provenance_work(item: Mapping[str, Any]) -> str:
    revision_url = _escape(item["revision_url"])
    fantlab_url = _escape(item["fantlab_url"])
    body = (
        '<main id="main-content" tabindex="-1"><nav aria-label="Breadcrumb"><a href="../../">← All published analyses</a></nav>'
        f'<p class="eyebrow">{_escape(item["publication_status"])} · provenance-only</p>'
        f'<h1>{_escape(item["title"])}</h1>'
        f'<p class="lede">{_escape(item["author"])} · {_escape(item["work_title"])}</p>'
        '<section class="notice"><strong>Evidence boundary.</strong> '
        'This page freezes a public source candidate; it does not claim that FantLab analyzed the same bytes. '
        f'Benchmark: {_escape(item["benchmark_admissibility"])}. '
        f'Corpus: {_escape(item["corpus_admissibility"])}. '
        f'{_escape(item["representativeness_note"])}</section>'
        '<h2>Frozen source identity</h2><dl>'
        f'<dt>Pinned chapter revisions</dt><dd>{_escape(item["chapter_revision_count"])}</dd>'
        f'<dt>Characters including spaces</dt><dd>{_escape(item["character_count"])}</dd>'
        f'<dt>UTF-8 bytes</dt><dd>{_escape(item["utf8_byte_count"])}</dd>'
        f'<dt>Raw SHA-256</dt><dd><code>{_escape(item["raw_sha256"])}</code></dd>'
        f'<dt>Normalization</dt><dd>{_escape(item["normalization_profile"])}</dd>'
        f'<dt>Normalized characters</dt><dd>{_escape(item["normalized_character_count"])}</dd>'
        f'<dt>Normalized SHA-256</dt><dd><code>{_escape(item["normalized_sha256"])}</code></dd>'
        f'<dt>Composition profile</dt><dd><code>{_escape(item["composition_profile"])}</code></dd>'
        f'<dt>Extraction profile</dt><dd><code>{_escape(item["extraction_profile"])}</code></dd>'
        f'<dt>Revision manifest</dt><dd><code>{_escape(item["revision_manifest"])}</code></dd>'
        '</dl>'
        '<h2>Public-source provenance</h2><dl>'
        f'<dt>Provider</dt><dd>{_escape(item["provider"])}</dd>'
        f'<dt>Source page</dt><dd>{_escape(item["page"])}</dd>'
        f'<dt>Edition</dt><dd>{_escape(item["edition_note"])}</dd>'
        f'<dt>Legal basis</dt><dd>{_escape(item["legal_basis"])}</dd>'
        f'<dt>Immutable source reference</dt><dd><a rel="noreferrer" href="{revision_url}">{revision_url}</a></dd>'
        '</dl>'
        '<h2>FantLab boundary</h2><dl>'
        f'<dt>FantLab work</dt><dd><a rel="noreferrer" href="{fantlab_url}">work {_escape(item["fantlab_work_id"])}</a></dd>'
        f'<dt>Analysis date</dt><dd>{_escape(item["fantlab_analysis_date"])}</dd>'
        f'<dt>Displayed characters</dt><dd>{_escape(item["fantlab_displayed_character_count"])}</dd>'
        f'<dt>Displayed words</dt><dd>{_escape(item["fantlab_displayed_word_count"])}</dd>'
        '<dt>Source-edition match</dt><dd><strong>unknown</strong></dd>'
        '<dt>M2 parity admissible</dt><dd><strong>false</strong></dd>'
        f'</dl><p class="notice">{_escape(item["fantlab_note"])}</p>'
        '<p class="notice">Source text is deliberately not included in this site build.</p></main>'
    )
    return _page(item["title"], "../../assets/site.css", body)


def _render_work(item: Mapping[str, Any]) -> str:
    if item.get("render_mode") == "comparison":
        return item["report_html"]
    if item.get("render_mode") == "frozen_diagnostic":
        return item["report_html"]
    if item.get("render_mode") == "provenance":
        return _render_provenance_work(item)
    return _render_metric_work(item)


_SITE_CSS = """\
:root {
  color-scheme: light;
  --paper: #fbf8f0;
  --surface: #fffdf8;
  --ink: #202d2a;
  --muted: #465954;
  --accent: #13554e;
  --accent-soft: #e6efeb;
  --line: #9fada3;
  --focus: #a54b18;
  font-family: "Iowan Old Style", Georgia, "Times New Roman", serif;
  font-size: 100%;
  line-height: 1.65;
}
* { box-sizing: border-box; }
html { scroll-behavior: smooth; }
body {
  min-width: 0;
  margin: 0;
  color: var(--ink);
  background: radial-gradient(circle at 90% 0%, #efe8d9 0, transparent 32rem), var(--paper);
}
main, footer { max-width: 78rem; margin-inline: auto; padding: clamp(1rem, 4vw, 3rem); }
main { min-height: 70vh; }
footer { border-top: 1px solid var(--line); color: var(--muted); font: .9rem/1.6 system-ui, sans-serif; }
a {
  color: var(--accent);
  text-underline-offset: .2em;
  text-decoration-thickness: .075em;
}
a:hover { text-decoration-thickness: .15em; }
a:focus-visible, :where(button, input, select, textarea, [tabindex]):focus-visible {
  outline: 3px solid var(--focus);
  outline-offset: 4px;
}
.skip-link {
  position: fixed;
  top: .5rem;
  left: .5rem;
  z-index: 100;
  padding: .75rem 1.1rem;
  min-height: 44px;
  background: var(--surface);
  border: 2px solid var(--focus);
  border-radius: .25rem;
  font: 600 .95rem/1.4 system-ui, sans-serif;
}
.skip-link:not(:focus) {
  clip-path: inset(50%);
  width: 1px;
  height: 1px;
  overflow: hidden;
  padding: 0;
  border: 0;
}
.hero {
  padding-block: clamp(2rem, 6vw, 6rem);
  border-bottom: 2px solid var(--ink);
}
.hero h1 { max-width: 17ch; }
h1, h2, h3 { font-weight: 650; text-wrap: balance; }
h1 { font-size: clamp(2.2rem, 6.5vw, 5.4rem); letter-spacing: -.035em; line-height: 1.08; margin-block: .65rem 1.25rem; }
h2 { font-size: clamp(1.5rem, 2.8vw, 2.1rem); line-height: 1.2; }
h3 { font-size: 1.18rem; line-height: 1.3; }
.eyebrow {
  color: var(--muted);
  font: 750 .78rem/1.5 system-ui, sans-serif;
  letter-spacing: .14em;
  text-transform: uppercase;
}
.lede { max-width: 61ch; font-size: clamp(1.1rem, 2vw, 1.35rem); line-height: 1.7; }
.actions { display: flex; flex-wrap: wrap; align-items: center; gap: .7rem 1rem; margin-block: 1.7rem; }
.actions a, nav a, .card h2 a {
  display: inline-flex;
  align-items: center;
  min-height: 44px;
  padding: .55rem .2rem;
}
.primary-action {
  padding: .65rem 1.2rem !important;
  border: 2px solid var(--accent);
  border-radius: .3rem;
  background: var(--accent);
  color: #ffffff;
  font: 700 1rem/1.45 system-ui, sans-serif;
  text-decoration: none;
}
.primary-action:hover { background: var(--ink); border-color: var(--ink); color: #fff; }
.reading-guide { padding-block: clamp(1rem, 3vw, 2rem); }
.reading-guide ol {
  padding: 0;
  margin-block: 1.1rem;
  list-style: none;
  display: grid;
  grid-template-columns: repeat(3, minmax(0, 1fr));
  gap: 1rem;
  counter-reset: read-step;
}
.reading-guide li {
  counter-increment: read-step;
  min-width: 0;
  padding: 1.2rem;
  border-left: 3px solid var(--accent);
  background: var(--surface);
}
.reading-guide li::before {
  content: "0" counter(read-step);
  display: block;
  color: var(--muted);
  font: 750 .85rem/1.5 system-ui, sans-serif;
  letter-spacing: .05em;
  margin-bottom: .6rem;
}
.reading-guide p, .notice { max-width: 80ch; }
.notice {
  padding: clamp(1rem, 2.2vw, 1.5rem);
  margin-block: 2rem;
  border: 1px solid var(--line);
  border-left: 4px solid var(--accent);
  border-radius: .2rem;
  background: var(--accent-soft);
}
.section-title { margin-top: 2.5rem; }
.grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(min(18rem, 100%), 1fr));
  gap: 1rem;
  margin-block: 1.5rem 3rem;
}
.card {
  min-width: 0;
  border: 1px solid var(--line);
  border-radius: .35rem;
  background: var(--surface);
  padding: clamp(1rem, 2vw, 1.6rem);
  box-shadow: 0 5px 0 #aebeb180;
}
.card h2 { font-size: clamp(1.3rem, 2vw, 1.65rem); }
.card p { overflow-wrap: anywhere; }
.empty-state { padding: 2rem; border: 1px dashed var(--line); }
.table-wrap { max-width: 100%; overflow-x: auto; padding-bottom: .3rem; }
.table-wrap:focus-visible { outline: 3px solid var(--focus); outline-offset: 4px; }
table { border-collapse: collapse; width: 100%; font: .94rem/1.5 system-ui, sans-serif; }
caption { text-align: left; font-weight: 700; padding-block: .7rem; }
th, td { border-bottom: 1px solid var(--line); padding: .75rem .65rem; vertical-align: top; text-align: left; }
thead { background: var(--accent-soft); }
tbody tr:nth-child(even) { background: var(--surface); }
dt { margin-top: 1rem; font-weight: 700; }
dd { margin-left: 0; overflow-wrap: anywhere; }
.status { font-weight: 750; }
code { overflow-wrap: anywhere; }
@media (max-width: 720px) {
  .reading-guide ol { grid-template-columns: 1fr; gap: .6rem; }
  .hero { padding-block: 1.5rem 2rem; }
  .actions { align-items: stretch; }
  .actions a { justify-content: center; }
  th, td { padding: .6rem .45rem; }
}
@media (prefers-color-scheme: dark) {
  :root {
    color-scheme: dark;
    --paper: #14201d;
    --surface: #1e2b27;
    --ink: #f2ebdc;
    --muted: #d1d8cf;
    --accent: #a0e2d2;
    --accent-soft: #20372f;
    --line: #73887e;
    --focus: #f2b273;
  }
  body { background: var(--paper); }
  .primary-action { color: #14201d; }
  .primary-action:hover { background: #f2ebdc; border-color: #f2ebdc; color: #14201d; }
  .card { box-shadow: 0 5px 0 #00000035; }
}
@media (prefers-reduced-motion: reduce) {
  html { scroll-behavior: auto; }
  *, *::before, *::after { animation: none !important; transition: none !important; }
}
@media (forced-colors: active) {
  .card, .notice, .primary-action, .reading-guide li { border: 1px solid CanvasText; }
  .primary-action { color: ButtonText; background: ButtonFace; }
}
@media print {
  :root { color-scheme: light; --paper: #fff; --surface: #fff; --ink: #000; --muted: #222; --accent: #000; --accent-soft: #fff; --line: #666; }
  body { background: #fff !important; color: #000 !important; }
  main, footer { max-width: none; min-height: 0; padding: .3cm; }
  .hero { padding: .4cm 0; }
  .skip-link, .actions, nav { display: none !important; }
  .grid, .reading-guide ol { display: block; }
  .card, .reading-guide li, .notice { box-shadow: none; break-inside: avoid; margin-bottom: .4cm; background: #fff; }
  .table-wrap { overflow: visible; }
  a { color: #000; text-decoration: underline; }
  @page { margin: 1.5cm; }
}
"""


def _prepare_output(repo_root: Path, output_dir: Path) -> Path:
    root = repo_root.resolve()
    if output_dir.is_symlink():
        raise PublicationBuildError("output directory must not be a symlink")
    if output_dir.absolute() != output_dir.resolve(strict=False):
        raise PublicationBuildError("output directory must stay inside the repository build/ tree")
    output = output_dir.resolve(strict=False)
    try:
        relative = output.relative_to(root)
    except ValueError as exc:
        raise PublicationBuildError("output directory must stay inside the repository build/ tree") from exc
    if not relative.parts or relative.parts[0] != "build" or len(relative.parts) < 2:
        raise PublicationBuildError("output directory must stay inside the repository build/ tree")
    if output.exists() and not output.is_dir():
        raise PublicationBuildError("output directory must be a directory")
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

        if entry.get("kind") == "work_comparison":
            try:
                site_work_comparison.validate_entry(dict(entry))
                published = site_work_comparison.build(root)
            except site_work_comparison.ComparisonBuildError as exc:
                raise PublicationBuildError(str(exc)) from exc
            item = {
                **site_work_comparison.EXPECTED_ENTRY,
                "render_mode": "comparison",
                "author": "Alexander Grin / Jules Verne",
                "work_title": "Running on Waves / The Children of Captain Grant — Beketova translation",
                "report_html": published["html"],
                "json_data": published["json"],
                "csv_data": published["csv"],
            }
            render_items.append(item)
            input_rows.append({
                "entry_id": entry_id,
                "artifact_paths": published["input_artifacts"],
                "route": f"works/{slug}/",
            })
            continue

        artifact_path = _safe_artifact_path(root, entry.get("artifact_path"))
        artifact, artifact_raw = _read_json(artifact_path)
        item = _validate_showcase(entry, artifact, artifact_raw)
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
    destination = _prepare_output(root, output_path)
    try:
        with staged_site(root, destination) as output:
            (output / "assets").mkdir()
            (output / "assets" / "site.css").write_text(_SITE_CSS + FILTER_CSS, encoding="utf-8", newline="\n")
            (output / "assets" / "evidence-filter.js").write_text(FILTER_JS, encoding="utf-8", newline="\n")
            (output / "index.html").write_text(index_html, encoding="utf-8", newline="\n")
            for slug, page_html in work_pages.items():
                work_dir = output / "works" / slug
                work_dir.mkdir(parents=True)
                (work_dir / "index.html").write_text(page_html, encoding="utf-8", newline="\n")
                registered = next(item for item in render_items if item["slug"] == slug)
                if registered.get("render_mode") == "comparison":
                    (work_dir / "measurements.json").write_text(
                        registered["json_data"], encoding="utf-8", newline="\n"
                    )
                    (work_dir / "measurements.csv").write_text(
                        registered["csv_data"], encoding="utf-8", newline="\n"
                    )
            (output / "build.json").write_text(
                json.dumps(build_record, ensure_ascii=False, indent=2, sort_keys=True) + "\n",
                encoding="utf-8",
                newline="\n",
            )
    except OSError as exc:
        raise PublicationBuildError("atomic site publication failed") from exc
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
