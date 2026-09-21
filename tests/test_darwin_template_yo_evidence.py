from __future__ import annotations

from copy import deepcopy
import json
from pathlib import Path
import unittest

from scriptorium.darwin_template_yo_evidence import (
    build_evidence,
    build_evidence_from_paths,
    validate_evidence,
)


ROOT = Path(__file__).resolve().parents[1]
BACKLOG = ROOT / "corpus/candidates/source-edition-traces/darwin-origin-species-rachinsky-1864-ru.semantic-backlog.json"
SHARD = ROOT / "corpus/candidates/source-edition-traces/darwin-origin-species-rachinsky-1864-ru.page-revisions.01.json"
EVIDENCE = ROOT / "corpus/candidates/source-edition-traces/darwin-origin-species-rachinsky-1864-ru.template-yo-evidence.json"


def load(path: Path) -> dict[str, object]:
    value = json.loads(path.read_text(encoding="utf-8"))
    assert isinstance(value, dict)
    return value


class DarwinTemplateYoEvidenceTests(unittest.TestCase):
    def test_committed_evidence_rebuilds_exactly(self) -> None:
        expected = build_evidence_from_paths(BACKLOG, SHARD)
        committed = load(EVIDENCE)
        self.assertEqual(committed, expected)
        validate_evidence(committed, load(BACKLOG), load(SHARD))
        self.assertEqual(
            committed["evidence_sha256"],
            "3c0af5dfe8d23cd6d47ce2f92b30c58b83e352df692c18e6d4f59a14928eb06a",
        )

    def test_documented_semantics_are_conditional_not_literal(self) -> None:
        evidence = build_evidence(load(BACKLOG), load(SHARD))
        semantics = evidence["documented_semantics"]
        self.assertEqual(semantics["output_kind"], "conditional_single_character")
        self.assertEqual(semantics["forced_yoification_output"], "ё")
        self.assertEqual(semantics["non_forced_yoification_output"], "е")
        self.assertFalse(semantics["historical_equivalence_proven"])
        self.assertEqual(evidence["target"]["count"], 2227)
        self.assertEqual(evidence["target"]["semantic_status"], "unresolved")

    def test_historical_gap_uses_retained_pre_documentation_page_revision(self) -> None:
        evidence = build_evidence(load(BACKLOG), load(SHARD))
        witness = evidence["historical_gap_witness"]
        self.assertEqual(witness["page_sequence"], 11)
        self.assertEqual(witness["revision_id"], 3358032)
        self.assertEqual(witness["revision_timestamp"], "2018-08-13T19:18:33Z")
        self.assertTrue(witness["documentation_revision_postdates_page_revision"])

    def test_without_pre_documentation_page_revision_evidence_fails_closed(self) -> None:
        shard = deepcopy(load(SHARD))
        shard["page_identities"] = [
            [11, 6000000, "2025-01-01T00:00:00Z", "0" * 40],
        ]
        with self.assertRaisesRegex(ValueError, "predates documentation evidence"):
            build_evidence(load(BACKLOG), shard)

    def test_backlog_target_drift_fails_closed(self) -> None:
        backlog = deepcopy(load(BACKLOG))
        backlog["next_research_slice"] = dict(backlog["next_research_slice"])
        backlog["next_research_slice"]["count"] += 1
        with self.assertRaisesRegex(ValueError, "research target drift: count"):
            build_evidence(backlog, load(SHARD))

    def test_profile_and_downstream_gates_remain_closed(self) -> None:
        evidence = build_evidence(load(BACKLOG), load(SHARD))
        decision = evidence["promotion_decision"]
        self.assertFalse(decision["render_profile_rule_promoted"])
        self.assertFalse(decision["backlog_item_removed"])
        for key in (
            "renderer_semantics_complete",
            "renderer_implementation_ready",
            "inter_page_composition_frozen",
            "literary_body_count_and_digests_frozen",
            "minimum_300k_proved",
            "admitted_for_calibration",
            "diagnostic_ready",
            "m2_parity_admissible",
        ):
            self.assertFalse(evidence[key], key)
        self.assertEqual(evidence["fantlab_source_edition_match"], "unknown")


if __name__ == "__main__":
    unittest.main()
