"""Matched-model OCR diagnostic for the pinned Petersburg carrier; no body promotion."""
from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
import subprocess
import tempfile

from . import petersburg_ocr_sample as baseline
from .petersburg_ocr_contract import SCAN_IDENTITY, SOURCE_PDF_PAGE_COUNT, CANDIDATE_ID

ISKRA_REV = "02f34dc42af9f78d022848e83e103b182c9af134"
ISKRA_BLOB = "4c5f96a3cfde2d74e6a5c414611d14b16e965ab1"
ISKRA_SIZE = 11786045
GLYPHS = "ѣѢіІѳѲѵѴ"
MODE = 6


def verify_iskra(model: Path) -> dict:
    if model.stat().st_size != ISKRA_SIZE:
        raise ValueError("Iskra model size mismatch")
    raw = model.read_bytes()
    if hashlib.sha1(b"blob " + str(len(raw)).encode("ascii") + b"\0" + raw).hexdigest() != ISKRA_BLOB:
        raise ValueError("Iskra model Git blob mismatch")
    return {"revision": ISKRA_REV, "git_blob": ISKRA_BLOB,
            "byte_count": len(raw), "sha256": hashlib.sha256(raw).hexdigest(),
            "license": "Apache-2.0"}


def glyph_counts(text: str) -> dict:
    return {glyph: text.count(glyph) for glyph in GLYPHS}


def aligned_reference(reference: str, hypothesis: str) -> dict:
    """Minimum edit alignment with diagonal, deletion, insertion tie priority."""
    ref, hyp = baseline.canonical(reference), baseline.canonical(hypothesis)
    if not ref:
        raise ValueError("empty reference")
    # Bounded full-page diagnostic, not a general book alignment engine.
    if (len(ref) + 1) * (len(hyp) + 1) > 25000000:
        raise ValueError("reference alignment exceeds bounded page size")
    width = len(hyp) + 1
    trace = bytearray((len(ref) + 1) * width)
    trace[1:width] = b"\x02" * len(hyp)
    row = list(range(width))
    for i, x in enumerate(ref, 1):
        nxt = [i]
        trace[i * width] = 1
        for j, y in enumerate(hyp, 1):
            diagonal, deletion, insertion = row[j - 1] + (x != y), row[j] + 1, nxt[-1] + 1
            cost = min(diagonal, deletion, insertion)
            nxt.append(cost)
            trace[i * width + j] = 0 if cost == diagonal else 1 if cost == deletion else 2
        row = nxt
    matches = dict.fromkeys(GLYPHS, 0)
    i, j = len(ref), len(hyp)
    while i or j:
        op = trace[i * width + j]
        if op == 0:
            if ref[i - 1] == hyp[j - 1] and ref[i - 1] in matches:
                matches[ref[i - 1]] += 1
            i -= 1
            j -= 1
        elif op == 1:
            i -= 1
        else:
            j -= 1
    return {"reference_codepoints": len(ref), "character_edits": row[-1],
            "reference_whitespace_tokens": len(ref.split()),
            "word_edits": baseline.distance(ref.split(), hyp.split()),
            "reference_glyph_counts": glyph_counts(ref),
            "matched_glyph_counts": matches}


def compare(pdf: Path, stock_dir: Path, iskra_dir: Path, references: dict | None = None) -> dict:
    baseline.verify_carrier(pdf)
    model = verify_iskra(iskra_dir / "orus.traineddata")
    stock = baseline.digest(stock_dir / "rus.traineddata")
    refs = {} if references is None else references
    if not isinstance(refs, dict) or set(refs) - {str(p) for p in baseline.PAGES}:
        raise ValueError("reference outside bounded sample")
    tools = {name: baseline.version(name, flag) for name, flag in
             (("pdfinfo", "-v"), ("pdftoppm", "-v"), ("tesseract", "--version"))}
    rows = []
    with tempfile.TemporaryDirectory() as temp:
        for page in baseline.PAGES:
            prefix = Path(temp) / "page"
            baseline.run(["pdftoppm", "-f", str(page), "-l", str(page), "-r", str(baseline.DPI),
                          "-gray", "-singlefile", "-png", str(pdf), str(prefix)])
            raster = prefix.with_suffix(".png")
            raster_sha = baseline.digest(raster)
            supplied = refs.get(str(page))
            if str(page) in refs and (
                not isinstance(supplied, dict)
                or set(supplied) != {"raster_sha256", "transcription"}
                or supplied["raster_sha256"] != raster_sha
                or not isinstance(supplied["transcription"], str)
                or not baseline.canonical(supplied["transcription"])
            ):
                raise ValueError("reference identity or content mismatch")
            variants, texts = [], []
            for language, directory in (("rus", stock_dir), ("orus", iskra_dir)):
                raw = baseline.run(["tesseract", str(raster), "stdout", "--tessdata-dir",
                                    str(directory), "-l", language, "--oem", "1", "--psm", str(MODE)])
                text = baseline.canonical(raw.decode("utf-8"))
                texts.append(text)
                variants.append({"language": language, "raw_sha256": hashlib.sha256(raw).hexdigest(),
                                 "canonical_codepoints": len(text), "glyph_counts": glyph_counts(text),
                                 "reference_errors": aligned_reference(supplied["transcription"], text)
                                 if supplied else None})
            rows.append({"physical_page": page, "raster_sha256": raster_sha,
                         "scope": "TITLE_CONTROL" if page == 1 else "UNCLASSIFIED_SAMPLE",
                         "reference_status": "CALLER_SUPPLIED_NOT_INDEPENDENTLY_VERIFIED" if supplied else "NOT_RUN",
                         "variants": variants, "between_model_character_edits": baseline.distance(*texts),
                         "between_model_word_edits": baseline.distance(*(t.split() for t in texts))})
            raster.unlink()
    return {"schema": "scriptorium-petersburg-ocr-model-comparison-v1", "candidate_id": CANDIDATE_ID,
            "carrier": SCAN_IDENTITY, "physical_page_count": SOURCE_PDF_PAGE_COUNT,
            "settings": {"dpi": baseline.DPI, "grayscale": True, "oem": 1, "psm": MODE,
                         "comparison": "NFC_WHITESPACE_COLLAPSE_CASE_ORTHOGRAPHY_PUNCTUATION_PRESERVED",
                         "glyph_alignment": "MINIMUM_EDIT_DIAGONAL_DELETE_INSERT_TIES"},
            "models": {"rus": {"sha256": stock}, "orus": model}, "tools": tools, "pages": rows,
            "source_free": True, "accuracy_status": "UNVERIFIED" if refs else "NOT_RUN",
            "whole_volume_ocr_authorized_by_sample": False, "literary_body_frozen": False,
            "minimum_300k_proved_from_frozen_body": False, "admitted_for_calibration": False,
            "fantlab_source_edition_match": "unknown", "m2_parity_admissible": False}


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("pdf", type=Path)
    parser.add_argument("--stock-tessdata", type=Path, required=True)
    parser.add_argument("--iskra-tessdata", type=Path, required=True)
    parser.add_argument("--private-references", type=Path)
    args = parser.parse_args()
    try:
        refs = json.loads(args.private_references.read_text(encoding="utf-8")) if args.private_references else None
        if args.private_references and not isinstance(refs, dict):
            raise ValueError("invalid reference mapping")
        receipt = compare(args.pdf, args.stock_tessdata, args.iskra_tessdata, refs)
    except (OSError, ValueError, subprocess.SubprocessError):
        parser.exit(1, "OCR model comparison refused: carrier, model, reference, tool or output validation failed\n")
    print(json.dumps(receipt, sort_keys=True, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
