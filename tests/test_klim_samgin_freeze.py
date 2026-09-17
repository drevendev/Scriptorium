from __future__ import annotations

from hashlib import sha256
import unittest

from scriptorium.klim_samgin_freeze import (
    DEPENDENCY_CANDIDATE_ID,
    DEPENDENCY_TITLE,
    PART2_CANDIDATE_ID,
    LST_CONTRACT_VERSION,
    LST_SELECTION_PROFILE,
    build_lst_contract,
    parse_single_lst_invocation,
    replay_lst_contract,
    select_labeled_sections,
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
    def test_simple_invocation_freezes_target_label_and_placement(self) -> None:
        source = "prefix\n{{#lst:Page/Subpage|section-2}}\nsuffix"
        invocation = parse_single_lst_invocation(source)
        self.assertEqual(invocation["target_title"], "Page/Subpage")
        self.assertEqual(invocation["section_label"], "section-2")
        self.assertEqual(
            source[invocation["parent_start_offset"]:invocation["parent_end_offset"]],
            "{{#lst:Page/Subpage|section-2}}",
        )

    def test_invocation_rejects_ranges_multiple_calls_and_unparsed_shape(self) -> None:
        with self.assertRaisesRegex(ValueError, "range syntax"):
            parse_single_lst_invocation("{{#lst:Page|a|b}}")
        with self.assertRaisesRegex(ValueError, "exactly one"):
            parse_single_lst_invocation("{{#lst:Page|a}}{{#lst:Page|b}}")
        with self.assertRaisesRegex(ValueError, "unsupported"):
            parse_single_lst_invocation("{{#lst:Page}}")

    def test_same_label_sections_are_selected_in_source_order_without_separator(self) -> None:
        dependency = (
            "outside"
            '<section begin="keep" />alpha<section end="keep" />'
            "ignored"
            "<section begin=keep />βeta<section end=keep />"
            "tail"
        )
        selected = select_labeled_sections(dependency, "keep")
        self.assertEqual(selected["selected_segment_count"], 2)
        self.assertEqual(selected["selected_label_marker_count"], 4)
        self.assertEqual(
            selected["selection_identity"]["sha256"],
            sha256("alphaβeta".encode("utf-8")).hexdigest(),
        )
        self.assertNotIn("wikitext", selected)

    def test_section_selection_fails_closed_on_unpaired_or_unsupported_markers(self) -> None:
        with self.assertRaisesRegex(ValueError, "matching end"):
            select_labeled_sections("<section begin=x />abc", "x")
        with self.assertRaisesRegex(ValueError, "unsupported labeled-section"):
            select_labeled_sections('<section begin="x">abc</section>', "x")

    def test_contract_is_source_free_and_replay_stable(self) -> None:
        parent_text = f"before\n{{{{#lst:{DEPENDENCY_TITLE}|part-two}}}}\nafter"
        dependency_text = (
            "metadata\n"
            '<section begin="part-two" />FIRST<section end="part-two" />'
            "skip"
            '<section begin="part-two" />SECOND<section end="part-two" />'
        )
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
        validate_lst_contract(
            contract,
            parent_revision_manifest=parent,
            dependency_revision_manifest=dependency,
        )
        self.assertEqual(contract["contract_version"], LST_CONTRACT_VERSION)
        self.assertEqual(contract["selection_profile"], LST_SELECTION_PROFILE)
        self.assertEqual(contract["dependency_selection"]["selected_segment_count"], 2)
        resolved = parent_text.replace(
            f"{{{{#lst:{DEPENDENCY_TITLE}|part-two}}}}",
            "FIRSTSECOND",
        )
        self.assertEqual(
            contract["resolved_parent_wikitext_identity"]["sha256"],
            sha256(resolved.encode("utf-8")).hexdigest(),
        )
        self.assertEqual(
            contract["capture_scope"],
            {
                "lst_labeled_section_selection_frozen": True,
                "lst_parent_placement_frozen": True,
                "resolved_part2_wikitext_identity_frozen": True,
                "literary_body_extraction_frozen": False,
                "composite_literary_body_identity_frozen": False,
                "source_text_committed": False,
            },
        )
        self.assertEqual(contract["fantlab_source_edition_match"], "unknown")
        self.assertIs(contract["diagnostic_ready"], False)
        self.assertIs(contract["gate_ready"], False)
        self.assertIs(contract["m2_parity_admissible"], False)
        self.assertFalse({"wikitext", "content", "body", "text", "source_text"}.intersection(contract))

        receipt = replay_lst_contract(parent, dependency, contract, fetcher=fetcher)
        self.assertIs(receipt["verified"], True)
        self.assertIs(receipt["source_text_included"], False)
        self.assertEqual(receipt["resolved_part2_wikitext_sha256"], contract["resolved_parent_wikitext_identity"]["sha256"])

    def test_contract_rejects_nested_dependency_lst(self) -> None:
        parent_text = f"{{{{#lst:{DEPENDENCY_TITLE}|x}}}}"
        dependency_text = "<section begin=x />{{#lst:Another|y}}<section end=x />"
        parent = _manifest(PART2_CANDIDATE_ID, "Жизнь Клима Самгина (Горький)/Часть 2", 10, 1, parent_text)
        dependency = _manifest(DEPENDENCY_CANDIDATE_ID, DEPENDENCY_TITLE, 11, 2, dependency_text)

        def fetcher(*, title: str, revision_id: int) -> dict[str, object]:
            manifest = parent if revision_id == 10 else dependency
            text = parent_text if revision_id == 10 else dependency_text
            return {**manifest["source_identity"], "wikitext": text}

        with self.assertRaisesRegex(ValueError, "additional source-graph pin"):
            build_lst_contract(parent, dependency, fetcher=fetcher)


if __name__ == "__main__":
    unittest.main()
