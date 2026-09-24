from __future__ import annotations

from copy import deepcopy
import json
from pathlib import Path
import unittest

from scriptorium.darwin_references_containment import (
    BACKLOG_SHA256,
    EXPECTED_REFERENCES_COUNT,
    PROFILE_PROMOTION_SHA256,
    PROBE_SCHEMA,
    SOURCE_REVISION_INDEX_SHA256,
    audit_reference_containment,
    build_probe_contract,
    validate_probe,
)


ROOT = Path(__file__).resolve().parents[1]
TRACE = ROOT / "corpus/candidates/source-edition-traces"
SURFACE = TRACE / "darwin-origin-species-rachinsky-1864-ru.render-surface.json"
PROMOTION = TRACE / "darwin-origin-species-rachinsky-1864-ru.render-profile-yo-promotion-v1.json"
BACKLOG = TRACE / "darwin-origin-species-rachinsky-1864-ru.semantic-backlog-v2.json"
PROBE = TRACE / "darwin-origin-species-rachinsky-1864-ru.references-containment-v1.json"


def load(path: Path) -> dict[str, object]:
    value = json.loads(path.read_text(encoding="utf-8"))
    assert isinstance(value, dict)
    return value


class DarwinReferencesContainmentTests(unittest.TestCase):
    def test_reference_inside_noinclude_is_proved(self) -> None:
        evidence = audit_reference_containment(
            "literary text<noinclude><references /></noinclude>tail"
        )
        self.assertEqual(
            evidence,
            {
                "references_total": 1,
                "references_inside_noinclude": 1,
                "references_outside_noinclude": 0,
                "all_observed_references_inside_noinclude": True,
            },
        )

    def test_reference_outside_noinclude_is_not_silently_dropped(self) -> None:
        evidence = audit_reference_containment(
            "<noinclude>metadata</noinclude>literary<references/>"
        )
        self.assertEqual(evidence["references_total"], 1)
        self.assertEqual(evidence["references_inside_noinclude"], 0)
        self.assertEqual(evidence["references_outside_noinclude"], 1)
        self.assertFalse(evidence["all_observed_references_inside_noinclude"])

    def test_non_self_closing_references_shape_fails_closed(self) -> None:
        with self.assertRaisesRegex(ValueError, "non-self-closing"):
            audit_reference_containment(
                "<noinclude><references></references></noinclude>"
            )

    def test_committed_probe_rebuilds_from_frozen_predecessors(self) -> None:
        surface = load(SURFACE)
        promotion = load(PROMOTION)
        backlog = load(BACKLOG)
        expected = build_probe_contract(
            surface,
            promotion,
            backlog,
            source_revision_index_sha256=SOURCE_REVISION_INDEX_SHA256,
            literary_dependency_count=388,
            references_total=EXPECTED_REFERENCES_COUNT,
            references_inside_noinclude=EXPECTED_REFERENCES_COUNT,
            references_outside_noinclude=0,
        )
        self.assertEqual(expected["schema_version"], PROBE_SCHEMA)
        self.assertEqual(expected["effective_state"]["profile_promotion_sha256"], PROFILE_PROMOTION_SHA256)
        self.assertEqual(expected["effective_state"]["semantic_backlog_sha256"], BACKLOG_SHA256)
        self.assertEqual(load(PROBE), expected)
        validate_probe(load(PROBE), surface, promotion, backlog)

    def test_predecessor_backlog_drift_fails_closed(self) -> None:
        backlog = deepcopy(load(BACKLOG))
        backlog["backlog_sha256"] = "0" * 64
        with self.assertRaisesRegex(ValueError, "semantic-backlog identity drift"):
            build_probe_contract(
                load(SURFACE),
                load(PROMOTION),
                backlog,
                source_revision_index_sha256=SOURCE_REVISION_INDEX_SHA256,
                literary_dependency_count=388,
                references_total=388,
                references_inside_noinclude=388,
                references_outside_noinclude=0,
            )

    def test_probe_does_not_promote_or_open_downstream_gates(self) -> None:
        probe = load(PROBE)
        self.assertFalse(probe["source_text_included"])
        self.assertTrue(probe["containment_evidence"]["all_observed_references_inside_noinclude"])
        self.assertTrue(probe["promotion_decision"]["candidate_local_drop_supported_by_containment"])
        self.assertFalse(probe["promotion_decision"]["provider_cite_semantics_replayed"])
        self.assertFalse(probe["promotion_decision"]["profile_rule_promoted"])
        for key in (
            "renderer_semantics_complete",
            "renderer_implementation_ready",
            "historical_transclusion_provenance_proved",
            "offline_version_pinned_mediawiki_environment_claimed",
            "inter_page_composition_frozen",
            "literary_body_count_and_digests_frozen",
            "minimum_300k_proved",
            "admitted_for_calibration",
            "diagnostic_ready",
            "m2_parity_admissible",
        ):
            self.assertFalse(probe[key], key)
        self.assertEqual(probe["fantlab_source_edition_match"], "unknown")


if __name__ == "__main__":
    unittest.main()
