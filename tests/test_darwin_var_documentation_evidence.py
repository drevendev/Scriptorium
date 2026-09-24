from __future__ import annotations

from copy import deepcopy
import json
from pathlib import Path
import unittest

from scriptorium.darwin_var_documentation_evidence import (
    build_evidence,
    build_evidence_from_path,
    validate_evidence,
)


ROOT = Path(__file__).resolve().parents[1]
BACKLOG = (
    ROOT
    / "corpus/candidates/source-edition-traces/"
    "darwin-origin-species-rachinsky-1864-ru.semantic-backlog-v3.json"
)
EVIDENCE = (
    ROOT
    / "corpus/candidates/source-edition-traces/"
    "darwin-origin-species-rachinsky-1864-ru.var-documentation-evidence.json"
)


def load(path: Path) -> dict[str, object]:
    value = json.loads(path.read_text(encoding="utf-8"))
    assert isinstance(value, dict)
    return value


class DarwinVarDocumentationEvidenceTests(unittest.TestCase):
    def test_committed_evidence_rebuilds_exactly(self) -> None:
        committed = load(EVIDENCE)
        expected = build_evidence_from_path(BACKLOG)
        self.assertEqual(committed, expected)
        validate_evidence(committed, load(BACKLOG))
        self.assertEqual(
            committed["evidence_sha256"],
            "321ced32bb7ffc75829b6fbb5255bce3243641a80c21ad4e2b7bb7a25138502d",
        )
        self.assertEqual(
            committed["schema_version"],
            "scriptorium-darwin-var-documentation-evidence-v1",
        )

    def test_backlog_target_is_exact_var_shape(self) -> None:
        evidence = build_evidence(load(BACKLOG))
        self.assertEqual(
            evidence["target"],
            {
                "source_kind": "template",
                "name": "ВАР",
                "positional": 2,
                "named": 0,
                "count": 388,
                "semantic_status": "unresolved",
                "backlog_priority_rank": 1,
            },
        )

    def test_documentation_and_module_are_revision_pinned(self) -> None:
        evidence = build_evidence(load(BACKLOG))
        self.assertEqual(evidence["official_documentation"]["revision_id"], 5711068)
        self.assertEqual(evidence["implementation_module"]["revision_id"], 5721277)
        self.assertEqual(
            evidence["implementation_module"]["direct_dependency_titles"],
            ["Module:Header"],
        )

    def test_documented_parameter_and_branch_roles_are_retained(self) -> None:
        semantics = build_evidence(load(BACKLOG))["documented_semantics"]
        self.assertEqual(semantics["first_parameter_role"], "pre_reform_text")
        self.assertEqual(semantics["second_parameter_role"], "modern_text")
        self.assertEqual(
            semantics["page_namespace_behavior"],
            "emit_both_variants_with_generated_references_and_divider",
        )
        self.assertEqual(
            semantics["isPRS_true_output"],
            "first_parameter_pre_reform",
        )
        self.assertEqual(
            semantics["isPRS_false_output"],
            "second_parameter_modern",
        )

    def test_candidate_output_and_historical_equivalence_remain_unproven(self) -> None:
        semantics = build_evidence(load(BACKLOG))["documented_semantics"]
        self.assertFalse(semantics["candidate_mainspace_branch_replayed"])
        self.assertFalse(semantics["historical_equivalence_proven"])

    def test_dependency_boundary_stays_fail_closed(self) -> None:
        boundary = build_evidence(load(BACKLOG))["dependency_boundary"]
        self.assertTrue(boundary["implementation_module_revision_documented"])
        self.assertFalse(boundary["template_root_revision_frozen"])
        self.assertFalse(boundary["module_header_revision_frozen"])
        self.assertFalse(boundary["nested_dependency_closure_frozen"])
        self.assertFalse(boundary["offline_version_pinned_runtime_proven"])

    def test_backlog_drift_fails_closed(self) -> None:
        changed = deepcopy(load(BACKLOG))
        changed["next_research_slice"] = dict(changed["next_research_slice"])
        changed["next_research_slice"]["count"] = 389
        with self.assertRaisesRegex(ValueError, "semantic backlog digest drift"):
            build_evidence(changed)

    def test_promotion_and_downstream_gates_remain_closed(self) -> None:
        evidence = build_evidence(load(BACKLOG))
        decision = evidence["promotion_decision"]
        self.assertFalse(decision["render_profile_rule_promoted"])
        self.assertFalse(decision["backlog_item_removed"])
        self.assertIn("Шаблон:ВАР", decision["next_evidence_required"])
        self.assertIn("Module:Header", decision["next_evidence_required"])
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
