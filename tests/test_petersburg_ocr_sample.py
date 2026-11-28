import json
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch

from scriptorium import petersburg_ocr_sample as ocr


class OCRSampleTests(unittest.TestCase):
    def test_historical_letters_and_whitespace(self):
        self.assertEqual(ocr.errors("Ѣсть\n міръ", "Ѣсть  міръ"),
                         {"reference_codepoints": 9, "character_edits": 0,
                          "reference_whitespace_tokens": 2, "word_edits": 0})
        self.assertEqual(ocr.errors("міръ", "мир")["character_edits"], 2)
        self.assertEqual(ocr.errors("міръ", "")["word_edits"], 1)

    def test_blank_reference_refused(self):
        with self.assertRaises(ValueError):
            ocr.errors(" \n ", "text")

    def test_carrier_drift_refused_before_subprocess(self):
        with tempfile.TemporaryDirectory() as folder:
            pdf = Path(folder) / "fake.pdf"
            pdf.write_bytes(b"not carrier")
            with patch.object(ocr, "run") as command, self.assertRaises(ValueError):
                ocr.verify_carrier(pdf)
            command.assert_not_called()

    def test_source_free_and_reference_scope(self):
        with tempfile.TemporaryDirectory() as folder:
            root = Path(folder)
            (root / "rus.traineddata").write_bytes(b"model")
            def fake_run(args):
                if args[0] == "pdftoppm":
                    Path(args[-1]).with_suffix(".png").write_bytes(b"raster")
                    return b""
                return "СЕКРЕТНЫЙ ТЕКСТЪ".encode()
            with patch.object(ocr, "verify_carrier"), patch.object(ocr, "version", return_value={}), patch.object(ocr, "run", side_effect=fake_run):
                receipt = ocr.sample(root / "carrier.pdf", root)
                self.assertEqual([r["physical_page"] for r in receipt["pages"]], list(ocr.PAGES))
                self.assertTrue(all(r["reference_status"] == "NOT_RUN" for r in receipt["pages"]))
                self.assertTrue(all(r["between_mode_character_edits"] == 0 for r in receipt["pages"]))
                self.assertTrue(all(v["reference_errors"] is None for r in receipt["pages"] for v in r["variants"]))
                self.assertNotIn("СЕКРЕТНЫЙ", json.dumps(receipt, ensure_ascii=False))
                self.assertFalse(receipt["literary_body_frozen"])
                with self.assertRaises(ValueError):
                    ocr.sample(root / "carrier.pdf", root, {"2": {}})
                with self.assertRaises(ValueError):
                    ocr.sample(root / "carrier.pdf", root, {"1": {"raster_sha256": "bad", "transcription": "text"}})
                with self.assertRaises(ValueError):
                    ocr.sample(root / "carrier.pdf", root, {"1": None})
                import hashlib
                refs = {"1": {"raster_sha256": hashlib.sha256(b"raster").hexdigest(),
                               "transcription": "СЕКРЕТНЫЙ ТЕКСТЪ"}}
                row = ocr.sample(root / "carrier.pdf", root, refs)["pages"][0]
                self.assertEqual(row["variants"][0]["reference_errors"]["character_edits"], 0)
                self.assertEqual(row["reference_status"], "CALLER_SUPPLIED_NOT_INDEPENDENTLY_VERIFIED")


if __name__ == "__main__":
    unittest.main()
