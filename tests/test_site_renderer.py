import copy
import json
import shutil
import tempfile
import unittest
from pathlib import Path

from scriptorium.site_renderer import PublicationBuildError, build_site


class StaticSiteRendererTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.root = Path(self.temp.name) / "repo"
        (self.root / "site").mkdir(parents=True)
        (self.root / "showcase").mkdir()
        self.output = self.root / "build" / "site"
        self.entry = {
            "entry_id": "example-v1",
            "kind": "work_showcase",
            "slug": "example",
            "title": "Example analysis",
            "artifact_path": "showcase/example.json",
            "artifact_schema": "scriptorium-deterministic-metrics-v1",
            "publication_status": "illustrative_excerpt",
            "benchmark_admissibility": "not_admissible",
            "corpus_admissibility": "not_admissible",
            "compatibility_claim": "mixed",
            "source_text_included": False,
        }
        self.artifact = {
            "showcase_id": "example-v1",
            "status": "illustrative_excerpt",
            "benchmark_admissibility": "not_admissible",
            "corpus_admissibility": "not_admissible",
            "representativeness_note": "Short illustrative excerpt; not parity evidence.",
            "work": {
                "author": "Author & Co.",
                "title": "Work <One>",
                "language": "ru",
            },
            "source": {
                "provider": "Example Source",
                "page": "Example page",
                "revision_url": "https://example.test/revision?id=1&old=2",
                "edition_note": "Example edition",
                "legal_basis": "public domain",
                "selection": {"start_text": "SECRET SOURCE PROSE"},
                "source_text_committed": False,
            },
            "analysis": {
                "schema_version": "scriptorium-deterministic-metrics-v1",
                "metrics": {
                    "fantlab.general.words": {
                        "value": 12,
                        "unit": "words",
                        "compatibility_status": "inferred",
                    },
                    "scriptorium.general.sentences": {
                        "value": 2,
                        "unit": "sentences",
                        "compatibility_status": "extension",
                    },
                },
            },
        }
        self._write_fixture()

    def tearDown(self):
        self.temp.cleanup()

    def _manifest(self):
        return {
            "schema_version": "scriptorium-publication-manifest-v1",
            "generated_from": {"repository": "drevendev/Scriptorium", "branch": "master"},
            "deployment": {
                "publication_source": "github_actions",
                "generated_output_committed": False,
            },
            "entries": [self.entry],
        }

    def _write_fixture(self):
        (self.root / "site" / "publication-manifest.json").write_text(
            json.dumps(self._manifest(), ensure_ascii=False), encoding="utf-8"
        )
        (self.root / "showcase" / "example.json").write_text(
            json.dumps(self.artifact, ensure_ascii=False), encoding="utf-8"
        )

    def _snapshot(self):
        return {
            path.relative_to(self.output).as_posix(): path.read_bytes()
            for path in sorted(self.output.rglob("*"))
            if path.is_file()
        }

    def test_build_is_deterministic_and_routes_are_stable(self):
        first = build_site(self.root, "build/site")
        first_snapshot = self._snapshot()
        second = build_site(self.root, "build/site")
        self.assertEqual(first, second)
        self.assertEqual(first_snapshot, self._snapshot())
        self.assertTrue((self.output / "index.html").is_file())
        page = self.output / "works" / "example" / "index.html"
        self.assertTrue(page.is_file())
        html = page.read_text(encoding="utf-8")
        self.assertIn("fantlab.general.words", html)
        self.assertIn("inferred", html)
        self.assertIn("not_admissible", html)
        self.assertNotIn("SECRET SOURCE PROSE", html)
        self.assertEqual(first["entries"][0]["route"], "works/example/")

    def test_unlisted_artifact_is_not_discovered(self):
        hidden = copy.deepcopy(self.artifact)
        hidden["showcase_id"] = "hidden-v1"
        hidden["work"]["title"] = "UNLISTED WORK"
        (self.root / "showcase" / "hidden.json").write_text(
            json.dumps(hidden), encoding="utf-8"
        )
        build_site(self.root, self.output)
        all_html = "\n".join(
            path.read_text(encoding="utf-8") for path in self.output.rglob("*.html")
        )
        self.assertNotIn("UNLISTED WORK", all_html)

    def test_artifact_controlled_strings_are_escaped(self):
        self.entry["title"] = '<script>alert("x")</script>'
        self.artifact["work"]["author"] = "A < B & C"
        self._write_fixture()
        build_site(self.root, self.output)
        html = (self.output / "works" / "example" / "index.html").read_text(encoding="utf-8")
        self.assertNotIn('<script>alert("x")</script>', html)
        self.assertIn("&lt;script&gt;alert(&quot;x&quot;)&lt;/script&gt;", html)
        self.assertIn("A &lt; B &amp; C", html)
        self.assertIn("?id=1&amp;old=2", html)

    def test_compatibility_upgrade_and_label_mismatch_fail_closed(self):
        self.entry["compatibility_claim"] = "reproduced"
        self._write_fixture()
        with self.assertRaisesRegex(PublicationBuildError, "compatibility_claim"):
            build_site(self.root, self.output)

        self.entry["compatibility_claim"] = "mixed"
        self.entry["corpus_admissibility"] = "admissible"
        self._write_fixture()
        with self.assertRaisesRegex(PublicationBuildError, "corpus_admissibility"):
            build_site(self.root, self.output)

    def test_source_text_flags_fail_closed(self):
        self.entry["source_text_included"] = True
        self._write_fixture()
        with self.assertRaisesRegex(PublicationBuildError, "source text"):
            build_site(self.root, self.output)

        self.entry["source_text_included"] = False
        self.artifact["source"]["source_text_committed"] = True
        self._write_fixture()
        with self.assertRaisesRegex(PublicationBuildError, "source text"):
            build_site(self.root, self.output)

    def test_canonical_manifest_and_artifacts_must_not_traverse_symlinks(self):
        alternate = self.root / "site" / "alternate.json"
        alternate.write_text(
            (self.root / "site" / "publication-manifest.json").read_text(encoding="utf-8"),
            encoding="utf-8",
        )
        (self.root / "site" / "publication-manifest.json").unlink()
        (self.root / "site" / "publication-manifest.json").symlink_to(alternate)
        with self.assertRaisesRegex(PublicationBuildError, "manifest must not traverse symlinks"):
            build_site(self.root, self.output)

        (self.root / "site" / "publication-manifest.json").unlink()
        alternate.replace(self.root / "site" / "publication-manifest.json")
        real_artifact = self.root / "showcase" / "real.json"
        (self.root / "showcase" / "example.json").replace(real_artifact)
        (self.root / "showcase" / "example.json").symlink_to(real_artifact)
        with self.assertRaisesRegex(PublicationBuildError, "artifact_path must not traverse symlinks"):
            build_site(self.root, self.output)

    def test_path_escape_unsupported_kind_and_unsafe_url_fail_closed(self):
        self.entry["artifact_path"] = "showcase/../outside.json"
        self._write_fixture()
        with self.assertRaisesRegex(PublicationBuildError, "unsafe artifact_path"):
            build_site(self.root, self.output)

        self.entry["artifact_path"] = "showcase/example.json"
        self.entry["kind"] = "benchmark"
        self._write_fixture()
        with self.assertRaisesRegex(PublicationBuildError, "does not yet support kind"):
            build_site(self.root, self.output)

        self.entry["kind"] = "work_showcase"
        self.artifact["source"]["revision_url"] = "javascript:alert(1)"
        self._write_fixture()
        with self.assertRaisesRegex(PublicationBuildError, "HTTP\\(S\\)"):
            build_site(self.root, self.output)

    def test_non_finite_metric_and_output_symlink_fail_closed(self):
        build_site(self.root, self.output)
        before = self._snapshot()
        self.artifact["analysis"]["metrics"]["fantlab.general.words"]["value"] = float("nan")
        self._write_fixture()
        with self.assertRaisesRegex(PublicationBuildError, "not finite JSON"):
            build_site(self.root, self.output)
        self.assertEqual(before, self._snapshot(), "failed validation must not refresh output partially")

        self.artifact["analysis"]["metrics"]["fantlab.general.words"]["value"] = 12
        self._write_fixture()
        shutil.rmtree(self.output)
        target = Path(self.temp.name) / "external"
        target.mkdir()
        self.output.parent.mkdir(parents=True, exist_ok=True)
        self.output.symlink_to(target, target_is_directory=True)
        with self.assertRaisesRegex(PublicationBuildError, "must not be a symlink"):
            build_site(self.root, self.output)

    def test_output_must_stay_under_repository_build_tree(self):
        outside = Path(self.temp.name) / "outside-site"
        with self.assertRaisesRegex(PublicationBuildError, "repository build/ tree"):
            build_site(self.root, outside)
        with self.assertRaisesRegex(PublicationBuildError, "repository build/ tree"):
            build_site(self.root, self.root / ".git")

        target = self.root / "valuable"
        target.mkdir()
        link = self.root / "build" / "linked"
        link.parent.mkdir(parents=True, exist_ok=True)
        link.symlink_to(target, target_is_directory=True)
        with self.assertRaisesRegex(PublicationBuildError, "repository build/ tree"):
            build_site(self.root, link / "site")
        self.assertTrue(target.is_dir())

    def test_rebuild_removes_stale_output(self):
        build_site(self.root, self.output)
        stale = self.output / "stale.html"
        stale.write_text("stale", encoding="utf-8")
        build_site(self.root, self.output)
        self.assertFalse(stale.exists())


if __name__ == "__main__":
    unittest.main()
