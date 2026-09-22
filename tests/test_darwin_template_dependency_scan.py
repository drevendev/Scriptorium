from __future__ import annotations

import unittest

from scriptorium.darwin_template_dependency_scan import (
    discover_direct_dependencies,
    source_free_scan_observation,
    transclusion_source,
)


class DarwinTemplateDependencyScanTests(unittest.TestCase):
    def test_redirect_is_a_direct_dependency(self) -> None:
        text = "#REDIRECT [[Шаблон:ЕЁ]]\n<noinclude>{{Doc}}</noinclude>"
        self.assertEqual(discover_direct_dependencies(text), ("Шаблон:ЕЁ",))

    def test_noinclude_is_excluded_and_includeonly_is_visible(self) -> None:
        text = "<noinclude>{{Doc}}</noinclude><includeonly>{{#invoke:String|replace|x|x|y}}</includeonly>"
        self.assertEqual(discover_direct_dependencies(text), ("Модуль:String",))
        visible = transclusion_source(text)
        self.assertNotIn("Doc", visible)
        self.assertIn("#invoke:String", visible)

    def test_onlyinclude_wins_over_surrounding_source(self) -> None:
        text = "{{Outside}}<onlyinclude>{{Inside}}</onlyinclude>{{AlsoOutside}}"
        self.assertEqual(discover_direct_dependencies(text), ("Шаблон:Inside",))

    def test_dynamic_template_name_fails_closed(self) -> None:
        with self.assertRaisesRegex(ValueError, "dynamic template name"):
            discover_direct_dependencies("{{{{{template_name}}}|x}}")

    def test_source_free_observation_contains_only_digests_and_titles(self) -> None:
        text = "<includeonly>{{#invoke:String|len|example}}</includeonly>"
        observation = source_free_scan_observation(text)
        self.assertEqual(observation["direct_dependencies"], ["Модуль:String"])
        self.assertIsNone(observation["redirect_target"])
        self.assertEqual(len(observation["source_sha1"]), 40)
        self.assertEqual(len(observation["transclusion_sha256"]), 64)
        self.assertFalse({"content", "text", "wikitext", "body", "source_text"}.intersection(observation))


if __name__ == "__main__":
    unittest.main()
