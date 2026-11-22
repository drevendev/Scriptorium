"""No-network positive/negative regressions for the pinned Grin lexical bridge."""
import hashlib
import json
import unittest
from unittest.mock import patch

from scriptorium import grin_lexical_pair as target


def identity(text):
    raw = text.encode("utf-8")
    return {
        "character_count_including_spaces": len(text),
        "utf8_byte_count": len(raw),
        "raw_sha256": hashlib.sha256(raw).hexdigest(),
        "normalized_sha256": hashlib.sha256(raw).hexdigest(),
    }


class GrinLexicalPairTests(unittest.TestCase):
    def setUp(self):
        self.road = "кот " * 8 + "ёж " * 4
        self.waves = "ветер " * 7 + "кот " * 2
        self.a = identity(self.road)
        self.b = identity(self.waves)

    def test_verified_bodies_emit_source_free_extension(self):
        result = target._assemble(self.road, self.waves, self.a, self.b)
        self.assertEqual(result["schema_version"], target.SCHEMA)
        self.assertEqual(result["status"], "FROZEN_PUBLIC_DOMAIN_PAIR_DIAGNOSTIC")
        self.assertFalse(result["source_text_included"])
        self.assertFalse(result["m2_parity_admissible"])
        self.assertEqual(result["public_reader_release"], "REQUIRES_SEPARATE_REVIEW")
        self.assertFalse(result["lexical_contrast"]["public_release_ready"])
        self.assertEqual(result["lexical_contrast"]["status"], "COMPARABLE")
        source_free = json.dumps(result, ensure_ascii=False)
        for secret in ("ёж", "кот", "ветер"):
            self.assertNotIn(secret, source_free)
        self.assertEqual(result["source_evidence"]["left"]["normalized_sha256"],
                         self.a["normalized_sha256"])

    def test_modified_body_or_claimed_digest_is_rejected(self):
        with self.assertRaisesRegex(ValueError, "identity drift"):
            target._assemble(self.road + "!", self.waves, self.a, self.b)
        with self.assertRaisesRegex(ValueError, "not comparable"):
            target._assemble(self.road, self.waves,
                             {**self.a, "normalized_sha256": "0" * 64}, self.b)
        with self.assertRaisesRegex(ValueError, "identity drift"):
            target._assemble(self.road, self.waves,
                             {**self.a, "utf8_byte_count": 1}, self.b)

    def test_identical_books_are_not_reported_as_two_book_contrast(self):
        with self.assertRaisesRegex(ValueError, "not comparable"):
            target._assemble(self.road, self.road, self.a, self.a)

    def test_unverified_rights_fail_before_network(self):
        with (patch.object(target.road_diagnostic, "_validate_pins"),
              patch.object(target.waves, "validate_manifest"),
              patch.object(target.road, "replay_body_manifest") as road_network,
              patch.object(target.waves, "replay_manifest") as waves_network):
            with self.assertRaisesRegex(ValueError, "rights"):
                target.build_pinned_pair({"legal_basis": "not_checked"}, {},
                                         {"legal_basis": "public_domain_original_russian_work_with_wikisource_reuse_terms"},
                                         {"corpus_admission": {"general_calibration_profile_admissible": True}})
            road_network.assert_not_called()
            waves_network.assert_not_called()


if __name__ == "__main__":
    unittest.main()
