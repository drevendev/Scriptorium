"""Pinned and accessible feature-removal sensitivity on the public Russian Reader."""
from __future__ import annotations

from copy import deepcopy
import json
from pathlib import Path
import unittest

from scriptorium import voice_ablation, voice_profile

ROOT = Path(__file__).resolve().parents[1]


class SensitivityReaderTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.html = (ROOT / "voice/index.html").read_text(encoding="utf-8")
        cls.preview = json.loads((ROOT / "assets/voice-preview.json").read_text(encoding="utf-8"))
        cls.report = voice_ablation.build_ablation(cls.preview)

    def test_all_rows_and_bar_widths_are_derived_from_pinned_four_books(self):
        self.assertEqual(self.report["baseline_summary"]["nearer_to_labelled_author"], 1)
        self.assertEqual(self.html.count('data-ablation-id="'), 8)
        self.assertEqual(len(self.report["ablations"]), 8)
        for entry in self.report["ablations"]:
            with self.subTest(feature=entry["omitted_feature_id"]):
                correct = entry["summary"]["nearer_to_labelled_author"]
                changed = entry["summary"]["changed_nearest"]
                self.assertEqual(correct + entry["summary"]["nearer_to_other_author"] +
                                 entry["summary"]["ties"], 4)
                self.assertEqual(changed, 1 if correct == 2 else 0)
                row = (
                    '<tr data-ablation-id="' + entry["omitted_feature_id"] + '"'
                    + (' class="sensitivity-highlight"' if changed else '')
                    + '><th scope="row">' + entry["omitted_feature_label"]
                    + '</th><td>' + entry["omitted_feature_unit"]
                    + '</td><td class="sensitivity-result"><span class="sensitivity-track" aria-hidden="true">'
                    + '<span class="sensitivity-fill" style="width:' + str(correct * 25)
                    + '%"></span></span><strong>' + str(correct)
                    + '/4</strong></td><td>' + str(changed) + '</td><td>'
                    + ('«Дорога в никуда»: Толстой → Грин' if changed
                       else 'Ближайший автор не изменился') + '</td></tr>'
                )
                self.assertIn(row, self.html)
        self.assertEqual([r["summary"]["nearer_to_labelled_author"]
                          for r in self.report["ablations"]], [1, 1, 1, 1, 1, 1, 2, 1])
        self.assertEqual(self.report["ablations"][6]["omitted_feature_id"],
                         "fantlab.punctuation.question.per_1000_words")
        self.assertEqual(self.report["ablations"][6]["folds"][1]["held_out_work_key"], "road")
        self.assertTrue(self.report["ablations"][6]["folds"][1]["nearest_changed_from_eight_features"])

    def test_scientific_boundaries_accessibility_and_branch_pages_route(self):
        h = self.html
        self.assertIn('id="sensitivity" aria-labelledby="sensitivity-title"', h)
        self.assertIn('href="#sensitivity">Чувствительность</a>', h)
        self.assertIn('href="#sensitivity">Проверить влияние признаков ↘</a>', h)
        self.assertIn('role="region" tabindex="0" aria-label="Восемь удалённых', h)
        self.assertIn('scope="col"', h)
        self.assertIn('aria-hidden="true"', h)
        self.assertIn('prefers-reduced-motion', h)
        self.assertIn('@media print', h)
        self.assertIn('@media(forced-colors:active)', h)
        self.assertIn("не независимая проверка", h)
        self.assertIn("утечку информации", h)
        self.assertIn("M2: 0/5 · M3: открыт", h)
        self.assertIn(self.report["source_snapshot_git_blob_sha1"], h)
        self.assertIn('scriptorium voice --ablate --format markdown', h)
        self.assertNotIn("<script", h)
        workflow = (ROOT / ".github/workflows/pages.yml").read_text(encoding="utf-8")
        self.assertIn("cmp voice/index.html build/branch-root-preview/voice/index.html", workflow)
        readme = (ROOT / "README.md").read_text(encoding="utf-8")
        self.assertIn("](https://drevendev.github.io/Scriptorium/voice/#sensitivity)", readme)

    def test_rebuild_identity_and_tamper_fail_closed(self):
        raw = (ROOT / "assets/evidence-snapshot.json").read_bytes()
        replay = voice_profile.build_preview(
            json.loads(raw), source_blob_sha1=voice_profile._git_blob_sha(raw))
        self.assertEqual(replay, self.preview)
        self.assertEqual(voice_ablation.build_ablation(replay), self.report)
        damaged = deepcopy(self.preview)
        damaged["scientific_boundary"]["m3_accepted"] = True
        with self.assertRaises(ValueError):
            voice_ablation.build_ablation(damaged)


if __name__ == "__main__":
    unittest.main()
