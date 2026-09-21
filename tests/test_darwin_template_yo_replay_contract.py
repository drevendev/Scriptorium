from __future__ import annotations

from copy import deepcopy
import json
from pathlib import Path
import unittest

from scriptorium.darwin_template_yo_replay_contract import (
    build_contract,
    build_contract_from_path,
    validate_contract,
    validate_dependency_closure,
)


ROOT = Path(__file__).resolve().parents[1]
EVIDENCE = ROOT / "corpus/candidates/source-edition-traces/darwin-origin-species-rachinsky-1864-ru.template-yo-evidence.json"
CONTRACT = ROOT / "corpus/candidates/source-edition-traces/darwin-origin-species-rachinsky-1864-ru.template-yo-replay-contract.json"


def load(path: Path) -> dict[str, object]:
    value = json.loads(path.read_text(encoding="utf-8"))
    assert isinstance(value, dict)
    return value


class DarwinTemplateYoReplayContractTests(unittest.TestCase):
    def test_committed_contract_rebuilds_exactly(self) -> None:
        expected = build_contract_from_path(EVIDENCE)
        committed = load(CONTRACT)
        self.assertEqual(committed, expected)
        validate_contract(committed, load(EVIDENCE))
        self.assertEqual(
            committed["contract_sha256"],
            "9ac0e52c8253ef523aefe9fd54b8e90edf69095ac6f7c45ac2a0bbd584049e2b",
        )

    def test_expandtemplates_revid_is_context_not_version_pin(self) -> None:
        contract = build_contract(load(EVIDENCE))
        api = contract["official_api_evidence"]
        self.assertEqual(api["revision_id"], 6729113)
        self.assertEqual(
            api["expandtemplates_revid"]["documented_scope"],
            "revision_context_for_REVISIONID_and_similar_variables",
        )
        self.assertFalse(api["expandtemplates_revid"]["pins_transcluded_template_revisions"])
        self.assertFalse(contract["replay_contract"]["native_expandtemplates_revid_is_version_pin"])

    def test_templatesandbox_single_override_does_not_close_recursive_graph(self) -> None:
        contract = build_contract(load(EVIDENCE))
        sandbox = contract["official_api_evidence"]["templatesandbox"]
        self.assertTrue(sandbox["direct_title_text_override_supported"])
        self.assertFalse(sandbox["single_override_proves_recursive_dependency_closure"])
        self.assertFalse(contract["replay_contract"]["single_templatesandbox_override_is_closed_graph"])

    def test_required_roots_and_dependency_identity_are_explicit(self) -> None:
        replay = build_contract(load(EVIDENCE))["replay_contract"]
        self.assertEqual(replay["required_root_titles"], ["Шаблон:ё", "Шаблон:ЕЁ"])
        self.assertEqual(
            replay["required_dependency_fields"],
            ["title", "revision_id", "revision_timestamp", "mediawiki_sha1"],
        )
        self.assertTrue(replay["dependency_graph_must_be_transitively_closed"])
        self.assertFalse(replay["live_or_unbound_dependency_allowed"])
        self.assertFalse(replay["dependency_closure_complete"])

    def test_upstream_evidence_mutation_with_stale_digest_fails_closed(self) -> None:
        evidence = deepcopy(load(EVIDENCE))
        evidence["documented_semantics"] = dict(evidence["documented_semantics"])
        evidence["documented_semantics"]["forced_yoification_output"] = "е"
        with self.assertRaisesRegex(ValueError, "self-digest drift"):
            build_contract(evidence)

    def test_complete_dependency_graph_requires_both_roots(self) -> None:
        rows = [
            {
                "title": "Шаблон:ё",
                "revision_id": 1,
                "revision_timestamp": "2026-09-21T00:00:00Z",
                "mediawiki_sha1": "0" * 40,
            }
        ]
        with self.assertRaisesRegex(ValueError, "required root dependency missing"):
            validate_dependency_closure(rows, [], require_complete=True)

    def test_dependency_edge_to_unbound_title_fails_closed(self) -> None:
        rows = [
            {
                "title": "Шаблон:ё",
                "revision_id": 1,
                "revision_timestamp": "2026-09-21T00:00:00Z",
                "mediawiki_sha1": "0" * 40,
            },
            {
                "title": "Шаблон:ЕЁ",
                "revision_id": 2,
                "revision_timestamp": "2026-09-21T00:00:00Z",
                "mediawiki_sha1": "1" * 40,
            },
        ]
        edges = [{"from": "Шаблон:ё", "to": "Шаблон:missing"}]
        with self.assertRaisesRegex(ValueError, "unbound title"):
            validate_dependency_closure(rows, edges, require_complete=True)

    def test_source_body_fields_are_rejected_from_dependency_identities(self) -> None:
        rows = [
            {
                "title": "Шаблон:ё",
                "revision_id": 1,
                "revision_timestamp": "2026-09-21T00:00:00Z",
                "mediawiki_sha1": "0" * 40,
                "wikitext": "forbidden",
            }
        ]
        with self.assertRaisesRegex(ValueError, "prose leaked"):
            validate_dependency_closure(rows, [], require_complete=False)

    def test_output_and_downstream_gates_remain_open(self) -> None:
        contract = build_contract(load(EVIDENCE))
        mode = contract["mode_verification"]
        self.assertFalse(mode["outputs_verified"])
        self.assertIsNone(mode["forced_yoification"]["verified_output_sha256"])
        self.assertIsNone(mode["non_forced_yoification"]["verified_output_sha256"])
        self.assertFalse(contract["promotion_decision"]["render_profile_rule_promoted"])
        self.assertFalse(contract["promotion_decision"]["backlog_item_removed"])
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
