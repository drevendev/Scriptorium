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

    def test_manifest_contract_and_artifact_schema_fail_closed(self):
        manifest = self._manifest()
        manifest["unexpected"] = True
        (self.root / "site" / "publication-manifest.json").write_text(
            json.dumps(manifest, ensure_ascii=False), encoding="utf-8"
        )
        with self.assertRaisesRegex(PublicationBuildError, "publication manifest has invalid keys"):
            build_site(self.root, self.output)

        self.entry["unexpected"] = "not in publication-manifest-v1"
        self._write_fixture()
        with self.assertRaisesRegex(PublicationBuildError, "manifest entry example-v1 has invalid keys"):
            build_site(self.root, self.output)
        self.entry.pop("unexpected")

        self.entry["artifact_schema"] = "scriptorium-unknown-v999"
        self.artifact["analysis"]["schema_version"] = "scriptorium-unknown-v999"
        self._write_fixture()
        with self.assertRaisesRegex(PublicationBuildError, "artifact_schema has unsupported value"):
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


    def test_mid_write_failure_preserves_previous_build(self):
        from unittest.mock import patch
        build_site(self.root, self.output)
        before = self._snapshot()
        original_write = Path.write_text

        def fail_receipt(path, *args, **kwargs):
            if path.name == "build.json":
                raise OSError("injected receipt write failure")
            return original_write(path, *args, **kwargs)

        with patch.object(Path, "write_text", fail_receipt):
            with self.assertRaisesRegex(PublicationBuildError, "atomic site publication failed"):
                build_site(self.root, self.output)
        self.assertEqual(before, self._snapshot())


    def _use_current_engine_fixture(self):
        from scriptorium.metrics import analyze_deterministic_metrics

        self.entry["artifact_schema"] = "scriptorium-deterministic-metrics-v4"
        self.artifact["analysis"] = analyze_deterministic_metrics(
            "Солнце взошло. — Здравствуй! Как дела?"
        )
        self._write_fixture()

    def test_current_v4_engine_artifact_publishes_deterministically_without_source(self):
        self._use_current_engine_fixture()
        first = build_site(self.root, self.output)
        snapshot = self._snapshot()
        self.assertEqual(first, build_site(self.root, self.output))
        self.assertEqual(snapshot, self._snapshot())
        page = (self.output / "works" / "example" / "index.html").read_text("utf-8")
        self.assertIn("fantlab.vocabulary.unique_words", page)
        self.assertIn("fantlab.punctuation.question.per_1000_words", page)
        self.assertNotIn("SECRET SOURCE PROSE", page)
        self.assertEqual(len(self.artifact["analysis"]["metrics"]), 29)

    def test_retained_v3_shape_requires_its_own_frozen_profiles(self):
        # Structural v3 fixture, not a claim that v4-generated counts are v3 measurements.
        self._use_current_engine_fixture()
        analysis = self.artifact["analysis"]
        self.entry["artifact_schema"] = analysis["schema_version"] = (
            "scriptorium-deterministic-metrics-v3"
        )
        analysis["profiles"]["metrics"] = "scriptorium-metrics-v3"
        analysis["profiles"]["punctuation"] = "scriptorium-punctuation-v1"
        self._write_fixture()
        build_site(self.root, self.output)
        self.assertTrue((self.output / "works" / "example" / "index.html").is_file())
        analysis["profiles"]["punctuation"] = "scriptorium-punctuation-v2"
        self._write_fixture()
        with self.assertRaisesRegex(PublicationBuildError, "metric profile identity"):
            build_site(self.root, self.output)

    def test_current_artifact_malformed_fields_fail_without_partial_publication(self):
        self._use_current_engine_fixture()
        build_site(self.root, self.output)
        pristine = self._snapshot()
        baseline = copy.deepcopy(self.artifact)
        cases = (
            ("wrong contract", lambda a: a["analysis"].__setitem__("metric_contract_id", "unreviewed")),
            ("wrong metric profile", lambda a: a["analysis"]["profiles"].__setitem__("metrics", "scriptorium-metrics-v1")),
            ("wrong punctuation profile", lambda a: a["analysis"]["profiles"].__setitem__("punctuation", "scriptorium-punctuation-v1")),
            ("extra analysis field", lambda a: a["analysis"].__setitem__("source_text", "PRIVATE MANUSCRIPT")),
            ("unknown metric", lambda a: a["analysis"]["metrics"].__setitem__("fabricated", {"value": 1})),
            ("missing metric", lambda a: a["analysis"]["metrics"].pop("fantlab.general.words")),
            ("false evidence", lambda a: a["analysis"]["metrics"]["fantlab.general.words"].__setitem__("compatibility_status", "reproduced")),
            ("wrong unit", lambda a: a["analysis"]["metrics"]["fantlab.general.words"].__setitem__("unit", "percent")),
            ("punctuation raw count", lambda a: a["analysis"]["metrics"]["fantlab.punctuation.question.per_1000_words"].__setitem__("raw_count", True)),
            ("boolean value", lambda a: a["analysis"]["metrics"]["fantlab.general.words"].__setitem__("value", True)),
            ("bad digest", lambda a: a["analysis"].__setitem__("normalized_sha256", "not-a-digest")),
            ("unbound dictionary", lambda a: a["analysis"]["metrics"]["fantlab.vocabulary.active_dictionary"].__setitem__("value", 9)),
        )
        for label, mutate in cases:
            with self.subTest(label=label):
                self.artifact = copy.deepcopy(baseline)
                mutate(self.artifact)
                self._write_fixture()
                with self.assertRaises(PublicationBuildError):
                    build_site(self.root, self.output)
                self.assertEqual(pristine, self._snapshot())

    def test_current_schema_mismatch_and_private_flag_fail_closed(self):
        self._use_current_engine_fixture()
        self.artifact["analysis"]["schema_version"] = "scriptorium-deterministic-metrics-v3"
        self._write_fixture()
        with self.assertRaisesRegex(PublicationBuildError, "artifact_schema"):
            build_site(self.root, self.output)
        self.artifact["analysis"]["schema_version"] = "scriptorium-deterministic-metrics-v4"
        self.artifact["source"]["source_text_committed"] = True
        self._write_fixture()
        with self.assertRaisesRegex(PublicationBuildError, "source text"):
            build_site(self.root, self.output)


if __name__ == "__main__":
    unittest.main()
