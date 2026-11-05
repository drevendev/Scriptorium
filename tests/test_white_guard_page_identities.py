"""Metadata-only Page: capture tests; network and book text are not used."""
from __future__ import annotations

from contextlib import redirect_stdout, redirect_stderr
import io
import json
import unittest
from unittest.mock import patch

from scriptorium import white_guard_page_identities as capture
from scriptorium.white_guard_delivery import MANIFEST_SHA256
from scriptorium.white_guard_revisions import SOURCE_FAMILY_1927

SENTINEL = "PRIVATE_MANUSCRIPT_SHOULD_NEVER_APPEAR"


def preview():
    chapters = []
    for number in range(1, 21):
        row = {"chapter": number, "source_family_id": SOURCE_FAMILY_1927 if number <= 11 else "moscow-pravda-1989"}
        if number <= 11:
            first, last = capture.EXPECTED_RANGES[number - 1]
            row.update({"extraction_status": "UNSUPPORTED_MARKUP",
                        "extraction_failure_code": "PROOFREADPAGE_UNPINNED",
                        "proofreadpage_page_plan": {
                            "index_title": capture.PROOFREADPAGE_INDEX,
                            "first_page": first, "last_page": last, "page_count": last - first + 1}})
        chapters.append(row)
    return {"provider_replay": "VERIFIED_IDENTITIES", "manifest_sha256": MANIFEST_SHA256,
            "chapter_count": 20, "chapters": chapters}


def record(row):
    return {"page_id": 1000 + row["page_number"], "revision_id": 2000 + row["page_number"],
            "revision_timestamp": "2026-11-04T02:00:00Z", "mediawiki_sha1": "a" * 40}


def fetcher(rows):
    return {row["title"]: record(row) for row in rows}


def replayer(rows):
    return {row["title"]: {key: row[key] for key in (
        "page_id", "revision_id", "revision_timestamp", "mediawiki_sha1")}
            for row in rows}


class WhiteGuardPageIdentityTests(unittest.TestCase):
    def test_builds_exact_replayable_185_page_inventory_without_prose(self):
        a = capture.build_inventory(previewer=preview, fetcher=fetcher, replayer=replayer)
        self.assertEqual(a["schema_version"], capture.SCHEMA_VERSION)
        self.assertEqual(a["page_count"], 185)
        self.assertEqual(a["chapter_count"], 11)
        self.assertEqual([p["page_number"] for p in a["pages"]], list(range(5, 190)))
        self.assertEqual(a["pages"][0]["chapter"], 1)
        self.assertEqual(a["pages"][-1]["chapter"], 11)
        self.assertEqual(a["captured_page_replay"], "VERIFIED_IDENTITIES")
        self.assertFalse(a["single_edition_body_frozen"])
        self.assertFalse(a["m2_parity_admissible"])
        self.assertEqual(a["fantlab_input_identity"], "unknown")
        self.assertNotIn(SENTINEL, json.dumps(a, ensure_ascii=False))
        self.assertEqual(a, capture.build_inventory(previewer=preview, fetcher=fetcher, replayer=replayer))

    def test_rejects_unpinned_parent_routes_and_parent_identity_drift(self):
        for mutation in (
            lambda d: d.update(provider_replay="INJECTED_FIXTURE"),
            lambda d: d.update(manifest_sha256="0" * 64),
            lambda d: d["chapters"][2]["proofreadpage_page_plan"].update(last_page=54),
            lambda d: d["chapters"][3].update(extraction_failure_code="UNSUPPORTED_INLINE_MARKUP"),
            lambda d: d["chapters"][10].update(source_family_id="moscow-pravda-1989"),
        ):
            with self.subTest(mutation=repr(mutation)):
                p = preview()
                mutation(p)
                with self.assertRaises(ValueError):
                    capture.expected_page_rows(p)

    def test_missing_or_divergent_replay_fails_without_partial_receipt(self):
        rows = capture.expected_page_rows(preview())
        def short_fetch(_):
            d = fetcher(rows)
            d.pop(rows[0]["title"])
            return d
        with self.assertRaises(ValueError):
            capture.build_inventory(previewer=preview, fetcher=short_fetch, replayer=replayer)
        with self.assertRaises(ValueError):
            capture.build_inventory(previewer=preview, fetcher=fetcher, replayer=lambda _: {})
        def drift(pinned):
            d = replayer(pinned)
            d[pinned[0]["title"]]["mediawiki_sha1"] = "b" * 40
            return d
        with self.assertRaises(ValueError):
            capture.build_inventory(previewer=preview, fetcher=fetcher, replayer=drift)

    def test_provider_batches_are_bounded_metadata_only_and_fully_validated(self):
        rows = capture.expected_page_rows(preview())
        calls = []
        def query(params):
            calls.append(params)
            titles = params["titles"].split("|")
            self.assertNotIn("content", params["rvprop"])
            self.assertLessEqual(len(titles), 25)
            pages = []
            for title in titles:
                n = int(title.rsplit("/", 1)[1])
                identity = record({"page_number": n})
                pages.append({"title": title, "ns": 104, "pageid": identity["page_id"],
                              "revisions": [{"revid": identity["revision_id"],
                                             "timestamp": identity["revision_timestamp"],
                                             "sha1": identity["mediawiki_sha1"]}]})
            return {"query": {"pages": pages}}
        output = capture.fetch_current_page_identities(rows, query=query)
        self.assertEqual(len(output), 185)
        self.assertEqual(len(calls), 8)
        self.assertTrue(all(c["redirects"] == "0" for c in calls))

    def test_provider_rejects_redirect_ns_mismatch_bad_digest_duplicate_missing_and_normalized(self):
        rows = capture.expected_page_rows(preview())[:2]
        def raw_query(params):
            return {"query": {"pages": [
                {"title": title, "ns": 104, "pageid": 1000 + i,
                 "revisions": [{"revid": 2000 + i, "timestamp": "2026-11-04T02:00:00Z",
                                "sha1": "a" * 40}]}
                for i, title in enumerate(params["titles"].split("|"))]}}
        for mutation in (
            lambda d: d["query"]["pages"][0].update(ns=0),
            lambda d: d["query"]["pages"][0].update(redirect=True),
            lambda d: d["query"]["pages"][0]["revisions"][0].update(sha1=SENTINEL),
            lambda d: d["query"]["pages"][0]["revisions"][0].update(revid=True),
            lambda d: d["query"]["pages"].pop(),
            lambda d: d["query"].update(normalized=[{"from": "x", "to": "y"}]),
            lambda d: d["query"]["pages"][1].update(pageid=1000),
        ):
            with self.subTest(mutation=repr(mutation)):
                def broken(params):
                    value = raw_query(params)
                    mutation(value)
                    return value
                with self.assertRaises(ValueError):
                    capture.fetch_current_page_identities(rows, query=broken)

    def test_cli_never_emits_provider_error_or_partial_inventory(self):
        stdout, stderr = io.StringIO(), io.StringIO()
        with patch.object(capture, "build_inventory", side_effect=RuntimeError(SENTINEL)):
            with redirect_stdout(stdout), redirect_stderr(stderr):
                code = capture.main([])
        self.assertEqual(code, 2)
        self.assertEqual(stdout.getvalue(), "")
        self.assertNotIn(SENTINEL, stderr.getvalue())
        self.assertIn("no receipt issued", stderr.getvalue())


if __name__ == "__main__":
    unittest.main()
