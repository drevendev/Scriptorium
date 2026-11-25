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
    path: Path, pages: list[int], *, expected_sha256: str | None = None
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
    if (not pages or len(pages) > MAX_SAMPLE
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
    if max(pages) > total:
        raise ValueError("sample exceeds physical PDF page count")
    samples = []
    for page in sorted(pages):
        raw = _run(["pdftotext", "-f", str(page), "-l", str(page),
                    "-enc", "UTF-8", "-nopgbrk", str(path), "-"])
        samples.append({
            "physical_page": page,
            "extracted_codepoints_including_whitespace": len(raw),
            "non_whitespace_codepoints": sum(not c.isspace() for c in raw),
        })
    if file_identity(path) != identity:
        raise ValueError("PDF changed during inspection")
    return {
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


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("pdf", type=Path)
    parser.add_argument("--pages", type=int, nargs="+", required=True)
    parser.add_argument("--expect-sha256", help="Require the previously pinned PDF SHA-256 before invoking Poppler")
    args = parser.parse_args(argv)
    try:
        receipt = preflight(args.pdf, args.pages, expected_sha256=args.expect_sha256)
    except (OSError, ValueError):
        parser.exit(2, "PDF preflight failed; no receipt generated.\n")
    print(json.dumps(receipt, ensure_ascii=False, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
