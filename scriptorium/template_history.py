"""Freeze historical MediaWiki template revision identities without source prose.

This module supports provenance reconstruction where a pinned page revision depends on
mutable templates.  It deliberately freezes only a deterministic *revision-selection
policy* and the selected template revision bytes.  Selecting the latest template
revision at or before a page-save timestamp is an inferred reconstruction anchor, not
proof of the exact parser-cache/template state that MediaWiki used for a historical
render.
"""

from __future__ import annotations

import argparse
from datetime import datetime, timezone
from hashlib import sha256
import json
from pathlib import Path
from typing import Callable, Mapping, Sequence
from urllib.parse import quote

from .single_page_revision import _api_query, fetch_pinned_revision


MANIFEST_VERSION = "scriptorium-historical-template-revision-v1"
RESOLUTION_POLICY = "latest_revision_not_after_anchor_timestamp"


def _parse_utc_timestamp(value: object) -> datetime:
    if not isinstance(value, str) or not value.endswith("Z"):
        raise ValueError("timestamp must be an ISO-8601 UTC string ending in Z")
    try:
        parsed = datetime.fromisoformat(value[:-1] + "+00:00")
    except ValueError as exc:
        raise ValueError(f"invalid UTC timestamp {value!r}") from exc
    if parsed.tzinfo != timezone.utc:
        raise ValueError("timestamp must be UTC")
    return parsed


def _source_free_identity(page: Mapping[str, object], revision: Mapping[str, object]) -> dict[str, object]:
    title = page.get("title")
    page_id = page.get("pageid")
    revision_id = revision.get("revid")
    timestamp = revision.get("timestamp")
    mediawiki_sha1 = revision.get("sha1")
    slots = revision.get("slots")
    main = slots.get("main") if isinstance(slots, dict) else None
    wikitext = main.get("content") if isinstance(main, dict) else None
    if not isinstance(title, str) or not title:
        raise ValueError("historical template title missing")
    if not isinstance(page_id, int) or page_id <= 0:
        raise ValueError("historical template page id missing")
    if not isinstance(revision_id, int) or revision_id <= 0:
        raise ValueError("historical template revision id missing")
    if not isinstance(timestamp, str) or not timestamp.endswith("Z"):
        raise ValueError("historical template revision timestamp missing")
    if not isinstance(mediawiki_sha1, str) or len(mediawiki_sha1) != 40:
        raise ValueError("historical template MediaWiki SHA-1 missing")
    try:
        int(mediawiki_sha1, 16)
    except ValueError as exc:
        raise ValueError("historical template MediaWiki SHA-1 is not hex") from exc
    if not isinstance(wikitext, str):
        raise ValueError("historical template main-slot wikitext missing")
    raw = wikitext.encode("utf-8")
    return {
        "title": title,
        "page_id": page_id,
        "revision_id": revision_id,
        "revision_timestamp": timestamp,
        "mediawiki_sha1": mediawiki_sha1,
        "wikitext_character_count": len(wikitext),
        "wikitext_utf8_byte_count": len(raw),
        "wikitext_sha256": sha256(raw).hexdigest(),
    }


def resolve_revision_at_or_before(
    *,
    title: str,
    anchor_timestamp: str,
    query: Callable[[dict[str, str]], dict[str, object]] = _api_query,
) -> dict[str, object]:
    """Resolve the newest revision whose timestamp is not later than ``anchor_timestamp``."""

    if not isinstance(title, str) or not title:
        raise ValueError("title must be non-empty")
    anchor = _parse_utc_timestamp(anchor_timestamp)
    payload = query(
        {
            "action": "query",
            "prop": "revisions",
            "titles": title,
            "rvprop": "ids|timestamp|sha1|content",
            "rvslots": "main",
            "rvlimit": "1",
            "rvstart": anchor_timestamp,
            "rvdir": "older",
        }
    )
    query_obj = payload.get("query")
    if not isinstance(query_obj, dict):
        raise ValueError("MediaWiki response missing query")
    pages = query_obj.get("pages")
    if not isinstance(pages, list) or len(pages) != 1 or not isinstance(pages[0], dict):
        raise ValueError("expected exactly one historical template page")
    page = pages[0]
    if page.get("title") != title:
        raise ValueError(f"historical template title drift: {page.get('title')!r}")
    revisions = page.get("revisions")
    if not isinstance(revisions, list) or len(revisions) != 1 or not isinstance(revisions[0], dict):
        raise ValueError("expected exactly one historical template revision")
    identity = _source_free_identity(page, revisions[0])
    observed = _parse_utc_timestamp(identity["revision_timestamp"])
    if observed > anchor:
        raise ValueError("historical template resolver returned a revision after the anchor")
    return identity


def build_manifest(
    *,
    candidate_id: str,
    title: str,
    anchor_timestamp: str,
    anchor_revision_id: int,
    resolver: Callable[..., dict[str, object]] = resolve_revision_at_or_before,
) -> dict[str, object]:
    if not isinstance(candidate_id, str) or not candidate_id:
        raise ValueError("candidate_id must be non-empty")
    if not isinstance(anchor_revision_id, int) or anchor_revision_id <= 0:
        raise ValueError("anchor_revision_id must be positive")
    _parse_utc_timestamp(anchor_timestamp)
    identity = resolver(title=title, anchor_timestamp=anchor_timestamp)
    revision_id = identity.get("revision_id")
    if not isinstance(revision_id, int):
        raise ValueError("resolved template revision id missing")
    encoded_title = quote(title.replace(" ", "_"), safe="()/:_")
    return {
        "manifest_version": MANIFEST_VERSION,
        "candidate_id": candidate_id,
        "provider": "Russian Wikisource",
        "dependency_kind": "mediawiki_template",
        "resolution_policy": {
            "kind": RESOLUTION_POLICY,
            "anchor_revision_id": anchor_revision_id,
            "anchor_timestamp": anchor_timestamp,
            "evidence_class": "inferred_reconstruction_anchor",
            "historical_render_equivalence_proven": False,
        },
        "source_work_url": f"https://ru.wikisource.org/wiki/{encoded_title}",
        "permanent_source_url": (
            "https://ru.wikisource.org/w/index.php?title="
            f"{encoded_title}&oldid={revision_id}"
        ),
        "source_identity": identity,
        "capture_scope": {
            "historical_revision_selection_frozen": True,
            "template_revision_wikitext_identity_frozen": True,
            "template_expansion_reproduced": False,
            "historical_render_equivalence_proven": False,
            "source_text_committed": False,
        },
        "boundary": (
            "The selected template revision is the latest revision not later than the pinned "
            "anchor page-save timestamp. This is a deterministic reconstruction policy, not proof "
            "of MediaWiki parser-cache or render-time template state. Template expansion remains unfrozen."
        ),
    }


def validate_manifest(manifest: Mapping[str, object]) -> None:
    if manifest.get("manifest_version") != MANIFEST_VERSION:
        raise ValueError("unsupported historical template manifest version")
    if not isinstance(manifest.get("candidate_id"), str) or not manifest["candidate_id"]:
        raise ValueError("historical template candidate_id missing")
    if manifest.get("provider") != "Russian Wikisource":
        raise ValueError("unexpected historical template provider")
    if manifest.get("dependency_kind") != "mediawiki_template":
        raise ValueError("unexpected historical dependency kind")
    policy = manifest.get("resolution_policy")
    if not isinstance(policy, dict) or policy.get("kind") != RESOLUTION_POLICY:
        raise ValueError("historical template resolution policy drift")
    anchor_revision_id = policy.get("anchor_revision_id")
    if not isinstance(anchor_revision_id, int) or anchor_revision_id <= 0:
        raise ValueError("historical template anchor revision id invalid")
    anchor = _parse_utc_timestamp(policy.get("anchor_timestamp"))
    if policy.get("evidence_class") != "inferred_reconstruction_anchor":
        raise ValueError("historical template evidence class drift")
    if policy.get("historical_render_equivalence_proven") is not False:
        raise ValueError("historical render equivalence must remain unproven")
    identity = manifest.get("source_identity")
    if not isinstance(identity, dict):
        raise ValueError("historical template source identity missing")
    required = {
        "title": str,
        "page_id": int,
        "revision_id": int,
        "revision_timestamp": str,
        "mediawiki_sha1": str,
        "wikitext_character_count": int,
        "wikitext_utf8_byte_count": int,
        "wikitext_sha256": str,
    }
    for key, kind in required.items():
        if not isinstance(identity.get(key), kind):
            raise ValueError(f"historical template source identity missing {key}")
    if _parse_utc_timestamp(identity["revision_timestamp"]) > anchor:
        raise ValueError("historical template revision is newer than the anchor")
    mediawiki_sha1 = identity["mediawiki_sha1"]
    wikitext_sha256 = identity["wikitext_sha256"]
    if len(mediawiki_sha1) != 40 or len(wikitext_sha256) != 64:
        raise ValueError("historical template digest width invalid")
    try:
        int(mediawiki_sha1, 16)
        int(wikitext_sha256, 16)
    except ValueError as exc:
        raise ValueError("historical template digest must be hex") from exc
    for key in ("page_id", "revision_id", "wikitext_character_count", "wikitext_utf8_byte_count"):
        if int(identity[key]) <= 0:
            raise ValueError(f"historical template {key} must be positive")
    expected_scope = {
        "historical_revision_selection_frozen": True,
        "template_revision_wikitext_identity_frozen": True,
        "template_expansion_reproduced": False,
        "historical_render_equivalence_proven": False,
        "source_text_committed": False,
    }
    if manifest.get("capture_scope") != expected_scope:
        raise ValueError("historical template capture scope drift")
    forbidden = {"wikitext", "content", "body", "text", "source_text"}
    if forbidden.intersection(manifest) or forbidden.intersection(identity):
        raise ValueError("source prose leaked into historical template manifest")


def replay_manifest(
    manifest: Mapping[str, object],
    *,
    resolver: Callable[..., dict[str, object]] = resolve_revision_at_or_before,
    pinned_fetcher: Callable[..., dict[str, object]] = fetch_pinned_revision,
) -> dict[str, object]:
    validate_manifest(manifest)
    policy = manifest["resolution_policy"]
    identity = manifest["source_identity"]
    assert isinstance(policy, dict)
    assert isinstance(identity, dict)
    title = identity["title"]
    revision_id = identity["revision_id"]
    assert isinstance(title, str)
    assert isinstance(revision_id, int)
    selected = resolver(title=title, anchor_timestamp=policy["anchor_timestamp"])
    if selected != identity:
        raise ValueError("historical template revision selection drift")
    pinned = pinned_fetcher(title=title, revision_id=revision_id)
    if pinned != identity:
        raise ValueError("historical template pinned revision identity drift")
    return {
        "receipt_version": "scriptorium-historical-template-replay-v1",
        "candidate_id": manifest["candidate_id"],
        "revision_id": revision_id,
        "wikitext_sha256": identity["wikitext_sha256"],
        "verified": True,
        "source_text_committed": False,
        "historical_render_equivalence_proven": False,
        "template_expansion_reproduced": False,
    }


def _write_json(path: Path, value: Mapping[str, object]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def main(argv: Sequence[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Capture/replay a historical Wikisource template revision identity.")
    subparsers = parser.add_subparsers(dest="command", required=True)
    capture = subparsers.add_parser("capture")
    capture.add_argument("--candidate-id", required=True)
    capture.add_argument("--title", required=True)
    capture.add_argument("--anchor-timestamp", required=True)
    capture.add_argument("--anchor-revision-id", type=int, required=True)
    capture.add_argument("--output", type=Path, required=True)
    replay = subparsers.add_parser("replay")
    replay.add_argument("--manifest", type=Path, required=True)
    replay.add_argument("--receipt", type=Path)
    args = parser.parse_args(argv)
    if args.command == "capture":
        manifest = build_manifest(
            candidate_id=args.candidate_id,
            title=args.title,
            anchor_timestamp=args.anchor_timestamp,
            anchor_revision_id=args.anchor_revision_id,
        )
        validate_manifest(manifest)
        _write_json(args.output, manifest)
        return 0
    manifest_obj = json.loads(args.manifest.read_text(encoding="utf-8"))
    if not isinstance(manifest_obj, dict):
        raise ValueError("manifest must be a JSON object")
    receipt = replay_manifest(manifest_obj)
    if args.receipt is not None:
        _write_json(args.receipt, receipt)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
