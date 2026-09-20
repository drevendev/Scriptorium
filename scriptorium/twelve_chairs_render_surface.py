"""Audit exact 1928 Twelve Chairs Page markup without persisting source prose.

The 410 already-pinned canonical Page revisions are replayed transiently, identity-
checked, and reduced to source-free construct shapes plus per-Page digests/signatures.
This is a renderer prerequisite only: no rendering profile, literary body, corpus
admission, FantLab source match, diagnostics, or parity claim is frozen here.
"""

from __future__ import annotations

import argparse
from collections import Counter
from hashlib import sha256
import json
from pathlib import Path
from typing import Callable, Iterable, Mapping, Sequence

from .darwin_page_freeze import CAPTURE_BATCH_SIZE, _api_query
from .darwin_render_surface import audit_wikitext
from .twelve_chairs_page_freeze import (
    CANDIDATE_ID,
    EXPECTED_PAGE_COUNT,
    FAMILY_ID,
    load_sharded_manifest,
)

AUDIT_VERSION = "scriptorium-twelve-chairs-render-surface-audit-v1"
PROFILE_STATUS = "surface_inventory_verified_renderer_unfrozen"


def _canonical_json(value: object) -> str:
    return json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":"))


def _sha256_text(text: str) -> str:
    return sha256(text.encode("utf-8")).hexdigest()


def fetch_pinned_wikitext(
    rows: Iterable[Mapping[str, object]],
    *,
    query: Callable[[Mapping[str, str]], dict[str, object]] = _api_query,
) -> dict[int, str]:
    expected = tuple(rows)
    if len(expected) != EXPECTED_PAGE_COUNT:
        raise ValueError(f"expected exactly {EXPECTED_PAGE_COUNT} frozen Page identities")

    fetched: dict[int, str] = {}
    for offset in range(0, len(expected), CAPTURE_BATCH_SIZE):
        batch = expected[offset : offset + CAPTURE_BATCH_SIZE]
        ids = [int(row["revision_id"]) for row in batch]
        by_id = {int(row["revision_id"]): row for row in batch}
        payload = query(
            {
                "action": "query",
                "prop": "revisions",
                "revids": "|".join(map(str, ids)),
                "rvprop": "ids|timestamp|sha1|content",
                "rvslots": "main",
            }
        )
        query_obj = payload.get("query")
        pages = query_obj.get("pages") if isinstance(query_obj, dict) else None
        if not isinstance(pages, list):
            raise ValueError("MediaWiki content replay response missing pages")
        for page in pages:
            if not isinstance(page, dict):
                raise ValueError("unexpected MediaWiki content replay page")
            revisions = page.get("revisions")
            if not isinstance(revisions, list) or len(revisions) != 1:
                raise ValueError("unexpected MediaWiki content replay shape")
            revision = revisions[0]
            if not isinstance(revision, dict):
                raise ValueError("unexpected MediaWiki content revision")
            revid = revision.get("revid")
            if not isinstance(revid, int) or revid not in by_id or revid in fetched:
                raise ValueError(f"unexpected/duplicate pinned revision ID: {revid!r}")
            row = by_id[revid]
            if (
                page.get("title") != row["title"]
                or revision.get("timestamp") != row["timestamp"]
                or revision.get("sha1") != row["mediawiki_sha1"]
            ):
                raise ValueError(f"pinned Page identity drift before markup audit: {revid}")
            slots = revision.get("slots")
            main = slots.get("main") if isinstance(slots, dict) else None
            content = main.get("content") if isinstance(main, dict) else None
            if not isinstance(content, str):
                raise ValueError(f"missing exact Page wikitext for revision {revid}")
            fetched[revid] = content

    expected_ids = {int(row["revision_id"]) for row in expected}
    if set(fetched) != expected_ids:
        raise ValueError("Page content replay inventory mismatch")
    return fetched


def build_audit_manifest(
    index_path: Path,
    *,
    fetcher: Callable[[Iterable[Mapping[str, object]]], dict[int, str]] = fetch_pinned_wikitext,
) -> dict[str, object]:
    rows = load_sharded_manifest(index_path)
    if len(rows) != EXPECTED_PAGE_COUNT:
        raise ValueError("frozen Twelve Chairs dependency count drift")
    fetched = fetcher(rows)

    templates: Counter[tuple[str, int, int]] = Counter()
    tags: Counter[tuple[str, str]] = Counter()
    totals: Counter[str] = Counter()
    receipts: list[dict[str, object]] = []

    for row in rows:
        revid = int(row["revision_id"])
        wikitext = fetched[revid]
        try:
            summary = audit_wikitext(wikitext)
        except ValueError as exc:
            raise ValueError(f"Page {row['page_sequence']} revision {revid}: {exc}") from exc
        for item in summary["template_shapes"]:
            templates[(str(item["name"]), int(item["positional"]), int(item["named"]))] += int(item["count"])
        for item in summary["tag_shapes"]:
            tags[(str(item["name"]), str(item["kind"]))] += int(item["count"])
        for key in (
            "comment_count",
            "noinclude_block_count",
            "template_parameter_count",
            "wikilink_count",
            "external_link_count",
            "heading_count",
            "table_open_count",
            "table_close_count",
        ):
            totals[key] += int(summary[key])
        receipts.append(
            {
                "page_sequence": int(row["page_sequence"]),
                "revision_id": revid,
                "mediawiki_sha1": row["mediawiki_sha1"],
                "wikitext_sha256": _sha256_text(wikitext),
                "surface_signature_sha256": summary["surface_signature_sha256"],
                "template_invocation_count": sum(int(item["count"]) for item in summary["template_shapes"]),
                "tag_token_count": sum(int(item["count"]) for item in summary["tag_shapes"]),
            }
        )

    manifest: dict[str, object] = {
        "audit_version": AUDIT_VERSION,
        "candidate_id": CANDIDATE_ID,
        "family_id": FAMILY_ID,
        "status": PROFILE_STATUS,
        "source_revision_index_sha256": sha256(index_path.read_bytes()).hexdigest(),
        "dependency_count": len(rows),
        "identity_replay_match": True,
        "source_text_included": False,
        "template_shapes": [
            {"name": name, "positional": positional, "named": named, "count": count}
            for (name, positional, named), count in sorted(templates.items())
        ],
        "tag_shapes": [
            {"name": name, "kind": kind, "count": count}
            for (name, kind), count in sorted(tags.items())
        ],
        "construct_totals": dict(sorted(totals.items())),
        "page_surface_receipts": receipts,
        "rendering_profile_frozen": False,
        "inter_page_composition_frozen": False,
        "literary_body_count_and_digests_frozen": False,
        "minimum_300k_proved": False,
        "admitted_for_calibration": False,
        "fantlab_source_edition_match": "unknown",
        "diagnostic_ready": False,
        "m2_parity_admissible": False,
    }
    manifest["audit_sha256"] = _sha256_text(_canonical_json(manifest))
    return manifest


def validate_audit_manifest(manifest: Mapping[str, object]) -> None:
    if manifest.get("audit_version") != AUDIT_VERSION:
        raise ValueError("Twelve Chairs rendering-surface audit version drift")
    if manifest.get("candidate_id") != CANDIDATE_ID or manifest.get("family_id") != FAMILY_ID:
        raise ValueError("Twelve Chairs rendering-surface candidate/family drift")
    if manifest.get("status") != PROFILE_STATUS or manifest.get("dependency_count") != EXPECTED_PAGE_COUNT:
        raise ValueError("Twelve Chairs rendering-surface status/dependency drift")
    if manifest.get("identity_replay_match") is not True or manifest.get("source_text_included") is not False:
        raise ValueError("Twelve Chairs rendering-surface source boundary drift")
    receipts = manifest.get("page_surface_receipts")
    if not isinstance(receipts, list) or len(receipts) != EXPECTED_PAGE_COUNT:
        raise ValueError("Twelve Chairs rendering-surface receipt count drift")
    allowed_receipt_keys = {
        "page_sequence",
        "revision_id",
        "mediawiki_sha1",
        "wikitext_sha256",
        "surface_signature_sha256",
        "template_invocation_count",
        "tag_token_count",
    }
    if any(not isinstance(row, dict) or set(row) != allowed_receipt_keys for row in receipts):
        raise ValueError("source payload key or receipt shape drift")
    for forbidden in ("wikitext", "text", "content", "ocr", "rendered_prose", "source_text"):
        if forbidden in manifest:
            raise ValueError(f"source payload key forbidden: {forbidden}")
    for key in (
        "rendering_profile_frozen",
        "inter_page_composition_frozen",
        "literary_body_count_and_digests_frozen",
        "minimum_300k_proved",
        "admitted_for_calibration",
        "diagnostic_ready",
        "m2_parity_admissible",
    ):
        if manifest.get(key) is not False:
            raise ValueError(f"{key} must remain false")
    if manifest.get("fantlab_source_edition_match") != "unknown":
        raise ValueError("FantLab source-edition match must remain unknown")
    for key in ("template_shapes", "tag_shapes", "construct_totals"):
        if key not in manifest:
            raise ValueError(f"missing rendering-surface field: {key}")
    digest = manifest.get("audit_sha256")
    unsigned = dict(manifest)
    unsigned.pop("audit_sha256", None)
    if digest != _sha256_text(_canonical_json(unsigned)):
        raise ValueError("Twelve Chairs rendering-surface audit digest drift")


def _write_json(path: Path, payload: Mapping[str, object]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def main(argv: Sequence[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--index", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args(argv)
    manifest = build_audit_manifest(args.index)
    validate_audit_manifest(manifest)
    _write_json(args.output, manifest)
    print(json.dumps({
        "audit_sha256": manifest["audit_sha256"],
        "dependency_count": manifest["dependency_count"],
        "source_text_included": manifest["source_text_included"],
    }, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
