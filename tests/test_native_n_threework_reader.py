"""Evidence-locked, privacy-safe three-work no-JavaScript Reader comparison."""
import copy
import json
from pathlib import Path
import unittest

ROOT = Path(__file__).resolve().parents[1]
EXPECTED = {
 "word_count": 55778, "sentence_count": 4928, "baseline_defined": 25390,
 "n_only": 12724, "n_mixed_excluded": 3754, "conditional_defined": 38114,
}
EVIDENCE = {
 "normalized_sha256": "41a1ada3caabea2909976372ca6312fb8a478f2d0d87c088f304fcb30c52fdbc",
 "runtime_analysis_sha256": "429a22deec17b943598abc83abaf914916c82224e4befb3ab4b9bed4a2d2f58d",
 "artifact_json_sha256": "4d33425af45b9036ef435442ca0ecfdc47f84e617b9173a27e058237005a6dbf",
 "artifact_zip_sha256": "071ea19a89f192c60b2060c70da72083e22bca86aff2f7894976f90236d715f0",
 "head_sha": "81f6cecb2c62f90cdaef76e3019680021eab7ae9",
 "run_id": 44978278220, "artifact_id": 14735759621,
 "receipt_url": "https://github.com/drevendev/Scriptorium/pull/610#issuecomment-7073245431",
}
PROVIDER = {
 "distribution": "pylem", "version": "0.0.18",
 "runtime_profile": "pylem-0.0.18-python39-sidecar-v1",
 "sdist_sha256": "66c0d13414006a803f200979540fcee9653738701c14496a418db67542b26515",
}

def validate_grin(doc):
    if set(doc) != {"schema_version", "status", "source_text_included",
                    "m2_parity_admissible", "work", "provider", "evidence",
                    "counts", "note"}:
        raise ValueError("unexpected receipt fields")
    if (doc["schema_version"] != "scriptorium-native-n-grin-public-summary-v1"
        or doc["status"] != "diagnostic_only"
        or doc["source_text_included"] is not False
        or doc["m2_parity_admissible"] is not False
        or doc["provider"] != PROVIDER or doc["evidence"] != EVIDENCE):
        raise ValueError("scientific, provider or artifact drift")
    work = doc["work"]
    if work != {
        "candidate_id": "grin-running-on-waves-ru", "title": "Бегущая по волнам",
        "author": "Александр Грин", "language": "ru",
        "edition": "Детская литература, 1965 · frozen Wikisource transcription",
        "literary_page_revisions": 36, "characters_including_spaces": 363819,
    } or type(work["characters_including_spaces"]) is not int:
        raise ValueError("edition identity drift")
    counts = doc["counts"]
    if (not isinstance(counts, dict) or set(counts) != set(EXPECTED)
        or any(type(counts[k]) is not int for k in EXPECTED)
        or counts != EXPECTED
        or counts["n_only"] + counts["baseline_defined"] != counts["conditional_defined"]):
        raise ValueError("native counts drift")
    if not isinstance(doc["note"], str) or "Source-free" not in doc["note"]:
        raise ValueError("missing summary boundary")
    return counts

def fmt_int(x):
    return f"{x:,}".replace(",", " ")

def fmt_pct(x):
    return f"{x:.2f}".replace(".", ",")


class ThreeWorkReaderTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.doc = json.loads((ROOT / "assets/n-uncertainty-grin-summary.json").read_text(encoding="utf-8"))
        cls.page = (ROOT / "n-uncertainty.html").read_text(encoding="utf-8")

    def test_exact_source_free_native_projection(self):
        counts = validate_grin(self.doc)
        self.assertEqual(counts["n_only"] + counts["n_mixed_excluded"], 16478)
        self.assertNotIn("normalized_text", self.doc)
        self.assertNotIn("source_text", self.doc)
        self.assertNotIn("tokens", self.doc)
        self.assertIn("not this projection", self.doc["note"])

    def test_forged_metadata_or_measurements_rejected(self):
        for section, field, replacement in (
            ("counts", "n_only", 12725),
            ("counts", "word_count", 55778.0),
            ("counts", "sentence_count", True),
            ("provider", "version", "0.0.19"),
            ("evidence", "artifact_json_sha256", "0" * 64),
            ("evidence", "run_id", 1),
            ("work", "characters_including_spaces", 299999),
            (None, "source_text_included", True),
            (None, "m2_parity_admissible", True),
        ):
            with self.subTest(field=field):
                fake = copy.deepcopy(self.doc)
                (fake[section] if section else fake)[field] = replacement
                with self.assertRaises(ValueError):
                    validate_grin(fake)
        fake = copy.deepcopy(self.doc)
        fake["normalized_text"] = "not for publication"
        with self.assertRaises(ValueError):
            validate_grin(fake)

    def test_html_rows_charts_and_provenance_are_source_bound(self):
        grin = validate_grin(self.doc)
        anna = json.loads((ROOT / "assets/n-uncertainty-anna.json").read_text(encoding="utf-8"))["counts"]
        resurrection = json.loads((ROOT / "assets/n-uncertainty-resurrection-summary.json").read_text(encoding="utf-8"))["counts"]
        for key, title, counts in (
            ("anna", "Анна Каренина", anna),
            ("resurrection", "Воскресение", resurrection),
            ("grin", "Бегущая по волнам", grin),
        ):
            total, only, mixed = (counts[k] for k in ("word_count","n_only","n_mixed_excluded"))
            row = (f'<tr data-n-threework="{key}"><th scope="row">{title}</th>'
                   f'<td>{fmt_int(total)}</td>'
                   f'<td>{fmt_int(only)} · {fmt_pct(100*only/total)}%</td>'
                   f'<td>{fmt_int(mixed)} · {fmt_pct(100*mixed/total)}%</td>'
                   f'<td>{fmt_int(only+mixed)} · {fmt_pct(100*(only+mixed)/total)}%</td></tr>')
            self.assertIn(row, self.page)
            self.assertIn(f'data-n-bar="{key}"', self.page)
            self.assertIn(f'style="width:{100*only/total:.6f}%"', self.page)
            self.assertIn(f'style="width:{100*mixed/total:.6f}%"', self.page)
        self.assertEqual(self.page.count('class="n-compare-track"'), 4)
        self.assertIn('id="n-three-work-table"', self.page)
        self.assertIn("<figcaption>", self.page)
        self.assertIn('tabindex="0"', self.page)
        self.assertIn('href="./assets/n-uncertainty-grin-summary.json"', self.page)
        self.assertIn("actions/runs/44978278220", self.page)
        self.assertIn(EVIDENCE["normalized_sha256"], self.page)
        self.assertIn(EVIDENCE["runtime_analysis_sha256"], self.page)
        self.assertIn("DIAGNOSTIC_ONLY · M2: 0/5", self.page)
        self.assertIn("не восстановленная частота существительных", self.page)
        self.assertNotIn("<script", self.page)

    def test_exact_branch_root_publication_staging(self):
        workflow = (ROOT / ".github/workflows/pages.yml").read_text(encoding="utf-8")
        audit = (ROOT / "scriptorium/branch_pages_audit.py").read_text(encoding="utf-8")
        readme = (ROOT / "README.md").read_text(encoding="utf-8")
        name = "assets/n-uncertainty-grin-summary.json"
        self.assertIn(f'"{name}"', audit)
        self.assertIn(f"cp {name} build/branch-root-preview/{name}", workflow)
        self.assertIn(f"test -s build/branch-root-preview/{name}", workflow)
        self.assertIn(f"cmp {name} build/branch-root-preview/{name}", workflow)
        self.assertIn("n-uncertainty.html#n-three-work", readme)
        self.assertIn("M2 0/5", readme)

if __name__ == "__main__":
    unittest.main()
