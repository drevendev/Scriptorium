from __future__ import annotations

import unittest

from scriptorium.mediawiki_poem_render_surface import (
    _core_sensitive_surface,
    _poem_branch_surface,
    _render_plain_poem_fragment,
)


class MediaWikiPoemRenderSurfaceTests(unittest.TestCase):
    def test_plain_multiline_value_reconstructs_post_unstrip_fragment(self) -> None:
        value = "Первая строка\nВторая строка"
        self.assertEqual(
            _render_plain_poem_fragment(value),
            '<div class="poem">\nПервая строка<br />\nВторая строка\n</div>',
        )
        self.assertEqual(
            _poem_branch_surface(value),
            {
                "line_count": 2,
                "newline_count": 1,
                "leading_colon_line_count": 0,
                "leading_space_line_count": 0,
                "horizontal_rule_line_count": 0,
                "edge_whitespace_present": False,
            },
        )

    def test_core_sensitive_inventory_is_source_free_and_conservative(self) -> None:
        surface = _core_sensitive_surface(
            "[[link]]\n----\n__NOTOC__\n== heading ==\nISBN 978-0-00-000000-0"
        )
        self.assertEqual(surface["internal_link_open_count"], 1)
        self.assertEqual(surface["horizontal_rule_line_count"], 1)
        self.assertEqual(surface["behavior_switch_delimiter_count"], 2)
        self.assertEqual(surface["heading_line_count"], 1)
        self.assertEqual(surface["magic_link_token_count"], 1)

    def test_active_core_syntax_fails_closed(self) -> None:
        for value in (
            "[[link]]",
            "----\nline",
            "__NOTOC__",
            "== heading ==",
            "https://example.test/",
            "&nbsp;",
            "-{ru:текст}-",
        ):
            with self.subTest(value=value):
                with self.assertRaises(ValueError):
                    _render_plain_poem_fragment(value)

    def test_poem_specific_non_plain_branches_fail_closed(self) -> None:
        for value in (":indent", " leading", "line\n----", " trailing "):
            with self.subTest(value=value):
                with self.assertRaises(ValueError):
                    _render_plain_poem_fragment(value)

    def test_ordinary_russian_punctuation_remains_plain(self) -> None:
        value = "— Да, конечно! — сказал он: «Так и будет…»"
        self.assertTrue(all(count == 0 for count in _core_sensitive_surface(value).values()))
        rendered = _render_plain_poem_fragment(value)
        self.assertIn(value, rendered)
        self.assertTrue(rendered.startswith('<div class="poem">\n'))
        self.assertTrue(rendered.endswith("\n</div>"))


if __name__ == "__main__":
    unittest.main()
