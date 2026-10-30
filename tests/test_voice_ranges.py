"""Verify the source-bound observed-book ranges and non-inferential visualization."""
from __future__ import annotations

import json
from pathlib import Path
import re
import unittest

from scriptorium import voice_profile

ROOT = Path(__file__).resolve().parents[1]
SITE = ROOT / "voice/index.html"
DATA = ROOT / "assets/voice-preview.json"
SNAPSHOT = ROOT / "assets/evidence-snapshot.json"


class ObservedRangeTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.html = SITE.read_text(encoding="utf-8")
        cls.report = json.loads(DATA.read_text(encoding="utf-8"))

    def test_ranges_are_exactly_derived_from_32_pinned_work_observations(self):
        a, b = self.report["authors"]
        self.assertEqual([x["author_id"] for x in (a, b)], ["grin", "tolstoy"])
        self.assertEqual(len(a["metrics"]), len(b["metrics"]))
        self.assertEqual(len(a["metrics"]), 8)
        overlapping = 0
        for left, right in zip(a["metrics"], b["metrics"]):
            self.assertEqual((left["id"], left["unit"]), (right["id"], right["unit"]))
            gv = [x["value"] for x in left["per_work"]]
            tv = [x["value"] for x in right["per_work"]]
            self.assertEqual((len(gv), len(tv)), (2, 2))
            glo, ghi = min(gv), max(gv)
            tlo, thi = min(tv), max(tv)
            intersects = glo <= thi and tlo <= ghi
            overlapping += intersects
            row = ('<tr data-range-id="' + left["id"] + '"><th scope="row">' +
                   left["label"] + '</th><td>' + left["unit"] + '</td><td>' +
                   f'{glo:.6f}–{ghi:.6f}' + '</td><td>' +
                   f'{tlo:.6f}–{thi:.6f}' + '</td><td>' +
                   ("пересекаются" if intersects else "не пересекаются") + '</td></tr>')
            self.assertIn(row, self.html)
        self.assertEqual(overlapping, 4)
        self.assertEqual(self.html.count('<tr data-range-id="'), 8)
        self.assertIn("4 показателя с пересечением, 4 — без пересечения.", self.html)

    def test_two_range_plots_have_exact_pinned_geometry(self):
        a, b = self.report["authors"]
        for index in (2, 5):
            left, right = a["metrics"][index], b["metrics"][index]
            left_values = [x["value"] for x in left["per_work"]]
            right_values = [x["value"] for x in right["per_work"]]
            minimum = min(*left_values, *right_values)
            maximum = max(*left_values, *right_values)
            width = maximum - minimum
            self.assertGreater(width, 0)
            start = self.html.index('data-range-card="' + left["id"] + '"')
            end = self.html.index('</li>', start)
            card = self.html[start:end]
            for values, name in ((left_values, "emerald"), (right_values, "amber")):
                low, high = min(values), max(values)
                geometry = (f'class="range-span {name}" style="left:'
                            f'{100 * (low - minimum) / width:.2f}%;width:'
                            f'{100 * (high - low) / width:.2f}%"')
                self.assertIn(geometry, card)
                self.assertIn(f'{low:.6f}–{high:.6f}', card)
        self.assertEqual(self.html.count('data-range-card="'), 2)

    def test_boundary_accessibility_and_reproducibility(self):
        self.assertIn('id="ranges" aria-labelledby="ranges-title"', self.html)
        self.assertIn('href="#ranges">Диапазоны</a>', self.html)
        self.assertIn('role="region" aria-label="Полная таблица', self.html)
        self.assertIn('scope="col"', self.html)
        self.assertIn('aria-hidden="true"', self.html)
        self.assertIn('prefers-reduced-motion', self.html)
        self.assertIn("Диапазон не является доверительным интервалом", self.html)
        self.assertIn("не доказывает устойчивого авторского различия", self.html)
        self.assertIn("M3 не подтверждены", self.html)
        self.assertNotIn("<script", self.html)
        raw = SNAPSHOT.read_bytes()
        replay = voice_profile.build_preview(
            json.loads(raw), source_blob_sha1=voice_profile._git_blob_sha(raw))
        self.assertEqual(replay, self.report)

    def test_tampered_observation_does_not_match_public_range(self):
        damaged = json.loads(DATA.read_text(encoding="utf-8"))
        damaged["authors"][0]["metrics"][2]["per_work"][0]["value"] += 100
        actual = damaged["authors"][0]["metrics"][2]["per_work"]
        changed = f'{min(row["value"] for row in actual):.6f}–{max(row["value"] for row in actual):.6f}'
        self.assertNotIn(changed, self.html)


if __name__ == "__main__":
    unittest.main()
