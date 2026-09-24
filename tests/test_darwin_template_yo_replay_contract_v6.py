from __future__ import annotations

from copy import deepcopy
import json
from pathlib import Path
import unittest

from scriptorium.darwin_template_yo_replay_contract_v6 import (
    BOUND_IDENTITIES,
    CONTRACT_VERSION,
    MODES,
    PREDECESSOR_SHA256,
    build_contract,
    build_contract_from_path,
    normalize_semantic_output,
    validate_contract,
    verify_identity_window,
    verify_mode_replays,
)


ROOT = Path(__file__).resolve().parents[1]
PREDECESSOR = ROOT / "corpus/candidates/source-edition-traces/darwin-origin-species-rachinsky-1864-ru.template-yo-replay-contract-v5.json"
CONTRACT = ROOT / "corpus/candidates/source-edition-traces/darwin-origin-species-rachinsky-1864-ru.template-yo-replay-contract-v6.json"


def load(path: Path) -> dict[str, object]:
    value = json.loads(path.read_text(encoding="utf-8"))
    assert isinstance(value, dict)
    return value


def identity_payload(rows=BOUND_IDENTITIES) -> dict[str, object]:
    return {
        "query": {
            "pages": [
                {
                    "title": row["title"],
                    "revisions": [
                        {
                            "revid": row["revision_id"],
                            "timestamp": row["revision_timestamp"],
                            "sha1": row["mediawiki_sha1"],
                        }
                    ],
                }
                for row in rows
            ]
        }
    }


def replay_payload(output: str) -> dict[str, object]:
    return {"expandtemplates": {"wikitext": output}}


class DarwinTemplateYoReplayContractV6Tests(unittest.TestCase):
    def build(self) -> dict[str, object]:
        return build_contract(load(PREDECESSOR))

    def test_committed_contract_is_exact_deterministic_build(self) -> None:
        expected = build_contract_from_path(PREDECESSOR)
        actual = load(CONTRACT)
        self.assertEqual(actual, expected)
        self.assertEqual(actual["schema_version"], CONTRACT_VERSION)
        self.assertEqual(actual["predecessor_contract"]["contract_sha256"], PREDECESSOR_SHA256)
        validate_contract(actual, load(PREDECESSOR))

    def test_mode_outputs_are_frozen_but_profile_promotion_stays_separate(self) -> None:
        contract = self.build()
        self.assertTrue(contract["mode_verification"]["outputs_verified"])
        self.assertEqual(
            contract["mode_verification"]["forced_yoification"]["verified_semantic_output"],
            "ё",
        )
        self.assertEqual(
            contract["mode_verification"]["non_forced_yoification"]["verified_semantic_output"],
            "е",
        )
        self.assertFalse(contract["promotion_decision"]["render_profile_rule_promoted"])
        self.assertFalse(contract["promotion_decision"]["backlog_item_removed"])
        gates = contract["gates"]
        self.assertTrue(gates["semantic_dependency_closure_proved"])
        self.assertTrue(gates["zero_argument_template_yo_outputs_verified"])
        self.assertTrue(gates["outputs_verified"])
        for key in (
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

    def test_identity_window_requires_all_three_exact_current_revisions(self) -> None:
        before = identity_payload()
        after = identity_payload()
        verify_identity_window(before, after)

        drifted = deepcopy(after)
        drifted["query"]["pages"][2]["revisions"][0]["revid"] += 1
        with self.assertRaisesRegex(ValueError, "post-window dependency identity drift"):
            verify_identity_window(before, drifted)

    def test_replay_requires_two_identical_semantic_outputs_per_mode(self) -> None:
        contract = self.build()
        payloads = {
            "forced_yoification": [replay_payload(" ё \n"), replay_payload("ё")],
            "non_forced_yoification": [replay_payload("\nе"), replay_payload("е ")],
        }
        verified = verify_mode_replays(contract, payloads)
        self.assertEqual(
            verified["forced_yoification"],
            contract["mode_verification"]["forced_yoification"]["verified_semantic_output_sha256"],
        )
        self.assertEqual(
            verified["non_forced_yoification"],
            contract["mode_verification"]["non_forced_yoification"]["verified_semantic_output_sha256"],
        )

        nondeterministic = deepcopy(payloads)
        nondeterministic["forced_yoification"][1] = replay_payload("е")
        with self.assertRaisesRegex(ValueError, "nondeterministic"):
            verify_mode_replays(contract, nondeterministic)

    def test_normalization_is_explicit_and_nfc(self) -> None:
        self.assertEqual(normalize_semantic_output("  е\u0308\n"), "ё")
        self.assertEqual(normalize_semantic_output("\tе "), "е")

    def test_predecessor_or_contract_mutation_fails_closed(self) -> None:
        predecessor = deepcopy(load(PREDECESSOR))
        predecessor["contract_sha256"] = "0" * 64
        with self.assertRaisesRegex(ValueError, "predecessor digest identity drift"):
            build_contract(predecessor)

        contract = self.build()
        contract["replay_environment"]["identity_stable_window_required"] = False
        with self.assertRaisesRegex(ValueError, "contract drift"):
            validate_contract(contract, load(PREDECESSOR))

    def test_contract_does_not_claim_historical_or_offline_pinning(self) -> None:
        contract = self.build()
        environment = contract["replay_environment"]
        self.assertFalse(environment["revid_used_as_recursive_dependency_selector"])
        self.assertFalse(environment["offline_version_pinned_mediawiki_environment_claimed"])
        self.assertFalse(environment["historical_transclusion_provenance_proved"])
        self.assertTrue(environment["identity_stable_window_required"])
        self.assertEqual(
            environment["current_revision_identities_required_before_and_after"],
            [dict(row) for row in BOUND_IDENTITIES],
        )
        self.assertFalse(contract["source_text_included"])
        self.assertEqual(
            contract["mode_verification"]["forced_yoification"]["context_title"],
            MODES["forced_yoification"]["context_title"],
        )
        self.assertEqual(
            contract["mode_verification"]["non_forced_yoification"]["context_title"],
            MODES["non_forced_yoification"]["context_title"],
        )


if __name__ == "__main__":
    unittest.main()
