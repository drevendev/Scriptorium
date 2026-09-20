from __future__ import annotations

from copy import deepcopy
from pathlib import Path
import unittest

from scriptorium.darwin_render_surface import audit_wikitext, build_audit_manifest, validate_audit_manifest
from scriptorium.darwin_page_shards import load_sharded_manifest


ROOT = Path(__file__).resolve().parents[1]
INDEX = ROOT / "corpus/candidates/source-edition-traces/darwin-origin-species-rachinsky-1864-ru.page-revisions.index.json"


class DarwinRenderSurfaceTests(unittest.TestCase):
    def test_audit_records_shapes_without_argument_values(self) -> None:
        source = (
            "<!-- editor note -->"
            "<noinclude><pagequality level=\"4\" />header {{ignored|secret}}</noinclude>"
            "{{outer|{{inner|lexical value|named=private}}|link=[[Target|Label]]}}"
            "<ref name=\"x\">citation</ref><br />"
            "<noinclude>footer</noinclude>"
        )
        audit = audit_wikitext(source)
        shapes = {
            (item["name"], item["positional"], item["named"], item["count"])
            for item in audit["template_shapes"]
        }
        self.assertIn(("inner", 1, 1, 1), shapes)
        self.assertIn(("outer", 1, 1, 1), shapes)
        self.assertFalse(any(item["name"] == "ignored" for item in audit["template_shapes"]))
        serialized = str(audit)
        for forbidden in ("lexical value", "private", "Target", "Label"):
            self.assertNotIn(forbidden, serialized)
        self.assertEqual(audit["comment_count"], 1)
        self.assertEqual(audit["noinclude_block_count"], 2)
        self.assertEqual(audit["wikilink_count"], 1)

    def test_nested_template_closing_is_not_mistaken_for_parameter_braces(self) -> None:
        audit = audit_wikitext("{{outer|{{inner|x}}}}")
        names = [item["name"] for item in audit["template_shapes"]]
        self.assertEqual(names, ["inner", "outer"])
        self.assertEqual(audit["template_parameter_count"], 0)

    def test_parameter_construct_is_counted_without_serializing_value(self) -> None:
        audit = audit_wikitext("{{outer|{{{parameter|secret default}}}}}")
        self.assertEqual(audit["template_parameter_count"], 1)
        self.assertNotIn("secret default", str(audit))

    def test_audit_fails_closed_on_unbalanced_constructs(self) -> None:
        with self.assertRaisesRegex(ValueError, "unbalanced curly construct"):
            audit_wikitext("visible {{broken|value")
        with self.assertRaisesRegex(ValueError, "unbalanced noinclude"):
            audit_wikitext("<noinclude>header visible")

    def test_literal_blocks_do_not_create_false_template_shapes(self) -> None:
        audit = audit_wikitext("<nowiki>{{not-a-template|x}}</nowiki>{{real|x}}")
        names = [item["name"] for item in audit["template_shapes"]]
        self.assertEqual(names, ["real"])

    def test_build_selects_388_literary_dependencies_and_keeps_gates_closed(self) -> None:
        rows = load_sharded_manifest(INDEX)
        by_id = {int(row["revision_id"]): row for row in rows}

        def fake_fetcher(selected):
            result = {}
            for row in selected:
                revid = int(row["revision_id"])
                self.assertEqual(row, by_id[revid])
                result[revid] = (
                    "<noinclude><pagequality level=\"4\" /></noinclude>"
                    "{{razr|synthetic}} [[Example|label]]<br />"
                    "<noinclude>footer</noinclude>"
                )
            return result

        manifest = build_audit_manifest(INDEX, fetcher=fake_fetcher)
        validate_audit_manifest(manifest)
        self.assertEqual(manifest["literary_dependency_count"], 388)
        self.assertEqual(len(manifest["page_surface_receipts"]), 388)
        self.assertFalse(manifest["rendering_profile_frozen"])
        self.assertFalse(manifest["literary_body_count_and_digests_frozen"])
        self.assertFalse(manifest["minimum_300k_proved"])
        self.assertFalse(manifest["admitted_for_calibration"])
        self.assertEqual(manifest["fantlab_source_edition_match"], "unknown")
        self.assertFalse(manifest["m2_parity_admissible"])

    def test_validator_rejects_source_payload_key(self) -> None:
        def fake_fetcher(selected):
            return {int(row["revision_id"]): "plain synthetic text" for row in selected}

        manifest = build_audit_manifest(INDEX, fetcher=fake_fetcher)
        leaked = deepcopy(manifest)
        leaked["wikitext"] = "forbidden"
        with self.assertRaisesRegex(ValueError, "source payload key"):
            validate_audit_manifest(leaked)


if __name__ == "__main__":
    unittest.main()
