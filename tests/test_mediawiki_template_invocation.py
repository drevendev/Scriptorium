from __future__ import annotations

import hashlib
import unittest

from scriptorium.mediawiki_template_invocation import (
    MANIFEST_VERSION,
    PROFILE_VERSION,
    build_invocation_binding_manifest,
    find_template_invocations,
    parse_template_invocation,
)


class MediaWikiTemplateInvocationTests(unittest.TestCase):
    def test_anonymous_and_named_binding_whitespace_semantics(self) -> None:
        parsed = parse_template_invocation(
            "{{poemx1|  anonymous  | small = yes |2= explicit two }}",
            template_name="poemx1",
        )
        self.assertEqual(parsed["anonymous_argument_count"], 1)
        self.assertEqual(parsed["named_argument_count"], 2)
        effective = parsed["effective_bindings"]
        self.assertEqual(effective["1"]["character_count"], len("  anonymous  "))
        self.assertEqual(
            effective["1"]["sha256"],
            hashlib.sha256("  anonymous  ".encode()).hexdigest(),
        )
        self.assertEqual(effective["small"]["character_count"], 3)
        self.assertEqual(
            effective["small"]["sha256"], hashlib.sha256(b"yes").hexdigest()
        )
        self.assertEqual(
            effective["2"]["sha256"], hashlib.sha256(b"explicit two").hexdigest()
        )

    def test_anonymous_numbering_ignores_named_arguments(self) -> None:
        parsed = parse_template_invocation(
            "{{poemx1|small=1|first|width=20em|second}}",
            template_name="poemx1",
        )
        self.assertEqual(set(parsed["effective_bindings"]), {"1", "2", "small", "width"})
        self.assertEqual(parsed["effective_bindings"]["1"]["argument_ordinal"], 2)
        self.assertEqual(parsed["effective_bindings"]["2"]["argument_ordinal"], 4)

    def test_later_duplicate_assignment_wins(self) -> None:
        parsed = parse_template_invocation(
            "{{poemx1|first|1=override|small=yes|small=no}}",
            template_name="poemx1",
        )
        self.assertEqual(parsed["duplicate_assignment_counts"], {"1": 2, "small": 2})
        self.assertEqual(parsed["effective_bindings"]["1"]["assignment_kind"], "named")
        self.assertEqual(
            parsed["effective_bindings"]["1"]["sha256"],
            hashlib.sha256(b"override").hexdigest(),
        )
        self.assertEqual(
            parsed["effective_bindings"]["small"]["sha256"],
            hashlib.sha256(b"no").hexdigest(),
        )

    def test_nested_template_and_wikilink_pipes_do_not_split_arguments(self) -> None:
        raw = "{{poemx1|[[Page|label]]|{{inner|a|b}}|fixed=1}}"
        parsed = parse_template_invocation(raw, template_name="poemx1")
        self.assertEqual(parsed["argument_count"], 3)
        self.assertEqual(set(parsed["effective_bindings"]), {"1", "2", "fixed"})

    def test_dynamic_named_argument_fails_closed(self) -> None:
        with self.assertRaises(ValueError):
            parse_template_invocation(
                "{{poemx1|{{{name}}}=value}}", template_name="poemx1"
            )

    def test_find_invocations_records_only_source_free_identities(self) -> None:
        source = "before {{poemx1|alpha}} middle {{Poemx1|small=yes|beta}} after"
        records = find_template_invocations(source, template_name="poemx1")
        self.assertEqual(len(records), 2)
        self.assertEqual(records[0]["parent_start_offset"], source.index("{{poemx1"))
        self.assertEqual(records[1]["anonymous_argument_count"], 1)
        serialized = repr(records)
        self.assertNotIn("alpha", serialized)
        self.assertNotIn("beta", serialized)

    def test_manifest_binds_six_calls_to_parameter_surface_without_source_prose(self) -> None:
        source = "\n".join(
            [
                "{{poemx1|one}}",
                "{{poemx1|two|small=yes}}",
                "{{poemx1|three|fixed=}}",
                "{{poemx1|four|width=20em}}",
                "{{poemx1|five|poem=1}}",
                "{{poemx1|six|1=override|3=tail}}",
            ]
        )
        identity = {
            "title": "dependency",
            "revision_id": 2366546,
            "wikitext_sha256": hashlib.sha256(source.encode()).hexdigest(),
        }
        manifest = build_invocation_binding_manifest(
            candidate_id="gorky-klim-samgin-ru-poemx1-invocations",
            dependency_revision_identity=identity,
            dependency_wikitext=source,
            parameter_surface_names=["1", "2", "3", "fixed", "poem", "small", "width"],
            research_date="2026-09-17",
        )
        self.assertEqual(manifest["manifest_version"], MANIFEST_VERSION)
        self.assertEqual(manifest["binding_profile"], PROFILE_VERSION)
        self.assertEqual(manifest["summary"]["invocation_count"], 6)
        self.assertEqual(
            manifest["summary"]["parameter_surface_status"]["1"]["defined_invocation_count"],
            6,
        )
        self.assertEqual(
            manifest["summary"]["parameter_surface_status"]["2"]["omitted_invocation_count"],
            6,
        )
        self.assertEqual(
            manifest["summary"]["effective_binding_names_outside_parameter_surface"], []
        )
        self.assertIs(
            manifest["capture_scope"]["invocation_argument_binding_reproduced"], True
        )
        self.assertIs(
            manifest["capture_scope"]["inserted_parameter_value_recursive_expansion_reproduced"],
            False,
        )
        self.assertNotIn("one", repr(manifest))
        self.assertNotIn("override", repr(manifest))
        self.assertIs(manifest["source_text_included"], False)

    def test_manifest_rejects_dependency_digest_drift(self) -> None:
        with self.assertRaises(ValueError):
            build_invocation_binding_manifest(
                candidate_id="x",
                dependency_revision_identity={
                    "title": "dependency",
                    "revision_id": 1,
                    "wikitext_sha256": "0" * 64,
                },
                dependency_wikitext="{{poemx1|x}}" * 6,
                parameter_surface_names=["1"],
                research_date="2026-09-17",
            )


if __name__ == "__main__":
    unittest.main()
