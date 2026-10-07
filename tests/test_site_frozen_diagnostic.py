"""Integration tests for the explicitly registered historical full-work route."""
import copy
from hashlib import sha256
from html.parser import HTMLParser
import json
from pathlib import Path
import shutil
import tempfile
import unittest
from unittest.mock import patch
from urllib.parse import urlsplit, unquote

from scriptorium import site_frozen_diagnostic as frozen
from scriptorium import site_renderer as site

ROOT = Path(__file__).resolve().parents[1]


class Links(HTMLParser):
    def __init__(self, text):
        super().__init__()
        self.links = []
        self.ids = []
        self.feed(text)

    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        if "id" in attrs:
            self.ids.append(attrs["id"])
        if tag in {"a", "link"} and "href" in attrs:
            self.links.append(attrs["href"])


class FrozenSiteIntegrationTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name) / "repo"
        self.manifest = json.loads((ROOT / "site/publication-manifest.json").read_text())
        (self.root / "site").mkdir(parents=True)
        for entry in self.manifest["entries"]:
            destination = self.root / entry["artifact_path"]
            destination.parent.mkdir(parents=True, exist_ok=True)
            shutil.copyfile(ROOT / entry["artifact_path"], destination)
        self.entry = next(row for row in self.manifest["entries"] if row["entry_id"] == frozen.ENTRY_ID)
        self.raw = (self.root / frozen.ARTIFACT_PATH).read_bytes()
        self.artifact = json.loads(self.raw)
        self.output = self.root / "build/site"
        self.write_manifest()

    def write_manifest(self):
        (self.root / "site/publication-manifest.json").write_text(json.dumps(self.manifest, ensure_ascii=False))

    def snapshot(self):
        return {path.relative_to(self.output).as_posix(): path.read_bytes()
                for path in sorted(self.output.rglob("*")) if path.is_file()}

    def test_canonical_site_preserves_four_routes_and_adds_one_real_report(self):
        record = site.build_site(self.root, self.output)
        routes = {row["route"] for row in record["entries"]}
        self.assertEqual(routes, {
            "works/anna-karenina-part1-ch1-opening/",
            "works/anna-karenina-part1-ch2-dialogue/",
            "works/tolstoy-anna-karenina-morphology-diagnostic/",
            "works/tolstoy-resurrection-provenance/",
            f"works/{frozen.SLUG}/",
        })
        self.assertEqual(record["generator_profile"], "scriptorium-static-site-v2")
        row = next(row for row in record["entries"] if row["entry_id"] == frozen.ENTRY_ID)
        self.assertEqual(row["artifact_sha256"], frozen.ARTIFACT_SHA256)
        index = (self.output / "index.html").read_text()
        self.assertIn("Explore the 28-metric full-work report", index)
        self.assertIn("full-work metrics", index)
        self.assertIn("provenance-only", index)
        self.assertEqual(index.count('class="card"'), 5)
        rendered = (self.output / "works" / frozen.SLUG / "index.html").read_text()
        self.assertEqual(rendered.count('scope="row"'), 28)
        self.assertEqual(rendered.count("characters / word"), 1)
        self.assertEqual(rendered.count("characters / sentence"), 3)
        self.assertIn("Historical snapshot", rendered)
        self.assertIn("0/5", rendered)
        self.assertIn("unknown", rendered)
        self.assertIn('href="../../"', rendered)
        self.assertIn('id="metrics" tabindex="-1"', rendered)
        self.assertEqual(frozen.report.summarize(self.artifact)["missing_actual_count"], 5)
        self.assertEqual((self.root / frozen.ARTIFACT_PATH).read_bytes(), self.raw)

    def test_double_build_is_byte_identical(self):
        site.build_site(self.root, self.output)
        before = self.snapshot()
        site.build_site(self.root, self.output)
        self.assertEqual(self.snapshot(), before)

    def test_all_internal_links_and_fragments_resolve(self):
        site.build_site(self.root, self.output)
        for path in self.output.rglob("*.html"):
            parsed = Links(path.read_text())
            self.assertEqual(len(parsed.ids), len(set(parsed.ids)), path)
            for href in parsed.links:
                link = urlsplit(href)
                if link.scheme or link.netloc:
                    continue
                target = (path.parent / unquote(link.path)).resolve() if link.path else path
                if target.is_dir():
                    target = target / "index.html"
                self.assertTrue(target.is_file(), (path, href))
                self.assertTrue(target.is_relative_to(self.output), (path, href))
                if link.fragment:
                    self.assertIn(link.fragment, Links(target.read_text()).ids)

    def test_every_page_has_targetable_main_and_no_source_selection_prose(self):
        site.build_site(self.root, self.output)
        for path in self.output.rglob("*.html"):
            rendered = path.read_text()
            self.assertIn('id="main-content" tabindex="-1"', rendered)
            self.assertNotIn("<script", rendered)
            self.assertNotIn("Все счастливые семьи похожи друг на друга", rendered)
        css = (self.output / "assets/site.css").read_text()
        for contract in ("*:focus-visible", "min-height: 44px", "prefers-reduced-motion", "min(18rem, 100%)"):
            self.assertIn(contract, css)

    def test_unlisted_snapshot_is_not_discovered_or_featured(self):
        self.manifest["entries"].remove(self.entry)
        self.write_manifest()
        site.build_site(self.root, self.output)
        self.assertFalse((self.output / "works" / frozen.SLUG).exists())
        self.assertNotIn("primary-action", (self.output / "index.html").read_text())

    def test_every_fixed_declaration_field_fails_closed(self):
        site.build_site(self.root, self.output)
        before = self.snapshot()
        for key, bad in {
            "entry_id": "other-v1", "slug": "other", "publication_status": "published",
            "benchmark_admissibility": "admissible", "corpus_admissibility": "admissible",
            "compatibility_claim": "reproduced", "source_text_included": True,
        }.items():
            with self.subTest(key=key):
                old = self.entry[key]
                self.entry[key] = bad
                self.write_manifest()
                with self.assertRaises(site.PublicationBuildError):
                    site.build_site(self.root, self.output)
                self.assertEqual(self.snapshot(), before)
                self.entry[key] = old
        self.write_manifest()

    def test_source_flag_numeric_false_is_not_boolean_permission(self):
        entry = dict(self.entry, source_text_included=0)
        with self.assertRaises(ValueError):
            frozen.prepare(entry, self.artifact, self.raw)

    def test_any_changed_snapshot_bytes_preserve_last_valid_build(self):
        site.build_site(self.root, self.output)
        before = self.snapshot()
        path = self.root / frozen.ARTIFACT_PATH
        changes = [self.raw + b" ", b'{"duplicate":1,"duplicate":2}', b"not JSON"]
        for content in changes:
            with self.subTest(content=content[:20]):
                path.write_bytes(content)
                with self.assertRaises(site.PublicationBuildError):
                    site.build_site(self.root, self.output)
                self.assertEqual(self.snapshot(), before)
        path.write_bytes(self.raw)

    def test_object_cannot_disagree_with_verified_bytes(self):
        changed = copy.deepcopy(self.artifact)
        changed["observations"].append("UNREVIEWED PAYLOAD")
        with self.assertRaisesRegex(ValueError, "differs from"):
            frozen.prepare(self.entry, changed, self.raw)

    def test_validator_is_still_required_after_digest_approval(self):
        changed = copy.deepcopy(self.artifact)
        changed["epistemic_status"]["m2_parity_admissible"] = True
        raw = json.dumps(changed).encode()
        # A future digest approval must not turn off the science schema validator.
        with patch.object(frozen, "ARTIFACT_SHA256", sha256(raw).hexdigest()):
            with self.assertRaises(ValueError):
                frozen.prepare(self.entry, changed, raw)

    def test_wrong_candidate_is_rejected_even_with_a_new_approved_digest(self):
        changed = copy.deepcopy(self.artifact)
        changed["candidate_id"] = "different-candidate"
        raw = json.dumps(changed).encode()
        with patch.object(frozen, "ARTIFACT_SHA256", sha256(raw).hexdigest()):
            with self.assertRaisesRegex(ValueError, "candidate identity"):
                frozen.prepare(self.entry, changed, raw)

    def test_missing_snapshot_and_unregistered_path_preserve_output(self):
        site.build_site(self.root, self.output)
        before = self.snapshot()
        path = self.root / frozen.ARTIFACT_PATH
        alternate = path.with_name("alternate.json")
        path.rename(alternate)
        with self.assertRaises(site.PublicationBuildError):
            site.build_site(self.root, self.output)
        self.entry["artifact_path"] = alternate.relative_to(self.root).as_posix()
        self.write_manifest()
        with self.assertRaises(site.PublicationBuildError):
            site.build_site(self.root, self.output)
        self.assertEqual(self.snapshot(), before)

    def test_snapshot_symlink_is_not_a_publication_route(self):
        path = self.root / frozen.ARTIFACT_PATH
        alternate = path.with_name("alternate.json")
        path.rename(alternate)
        path.symlink_to(alternate)
        with self.assertRaisesRegex(site.PublicationBuildError, "symlinks"):
            site.build_site(self.root, self.output)

    def test_title_is_escaped_in_index_and_reused_report(self):
        self.entry["title"] = '<script>alert("x")</script>'
        self.write_manifest()
        site.build_site(self.root, self.output)
        for path in (self.output / "index.html", self.output / "works" / frozen.SLUG / "index.html"):
            text = path.read_text()
            self.assertNotIn("<script>", text)
            self.assertIn("&lt;script&gt;", text)

    def test_report_adapter_marker_drift_preserves_output(self):
        site.build_site(self.root, self.output)
        before = self.snapshot()
        with patch.object(frozen.report, "render_html", return_value="<html>changed contract</html>"):
            with self.assertRaisesRegex(site.PublicationBuildError, "integration marker"):
                site.build_site(self.root, self.output)
        self.assertEqual(self.snapshot(), before)


if __name__ == "__main__":
    unittest.main()
