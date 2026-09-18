from __future__ import annotations

import unittest

from scriptorium.klim_samgin_direct_poemx1_surface import (
    _branch_is_plain,
    _classify_invocation,
)
from scriptorium.mediawiki_poem_render_surface import (
    _core_sensitive_surface,
    _poem_branch_surface,
)
from scriptorium.mediawiki_template_invocation import find_template_invocations


class DirectParentPoemx1SurfaceTests(unittest.TestCase):
    def test_plain_surface_is_safe(self) -> None:
        value = "Первая строка\nВторая строка"
        self.assertTrue(
            _branch_is_plain(
                _core_sensitive_surface(value),
                _poem_branch_surface(value),
            )
        )

    def test_active_wikilink_surface_is_not_safe(self) -> None:
        value = "[[Цель|текст]]"
        self.assertFalse(
            _branch_is_plain(
                _core_sensitive_surface(value),
                _poem_branch_surface(value),
            )
        )

    def test_leading_space_poem_branch_is_not_safe(self) -> None:
        value = " строка"
        self.assertFalse(
            _branch_is_plain(
                _core_sensitive_surface(value),
                _poem_branch_surface(value),
            )
        )

    def test_classification_never_emits_source_text(self) -> None:
        source = "prefix {{poemx1||Первая строка\nВторая строка}} suffix"
        observed = find_template_invocations(source, template_name="poemx1")
        self.assertEqual(len(observed), 1)
        row = _classify_invocation(
            part=1,
            wikitext=source,
            observed=observed[0],
            frozen=observed[0],
        )
        self.assertTrue(row["plain_value_literary_replacement_safe"])
        self.assertEqual(row["parameter_2_identity"]["character_count"], 27)
        self.assertNotIn("Первая", repr(row))
        self.assertFalse(row["source_text_included"])
        reconstruction = row["bounded_poem_reconstruction"]
        self.assertIsInstance(reconstruction, dict)
        self.assertEqual(
            reconstruction["literary_plain_value_sha256"],
            row["parameter_2_identity"]["sha256"],
        )

    def test_classification_records_unresolved_active_surface_without_rendering(self) -> None:
        source = "{{poemx1||[[Цель|текст]]}}"
        observed = find_template_invocations(source, template_name="poemx1")
        row = _classify_invocation(
            part=1,
            wikitext=source,
            observed=observed[0],
            frozen=observed[0],
        )
        self.assertFalse(row["plain_value_literary_replacement_safe"])
        self.assertIsNone(row["bounded_poem_reconstruction"])
        self.assertGreater(row["core_sensitive_surface"]["internal_link_open_count"], 0)

    def test_structural_row_drift_fails_closed(self) -> None:
        source = "{{poemx1||Текст}}"
        observed = find_template_invocations(source, template_name="poemx1")
        frozen = dict(observed[0])
        frozen["invocation_sha256"] = "0" * 64
        with self.assertRaisesRegex(ValueError, "structural row drift"):
            _classify_invocation(
                part=1,
                wikitext=source,
                observed=observed[0],
                frozen=frozen,
            )


if __name__ == "__main__":
    unittest.main()
