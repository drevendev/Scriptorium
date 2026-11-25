"""Local PDF preflight regressions using synthetic provider responses."""
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch

from scriptorium.local_pdf_preflight import file_identity, preflight


class LocalPdfPreflightTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.path = Path(self.temp.name) / "synthetic.pdf"
        self.path.write_bytes(b"%PDF-1.4\nsynthetic")

    def fake_run(self, args, **kwargs):
        if args[-1] == "-v":
            return f"{args[0]} version 24.02.0\n"
        if args[0] == "pdfinfo":
            return "Pages: 3\n"
        return "private words\n" if args[2] == "1" else " \n"

    def test_source_free_sorted_samples(self):
        with patch("scriptorium.local_pdf_preflight._run", side_effect=self.fake_run):
            report = preflight(self.path, [3, 1])
        self.assertEqual(report["physical_page_count"], 3)
        self.assertEqual(report["carrier"], file_identity(self.path))
        self.assertEqual(report["sampled_text_layer"], [
            {"physical_page": 1, "extracted_codepoints_including_whitespace": 14,
             "non_whitespace_codepoints": 12},
            {"physical_page": 3, "extracted_codepoints_including_whitespace": 2,
             "non_whitespace_codepoints": 0},
        ])
        self.assertNotIn("private words", str(report))
        self.assertNotIn(str(self.path), str(report))
        self.assertFalse(report["literary_body_frozen"])
        self.assertFalse(report["m2_parity_admissible"])

    def test_invalid_sample_fails_closed(self):
        for pages in ([], [0], [True], [1, 1], [4], list(range(1, 34))):
            with self.subTest(pages=pages):
                with patch("scriptorium.local_pdf_preflight._run", side_effect=self.fake_run):
                    with self.assertRaises(ValueError):
                        preflight(self.path, pages)

    def test_invalid_signature(self):
        self.path.write_bytes(b"not a pdf")
        with self.assertRaises(ValueError):
            file_identity(self.path)

    def test_mutated_carrier_rejected(self):
        def mutate(args, **kwargs):
            result = self.fake_run(args, **kwargs)
            if args[0] == "pdftotext" and args[-1] == "-":
                self.path.write_bytes(b"%PDF-1.4\nchanged")
            return result
        with patch("scriptorium.local_pdf_preflight._run", side_effect=mutate):
            with self.assertRaisesRegex(ValueError, "changed"):
                preflight(self.path, [1])

    def test_ambiguous_count_rejected(self):
        def ambiguous(args, **kwargs):
            if args[0] == "pdfinfo" and args[-1] != "-v":
                return "Pages: 3\nPages: 4\n"
            return self.fake_run(args, **kwargs)
        with patch("scriptorium.local_pdf_preflight._run", side_effect=ambiguous):
            with self.assertRaisesRegex(ValueError, "ambiguous"):
                preflight(self.path, [1])
