from __future__ import annotations

import json
from pathlib import Path
import unittest

from scriptorium.darwin_var_provider_drift_evidence import (
    CANDIDATE_MAINSPACE_TITLE,
    OBSERVED_HEADER_REVISION_ID,
    build_evidence,
    parse_title_is_prs,
    validate_evidence,
)


ROOT = Path(__file__).resolve().parents[1]
PRIOR = ROOT / "corpus/candidates/source-edition-traces/darwin-origin-species-rachinsky-1864-ru.var-documentation-evidence.json"
EVIDENCE = ROOT / "corpus/candidates/source-edition-traces/darwin-origin-species-rachinsky-1864-ru.var-provider-drift-evidence.json"


class DarwinVarProviderDriftEvidenceTests(unittest.TestCase):
    def setUp(self) -> None:
        self.prior = json.loads(PRIOR.read_text(encoding="utf-8"))
        self.evidence = json.loads(EVIDENCE.read_text(encoding="utf-8"))

    def test_committed_evidence_rebuilds_byte_for_byte_semantically(self) -> None:
        self.assertEqual(self.evidence, build_evidence(self.prior))
        validate_evidence(self.evidence, self.prior)

    def test_candidate_title_classifies_as_non_prs(self) -> None:
        self.assertFalse(parse_title_is_prs(CANDIDATE_MAINSPACE_TITLE))
        replay = self.evidence["observed_header_rule_replay"]
        self.assertEqual(replay["header_revision_id"], OBSERVED_HEADER_REVISION_ID)
        self.assertFalse(replay["isPRS"])
        self.assertEqual(
            replay["selected_variant_if_module_branch_is_reached"],
            "second_parameter_modern",
        )

    def test_prs_examples_still_take_prs_branch(self) -> None:
        self.assertTrue(parse_title_is_prs("Пример/ДО"))
        self.assertTrue(parse_title_is_prs("Пример/1864 (ДО)"))
        self.assertTrue(parse_title_is_prs("Пример/1864/ДО"))
        self.assertFalse(parse_title_is_prs("Пример/1864 (ВТ:Ё)"))

    def test_full_replay_and_promotion_stay_closed(self) -> None:
        boundary = self.evidence["dependency_boundary"]
        self.assertFalse(boundary["template_root_revision_frozen"])
        self.assertFalse(boundary["module_header_mediawiki_sha1_frozen"])
        self.assertFalse(boundary["nested_dependency_closure_frozen"])
        self.assertFalse(boundary["full_var_candidate_branch_replayed"])
        self.assertFalse(boundary["historical_transclusion_proven"])
        self.assertFalse(boundary["offline_version_pinned_runtime_proven"])
        decision = self.evidence["promotion_decision"]
        self.assertFalse(decision["render_profile_rule_promoted"])
        self.assertFalse(decision["backlog_item_removed"])
        self.assertFalse(decision["effective_backlog_changed"])

    def test_provider_warning_is_not_promoted_to_runtime_failure(self) -> None:
        warning = self.evidence["provider_drift_observation"]["community_warning"]
        self.assertEqual(warning["discussion_date"], "2026-09-08")
        self.assertEqual(
            warning["claim_scope"],
            "provider_drift_risk_not_a_proven_runtime_failure",
        )


if __name__ == "__main__":
    unittest.main()
