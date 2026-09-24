from __future__ import annotations

import json
from pathlib import Path
import re
import unittest

from scriptorium.darwin_var_revision_identities import RESOURCES, build_evidence, validate_evidence


ROOT = Path(__file__).resolve().parents[1]
EVIDENCE = ROOT / "corpus/candidates/source-edition-traces/darwin-origin-species-rachinsky-1864-ru.var-revision-identities-evidence.json"


class DarwinVarRevisionIdentityTests(unittest.TestCase):
    def setUp(self) -> None:
        self.evidence = json.loads(EVIDENCE.read_text(encoding="utf-8"))

    def test_committed_evidence_rebuilds_exactly(self) -> None:
        self.assertEqual(self.evidence, build_evidence())
        validate_evidence(self.evidence)

    def test_exact_six_revision_set_is_bound(self) -> None:
        resources = self.evidence["resources"]
        expected = [
            (closure_title, provider_title, revision_id)
            for closure_title, provider_title, _page_id, revision_id, _timestamp, _sha1, _chars, _bytes, _sha256 in RESOURCES
        ]
        self.assertEqual(
            [(item["closure_title"], item["title"], item["revision_id"]) for item in resources],
            expected,
        )
        self.assertEqual(len(resources), 6)

    def test_provider_namespace_aliases_are_explicit(self) -> None:
        resources = {item["closure_title"]: item for item in self.evidence["resources"]}
        self.assertEqual(resources["Module:Header"]["title"], "Модуль:Header")
        self.assertEqual(resources["Module:BEED"]["title"], "Модуль:BEED")
        self.assertEqual(resources["Module:Util"]["title"], "Модуль:Util")
        self.assertEqual(resources["Module:RomanNumber"]["title"], "Модуль:RomanNumber")
        self.assertEqual(resources["Шаблон:ВАР"]["title"], "Шаблон:ВАР")
        self.assertEqual(
            resources["Модуль:Дореформенная орфография"]["title"],
            "Модуль:Дореформенная орфография",
        )

    def test_mediawiki_sha1_identity_gate_is_complete(self) -> None:
        gate = self.evidence["identity_gate"]
        self.assertTrue(gate["revision_ids_complete"])
        self.assertTrue(gate["mediawiki_sha1_complete"])
        self.assertTrue(gate["provider_title_aliases_explicit"])
        self.assertEqual(gate["missing_mediawiki_sha1_titles"], [])
        self.assertTrue(
            all(
                re.fullmatch(r"[0-9a-f]{40}", item["mediawiki_sha1"])
                for item in self.evidence["resources"]
            )
        )

    def test_provider_identity_rows_are_exact(self) -> None:
        resources = {item["closure_title"]: item for item in self.evidence["resources"]}
        self.assertEqual(resources["Шаблон:ВАР"]["mediawiki_sha1"], "fdb6fa7c0d4b08157bc30d44f5f77c5b9313167c")
        self.assertEqual(resources["Модуль:Дореформенная орфография"]["mediawiki_sha1"], "64d28378f4f620c67e1823a0d4292445d9ab293d")
        self.assertEqual(resources["Module:Header"]["mediawiki_sha1"], "2ab2bfdd7e49c73c4ec9ef24e4625c1d228cfba0")
        self.assertEqual(resources["Module:BEED"]["mediawiki_sha1"], "9e9531e9178e0333bd3a939ace91e6a71e114cc5")
        self.assertEqual(resources["Module:Util"]["mediawiki_sha1"], "945f8e6bf173bb5712385995255a8b6eccef38ed")
        self.assertEqual(resources["Module:RomanNumber"]["mediawiki_sha1"], "51a3956469ee3fbd4ed56ce3a1f72f76f231e1d3")
        self.assertEqual(resources["Module:Header"]["page_id"], 361783)
        self.assertEqual(resources["Module:Header"]["revision_timestamp"], "2026-09-10T02:29:30Z")

    def test_identity_completion_does_not_open_replay_or_parity(self) -> None:
        self.assertFalse(self.evidence["identity_gate"]["replay_ready"])
        self.assertFalse(self.evidence["historical_transclusion_proven"])
        self.assertFalse(self.evidence["offline_version_pinned_runtime_proven"])
        decision = self.evidence["promotion_decision"]
        self.assertEqual(decision["var_invocations_unresolved"], 388)
        self.assertFalse(decision["full_var_candidate_branch_replayed"])
        self.assertFalse(decision["render_profile_rule_promoted"])
        self.assertFalse(decision["backlog_item_removed"])
        self.assertFalse(decision["effective_backlog_changed"])
        self.assertFalse(self.evidence["renderer_semantics_complete"])
        self.assertFalse(self.evidence["literary_body_count_and_digests_frozen"])
        self.assertFalse(self.evidence["minimum_300k_proved"])
        self.assertEqual(self.evidence["fantlab_source_edition_match"], "unknown")
        self.assertFalse(self.evidence["m2_parity_admissible"])


if __name__ == "__main__":
    unittest.main()
