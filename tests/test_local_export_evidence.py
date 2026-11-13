"""Private Markdown and CSV must preserve the registered evidence contract.

Rendering an imported JSON report validates declarations, not source authenticity.
Use 'verify' with the original manuscript for an actual replay.
"""
from __future__ import annotations

import copy
import csv
import io
import json
import unittest

from scriptorium.analyze import build_local_analysis, render_csv, render_markdown


TEXT = "Кот сказал: — Привет!\nА потом замолчал."


class LocalExportEvidenceContractTests(unittest.TestCase):
    def setUp(self) -> None:
        self.artifact = build_local_analysis(TEXT.encode("utf-8"))

    def test_valid_csv_and_markdown_preserve_values_and_missing_rows(self):
        for artifact in (self.artifact, build_local_analysis(b"")):
            before = json.dumps(artifact, sort_keys=True, ensure_ascii=False)
            markdown = render_markdown(artifact)
            csv_text = render_csv(artifact)
            rows = list(csv.DictReader(io.StringIO(csv_text)))
            self.assertEqual(len(rows), 29)
            self.assertEqual({row["metric_id"] for row in rows}, set(artifact["metrics"]))
            for row in rows:
                value = artifact["metrics"][row["metric_id"]]["value"]
                self.assertEqual(row["value"], "" if value is None else str(value))
            self.assertIn("NOT** verified FantLab parity", markdown)
            self.assertNotIn(TEXT, markdown)
            self.assertNotIn(TEXT, csv_text)
            self.assertEqual(before, json.dumps(artifact, sort_keys=True, ensure_ascii=False))
            self.assertEqual(render_markdown(artifact), markdown)
            self.assertEqual(render_csv(artifact), csv_text)

    def test_registered_unit_and_evidence_tampering_fail_closed_in_both_formats(self):
        cases = (
            ("fantlab.general.words", "unit", "percent"),
            ("fantlab.punctuation.comma.per_1000_words", "unit", "percent"),
            ("fantlab.vocabulary.unique_words", "definition_evidence", "scriptorium_extension"),
            ("fantlab.general.words", "compatibility_status", "extension"),
            ("scriptorium.general.sentences", "compatibility_status", "inferred"),
        )
        for metric_id, key, value in cases:
            for renderer in (render_csv, render_markdown):
                with self.subTest(format=renderer.__name__, metric=metric_id, key=key):
                    artifact = copy.deepcopy(self.artifact)
                    artifact["metrics"][metric_id][key] = value
                    with self.assertRaises(ValueError):
                        renderer(artifact)

    def test_corrupt_provenance_counts_and_threshold_fail_closed(self):
        def edits():
            yield lambda a: a["source"].update(raw_sha256="0" * 32)
            yield lambda a: a["source"].update(normalized_character_count=0)
            yield lambda a: a["representativeness"].update(meets_calibration_threshold=True)
            yield lambda a: a["representativeness"].update(calibration_threshold_characters=1)
            yield lambda a: a.update(metric_contract_id="false-parity")
            yield lambda a: a["analyzer"]["profiles"].update(normalization=None)
            yield lambda a: a["metrics"]["fantlab.general.words"].update(raw_count=-1)
        for index, edit in enumerate(edits()):
            for renderer in (render_csv, render_markdown):
                with self.subTest(case=index, format=renderer.__name__):
                    artifact = copy.deepcopy(self.artifact)
                    edit(artifact)
                    with self.assertRaises(ValueError):
                        renderer(artifact)

    def test_dictionary_provenance_and_unavailable_values(self):
        private = build_local_analysis(
            TEXT.encode("utf-8"), dictionary_words=["кот"], dictionary_profile="private-v1"
        )
        for renderer in (render_csv, render_markdown):
            self.assertTrue(renderer(private))
            artifact = copy.deepcopy(private)
            artifact["analyzer"]["dependencies"]["vocabulary_dictionary"]["lexeme_count"] = -1
            with self.assertRaises(ValueError):
                renderer(artifact)
        # An unavailable observation is not zero; both formats preserve it.
        empty = build_local_analysis(b"")
        rows = list(csv.DictReader(io.StringIO(render_csv(empty))))
        unavailable = [r for r in rows if empty["metrics"][r["metric_id"]]["value"] is None]
        self.assertGreater(len(unavailable), 0)
        self.assertTrue(all(r["value"] == "" for r in unavailable))
        self.assertIn("Unavailable", render_markdown(empty))


if __name__ == "__main__":
    unittest.main()
