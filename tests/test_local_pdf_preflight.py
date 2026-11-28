"""Local PDF preflight regressions using synthetic provider responses."""
from contextlib import redirect_stderr, redirect_stdout
from io import StringIO
from pathlib import Path
import hashlib
import tempfile
import unittest
from unittest.mock import patch

from scriptorium.local_pdf_preflight import file_identity, main, preflight


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

    def test_expected_digest_preserves_receipt(self):
        expected = file_identity(self.path)["sha256"]
        with patch("scriptorium.local_pdf_preflight._run", side_effect=self.fake_run):
            unpinned = preflight(self.path, [1])
            pinned = preflight(self.path, [1], expected_sha256=expected.upper())
        self.assertEqual(pinned, unpinned)

    def test_bad_digest_rejected_before_pdf_tools(self):
        for expected in ("0" * 64, "", "g" * 64, "a" * 63, "a" * 64 + "\n", True):
            with self.subTest(expected=expected):
                with patch("scriptorium.local_pdf_preflight._run") as run:
                    with self.assertRaises(ValueError):
                        preflight(self.path, [1], expected_sha256=expected)
                    run.assert_not_called()

    def test_cli_wrong_carrier_emits_no_receipt(self):
        stdout, stderr = StringIO(), StringIO()
        with patch("scriptorium.local_pdf_preflight._run") as run:
            with redirect_stdout(stdout), redirect_stderr(stderr):
                with self.assertRaises(SystemExit) as failure:
                    main([str(self.path), "--pages", "1", "--expect-sha256", "0" * 64])
            run.assert_not_called()
        self.assertEqual(failure.exception.code, 2)
        self.assertEqual(stdout.getvalue(), "")
        self.assertNotIn(str(self.path), stderr.getvalue())

    def test_complete_inventory_and_framed_digest(self):
        expected = file_identity(self.path)["sha256"]
        with patch("scriptorium.local_pdf_preflight._run", side_effect=self.fake_run):
            report = preflight(self.path, None, expected_sha256=expected, expected_page_count=3)
        chunks = [b"private words\n", b" \n", b" \n"]
        digest = hashlib.sha256(b"".join(len(c).to_bytes(8, "big") + c for c in chunks)).hexdigest()
        self.assertEqual(report["output_sha256"], digest)
        self.assertEqual(report["output_utf8_bytes"], 18)
        self.assertEqual(report["total_extracted_codepoints"], 18)
        self.assertEqual(report["total_non_whitespace_codepoints"], 12)
        self.assertEqual(report["pages_with_non_whitespace"], 1)
        self.assertEqual(report["pages_without_non_whitespace"], 2)
        self.assertEqual(report["coverage"], "ALL_PHYSICAL_PAGES")
        self.assertEqual(report["extraction_strategy"], "MIXED_LAYER_REQUIRES_COLLATION")
        self.assertEqual([row["physical_page"] for row in report["sampled_text_layer"]], [1, 2, 3])
        self.assertNotIn("private words", str(report))
        self.assertFalse(report["literary_body_frozen"])
        self.assertFalse(report["m2_parity_admissible"])

    def test_complete_requires_pins_and_refuses_count_drift(self):
        expected = file_identity(self.path)["sha256"]
        for sha, count in [(None, 3), (expected, None), (expected, 0),
                           (expected, True), (expected, 1025), ("0" * 64, 3)]:
            with self.subTest(sha=sha, count=count):
                with patch("scriptorium.local_pdf_preflight._run") as run:
                    with self.assertRaises(ValueError):
                        preflight(self.path, None, expected_sha256=sha, expected_page_count=count)
                    run.assert_not_called()
        with patch("scriptorium.local_pdf_preflight._run", side_effect=self.fake_run) as run:
            with self.assertRaisesRegex(ValueError, "page count"):
                preflight(self.path, None, expected_sha256=expected, expected_page_count=4)
            self.assertFalse(any(call.args[0][0] == "pdftotext" and "-f" in call.args[0]
                                 for call in run.call_args_list))

    def test_complete_refuses_partial_extraction(self):
        expected = file_identity(self.path)["sha256"]
        def fail_middle(args, **kwargs):
            if args[0] == "pdftotext" and "-f" in args and args[2] == "2":
                raise ValueError("tool failure")
            return self.fake_run(args, **kwargs)
        with patch("scriptorium.local_pdf_preflight._run", side_effect=fail_middle):
            with redirect_stdout(StringIO()) as stdout, redirect_stderr(StringIO()):
                with self.assertRaises(SystemExit) as failure:
                    main([str(self.path), "--all-pages", "--expect-page-count", "3",
                          "--expect-sha256", expected])
            self.assertEqual(failure.exception.code, 2)
            self.assertEqual(stdout.getvalue(), "")
