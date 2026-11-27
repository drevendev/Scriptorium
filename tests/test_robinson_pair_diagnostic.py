"""Regression tests for the source-free comparison renderer and gate."""
import copy
import json
from pathlib import Path
import unittest

from scriptorium.robinson_pair_diagnostic import build, render, load_shish, SHISH_RELATIVE, SCOPE
from scriptorium.trusov_excerpt_export import load_frozen_report, SOURCE_RELATIVE


class RobinsonPairTests(unittest.TestCase):
    def setUp(self):
        self.interior = load_frozen_report(Path(SOURCE_RELATIVE))
        self.shish = load_shish(Path(SHISH_RELATIVE))
        # Synthetic assembly values, deliberately NOT real measurements.
        i = self.interior
        self.a = {
            "schema_version": "scriptorium-trusov-boundary-assembly-v1",
            "scope": SCOPE, "page_interval": {"from": 2, "to": 151, "count": 150},
            "source_page_graph_sha256": i["source_page_graph_sha256"],
            "baseline_normalized_sha256": i["normalized_sha256"],
            "interior_source_revision_list_sha256": i["source_revision_list_sha256"],
            "join_profile": i["join"]["projected_page_join_profile"],
            "closing_scope": "SIX_LITERAL_SEAMS_AND_CURRENT_LAYOUT_VERIFIED",
            "full_literary_body": "NOT_VERIFIED", "print_collation": "NOT_VERIFIED",
            "historical_render_equivalence_proven": False, "historical_page_join_verified": False,
            "corpus_admitted": False, "m2_parity_admissible": False, "source_text_committed": False,
            "boundary_pages": [{"page_sequence": n, "characters": 1} for n in (2,148,149,150,151)],
            "boundary_source_identities": [{"revision_id": n} for n in (4958669,4958660,4958661,4958663,4958664)],
            "raw_joined_characters": 303892, "normalized_characters_including_spaces": 303892,
            "normalized_sha256": "a"*64, "raw_joined_sha256": "b"*64,
            "metric_rows": [{"metric_id": r["metric_id"], "unit": r["unit"],
                             "interior_value": r["actual"],
                             "assembly_value": r["actual"],
                             "delta": None if r["actual"] is None else 0} for r in i["metric_rows"]],
            "numeric_metric_count": 22, "unavailable_metric_count": 7,
        }
        c = next(r for r in self.a["metric_rows"] if r["metric_id"] == "fantlab.general.characters")
        c.update(assembly_value=303892, delta=10)

    def test_comparison_nulls_and_sign(self):
        report = build(self.a, self.interior, self.shish)
        self.assertEqual(report["joint_numeric_count"], 22)
        c = next(r for r in report["metric_rows"] if r["metric_id"] == "fantlab.general.characters")
        self.assertEqual(c["delta_trusov_minus_shishmareva"], 303892-572587)
        self.assertEqual(sum(r["delta_trusov_minus_shishmareva"] is None for r in report["metric_rows"]), 7)
        self.assertFalse(report["corpus_admitted"])
        html = render(report)
        self.assertEqual(html.count("<tr>"), 30)
        self.assertIn("Unavailable", html)
        self.assertIn("Coverage and abridgement are not aligned", html)
        self.assertIn("robinson-pair.json", html)

    def test_scope_and_metric_tampering_refused(self):
        for key, value in (("corpus_admitted", True), ("baseline_normalized_sha256", "x"),
                           ("numeric_metric_count", 29), ("raw_joined_characters", 0)):
            a = copy.deepcopy(self.a)
            a[key] = value
            with self.subTest(key=key), self.assertRaises(ValueError):
                build(a, self.interior, self.shish)
        a = copy.deepcopy(self.a)
        a["metric_rows"][0]["unit"] = "words"
        with self.assertRaises(ValueError):
            build(a, self.interior, self.shish)
        a = copy.deepcopy(self.a)
        r = next(r for r in a["metric_rows"] if r["metric_id"] == "fantlab.vocabulary.active_dictionary")
        r["assembly_value"] = 0
        with self.assertRaises(ValueError):
            build(a, self.interior, self.shish)

    def test_profile_mismatch_refused(self):
        s = copy.deepcopy(self.shish)
        s["scriptorium"]["profiles"]["metrics"] = "different"
        with self.assertRaises(ValueError):
            build(self.a, self.interior, s)
