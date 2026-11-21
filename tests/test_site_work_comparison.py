"""Positive/negative tests on real pinned, source-free derived evidence."""
from __future__ import annotations

from decimal import Decimal

import copy
import hashlib
import json
import os
from pathlib import Path
import shutil
import tempfile
import unittest

from scriptorium import site_work_comparison as subject

REPO = Path(__file__).resolve().parents[1]


class FrozenComparisonPublicationTests(unittest.TestCase):
    def test_real_pinned_build_and_exact_metric_units(self):
        rendered = subject.build(REPO)
        data = json.loads(rendered["json"])
        self.assertEqual(len(data["measurements"]), 10)
        self.assertEqual(data["scientific_boundary"]["m2_weight"], 0)
        self.assertFalse(data["scientific_boundary"]["m2_parity_admissible"])
        self.assertEqual(data["works"][0]["characters_including_spaces"], 363819)
        self.assertEqual(data["works"][1]["characters_including_spaces"], 1095467)
        self.assertEqual(data["works"][1]["author_or_translator"],
                         "Jules Verne · Alexandra Beketova translation")
        metrics = {row["metric_id"]: row for row in data["measurements"]}
        self.assertEqual(metrics["fantlab.dialogue.share_percent"]["difference_unit"], "percentage points")
        self.assertEqual(metrics["fantlab.general.words"]["difference_unit"], "words")
        self.assertIn("right_minus_left", rendered["json"])


    def test_visible_signed_differences_match_exact_json_without_export_drift(self):
        rendered = subject.build(REPO)
        page = rendered["html"]
        metrics = json.loads(rendered["json"])["measurements"]
        self.assertIn("id='signed-differences'", page)
        self.assertIn("правая книга минус левая", page)
        self.assertIn("процентных пунктах", page)
        self.assertEqual(page.count("data-metric-id='"), 7)
        for item in metrics:
            marker = "data-metric-id='" + item["metric_id"] + "'"
            if not item["normalized_for_visual_comparison"]:
                self.assertNotIn(marker, page)
                continue
            self.assertIn(marker, page)
            value = item["right_minus_left_decimal"]
            signed = ("+" if Decimal(value) > 0 else "") + value
            self.assertIn(">" + signed + " " + subject._RU_UNITS[item["difference_unit"]] + "</td>", page)
        self.assertNotIn("data-metric-id='fantlab.general.characters'", page)
        self.assertIn("right_minus_left", rendered["json"])
        from scriptorium import full_work_gallery
        self.assertEqual(rendered["csv"], full_work_gallery.render_csv(
            full_work_gallery.load_gallery(REPO)
        ))

    def test_standalone_comparison_explains_every_metric_via_real_guide(self):
        page = subject.build(REPO)["html"]
        guide = (REPO / "metrics.html").read_text(encoding="utf-8")
        self.assertEqual(page.count(f"href='{subject.GUIDE_URL}'>"), 1)
        self.assertIn(f"href='{subject.GUIDE_URL}'>Как читать показатели</a>", page)
        total = 0
        for metric_id, _, _, normalized in subject.gallery.METRICS:
            anchor = f"metric-{metric_id}"
            self.assertIn(f'id="{anchor}"', guide)  # no broken methodology links
            count = 3 if normalized else 1  # rate chart + exact + signed table
            self.assertEqual(page.count(f"href='{subject.GUIDE_URL}#{anchor}'"), count)
            self.assertEqual(
                page.count(f"aria-label='Методика: {subject.METRIC_LABELS_RU[metric_id]}'"),
                count,
            )
            total += count
        self.assertEqual(total, 24)
        self.assertEqual(page.count(f"href='{subject.GUIDE_URL}#metric-"), total)
        self.assertNotIn("<script", page)
        # Source-derived canonical downloads must remain byte-for-byte unchanged.
        from scriptorium import full_work_gallery
        self.assertEqual(subject.build(REPO)["csv"],
                         full_work_gallery.render_csv(full_work_gallery.load_gallery(REPO)))

    def test_missing_russian_glossary_label_fails_closed(self):
        from unittest.mock import patch
        labels = {**subject.METRIC_LABELS_RU, "fantlab.general.words": ""}
        with patch.object(subject, "METRIC_LABELS_RU", labels):
            with self.assertRaisesRegex(subject.ComparisonBuildError, "label or unit"):
                subject.build(REPO)

    def test_russian_pinned_reader_has_one_language_and_reviewed_units(self):
        rendered = subject.build(REPO)
        page = rendered["html"]
        self.assertIn("<html lang='ru'>", page)
        self.assertIn("Две книги. Разный ритм.", page)
        self.assertIn("«Бегущая по волнам»", page)
        self.assertIn("«Дети капитана Гранта»", page)
        self.assertIn("перевод А. А. Бекетовой", page)
        self.assertIn("Научная граница: M2 — 0/5", page)
        self.assertIn("Семь измерений с разностями со знаком", page)
        self.assertIn("href='measurements.json'", page)
        self.assertIn("Скачать таблицу метрик (CSV)", page)
        self.assertIn("<nav aria-label='Навигация по результатам'>", page)
        self.assertEqual(page.count("<nav "), 1)
        self.assertNotIn("aria-label='Reader navigation'", page)
        self.assertEqual(page.count("<th scope='row'>"), 17)
        self.assertEqual(page.count("<h3>"), 7)
        for metric_id, _, unit, normalized in subject.gallery.METRICS:
            label = subject.METRIC_LABELS_RU[metric_id]
            pretty_unit = subject._RU_UNITS[unit]
            self.assertEqual(
                page.count(f"{label} <small>{pretty_unit}</small>"),
                3 if normalized else 1,
            )
        for english in ("Two books. Different rhythms.",
                        "No manuscript text", "Seven normalized measures",
                        "Observed differences", "Percentage points"):
            self.assertNotIn(english, page)
        self.assertNotIn("<script", page)
        # Human copy changes only: stable machine and CSV contracts.
        data = json.loads(rendered["json"])
        self.assertEqual(data["schema_version"], "scriptorium-work-comparison-export-v1")
        self.assertEqual(data["measurements"][0]["label"], "Characters including spaces")
        self.assertIn("Characters including spaces", rendered["csv"])

    def test_russian_reader_refuses_unexpected_gallery_markup(self):
        with self.assertRaisesRegex(subject.ComparisonBuildError, "drift"):
            subject._russian_reader_html("<html lang='en'></html>")

    def test_signed_differences_refuse_unexpected_metric_coverage(self):
        with self.assertRaises(subject.ComparisonBuildError):
            subject._render_signed_differences([])

    def test_links_accessibility_and_no_scripts(self):
        page = subject.build(REPO)["html"]
        for piece in ("href='../../'", "href='measurements.json'",
                      "href='measurements.csv'", "href='#main'", "<table>",
                      "Сами произведения здесь не опубликованы"):
            self.assertIn(piece, page)
        self.assertNotIn("<script", page)

    def test_replay_and_input_digests(self):
        first = subject.build(REPO)
        self.assertEqual(first, subject.build(REPO))
        self.assertEqual(len(first["input_artifacts"]), 2)
        for row in first["input_artifacts"]:
            self.assertEqual(hashlib.sha256((REPO / row["path"]).read_bytes()).hexdigest(), row["sha256"])
        self.assertIn("fantlab.general.words", first["csv"])

    def test_strict_manifest_registration(self):
        subject.validate_entry(copy.deepcopy(subject.EXPECTED_ENTRY))
        for key, value in (("kind", "work_showcase"), ("compatibility_claim", "reproduced"),
                           ("corpus_admissibility", "admissible"), ("source_text_included", True),
                           ("artifact_paths", ["corpus/candidates/diagnostics/other.json"])):
            with self.subTest(key=key):
                modified = copy.deepcopy(subject.EXPECTED_ENTRY)
                modified[key] = value
                with self.assertRaises(subject.ComparisonBuildError):
                    subject.validate_entry(modified)
        with self.assertRaises(subject.ComparisonBuildError):
            subject.validate_entry({**subject.EXPECTED_ENTRY, "surprise": "new"})

    def test_tampering_rejected_without_private_paths(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            for rel in subject.SOURCE_PATHS:
                path = root / rel
                path.parent.mkdir(parents=True, exist_ok=True)
                shutil.copyfile(REPO / rel, path)
            self.assertTrue(subject.build(root)["json"])
            tampered = root / subject.SOURCE_PATHS[0]
            tampered.write_bytes(tampered.read_bytes() + b" ")
            with self.assertRaises(subject.ComparisonBuildError) as raised:
                subject.build(root)
            self.assertNotIn(directory, str(raised.exception))

    @unittest.skipUnless(hasattr(os, "mkfifo"), "requires FIFO support")
    def test_nonblocking_source_validation(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            for rel in subject.SOURCE_PATHS:
                path = root / rel
                path.parent.mkdir(parents=True, exist_ok=True)
                shutil.copyfile(REPO / rel, path)
            fifo = root / subject.SOURCE_PATHS[0]
            fifo.unlink()
            os.mkfifo(fifo)
            with self.assertRaises(subject.ComparisonBuildError):
                subject.build(root)


if __name__ == "__main__":
    unittest.main()
