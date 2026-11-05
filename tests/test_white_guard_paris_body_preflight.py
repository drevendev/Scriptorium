"""Source-free positive, negative and privacy tests for Paris Page candidates."""
from __future__ import annotations

from contextlib import redirect_stdout, redirect_stderr
from io import StringIO
from unittest.mock import patch
import unittest

from scriptorium import white_guard_paris_body_preflight as preflight

SENTINEL = "PRIVATE_MANUSCRIPT_NEVER_PRINT"


def fixture():
    bounds = {p: chapter for chapter, (first, last) in enumerate(preflight.EXPECTED_RANGES, 1)
              for p in range(first, last + 1)}
    return tuple({"page_number": p, "chapter": bounds[p], "title": f"Page/{p}",
                  "page_id": p, "revision_id": p + 1000,
                  "revision_timestamp": "2026-01-01T00:00:00Z", "mediawiki_sha1": "a" * 40}
                 for p in range(5, 190))


class ParisBodyPreflightTests(unittest.TestCase):
    def test_boundary_noincludes_are_removed_without_render_claim(self):
        text = '<noinclude><pagequality level="3"/></noinclude>\nПривет, мир!\n<noinclude>footer</noinclude>'
        self.assertEqual(preflight.candidate_page_body(text), ("CANDIDATE_ONLY", "Привет, мир!"))

    def test_refuse_inner_noinclude_markup_and_empty_page(self):
        samples = ["Проза<noinclude>hidden</noinclude>внутри", "{{template}}", "[[Link|text]]",
                   '<section begin="x" />Текст', "<noinclude>header</noinclude>   <noinclude>footer</noinclude>\n",
                   "= Heading =", "<noinclude>\nheader"]
        for source in samples:
            with self.subTest(source=source[:25]):
                self.assertNotEqual(preflight.candidate_page_body(source)[0], "CANDIDATE_ONLY")
        self.assertEqual(preflight.candidate_page_body("a" * (preflight.MAX_PAGE_CHARACTERS + 1))[0], "OVERSIZED_PAGE")

    def test_full_synthetic_185_page_replay_has_no_prose_in_receipt(self):
        rows = fixture()
        payload = {r["title"]: f"Page {r['page_number']} {SENTINEL}" for r in rows}
        result = preflight.build_preflight(loader=lambda: rows, fetcher=lambda ids: payload)
        self.assertEqual(result["page_count"], 185)
        self.assertEqual(result["candidate_page_count"], 185)
        self.assertEqual(result["candidate_chapter_count"], 11)
        self.assertFalse(result["historical_transclusion_proven"])
        self.assertFalse(result["m2_parity_admissible"])
        self.assertEqual(result["provider_replay"], "INJECTED_FIXTURE")
        self.assertNotIn(SENTINEL, str(result))

    def test_partial_page_blocks_chapter_digest_not_other_chapters(self):
        rows = fixture()
        payload = {r["title"]: "простая проза" for r in rows}
        payload["Page/6"] = "{{unsupported}}"
        result = preflight.build_preflight(loader=lambda: rows, fetcher=lambda ids: payload)
        self.assertEqual(result["candidate_page_count"], 184)
        self.assertEqual(result["candidate_chapter_count"], 10)
        self.assertIsNone(result["chapters"][0]["candidate_sha256"])
        self.assertIsNotNone(result["chapters"][1]["candidate_sha256"])

    def test_provider_failure_never_emits_partial_receipt_or_private_data(self):
        rows = fixture()
        with self.assertRaises(ValueError):
            preflight.build_preflight(loader=lambda: rows, fetcher=lambda ids: {})
        out, err = StringIO(), StringIO()
        with patch.object(preflight, "build_preflight", side_effect=RuntimeError(SENTINEL)):
            with redirect_stdout(out), redirect_stderr(err):
                result = preflight.main([])
        self.assertEqual(result, 2)
        self.assertEqual(out.getvalue(), "")
        self.assertNotIn(SENTINEL, err.getvalue())


if __name__ == "__main__":
    unittest.main()
