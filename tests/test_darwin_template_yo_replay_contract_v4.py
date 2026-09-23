from __future__ import annotations

from copy import deepcopy
import json
from pathlib import Path
import unittest

from scriptorium.darwin_template_yo_replay_contract import validate_dependency_closure
from scriptorium.darwin_template_yo_replay_contract_v4 import (
    BOUND_ROOT_EDGE,
    CONTRACT_VERSION,
    PREDECESSOR_SHA256,
    ROOT_SCAN_OBSERVATIONS,
    build_contract,
    build_contract_from_paths,
    validate_contract,
)


ROOT = Path(__file__).resolve().parents[1]
EVIDENCE = ROOT / "corpus/candidates/source-edition-traces/darwin-origin-species-rachinsky-1864-ru.template-yo-evidence.json"
V2 = ROOT / "corpus/candidates/source-edition-traces/darwin-origin-species-rachinsky-1864-ru.template-yo-replay-contract.json"
V3 = ROOT / "corpus/candidates/source-edition-traces/darwin-origin-species-rachinsky-1864-ru.template-yo-replay-contract-v3.json"


def load(path: Path) -> dict[str, object]:
    value = json.loads(path.read_text(encoding="utf-8"))
    assert isinstance(value, dict)
    return value


class DarwinTemplateYoReplayContractV4Tests(unittest.TestCase):
    def build(self) -> dict[str, object]:
        return build_contract(load(EVIDENCE), load(V2), load(V3))

    def test_builder_is_deterministic_and_tracks_predecessor(self) -> None:
        expected = build_contract_from_paths(EVIDENCE, V2, V3)
        actual = self.build()
        self.assertEqual(actual, expected)
        self.assertEqual(actual["schema_version"], CONTRACT_VERSION)
        self.assertEqual(actual["predecessor_contract"]["contract_sha256"], PREDECESSOR_SHA256)
        validate_contract(actual, load(EVIDENCE), load(V2), load(V3))

    def test_root_direct_dependency_discovery_is_complete_but_recursive_closure_is_open(self) -> None:
        contract = self.build()
        replay = contract["replay_contract"]
        self.assertTrue(replay["root_direct_dependency_discovery_complete"])
        self.assertFalse(replay["dependency_closure_complete"])
        self.assertEqual(replay["discovered_unbound_dependencies"], ["Модуль:String"])
        self.assertEqual(replay["edges"], [BOUND_ROOT_EDGE])
        dependencies = replay["dependencies"]
        self.assertEqual(dependencies[0]["discovery"]["direct_dependencies"], ["Шаблон:ЕЁ"])
        self.assertEqual(dependencies[1]["discovery"]["direct_dependencies"], ["Модуль:String"])
        validate_dependency_closure(dependencies, replay["edges"], require_complete=False)
        with self.assertRaisesRegex(ValueError, "discovered dependency remains unbound"):
            validate_dependency_closure(dependencies, replay["edges"], require_complete=True)

    def test_source_free_observations_match_frozen_scan_evidence(self) -> None:
        contract = self.build()
        observations = contract["direct_dependency_discovery"]["root_observations"]
        self.assertEqual(len(observations), len(ROOT_SCAN_OBSERVATIONS))
        for actual, frozen in zip(observations, ROOT_SCAN_OBSERVATIONS, strict=True):
            self.assertEqual(actual["title"], frozen["title"])
            self.assertEqual(actual["revision_id"], frozen["revision_id"])
            self.assertEqual(actual["source_sha1"], frozen["mediawiki_sha1"])
            self.assertEqual(actual["source_utf8_bytes"], frozen["source_utf8_bytes"])
            self.assertEqual(actual["transclusion_sha256"], frozen["transclusion_sha256"])
            self.assertEqual(actual["direct_dependencies"], frozen["direct_dependencies"])
            self.assertFalse({"content", "text", "wikitext", "body", "source_text"}.intersection(actual))
        self.assertFalse(contract["direct_dependency_discovery"]["source_text_retained"])

    def test_discovered_edges_separate_bound_and_unbound_targets(self) -> None:
        contract = self.build()
        self.assertEqual(
            contract["direct_dependency_discovery"]["discovered_edges"],
            [
                {"from": "Шаблон:Ё", "to": "Шаблон:ЕЁ", "target_identity_bound": True},
                {"from": "Шаблон:ЕЁ", "to": "Модуль:String", "target_identity_bound": False},
            ],
        )

    def test_magic_word_evidence_is_pinned(self) -> None:
        contract = self.build()
        evidence = contract["official_api_evidence"]["magic_word_classification"]
        self.assertEqual(evidence["revision_id"], 8589537)
        self.assertTrue(evidence["template_name_conflict_variable_wins_by_default"])
        self.assertTrue(evidence["parameters_can_force_template_transclusion"])

    def test_dependency_mutation_fails_closed(self) -> None:
        contract = deepcopy(self.build())
        contract["replay_contract"]["dependencies"][0]["discovery"]["direct_dependencies"] = []
        with self.assertRaisesRegex(ValueError, "v4 contract drift"):
            validate_contract(contract, load(EVIDENCE), load(V2), load(V3))

    def test_downstream_gates_remain_closed(self) -> None:
        contract = self.build()
        self.assertFalse(contract["mode_verification"]["outputs_verified"])
        self.assertFalse(contract["promotion_decision"]["render_profile_rule_promoted"])
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
            self.assertFalse(contract[key], key)
        self.assertEqual(contract["fantlab_source_edition_match"], "unknown")


if __name__ == "__main__":
    unittest.main()
