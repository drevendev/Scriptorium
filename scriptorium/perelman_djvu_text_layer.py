"""Inspect the frozen Perelman 1913 DjVu hidden-text layer without retaining prose.

The exact Commons DjVu is retrieved transiently and verified against the already frozen
carrier identity before ``djvutxt`` is executed. Durable output contains only counts,
cryptographic digests, page-presence summaries, tool/package identity and closed-gate
claims. Hidden text itself is never written by this module.
"""

from __future__ import annotations

import argparse
from hashlib import sha256
import json
from pathlib import Path
import subprocess
from tempfile import TemporaryDirectory
from typing import Mapping, Sequence

from .perelman_djvu_identity import (
    CANDIDATE_ID,
    EXPECTED_PROVIDER_BYTE_COUNT,
    EXPECTED_PROVIDER_PAGE_COUNT,
    EXPECTED_PROVIDER_SHA1,
    DJVU_URL,
    _remote_chunks,
    compute_identity,
    crosscheck_provider_identity,
)
from .text import NORMALIZATION_PROFILE, normalize_text

DIAGNOSTIC_VERSION = "scriptorium-perelman-1913-djvu-hidden-text-v1"
EXPECTED_CARRIER_SHA256 = "f1db2166ae0cb5d420aad445f00d90cb09ac0b97e19fc8ece16d9b8ecf9e2462"
TOOL_NAME = "djvutxt"
TOOL_PACKAGE = "djvulibre-bin"
EXPECTED_PACKAGE_VERSION = "3.5.28-2ubuntu0.24.04.2"


def _digest_json(value: object) -> str:
    payload = json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":")).encode("utf-8")
    return sha256(payload).hexdigest()


def _text_summary(payload: bytes) -> dict[str, object]:
    text = payload.decode("utf-8", errors="strict")
    normalized = normalize_text(text)
    return {
        "utf8_byte_count": len(payload),
        "character_count": len(text),
        "sha256": sha256(payload).hexdigest(),
        "normalized_profile": NORMALIZATION_PROFILE,
        "normalized_character_count": len(normalized),
        "normalized_sha256": sha256(normalized.encode("utf-8")).hexdigest(),
    }


def build_diagnostic(
    all_pages_output: bytes,
    page_outputs: Sequence[bytes],
    *,
    package_version: str,
) -> dict[str, object]:
    if len(page_outputs) != EXPECTED_PROVIDER_PAGE_COUNT:
        raise ValueError("Perelman DjVu page-output count does not match frozen carrier")
    if not package_version:
        raise ValueError("DjVuLibre package version is required")

    page_utf8_byte_counts = [len(payload) for payload in page_outputs]
    pages_with_text = [index + 1 for index, payload in enumerate(page_outputs) if payload]
    pages_without_text = [index + 1 for index, payload in enumerate(page_outputs) if not payload]
    summary = _text_summary(all_pages_output)

    diagnostic = {
        "diagnostic_version": DIAGNOSTIC_VERSION,
        "candidate_id": CANDIDATE_ID,
        "carrier": {
            "format": "DjVu",
            "exact_original_url": DJVU_URL,
            "byte_count": EXPECTED_PROVIDER_BYTE_COUNT,
            "sha1": EXPECTED_PROVIDER_SHA1,
            "sha256": EXPECTED_CARRIER_SHA256,
            "page_count": EXPECTED_PROVIDER_PAGE_COUNT,
            "identity_reverified_before_extraction": True,
        },
        "extractor": {
            "tool": TOOL_NAME,
            "package": TOOL_PACKAGE,
            "package_version": package_version,
            "mode": "hidden_text_utf8",
        },
        "hidden_text": {
            "inspected": True,
            "present": bool(all_pages_output),
            **summary,
            "pages_with_nonempty_output": len(pages_with_text),
            "pages_without_output": pages_without_text,
            "first_page_with_output": pages_with_text[0] if pages_with_text else None,
            "last_page_with_output": pages_with_text[-1] if pages_with_text else None,
            "page_utf8_byte_count_vector_sha256": _digest_json(page_utf8_byte_counts),
        },
        "source_text_included": False,
        "binary_bytes_committed": False,
        "page_equivalence_to_pdf_verified": False,
        "literary_page_selection_frozen": False,
        "canonical_ocr_extraction_carrier_changed": False,
        "literary_body_count_and_digests_frozen": False,
        "minimum_300k_proved_from_frozen_body": False,
        "admitted_for_calibration": False,
        "fantlab_source_edition_match": "unknown",
        "diagnostic_ready": False,
        "m2_parity_admissible": False,
    }
    validate_diagnostic(diagnostic)
    return diagnostic


def validate_diagnostic(diagnostic: Mapping[str, object]) -> None:
    required = {
        "diagnostic_version",
        "candidate_id",
        "carrier",
        "extractor",
        "hidden_text",
        "source_text_included",
        "binary_bytes_committed",
        "page_equivalence_to_pdf_verified",
        "literary_page_selection_frozen",
        "canonical_ocr_extraction_carrier_changed",
        "literary_body_count_and_digests_frozen",
        "minimum_300k_proved_from_frozen_body",
        "admitted_for_calibration",
        "fantlab_source_edition_match",
        "diagnostic_ready",
        "m2_parity_admissible",
    }
    if set(diagnostic) != required:
        raise ValueError("Perelman DjVu hidden-text diagnostic shape drift")
    if diagnostic.get("diagnostic_version") != DIAGNOSTIC_VERSION or diagnostic.get("candidate_id") != CANDIDATE_ID:
        raise ValueError("Perelman DjVu hidden-text diagnostic identity drift")

    carrier = diagnostic.get("carrier")
    if not isinstance(carrier, Mapping) or set(carrier) != {
        "format", "exact_original_url", "byte_count", "sha1", "sha256", "page_count", "identity_reverified_before_extraction"
    }:
        raise ValueError("Perelman DjVu hidden-text carrier shape drift")
    if carrier.get("format") != "DjVu" or carrier.get("exact_original_url") != DJVU_URL:
        raise ValueError("Perelman DjVu hidden-text carrier locator drift")
    if carrier.get("byte_count") != EXPECTED_PROVIDER_BYTE_COUNT or carrier.get("sha1") != EXPECTED_PROVIDER_SHA1:
        raise ValueError("Perelman DjVu hidden-text carrier provider identity drift")
    if carrier.get("sha256") != EXPECTED_CARRIER_SHA256 or carrier.get("page_count") != EXPECTED_PROVIDER_PAGE_COUNT:
        raise ValueError("Perelman DjVu hidden-text frozen carrier identity drift")
    if carrier.get("identity_reverified_before_extraction") is not True:
        raise ValueError("Perelman DjVu carrier must be reverified before hidden-text extraction")

    extractor = diagnostic.get("extractor")
    if not isinstance(extractor, Mapping) or set(extractor) != {"tool", "package", "package_version", "mode"}:
        raise ValueError("Perelman DjVu hidden-text extractor shape drift")
    if extractor.get("tool") != TOOL_NAME or extractor.get("package") != TOOL_PACKAGE or extractor.get("mode") != "hidden_text_utf8":
        raise ValueError("Perelman DjVu hidden-text extractor identity drift")
    if extractor.get("package_version") != EXPECTED_PACKAGE_VERSION:
        raise ValueError("Perelman DjVu hidden-text package version drift")

    hidden = diagnostic.get("hidden_text")
    if not isinstance(hidden, Mapping) or set(hidden) != {
        "inspected", "present", "utf8_byte_count", "character_count", "sha256", "normalized_profile",
        "normalized_character_count", "normalized_sha256", "pages_with_nonempty_output", "pages_without_output",
        "first_page_with_output", "last_page_with_output", "page_utf8_byte_count_vector_sha256"
    }:
        raise ValueError("Perelman DjVu hidden-text summary shape drift")
    if hidden.get("inspected") is not True:
        raise ValueError("Perelman DjVu hidden-text inspection must be explicit")
    if hidden.get("normalized_profile") != NORMALIZATION_PROFILE:
        raise ValueError("Perelman DjVu hidden-text normalization profile drift")
    for key in ("utf8_byte_count", "character_count", "normalized_character_count", "pages_with_nonempty_output"):
        value = hidden.get(key)
        if not isinstance(value, int) or isinstance(value, bool) or value < 0:
            raise ValueError(f"Perelman DjVu hidden-text {key} is invalid")
    for key in ("sha256", "normalized_sha256", "page_utf8_byte_count_vector_sha256"):
        value = hidden.get(key)
        if not isinstance(value, str) or len(value) != 64:
            raise ValueError(f"Perelman DjVu hidden-text {key} is malformed")
        try:
            int(value, 16)
        except ValueError as exc:
            raise ValueError(f"Perelman DjVu hidden-text {key} is not hexadecimal") from exc
    pages_without = hidden.get("pages_without_output")
    if not isinstance(pages_without, list) or any(
        not isinstance(value, int) or isinstance(value, bool) or not 1 <= value <= EXPECTED_PROVIDER_PAGE_COUNT
        for value in pages_without
    ):
        raise ValueError("Perelman DjVu pages_without_output is invalid")
    if len(set(pages_without)) != len(pages_without) or pages_without != sorted(pages_without):
        raise ValueError("Perelman DjVu pages_without_output must be sorted and unique")
    with_text = hidden["pages_with_nonempty_output"]
    if with_text + len(pages_without) != EXPECTED_PROVIDER_PAGE_COUNT:
        raise ValueError("Perelman DjVu hidden-text page accounting drift")
    present = hidden.get("present")
    if not isinstance(present, bool):
        raise ValueError("Perelman DjVu hidden-text presence flag is invalid")
    if present != bool(hidden["utf8_byte_count"]):
        raise ValueError("Perelman DjVu hidden-text presence/count contradiction")
    if bool(with_text) != present:
        raise ValueError("Perelman DjVu page-presence summary contradicts full hidden-text output")
    first_page = hidden.get("first_page_with_output")
    last_page = hidden.get("last_page_with_output")
    if present:
        if not isinstance(first_page, int) or not isinstance(last_page, int) or not 1 <= first_page <= last_page <= EXPECTED_PROVIDER_PAGE_COUNT:
            raise ValueError("Perelman DjVu hidden-text first/last page summary is invalid")
    elif first_page is not None or last_page is not None:
        raise ValueError("Perelman DjVu empty hidden-text layer cannot name first/last pages")

    false_gates = (
        "source_text_included",
        "binary_bytes_committed",
        "page_equivalence_to_pdf_verified",
        "literary_page_selection_frozen",
        "canonical_ocr_extraction_carrier_changed",
        "literary_body_count_and_digests_frozen",
        "minimum_300k_proved_from_frozen_body",
        "admitted_for_calibration",
        "diagnostic_ready",
        "m2_parity_admissible",
    )
    if any(diagnostic.get(key) is not False for key in false_gates):
        raise ValueError("Perelman DjVu hidden-text diagnostic advanced a forbidden corpus/parity gate")
    if diagnostic.get("fantlab_source_edition_match") != "unknown":
        raise ValueError("Perelman DjVu hidden-text diagnostic advanced FantLab source identity")


def _run_djvutxt(path: Path, *, page: int | None = None) -> bytes:
    command = [TOOL_NAME]
    if page is not None:
        command.append(f"--page={page}")
    command.append(str(path))
    result = subprocess.run(command, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    return result.stdout


def _download_verified_djvu(path: Path) -> None:
    chunks: list[bytes] = []
    with path.open("wb") as handle:
        for chunk in _remote_chunks():
            handle.write(chunk)
            chunks.append(chunk)
    identity = compute_identity(chunks)
    crosscheck_provider_identity(identity)
    if identity.get("sha256") != EXPECTED_CARRIER_SHA256:
        raise ValueError("Perelman DjVu SHA-256 no longer matches frozen carrier")


def probe_remote(*, package_version: str) -> dict[str, object]:
    with TemporaryDirectory(prefix="scriptorium-perelman-djvu-") as directory:
        path = Path(directory) / "carrier.djvu"
        _download_verified_djvu(path)
        all_pages_output = _run_djvutxt(path)
        page_outputs = [_run_djvutxt(path, page=page) for page in range(1, EXPECTED_PROVIDER_PAGE_COUNT + 1)]
        return build_diagnostic(all_pages_output, page_outputs, package_version=package_version)


def _load_object(path: Path) -> dict[str, object]:
    value = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(value, dict):
        raise ValueError(f"{path} must contain a JSON object")
    return value


def _write_object(path: Path, value: Mapping[str, object]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def main(argv: Sequence[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    subparsers = parser.add_subparsers(dest="command", required=True)
    probe = subparsers.add_parser("probe")
    probe.add_argument("--package-version", required=True)
    probe.add_argument("--output", type=Path, required=True)
    verify = subparsers.add_parser("verify")
    verify.add_argument("--package-version", required=True)
    verify.add_argument("--receipt", type=Path, required=True)
    args = parser.parse_args(argv)

    observed = probe_remote(package_version=args.package_version)
    if args.command == "probe":
        _write_object(args.output, observed)
        print(json.dumps(observed, ensure_ascii=False, sort_keys=True))
        return 0

    expected = _load_object(args.receipt)
    validate_diagnostic(expected)
    if observed != expected:
        raise ValueError("Perelman DjVu hidden-text diagnostic no longer matches frozen receipt")
    print(json.dumps({"verified": True, "diagnostic_sha256": _digest_json(observed)}, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
