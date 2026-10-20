"""Reject inconsistent count metrics and algorithm profiles in frozen literary comparisons.

The fixtures mutate source-free derived JSON and recompute its Git blob pin so tests
exercise the scientific invariants rather than mere checksum rejection.
"""
from __future__ import annotations

import hashlib
import json
from pathlib import Path
import shutil
import tempfile
import unittest
from unittest.mock import patch

from scriptorium import full_work_gallery as gallery


class FrozenGalleryEvidenceContract(unittest.TestCase):
    def setUp(self):
        temp = tempfile.TemporaryDirectory()
        self.addCleanup(temp.cleanup)
        self.root = Path(temp.name)
        source = Path(__file__).resolve().parents[1]
        for candidate, *_ in gallery.SOURCES:
            relative = Path("corpus/candidates/diagnostics") / f"{candidate}.json"
            (self.root / relative).parent.mkdir(parents=True, exist_ok=True)
            shutil.copyfile(source / relative, self.root / relative)

    def repin(self, index, edit):
        specs = list(gallery.SOURCES)
        spec = list(specs[index])
        path = self.root / "corpus/candidates/diagnostics" / f"{spec[0]}.json"
        doc = json.loads(path.read_text(encoding="utf-8"))
        edit(doc)
        data = (json.dumps(doc, ensure_ascii=False, indent=2) + "\n").encode("utf-8")
        path.write_bytes(data)
        spec[1] = hashlib.sha1(b"blob " + str(len(data)).encode() + b"\0" + data).hexdigest()
        specs[index] = tuple(spec)
        return tuple(specs)

    def test_frozen_records_have_valid_counts_and_five_matching_profiles(self):
        left, right = gallery.load_gallery(self.root)
        self.assertEqual(len(left["profiles"]), 5)
        self.assertEqual(left["profiles"], right["profiles"])
        for record in (left, right):
            self.assertLessEqual(record["values"]["fantlab.general.words"], record["body"])
            for mid in ("fantlab.general.characters", "fantlab.general.words", "fantlab.vocabulary.unique_words"):
                self.assertIs(type(record["values"][mid]), int)

    def test_fractional_count_is_rejected_after_repin(self):
        specs = self.repin(0, lambda doc: next(row for row in doc["metrics"] if row["metric_id"] == "fantlab.general.words").update(scriptorium_raw_value=55778.5))
        with patch.object(gallery, "SOURCES", specs), self.assertRaisesRegex(gallery.GalleryError, "cardinal measurement"):
            gallery.load_gallery(self.root)

    def test_integer_looking_float_is_not_an_integer_count(self):
        specs = self.repin(1, lambda doc: next(row for row in doc["metrics"] if row["metric_id"] == "fantlab.general.words").update(value=158881.0))
        with patch.object(gallery, "SOURCES", specs), self.assertRaisesRegex(gallery.GalleryError, "cardinal measurement"):
            gallery.load_gallery(self.root)

    def test_word_tokens_cannot_exceed_character_count(self):
        specs = self.repin(0, lambda doc: next(row for row in doc["metrics"] if row["metric_id"] == "fantlab.general.words").update(scriptorium_raw_value=363820))
        with patch.object(gallery, "SOURCES", specs), self.assertRaisesRegex(gallery.GalleryError, "inconsistent body statistics"):
            gallery.load_gallery(self.root)

    def test_dialogue_profile_drift_is_not_silently_compared(self):
        specs = self.repin(1, lambda doc: doc["scriptorium"]["profiles"].update(dialogue="scriptorium-dialogue-v999"))
        with patch.object(gallery, "SOURCES", specs), self.assertRaisesRegex(gallery.GalleryError, "incompatible measurement profiles"):
            gallery.load_gallery(self.root)

    def test_vocabulary_profile_drift_is_not_silently_compared(self):
        specs = self.repin(1, lambda doc: doc["scriptorium"]["profiles"].update(vocabulary="scriptorium-vocabulary-v999"))
        with patch.object(gallery, "SOURCES", specs), self.assertRaisesRegex(gallery.GalleryError, "incompatible measurement profiles"):
            gallery.load_gallery(self.root)

    def test_missing_profile_is_not_silently_compared(self):
        specs = self.repin(1, lambda doc: doc["scriptorium"]["profiles"].pop("dialogue"))
        with patch.object(gallery, "SOURCES", specs), self.assertRaisesRegex(gallery.GalleryError, "incompatible measurement profiles"):
            gallery.load_gallery(self.root)


if __name__ == "__main__":
    unittest.main()
