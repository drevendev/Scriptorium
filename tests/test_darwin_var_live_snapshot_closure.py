from __future__ import annotations

import json
from pathlib import Path
import unittest

from scriptorium.darwin_var_live_snapshot_closure import (
    RESOURCES,
    build_evidence,
    validate_evidence,
)


ROOT = Path(__file__).resolve().parents[1]
PRIOR = ROOT / "corpus/candidates/source-edition-traces/darwin-origin-species-rachinsky-1864-ru.var-provider-drift-evidence.json"
EVIDENCE = ROOT / "corpus/candidates/source-edition-traces/darwin-origin-species-rachinsky-1864-ru.var-live-snapshot-closure-evidence.json"


class DarwinVarLiveSnapshotClosureTests(unittest.TestCase):
    def setUp(self) -> None:
        self.prior = json.loads(PRIOR.read_text(encoding="utf-8"))
        self.evidence = json.loads(EVIDENCE.read_text(encoding="utf-8"))

    def test_committed_evidence_rebuilds_semantically(self) -> None:
        self.assertEqual(self.evidence, build_evidence(self.prior))
        validate_evidence(self.evidence, self.prior)

    def test_exact_observed_revision_set_is_bound(self) -> None:
        resources = self.evidence["snapshot"]["resources"]
        self.assertEqual(
            [(item["title"], item["revision_id"]) for item in resources],
            [(title, revision_id) for title, revision_id, _date, _role, _loads in RESOURCES],
        )
        self.assertEqual(len(resources), 6)

    def test_load_time_topology_is_explicit(self) -> None:
        resources = {item["title"]: item for item in self.evidence["snapshot"]["resources"]}
        self.assertEqual(resources["Шаблон:ВАР"]["loads"], ["Модуль:Дореформенная орфография"])
        self.assertEqual(resources["Модуль:Дореформенная орфография"]["loads"], ["Module:Header"])
        self.assertEqual(resources["Module:Header"]["loads"], ["Module:BEED", "Module:Util"])
        self.assertEqual(resources["Module:BEED"]["loads"], ["Module:RomanNumber"])
        self.assertEqual(resources["Module:Util"]["loads"], [])
        self.assertEqual(resources["Module:RomanNumber"]["loads"], [])

    def test_sha1_and_replay_fail_closed(self) -> None:
        gate = self.evidence["identity_gate"]
        self.assertTrue(gate["revision_ids_complete"])
        self.assertFalse(gate["mediawiki_sha1_complete"])
        self.assertFalse(gate["replay_ready"])
        self.assertEqual(len(gate["missing_mediawiki_sha1_titles"]), 6)
        self.assertTrue(all(item["mediawiki_sha1"] is None for item in self.evidence["snapshot"]["resources"]))

    def test_promotion_and_parity_gates_stay_closed(self) -> None:
        decision = self.evidence["promotion_decision"]
        self.assertEqual(decision["var_invocations_unresolved"], 388)
        self.assertFalse(decision["full_var_candidate_branch_replayed"])
        self.assertFalse(decision["render_profile_rule_promoted"])
        self.assertFalse(decision["backlog_item_removed"])
        self.assertFalse(decision["effective_backlog_changed"])
        self.assertFalse(self.evidence["snapshot"]["historical_transclusion_proven"])
        self.assertFalse(self.evidence["offline_version_pinned_runtime_proven"])
        self.assertFalse(self.evidence["m2_parity_admissible"])


if __name__ == "__main__":
    unittest.main()
