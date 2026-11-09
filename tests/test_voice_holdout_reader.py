"""Exact-source validation of the public four-fold negative author-rhythm result."""
from __future__ import annotations
from copy import deepcopy
from pathlib import Path
import json
import unittest
from scriptorium import voice_profile, voice_holdout

ROOT = Path(__file__).resolve().parents[1]

class HoldoutReaderTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.html = (ROOT / "voice/index.html").read_text(encoding="utf-8")
        cls.preview = json.loads((ROOT / "assets/voice-preview.json").read_text(encoding="utf-8"))
        cls.holdout = voice_holdout.build_holdout(cls.preview)

    def test_exact_four_folds_have_accessible_numbers_and_common_scale(self):
        self.assertEqual(self.holdout["summary"], {
            "total_folds": 4, "nearer_to_labelled_author": 1,
            "nearer_to_other_author": 3, "ties": 0,
        })
        labels = {"grin": "Грин", "tolstoy": "Толстой"}
        self.assertEqual(self.html.count('data-holdout-card="'), 4)
        self.assertEqual(self.html.count('data-holdout-key="'), 4)
        for fold in self.holdout["folds"]:
            with self.subTest(key=fold["held_out_work_key"]):
                key = fold["held_out_work_key"]
                d = fold["relative_distances"]
                nearest, correct = fold["nearest_author_id"], fold["nearer_to_labelled_author"]
                row = ('<tr data-holdout-key="' + key + '"><th scope="row">'
                       + fold["held_out_work_title"] + '</th><td>'
                       + labels[fold["known_author_id"]] + '</td><td>'
                       + f'{d["grin"]:.6f}' + '</td><td>'
                       + f'{d["tolstoy"]:.6f}' + '</td><td>'
                       + labels[nearest] + '</td><td>'
                       + ("свой" if correct else "другой") + '</td></tr>')
                self.assertIn(row, self.html)
                card = self.html.split('data-holdout-card="' + key + '"')[1].split('</li>', 1)[0]
                self.assertIn("✓ Ближе к своему автору" if correct
                              else "× Ближе к другому автору", card)
                for author, color in (("grin", "emerald"), ("tolstoy", "amber")):
                    width = f'{d[author] / .25 * 100:.2f}%'
                    self.assertIn(f'class="holdout-fill {color}" style="width:{width}"', card)
                    self.assertIn(f'{d[author]:.6f}', card)

    def test_science_accessibility_and_actual_published_route(self):
        h = self.html
        self.assertIn('id="holdout" aria-labelledby="holdout-title"', h)
        self.assertIn('href="#holdout">Проверка</a>', h)
        self.assertIn('href="#holdout">Проверить устойчивость ↘</a>', h)
        self.assertIn('href="../assets/voice-preview.json"', h)
        self.assertIn('role="region" aria-label="Четыре проверки', h)
        self.assertIn('scope="col"', h)
        self.assertIn('aria-hidden="true"', h)
        self.assertIn('prefers-reduced-motion', h)
        self.assertIn('@media print', h)
        self.assertIn('не является вероятностью', h)
        self.assertIn('не независимая внешняя валидация', h)
        self.assertIn('M2: 0/5 · M3: открыт', h)
        self.assertIn(self.holdout["source_snapshot_git_blob_sha1"], h)
        self.assertNotIn("<script", h)
        workflow = (ROOT / ".github/workflows/pages.yml").read_text(encoding="utf-8")
        self.assertIn("cp voice/index.html build/branch-root-preview/voice/index.html", workflow)
        self.assertIn("cmp voice/index.html build/branch-root-preview/voice/index.html", workflow)
        self.assertIn('voice/#holdout', (ROOT / "README.md").read_text(encoding="utf-8"))

    def test_stale_or_forged_evidence_cannot_match_published_distances(self):
        corrupt = deepcopy(self.preview)
        corrupt["authors"][0]["metrics"][0]["per_work"][0]["value"] += 3
        changed = voice_holdout.build_holdout(corrupt)
        self.assertNotEqual(changed["folds"][0]["relative_distances"],
                            self.holdout["folds"][0]["relative_distances"])
        self.assertNotIn(f'{changed["folds"][0]["relative_distances"]["grin"]:.6f}',
                         self.html.split('data-holdout-card="waves"')[1].split('</li>', 1)[0])
        corrupt = deepcopy(self.preview)
        corrupt["scientific_boundary"]["m3_accepted"] = True
        with self.assertRaises(ValueError):
            voice_holdout.build_holdout(corrupt)

    def test_snapshot_rebuild_is_bound_to_exact_published_evidence(self):
        raw = (ROOT / "assets/evidence-snapshot.json").read_bytes()
        rebuilt = voice_profile.build_preview(
            json.loads(raw), source_blob_sha1=voice_profile._git_blob_sha(raw))
        self.assertEqual(rebuilt, self.preview)
        self.assertEqual(voice_holdout.build_holdout(rebuilt), self.holdout)

if __name__ == "__main__":
    unittest.main()
