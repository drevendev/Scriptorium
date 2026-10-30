"""Source-bound two-work author rhythm preview: reproducibility and fail-closed gates."""
from __future__ import annotations

from copy import deepcopy
import json
from pathlib import Path
import unittest

from scriptorium import voice_profile as voice

ROOT = Path(__file__).resolve().parents[1]
SNAPSHOT = ROOT / "assets/evidence-snapshot.json"
DERIVED = ROOT / "assets/voice-preview.json"
SITE = ROOT / "voice/index.html"
WORKFLOW = ROOT / ".github/workflows/pages.yml"
LANDING = ROOT / "index.html"


class AuthorRhythmPreviewTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        raw = SNAPSHOT.read_bytes()
        cls.input = json.loads(raw)
        cls.git_sha = voice._git_blob_sha(raw)
        cls.retained = json.loads(DERIVED.read_text(encoding="utf-8"))

    def build(self, snapshot=None):
        return voice.build_preview(self.input if snapshot is None else snapshot,
                                   source_blob_sha1=self.git_sha)

    def test_derived_artifact_matches_exact_source_snapshot(self):
        self.assertEqual(self.build(), self.retained)
        self.assertEqual(self.retained["source_snapshot_git_blob_sha1"], self.git_sha)
        self.assertEqual(len(self.retained["authors"]), 2)
        self.assertEqual([a["word_weight_total"] for a in self.retained["authors"]],
                         [120850, 405487])
        self.assertEqual([a["work_count"] for a in self.retained["authors"]], [2, 2])
        self.assertEqual([len(a["metrics"]) for a in self.retained["authors"]], [8, 8])
        self.assertEqual([w["key"] for a in self.retained["authors"] for w in a["works"]],
                         ["waves", "road", "anna", "resurrection"])
        self.assertEqual(voice.render_json(self.build()), voice.render_json(self.build()))

    def test_scientific_boundary_is_open_and_all_sources_are_russian(self):
        boundary = self.retained["scientific_boundary"]
        self.assertIs(boundary["m2_parity_admissible"], False)
        self.assertEqual(boundary["m2_source_matched"], 0)
        self.assertIs(boundary["m3_accepted"], False)
        self.assertEqual(boundary["cross_validation"], "NOT_RUN")
        self.assertEqual(boundary["uncertainty"], "ONLY_TWO_WORKS_PER_AUTHOR")
        self.assertIs(boundary["source_text_committed"], False)
        self.assertIs(boundary["translation_mixed"], False)
        self.assertEqual(self.retained["aggregation"]["weight"],
                         "scriptorium_measured_word_count_per_work")
        self.assertIs(self.retained["aggregation"]["not_a_pooled_raw_text_analysis"], True)
        self.assertEqual(self.retained["source_metric_profiles"]["metrics"],
                         "scriptorium-metrics-v4")
        self.assertNotIn("wikitext", DERIVED.read_text(encoding="utf-8").lower())
        self.assertNotIn("literary_text", DERIVED.read_text(encoding="utf-8").lower())
        for author in self.retained["authors"]:
            self.assertEqual(len({w["source_sha256"] for w in author["works"]}), 2)
            for work in author["works"]:
                self.assertGreaterEqual(work["characters_including_spaces"], 300_000)
                self.assertEqual(len(work["source_sha256"]), 64)
                self.assertIn("/blob/master/", work["evidence_url"])

    def test_means_are_word_weighted_not_simple_work_averages(self):
        grin, tolstoy = self.retained["authors"]
        g_dialogue = next(m for m in grin["metrics"] if m["id"] == "fantlab.dialogue.share_percent")
        t_dialogue = next(m for m in tolstoy["metrics"] if m["id"] == "fantlab.dialogue.share_percent")
        self.assertAlmostEqual(g_dialogue["weighted_mean"], 40.963139, places=5)
        self.assertAlmostEqual(g_dialogue["weighted_population_stddev"], 4.697026, places=5)
        self.assertAlmostEqual(t_dialogue["weighted_mean"], 33.245748, places=5)
        self.assertGreater(g_dialogue["weighted_mean"], t_dialogue["weighted_mean"])
        self.assertNotEqual(g_dialogue["weighted_mean"],
                            (35.88986183443132 + 45.31181857828172) / 2)

    def test_negative_rights_source_profiles_and_missing_data(self):
        by_key = {b["key"]: i for i, b in enumerate(self.input["books"])}
        mutations = (
            ("road", lambda b: b.__setitem__("translator", {"name": "unverified"})),
            ("anna", lambda b: b.__setitem__("original_language", "en")),
            ("waves", lambda b: b.__setitem__("source_sha256", "0" * 64)),
            ("resurrection", lambda b: b.__setitem__("edition_id", "different")),
            ("road", lambda b: b["profiles"].__setitem__("metrics", "scriptorium-metrics-v5")),
            ("waves", lambda b: next(m for m in b["metrics"] if m["id"] == "fantlab.general.characters").__setitem__("actual", 299999)),
            ("road", lambda b: next(m for m in b["metrics"] if m["id"] == "fantlab.dialogue.share_percent").__setitem__("actual", None)),
            ("anna", lambda b: next(m for m in b["metrics"] if m["id"] == "fantlab.dialogue.share_percent").__setitem__("actual", 101)),
            ("resurrection", lambda b: b["metrics"].append(deepcopy(b["metrics"][0]))),
        )
        for key, change in mutations:
            with self.subTest(key=key, change=repr(change)):
                corrupt = deepcopy(self.input)
                change(corrupt["books"][by_key[key]])
                with self.assertRaises(ValueError):
                    self.build(corrupt)
        bad = deepcopy(self.input)
        bad["comparability"]["m2_parity_admissible"] = True
        with self.assertRaisesRegex(ValueError, "scientific boundary"):
            self.build(bad)
        with self.assertRaisesRegex(ValueError, "blob identity"):
            voice.build_preview(self.input, source_blob_sha1="not-a-sha")

    def test_static_reader_visible_accessible_and_matches_derived(self):
        html = SITE.read_text(encoding="utf-8")
        landing = LANDING.read_text(encoding="utf-8")
        self.assertIn('<html lang="ru">', html)
        self.assertIn('href="../assets/voice-preview.json"', html)
        self.assertIn('href="../assets/evidence-snapshot.json"', html)
        self.assertIn('href="../assets/pages-reader.css"', html)
        self.assertIn('tabindex="0" role="region"', html)
        self.assertIn('aria-hidden="true"', html)
        self.assertIn("prefers-reduced-motion", html)
        self.assertIn("M2: 0/5", html)
        self.assertIn("M3: открыт", html)
        self.assertIn("Нет перекрёстной проверки", html)
        self.assertNotIn('<script', html)
        self.assertEqual(html.count('class="metric-card"'), 4)
        self.assertEqual(html.count('<tr><th scope="row">'), 8)
        self.assertIn('href="./voice/"', landing)
        for author in self.retained["authors"]:
            self.assertIn(author["display_name"], html)
            for work in author["works"]:
                self.assertIn(work["source_sha256"], html)
            for row in author["metrics"]:
                self.assertIn(f"<td>{row['weighted_mean']:.6f}</td>", html)
                self.assertIn(f"<td>{row['weighted_population_stddev']:.6f}</td>", html)

    def test_preview_artifact_stages_both_local_dependencies(self):
        workflow = WORKFLOW.read_text(encoding="utf-8")
        for path in ("voice/index.html", "assets/voice-preview.json"):
            self.assertIn("cp " + path + " build/branch-root-preview/" + path, workflow)
            self.assertIn("test -s build/branch-root-preview/" + path, workflow)
        self.assertIn('"voice/**"', workflow)
        self.assertIn("python -m scriptorium.voice_profile --check assets/voice-preview.json", workflow)

    def test_cli_rechecks_committed_snapshot(self):
        self.assertEqual(voice.main([
            "--snapshot", str(SNAPSHOT), "--check", str(DERIVED)]), 0)


if __name__ == "__main__":
    unittest.main()
