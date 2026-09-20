import copy
import unittest

from scriptorium.twelve_chairs_gap_audit import (
    BODY_CLASSES,
    CANDIDATE_ID,
    GAP_SEQUENCES,
    build_gap_audit_manifest,
    expected_gap_pages,
    replay_gap_audit_manifest,
    summarize_wikitext,
    validate_gap_audit_manifest,
)


class TwelveChairsGapAuditTests(unittest.TestCase):
    def _records(self):
        bodies = {
            150: "<noinclude>header</noinclude>\n\n<noinclude>footer</noinclude>",
            151: "<noinclude>header</noinclude>\nТекст 12\n<noinclude>footer</noinclude>",
            314: "<!-- transient note --><noinclude>header</noinclude>\n \n",
            315: "<noinclude>header</noinclude>{{marker}}<noinclude>footer</noinclude>",
        }
        return {
            str(row["title"]): {
                "revision_id": 3_000_000 + int(row["page_sequence"]),
                "timestamp": "2026-09-20T00:00:00Z",
                "mediawiki_sha1": f"sha1-{int(row['page_sequence'])}",
                "wikitext": bodies[int(row["page_sequence"])],
            }
            for row in expected_gap_pages()
        }

    def _manifest(self):
        records = self._records()
        return build_gap_audit_manifest(fetcher=lambda: records, captured_at="2026-09-20T00:00:00Z")

    def test_gap_topology_is_exact_and_outside_dependency_ranges(self):
        self.assertEqual(GAP_SEQUENCES, (150, 151, 314, 315))
        pages = expected_gap_pages()
        self.assertEqual(len(pages), 4)
        self.assertEqual([row["page_sequence"] for row in pages], [150, 151, 314, 315])

    def test_summary_is_source_free_and_conservative(self):
        empty = summarize_wikitext("<noinclude>header</noinclude>\n\n<noinclude>footer</noinclude>")
        self.assertEqual(empty["body_presence_class"], "no_transcluded_body")
        self.assertEqual(empty["transcluded_body_non_whitespace_codepoints"], 0)
        nonempty = summarize_wikitext("<noinclude>h</noinclude>Проза 42<noinclude>f</noinclude>")
        self.assertEqual(nonempty["body_presence_class"], "nonempty_body_unclassified")
        self.assertGreater(nonempty["transcluded_body_letter_codepoints"], 0)
        self.assertGreater(nonempty["transcluded_body_number_codepoints"], 0)
        self.assertEqual(BODY_CLASSES, {"no_transcluded_body", "nonempty_body_unclassified"})

    def test_capture_keeps_dependency_and_downstream_gates_closed(self):
        manifest = self._manifest()
        rows = validate_gap_audit_manifest(manifest)
        self.assertEqual(manifest["candidate_id"], CANDIDATE_ID)
        self.assertFalse(manifest["source_text_included"])
        self.assertTrue(manifest["dependency_inventory_unchanged"])
        self.assertFalse(manifest["literary_membership_frozen"])
        self.assertFalse(manifest["literary_body_frozen"])
        self.assertFalse(manifest["admitted_for_calibration"])
        self.assertFalse(manifest["diagnostic_ready"])
        self.assertFalse(manifest["m2_parity_admissible"])
        self.assertEqual(manifest["fantlab_source_edition_match"], "unknown")
        self.assertEqual(len(rows), 4)
        self.assertFalse(manifest["all_gap_pages_have_no_transcluded_body"])

    def test_validation_rejects_source_payload_and_gate_promotion(self):
        manifest = self._manifest()
        with_payload = copy.deepcopy(manifest)
        with_payload["gap_pages"][0]["wikitext"] = "forbidden"
        with self.assertRaisesRegex(ValueError, "shape drift"):
            validate_gap_audit_manifest(with_payload)
        promoted = copy.deepcopy(manifest)
        promoted["literary_body_frozen"] = True
        with self.assertRaisesRegex(ValueError, "must remain false"):
            validate_gap_audit_manifest(promoted)
        changed_set = copy.deepcopy(manifest)
        changed_set["dependency_inventory_unchanged"] = False
        with self.assertRaisesRegex(ValueError, "boundary drift"):
            validate_gap_audit_manifest(changed_set)

    def test_replay_requires_exact_identity_and_source_free_summary(self):
        manifest = self._manifest()
        records = self._records()
        by_id = {
            int(record["revision_id"]): {
                "title": title,
                "timestamp": record["timestamp"],
                "mediawiki_sha1": record["mediawiki_sha1"],
                "wikitext": record["wikitext"],
            }
            for title, record in records.items()
        }
        receipt = replay_gap_audit_manifest(manifest, fetcher=lambda rows: by_id)
        self.assertTrue(receipt["identity_and_source_free_summary_replay_match"])
        self.assertTrue(receipt["dependency_inventory_unchanged"])
        self.assertFalse(receipt["source_text_included"])
        self.assertFalse(receipt["literary_body_frozen"])
        self.assertEqual(receipt["gap_page_count"], 4)
        broken = copy.deepcopy(by_id)
        first = next(iter(broken))
        broken[first]["wikitext"] += "x"
        with self.assertRaisesRegex(ValueError, "pinned gap audit mismatch"):
            replay_gap_audit_manifest(manifest, fetcher=lambda rows: broken)


if __name__ == "__main__":
    unittest.main()
