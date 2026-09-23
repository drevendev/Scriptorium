from __future__ import annotations

import hashlib
import json
from pathlib import Path
import unittest


ROOT = Path(__file__).resolve().parents[1]
ARTIFACT = (
    ROOT
    / "corpus"
    / "candidates"
    / "source-edition-traces"
    / "perelman-entertaining-physics-book1-1913-ru.wikisource-index-surface.json"
)
EXPECTED_DIGEST = "46803a34fb018f204588f798aca9b928393c37b54518f8adba36b790d6c33d77"
EXPECTED_CARRIERS = {
    "pdf": {
        "page_count": 223,
        "sha256": "3d87d22a42ad949654265e066f81211d7831e32c8b62b96c967cd4cd33e7ed61",
        "category": "PDF files in Russian without index page in Russian Wikisource",
    },
    "djvu": {
        "page_count": 218,
        "sha256": "f1db2166ae0cb5d420aad445f00d90cb09ac0b97e19fc8ece16d9b8ecf9e2462",
        "category": "DjVu files in Russian without index page in Russian Wikisource",
    },
}
FORBIDDEN_SOURCE_KEYS = {
    "source_text",
    "literary_text",
    "ocr_text",
    "text_content",
    "page_image",
    "page_image_bytes",
}


def canonical_payload_digest(document: dict[str, object]) -> str:
    payload = dict(document)
    payload.pop("canonical_payload_sha256", None)
    encoded = json.dumps(
        payload,
        ensure_ascii=False,
        sort_keys=True,
        separators=(",", ":"),
    ).encode("utf-8")
    return hashlib.sha256(encoded).hexdigest()


def walk_keys(value: object) -> set[str]:
    keys: set[str] = set()
    if isinstance(value, dict):
        for key, child in value.items():
            keys.add(str(key))
            keys.update(walk_keys(child))
    elif isinstance(value, list):
        for child in value:
            keys.update(walk_keys(child))
    return keys


class PerelmanWikisourceIndexSurfaceTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.document = json.loads(ARTIFACT.read_text(encoding="utf-8"))

    def test_canonical_payload_digest_is_frozen(self) -> None:
        self.assertEqual(self.document["canonical_payload_sha256"], EXPECTED_DIGEST)
        self.assertEqual(canonical_payload_digest(self.document), EXPECTED_DIGEST)

    def test_observation_is_source_free_and_current_surface_only(self) -> None:
        self.assertTrue(self.document["source_free"])
        self.assertFalse(self.document["source_text_committed"])
        self.assertFalse(self.document["decision"]["historical_absence_proved"])
        self.assertEqual(
            self.document["decision"]["status"],
            "current_wikisource_index_surface_not_established",
        )
        self.assertFalse(
            self.document["decision"][
                "proofreadpage_index_may_be_used_as_current_page_label_authority"
            ]
        )
        self.assertTrue(walk_keys(self.document).isdisjoint(FORBIDDEN_SOURCE_KEYS))

    def test_carrier_bindings_and_categories_are_exact(self) -> None:
        carriers = {
            carrier["carrier_kind"]: carrier for carrier in self.document["carriers"]
        }
        self.assertEqual(set(carriers), set(EXPECTED_CARRIERS))
        for kind, expected in EXPECTED_CARRIERS.items():
            carrier = carriers[kind]
            self.assertEqual(carrier["page_count"], expected["page_count"])
            self.assertEqual(carrier["sha256"], expected["sha256"])
            self.assertEqual(carrier["observed_commons_category"], expected["category"])
            self.assertFalse(carrier["current_russian_wikisource_index_surface_established"])

    def test_downstream_gates_remain_closed(self) -> None:
        gates = self.document["gate_state"]
        for key in (
            "canonical_extraction_carrier_selected",
            "diagnostic_ready",
            "fantlab_input_identity_established",
            "literary_body_frozen",
            "literary_page_selection_bound",
            "m2_parity_admissible",
            "minimum_300k_proved_from_frozen_body",
            "ocr_correctness_verified",
            "pdf_djvu_page_equivalence_verified",
        ):
            self.assertFalse(gates[key], key)
        self.assertEqual(gates["fantlab_source_edition_match"], "unknown")
        self.assertEqual(gates["m2_progress_after_observation"], "0/5")


if __name__ == "__main__":
    unittest.main()
