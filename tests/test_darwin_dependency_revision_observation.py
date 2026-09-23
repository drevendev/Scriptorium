from __future__ import annotations

from copy import deepcopy
import json
from pathlib import Path
import unittest

from scriptorium.darwin_dependency_revision_observation import (
    DEPENDENCY_TITLE,
    build_observation,
    observation_sha256,
    validate_observation,
)

ROOT = Path(__file__).resolve().parents[1]
V4 = ROOT / "corpus/candidates/source-edition-traces/darwin-origin-species-rachinsky-1864-ru.template-yo-replay-contract-v4.json"
POLICY = ROOT / "corpus/candidates/source-edition-traces/darwin-origin-species-rachinsky-1864-ru.dependency-revision-selection-policy-v1.json"


def load(path: Path) -> dict[str, object]:
    value = json.loads(path.read_text(encoding="utf-8"))
    assert isinstance(value, dict)
    return value


def api_payload() -> dict[str, object]:
    return {
        "curtimestamp": "2026-09-23T05:55:00Z",
        "query": {
            "pages": [
                {
                    "pageid": 123,
                    "ns": 828,
                    "title": DEPENDENCY_TITLE,
                    "revisions": [
                        {
                            "revid": 6543210,
                            "parentid": 6543200,
                            "timestamp": "2026-09-20T10:11:12Z",
                            "sha1": "0123456789abcdef0123456789abcdef01234567",
                        }
                    ],
                }
            ]
        },
    }


class DarwinDependencyRevisionObservationTests(unittest.TestCase):
    def test_source_free_observation_validates_and_digest_is_stable(self) -> None:
        observation = build_observation(api_payload())
        validate_observation(observation, load(V4), load(POLICY))
        self.assertEqual(observation["observation_sha256"], observation_sha256(observation))
        self.assertEqual(observation["identity"]["canonical_title"], DEPENDENCY_TITLE)
        self.assertFalse(observation["gates"]["module_string_identity_bound"])
        self.assertFalse(observation["gates"]["dependency_closure_complete"])

    def test_canonical_title_drift_fails_closed(self) -> None:
        payload = api_payload()
        payload["query"]["pages"][0]["title"] = "Модуль:string"
        with self.assertRaises(ValueError):
            build_observation(payload)

    def test_source_content_is_rejected(self) -> None:
        payload = api_payload()
        payload["query"]["pages"][0]["revisions"][0]["slots"] = {
            "main": {"content": "not retained"}
        }
        with self.assertRaises(ValueError):
            build_observation(payload)

    def test_observation_context_cannot_be_removed(self) -> None:
        observation = build_observation(api_payload())
        observation["observation_context"].pop("observed_at")
        observation["observation_sha256"] = observation_sha256(observation)
        with self.assertRaises(ValueError):
            validate_observation(observation, load(V4), load(POLICY))

    def test_downstream_gates_remain_open(self) -> None:
        gates = build_observation(api_payload())["gates"]
        self.assertTrue(gates["module_string_identity_observed"])
        self.assertFalse(gates["module_string_identity_bound"])
        self.assertFalse(gates["dependency_closure_complete"])
        self.assertFalse(gates["outputs_verified"])
        self.assertFalse(gates["render_profile_rule_promoted"])
        self.assertFalse(gates["minimum_300k_proved"])
        self.assertFalse(gates["m2_parity_admissible"])
        self.assertEqual(gates["fantlab_source_edition_match"], "unknown")


if __name__ == "__main__":
    unittest.main()
