"""Offline curated tag CSV: real numeric replay, privacy and CLI safety."""
from __future__ import annotations

from copy import deepcopy
import contextlib
import csv
from hashlib import sha256
from io import StringIO
import json
from pathlib import Path
import tempfile
import unittest

from scriptorium import cli
from scriptorium.tag_profile import build_tag_profiles, FEATURES
from scriptorium.tag_profile_csv import render_tag_profiles_csv


def sample():
    books, claims = [], []
    for key, word, comma in (("a", 4.2, 10.0), ("b", 5.2, None)):
        rows = [
            {"id": "fantlab.general.characters", "actual": 350000,
             "status": "measured", "kind": "candidate"},
            {"id": "fantlab.general.mean_word_length_chars", "actual": word,
             "status": "measured", "kind": "candidate"},
            {"id": "fantlab.general.mean_sentence_length_chars", "actual": 50.0,
             "status": "measured", "kind": "candidate"},
            {"id": "fantlab.dialogue.share_percent", "actual": 0.0,
             "status": "measured", "kind": "candidate"},
            {"id": "fantlab.punctuation.comma.per_1000_words", "actual": comma,
             "status": "measured" if comma is not None else "unavailable",
             "kind": "candidate"},
        ]
        books.append({"key": key, "candidate_id": "work-" + key,
                      "edition_id": "edition-" + key, "source_sha256": key * 64,
                      "language": "ru", "translator": None, "text_status": "measured",
                      "profiles": {"metrics": "scriptorium-metrics-v4"}, "metrics": rows})
        claims.append({"key": key, "candidate_id": "work-" + key,
                       "edition_id": "edition-" + key, "source_sha256": key * 64,
                       "language": "ru", "translator": None,
                       "rights": {"basis": "public_domain", "reviewed": True,
                                  "evidence_url": "https://example.org/rights/" + key},
                       "annotations": [{"tag_id": "historical", "authority": "human_curator",
                                        "certainty": "confirmed",
                                        "evidence_url": "https://example.org/tags/" + key}]})
    snapshot = {"schema": "scriptorium-ru-reader-v2", "scientific_claim": "DIAGNOSTIC_ONLY",
                "fantlab_input_identity": "UNKNOWN", "counts": {"m2_source_matched": 0},
                "comparability": {"m2_parity_admissible": False}, "books": books}
    curation = {"schema": "scriptorium-tag-curation-v1", "taxonomy_version": "taxonomy-v1",
                "tags": [{"id": "historical", "label": "Historical fiction"},
                         {"id": "science", "label": "Science"}], "editions": claims}
    return snapshot, curation


def records(value):
    reader = csv.DictReader(StringIO(value))
    assert reader.fieldnames == ["section", "field", "value", "unit"]
    data = {(row["section"], row["field"]): row for row in reader}
    assert len(data) == len(list(csv.DictReader(StringIO(value))))
    return data


class TagProfileCsvTests(unittest.TestCase):
    def report(self):
        s, c = sample()
        return build_tag_profiles(s, c, snapshot_sha256="f" * 64)

    def test_tidy_numeric_units_missing_zero_and_edition_identity(self):
        report = self.report()
        data = records(render_tag_profiles_csv(report))
        self.assertEqual(data["report", "source_snapshot_sha256"]["value"], "f" * 64)
        self.assertEqual(data["scientific_boundary", "public_release_ready"]["value"], "false")
        self.assertEqual(data["scientific_boundary", "m2_source_matched"]["value"], "0")
        self.assertEqual(data["source_profile", "metrics"]["value"], "scriptorium-metrics-v4")
        self.assertEqual(data["tag/historical", "confirmed_work_count"]["value"], "2")
        self.assertEqual(data["tag/science", "confirmed_work_count"]["value"], "0")
        word = "metric/historical/fantlab.general.mean_word_length_chars"
        self.assertEqual(data[word, "mean_per_work"]["value"], "4.7")
        self.assertEqual(data[word, "population_stddev_between_works"]["value"], "0.5")
        self.assertEqual(data[word, "mean_per_work"]["unit"], "characters/word")
        self.assertEqual(data[word, "observed_count"]["unit"], "editions")
        zero = "metric/historical/fantlab.dialogue.share_percent"
        self.assertEqual(data[zero, "mean_per_work"]["value"], "0.0")
        self.assertEqual(data[zero, "mean_per_work"]["unit"], "%")
        missing = "metric/historical/fantlab.punctuation.dash.per_1000_words"
        self.assertEqual(data[missing, "mean_per_work"]["value"], "NOT_RUN")
        self.assertEqual(data[missing, "observed_count"]["value"], "0")
        self.assertEqual(data["edition/historical/1", "source_sha256"]["value"], "a" * 64)
        self.assertEqual(data["edition/historical/2", "tag_evidence_url"]["value"],
                         "https://example.org/tags/b")
        self.assertNotIn("source_text", render_tag_profiles_csv(report))

    def test_order_independent_and_spreadsheet_formula_safe(self):
        report = self.report()
        baseline = render_tag_profiles_csv(report)
        reordered = deepcopy(report)
        reordered["tags"].reverse()
        for tag in reordered["tags"]:
            tag["metrics"].reverse()
            tag["works"].reverse()
        self.assertEqual(baseline, render_tag_profiles_csv(reordered))
        report["tags"][0]["label"] = '=SUM(1,2),"sheet"'
        report["tags"][0]["works"][0]["edition_id"] = "@DANGEROUS"
        csv_text = render_tag_profiles_csv(report)
        data = records(csv_text)
        self.assertEqual(data["tag/historical", "label"]["value"], "'=SUM(1,2),\"sheet\"")
        self.assertEqual(data["edition/historical/1", "edition_id"]["value"], "'@DANGEROUS")

    def test_bad_evidence_and_profile_spoofing_are_rejected(self):
        for mutation in (
            lambda r: r["scientific_boundary"].update(public_release_ready=True),
            lambda r: r["tags"][0]["metrics"][0].update(mean_per_work=float("nan")),
            lambda r: r["tags"][0]["works"][0].update(source_text="PRIVATE MANUSCRIPT"),
            lambda r: r.update(source_metric_profiles={"metrics": "=HYPERLINK(1)"}),
            lambda r: r["tags"][0]["metrics"][0].update(missing_count=99),
        ):
            with self.subTest(mutation=mutation):
                report = self.report()
                mutation(report)
                with self.assertRaises(ValueError):
                    render_tag_profiles_csv(report)

    def test_cli_csv_is_create_only_and_json_default_stays_unchanged(self):
        snapshot, curation = sample()
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            snap_path, curated_path, dest = (root / name for name in
                                            ("snapshot.json", "curation.json", "private-tags.csv"))
            snap_path.write_text(json.dumps(snapshot), encoding="utf-8")
            curated_path.write_text(json.dumps(curation), encoding="utf-8")
            args = ["tags", "--snapshot", str(snap_path),
                    "--curation", str(curated_path)]
            with contextlib.redirect_stdout(StringIO()) as stdout:
                self.assertEqual(cli.main(args), 0)
            default = json.loads(stdout.getvalue())
            self.assertEqual(default["source_snapshot_sha256"],
                             sha256(snap_path.read_bytes()).hexdigest())
            with contextlib.redirect_stdout(StringIO()):
                self.assertEqual(cli.main(args + ["--format", "csv", "--output", str(dest)]), 0)
            written = dest.read_text(encoding="utf-8")
            self.assertEqual(written, render_tag_profiles_csv(default))
            self.assertEqual(records(written)["tag/historical", "label"]["value"],
                             "Historical fiction")
            with contextlib.redirect_stderr(StringIO()), self.assertRaises(SystemExit):
                cli.main(args + ["--format", "csv", "--output", str(dest)])
            self.assertEqual(written, dest.read_text(encoding="utf-8"))


if __name__ == "__main__":
    unittest.main()
