"""Source-free regressions; provider network and historical body are NOT_RUN."""
from __future__ import annotations

from contextlib import redirect_stderr, redirect_stdout
from hashlib import sha256
import io
import json
from pathlib import Path
import unittest
from unittest.mock import patch

from scriptorium import white_guard_body_preflight as preflight
from scriptorium import white_guard_delivery as delivery
from scriptorium import white_guard_revisions as revisions

ROOT = Path(__file__).resolve().parents[1]
MANIFEST = ROOT / delivery.MANIFEST_PATH
PRIVATE_SENTINEL = "SECRET_PRIVATE_CHAPTER_PROSE_9z4"


class WhiteGuardBodyPreflightTests(unittest.TestCase):
    def setUp(self):
        self.rows = revisions.validate_manifest(delivery.load_manifest(MANIFEST))

    def sources(self):
        return {row["title"]: '<div class="text">' + PRIVATE_SENTINEL + f' {row["ordinal"]}.</div>'
                for row in self.rows}

    def test_full_preview_is_source_free_partitioned_and_explicitly_unadmitted(self):
        data = self.sources()
        receipt = preflight.build_preflight(MANIFEST, fetcher=lambda _: data)
        self.assertEqual(receipt["schema_version"], preflight.SCHEMA_VERSION)
        self.assertEqual(receipt["chapter_count"], 20)
        self.assertEqual(receipt["candidate_chapter_count"], 20)
        self.assertEqual(receipt["provider_replay"], "INJECTED_FIXTURE")
        self.assertEqual([r["chapter"] for r in receipt["chapters"]], list(range(1, 21)))
        self.assertEqual([r["source_family_id"] for r in receipt["chapters"]],
                         [revisions.SOURCE_FAMILY_1927] * 11 + [revisions.SOURCE_FAMILY_1989] * 9)
        self.assertTrue(all(r["extraction_status"] == "CANDIDATE_ONLY" for r in receipt["chapters"]))
        self.assertTrue(all(r["extraction_failure_code"] is None for r in receipt["chapters"]))
        self.assertEqual(receipt["chapters"][0]["wikitext_sha256"],
                         sha256(data[self.rows[0]["title"]].encode()).hexdigest())
        self.assertIs(receipt["candidate_meets_size_threshold"], False)
        self.assertIs(receipt["literary_body_extraction_frozen"], False)
        self.assertIs(receipt["single_edition_identity"], False)
        self.assertIs(receipt["m2_parity_admissible"], False)
        self.assertEqual(receipt["fantlab_input_identity"], "unknown")
        self.assertNotIn(PRIVATE_SENTINEL, json.dumps(receipt, ensure_ascii=False))
        self.assertEqual(receipt, preflight.build_preflight(MANIFEST, fetcher=lambda _: data))

    def test_one_unsupported_chapter_invalidates_composite_without_losing_safe_coverage(self):
        data = self.sources()
        data[self.rows[12]["title"]] = "unrecognized {{PrivateMarkup|" + PRIVATE_SENTINEL + "}}"
        receipt = preflight.build_preflight(MANIFEST, fetcher=lambda _: data)
        self.assertEqual(receipt["candidate_chapter_count"], 19)
        self.assertIsNone(receipt["candidate_composite_characters_including_spaces"])
        self.assertIsNone(receipt["candidate_composite_sha256"])
        self.assertIsNone(receipt["candidate_meets_size_threshold"])
        self.assertEqual(receipt["chapters"][12]["extraction_status"], "UNSUPPORTED_MARKUP")
        self.assertEqual(receipt["chapters"][12]["extraction_failure_code"], "BODY_CONTAINER_ABSENT")
        self.assertIsNone(receipt["chapters"][12]["candidate_body_characters"])
        self.assertNotIn(PRIVATE_SENTINEL, json.dumps(receipt, ensure_ascii=False))

    def test_missing_extra_wrong_type_and_overlarge_source_fail_closed(self):
        base = self.sources()
        for change in (
            lambda d: d.pop(self.rows[0]["title"]),
            lambda d: d.update(unexpected="other"),
            lambda d: d.update({self.rows[0]["title"]: b"raw"}),
            lambda d: d.update({self.rows[0]["title"]: "x" * (preflight.MAX_CHAPTER_WIKITEXT_CHARACTERS + 1)}),
        ):
            sample = dict(base)
            change(sample)
            with self.subTest(case=len(sample)):
                with self.assertRaises(ValueError):
                    preflight.build_preflight(MANIFEST, fetcher=lambda _: sample)

    def test_fetcher_receives_exact_20_pinned_revisions(self):
        seen = []
        def fetcher(rows):
            seen.extend(rows)
            return self.sources()
        preflight.build_preflight(MANIFEST, fetcher=fetcher)
        self.assertEqual(seen, list(self.rows))
        self.assertEqual(seen[0]["revision_id"], 2423390)
        self.assertEqual(len({r["revision_id"] for r in seen}), 20)

    def test_unsafe_extractor_exception_never_enters_receipt(self):
        def rejecting(source):
            raise ValueError("sensitive wikitext: " + source)
        receipt = preflight.build_preflight(MANIFEST, fetcher=lambda _: self.sources(), extractor=rejecting)
        self.assertEqual(receipt["candidate_chapter_count"], 0)
        self.assertNotIn(PRIVATE_SENTINEL, json.dumps(receipt, ensure_ascii=False))
        self.assertTrue(all(r["extraction_status"] == "UNSUPPORTED_MARKUP" for r in receipt["chapters"]))

    def test_each_structural_failure_has_a_safe_code_without_exposing_prose(self):
        cases = (
            ("absent", "no body: " + PRIVATE_SENTINEL, "BODY_CONTAINER_ABSENT"),
            ("multiple", '<div class="text">one</div><div class="text">two</div>',
             "BODY_CONTAINER_MULTIPLE"),
            ("template", '<div class="text">one {{Unknown|x}} ' + PRIVATE_SENTINEL + '</div>',
             "UNSUPPORTED_TEMPLATE"),
            ("heading", '<div class="text">one\n== Heading ==\n' + PRIVATE_SENTINEL + '</div>',
             "TABLE_OR_HEADING"),
            ("html", '<div class="text"><section>one</section> ' + PRIVATE_SENTINEL + '</div>',
             "UNSUPPORTED_INLINE_MARKUP"),
            ("empty", '<div class="text"> </div>', "EMPTY_BODY"),
        )
        for label, source, code in cases:
            with self.subTest(label=label):
                data = self.sources()
                data[self.rows[0]["title"]] = source
                receipt = preflight.build_preflight(MANIFEST, fetcher=lambda _: data)
                first = receipt["chapters"][0]
                self.assertEqual(first["extraction_status"], "UNSUPPORTED_MARKUP")
                self.assertEqual(first["extraction_failure_code"], code)
                self.assertIsNone(first["candidate_body_characters"])
                self.assertEqual(receipt["candidate_chapter_count"], 19)
                self.assertIsNone(receipt["candidate_composite_sha256"])
                self.assertNotIn(PRIVATE_SENTINEL, json.dumps(receipt, ensure_ascii=False))

    def test_unknown_or_untrusted_extractor_failures_are_unclassified(self):
        from scriptorium.wikisource_freeze import BodyExtractionError

        def forged(_):
            raise BodyExtractionError(PRIVATE_SENTINEL, PRIVATE_SENTINEL)

        def crashing_runtime(source):
            raise RuntimeError("unexpected parser fault: " + source)

        def crashing_key(source):
            raise KeyError("unexpected parser fault: " + source)

        for extractor in (forged, lambda _: 23, crashing_runtime, crashing_key):
            with self.subTest(extractor=extractor.__name__):
                receipt = preflight.build_preflight(
                    MANIFEST, fetcher=lambda _: self.sources(), extractor=extractor
                )
                self.assertEqual(receipt["candidate_chapter_count"], 0)
                self.assertIsNone(receipt["candidate_composite_sha256"])
                self.assertFalse(receipt["m2_parity_admissible"])
                self.assertTrue(all(
                    c["extraction_status"] == "UNSUPPORTED_MARKUP"
                    and c["extraction_failure_code"] == "UNCLASSIFIED_ERROR"
                    for c in receipt["chapters"]
                ))
                self.assertNotIn(PRIVATE_SENTINEL, json.dumps(receipt, ensure_ascii=False))

    def test_unexpected_parser_error_stays_source_free_through_cli(self):
        original_build = preflight.build_preflight

        def crashing_extractor(source):
            raise RuntimeError("private chapter data: " + source)

        def injected_build(_):
            return original_build(
                MANIFEST, fetcher=lambda _: self.sources(), extractor=crashing_extractor
            )

        out, err = io.StringIO(), io.StringIO()
        with patch.object(preflight, "build_preflight", side_effect=injected_build):
            with redirect_stdout(out), redirect_stderr(err):
                result = preflight.main([])
        self.assertEqual(result, 0)
        self.assertEqual(err.getvalue(), "")
        self.assertNotIn(PRIVATE_SENTINEL, out.getvalue())
        receipt = json.loads(out.getvalue())
        self.assertEqual(receipt["candidate_chapter_count"], 0)
        self.assertTrue(all(c["extraction_failure_code"] == "UNCLASSIFIED_ERROR"
                            for c in receipt["chapters"]))

    def test_unexpected_provider_failure_remains_fatal_not_a_partial_receipt(self):
        def failing_provider(_):
            raise RuntimeError("provider rejected request: " + PRIVATE_SENTINEL)

        with self.assertRaises(RuntimeError):
            preflight.build_preflight(MANIFEST, fetcher=failing_provider)

    def test_cli_sanitizes_provider_failure_and_never_outputs_partial_text(self):
        for error in (ValueError(PRIVATE_SENTINEL), RuntimeError(PRIVATE_SENTINEL),
                      KeyError(PRIVATE_SENTINEL)):
            with self.subTest(error=type(error).__name__):
                out, err = io.StringIO(), io.StringIO()
                with patch.object(preflight, "build_preflight", side_effect=error):
                    with redirect_stdout(out), redirect_stderr(err):
                        result = preflight.main([])
                self.assertEqual(result, 2)
                self.assertEqual(out.getvalue(), "")
                self.assertNotIn(PRIVATE_SENTINEL, err.getvalue())
                self.assertEqual(
                    err.getvalue().strip(),
                    "Pinned White Guard body preflight failed; no receipt issued."
                )


if __name__ == "__main__":
    unittest.main()
