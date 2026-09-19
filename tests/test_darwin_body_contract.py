from __future__ import annotations

from copy import deepcopy
from hashlib import sha256
from pathlib import Path
import unittest

from scriptorium.darwin_body_contract import (
    EXPECTED_APPARATUS_PAGE_COUNT,
    EXPECTED_LITERARY_PAGE_COUNT,
    apparatus_page_sequences,
    build_contract,
    build_contract_from_index,
    literary_page_sequences,
    validate_contract,
)
from scriptorium.darwin_page_shards import load_sharded_manifest


ROOT = Path(__file__).resolve().parents[1]
INDEX = ROOT / "corpus/candidates/source-edition-traces/darwin-origin-species-rachinsky-1864-ru.page-revisions.index.json"


class DarwinLiteraryBodyContractTests(unittest.TestCase):
    def test_partition_covers_frozen_inventory_without_overlap(self) -> None:
        rows = load_sharded_manifest(INDEX)
        frozen = {int(row["page_sequence"]) for row in rows}
        literary = set(literary_page_sequences())
        apparatus = set(apparatus_page_sequences())

        self.assertEqual(len(literary), EXPECTED_LITERARY_PAGE_COUNT)
        self.assertEqual(len(apparatus), EXPECTED_APPARATUS_PAGE_COUNT)
        self.assertFalse(literary & apparatus)
        self.assertEqual(literary | apparatus, frozen)
        self.assertNotIn(114, frozen)
        self.assertNotIn(411, frozen)

    def test_contract_selects_numbered_routes_only_and_keeps_gates_closed(self) -> None:
        contract = build_contract_from_index(INDEX)
        composition = contract["composition"]
        apparatus = composition["apparatus_excluded"]

        self.assertEqual(composition["literary_dependency_count"], 388)
        self.assertEqual(composition["selection"], "rendered numbered routes /1 through /14 only")
        self.assertEqual(len(composition["numbered_routes"]), 14)
        self.assertEqual(apparatus["alphabetical_index_route"]["from"], 412)
        self.assertEqual(apparatus["alphabetical_index_route"]["to"], 422)
        self.assertEqual(apparatus["apparatus_dependency_count"], 30)
        self.assertFalse(contract["source_text_included"])
        self.assertFalse(contract["admitted_for_calibration"])
        self.assertEqual(contract["fantlab_source_edition_match"], "unknown")
        self.assertFalse(contract["m2_parity_admissible"])
        self.assertFalse(contract["deferred_gates"]["literary_body_count_and_digests_frozen"])
        self.assertFalse(contract["deferred_gates"]["minimum_300k_proved"])
        self.assertEqual(len(contract["source_revision_index_sha256"]), 64)
        self.assertEqual(len(contract["source_identity_set_sha256"]), 64)

    def test_contract_fails_closed_on_topology_drift(self) -> None:
        rows = list(load_sharded_manifest(INDEX))
        with self.assertRaisesRegex(ValueError, "exact frozen 418-Page"):
            build_contract(rows[:-1], index_sha256=sha256(INDEX.read_bytes()).hexdigest())

    def test_contract_rejects_source_payload_keys(self) -> None:
        rows = [dict(row) for row in load_sharded_manifest(INDEX)]
        rows[0]["wikitext"] = "synthetic forbidden payload"
        with self.assertRaisesRegex(ValueError, "source payload key"):
            build_contract(rows, index_sha256=sha256(INDEX.read_bytes()).hexdigest())

    def test_validator_detects_contract_drift(self) -> None:
        rows = load_sharded_manifest(INDEX)
        digest = sha256(INDEX.read_bytes()).hexdigest()
        contract = build_contract(rows, index_sha256=digest)
        drifted = deepcopy(contract)
        drifted["admitted_for_calibration"] = True
        with self.assertRaisesRegex(ValueError, "contract drift"):
            validate_contract(drifted, rows, index_sha256=digest)


if __name__ == "__main__":
    unittest.main()
