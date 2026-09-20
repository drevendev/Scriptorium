from __future__ import annotations

import json
from pathlib import Path
import tempfile
import unittest

from scriptorium.twelve_chairs_gap_membership import (
    COMPOSITION_SURFACE,
    build_decision,
    validate_decision,
)
from scriptorium.twelve_chairs_page_freeze import expected_page_sequences


ROOT = Path(__file__).resolve().parents[1]
TRACE_DIR = ROOT / "corpus" / "candidates" / "source-edition-traces"
INDEX = TRACE_DIR / "ilf-petrov-twelve-chairs-zif-1928.page-revisions.index.json"
GAP_AUDIT = TRACE_DIR / "ilf-petrov-twelve-chairs-zif-1928.gap-audit.json"
DECISION = TRACE_DIR / "ilf-petrov-twelve-chairs-zif-1928.gap-membership.json"


class TwelveChairsGapMembershipTests(unittest.TestCase):
    def test_committed_decision_rebuilds_exactly(self) -> None:
        committed = json.loads(DECISION.read_text(encoding="utf-8"))
        validate_decision(committed, index_path=INDEX, gap_audit_path=GAP_AUDIT)
        self.assertEqual(
            committed,
            build_decision(index_path=INDEX, gap_audit_path=GAP_AUDIT),
        )

    def test_all_gaps_are_excluded_from_410_dependency_surface(self) -> None:
        decision = build_decision(index_path=INDEX, gap_audit_path=GAP_AUDIT)
        dependencies = set(expected_page_sequences())
        self.assertEqual(decision["composition_surface"], COMPOSITION_SURFACE)
        self.assertEqual(decision["literary_dependency_count"], 410)
        self.assertEqual(
            [row["page_sequence"] for row in decision["decisions"]],
            [150, 151, 314, 315],
        )
        self.assertTrue(all(row["composition_membership"] == "excluded" for row in decision["decisions"]))
        self.assertFalse(any(row["page_sequence"] in dependencies for row in decision["decisions"]))

    def test_nonempty_gap_exclusion_is_not_semantic_classification(self) -> None:
        decision = build_decision(index_path=INDEX, gap_audit_path=GAP_AUDIT)
        by_page = {row["page_sequence"]: row for row in decision["decisions"]}
        for page in (150, 314):
            self.assertEqual(by_page[page]["body_presence_class"], "nonempty_body_unclassified")
            self.assertEqual(by_page[page]["semantic_literary_classification"], "not_claimed")
            self.assertEqual(
                by_page[page]["rationale"],
                "nonempty_but_not_transcluded_by_frozen_canonical_part_routes",
            )
        for page in (151, 315):
            self.assertEqual(by_page[page]["body_presence_class"], "no_transcluded_body")

    def test_downstream_body_and_parity_gates_remain_closed(self) -> None:
        decision = build_decision(index_path=INDEX, gap_audit_path=GAP_AUDIT)
        self.assertTrue(decision["gap_membership_frozen"])
        self.assertTrue(decision["dependency_inventory_unchanged"])
        for key in (
            "literary_body_composition_frozen",
            "page_body_rendering_profile_frozen",
            "literary_body_count_and_digests_frozen",
            "minimum_300k_proved",
            "admitted_for_calibration",
            "diagnostic_ready",
            "gate_ready",
            "m2_parity_admissible",
        ):
            self.assertFalse(decision[key], key)
        self.assertEqual(decision["fantlab_source_edition_match"], "unknown")
        self.assertFalse(decision["source_text_included"])

    def test_gap_audit_drift_fails_closed(self) -> None:
        committed = json.loads(DECISION.read_text(encoding="utf-8"))
        gap = json.loads(GAP_AUDIT.read_text(encoding="utf-8"))
        gap["gap_pages"][0]["body_presence_class"] = "no_transcluded_body"
        with tempfile.TemporaryDirectory() as tmp:
            altered = Path(tmp) / "gap-audit.json"
            altered.write_text(json.dumps(gap, ensure_ascii=False), encoding="utf-8")
            with self.assertRaises(ValueError):
                validate_decision(committed, index_path=INDEX, gap_audit_path=altered)


if __name__ == "__main__":
    unittest.main()
