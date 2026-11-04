"""Exact-type invariants on actual source modules, with synthetic local fixtures."""
from copy import deepcopy
from hashlib import sha256
import unittest
from unittest.mock import Mock

from scriptorium import source_revision_manifest as packed
from scriptorium import wikisource_freeze as freeze
from scriptorium import wikisource_replay as replay
from scriptorium import single_page_revision as single

STAMP = "2026-01-01T00:00:00Z"
ROW = {"title": "Synthetic chapter", "revision_id": 1, "page_id": 1,
       "revision_timestamp": STAMP, "mediawiki_sha1": "a" * 40}


def payload(rows):
    return {"query": {"pages": [{"pageid": row.get("page_id", 1), "title": row["title"],
        "revisions": [{"revid": row["revision_id"], "timestamp": row["revision_timestamp"],
                       "sha1": row["mediawiki_sha1"],
                       "slots": {"main": {"content": "Synthetic fixture."}}}]} for row in rows]}}


def receipt():
    rows = [{**chapter, "revision_id": chapter["ordinal"],
             "revision_timestamp": STAMP, "mediawiki_sha1": "a" * 40}
            for chapter in freeze.expected_chapters()]
    result = {key: "fixture" for key in packed._COPY_KEYS}
    result.update(manifest_version=packed.EXPANDED_RECEIPT_VERSION, chapters=rows,
                  composition={"part_chapter_counts": list(freeze.PART_CHAPTER_COUNTS)},
                  composite_identity={})
    return result


class ExactReplayIdentityTests(unittest.TestCase):
    def test_valid_revision_returns_same_content(self):
        query = Mock(return_value=payload([ROW]))
        self.assertEqual(replay.fetch_pinned_chapter_revisions([ROW], query=query),
                         {ROW["title"]: "Synthetic fixture."})
        self.assertEqual(query.call_args.args[0]["revids"], "1")
        self.assertNotIn("redirects", query.call_args.args[0])

    def test_expected_id_not_coerced_and_no_request_sent(self):
        for value in (True, False, 1.0, 1.9, "1", None, 0, -1):
            with self.subTest(value=value):
                query = Mock()
                with self.assertRaisesRegex(ValueError, "expected revision id"):
                    replay.fetch_pinned_chapter_revisions([{**ROW, "revision_id": value}], query=query)
                query.assert_not_called()

    def test_observed_revision_requires_exact_integer(self):
        for value in (True, 1.0, "1", None):
            with self.subTest(value=value):
                with self.assertRaisesRegex(ValueError, "unexpected revision id"):
                    replay.fetch_pinned_chapter_revisions([ROW], query=lambda _: payload([{**ROW, "revision_id": value}]))

    def test_all_batches_preflight_before_network(self):
        rows = [{**ROW, "title": f"Synthetic {i}", "revision_id": i + 1} for i in range(41)]
        rows[-1]["revision_id"] = True
        query = Mock()
        with self.assertRaises(ValueError):
            replay.fetch_pinned_chapter_revisions(rows, query=query)
        query.assert_not_called()

    def test_duplicate_id_and_title_rejected_before_network(self):
        for rows in ([ROW, {**ROW, "title": "Other"}], [ROW, {**ROW, "revision_id": 2}]):
            with self.subTest(rows=rows):
                query = Mock()
                with self.assertRaisesRegex(ValueError, "duplicate"):
                    replay.fetch_pinned_chapter_revisions(rows, query=query)
                query.assert_not_called()

    def test_invalid_metadata_and_page_id_preflight(self):
        for key, value in (("page_id", True), ("page_id", 1.0), ("title", ""),
                           ("title", None), ("revision_timestamp", 0), ("mediawiki_sha1", "")):
            with self.subTest(key=key, value=value):
                query = Mock()
                with self.assertRaises(ValueError):
                    replay.fetch_pinned_chapter_revisions([{**ROW, key: value}], query=query)
                query.assert_not_called()

    def test_drift_and_missing_revisions_still_rejected(self):
        variants = [payload([{**ROW, "title": "Other"}]), payload([{**ROW, "page_id": 2}]),
                    payload([{**ROW, "revision_timestamp": "2026-01-02T00:00:00Z"}]),
                    payload([{**ROW, "mediawiki_sha1": "b" * 40}]), payload([]), payload([ROW, ROW]), None]
        for response in variants:
            with self.subTest(response=response):
                with self.assertRaises(ValueError):
                    replay.fetch_pinned_chapter_revisions([ROW], query=lambda _: response)

    def test_valid_multibatch_order_is_stable(self):
        rows = [{**ROW, "title": f"Synthetic {i}", "revision_id": i + 1} for i in range(41)]
        queries = []
        def query(params):
            queries.append(params)
            ids = {int(i) for i in params["revids"].split("|")}
            return payload([r for r in rows if r["revision_id"] in ids][::-1])
        observed = replay.fetch_pinned_chapter_revisions(rows, query=query)
        self.assertEqual(set(observed), {r["title"] for r in rows})
        self.assertEqual(len(queries), 2)
        self.assertEqual(queries[1]["revids"], "41")

    def test_current_capture_rejects_boolean_revision(self):
        with self.assertRaisesRegex(ValueError, "incomplete revision identity"):
            freeze.fetch_current_chapter_revisions([{"title": ROW["title"]}],
                query=lambda _: payload([{**ROW, "revision_id": True}]))


class PackedIdentityTests(unittest.TestCase):
    def test_valid_roundtrip_and_canonical_bytes_unchanged(self):
        original = receipt()
        manifest = packed.pack_revision_manifest(original)
        rows = packed.decode_chapter_identities(manifest)
        self.assertEqual(list(rows), original["chapters"])
        self.assertEqual(manifest["chapter_identity_encoding"]["captured_identity_sha256"],
                         packed.chapter_identity_sha256(original["chapters"]))
        self.assertEqual(packed.canonical_json_text(manifest),
                         packed.canonical_json_text(packed.pack_revision_manifest(original)))

    def test_expanded_scalar_identity_types(self):
        for key in ("ordinal", "part", "chapter", "revision_id"):
            for bad in (True, 1.0, "1"):
                with self.subTest(key=key, bad=bad):
                    original = receipt()
                    original["chapters"][0][key] = bad
                    with self.assertRaises(ValueError):
                        packed.pack_revision_manifest(original)

    def test_packed_offsets_reject_boolean_fractional_string_and_overflow(self):
        for bad in (False, True, 0.0, "0", -1, 10 ** 30):
            with self.subTest(bad=bad):
                manifest = packed.pack_revision_manifest(receipt())
                manifest["chapter_identity_encoding"]["revision_timestamp_offsets_seconds"][0] = bad
                with self.assertRaisesRegex(ValueError, "timestamp offset"):
                    packed.decode_chapter_identities(manifest)

    def test_packed_revision_types_even_with_recomputed_digest(self):
        for bad in (True, 1.0, "1"):
            with self.subTest(bad=bad):
                original = receipt()
                manifest = packed.pack_revision_manifest(original)
                original["chapters"][0]["revision_id"] = bad
                encoding = manifest["chapter_identity_encoding"]
                encoding["revision_ids"][0] = bad
                encoding["captured_identity_sha256"] = packed.chapter_identity_sha256(original["chapters"])
                with self.assertRaisesRegex(ValueError, "revision_id"):
                    packed.decode_chapter_identities(manifest)

    def test_packed_width_and_counts_require_integers(self):
        for field in ("width", "counts"):
            with self.subTest(field=field):
                manifest = packed.pack_revision_manifest(receipt())
                if field == "width":
                    manifest["chapter_identity_encoding"]["mediawiki_sha1_base64_no_padding_fixed_width"] = 27.0
                else:
                    manifest["composition"]["part_chapter_counts"][0] = 34.0
                with self.assertRaises(ValueError):
                    packed.decode_chapter_identities(manifest)

    def test_duplicate_and_digest_drift_still_fail(self):
        for field in ("revision_ids", "captured_identity_sha256"):
            manifest = packed.pack_revision_manifest(receipt())
            if field == "revision_ids":
                manifest["chapter_identity_encoding"][field][1] = 1
            else:
                manifest["chapter_identity_encoding"][field] = "0" * 64
            with self.assertRaises(ValueError):
                packed.decode_chapter_identities(manifest)


class SingleIdentityTests(unittest.TestCase):
    def manifest(self):
        return single.build_manifest(candidate_id="synthetic", title=ROW["title"], revision_id=1,
            source_work_url="https://example.org/work", permanent_source_url="https://example.org/?oldid=1",
            bibliographic_source="synthetic fixture", legal_basis="synthetic fixture",
            fetcher=lambda **kw: single.fetch_pinned_revision(**kw, query=lambda _: payload([ROW])))

    def test_valid_source_free_manifest_stays_valid(self):
        manifest = self.manifest()
        single.validate_manifest(manifest)
        result = single.replay_manifest(manifest, fetcher=lambda **_: manifest["source_identity"].copy())
        self.assertTrue(result["verified"])
        self.assertNotIn("Synthetic fixture.", str(result))
        self.assertEqual(result["wikitext_sha256"], sha256(b"Synthetic fixture.").hexdigest())

    def test_expected_id_rejected_before_single_request(self):
        for value in (True, 1.0, "1", 0, -1):
            query = Mock()
            with self.assertRaises(ValueError):
                single.fetch_pinned_revision(title=ROW["title"], revision_id=value, query=query)
            query.assert_not_called()

    def test_observed_id_and_page_types_rejected(self):
        for key in ("page_id", "revision_id"):
            for value in (True, 1.0, "1"):
                with self.subTest(key=key, value=value):
                    with self.assertRaises(ValueError):
                        single.fetch_pinned_revision(title=ROW["title"], revision_id=1,
                            query=lambda _: payload([{**ROW, key: value}]))

    def test_manifest_types_and_scientific_flags_rejected(self):
        for key in ("revision_id", "page_id", "wikitext_character_count", "wikitext_utf8_byte_count"):
            for bad in (True, 1.0, "1"):
                manifest = self.manifest()
                manifest["source_identity"][key] = bad
                with self.assertRaises(ValueError):
                    single.validate_manifest(manifest)
        for key, value in self.manifest()["capture_scope"].items():
            manifest = self.manifest()
            manifest["capture_scope"][key] = int(value)
            with self.assertRaisesRegex(ValueError, "scope drift"):
                single.validate_manifest(manifest)

    def test_replay_injected_type_confusion_not_equal_to_identity(self):
        manifest = self.manifest()
        observed = deepcopy(manifest["source_identity"])
        observed["revision_id"] = True
        with self.assertRaises(ValueError):
            single.replay_manifest(manifest, fetcher=lambda **_: observed)
