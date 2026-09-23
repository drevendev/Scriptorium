from __future__ import annotations

import json
from pathlib import Path
import unittest

from scriptorium.darwin_module_string_dependency_probe import (
    _assert_source_free,
    probe_sha256,
)


ROOT = Path(__file__).resolve().parents[1]
PROBE = ROOT / "corpus/candidates/source-edition-traces/darwin-origin-species-rachinsky-1864-ru.module-string-dependency-probe-v1.json"
EXPECTED_PROBE_SHA256 = "e27a2af9f01c760f995c633e296e1d5825642d4c4bcbeb5fba8ae0a697c234cb"


def load_probe() -> dict[str, object]:
    value = json.loads(PROBE.read_text(encoding="utf-8"))
    assert isinstance(value, dict)
    return value


class DarwinModuleStringDependencyProbeFreezeTests(unittest.TestCase):
    def test_canonical_probe_digest_and_identity_are_frozen(self) -> None:
        probe = load_probe()
        self.assertEqual(probe["probe_sha256"], EXPECTED_PROBE_SHA256)
        self.assertEqual(probe_sha256(probe), EXPECTED_PROBE_SHA256)
        self.assertEqual(probe["schema_version"], "scriptorium-darwin-module-string-dependency-probe-v1")
        self.assertEqual(probe["identity"]["canonical_title"], "Модуль:String")
        self.assertEqual(probe["identity"]["revision_id"], 3684569)
        self.assertEqual(probe["identity"]["revision_timestamp"], "2019-06-04T20:18:11Z")
        self.assertEqual(probe["identity"]["mediawiki_sha1"], "a34727a1e4ec3c4b4c7ec556c94991f75442d99c")
        _assert_source_free(probe)
        self.assertFalse(probe["source_text_included"])

    def test_canonical_dependency_surface_preserves_fail_closed_boundary(self) -> None:
        probe = load_probe()
        surface = probe["dependency_surface"]
        self.assertEqual(surface["source_utf8_bytes"], 18468)
        self.assertEqual(surface["source_sha256"], "258cec6ab8b4c1e3eb0e812d72d39f4302f321a4d1fdd7aa3883187db0eecb03")
        self.assertEqual(surface["static_wiki_module_dependencies"], [])
        self.assertEqual(surface["non_wiki_require_literals"], [])
        self.assertEqual(surface["dynamic_or_unsupported_loader_calls"], [])
        self.assertTrue(surface["scan_complete"])
        self.assertFalse(surface["semantic_dependency_closure_proved"])

    def test_downstream_gates_remain_closed(self) -> None:
        gates = load_probe()["gates"]
        self.assertTrue(gates["module_string_dependency_surface_probed"])
        self.assertFalse(gates["module_string_identity_bound"])
        self.assertFalse(gates["dependency_closure_complete"])
        self.assertFalse(gates["outputs_verified"])
        self.assertFalse(gates["render_profile_rule_promoted"])
        self.assertFalse(gates["literary_body_count_and_digests_frozen"])
        self.assertFalse(gates["minimum_300k_proved"])
        self.assertEqual(gates["fantlab_source_edition_match"], "unknown")
        self.assertFalse(gates["m2_parity_admissible"])


if __name__ == "__main__":
    unittest.main()
