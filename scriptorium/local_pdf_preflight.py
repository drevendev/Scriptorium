"""Source-free local PDF text-layer preflight; no corpus or rights decision."""
from __future__ import annotations

import argparse
import hashlib
import json
import os
from pathlib import Path
import re
import subprocess

VERSION = "scriptorium-local-pdf-preflight-v1"
MAX_BYTES = 256 * 1024 * 1024
MAX_SAMPLE = 32
MAX_COMPLETE_PAGES = 1024
COMPLETE_VERSION = "scriptorium-local-pdf-complete-text-layer-v1"


def file_identity(path: Path) -> dict:
    digest = hashlib.sha256()
    size = 0
    with path.open("rb") as stream:
        if stream.read(5) != b"%PDF-":
            raise ValueError("missing PDF signature")
        stream.seek(0)
        while chunk := stream.read(1024 * 1024):
            size += len(chunk)
            if size > MAX_BYTES:
                raise ValueError("PDF exceeds local preflight byte cap")
            digest.update(chunk)
    return {"byte_count": size, "sha256": digest.hexdigest()}


def _run(args: list[str], *, version: bool = False) -> str:
    try:
        result = subprocess.run(
            args, capture_output=True, check=False, timeout=90,
            env={**os.environ, "LC_ALL": "C"},
        )
        if result.returncode or (result.stderr and not version):
            raise ValueError("PDF tool failed or reported warnings")
        data = result.stderr + result.stdout if version else result.stdout
        return data.decode("utf-8", errors="strict")
    except (OSError, subprocess.TimeoutExpired, UnicodeError) as exc:
        raise ValueError("PDF tool unavailable, timed out or returned invalid UTF-8") from exc


def _version(tool: str) -> str:
    match = re.search(r"(?m)^" + re.escape(tool) + r" version ([0-9.]+)$",
                      _run([tool, "-v"], version=True))
    if not match:
        raise ValueError("unrecognized PDF tool version")
    return match.group(1)


def preflight(
    path: Path, pages: list[int] | None, *, expected_sha256: str | None = None,
    expected_page_count: int | None = None
) -> dict:
    """Inspect a local carrier, optionally requiring a previously pinned SHA-256."""
    if expected_sha256 is not None and (
        not isinstance(expected_sha256, str)
        or re.fullmatch(r"[0-9a-fA-F]{64}", expected_sha256) is None
    ):
        raise ValueError("expected SHA-256 must contain exactly 64 hexadecimal digits")
    path = path.resolve(strict=True)
    if not path.is_file():
        raise ValueError("input must be a regular PDF")
    complete = pages is None
    if complete:
        if (expected_sha256 is None or type(expected_page_count) is not int
                or not 1 <= expected_page_count <= MAX_COMPLETE_PAGES):
            raise ValueError("complete inspection requires carrier hash and bounded page count")
    elif (not pages or len(pages) > MAX_SAMPLE
            or any(type(p) is not int or p < 1 for p in pages)
            or len(set(pages)) != len(pages)):
        raise ValueError("provide 1–32 unique positive physical page numbers")
    identity = file_identity(path)
    if expected_sha256 is not None and identity["sha256"] != expected_sha256.lower():
        raise ValueError("PDF SHA-256 does not match the expected carrier")
    versions = {name: _version(name) for name in ("pdfinfo", "pdftotext")}
    info = _run(["pdfinfo", str(path)])
    matches = re.findall(r"(?m)^Pages:[ \t]*([1-9][0-9]*)[ \t]*$", info)
    if len(matches) != 1:
        raise ValueError("ambiguous physical PDF page count")
    total = int(matches[0])
    if complete:
        if total != expected_page_count:
            raise ValueError("physical page count does not match the expected carrier")
        pages = list(range(1, total + 1))
    if max(pages) > total:
        raise ValueError("sample exceeds physical PDF page count")
    samples = []
    output_digest = hashlib.sha256()
    output_bytes = 0
    for page in sorted(pages):
        raw = _run(["pdftotext", "-f", str(page), "-l", str(page),
                    "-enc", "UTF-8", "-nopgbrk", str(path), "-"])
        if complete:
            encoded = raw.encode("utf-8")
            output_digest.update(len(encoded).to_bytes(8, "big"))
            output_digest.update(encoded)
            output_bytes += len(encoded)
        samples.append({
            "physical_page": page,
            "extracted_codepoints_including_whitespace": len(raw),
            "non_whitespace_codepoints": sum(not c.isspace() for c in raw),
        })
    if file_identity(path) != identity:
        raise ValueError("PDF changed during inspection")
    receipt = {
        "version": VERSION, "source_free": True, "carrier": identity,
        "tool_versions": versions, "physical_page_count": total,
        "sampled_text_layer": samples,
        "bibliographic_mapping_verified": False,
        "scan_completeness_verified": False,
        "ocr_correctness_verified": False,
        "literary_body_frozen": False,
        "minimum_300k_proved_from_frozen_body": False,
        "rights_independently_verified": False,
        "admitted_for_calibration": False,
        "fantlab_source_edition_match": "unknown",
        "m2_parity_admissible": False,
    }
    if complete:
        nonempty = sum(row["non_whitespace_codepoints"] > 0 for row in samples)
        receipt.update({
            "version": COMPLETE_VERSION,
            "coverage": "ALL_PHYSICAL_PAGES",
            "pages_with_non_whitespace": nonempty,
            "pages_without_non_whitespace": total - nonempty,
            "total_extracted_codepoints": sum(row["extracted_codepoints_including_whitespace"] for row in samples),
            "total_non_whitespace_codepoints": sum(row["non_whitespace_codepoints"] for row in samples),
            "output_utf8_bytes": output_bytes,
            "output_digest_framing": "u64be_utf8_byte_length_then_utf8_bytes_per_ascending_physical_page",
            "output_sha256": output_digest.hexdigest(),
            "extraction_strategy": ("TEXT_LAYER_REQUIRES_COLLATION" if nonempty == total
                                    else "BOUNDED_OCR_EXPERIMENT" if nonempty == 0
                                    else "MIXED_LAYER_REQUIRES_COLLATION"),
        })
    return receipt


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("pdf", type=Path)
    mode = parser.add_mutually_exclusive_group(required=True)
    mode.add_argument("--pages", type=int, nargs="+")
    mode.add_argument("--all-pages", action="store_true", help="Inspect all pinned physical pages")
    parser.add_argument("--expect-page-count", type=int)
    parser.add_argument("--expect-sha256", help="Require the previously pinned PDF SHA-256 before invoking Poppler")
    args = parser.parse_args(argv)
    try:
        receipt = preflight(args.pdf, args.pages, expected_sha256=args.expect_sha256,
                            expected_page_count=args.expect_page_count)
    except (OSError, ValueError):
        parser.exit(2, "PDF preflight failed; no receipt generated.\n")
    print(json.dumps(receipt, ensure_ascii=False, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
