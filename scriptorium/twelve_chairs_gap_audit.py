"""Inspect the four non-transcluded Twelve Chairs scan gaps without persisting source text.

Exact Page revisions are read transiently and reduced to identities, hashes/counts and a
conservative body-presence class. The 410-Page dependency set, literary-body renderer,
composition, corpus admission and FantLab source-match gates remain unchanged.
"""

from __future__ import annotations

import argparse
from datetime import datetime, timezone
from hashlib import sha256
import json
from pathlib import Path
import re
import unicodedata
from typing import Callable, Mapping, Sequence

from .darwin_page_freeze import _api_query
from .twelve_chairs_page_freeze import (
    CANDIDATE_ID,
    FAMILY_ID,
    NON_TRANSCLUDED_GAPS,
    PAGE_TITLE_PREFIX,
)

GAP_SEQUENCES = tuple(page for start, end in NON_TRANSCLUDED_GAPS for page in range(start, end + 1))
EXPECTED_GAP_COUNT = 4
MANIFEST_VERSION = "scriptorium-twelve-chairs-gap-audit-v1"
REPLAY_VERSION = "scriptorium-twelve-chairs-gap-audit-replay-v1"
BODY_CLASSES = {"no_transcluded_body", "nonempty_body_unclassified"}

_COMMENT_RE = re.compile(r"<!--.*?-->", re.DOTALL)
_NOINCLUDE_BLOCK_RE = re.compile(r"<noinclude\b[^>]*>.*?</noinclude\s*>", re.I | re.S)
_NOINCLUDE_EMPTY_RE = re.compile(r"<noinclude\b[^>]*/\s*>", re.I)
_NOINCLUDE_TOKEN_RE = re.compile(r"</?noinclude\b", re.I)


def _sha256_text(text: str) -> str:
    return sha256(text.encode("utf-8")).hexdigest()


def expected_gap_pages() -> tuple[dict[str, object], ...]:
    if GAP_SEQUENCES != (150, 151, 314, 315):
        raise AssertionError("Twelve Chairs gap topology drift")
    return tuple(
        {
            "ordinal": ordinal,
            "page_sequence": sequence,
            "title": f"{PAGE_TITLE_PREFIX}{sequence}",
        }
        for ordinal, sequence in enumerate(GAP_SEQUENCES, start=1)
    )


def _strip_nontranscluded_regions(wikitext: str) -> tuple[str, int, int]:
    comment_count = len(_COMMENT_RE.findall(wikitext))
    text = _COMMENT_RE.sub("", wikitext)
    noinclude_block_count = len(_NOINCLUDE_BLOCK_RE.findall(text))
    text = _NOINCLUDE_BLOCK_RE.sub("", text)
    text = _NOINCLUDE_EMPTY_RE.sub("", text)
    if _NOINCLUDE_TOKEN_RE.search(text):
        raise ValueError("unbalanced noinclude markup in gap Page wikitext")
    return text, comment_count, noinclude_block_count


def summarize_wikitext(wikitext: str) -> dict[str, object]:
    """Reduce exact Page wikitext to source-free structural evidence."""
    if not isinstance(wikitext, str):
        raise TypeError("wikitext must be str")
    body, comment_count, noinclude_block_count = _strip_nontranscluded_regions(wikitext)
    non_whitespace = sum(not char.isspace() for char in body)
    letter_count = sum(unicodedata.category(char).startswith("L") for char in body)
    number_count = sum(unicodedata.category(char).startswith("N") for char in body)
    body_class = "no_transcluded_body" if not body.strip() else "nonempty_body_unclassified"
    return {
        "raw_wikitext_utf8_bytes": len(wikitext.encode("utf-8")),
        "raw_wikitext_sha256": _sha256_text(wikitext),
        "comment_count": comment_count,
        "noinclude_block_count": noinclude_block_count,
        "transcluded_body_codepoints": len(body),
        "transcluded_body_utf8_bytes": len(body.encode("utf-8")),
        "transcluded_body_non_whitespace_codepoints": non_whitespace,
        "transcluded_body_letter_codepoints": letter_count,
        "transcluded_body_number_codepoints": number_count,
        "transcluded_body_sha256": _sha256_text(body),
        "body_presence_class": body_class,
    }


def _extract_revision(page: Mapping[str, object]) -> tuple[int, str, str, str]:
    revisions = page.get("revisions")
    if not isinstance(revisions, list) or len(revisions) != 1 or not isinstance(revisions[0], dict):
        raise ValueError("unexpected MediaWiki gap revision shape")
    revision = revisions[0]
    revid = revision.get("revid")
    timestamp = revision.get("timestamp")
    mediawiki_sha1 = revision.get("sha1")
    slots = revision.get("slots")
    main = slots.get("main") if isinstance(slots, dict) else None
    content = main.get("content") if isinstance(main, dict) else None
    if not isinstance(revid, int) or not isinstance(timestamp, str) or not isinstance(mediawiki_sha1, str):
        raise ValueError("incomplete MediaWiki gap revision identity")
    if not isinstance(content, str):
        raise ValueError("missing exact gap Page wikitext")
    return revid, timestamp, mediawiki_sha1, content


def fetch_current_gap_pages(
    *, query: Callable[[Mapping[str, str]], dict[str, object]] = _api_query
) -> dict[str, dict[str, object]]:
    titles = [str(row["title"]) for row in expected_gap_pages()]
    payload = query({
        "action": "query",
        "prop": "revisions",
        "titles": "|".join(titles),
        "rvprop": "ids|timestamp|sha1|content",
        "rvslots": "main",
        "redirects": "0",
    })
    query_obj = payload.get("query")
    pages = query_obj.get("pages") if isinstance(query_obj, dict) else None
    if not isinstance(pages, list):
        raise ValueError("MediaWiki gap capture response missing pages")
    records: dict[str, dict[str, object]] = {}
    for page in pages:
        if not isinstance(page, dict):
            raise ValueError("unexpected MediaWiki gap page")
        title = page.get("title")
        if not isinstance(title, str) or title not in titles or page.get("missing") is True:
            raise ValueError(f"unexpected/missing gap Page: {title!r}")
        revid, timestamp, mediawiki_sha1, content = _extract_revision(page)
        records[title] = {
            "revision_id": revid,
            "timestamp": timestamp,
            "mediawiki_sha1": mediawiki_sha1,
            "wikitext": content,
        }
    if set(records) != set(titles):
        raise ValueError("gap Page inventory mismatch")
    return records


def fetch_pinned_gap_pages(
    rows: Sequence[Mapping[str, object]],
    *, query: Callable[[Mapping[str, str]], dict[str, object]] = _api_query
) -> dict[int, dict[str, object]]:
    expected = tuple(rows)
    revision_ids = [int(row["revision_id"]) for row in expected]
    payload = query({
        "action": "query",
        "prop": "revisions",
        "revids": "|".join(map(str, revision_ids)),
        "rvprop": "ids|timestamp|sha1|content",
        "rvslots": "main",
    })
    query_obj = payload.get("query")
    pages = query_obj.get("pages") if isinstance(query_obj, dict) else None
    if not isinstance(pages, list):
        raise ValueError("MediaWiki gap replay response missing pages")
    by_id: dict[int, dict[str, object]] = {}
    for page in pages:
        if not isinstance(page, dict):
            raise ValueError("unexpected MediaWiki gap replay page")
        title = page.get("title")
        revid, timestamp, mediawiki_sha1, content = _extract_revision(page)
        if revid not in revision_ids or revid in by_id:
            raise ValueError(f"unexpected/duplicate pinned gap revision: {revid}")
        by_id[revid] = {
            "title": title,
            "timestamp": timestamp,
            "mediawiki_sha1": mediawiki_sha1,
            "wikitext": content,
        }
    if set(by_id) != set(revision_ids):
        raise ValueError("pinned gap revision inventory mismatch")
    return by_id


def build_gap_audit_manifest(
    *,
    fetcher: Callable[[], dict[str, dict[str, object]]] = fetch_current_gap_pages,
    captured_at: str | None = None,
) -> dict[str, object]:
    records = fetcher()
    rows: list[dict[str, object]] = []
    seen_revisions: set[int] = set()
    for expected in expected_gap_pages():
        title = str(expected["title"])
        record = records[title]
        revid = record.get("revision_id")
        if not isinstance(revid, int) or revid in seen_revisions:
            raise ValueError(f"duplicate/invalid gap revision ID for {title}")
        seen_revisions.add(revid)
        wikitext = record.get("wikitext")
        if not isinstance(wikitext, str):
            raise ValueError(f"missing transient wikitext for {title}")
        rows.append({
            "ordinal": expected["ordinal"],
            "page_sequence": expected["page_sequence"],
            "title": title,
            "revision_id": revid,
            "timestamp": record["timestamp"],
            "mediawiki_sha1": record["mediawiki_sha1"],
            "permanent_url": f"https://ru.wikisource.org/w/index.php?oldid={revid}",
            **summarize_wikitext(wikitext),
        })
    all_empty = all(row["body_presence_class"] == "no_transcluded_body" for row in rows)
    return {
        "manifest_version": MANIFEST_VERSION,
        "candidate_id": CANDIDATE_ID,
        "family_id": FAMILY_ID,
        "captured_at_utc": captured_at
        or datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z"),
        "source_text_included": False,
        "gap_sequences": list(GAP_SEQUENCES),
        "gap_dependency_status": "outside_410_dependency_set_inspected_not_composed",
        "dependency_inventory_unchanged": True,
        "gap_pages": rows,
        "all_gap_pages_have_no_transcluded_body": all_empty,
        "literary_membership_frozen": False,
        "literary_body_frozen": False,
        "admitted_for_calibration": False,
        "fantlab_source_edition_match": "unknown",
        "diagnostic_ready": False,
        "m2_parity_admissible": False,
    }


def validate_gap_audit_manifest(manifest: Mapping[str, object]) -> tuple[dict[str, object], ...]:
    if manifest.get("manifest_version") != MANIFEST_VERSION:
        raise ValueError("unexpected gap audit manifest version")
    if manifest.get("candidate_id") != CANDIDATE_ID or manifest.get("family_id") != FAMILY_ID:
        raise ValueError("gap audit candidate/family mismatch")
    if manifest.get("source_text_included") is not False or manifest.get("dependency_inventory_unchanged") is not True:
        raise ValueError("gap audit source/dependency boundary drift")
    if manifest.get("gap_sequences") != list(GAP_SEQUENCES):
        raise ValueError("gap sequence contract drift")
    if manifest.get("gap_dependency_status") != "outside_410_dependency_set_inspected_not_composed":
        raise ValueError("gap dependency status drift")
    for key in ("literary_membership_frozen", "literary_body_frozen", "admitted_for_calibration", "diagnostic_ready", "m2_parity_admissible"):
        if manifest.get(key) is not False:
            raise ValueError(f"{key} must remain false")
    if manifest.get("fantlab_source_edition_match") != "unknown":
        raise ValueError("FantLab source-edition match must remain unknown")
    pages = manifest.get("gap_pages")
    if not isinstance(pages, list) or len(pages) != EXPECTED_GAP_COUNT:
        raise ValueError("gap audit must contain exactly four source-free Page receipts")
    allowed_keys = {
        "ordinal", "page_sequence", "title", "revision_id", "timestamp", "mediawiki_sha1", "permanent_url",
        "raw_wikitext_utf8_bytes", "raw_wikitext_sha256", "comment_count", "noinclude_block_count",
        "transcluded_body_codepoints", "transcluded_body_utf8_bytes", "transcluded_body_non_whitespace_codepoints",
        "transcluded_body_letter_codepoints", "transcluded_body_number_codepoints", "transcluded_body_sha256",
        "body_presence_class",
    }
    expected = {int(row["page_sequence"]): row for row in expected_gap_pages()}
    normalized: list[dict[str, object]] = []
    seen_revisions: set[int] = set()
    for raw in pages:
        if not isinstance(raw, dict) or set(raw) != allowed_keys:
            raise ValueError("gap Page receipt shape drift or source payload key detected")
        sequence = raw.get("page_sequence")
        revid = raw.get("revision_id")
        if not isinstance(sequence, int) or sequence not in expected:
            raise ValueError(f"unexpected gap Page sequence: {sequence!r}")
        if not isinstance(revid, int) or revid in seen_revisions:
            raise ValueError("duplicate/invalid gap revision ID")
        expected_row = expected[sequence]
        if raw.get("ordinal") != expected_row["ordinal"] or raw.get("title") != expected_row["title"]:
            raise ValueError(f"gap Page identity mismatch for {sequence}")
        if raw.get("permanent_url") != f"https://ru.wikisource.org/w/index.php?oldid={revid}":
            raise ValueError(f"gap permanent URL mismatch for {sequence}")
        if not isinstance(raw.get("timestamp"), str) or not isinstance(raw.get("mediawiki_sha1"), str):
            raise ValueError(f"incomplete gap identity for {sequence}")
        for key in (
            "raw_wikitext_utf8_bytes", "comment_count", "noinclude_block_count", "transcluded_body_codepoints",
            "transcluded_body_utf8_bytes", "transcluded_body_non_whitespace_codepoints",
            "transcluded_body_letter_codepoints", "transcluded_body_number_codepoints",
        ):
            if not isinstance(raw.get(key), int) or int(raw[key]) < 0:
                raise ValueError(f"invalid source-free count {key} for {sequence}")
        for key in ("raw_wikitext_sha256", "transcluded_body_sha256"):
            value = raw.get(key)
            if not isinstance(value, str) or len(value) != 64:
                raise ValueError(f"invalid digest {key} for {sequence}")
        if raw.get("body_presence_class") not in BODY_CLASSES:
            raise ValueError(f"invalid body presence class for {sequence}")
        seen_revisions.add(revid)
        normalized.append(dict(raw))
    normalized.sort(key=lambda row: int(row["ordinal"]))
    if tuple(int(row["page_sequence"]) for row in normalized) != GAP_SEQUENCES:
        raise ValueError("gap Page ordering drift")
    all_empty = all(row["body_presence_class"] == "no_transcluded_body" for row in normalized)
    if manifest.get("all_gap_pages_have_no_transcluded_body") is not all_empty:
        raise ValueError("aggregate gap body-presence flag mismatch")
    return tuple(normalized)


def replay_gap_audit_manifest(
    manifest: Mapping[str, object],
    *, fetcher: Callable[[Sequence[Mapping[str, object]]], dict[int, dict[str, object]]] = fetch_pinned_gap_pages,
) -> dict[str, object]:
    rows = validate_gap_audit_manifest(manifest)
    fetched = fetcher(rows)
    mismatches: list[int] = []
    for row in rows:
        revid = int(row["revision_id"])
        record = fetched[revid]
        if (
            record.get("title") != row["title"]
            or record.get("timestamp") != row["timestamp"]
            or record.get("mediawiki_sha1") != row["mediawiki_sha1"]
        ):
            mismatches.append(revid)
            continue
        summary = summarize_wikitext(str(record["wikitext"]))
        for key, value in summary.items():
            if row.get(key) != value:
                mismatches.append(revid)
                break
    if mismatches:
        raise ValueError(f"pinned gap audit mismatch: {mismatches!r}")
    canonical = json.dumps(manifest, ensure_ascii=False, indent=2, sort_keys=True) + "\n"
    return {
        "receipt_version": REPLAY_VERSION,
        "candidate_id": CANDIDATE_ID,
        "gap_page_count": EXPECTED_GAP_COUNT,
        "gap_sequences": list(GAP_SEQUENCES),
        "manifest_sha256": sha256(canonical.encode("utf-8")).hexdigest(),
        "identity_and_source_free_summary_replay_match": True,
        "body_presence_classes": [row["body_presence_class"] for row in rows],
        "source_text_included": False,
        "dependency_inventory_unchanged": True,
        "literary_body_frozen": False,
        "admitted_for_calibration": False,
        "fantlab_source_edition_match": "unknown",
        "diagnostic_ready": False,
        "m2_parity_admissible": False,
    }


def _load_object(path: Path) -> dict[str, object]:
    payload = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(payload, dict):
        raise ValueError("gap audit JSON root must be an object")
    return payload


def _write_json(path: Path, payload: Mapping[str, object]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def main(argv: Sequence[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    sub = parser.add_subparsers(dest="command", required=True)
    capture = sub.add_parser("capture")
    capture.add_argument("--manifest", type=Path, required=True)
    replay = sub.add_parser("replay")
    replay.add_argument("--manifest", type=Path, required=True)
    replay.add_argument("--receipt", type=Path, required=True)
    args = parser.parse_args(argv)
    if args.command == "capture":
        payload = build_gap_audit_manifest()
        validate_gap_audit_manifest(payload)
        _write_json(args.manifest, payload)
    else:
        manifest = _load_object(args.manifest)
        payload = replay_gap_audit_manifest(manifest)
        _write_json(args.receipt, payload)
    print(json.dumps(payload, ensure_ascii=False, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
