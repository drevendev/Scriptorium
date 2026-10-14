"""Publish only the explicitly reviewed frozen full-work diagnostic snapshot.

Digest approval is a publication boundary, not an assertion of FantLab source identity.
The historical artifact stays immutable; new snapshots require a reviewed registration.
"""

from __future__ import annotations

from collections.abc import Mapping
from hashlib import sha256
import json
from typing import Any

from . import frozen_diagnostic_report as report


FROZEN_PROFILE = report.SCHEMA_VERSION
ARTIFACT_PATH = "benchmarks/fantlab/work270306-wikisource-diagnostic.json"
ARTIFACT_SHA256 = "2a25c3d2df91c2f26b283ec40055ca20248f865cffadc932026cf9c98b5d0e8b"
ENTRY_ID = "tolstoy-anna-karenina-full-work-diagnostic-v1"
SLUG = "anna-karenina-full-work-diagnostic"
_DECLARATION = {
    "entry_id": ENTRY_ID,
    "kind": "work_showcase",
    "slug": SLUG,
    "artifact_path": ARTIFACT_PATH,
    "artifact_schema": FROZEN_PROFILE,
    "publication_status": "diagnostic",
    "benchmark_admissibility": "diagnostic_only",
    "corpus_admissibility": "not_admissible",
    "compatibility_claim": "inferred",
    "source_text_included": False,
}


def prepare(
    entry: Mapping[str, Any], artifact: Mapping[str, Any], raw: bytes | None
) -> dict[str, Any]:
    """Validate the publication registration and reuse the standalone report renderer."""
    if set(entry) != {*_DECLARATION, "title"}:
        raise ValueError("frozen diagnostic declaration keys drift")
    for key, expected in _DECLARATION.items():
        actual = entry.get(key)
        if type(actual) is not type(expected) or actual != expected:
            raise ValueError(f"frozen diagnostic declaration mismatch: {key}")
    if not isinstance(raw, bytes) or sha256(raw).hexdigest() != ARTIFACT_SHA256:
        raise ValueError("frozen diagnostic bytes do not match the reviewed SHA-256")
    if json.loads(raw) != artifact:
        raise ValueError("frozen diagnostic object differs from its verified bytes")
    value = report.validate_artifact(artifact)
    if value["candidate_id"] != "tolstoy-anna-karenina-ru":
        raise ValueError("frozen diagnostic candidate identity drift")
    title = entry["title"]
    rendered = report.render_html(value, title=title)
    # The reused renderer owns all metric tables, values, units and historical labels.
    # Add only navigation to the site's work list and a focusable skip-link destination.
    if rendered.count("<main>") != 1 or rendered.count('<div id="metrics">') != 1:
        raise ValueError("frozen diagnostic navigation integration marker drift")
    rendered = rendered.replace(
        "<main>",
        '<main id="main-content" tabindex="-1"><nav aria-label="Work navigation">'
        '<a href="../../">← All published analyses</a></nav>',
        1,
    ).replace('<div id="metrics">', '<div id="metrics" tabindex="-1">', 1)
    return {
        **_DECLARATION,
        "render_mode": "frozen_diagnostic",
        "title": title,
        "author": "Leo Tolstoy",
        "work_title": "Anna Karenina",
        "metric_count": report.summarize(value)["metric_count"],
        "report_html": rendered,
    }
