from __future__ import annotations

from hashlib import sha256
import json
from pathlib import Path
import unittest

from scriptorium.klim_samgin_body_surface import (
    LST_CONTRACT_VERSION,
    _analyze_part,
    _part2_substitution_boundary,
    validate_body_surface_manifest,
)


TRACE = Path("corpus/candidates/source-edition-traces/gorky-klim-samgin-ru.body-surface.json")


def _identity(*, title: str, revision_id: int, text: str) -> dict[str, object]:
    return {
        "title": title,
        "revision_id": revision_id,
        "wikitext_sha256": sha256(text.encode("utf-8")).hexdigest(),
    }


class KlimSamginBodySurfaceTests(unittest.TestCase):
    def test_part2_boundary_keeps_direct_poemx1_outside_target_substitution(self) -> None:
        first = "{{poemx1||a|}}"
        lst = "{{#lst:Target}}"
        second = "{{poemx1||b|}}"
        text = first + "\n" + lst + "\n" + second
        row = _analyze_part(
            part=2,
            wikitext=text,
            source_identity=_identity(
                title="Жизнь Клима Самгина (Горький)/Часть 2",
                revision_id=5198033,
                text=text,
            ),
        )
        start = text.index(lst)
        boundary = _part2_substitution_boundary(
            row,
            {
                "contract_version": LST_CONTRACT_VERSION,
                "invocation": {
                    "argument_count": 1,
                    "section_label": None,
                    "parent_start_offset": start,
                    "parent_end_offset": start + len(lst),
                    "invocation_sha256": sha256(lst.encode("utf-8")).hexdigest(),
                },
            },
        )
        self.assertEqual(boundary["direct_parent_poemx1_count"], 2)
        self.assertTrue(boundary["target_only_lst_substitution_preserves_direct_parent_poemx1"])
        self.assertTrue(boundary["resolved_target_substitution_is_not_a_template_free_parent_claim"])

    def test_part2_boundary_fails_if_poem_call_overlaps_lst_span(self) -> None:
        first = "{{poemx1||a|}}"
        second = "{{poemx1||b|}}"
        text = first + "\n" + second
        row = _analyze_part(
            part=2,
            wikitext=text,
            source_identity=_identity(
                title="Жизнь Клима Самгина (Горький)/Часть 2",
                revision_id=5198033,
                text=text,
            ),
        )
        with self.assertRaisesRegex(ValueError, "overlaps"):
            _part2_substitution_boundary(
                row,
                {
                    "contract_version": LST_CONTRACT_VERSION,
                    "invocation": {
                        "argument_count": 1,
                        "section_label": None,
                        "parent_start_offset": 0,
                        "parent_end_offset": len(first),
                        "invocation_sha256": "0" * 64,
                    },
                },
            )

    def test_committed_surface_is_source_free_and_fail_closed(self) -> None:
        manifest = json.loads(TRACE.read_text(encoding="utf-8"))
        validate_body_surface_manifest(manifest)
        self.assertEqual(
            [row["direct_poemx1_invocation_count"] for row in manifest["parts"]],
            [5, 2, 0, 0],
        )
        self.assertEqual(manifest["aggregate_template_name_counts"]["poemx1"], 7)
        self.assertEqual(manifest["aggregate_html_tag_name_counts"]["nowiki"], 50)
        self.assertFalse(manifest["capture_scope"]["literary_body_extraction_frozen"])
        self.assertFalse(manifest["capture_scope"]["literary_composition_frozen"])
        self.assertEqual(manifest["fantlab_source_edition_match"], "unknown")
        self.assertFalse(manifest["m2_parity_admissible"])

        forbidden = {"wikitext", "content", "body", "text", "source_text"}

        def walk(value: object) -> None:
            if isinstance(value, dict):
                self.assertFalse(forbidden.intersection(value))
                for child in value.values():
                    walk(child)
            elif isinstance(value, list):
                for child in value:
                    walk(child)

        walk(manifest)


if __name__ == "__main__":
    unittest.main()
