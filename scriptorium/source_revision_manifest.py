"""Pack and decode source-free Wikisource revision identity manifests."""

from __future__ import annotations

import argparse
import base64
from datetime import datetime, timedelta, timezone
import json
from hashlib import sha256
from pathlib import Path
from typing import Mapping, Sequence

from .wikisource_freeze import PART_CHAPTER_COUNTS, expected_chapters


EXPANDED_RECEIPT_VERSION = "scriptorium-source-revision-manifest-v1"
PACKED_MANIFEST_VERSION = "scriptorium-source-revision-packed-manifest-v1"
_SHA1_WIDTH_BYTES = 20
_SHA1_B64_NO_PADDING_WIDTH = 27
_COPY_KEYS = (
    "bibliographic_source",
    "candidate_id",
    "composite_identity",
    "composition",
    "legal_basis",
    "provider",
    "source_work_index_revision_id",
    "source_work_url",
)


def _parse_utc_timestamp(value: object) -> datetime:
    if not isinstance(value, str) or not value.endswith("Z"):
        raise ValueError(f"expected UTC timestamp ending in Z, got {value!r}")
    try:
        parsed = datetime.fromisoformat(value[:-1] + "+00:00")
    except ValueError as exc:
        raise ValueError(f"invalid UTC timestamp {value!r}") from exc
    if parsed.tzinfo != timezone.utc:
        raise ValueError(f"timestamp is not UTC: {value!r}")
    if parsed.microsecond:
        raise ValueError(f"timestamp must have whole-second precision: {value!r}")
    return parsed


def _format_utc_timestamp(value: datetime) -> str:
    return value.astimezone(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def _validated_receipt_rows(receipt: Mapping[str, object]) -> tuple[Mapping[str, object], ...]:
    if receipt.get("manifest_version") != EXPANDED_RECEIPT_VERSION:
        raise ValueError(
            "expanded receipt must use "
            f"{EXPANDED_RECEIPT_VERSION!r}, got {receipt.get('manifest_version')!r}"
        )
    rows = receipt.get("chapters")
    if not isinstance(rows, list):
        raise ValueError("expanded receipt must contain a chapters array")
    expected = expected_chapters()
    if len(rows) != len(expected):
        raise ValueError(f"expected {len(expected)} chapter rows, got {len(rows)}")

    validated: list[Mapping[str, object]] = []
    revision_ids: set[int] = set()
    for chapter, row in zip(expected, rows, strict=True):
        if not isinstance(row, dict):
            raise ValueError("chapter receipt rows must be objects")
        for key in ("ordinal", "part", "chapter", "title"):
            if row.get(key) != chapter[key]:
                raise ValueError(
                    f"chapter identity drift at ordinal {chapter['ordinal']}: "
                    f"{key}={row.get(key)!r}, expected {chapter[key]!r}"
                )
        revision_id = row.get("revision_id")
        if not isinstance(revision_id, int) or revision_id <= 0:
            raise ValueError(f"invalid revision_id at {chapter['title']!r}")
        if revision_id in revision_ids:
            raise ValueError(f"duplicate revision_id {revision_id}")
        revision_ids.add(revision_id)
        _parse_utc_timestamp(row.get("revision_timestamp"))
        mw_sha1 = row.get("mediawiki_sha1")
        if not isinstance(mw_sha1, str) or len(mw_sha1) != 40:
            raise ValueError(f"invalid MediaWiki SHA-1 at {chapter['title']!r}")
        try:
            raw_sha1 = bytes.fromhex(mw_sha1)
        except ValueError as exc:
            raise ValueError(f"invalid MediaWiki SHA-1 at {chapter['title']!r}") from exc
        if len(raw_sha1) != _SHA1_WIDTH_BYTES:
            raise ValueError(f"invalid MediaWiki SHA-1 width at {chapter['title']!r}")
        validated.append(row)
    return tuple(validated)


def chapter_identity_sha256(rows: Sequence[Mapping[str, object]]) -> str:
    """Hash the ordered source-free identity projection of captured chapter rows."""

    projection = [
        {
            key: row[key]
            for key in (
                "ordinal",
                "part",
                "chapter",
                "title",
                "revision_id",
                "revision_timestamp",
                "mediawiki_sha1",
            )
        }
        for row in rows
    ]
    payload = (
        json.dumps(projection, ensure_ascii=False, sort_keys=True, separators=(",", ":"))
        + "\n"
    ).encode("utf-8")
    return sha256(payload).hexdigest()


def pack_revision_manifest(receipt: Mapping[str, object]) -> dict[str, object]:
    """Convert the expanded captured receipt into the canonical packed manifest."""

    rows = _validated_receipt_rows(receipt)
    timestamps = [_parse_utc_timestamp(row["revision_timestamp"]) for row in rows]
    base_timestamp = min(timestamps)
    timestamp_offsets = [int((value - base_timestamp).total_seconds()) for value in timestamps]

    encoded_sha1 = "".join(
        base64.b64encode(bytes.fromhex(str(row["mediawiki_sha1"]))).decode("ascii").rstrip("=")
        for row in rows
    )
    if len(encoded_sha1) != _SHA1_B64_NO_PADDING_WIDTH * len(rows):
        raise AssertionError("unexpected packed MediaWiki SHA-1 width")

    packed = {key: receipt[key] for key in _COPY_KEYS}
    packed["manifest_version"] = PACKED_MANIFEST_VERSION
    packed["chapter_identity_encoding"] = {
        "captured_identity_sha256": chapter_identity_sha256(rows),
        "mediawiki_sha1_base64_no_padding_concat": encoded_sha1,
        "mediawiki_sha1_base64_no_padding_fixed_width": _SHA1_B64_NO_PADDING_WIDTH,
        "order": "part ascending then chapter ascending; counts in composition.part_chapter_counts",
        "revision_ids": [int(row["revision_id"]) for row in rows],
        "revision_timestamp_base": _format_utc_timestamp(base_timestamp),
        "revision_timestamp_offsets_seconds": timestamp_offsets,
    }
    return packed


def decode_chapter_identities(manifest: Mapping[str, object]) -> tuple[dict[str, object], ...]:
    """Decode the packed manifest into ordered chapter revision identities."""

    if manifest.get("manifest_version") != PACKED_MANIFEST_VERSION:
        raise ValueError(
            "packed manifest must use "
            f"{PACKED_MANIFEST_VERSION!r}, got {manifest.get('manifest_version')!r}"
        )
    composition = manifest.get("composition")
    if not isinstance(composition, dict):
        raise ValueError("packed manifest missing composition")
    if composition.get("part_chapter_counts") != list(PART_CHAPTER_COUNTS):
        raise ValueError("packed manifest chapter-count contract drift")

    encoding = manifest.get("chapter_identity_encoding")
    if not isinstance(encoding, dict):
        raise ValueError("packed manifest missing chapter_identity_encoding")
    if encoding.get("order") != (
        "part ascending then chapter ascending; counts in composition.part_chapter_counts"
    ):
        raise ValueError("unsupported packed chapter order")

    expected = expected_chapters()
    revision_ids = encoding.get("revision_ids")
    offsets = encoding.get("revision_timestamp_offsets_seconds")
    width = encoding.get("mediawiki_sha1_base64_no_padding_fixed_width")
    concat = encoding.get("mediawiki_sha1_base64_no_padding_concat")
    if not isinstance(revision_ids, list) or len(revision_ids) != len(expected):
        raise ValueError("packed manifest revision_id count mismatch")
    if not isinstance(offsets, list) or len(offsets) != len(expected):
        raise ValueError("packed manifest timestamp-offset count mismatch")
    if width != _SHA1_B64_NO_PADDING_WIDTH or not isinstance(concat, str):
        raise ValueError("unsupported packed MediaWiki SHA-1 encoding")
    if len(concat) != width * len(expected):
        raise ValueError("packed MediaWiki SHA-1 payload length mismatch")
    base_timestamp = _parse_utc_timestamp(encoding.get("revision_timestamp_base"))

    rows: list[dict[str, object]] = []
    seen_revision_ids: set[int] = set()
    for index, chapter in enumerate(expected):
        revision_id = revision_ids[index]
        offset = offsets[index]
        if not isinstance(revision_id, int) or revision_id <= 0:
            raise ValueError(f"invalid packed revision_id at ordinal {index + 1}")
        if revision_id in seen_revision_ids:
            raise ValueError(f"duplicate packed revision_id {revision_id}")
        seen_revision_ids.add(revision_id)
        if not isinstance(offset, int) or offset < 0:
            raise ValueError(f"invalid packed timestamp offset at ordinal {index + 1}")
        chunk = concat[index * width : (index + 1) * width]
        try:
            raw_sha1 = base64.b64decode(chunk + "=", validate=True)
        except (ValueError, base64.binascii.Error) as exc:
            raise ValueError(f"invalid packed MediaWiki SHA-1 at ordinal {index + 1}") from exc
        if len(raw_sha1) != _SHA1_WIDTH_BYTES:
            raise ValueError(f"invalid packed MediaWiki SHA-1 width at ordinal {index + 1}")
        timestamp = base_timestamp + timedelta(seconds=offset)
        rows.append(
            {
                **chapter,
                "revision_id": revision_id,
                "revision_timestamp": _format_utc_timestamp(timestamp),
                "mediawiki_sha1": raw_sha1.hex(),
            }
        )
    captured_digest = encoding.get("captured_identity_sha256")
    if not isinstance(captured_digest, str) or captured_digest != chapter_identity_sha256(rows):
        raise ValueError("packed captured identity digest mismatch")
    return tuple(rows)


def canonical_json_text(value: Mapping[str, object]) -> str:
    """Return the repository's deterministic compact JSON representation."""

    return json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":")) + "\n"


def main(argv: Sequence[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description="Pack a captured Wikisource revision receipt into the canonical source-free manifest."
    )
    parser.add_argument("--receipt", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args(argv)
    receipt = json.loads(args.receipt.read_text(encoding="utf-8"))
    if not isinstance(receipt, dict):
        raise ValueError("research receipt must be a JSON object")
    packed = pack_revision_manifest(receipt)
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(canonical_json_text(packed), encoding="utf-8")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
