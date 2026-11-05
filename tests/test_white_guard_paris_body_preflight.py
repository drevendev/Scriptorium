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

    def test_wikitext_apostrophe_markup_blocks_page_and_chapter_digest(self):
        for sample in ("Текст ''курсив''.", "'''Жирный'''", "'''''Оба'''''", "''"):
            with self.subTest(sample=sample):
                self.assertEqual(preflight.candidate_page_body(sample)[0], "UNSUPPORTED_PAGE_MARKUP")
        self.assertEqual(preflight.candidate_page_body("rock'n'roll"), ("CANDIDATE_ONLY", "rock'n'roll"))
        rows = fixture()
        payload = {r["title"]: "простая проза" for r in rows}
        payload["Page/6"] = f"{SENTINEL} ''markup''"
        report = preflight.build_preflight(loader=lambda: rows, fetcher=lambda ids: payload)
        self.assertEqual(report["candidate_page_count"], 184)
        self.assertEqual(report["candidate_chapter_count"], 10)
        self.assertEqual(report["pages"][1]["status"], "UNSUPPORTED_PAGE_MARKUP")
        self.assertIsNone(report["pages"][1]["candidate_sha256"])
        self.assertIsNone(report["pages"][1]["candidate_characters_including_spaces"])
        self.assertEqual(report["chapters"][0]["status"], "INCOMPLETE")
        self.assertIsNone(report["chapters"][0]["candidate_sha256"])
        self.assertIsNone(report["chapters"][0]["candidate_characters_including_spaces"])
        self.assertIsNotNone(report["chapters"][1]["candidate_sha256"])
        self.assertNotIn(SENTINEL, str(report))

    def test_line_start_structures_reject_page_and_chapter_digests(self):
        unsupported = ("* bullet", "** nested", "# numbered", "## nested",
                       ": indent", "; term", "----", "-----",
                       "  * bullet", "Проза\n: citation")
        for source in unsupported:
            with self.subTest(source=source):
                self.assertEqual(preflight.candidate_page_body(source)[0], "UNSUPPORTED_PAGE_MARKUP")
        for plain in ("Обычная проза; продолжение.", "— Диалог.", "A #hashtag in prose",
                      "Три дефиса --- внутри текста.", "rock'n'roll"):
            with self.subTest(plain=plain):
                self.assertEqual(preflight.candidate_page_body(plain), ("CANDIDATE_ONLY", plain))
        rows = fixture()
        payload = {r["title"]: "обычная проза" for r in rows}
        payload["Page/6"] = f"{SENTINEL}\n* list item"
        report = preflight.build_preflight(loader=lambda: rows, fetcher=lambda ids: payload)
        self.assertEqual(report["candidate_page_count"], 184)
        self.assertEqual(report["candidate_chapter_count"], 10)
        self.assertEqual(report["pages"][1]["status"], "UNSUPPORTED_PAGE_MARKUP")
        self.assertIsNone(report["pages"][1]["candidate_sha256"])
        self.assertIsNone(report["pages"][1]["candidate_characters_including_spaces"])
        self.assertEqual(report["chapters"][0]["status"], "INCOMPLETE")
        self.assertIsNone(report["chapters"][0]["candidate_sha256"])
        self.assertIsNone(report["chapters"][0]["candidate_characters_including_spaces"])
        self.assertIsNotNone(report["chapters"][1]["candidate_sha256"])
        self.assertNotIn(SENTINEL, str(report))

    def test_external_link_markup_blocks_page_and_chapter_digest(self):
        for source in (
            "[//en.wikipedia.org Wikipedia]",
            "[mailto:editor@example.org contact]",
            "[ftp://example.org data]",
            "[https://example.org link]",
            "[SSH+GIT://example.org source]",
        ):
            with self.subTest(source=source):
                self.assertEqual(preflight.candidate_page_body(source),
                                 ("UNSUPPORTED_PAGE_MARKUP", None))
        for prose in (
            "Обычная проза [примечание автора].",
            "Обычная ссылка без wiki-скобок https://example.org",
            "Слово [11] и тире — в повествовании.",
        ):
            with self.subTest(prose=prose):
                self.assertEqual(preflight.candidate_page_body(prose), ("CANDIDATE_ONLY", prose))
        rows = fixture()
        payload = {r["title"]: "обычная проза" for r in rows}
        payload["Page/6"] = f"{SENTINEL} [mailto:editor@example.org contact]"
        report = preflight.build_preflight(loader=lambda: rows, fetcher=lambda ids: payload)
        self.assertEqual(report["candidate_page_count"], 184)
        self.assertEqual(report["candidate_chapter_count"], 10)
        self.assertEqual(report["pages"][1]["status"], "UNSUPPORTED_PAGE_MARKUP")
        self.assertIsNone(report["pages"][1]["candidate_sha256"])
        self.assertIsNone(report["pages"][1]["candidate_characters_including_spaces"])
        self.assertEqual(report["chapters"][0]["status"], "INCOMPLETE")
        self.assertIsNone(report["chapters"][0]["candidate_sha256"])
        self.assertIsNone(report["chapters"][0]["candidate_characters_including_spaces"])
        self.assertIsNotNone(report["chapters"][1]["candidate_sha256"])
        self.assertNotIn(SENTINEL, str(report))

    def test_unspaced_mediawiki_headings_block_page_and_chapter_digests(self):
        for source in ("==Заголовок==", "===Раздел===", "  == Введение ==",
                       "Проза\n==Heading==", "= Single ="):
            with self.subTest(source=source):
                self.assertEqual(preflight.candidate_page_body(source),
                                 ("UNSUPPORTED_PAGE_MARKUP", None))
        for prose in ("Обычная проза с 1=2.", "Равенство == внутри строки.",
                      "— Диалог: 2 = 2."):
            with self.subTest(prose=prose):
                self.assertEqual(preflight.candidate_page_body(prose), ("CANDIDATE_ONLY", prose))
        rows = fixture()
        payload = {r["title"]: "обычная проза" for r in rows}
        payload["Page/6"] = f"{SENTINEL}\n===Раздел==="
        report = preflight.build_preflight(loader=lambda: rows, fetcher=lambda ids: payload)
        self.assertEqual(report["candidate_page_count"], 184)
        self.assertEqual(report["candidate_chapter_count"], 10)
        self.assertEqual(report["pages"][1]["status"], "UNSUPPORTED_PAGE_MARKUP")
        self.assertIsNone(report["pages"][1]["candidate_characters_including_spaces"])
        self.assertIsNone(report["pages"][1]["candidate_sha256"])
        self.assertEqual(report["chapters"][0]["status"], "INCOMPLETE")
        self.assertIsNone(report["chapters"][0]["candidate_characters_including_spaces"])
        self.assertIsNone(report["chapters"][0]["candidate_sha256"])
        self.assertIsNotNone(report["chapters"][1]["candidate_sha256"])
        self.assertNotIn(SENTINEL, str(report))

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
