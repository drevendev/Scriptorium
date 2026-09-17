from __future__ import annotations

from hashlib import sha256
import json
from pathlib import Path
import unittest

from scriptorium.klim_samgin_freeze import validate_lst_contract
from scriptorium.single_page_revision import validate_manifest


ROOT = Path(__file__).resolve().parents[1]
TRACE_DIR = ROOT / "corpus" / "candidates" / "source-edition-traces"
SUMMARY_PATH = TRACE_DIR / "gorky-klim-samgin-ru.revisions.json"
DEPENDENCY_PATH = TRACE_DIR / "gorky-klim-samgin-ru.part2-part2.revision.json"
LST_CONTRACT_PATH = TRACE_DIR / "gorky-klim-samgin-ru.part2-lst.json"
EXPECTED_REVISIONS = (5733765, 5198033, 5138882, 5724453)
EXPECTED_TITLES = tuple(f"Жизнь Клима Самгина (Горький)/Часть {part}" for part in range(1, 5))
FORBIDDEN_PROSE_KEYS = {"wikitext", "content", "body", "text", "source_text"}


def _load(path: Path) -> dict[str, object]:
    value = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(value, dict):
        raise AssertionError(f"expected JSON object at {path}")
    return value


def _ordered_identity_digest(rows: list[dict[str, object]]) -> str:
    projection = [
        {key: row[key] for key in (
            "part", "title", "page_id", "revision_id", "revision_timestamp",
            "mediawiki_sha1", "wikitext_character_count", "wikitext_utf8_byte_count", "wikitext_sha256",
        )}
        for row in rows
    ]
    payload = (json.dumps(projection, ensure_ascii=False, sort_keys=True, separators=(",", ":")) + "\n").encode("utf-8")
    return sha256(payload).hexdigest()


class KlimSamginRevisionManifestTests(unittest.TestCase):
    def test_four_part_manifests_are_source_free_and_exactly_ordered(self) -> None:
        rows: list[dict[str, object]] = []
        page_ids: set[int] = set()
        wikitext_digests: set[str] = set()
        for part, expected_revision, expected_title in zip(range(1, 5), EXPECTED_REVISIONS, EXPECTED_TITLES, strict=True):
            manifest = _load(TRACE_DIR / f"gorky-klim-samgin-ru.part{part}.revision.json")
            validate_manifest(manifest)
            self.assertEqual(manifest["candidate_id"], f"gorky-klim-samgin-ru-part-{part}")
            self.assertEqual(manifest["capture_scope"], {
                "composite_identity_frozen": False,
                "literary_body_extraction_frozen": False,
                "revision_wikitext_identity_frozen": True,
                "source_text_committed": False,
            })
            identity = manifest["source_identity"]
            self.assertIsInstance(identity, dict)
            assert isinstance(identity, dict)
            self.assertEqual(identity["revision_id"], expected_revision)
            self.assertEqual(identity["title"], expected_title)
            self.assertFalse(FORBIDDEN_PROSE_KEYS.intersection(identity))
            self.assertNotIn("source_text", manifest)
            page_id = identity["page_id"]
            digest = identity["wikitext_sha256"]
            self.assertIsInstance(page_id, int)
            self.assertIsInstance(digest, str)
            assert isinstance(page_id, int) and isinstance(digest, str)
            page_ids.add(page_id)
            wikitext_digests.add(digest)
            rows.append({"part": part, **identity})
        self.assertEqual(len(page_ids), 4)
        self.assertEqual(len(wikitext_digests), 4)
        summary = _load(SUMMARY_PATH)
        self.assertEqual(summary["manifest_version"], "scriptorium-multi-page-source-revision-set-v2")
        self.assertEqual(summary["candidate_id"], "gorky-klim-samgin-ru")
        self.assertEqual(summary["ordered_revision_identity_sha256"], _ordered_identity_digest(rows))
        self.assertEqual(summary["total_revision_wikitext_character_count"], sum(int(row["wikitext_character_count"]) for row in rows))
        self.assertEqual(summary["total_revision_wikitext_utf8_byte_count"], sum(int(row["wikitext_utf8_byte_count"]) for row in rows))

    def test_hidden_part2_transclusion_is_independently_pinned_and_source_free(self) -> None:
        dependency = _load(DEPENDENCY_PATH)
        validate_manifest(dependency)
        self.assertEqual(dependency["candidate_id"], "gorky-klim-samgin-ru-part-2-part2")
        self.assertEqual(dependency["capture_scope"], {
            "composite_identity_frozen": False,
            "literary_body_extraction_frozen": False,
            "revision_wikitext_identity_frozen": True,
            "source_text_committed": False,
        })
        identity = dependency["source_identity"]
        self.assertIsInstance(identity, dict)
        assert isinstance(identity, dict)
        self.assertEqual(identity["title"], "Жизнь Клима Самгина (Горький)/Часть 2/part2")
        self.assertEqual(identity["revision_id"], 2366546)
        self.assertEqual(identity["page_id"], 580081)
        self.assertEqual(identity["wikitext_character_count"], 583889)
        self.assertEqual(identity["wikitext_utf8_byte_count"], 1058733)
        self.assertEqual(identity["wikitext_sha256"], "173054997b54b96241adc07aeb6f76624beb497f94602452d7f9e4e57b0c6996")
        self.assertFalse(FORBIDDEN_PROSE_KEYS.intersection(identity))
        self.assertNotIn("source_text", dependency)
        summary = _load(SUMMARY_PATH)
        dependencies = summary["transclusion_dependencies"]
        self.assertEqual(len(dependencies), 1)
        self.assertEqual(dependencies[0]["revision_id"], 2366546)
        self.assertEqual(dependencies[0]["manifest"], "corpus/candidates/source-edition-traces/gorky-klim-samgin-ru.part2-part2.revision.json")

    def test_target_only_lst_contract_is_source_free_and_bound_to_pinned_revisions(self) -> None:
        contract = _load(LST_CONTRACT_PATH)
        parent = _load(TRACE_DIR / "gorky-klim-samgin-ru.part2.revision.json")
        dependency = _load(DEPENDENCY_PATH)
        validate_lst_contract(contract, parent_revision_manifest=parent, dependency_revision_manifest=dependency)
        self.assertEqual(contract["invocation"]["argument_count"], 1)
        self.assertIsNone(contract["invocation"]["section_label"])
        self.assertEqual(contract["dependency_shape"]["section_tag_count"], 0)
        self.assertEqual(contract["dependency_shape"]["lst_invocation_count"], 0)
        self.assertEqual(contract["dependency_shape"]["template_name_counts"], {"poemx1": 6})
        self.assertIs(contract["capture_scope"]["mediawiki_template_dom_expansion_reproduced"], False)
        self.assertIs(contract["capture_scope"]["resolved_part2_wikitext_identity_frozen"], False)
        self.assertFalse(FORBIDDEN_PROSE_KEYS.intersection(contract))

    def test_summary_stays_fail_closed_for_body_and_fantlab_identity(self) -> None:
        summary = _load(SUMMARY_PATH)
        self.assertEqual(summary["capture_scope"], {
            "all_part_revision_wikitext_identities_frozen": True,
            "composite_literary_body_identity_frozen": False,
            "literary_body_extraction_frozen": False,
            "literary_composition_frozen": False,
            "part2_target_only_lst_semantics_frozen": True,
            "resolved_part2_wikitext_identity_frozen": False,
            "source_text_committed": False,
            "transclusion_dependency_revision_wikitext_identities_frozen": True,
        })
        self.assertEqual(summary["part2_transclusion_contract"], "corpus/candidates/source-edition-traces/gorky-klim-samgin-ru.part2-lst.json")
        self.assertEqual(summary["fantlab_source_edition_match"], "unknown")
        self.assertIs(summary["diagnostic_ready"], False)
        self.assertIs(summary["gate_ready"], False)
        self.assertIs(summary["m2_parity_admissible"], False)
        self.assertFalse(FORBIDDEN_PROSE_KEYS.intersection(summary))
        self.assertEqual([row["revision_id"] for row in summary["part_manifests"]], list(EXPECTED_REVISIONS))


if __name__ == "__main__":
    unittest.main()
