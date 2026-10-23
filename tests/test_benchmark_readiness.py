"""Fail-closed, source-free cross-work benchmark readiness regressions."""
import copy
from contextlib import redirect_stderr
import csv
from io import StringIO
import json
from pathlib import Path
import tempfile
import unittest

from scriptorium.benchmark_readiness import (
    CATALOG, _SPECS, build_readiness, main, render_report,
)

ROOT = Path(__file__).resolve().parents[1]


def _write(root: Path, path: str, value: dict) -> None:
    target = root / path
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text(json.dumps(value, ensure_ascii=False), encoding="utf-8")


def _fixture(root: Path) -> None:
    candidates = []
    for i, (identifier, namespace, field) in enumerate(_SPECS):
        count = 350_000 + i * 10_000
        expected = count - (i + 1)
        work_id = i + 1
        url = f"https://fantlab.ru/work{work_id}/lp"
        digest = f"{i + 1:064x}"
        trace_path = f"corpus/candidates/source-edition-traces/{identifier}.json"
        candidate = {
            "candidate_id": identifier, "title": f"Работа {i}", "author": "Writer", "work_identity": "original",
            "source_edition_trace": trace_path, "source_identity_status": "public_candidate_frozen",
            "fantlab_source_edition_match": "unknown", "gate_ready": False,
            "fantlab": {"work_id": work_id, "analysis_url": url, "analysis_date": "2022-09-19", "characters": expected},
            "source": {"url": "https://ru.wikisource.org/wiki/Work", "edition_note": "Edition", "legal_basis": "public_domain", "legal_evidence": "Public-domain witness"},
        }
        if field:
            candidate.update({"frozen_candidate_characters": count, "frozen_candidate_sha256": digest})
        candidates.append(candidate)
        trace = {
            "candidate_id": identifier,
            "fantlab": {"work_id": work_id, "analysis_url": url, "analysis_date": "2022-09-19", "observed_counts": {"characters": expected}},
            "admissibility": {"fantlab_source_edition_match": "unknown", "m2_parity_admissible": False},
        }
        witness = {"character_count_including_spaces": count, "raw_sha256": digest, "normalized_sha256": digest, "utf8_byte_count": count * 2, "normalization_profile": "scriptorium-text-v1"}
        if field:
            witness.update({"status": "frozen_public_candidate", "source_text_committed": False})
            trace[namespace] = {field: witness}
        else:
            trace["primary_public_transcription"] = {"literary_body_witness": {"raw_sha256": digest, "normalized_sha256": digest, "character_count_including_spaces": count}}
            trace["admissibility"]["frozen_public_minus_fantlab_character_delta"] = count - expected
            body = {"candidate_id": identifier, "composite_identity": witness, "composition": {"source_text_committed": False}, "corpus_admission": {"fantlab_source_edition_match": "unknown"}}
            _write(root, f"corpus/candidates/source-edition-traces/{identifier}.literary-body.json", body)
        _write(root, trace_path, trace)
    _write(root, CATALOG, {"catalog_version": "fantlab-parity-candidates-v1", "minimum_characters_including_spaces": 300000, "candidates": candidates})
    first = candidates[0]
    _write(root, "benchmarks/fantlab/work270306.json", {
        "reference": {"work_id": 1, "url": "https://fantlab.ru/work1/lp", "analysis_date": "2022-09-19"},
        "expected": {"characters": first["fantlab"]["characters"]},
        "source_text": {"raw_sha256": first["frozen_candidate_sha256"]},
    })


class ReadinessTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.root = Path(self.tmp.name)
        _fixture(self.root)

    def test_five_frozen_works_stay_diagnostic_with_explicit_deltas(self):
        report = build_readiness(self.root)
        self.assertEqual(report["works_reported"], 5)
        self.assertEqual(report["m2_source_matched_pass_count"], 0)
        self.assertEqual([e["character_count_diagnostic"]["actual_minus_expected"] for e in report["entries"]], [1, 2, 3, 4, 5])
        for entry in report["entries"]:
            self.assertFalse(entry["parity_eligible"])
            self.assertEqual(entry["exact_fantlab_input_identity"], "UNKNOWN")
            self.assertEqual(entry["other_metric_comparisons"], "NOT_RUN")
            self.assertEqual(entry["character_count_diagnostic"]["result"], "UNRESOLVED_SOURCE")

    def test_reports_are_stable_source_free_and_csv_safe(self):
        report = build_readiness(self.root)
        for fmt in ("json", "csv", "markdown"):
            self.assertEqual(render_report(report, fmt), render_report(build_readiness(self.root), fmt))
        rows = list(csv.DictReader(StringIO(render_report(report, "csv"))))
        self.assertEqual(len(rows), 5)
        self.assertEqual(rows[0]["delta_characters"], "1")
        self.assertIn("0/5", render_report(report, "markdown"))
        self.assertEqual(json.loads(render_report(report, "json"))["works_reported"], 5)

    def test_cli_creates_output_without_overwrite(self):
        destination = self.root / "readiness.csv"
        self.assertEqual(main(["--root", str(self.root), "--format", "csv", "--output", str(destination)]), 0)
        before = destination.read_bytes()
        error_output = StringIO()
        with redirect_stderr(error_output), self.assertRaises(SystemExit):
            main(["--root", str(self.root), "--format", "csv", "--output", str(destination)])
        self.assertNotIn(str(destination), error_output.getvalue())
        self.assertIn("already exists", error_output.getvalue())
        self.assertEqual(destination.read_bytes(), before)

    def test_rejects_forged_source_match(self):
        data = json.loads((self.root / CATALOG).read_text(encoding="utf-8"))
        data["candidates"][0]["fantlab_source_edition_match"] = "exact"
        _write(self.root, CATALOG, data)
        with self.assertRaisesRegex(ValueError, "source match"):
            build_readiness(self.root)

    def test_rejects_short_or_forged_frozen_witness(self):
        p = self.root / f"corpus/candidates/source-edition-traces/{_SPECS[0][0]}.json"
        raw = json.loads(p.read_text(encoding="utf-8"))
        bad = copy.deepcopy(raw)
        bad["public_transcription"]["frozen_candidate"]["character_count_including_spaces"] = 20
        _write(self.root, str(p.relative_to(self.root)), bad)
        with self.assertRaisesRegex(ValueError, "300,000"):
            build_readiness(self.root)
        bad = copy.deepcopy(raw)
        bad["public_transcription"]["frozen_candidate"]["raw_sha256"] = "f" * 64
        _write(self.root, str(p.relative_to(self.root)), bad)
        with self.assertRaisesRegex(ValueError, "digest"):
            build_readiness(self.root)

    def test_rejects_forged_running_waves_body_digest(self):
        identifier = _SPECS[-1][0]
        p = self.root / f"corpus/candidates/source-edition-traces/{identifier}.literary-body.json"
        body = json.loads(p.read_text(encoding="utf-8"))
        body["composite_identity"]["raw_sha256"] = "f" * 64
        _write(self.root, str(p.relative_to(self.root)), body)
        with self.assertRaisesRegex(ValueError, "running body trace raw digest"):
            build_readiness(self.root)

    def test_rejects_falsified_fantlab_url_and_duplicate_json_fields(self):
        path = self.root / CATALOG
        data = json.loads(path.read_text(encoding="utf-8"))
        data["candidates"][0]["fantlab"]["analysis_url"] = "https://fantlab.ru/work999/lp"
        _write(self.root, CATALOG, data)
        with self.assertRaisesRegex(ValueError, "FantLab URL"):
            build_readiness(self.root)
        path.write_text('{"catalog_version":"v1","catalog_version":"v2"}', encoding="utf-8")
        with self.assertRaisesRegex(ValueError, "duplicate JSON field"):
            build_readiness(self.root)

    def test_real_repository_witnesses_and_deltas(self):
        if not (ROOT / CATALOG).exists():
            self.skipTest("full source-free corpus metadata not present in local fixture")
        report = build_readiness(ROOT)
        self.assertEqual([e["character_count_diagnostic"]["actual_minus_expected"] for e in report["entries"]], [12958, 3244, 14075, 3527, 2832])
        self.assertEqual(report["m2_source_matched_pass_count"], 0)


if __name__ == "__main__":
    unittest.main()
