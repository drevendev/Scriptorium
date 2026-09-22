from __future__ import annotations

from copy import deepcopy
import json
from pathlib import Path
import unittest

from scriptorium.darwin_template_yo_replay_contract import validate_dependency_closure
from scriptorium.darwin_template_yo_replay_contract_v3 import (
    CONTRACT_VERSION,
    PREDECESSOR_SHA256,
    ROOT_IDENTITIES,
    build_contract,
    build_contract_from_paths,
    validate_contract,
)


ROOT = Path(__file__).resolve().parents[1]
EVIDENCE = ROOT / "corpus/candidates/source-edition-traces/darwin-origin-species-rachinsky-1864-ru.template-yo-evidence.json"
PREDECESSOR = ROOT / "corpus/candidates/source-edition-traces/darwin-origin-species-rachinsky-1864-ru.template-yo-replay-contract.json"
CONTRACT = ROOT / "corpus/candidates/source-edition-traces/darwin-origin-species-rachinsky-1864-ru.template-yo-replay-contract-v3.json"


def load(path: Path) -> dict[str, object]:
    value = json.loads(path.read_text(encoding="utf-8"))
    assert isinstance(value, dict)
    return value


class DarwinTemplateYoReplayContractV3Tests(unittest.TestCase):
    def test_committed_contract_rebuilds_exactly(self) -> None:
        expected = build_contract_from_paths(EVIDENCE, PREDECESSOR)
        committed = load(CONTRACT)
        self.assertEqual(committed, expected)
        validate_contract(committed, load(EVIDENCE), load(PREDECESSOR))
        self.assertEqual(committed["schema_version"], CONTRACT_VERSION)
        self.assertEqual(
            committed["contract_sha256"],
            "8caa144d9f4c0b9a8149c1822bd79d168d212dea14d72079c3259d55e5e03c8c",
        )
        self.assertEqual(committed["predecessor_contract"]["contract_sha256"], PREDECESSOR_SHA256)

    def test_exact_root_identity_surface_is_source_free(self) -> None:
        contract = build_contract(load(EVIDENCE), load(PREDECESSOR))
        observations = contract["root_title_observations"]
        dependencies = contract["replay_contract"]["dependencies"]
        self.assertEqual(dependencies, [dict(row) for row in ROOT_IDENTITIES])
        self.assertTrue(contract["replay_contract"]["root_identities_bound"])
        for observation, identity in zip(observations, ROOT_IDENTITIES, strict=True):
            self.assertEqual(observation["canonical_title"], identity["title"])
            self.assertEqual(observation["revision_id"], identity["revision_id"])
            self.assertEqual(observation["revision_timestamp"], identity["revision_timestamp"])
            self.assertEqual(observation["mediawiki_sha1"], identity["mediawiki_sha1"])
            self.assertTrue(observation["mediawiki_sha1_bound"])
            self.assertFalse({"content", "text", "wikitext", "body", "source_text"}.intersection(observation))
        self.assertFalse(contract["source_text_included"])

    def test_api_identity_query_explicitly_excludes_content(self) -> None:
        query = build_contract(load(EVIDENCE), load(PREDECESSOR))["official_api_evidence"]["revision_identity_query"]
        self.assertEqual(query["endpoint"], "https://ru.wikisource.org/w/api.php")
        self.assertEqual(query["query_mode"], "revids")
        self.assertEqual(query["rvprop"], "ids|timestamp|sha1")
        self.assertEqual(query["sha1_encoding"], "base16")
        self.assertFalse(query["source_content_requested"])

    def test_recursive_closure_remains_open_after_root_binding(self) -> None:
        contract = build_contract(load(EVIDENCE), load(PREDECESSOR))
        replay = contract["replay_contract"]
        self.assertEqual(replay["edges"], [])
        self.assertFalse(replay["dependency_closure_complete"])
        with self.assertRaisesRegex(ValueError, "lacks dependency discovery proof"):
            validate_dependency_closure(replay["dependencies"], replay["edges"], require_complete=True)

    def test_predecessor_digest_drift_fails_closed(self) -> None:
        predecessor = deepcopy(load(PREDECESSOR))
        predecessor["contract_sha256"] = "0" * 64
        with self.assertRaises(ValueError):
            build_contract(load(EVIDENCE), predecessor)

    def test_root_sha1_mutation_fails_closed(self) -> None:
        contract = deepcopy(build_contract(load(EVIDENCE), load(PREDECESSOR)))
        contract["root_title_observations"][0]["mediawiki_sha1"] = "0" * 40
        with self.assertRaisesRegex(ValueError, "v3 contract drift"):
            validate_contract(contract, load(EVIDENCE), load(PREDECESSOR))

    def test_downstream_gates_remain_closed(self) -> None:
        contract = build_contract(load(EVIDENCE), load(PREDECESSOR))
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
