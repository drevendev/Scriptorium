"""Offline regressions for the provider-captured, source-free identity delivery."""
from contextlib import redirect_stderr, redirect_stdout
import copy
from hashlib import sha256
import io
import json
import os
from pathlib import Path
import tempfile
import unittest
from unittest.mock import Mock, patch

from scriptorium import white_guard_delivery as delivery
from scriptorium import white_guard_revisions as revisions

ROOT = Path(__file__).resolve().parents[1]
MANIFEST = ROOT / delivery.MANIFEST_PATH


class WhiteGuardDeliveryTests(unittest.TestCase):
    def setUp(self):
        self.raw = MANIFEST.read_bytes()
        self.manifest = json.loads(self.raw)

    def encoded(self, value):
        return revisions.canonical_json_text(value).encode("utf-8")

    def provider(self):
        return {"query": {"pages": [
            {"pageid": row["page_id"], "title": row["title"], "revisions": [{
                "revid": row["revision_id"], "timestamp": row["revision_timestamp"],
                "sha1": row["mediawiki_sha1"],
            }]}
            for row in reversed(self.manifest["pages"])
        ]}}

    def test_exact_captured_inventory_and_partition(self):
        self.assertEqual(sha256(self.raw).hexdigest(), delivery.MANIFEST_SHA256)
        self.assertEqual(self.raw, self.encoded(self.manifest))
        self.assertEqual(delivery.load_manifest(MANIFEST), self.manifest)
        rows = revisions.validate_manifest(self.manifest)
        self.assertEqual([r["ordinal"] for r in rows], list(range(1, 21)))
        self.assertEqual(len({r["page_id"] for r in rows}), 20)
        self.assertEqual(len({r["revision_id"] for r in rows}), 20)
        self.assertEqual([r["source_family_id"] for r in self.manifest["pages"]],
                         [revisions.SOURCE_FAMILY_1927] * 11 + [revisions.SOURCE_FAMILY_1989] * 9)

    def test_ordinal_chapter_and_index_types_are_exact(self):
        for key in ("ordinal", "chapter"):
            for bad in (True, 1.0, "1"):
                with self.subTest(key=key, bad=bad):
                    item = copy.deepcopy(self.manifest)
                    item["pages"][0][key] = bad
                    with self.assertRaises(ValueError):
                        revisions.validate_manifest(item)
        for bad in (4715350.0, "4715350", True):
            item = copy.deepcopy(self.manifest)
            item["source_work_index_revision_id"] = bad
            with self.assertRaises(ValueError):
                revisions.validate_manifest(item)

    def test_composition_and_all_boolean_gates_are_exact(self):
        for key, value in self.manifest["capture_scope"].items():
            if type(value) is bool:
                for bad in (int(value), float(value), str(value)):
                    with self.subTest(key=key, bad=bad):
                        item = copy.deepcopy(self.manifest)
                        item["capture_scope"][key] = bad
                        with self.assertRaises(ValueError):
                            revisions.validate_manifest(item)
        for key, bad in (("literary_page_count", 20.0), ("single_edition_identity", 0)):
            item = copy.deepcopy(self.manifest)
            item["composition_contract"][key] = bad
            with self.assertRaises(ValueError):
                revisions.validate_manifest(item)

    def test_impossible_inventory_and_source_prose_fail_closed(self):
        for change in (
            lambda m: m["pages"].pop(),
            lambda m: m["pages"].reverse(),
            lambda m: m["pages"][1].update(page_id=m["pages"][0]["page_id"]),
            lambda m: m["pages"][1].update(revision_id=m["pages"][0]["revision_id"]),
            lambda m: m["pages"][0].update(source_family_id=revisions.SOURCE_FAMILY_1989),
            lambda m: m["pages"][0].update(content="forbidden synthetic fixture"),
            lambda m: m["capture_scope"].update(source_text_committed=True),
            lambda m: m.update(extra={"text": "forbidden synthetic fixture"}),
        ):
            item = copy.deepcopy(self.manifest)
            change(item)
            with self.assertRaises(ValueError):
                delivery.parse_manifest(self.encoded(item))

    def test_strict_json_and_bounds(self):
        bad_inputs = [
            b"", b"[]", b"null", b"\xff", b"{}" * 40000,
            b'{"x":1,"x":2}',
            self.raw.replace(b'"chapter": 1,', b'"chapter": 1,"chapter": 1,'),
            self.raw.replace(b'"chapter": 1,', b'"chapter": NaN,'),
            self.raw.replace(b'"chapter": 1,', b'"chapter": Infinity,'),
            self.raw.replace(b'"chapter": 1,', b'"chapter": 1e0,'),
            b"[" * 2000 + b"0" + b"]" * 2000,
        ]
        for raw in bad_inputs:
            with self.subTest(length=len(raw)):
                with self.assertRaises(ValueError):
                    delivery.parse_manifest(raw)

    def test_valid_but_different_revision_requires_readmission(self):
        item = copy.deepcopy(self.manifest)
        item["pages"][0]["revision_id"] += 1
        self.assertEqual(len(revisions.validate_manifest(item)), 20)
        with tempfile.TemporaryDirectory() as td:
            path = Path(td) / "manifest.json"
            for raw in (self.encoded(item), self.raw + b" "):
                path.write_bytes(raw)
                with self.assertRaisesRegex(ValueError, "reviewed manifest bytes changed"):
                    delivery.load_manifest(path)

    def test_missing_oversized_and_nonregular_files(self):
        with tempfile.TemporaryDirectory() as td:
            path = Path(td) / "missing.json"
            with self.assertRaises(OSError):
                delivery.load_manifest(path)
            path.write_bytes(b"x" * (delivery.MAX_MANIFEST_BYTES + 1))
            with self.assertRaises(ValueError):
                delivery.load_manifest(path)
            with self.assertRaises((OSError, ValueError)):
                delivery.load_manifest(Path(td))

    @unittest.skipUnless(hasattr(os, "symlink"), "symlinks unavailable")
    def test_leaf_and_parent_symlinks_rejected(self):
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            real = root / "real"
            real.mkdir()
            (real / "manifest.json").write_bytes(self.raw)
            (root / "leaf.json").symlink_to(real / "manifest.json")
            (root / "parent").symlink_to(real, target_is_directory=True)
            for path in (root / "leaf.json", root / "parent/manifest.json"):
                with self.assertRaisesRegex(ValueError, "symlinks"):
                    delivery.load_manifest(path)

    @unittest.skipUnless(hasattr(os, "mkfifo"), "FIFOs unavailable")
    def test_fifo_is_rejected_without_waiting_for_writer(self):
        with tempfile.TemporaryDirectory() as td:
            path = Path(td) / "input"
            os.mkfifo(path)
            with self.assertRaisesRegex(ValueError, "regular file"):
                delivery.load_manifest(path)

    def test_offline_inventory_is_not_provider_verification(self):
        query = Mock(side_effect=AssertionError("offline must not use the network"))
        receipt = delivery.build_receipt(MANIFEST, offline=True, query=query)
        query.assert_not_called()
        self.assertEqual(receipt["provider_replay"], "NOT_RUN")
        self.assertEqual(receipt["mode"], "offline_inventory")
        self.assertNotIn("verified", receipt)
        self.assertEqual(receipt["revision_count"], 20)
        self.assertEqual(receipt["source_partition_counts"], {
            "paris-concorde-1927": 11, "moscow-pravda-1989": 9,
        })
        for key in ("source_text_committed", "literary_body_extraction_frozen",
                    "single_edition_identity", "m2_parity_admissible"):
            self.assertIs(receipt[key], False)
        self.assertEqual(receipt["fantlab_source_edition_match"], "unknown")

    def test_replay_requests_only_exact_ids_and_metadata(self):
        query = Mock(return_value=self.provider())
        receipt = delivery.build_receipt(MANIFEST, query=query)
        query.assert_called_once_with({
            "action": "query", "prop": "revisions",
            "revids": "|".join(str(r["revision_id"]) for r in self.manifest["pages"]),
            "rvprop": "ids|timestamp|sha1",
        })
        self.assertEqual(receipt["provider_replay"], "VERIFIED")
        self.assertEqual(receipt["mode"], "pinned_replay")
        self.assertIs(receipt["m2_parity_admissible"], False)
        self.assertEqual(receipt, delivery.build_receipt(MANIFEST, query=query))

    def test_provider_identity_drift_or_omission_never_yields_receipt(self):
        for target, key, bad in (
            ("page", "pageid", 1), ("page", "title", "different title"),
            ("revision", "revid", 1), ("revision", "timestamp", "2000-01-01T00:00:00Z"),
            ("revision", "sha1", "0" * 40),
        ):
            response = self.provider()
            page = response["query"]["pages"][0]
            (page if target == "page" else page["revisions"][0])[key] = bad
            with self.subTest(key=key):
                with self.assertRaises(ValueError):
                    delivery.build_receipt(MANIFEST, query=lambda _: response)
        for response in ({}, {"query": {"pages": []}}):
            with self.assertRaises(ValueError):
                delivery.build_receipt(MANIFEST, query=lambda _: response)

    def test_invalid_file_never_reaches_provider(self):
        query = Mock()
        with tempfile.TemporaryDirectory() as td:
            with self.assertRaises(OSError):
                delivery.build_receipt(Path(td) / "missing", query=query)
        query.assert_not_called()

    def test_cli_offline_and_safe_failure(self):
        out, err = io.StringIO(), io.StringIO()
        with redirect_stdout(out), redirect_stderr(err):
            self.assertEqual(delivery.main(["--manifest", str(MANIFEST), "--offline"]), 0)
        self.assertEqual(json.loads(out.getvalue())["provider_replay"], "NOT_RUN")
        self.assertEqual(err.getvalue(), "")
        with tempfile.TemporaryDirectory() as td:
            out, err = io.StringIO(), io.StringIO()
            with redirect_stdout(out), redirect_stderr(err):
                self.assertEqual(delivery.main(["--manifest", str(Path(td) / "private-missing")]), 2)
            self.assertEqual(out.getvalue(), "")
            self.assertNotIn(td, err.getvalue())

    def test_workflow_is_read_only_pinned_replay_without_bootstrap(self):
        workflow = (ROOT / ".github/workflows/white-guard-source-revisions.yml").read_text()
        self.assertIn("contents: read", workflow)
        self.assertIn("persist-credentials: false", workflow)
        self.assertIn("github.event.pull_request.head.sha || github.sha", workflow)
        self.assertIn("python -m unittest discover -s tests -v", workflow)
        self.assertIn("python -m scriptorium.white_guard_delivery", workflow)
        self.assertIn("path: build/white-guard/replay.json", workflow)
        for forbidden in ("build_manifest", "BOOTSTRAP_AUTHORIZED", "capture --", "pull_request_target", "if: always()"):
            self.assertNotIn(forbidden, workflow)

    def test_cli_failure_does_not_serialize_partial_receipt(self):
        out, err = io.StringIO(), io.StringIO()
        with patch.object(delivery, "build_receipt", side_effect=ValueError("provider drift")):
            with redirect_stdout(out), redirect_stderr(err):
                self.assertEqual(delivery.main([]), 2)
        self.assertEqual(out.getvalue(), "")
        self.assertIn("no receipt issued", err.getvalue())


if __name__ == "__main__":
    unittest.main()
