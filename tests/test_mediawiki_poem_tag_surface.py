import unittest

from scriptorium.mediawiki_poem_tag_surface import extract_poem_tag_surface


class PoemTagSurfaceTests(unittest.TestCase):
    def test_extracts_nested_content_and_named_attributes_without_rendering(self):
        text = (
            "prefix"
            "{{#tag:poem|{{{2|}}}|class=poem|"
            "style={{#if:{{{width|}}}|width:{{{width|}}}ex;|margin:0;}}}}}"
            "suffix"
        )
        surface = extract_poem_tag_surface(text)

        self.assertEqual(surface["top_level_argument_count"], 3)
        self.assertEqual(surface["attribute_count"], 2)
        self.assertEqual(surface["attribute_names"], ["class", "style"])
        self.assertEqual(
            surface["content_argument"]["parameter_references"]["parameter_reference_counts"],
            {"2": 1},
        )
        style = surface["attributes"][1]
        self.assertEqual(style["name"], "style")
        self.assertEqual(
            style["parameter_references"]["parameter_reference_counts"],
            {"width": 2},
        )
        self.assertEqual(style["dependency_graph"]["parser_function_counts"], {"#if": 1})
        self.assertNotIn("value", style)

    def test_requires_exactly_one_poem_tag(self):
        with self.assertRaisesRegex(ValueError, "exactly one"):
            extract_poem_tag_surface("no extension tag")
        with self.assertRaisesRegex(ValueError, "exactly one"):
            extract_poem_tag_surface("{{#tag:poem|a}}{{#tag:poem|b}}")

    def test_rejects_positional_or_duplicate_attributes(self):
        with self.assertRaisesRegex(ValueError, "named attributes"):
            extract_poem_tag_surface("{{#tag:poem|text|compact}}")
        with self.assertRaisesRegex(ValueError, "duplicate"):
            extract_poem_tag_surface("{{#tag:poem|text|style=a|style=b}}")


if __name__ == "__main__":
    unittest.main()
