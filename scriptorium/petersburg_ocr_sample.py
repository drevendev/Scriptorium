"""Bounded, source-free OCR comparison; never promotes the v1 body contract."""
from __future__ import annotations

import argparse
import hashlib
import json
import os
from pathlib import Path
import re
import shutil
import subprocess
import tempfile
import unicodedata

from .petersburg_ocr_contract import SCAN_IDENTITY, SOURCE_PDF_PAGE_COUNT, CANDIDATE_ID

PAGES = (1, 21, 22, 160, 320, 480, 600)
MODES = (3, 6)
DPI = 300


def digest(path: Path) -> str:
    with path.open("rb") as stream:
        return hashlib.file_digest(stream, "sha256").hexdigest()


def canonical(text: str) -> str:
    # Layout whitespace only; preserve historical spelling, punctuation and case.
    return " ".join(unicodedata.normalize("NFC", text).split())


def distance(a, b) -> int:
    if len(b) > len(a):
        a, b = b, a
    row = list(range(len(b) + 1))
    for i, x in enumerate(a, 1):
        nxt = [i]
        for j, y in enumerate(b, 1):
            nxt.append(min(row[j] + 1, nxt[-1] + 1, row[j - 1] + (x != y)))
        row = nxt
    return row[-1]


def errors(reference: str, hypothesis: str) -> dict:
    ref, hyp = canonical(reference), canonical(hypothesis)
    if not ref:
        raise ValueError("reference must contain non-whitespace characters")
    return {
        "reference_codepoints": len(ref),
        "character_edits": distance(ref, hyp),
        "reference_whitespace_tokens": len(ref.split()),
        "word_edits": distance(ref.split(), hyp.split()),
    }


def run(argv: list[str]) -> bytes:
    # Never include subprocess output/arguments in errors: OCR may contain prose.
    try:
        result = subprocess.run(argv, capture_output=True, check=False, timeout=120,
                                env={**os.environ, "LC_ALL": "C", "OMP_THREAD_LIMIT": "1"})
    except (OSError, subprocess.TimeoutExpired):
        raise ValueError("OCR tool invocation failed") from None
    if result.returncode:
        raise ValueError("OCR tool returned nonzero exit status")
    return result.stdout


def version(tool: str, flag: str) -> dict:
    executable = shutil.which(tool)
    if not executable:
        raise ValueError("required tool unavailable")
    # Poppler reports its version on stderr; no source input here.
    proc = subprocess.run([executable, flag], capture_output=True, check=True, timeout=10)
    first = (proc.stdout or proc.stderr).decode("utf-8").splitlines()[0]
    return {"version": first, "executable_sha256": digest(Path(executable))}


def verify_carrier(pdf: Path) -> None:
    if pdf.stat().st_size != SCAN_IDENTITY["byte_count"] or digest(pdf) != SCAN_IDENTITY["sha256"]:
        raise ValueError("carrier identity mismatch")
    info = run(["pdfinfo", str(pdf)]).decode("utf-8")
    match = re.search(r"^Pages:\s+(\d+)\s*$", info, re.M)
    if not match or int(match[1]) != SOURCE_PDF_PAGE_COUNT:
        raise ValueError("carrier physical page count mismatch")


def sample(pdf: Path, tessdata: Path, references: dict | None = None) -> dict:
    verify_carrier(pdf)
    model = tessdata / "rus.traineddata"
    tools = {"pdfinfo": version("pdfinfo", "-v"),
             "pdftoppm": version("pdftoppm", "-v"),
             "tesseract": version("tesseract", "--version"),
             "rus_traineddata_sha256": digest(model)}
    references = {} if references is None else references
    if not isinstance(references, dict) or set(references) - {str(p) for p in PAGES}:
        raise ValueError("reference page outside bounded sample")
    rows = []
    with tempfile.TemporaryDirectory() as temp:
        for page in PAGES:
            prefix = Path(temp) / "raster"
            run(["pdftoppm", "-f", str(page), "-l", str(page), "-r", str(DPI),
                 "-gray", "-singlefile", "-png", str(pdf), str(prefix)])
            raster = prefix.with_suffix(".png")
            image_sha = digest(raster)
            supplied = references.get(str(page))
            if str(page) in references:
                if (not isinstance(supplied, dict)
                        or set(supplied) != {"raster_sha256", "transcription"}
                        or supplied["raster_sha256"] != image_sha
                        or not isinstance(supplied["transcription"], str)
                        or not canonical(supplied["transcription"])):
                    raise ValueError("reference identity or content mismatch")
            variants, texts = [], []
            for mode in MODES:
                raw = run(["tesseract", str(raster), "stdout", "--tessdata-dir",
                           str(tessdata), "-l", "rus", "--oem", "1", "--psm", str(mode)])
                text = raw.decode("utf-8")
                texts.append(canonical(text))
                variants.append({
                    "psm": mode, "raw_sha256": hashlib.sha256(raw).hexdigest(),
                    "raw_codepoints": len(text), "non_whitespace_codepoints": sum(not c.isspace() for c in text),
                    "historical_letter_count": sum(c in "ѣѢіІѳѲѵѴ" for c in text),
                    "reference_errors": errors(supplied["transcription"], text) if supplied else None,
                })
            rows.append({
                "physical_page": page, "raster_sha256": image_sha,
                "scope": "TITLE_CONTROL" if page == 1 else "UNCLASSIFIED_SAMPLE",
                "reference_status": "CALLER_SUPPLIED_NOT_INDEPENDENTLY_VERIFIED" if supplied else "NOT_RUN",
                "variants": variants,
                "between_mode_character_edits": distance(*texts),
                "between_mode_word_edits": distance(*(x.split() for x in texts)),
            })
            raster.unlink()
    return {
        "schema": "scriptorium-petersburg-ocr-sample-v1", "candidate_id": CANDIDATE_ID,
        "carrier": SCAN_IDENTITY, "physical_page_count": SOURCE_PDF_PAGE_COUNT,
        "settings": {"dpi": DPI, "grayscale": True, "language": "rus", "oem": 1, "psm": list(MODES),
                     "comparison": "NFC_WHITESPACE_COLLAPSE_CASE_ORTHOGRAPHY_PUNCTUATION_PRESERVED"},
        "tools": tools, "pages": rows, "source_free": True,
        "accuracy_status": "UNVERIFIED", "whole_volume_ocr_authorized_by_sample": False,
        "literary_body_frozen": False, "minimum_300k_proved_from_frozen_body": False,
        "admitted_for_calibration": False, "fantlab_source_edition_match": "unknown",
        "m2_parity_admissible": False,
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("pdf", type=Path)
    parser.add_argument("--tessdata", type=Path, required=True)
    parser.add_argument("--private-references", type=Path)
    args = parser.parse_args()
    try:
        refs = json.loads(args.private_references.read_text(encoding="utf-8")) if args.private_references else None
        if args.private_references and not isinstance(refs, dict):
            raise ValueError("invalid reference mapping")
        receipt = sample(args.pdf, args.tessdata, refs)
    except (OSError, ValueError, subprocess.SubprocessError):
        parser.exit(1, "OCR sample refused: carrier, reference, tool or output validation failed\n")
    print(json.dumps(receipt, sort_keys=True, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
