"""Source-bound six-fold, three-author negative result in the real static Reader.

The public HTML remains a no-JavaScript evidence view. No manuscripts are read
or committed; reconstruct the exact v2 fold distances from pinned measurements.
"""
from __future__ import annotations

from copy import deepcopy
from pathlib import Path
import json
import csv
from io import StringIO
from contextlib import redirect_stdout, redirect_stderr
import unittest

from scriptorium import voice_holdout, voice_profile

ROOT = Path(__file__).resolve().parents[1]
SNAPSHOT = ROOT / "assets/evidence-snapshot.json"
PAGE = ROOT / "voice/index.html"
AUTHORS = {
    "grin": "Грин",
    "tolstoy": "Толстой",
    "dostoevsky": "Достоевский",
}


class ThreeAuthorReaderTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.html = PAGE.read_text(encoding="utf-8")
        cls.raw = SNAPSHOT.read_bytes()
        cls.snapshot = json.loads(cls.raw)
        cls.preview = voice_profile.build_preview(
            cls.snapshot, source_blob_sha1=voice_profile._git_blob_sha(cls.raw),
            include_dostoevsky=True,
        )
        cls.report = voice_holdout.build_holdout(cls.preview)

    def test_six_exact_folds_are_reproduced_as_numeric_table_not_scores(self):
        self.assertEqual(self.report["schema_version"], voice_holdout.EXTENDED_VERSION)
        self.assertEqual(self.report["summary"], {
            "total_folds": 6, "nearer_to_labelled_author": 2,
            "nearer_to_other_author": 4, "ties": 0,
        })
        self.assertEqual(self.html.count('data-three-holdout-key="'), 6)
        books = {b["key"]: b for b in self.snapshot["books"]}
        self.assertEqual(
            [f["held_out_work_key"] for f in self.report["folds"]],
            ["waves", "road", "anna", "resurrection", "karamazov", "humiliated"],
        )
        for fold in self.report["folds"]:
            key = fold["held_out_work_key"]
            with self.subTest(edition=key):
                row = self.html.split('<tr data-three-holdout-key="' + key + '">', 1)[1].split("</tr>", 1)[0]
                self.assertIn('<a href="' + books[key]["evidence_url"] + '">', row)
                self.assertIn(fold["held_out_work_title"], row)
                self.assertIn("<td>" + AUTHORS[fold["known_author_id"]] + "</td>", row)
                for aid in AUTHORS:
                    self.assertIn("<td>" + f'{fold["relative_distances"][aid]:.6f}' + "</td>", row)
                self.assertIn(
                    "<td>" + AUTHORS[fold["nearest_author_id"]] + "</td>", row
                )
                self.assertIn(
                    'data-outcome="' + ("same" if fold["nearer_to_labelled_author"] else "other") + '">',
                    row,
                )
                self.assertIn("✓ Свой" if fold["nearer_to_labelled_author"] else "× Другой", row)

    def test_accessibility_navigation_methods_and_scientific_boundary(self):
        h = self.html
        self.assertIn('id="holdout-three" aria-labelledby="holdout-three-title"', h)
        self.assertIn('href="#holdout-three">Три автора</a>', h)
        self.assertIn('href="#holdout-three">Проверить на трёх авторах ↘</a>', h)
        self.assertIn('role="region" tabindex="0" aria-label="Шесть исключённых книг:', h)
        self.assertIn("Меньше — ближе, но не вероятность", h)
        self.assertIn("не независимая внешняя валидация", h)
        self.assertIn("M2: 0/5 · M3: открыт", h)
        self.assertIn('href="../assets/evidence-snapshot.json"', h)
        self.assertIn(self.report["source_snapshot_git_blob_sha1"], h)
        self.assertIn("scriptorium voice --include-dostoevsky --holdout --format markdown", h)
        self.assertIn("2 из 6", h)
        self.assertIn("4 из 6", h)
        self.assertIn("@media print", h)
        self.assertIn("@media(forced-colors:active)", h)
        self.assertNotIn("<script", h)
        self.assertIn('data-holdout-card="waves"', h)  # original v1 untouched
        self.assertIn("Только 1 из 4 исключённых книг", h)
        wf = (ROOT / ".github/workflows/pages.yml").read_text(encoding="utf-8")
        self.assertIn("cp voice/index.html build/branch-root-preview/voice/index.html", wf)
        self.assertIn("cmp voice/index.html build/branch-root-preview/voice/index.html", wf)
        readme = (ROOT / "README.md").read_text(encoding="utf-8")
        self.assertIn("](https://drevendev.github.io/Scriptorium/voice/#holdout-three)", readme)

    def test_forged_aggregates_and_source_boundaries_fail_closed(self):
        tampered = deepcopy(self.preview)
        tampered["authors"][2]["metrics"][0]["weighted_mean"] += 0.1
        with self.assertRaisesRegex(ValueError, "inconsistent source-bound author aggregate"):
            voice_holdout.build_holdout(tampered)
        tampered = deepcopy(self.preview)
        tampered["scientific_boundary"]["m3_accepted"] = True
        with self.assertRaises(ValueError):
            voice_holdout.build_holdout(tampered)


    def test_downloadable_csv_matches_exact_folds_and_cli(self):
        from scriptorium import cli
        content = (ROOT / "voice/holdout-three.csv").read_text(encoding="utf-8")
        self.assertEqual(content, voice_holdout.render_csv(self.report))
        rows = list(csv.DictReader(StringIO(content)))
        self.assertEqual(len(rows), 6)
        self.assertEqual([row["held_out_work_key"] for row in rows],
                         ["waves", "road", "anna", "resurrection", "karamazov", "humiliated"])
        for row, fold in zip(rows, self.report["folds"]):
            with self.subTest(work=row["held_out_work_key"]):
                self.assertEqual(row["schema_version"], voice_holdout.EXTENDED_VERSION)
                self.assertEqual(row["source_snapshot_git_blob_sha1"],
                                 self.report["source_snapshot_git_blob_sha1"])
                self.assertEqual(row["distance_unit"], "dimensionless")
                self.assertEqual(row["evidence_scope"], "in_sample_diagnostic")
                self.assertEqual(row["held_out_work_title"], fold["held_out_work_title"])
                for author_id in AUTHORS:
                    self.assertEqual(row["distance_to_" + author_id],
                                     f'{fold["relative_distances"][author_id]:.6f}')
        self.assertEqual(sum(row["nearest_author_outcome"] == "same" for row in rows), 2)
        self.assertEqual(sum(row["nearest_author_outcome"] == "other" for row in rows), 4)
        self.assertIn('href="holdout-three.csv"', self.html)
        workflow = (ROOT / ".github/workflows/pages.yml").read_text(encoding="utf-8")
        self.assertIn("cp voice/holdout-three.csv build/branch-root-preview/voice/holdout-three.csv",
                      workflow)
        self.assertIn("cmp voice/holdout-three.csv build/branch-root-preview/voice/holdout-three.csv",
                      workflow)
        with redirect_stdout(output := StringIO()):
            self.assertEqual(cli.main(["voice", "--include-dostoevsky", "--holdout",
                                       "--format", "csv"]), 0)
        self.assertEqual(output.getvalue(), content)

    def test_csv_rejects_misleading_or_unsafe_artifacts(self):
        old = voice_profile.build_preview(
            self.snapshot, source_blob_sha1=self.report["source_snapshot_git_blob_sha1"])
        with self.assertRaisesRegex(ValueError, "CSV scientific boundary"):
            voice_holdout.render_csv(voice_holdout.build_holdout(old))
        for field, value in (("m3_accepted", True), ("independent_external_validation", True)):
            broken = deepcopy(self.report)
            broken["scientific_boundary"][field] = value
            with self.subTest(field=field), self.assertRaises(ValueError):
                voice_holdout.render_csv(broken)
        broken = deepcopy(self.report)
        broken["folds"][0]["nearer_to_labelled_author"] = True
        with self.assertRaisesRegex(ValueError, "contradictory"):
            voice_holdout.render_csv(broken)
        broken = deepcopy(self.report)
        broken["folds"][0]["held_out_work_title"] = "=HYPERLINK(1)"
        with self.assertRaisesRegex(ValueError, "invalid six-fold CSV row"):
            voice_holdout.render_csv(broken)
        broken = deepcopy(self.report)
        broken["summary"]["nearer_to_labelled_author"] += 1
        with self.assertRaisesRegex(ValueError, "summary contradicts"):
            voice_holdout.render_csv(broken)
        from scriptorium import cli
        with redirect_stderr(stderr := StringIO()), self.assertRaises(SystemExit) as exc:
            cli.main(["voice", "--format", "csv"])
        self.assertEqual(exc.exception.code, 2)
        self.assertIn("CSV export requires", stderr.getvalue())


if __name__ == "__main__":
    unittest.main()
