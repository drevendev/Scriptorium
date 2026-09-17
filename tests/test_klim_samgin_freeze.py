from __future__ import annotations

from hashlib import sha256
import unittest

from scriptorium.klim_samgin_freeze import (
    DEPENDENCY_CANDIDATE_ID,
    DEPENDENCY_TITLE,
    LST_CONTRACT_VERSION,
    LST_SELECTION_PROFILE,
    PART2_CANDIDATE_ID,
    UPSTREAM_EVIDENCE_COMMIT,
    build_lst_contract,
    parse_target_only_lst_invocation,
    replay_lst_contract,
    validate_lst_contract,
)


def _identity(title: str, revision_id: int, page_id: int, wikitext: str) -> dict[str, object]:
    raw = wikitext.encode("utf-8")
    return {
        "title": title,
        "page_id": page_id,
        "revision_id": revision_id,
        "revision_timestamp": "2026-01-01T00:00:00Z",
        "mediawiki_sha1": "a" * 40,
        "wikitext_character_count": len(wikitext),
        "wikitext_utf8_byte_count": len(raw),
        "wikitext_sha256": sha256(raw).hexdigest(),
    }


def _manifest(candidate_id: str, title: str, revision_id: int, page_id: int, wikitext: str) -> dict[str, object]:
    return {
        "manifest_version": "scriptorium-single-page-source-revision-v1",
        "candidate_id": candidate_id,
        "provider": "Russian Wikisource",
        "source_work_url": "https://example.invalid/work",
        "permanent_source_url": "https://example.invalid/permanent",
        "bibliographic_source": "fixture",
        "legal_basis": "public_domain_original_russian_work",
        "source_identity": _identity(title, revision_id, page_id, wikitext),
        "capture_scope": {
            "revision_wikitext_identity_frozen": True,
            "literary_body_extraction_frozen": False,
            "composite_identity_frozen": False,
            "source_text_committed": False,
        },
    }


class KlimSamginLstTests(unittest.TestCase):
    def test_target_only_invocation_freezes_target_and_placement(self) -> None:
        source = "prefix\n{{#lst:Page/Subpage}}\nsuffix"
        invocation = parse_target_only_lst_invocation(source)
        self.assertEqual(invocation["argument_count"], 1)
        self.assertEqual(invocation["target_title"], "Page/Subpage")
        self.assertIsNone(invocation["section_label"])
        self.assertIsNone(invocation["range_end_label"])
        self.assertEqual(
            source[invocation["parent_start_offset"]:invocation["parent_end_offset"]],
            "{{#lst:Page/Subpage}}",
        )

    def test_target_only_parser_rejects_section_range_and_multiple_calls(self) -> None:
        with self.assertRaisesRegex(ValueError, "target-only"):
            parse_target_only_lst_invocation("{{#lst:Page|section}}")
        with self.assertRaisesRegex(ValueError, "target-only"):
            parse_target_only_lst_invocation("{{#lst:Page|a|b}}")
        with self.assertRaisesRegex(ValueError, "exactly one"):
            parse_target_only_lst_invocation("{{#lst:Page}}{{#lst:Other}}")

    def test_contract_freezes_semantic_branch_not_expanded_part2_bytes(self) -> None:
        parent_text = "before\n{{#lst:" + DEPENDENCY_TITLE + "}}\nafter"
        dependency_text = "dependency {{TemplateA}} payload"
        parent = _manifest(PART2_CANDIDATE_ID, "Жизнь Клима Самгина (Горький)/Часть 2", 10, 1, parent_text)
        dependency = _manifest(DEPENDENCY_CANDIDATE_ID, DEPENDENCY_TITLE, 11, 2, dependency_text)
        lookup = {
            (parent["source_identity"]["title"], 10): parent_text,
            (DEPENDENCY_TITLE, 11): dependency_text,
        }

        def fetcher(*, title: str, revision_id: int) -> dict[str, object]:
            text = lookup[(title, revision_id)]
            manifest = parent if revision_id == 10 else dependency
            return {**manifest["source_identity"], "wikitext": text}

        contract = build_lst_contract(parent, dependency, fetcher=fetcher)
        validate_lst_contract(contract, parent_revision_manifest=parent, dependency_revision_manifest=dependency)
        self.assertEqual(contract["contract_version"], LST_CONTRACT_VERSION)
        self.assertEqual(contract["selection_profile"], LST_SELECTION_PROFILE)
        self.assertEqual(contract["selection_semantics"]["kind"], "target_only_full_template_dom_expansion")
        self.assertIs(contract["selection_semantics"]["labeled_section_filtering_applied"], False)
        self.assertEqual(contract["selection_semantics"]["upstream_evidence_commit"], UPSTREAM_EVIDENCE_COMMIT)
        self.assertEqual(contract["dependency_shape"]["template_name_counts"], {"TemplateA": 1})
        self.assertEqual(contract["dependency_shape"]["section_tag_count"], 0)
        self.assertEqual(contract["dependency_shape"]["lst_invocation_count"], 0)
        self.assertEqual(
            contract["capture_scope"],
            {
                "lst_invocation_shape_frozen": True,
                "lst_target_revision_frozen": True,
                "lst_selection_semantics_frozen": True,
                "lst_parent_placement_frozen": True,
                "mediawiki_template_dom_expansion_reproduced": False,
                "resolved_part2_wikitext_identity_frozen": False,
                "literary_body_extraction_frozen": False,
                "composite_literary_body_identity_frozen": False,
                "source_text_committed": False,
            },
        )
        self.assertNotIn("resolved_part2_wikitext_identity", contract)
        self.assertEqual(contract["fantlab_source_edition_match"], "unknown")
        self.assertIs(contract["diagnostic_ready"], False)
        self.assertIs(contract["gate_ready"], False)
        self.assertIs(contract["m2_parity_admissible"], False)

        receipt = replay_lst_contract(parent, dependency, contract, fetcher=fetcher)
        self.assertIs(receipt["verified"], True)
        self.assertIs(receipt["source_text_included"], False)
        self.assertIs(receipt["resolved_part2_wikitext_identity_frozen"], False)

    def test_contract_detects_dependency_shape_without_promoting_it_to_expansion(self) -> None:
        parent_text = "{{#lst:" + DEPENDENCY_TITLE + "}}"
        dependency_text = "<section begin=x />{{#lst:Other}}<section end=x />{{T}}"
        parent = _manifest(PART2_CANDIDATE_ID, "Жизнь Клима Самгина (Горький)/Часть 2", 10, 1, parent_text)
        dependency = _manifest(DEPENDENCY_CANDIDATE_ID, DEPENDENCY_TITLE, 11, 2, dependency_text)

        def fetcher(*, title: str, revision_id: int) -> dict[str, object]:
            manifest = parent if revision_id == 10 else dependency
            text = parent_text if revision_id == 10 else dependency_text
            return {**manifest["source_identity"], "wikitext": text}

        contract = build_lst_contract(parent, dependency, fetcher=fetcher)
        self.assertEqual(contract["dependency_shape"]["section_tag_count"], 2)
        self.assertEqual(contract["dependency_shape"]["lst_invocation_count"], 1)
        self.assertEqual(contract["dependency_shape"]["template_name_counts"], {"#lst:Other": 1, "T": 1})
        self.assertIs(contract["capture_scope"]["mediawiki_template_dom_expansion_reproduced"], False)


if __name__ == "__main__":
    unittest.main()
