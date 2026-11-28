"""Private region-matched OCR evaluation for the pinned 1916 Petersburg scan."""
from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
import re
import subprocess
import tempfile

from . import petersburg_ocr_sample as baseline
from . import petersburg_ocr_models as models
from .petersburg_ocr_contract import CANDIDATE_ID, SCAN_IDENTITY

# Poppler's grayscale P5 output, not a general-purpose image parser.
HEADER = re.compile(rb"P5\n([1-9][0-9]{0,4}) ([1-9][0-9]{0,4})\n255\n")
MAX_PAGE_PIXELS = 30_000_000
MAX_CROP_PIXELS = 5_000_000
MAX_REGIONS = 32
MODES = {"TITLE_CONTROL": 6, "BODY_LINE": 7, "BODY_BLOCK": 6}
FIELDS = {"physical_page", "box", "scope", "page_sha256", "crop_sha256", "transcription"}


def sha(raw: bytes) -> str:
    return hashlib.sha256(raw).hexdigest()


def crop_pgm(raw: bytes, box: list[int]) -> bytes:
    """Losslessly slice an exact 8-bit Poppler raster using x,y,width,height."""
    header = HEADER.match(raw)
    if not header:
        raise ValueError("unsupported grayscale raster header")
    width, height = map(int, header.groups())
    if width * height > MAX_PAGE_PIXELS or len(raw) - header.end() != width * height:
        raise ValueError("invalid grayscale raster size")
    if not isinstance(box, list) or len(box) != 4 or any(type(n) is not int for n in box):
        raise ValueError("invalid region coordinates")
    x, y, w, h = box
    if min(x, y) < 0 or min(w, h) <= 0 or x + w > width or y + h > height or w * h > MAX_CROP_PIXELS:
        raise ValueError("region outside raster or size limit")
    start = header.end()
    pixels = b"".join(raw[start + row * width + x:start + row * width + x + w]
                      for row in range(y, y + h))
    return f"P5\n{w} {h}\n255\n".encode("ascii") + pixels


def rasterize(pdf: Path, page: int, directory: Path) -> bytes:
    if type(page) is not int or page not in baseline.PAGES:
        raise ValueError("page outside bounded sample")
    prefix = directory / "page"
    baseline.run(["pdftoppm", "-f", str(page), "-l", str(page), "-r", str(baseline.DPI),
                  "-gray", "-singlefile", str(pdf), str(prefix)])
    raster = prefix.with_suffix(".pgm")
    raw = raster.read_bytes()
    raster.unlink()
    return raw


def prepare(pdf: Path, page: int, box: list[int], destination: Path) -> dict:
    """Write one private crop exclusively; return coordinates and hashes, not prose."""
    baseline.verify_carrier(pdf)
    with tempfile.TemporaryDirectory() as temp:
        raw = rasterize(pdf, page, Path(temp))
        cropped = crop_pgm(raw, box)
        with destination.open("xb") as stream:
            stream.write(cropped)
    return {"physical_page": page, "box": box, "page_sha256": sha(raw),
            "crop_sha256": sha(cropped), "dpi": baseline.DPI}


def validate_references(refs: list[dict]) -> list[dict]:
    if not isinstance(refs, list) or not 1 <= len(refs) <= MAX_REGIONS:
        raise ValueError("invalid region reference collection")
    seen = set()
    for ref in refs:
        if not isinstance(ref, dict) or set(ref) != FIELDS:
            raise ValueError("invalid region reference fields")
        page, box, scope = ref["physical_page"], ref["box"], ref["scope"]
        if type(page) is not int or page not in baseline.PAGES:
            raise ValueError("page outside bounded sample")
        if not isinstance(scope, str) or scope not in MODES or (page == 1) != (scope == "TITLE_CONTROL"):
            raise ValueError("invalid region scope")
        if not isinstance(box, list) or len(box) != 4 or any(type(n) is not int for n in box):
            raise ValueError("invalid region coordinates")
        if min(box[:2]) < 0 or min(box[2:]) <= 0 or box[2] * box[3] > MAX_CROP_PIXELS:
            raise ValueError("invalid region size")
        key = (page, *box)
        if key in seen:
            raise ValueError("duplicate region")
        seen.add(key)
        for field in ("page_sha256", "crop_sha256"):
            if not isinstance(ref[field], str) or not re.fullmatch("[0-9a-f]{64}", ref[field]):
                raise ValueError("invalid region digest")
        if not isinstance(ref["transcription"], str) or not baseline.canonical(ref["transcription"]):
            raise ValueError("empty or invalid reference")
    return sorted(refs, key=lambda r: (r["physical_page"], *r["box"]))


def compare(pdf: Path, stock_dir: Path, iskra_dir: Path, refs: list[dict]) -> dict:
    ordered = validate_references(refs)
    baseline.verify_carrier(pdf)
    model = models.verify_iskra(iskra_dir / "orus.traineddata")
    stock = baseline.digest(stock_dir / "rus.traineddata")
    tools = {name: baseline.version(name, flag) for name, flag in
             (("pdfinfo", "-v"), ("pdftoppm", "-v"), ("tesseract", "--version"))}
    rows = []
    with tempfile.TemporaryDirectory() as temp:
        directory = Path(temp)
        raw, last_page = b"", None
        # Validate every region before invoking either model.
        for index, ref in enumerate(ordered):
            page = ref["physical_page"]
            if page != last_page:
                raw = rasterize(pdf, page, directory)
                last_page = page
            if sha(raw) != ref["page_sha256"]:
                raise ValueError("reference page identity mismatch")
            crop = crop_pgm(raw, ref["box"])
            if sha(crop) != ref["crop_sha256"]:
                raise ValueError("reference crop identity mismatch")
            (directory / f"crop-{index}.pgm").write_bytes(crop)
        for index, ref in enumerate(ordered):
            path = directory / f"crop-{index}.pgm"
            psm = MODES[ref["scope"]]
            variants = []
            for language, data in (("rus", stock_dir), ("orus", iskra_dir)):
                output = baseline.run(["tesseract", str(path), "stdout", "--tessdata-dir",
                                       str(data), "-l", language, "--oem", "1", "--psm", str(psm)])
                hypothesis = baseline.canonical(output.decode("utf-8"))
                variants.append({"language": language, "canonical_codepoints": len(hypothesis),
                                 "output_sha256": sha(output), "glyph_counts": models.glyph_counts(hypothesis),
                                 "reference_errors": models.aligned_reference(ref["transcription"], hypothesis)})
            rows.append({k: ref[k] for k in ("physical_page", "box", "scope", "page_sha256", "crop_sha256")}
                        | {"psm": psm, "reference_status": "CALLER_SUPPLIED_NOT_INDEPENDENTLY_VERIFIED",
                           "variants": variants})
            path.unlink()
    # Region rows are intentionally not aggregated: overlapping crops are possible.
    return {"schema": "scriptorium-petersburg-ocr-region-comparison-v1",
            "candidate_id": CANDIDATE_ID, "carrier": SCAN_IDENTITY,
            "settings": {"dpi": baseline.DPI, "grayscale": True, "raster_format": "P5_PGM",
                         "crop_coordinates": "ZERO_BASED_X_Y_WIDTH_HEIGHT_PIXELS",
                         "oem": 1, "comparison": "NFC_WHITESPACE_COLLAPSE_CASE_ORTHOGRAPHY_PUNCTUATION_PRESERVED",
                         "glyph_alignment": "MINIMUM_EDIT_DIAGONAL_DELETE_INSERT_TIES"},
            "models": {"rus": {"sha256": stock}, "orus": model}, "tools": tools, "regions": rows,
            "source_free": True, "accuracy_status": "UNVERIFIED",
            "whole_volume_ocr_authorized_by_sample": False, "literary_body_frozen": False,
            "minimum_300k_proved_from_frozen_body": False, "admitted_for_calibration": False,
            "fantlab_source_edition_match": "unknown", "m2_parity_admissible": False}


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("pdf", type=Path)
    commands = parser.add_subparsers(dest="command", required=True)
    prep = commands.add_parser("prepare")
    prep.add_argument("--page", required=True, type=int)
    prep.add_argument("--box", required=True, type=int, nargs=4)
    prep.add_argument("--private-crop", required=True, type=Path)
    evaluate = commands.add_parser("compare")
    evaluate.add_argument("--stock-tessdata", required=True, type=Path)
    evaluate.add_argument("--iskra-tessdata", required=True, type=Path)
    evaluate.add_argument("--private-references", required=True, type=Path)
    args = parser.parse_args()
    try:
        if args.command == "prepare":
            receipt = prepare(args.pdf, args.page, args.box, args.private_crop)
        else:
            refs = json.loads(args.private_references.read_text(encoding="utf-8"))
            receipt = compare(args.pdf, args.stock_tessdata, args.iskra_tessdata, refs)
    except (OSError, ValueError, subprocess.SubprocessError):
        parser.exit(1, "Region OCR refused: carrier, crop, reference, model or tool validation failed\n")
    print(json.dumps(receipt, sort_keys=True, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
