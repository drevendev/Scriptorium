import json
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch

from scriptorium import petersburg_ocr_regions as regions


PAGE = b"P5\n4 3\n255\n" + bytes(range(12))
BOX = [1, 1, 2, 2]
CROP = b"P5\n2 2\n255\n" + bytes([5, 6, 9, 10])


def reference():
    return {"physical_page": 21, "box": BOX.copy(), "scope": "BODY_LINE",
            "page_sha256": regions.sha(PAGE), "crop_sha256": regions.sha(CROP),
            "transcription": "ѣ і"}


class OCRRegionTests(unittest.TestCase):
    def test_exact_pixels_and_binary_whitespace(self):
        self.assertEqual(regions.crop_pgm(PAGE, BOX), CROP)
        self.assertEqual(regions.crop_pgm(PAGE, [0, 0, 4, 3]), PAGE)
        for bad in (PAGE[:-1], PAGE + b"x", PAGE.replace(b"255", b"256"), b""):
            with self.assertRaises(ValueError):
                regions.crop_pgm(bad, BOX)
        for box in ([3, 1, 2, 2], [-1, 0, 1, 1], [0, 0, 0, 1], [True, 0, 1, 1]):
            with self.assertRaises(ValueError):
                regions.crop_pgm(PAGE, box)

    def test_private_preparation_is_exclusive_and_hash_bound(self):
        with tempfile.TemporaryDirectory() as temp:
            dest = Path(temp) / "crop.pgm"
            with patch.object(regions.baseline, "verify_carrier"), patch.object(regions, "rasterize", return_value=PAGE):
                receipt = regions.prepare(Path("private.pdf"), 21, BOX, dest)
                self.assertEqual(dest.read_bytes(), CROP)
                self.assertEqual(receipt["crop_sha256"], regions.sha(CROP))
                self.assertEqual(receipt["page_sha256"], regions.sha(PAGE))
                with self.assertRaises(FileExistsError):
                    regions.prepare(Path("private.pdf"), 21, BOX, dest)

    def test_reject_wrong_scopes_and_duplicate_references(self):
        for changes in ({"physical_page": 1}, {"physical_page": 23}, {"scope": "TITLE_CONTROL"},
                        {"scope": "unknown"}, {"transcription": " "}, {"crop_sha256": "bad"},
                        {"box": [0, 0, 1, False]}, {"extra": "secret"}):
            with self.assertRaises(ValueError):
                regions.validate_references([reference() | changes])
        for refs in ([], [reference(), reference()], {}, None):
            with self.assertRaises(ValueError):
                regions.validate_references(refs)

    def test_identical_crop_and_segmentation_for_both_models(self):
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            (root / "rus.traineddata").write_bytes(b"stock")
            calls = []
            def fake_run(args):
                self.assertEqual(Path(args[1]).read_bytes(), CROP)
                calls.append(args)
                return ("ѣ і" if "orus" in args else "е и СЕКРЕТ").encode()
            with patch.object(regions.baseline, "verify_carrier"), patch.object(regions.models, "verify_iskra", return_value={}), patch.object(regions.baseline, "version", return_value={}), patch.object(regions, "rasterize", return_value=PAGE), patch.object(regions.baseline, "run", side_effect=fake_run):
                receipt = regions.compare(root / "carrier.pdf", root, root, [reference()])
                self.assertEqual(len(calls), 2)
                self.assertEqual(calls[0][1], calls[1][1])
                self.assertEqual(calls[0][-4:], calls[1][-4:])
                self.assertEqual(calls[0][-1], "7")
                self.assertEqual(receipt["regions"][0]["variants"][1]["reference_errors"]["character_edits"], 0)
                self.assertEqual(receipt["regions"][0]["variants"][0]["reference_errors"]["matched_glyph_counts"]["ѣ"], 0)
                self.assertEqual(receipt["accuracy_status"], "UNVERIFIED")
                self.assertFalse(receipt["m2_parity_admissible"])
                self.assertNotIn("СЕКРЕТ", json.dumps(receipt, ensure_ascii=False))
                self.assertNotIn("transcription", json.dumps(receipt))
                calls.clear()
                for field in ("page_sha256", "crop_sha256"):
                    with self.assertRaises(ValueError):
                        regions.compare(root / "carrier.pdf", root, root, [reference() | {field: "0" * 64}])
                self.assertEqual(calls, [])
