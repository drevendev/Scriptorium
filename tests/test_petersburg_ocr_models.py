import hashlib
import json
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch

from scriptorium import petersburg_ocr_models as models


class OCRModelTests(unittest.TestCase):
    def test_aligned_historical_glyphs(self):
        result = models.aligned_reference("ѣ і ѳ ѵ", "ѣ и ѳ")
        self.assertEqual(result["character_edits"], 3)
        self.assertEqual(result["reference_codepoints"], 7)
        self.assertEqual(result["reference_whitespace_tokens"], 4)
        self.assertEqual(result["word_edits"], 2)
        for glyph in "ѣіѳѵ":
            self.assertEqual(result["reference_glyph_counts"][glyph], 1)
        self.assertEqual(result["matched_glyph_counts"]["ѣ"], 1)
        self.assertEqual(result["matched_glyph_counts"]["ѳ"], 1)
        self.assertEqual(result["matched_glyph_counts"]["і"], 0)
        self.assertEqual(result["matched_glyph_counts"]["ѵ"], 0)

    def test_reference_counts_not_occurrence_proxy(self):
        self.assertEqual(models.aligned_reference("а", "ѣа")["matched_glyph_counts"]["ѣ"], 0)
        self.assertEqual(models.aligned_reference("ѣ", "")["character_edits"], 1)
        self.assertEqual(models.aligned_reference("Ѣ\nі", "Ѣ і")["character_edits"], 0)
        with self.assertRaises(ValueError):
            models.aligned_reference(" ", "ѣ")

    def test_pinned_model_refuses_size_and_blob_drift(self):
        with tempfile.TemporaryDirectory() as temp:
            model = Path(temp) / "orus.traineddata"
            model.write_bytes(b"abc")
            with self.assertRaises(ValueError):
                models.verify_iskra(model)
            with patch.object(models, "ISKRA_SIZE", 3):
                with self.assertRaises(ValueError):
                    models.verify_iskra(model)
                blob = hashlib.sha1(b"blob 3\0abc").hexdigest()
                with patch.object(models, "ISKRA_BLOB", blob):
                    self.assertEqual(models.verify_iskra(model)["sha256"], hashlib.sha256(b"abc").hexdigest())

    def test_same_raster_and_settings_no_prose_or_false_accuracy(self):
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            (root / "rus.traineddata").write_bytes(b"stock")
            calls = []

            def fake_run(args):
                if args[0] == "pdftoppm":
                    Path(args[-1]).with_suffix(".png").write_bytes(b"raster")
                    return b""
                calls.append(args)
                return ("СЕКРЕТЪ ѣ" if "orus" in args else "СЕКРЕТ е").encode()

            with patch.object(models.baseline, "verify_carrier"), patch.object(models, "verify_iskra", return_value={}), patch.object(models.baseline, "version", return_value={}), patch.object(models.baseline, "run", side_effect=fake_run):
                receipt = models.compare(root / "carrier.pdf", root, root)
                self.assertEqual(len(calls), 2 * len(models.baseline.PAGES))
                for left, right in zip(calls[::2], calls[1::2]):
                    self.assertEqual(left[:3], right[:3])
                    self.assertEqual(left[-4:], right[-4:])
                    self.assertEqual((left[6], right[6]), ("rus", "orus"))
                self.assertEqual(receipt["accuracy_status"], "NOT_RUN")
                self.assertFalse(receipt["literary_body_frozen"])
                self.assertNotIn("СЕКРЕТ", json.dumps(receipt, ensure_ascii=False))
                self.assertTrue(all(v["reference_errors"] is None for r in receipt["pages"] for v in r["variants"]))
                refs = {"1": {"raster_sha256": "wrong", "transcription": "ѣ"}}
                with self.assertRaises(ValueError):
                    models.compare(root / "carrier.pdf", root, root, refs)
                refs["1"]["raster_sha256"] = hashlib.sha256(b"raster").hexdigest()
                checked = models.compare(root / "carrier.pdf", root, root, refs)
                self.assertEqual(checked["accuracy_status"], "UNVERIFIED")
                self.assertEqual(checked["pages"][0]["variants"][1]["reference_errors"]["matched_glyph_counts"]["ѣ"], 1)


if __name__ == "__main__":
    unittest.main()
