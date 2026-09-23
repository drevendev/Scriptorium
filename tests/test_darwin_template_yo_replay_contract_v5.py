from __future__ import annotations

from copy import deepcopy
import json
from pathlib import Path
import unittest

from scriptorium.darwin_template_yo_replay_contract import validate_dependency_closure
from scriptorium.darwin_template_yo_replay_contract_v5 import (
    BOUND_MODULE_EDGE,
    CONTRACT_VERSION,
    PREDECESSOR_SHA256,
    PROBE_SHA256,
    build_contract,
    build_contract_from_paths,
    validate_contract,
)


ROOT = Path(__file__).resolve().parents[1]
PREDECESSOR = ROOT / "corpus/candidates/source-edition-traces/darwin-origin-species-rachinsky-1864-ru.template-yo-replay-contract-v4.json"
PROBE = ROOT / "corpus/candidates/source-edition-traces/darwin-origin-species-rachinsky-1864-ru.module-string-dependency-probe-v1.json"
CONTRACT = ROOT / "corpus/candidates/source-edition-traces/darwin-origin-species-rachinsky-1864-ru.template-yo-replay-contract-v5.json"


def load(path: Path) -> dict[str, object]:
    value = json.loads(path.read_text(encoding="utf-8"))
    assert isinstance(value, dict)
    return value


class DarwinTemplateYoReplayContractV5Tests(unittest.TestCase):
    def build(self) -> dict[str, object]:
        return build_contract(load(PREDECESSOR), load(PROBE))

    def test_committed_contract_is_exact_deterministic_build(self) -> None:
        expected = build_contract_from_paths(PREDECESSOR, PROBE)
        actual = load(CONTRACT)
        self.assertEqual(actual, expected)
        self.assertEqual(actual["schema_version"], CONTRACT_VERSION)
        self.assertEqual(actual["predecessor_contract"]["contract_sha256"], PREDECESSOR_SHA256)
        self.assertEqual(actual["binding_evidence"]["module_string_probe"]["probe_sha256"], PROBE_SHA256)
        validate_contract(actual, load(PREDECESSOR), load(PROBE))

    def test_three_node_graph_is_transitively_closed(self) -> None:
        contract = self.build()
        replay = contract["replay_contract"]
        self.assertTrue(replay["dependency_closure_complete"])
        self.assertEqual(replay["discovered_unbound_dependencies"], [])
        self.assertEqual(replay["edges"][-1], BOUND_MODULE_EDGE)
        self.assertEqual([row["title"] for row in replay["dependencies"]], ["Шаблон:Ё", "Шаблон:ЕЁ", "Модуль:String"])
        validate_dependency_closure(replay["dependencies"], replay["edges"], require_complete=True)

    def test_module_leaf_is_bound_only_from_complete_reviewed_probe(self) -> None:
        contract = self.build()
        module = contract["replay_contract"]["dependencies"][-1]
        self.assertEqual(module["revision_id"], 3684569)
        self.assertEqual(module["mediawiki_sha1"], "a34727a1e4ec3c4b4c7ec556c94991f75442d99c")
        self.assertEqual(module["discovery"]["method"], "scriptorium-darwin-lua-loader-scan-v1")
        self.assertEqual(module["discovery"]["direct_dependencies"], [])
        self.assertEqual(module["discovery"]["evidence_sha256"], "cb1045fbeb2dbb4309e0355fabd2cce8ee5e8bc3051803c9caec4d9bfd7edf0d")

    def test_probe_mutations_fail_closed(self) -> None:
        probe = deepcopy(load(PROBE))
        probe["dependency_surface"]["static_wiki_module_dependencies"] = ["Модуль:Unexpected"]
        with self.assertRaisesRegex(ValueError, "probe self-digest drift"):
            build_contract(load(PREDECESSOR), probe)

        probe = deepcopy(load(PROBE))
        probe["probe_sha256"] = "0" * 64
        with self.assertRaisesRegex(ValueError, "probe digest identity drift"):
            build_contract(load(PREDECESSOR), probe)

    def test_predecessor_mutation_fails_closed(self) -> None:
        predecessor = deepcopy(load(PREDECESSOR))
        predecessor["replay_contract"]["discovered_unbound_dependencies"] = []
        with self.assertRaisesRegex(ValueError, "predecessor self-digest drift"):
            build_contract(predecessor, load(PROBE))

    def test_historical_provenance_and_downstream_gates_remain_closed(self) -> None:
        contract = self.build()
        selected = contract["binding_evidence"]["selected_dependency"]
        self.assertFalse(selected["historical_transclusion_provenance_proved"])
        self.assertFalse(contract["mode_verification"]["outputs_verified"])
        self.assertFalse(contract["promotion_decision"]["render_profile_rule_promoted"])
        gates = contract["gates"]
        self.assertTrue(gates["semantic_dependency_closure_proved"])
        for key in (
            "outputs_verified",
            "renderer_semantics_complete",
            "renderer_implementation_ready",
            "render_profile_rule_promoted",
            "inter_page_composition_frozen",
            "literary_body_count_and_digests_frozen",
            "minimum_300k_proved",
            "admitted_for_calibration",
            "diagnostic_ready",
            "m2_parity_admissible",
        ):
            self.assertFalse(gates[key], key)
        self.assertEqual(gates["fantlab_source_edition_match"], "unknown")
        self.assertFalse(contract["source_text_included"])


if __name__ == "__main__":
    unittest.main()
