"""Repin-aware regression for public gallery display/source unit contracts (#286).

Synthetic source-free records intentionally use freshly recomputed Git blob pins; a
checksum-only test would not detect a wrong unit in approved replacement evidence.
"""
from __future__ import annotations

import hashlib
import json
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch

from scriptorium import full_work_gallery as gallery


UNITS = {
    "characters": "characters",
    "words": "words",
    "characters/word": "characters/word",
    "characters/sentence": "characters/sentence",
    "%": "percent",
    "types": "words",
    "per 1,000 words": "occurrences/1000_words",
}


class RepinnedUnitContractTests(unittest.TestCase):
    def setUp(self):
        temporary = tempfile.TemporaryDirectory()
        self.addCleanup(temporary.cleanup)
        self.root = Path(temporary.name)
        self.docs = [self._doc(index) for index in range(2)]
        self._refresh_pins()

    @staticmethod
    def _doc(index):
        candidate = gallery.SOURCES[index][0]
        body_count = 363819 if index == 0 else 1095467
        values = {
            "fantlab.general.characters": body_count,
            "fantlab.general.words": 55778 if index == 0 else 158881,
            "fantlab.general.mean_word_length_chars": 5.15,
            "fantlab.general.mean_sentence_length_chars": 73.8,
            "fantlab.dialogue.share_percent": 35.5,
            "fantlab.dialogue.author_text_inside_dialogue_percent": 26.4,
            "fantlab.vocabulary.unique_words": 14406 if index == 0 else 29084,
            "fantlab.punctuation.comma.per_1000_words": 100.1,
            "fantlab.punctuation.dash.per_1000_words": 40.2,
            "fantlab.punctuation.question.per_1000_words": 4.3,
        }
        metrics = []
        for mid, _, display_unit, _ in gallery.METRICS:
            row = {"metric_id": mid}
            if index == 0:
                row.update(status="diagnostic_only_source_unmatched", scriptorium_raw_value=values[mid])
            else:
                row.update(compatibility_status="inferred", value=values[mid], unit=UNITS[display_unit])
            metrics.append(row)
        base = {
            "candidate_id": candidate,
            "source_text_committed": False,
            "body_identity": {"character_count_including_spaces": body_count, "raw_sha256": "a" * 64},
            "gates": {
                "fantlab_source_edition_match": "unknown",
                "m2_parity_admissible": False,
                "m2_weight": 0,
                "gate_ready": False,
            },
            "scriptorium": {"profiles": {
                "metrics": "scriptorium-metrics-v4", "normalization": "scriptorium-text-v1",
                "dialogue": "scriptorium-dialogue-v1", "vocabulary": "scriptorium-vocabulary-v1",
                "punctuation": "scriptorium-punctuation-v2",
            }},
            "metrics": metrics,
        }
        if index == 0:
            base.update(comparison_policy={"class": "diagnostic_unmatched_source"},
                        fantlab={"source_edition_disclosed": False, "source_bytes_disclosed": False})
        else:
            base.update(translation_identity="Alexandra A. Beketova Russian translation",
                        interpretation={"fantlab_comparison_performed": False})
        return base

    def _refresh_pins(self):
        specs = list(gallery.SOURCES)
        for index, doc in enumerate(self.docs):
            path = self.root / "corpus/candidates/diagnostics" / (specs[index][0] + ".json")
            path.parent.mkdir(parents=True, exist_ok=True)
            raw = (json.dumps(doc, sort_keys=True, ensure_ascii=False, indent=2) + "\n").encode("utf-8")
            path.write_bytes(raw)
            updated = list(specs[index])
            updated[1] = hashlib.sha1(b"blob " + str(len(raw)).encode("ascii") + b"\0" + raw).hexdigest()
            specs[index] = tuple(updated)
        return tuple(specs)

    def _load(self):
        with patch.object(gallery, "SOURCES", self._refresh_pins()):
            return gallery.load_gallery(self.root)

    def _edit_beketova_unit(self, display_unit, replacement):
        metric_id = next(mid for mid, _, label, _ in gallery.METRICS if label == display_unit)
        next(row for row in self.docs[1]["metrics"] if row["metric_id"] == metric_id)["unit"] = replacement

    def test_all_ten_display_units_accept_compatible_derived_source_units(self):
        left, right = self._load()
        self.assertEqual(len(gallery.METRICS), 10)
        self.assertEqual(left["body"], 363819)
        self.assertEqual(right["body"], 1095467)
        self.assertEqual(len(gallery.render_csv((left, right)).splitlines()), 21)
        self.assertEqual(gallery.render_html((left, right)).count("<li><h3>"), 7)
        self.assertTrue(all("unit" not in row for row in self.docs[0]["metrics"]))

    def test_canonical_frozen_records_retain_exact_metrics_and_units(self):
        root = Path(__file__).resolve().parents[1]
        records = gallery.load_gallery(root)
        self.assertEqual([record["body"] for record in records], [363819, 1095467])
        self.assertEqual(len(gallery.METRICS), 10)
        self.assertEqual(len(gallery.render_csv(records).splitlines()), 21)
        page = gallery.render_html(records)
        self.assertEqual(page.count("<li><h3>"), 7)
        self.assertIn("nav a,.actions a{display:inline-flex;align-items:center;min-height:44px", page)
        self.assertIn("summary:focus-visible", page)
        self.assertIn("prefers-reduced-motion", page)
        self.assertIn("M2 0/5", page)

    def test_percent_to_ratio_repin_is_rejected(self):
        self._edit_beketova_unit("%", "ratio")
        with self.assertRaisesRegex(gallery.GalleryError, "source unit"):
            self._load()

    def test_per_thousand_rate_changed_to_words_repin_is_rejected(self):
        self._edit_beketova_unit("per 1,000 words", "words")
        with self.assertRaisesRegex(gallery.GalleryError, "source unit"):
            self._load()

    def test_cardinal_unit_changed_to_percent_repin_is_rejected(self):
        self._edit_beketova_unit("characters", "percent")
        with self.assertRaisesRegex(gallery.GalleryError, "source unit"):
            self._load()

    def test_unique_word_forms_use_source_words_not_display_types(self):
        self._edit_beketova_unit("types", "types")
        with self.assertRaisesRegex(gallery.GalleryError, "source unit"):
            self._load()

    def test_missing_null_and_nonnumeric_unit_fail_closed(self):
        for invalid in (None, 100, [], {}):
            with self.subTest(invalid=invalid):
                self._edit_beketova_unit("characters/word", invalid)
                with self.assertRaisesRegex(gallery.GalleryError, "source unit"):
                    self._load()

    def test_repin_does_not_silently_upgrade_scientific_status(self):
        self.docs[1]["gates"]["m2_weight"] = 1
        with self.assertRaisesRegex(gallery.GalleryError, "scientific gate"):
            self._load()

    def test_pins_are_still_mandatory(self):
        specs = self._refresh_pins()
        target = self.root / "corpus/candidates/diagnostics" / (specs[1][0] + ".json")
        target.write_bytes(target.read_bytes() + b" ")
        with patch.object(gallery, "SOURCES", specs), self.assertRaisesRegex(gallery.GalleryError, "checksum"):
            gallery.load_gallery(self.root)


if __name__ == "__main__":
    unittest.main()
