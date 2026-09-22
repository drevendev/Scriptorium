from __future__ import annotations

from copy import deepcopy
import json
from pathlib import Path
import unittest

from scriptorium.darwin_template_yo_replay_contract import (
    build_contract,
    build_contract_from_path,
    dependency_discovery_evidence_sha256,
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


def dependency(
    title: str,
    revision_id: int,
    sha1_char: str,
    *,
    children: tuple[str, ...] | None = None,
) -> dict[str, object]:
    row: dict[str, object] = {
        "title": title,
        "revision_id": revision_id,
        "revision_timestamp": "2026-09-22T00:00:00Z",
        "mediawiki_sha1": sha1_char * 40,
    }
    if children is not None:
        row["discovery"] = {
            "status": "complete",
            "method": "version_pinned_parser_trace",
            "direct_dependencies": list(children),
            "evidence_sha256": "0" * 64,
        }
        row["discovery"]["evidence_sha256"] = dependency_discovery_evidence_sha256(row)
    return row


class DarwinTemplateYoReplayContractTests(unittest.TestCase):
    def test_committed_contract_rebuilds_exactly(self) -> None:
        expected = build_contract_from_path(EVIDENCE)
        committed = load(CONTRACT)
        self.assertEqual(committed, expected)
        validate_contract(committed, load(EVIDENCE))
        self.assertEqual(
            committed["contract_sha256"],
            "9b2e8914a5b4c3518ef331c27dc09a6a30d4d6433e90169c677348048f3dcd52",
        )
        self.assertEqual(committed["schema_version"], "scriptorium-darwin-template-yo-replay-contract-v2")

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

    def test_recursive_expansion_evidence_is_revision_pinned(self) -> None:
        recursive = build_contract(load(EVIDENCE))["official_api_evidence"]["recursive_expansion"]
        self.assertEqual(recursive["title"], "Help:ExpandTemplates")
        self.assertEqual(recursive["revision_id"], 8168760)
        self.assertEqual(recursive["revision_date"], "2026-01-23")
        self.assertEqual(
            recursive["permanent_url"],
            "https://www.mediawiki.org/w/index.php?title=Help:ExpandTemplates&oldid=8168760",
        )
        self.assertTrue(recursive["templates_parser_functions_and_variables_expand_recursively"])

    def test_title_canonicalization_evidence_and_root_observations_are_pinned(self) -> None:
        contract = build_contract(load(EVIDENCE))
        title_evidence = contract["official_api_evidence"]["title_canonicalization"]
        self.assertEqual(title_evidence["title"], "Manual:Page naming/en")
        self.assertEqual(title_evidence["revision_id"], 8270202)
        self.assertEqual(title_evidence["revision_date"], "2026-03-07")
        self.assertTrue(title_evidence["first_page_name_character_auto_capitalized_by_default"])
        self.assertTrue(title_evidence["canonical_form_capitalizes_first_page_name_character"])

        observations = contract["root_title_observations"]
        self.assertEqual(
            observations,
            [
                {
                    "provider": "Russian Wikisource",
                    "invocation_spelling": "Шаблон:ё",
                    "canonical_title": "Шаблон:Ё",
                    "revision_id": 5687302,
                    "revision_date": "2026-01-21",
                    "permanent_url": "https://ru.wikisource.org/w/index.php?title=Шаблон:Ё&oldid=5687302",
                    "mediawiki_sha1_bound": False,
                },
                {
                    "provider": "Russian Wikisource",
                    "invocation_spelling": "Шаблон:ЕЁ",
                    "canonical_title": "Шаблон:ЕЁ",
                    "revision_id": 3684646,
                    "revision_date": "2019-06-04",
                    "permanent_url": "https://ru.wikisource.org/w/index.php?title=Шаблон:ЕЁ&oldid=3684646",
                    "mediawiki_sha1_bound": False,
                },
            ],
        )

    def test_templatesandbox_single_override_does_not_close_recursive_graph(self) -> None:
        contract = build_contract(load(EVIDENCE))
        sandbox = contract["official_api_evidence"]["templatesandbox"]
        self.assertTrue(sandbox["direct_title_text_override_supported"])
        self.assertFalse(sandbox["single_override_proves_recursive_dependency_closure"])
        self.assertFalse(contract["replay_contract"]["single_templatesandbox_override_is_closed_graph"])

    def test_required_roots_identity_and_discovery_proof_are_explicit(self) -> None:
        replay = build_contract(load(EVIDENCE))["replay_contract"]
        self.assertEqual(replay["required_root_titles"], ["Шаблон:Ё", "Шаблон:ЕЁ"])
        self.assertEqual(
            replay["required_dependency_fields"],
            ["title", "revision_id", "revision_timestamp", "mediawiki_sha1"],
        )
        self.assertEqual(
            replay["required_discovery_proof_fields"],
            ["status", "method", "direct_dependencies", "evidence_sha256"],
        )
        self.assertEqual(
            replay["dependency_discovery_evidence_schema_version"],
            "scriptorium-template-dependency-discovery-evidence-v1",
        )
        self.assertIn("exact dependency identity", replay["dependency_discovery_evidence_sha256_scope"])
        self.assertIn("canonical exact page title", replay["dependency_identity_scope"])
        self.assertTrue(replay["dependency_discovery_proof_required"])
        self.assertTrue(replay["dependency_graph_must_be_transitively_closed"])
        self.assertFalse(replay["live_or_unbound_dependency_allowed"])
        self.assertFalse(replay["dependency_closure_complete"])

    def test_upstream_evidence_mutation_with_stale_digest_fails_closed(self) -> None:
        evidence = deepcopy(load(EVIDENCE))
        evidence["documented_semantics"] = dict(evidence["documented_semantics"])
        evidence["documented_semantics"]["forced_yoification_output"] = "е"
        with self.assertRaisesRegex(ValueError, "self-digest drift"):
            build_contract(evidence)

    def test_complete_dependency_graph_requires_both_canonical_roots(self) -> None:
        rows = [dependency("Шаблон:Ё", 1, "0")]
        with self.assertRaisesRegex(ValueError, "required root dependency missing"):
            validate_dependency_closure(rows, [], require_complete=True)

    def test_lowercase_invocation_alias_cannot_satisfy_canonical_root(self) -> None:
        rows = [
            dependency("Шаблон:ё", 1, "0", children=()),
            dependency("Шаблон:ЕЁ", 2, "1", children=()),
        ]
        with self.assertRaisesRegex(ValueError, "required root dependency missing"):
            validate_dependency_closure(rows, [], require_complete=True)

    def test_two_roots_without_discovery_proof_cannot_pass_complete(self) -> None:
        rows = [
            dependency("Шаблон:Ё", 1, "0"),
            dependency("Шаблон:ЕЁ", 2, "1"),
        ]
        with self.assertRaisesRegex(ValueError, "lacks dependency discovery proof"):
            validate_dependency_closure(rows, [], require_complete=True)

    def test_explicit_discovered_leaf_roots_can_form_complete_closure(self) -> None:
        rows = [
            dependency("Шаблон:Ё", 1, "0", children=()),
            dependency("Шаблон:ЕЁ", 2, "1", children=()),
        ]
        validate_dependency_closure(rows, [], require_complete=True)

    def test_arbitrary_discovery_digest_cannot_prove_leaf(self) -> None:
        rows = [
            dependency("Шаблон:Ё", 1, "0", children=()),
            dependency("Шаблон:ЕЁ", 2, "1", children=()),
        ]
        rows[0]["discovery"]["evidence_sha256"] = "a" * 64
        with self.assertRaisesRegex(ValueError, "discovery evidence digest drift"):
            validate_dependency_closure(rows, [], require_complete=True)

    def test_stale_digest_after_direct_dependency_change_fails_closed(self) -> None:
        rows = [
            dependency("Шаблон:Ё", 1, "0", children=()),
            dependency("Шаблон:ЕЁ", 2, "1", children=()),
        ]
        rows[0]["discovery"]["direct_dependencies"] = ["Шаблон:ЕЁ"]
        with self.assertRaisesRegex(ValueError, "discovery evidence digest drift"):
            validate_dependency_closure(
                rows,
                [{"from": "Шаблон:Ё", "to": "Шаблон:ЕЁ"}],
                require_complete=True,
            )

    def test_stale_digest_after_revision_change_fails_closed(self) -> None:
        rows = [
            dependency("Шаблон:Ё", 1, "0", children=()),
            dependency("Шаблон:ЕЁ", 2, "1", children=()),
        ]
        rows[0]["revision_id"] = 999
        with self.assertRaisesRegex(ValueError, "discovery evidence digest drift"):
            validate_dependency_closure(rows, [], require_complete=True)

    def test_discovered_child_must_be_bound_and_edge_exact(self) -> None:
        rows = [
            dependency("Шаблон:Ё", 1, "0", children=("Шаблон:ЕЁ",)),
            dependency("Шаблон:ЕЁ", 2, "1", children=()),
        ]
        with self.assertRaisesRegex(ValueError, "edges do not match discovery proof"):
            validate_dependency_closure(rows, [], require_complete=True)
        validate_dependency_closure(
            rows,
            [{"from": "Шаблон:Ё", "to": "Шаблон:ЕЁ"}],
            require_complete=True,
        )

    def test_discovered_unbound_child_fails_closed(self) -> None:
        rows = [
            dependency("Шаблон:Ё", 1, "0", children=("Модуль:missing",)),
            dependency("Шаблон:ЕЁ", 2, "1", children=()),
        ]
        with self.assertRaisesRegex(ValueError, "discovered dependency remains unbound"):
            validate_dependency_closure(rows, [], require_complete=True)

    def test_dependency_edge_to_unbound_title_fails_closed(self) -> None:
        rows = [
            dependency("Шаблон:Ё", 1, "0"),
            dependency("Шаблон:ЕЁ", 2, "1"),
        ]
        edges = [{"from": "Шаблон:Ё", "to": "Шаблон:missing"}]
        with self.assertRaisesRegex(ValueError, "unbound title"):
            validate_dependency_closure(rows, edges, require_complete=True)

    def test_source_body_fields_are_rejected_from_dependency_identities(self) -> None:
        row = dependency("Шаблон:Ё", 1, "0")
        row["wikitext"] = "forbidden"
        with self.assertRaisesRegex(ValueError, "prose leaked"):
            validate_dependency_closure([row], [], require_complete=False)

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
