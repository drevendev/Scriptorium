from __future__ import annotations

from copy import deepcopy
import json
from pathlib import Path
import unittest

from scriptorium.darwin_dependency_revision_policy import (
    POLICY_SHA256,
    policy_sha256,
    validate_policy,
)


ROOT = Path(__file__).resolve().parents[1]
POLICY = ROOT / "corpus/candidates/source-edition-traces/darwin-origin-species-rachinsky-1864-ru.dependency-revision-selection-policy-v1.json"
V4 = ROOT / "corpus/candidates/source-edition-traces/darwin-origin-species-rachinsky-1864-ru.template-yo-replay-contract-v4.json"


def load(path: Path) -> dict[str, object]:
    value = json.loads(path.read_text(encoding="utf-8"))
    assert isinstance(value, dict)
    return value


class DarwinDependencyRevisionPolicyTests(unittest.TestCase):
    def test_committed_policy_validates_and_digest_is_stable(self) -> None:
        policy = load(POLICY)
        validate_policy(policy, load(V4))
        self.assertEqual(policy["policy_sha256"], POLICY_SHA256)
        self.assertEqual(policy_sha256(policy), POLICY_SHA256)

    def test_caller_timestamp_cannot_become_dependency_selector(self) -> None:
        policy = deepcopy(load(POLICY))
        policy["decision"]["caller_revision_timestamp_selects_dependency_revision"] = True
        with self.assertRaises(ValueError):
            validate_policy(policy, load(V4))

    def test_expandtemplates_revid_cannot_become_recursive_version_pin(self) -> None:
        policy = deepcopy(load(POLICY))
        policy["decision"]["expandtemplates_revid_pins_transcluded_dependency_revisions"] = True
        with self.assertRaises(ValueError):
            validate_policy(policy, load(V4))

    def test_downstream_gates_remain_open(self) -> None:
        policy = load(POLICY)
        gates = policy["gates"]
        self.assertFalse(gates["module_string_identity_bound"])
        self.assertFalse(gates["dependency_closure_complete"])
        self.assertFalse(gates["outputs_verified"])
        self.assertFalse(gates["render_profile_rule_promoted"])
        self.assertFalse(gates["minimum_300k_proved"])
        self.assertFalse(gates["m2_parity_admissible"])
        self.assertEqual(gates["fantlab_source_edition_match"], "unknown")


if __name__ == "__main__":
    unittest.main()
