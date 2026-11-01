"""Offline source-bound/negative tests for measured Shishmareva diagnostics."""
from __future__ import annotations

from contextlib import contextmanager
from copy import deepcopy
from hashlib import sha256
import json
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch

from scriptorium import robinson_shishmareva_diagnostic as diag
from test_robinson_shishmareva_body import sample


class ShishmarevaMeasurementTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.source = sample("Пятница увидел корабль. Робинзон ответил ему.\n\n" * 8500)
        cls.inventory = json.loads(Path(
            "corpus/candidates/source-edition-traces/"
            "defoe-robinson-crusoe-translation-pair-ru.revision-inventory.json"
        ).read_text(encoding="utf-8"))
        cls.row = next(w for w in cls.inventory["witnesses"]
                       if w["work_id"] == diag.pinned.CANDIDATE_ID)
        cls.digest = sha256(cls.source.encode("utf-8")).hexdigest()
        cls.row["wikitext_sha256"] = cls.digest
        cls.row["wikitext_characters_including_spaces"] = len(cls.source)
        cls.row["wikitext_utf8_bytes"] = len(cls.source.encode("utf-8"))
        cls.observed = {
            "title": diag.pinned.TITLE,
            "revision_id": diag.pinned.REVISION_ID,
            "page_id": diag.pinned.PAGE_ID,
            "revision_timestamp": cls.row["timestamp_utc"],
            "mediawiki_sha1": diag.pinned.MEDIAWIKI_SHA1,
            "wikitext_sha256": cls.digest,
            "wikitext_character_count": len(cls.source),
            "wikitext_utf8_byte_count": len(cls.source.encode("utf-8")),
            "wikitext": cls.source,
        }
        with cls.pins():
            cls.body_manifest = diag.pinned.build_manifest(
                cls.inventory, fetcher=lambda **_: dict(cls.observed)
            )

    @classmethod
    @contextmanager
    def pins(cls):
        with patch.multiple(
            diag.pinned,
            WIKITEXT_SHA256=cls.digest,
            EXPECTED_WIKITEXT_CHARACTERS=len(cls.source),
            EXPECTED_WIKITEXT_BYTES=len(cls.source.encode("utf-8")),
        ):
            yield

    def measure(self, *, inventory=None, body=None, source=None):
        with self.pins():
            return diag.build_diagnostic(
                inventory if inventory is not None else self.inventory,
                body if body is not None else self.body_manifest,
                fetcher=lambda **_: dict(source if source is not None else self.observed),
            )

    def test_real_extraction_plus_analyzer_and_no_prose(self):
        receipt = self.measure()
        rows = {r["metric_id"]: r for r in receipt["metric_rows"]}
        self.assertEqual(len(rows), 29)
        self.assertEqual(rows["fantlab.general.characters"]["actual"],
                         receipt["body"]["normalized_characters_including_spaces"])
        self.assertGreater(receipt["body"]["characters_including_spaces"], 300_000)
        self.assertGreater(rows["fantlab.general.words"]["actual"], 10_000)
        self.assertGreaterEqual(receipt["numeric_metric_count"], 21)
        self.assertEqual(receipt["numeric_metric_count"] + receipt["unavailable_metric_count"], 29)
        self.assertEqual(receipt["source"]["revision_id"], 5634933)
        self.assertEqual(receipt["translator"], "Мария Андреевна Шишмарёва")
        self.assertEqual(receipt["source"]["wikitext_sha256"], self.digest)
        self.assertEqual(receipt["body"]["raw_sha256"],
                         self.body_manifest["literary_body_identity"]["raw_sha256"])
        self.assertEqual(receipt["gates"]["fantlab_input_identity"], "UNKNOWN")
        self.assertEqual(receipt["gates"]["m2_weight"], 0)
        self.assertFalse(receipt["gates"]["corpus_admitted_for_calibration"])
        self.assertFalse(receipt["gates"]["source_text_committed"])
        serialized = diag.render_json(receipt)
        for forbidden in ("Пятница увидел корабль", "Редакторское примечание",
                          "Отексте", "wikitext\": \"", "source_text\": \""):
            self.assertNotIn(forbidden, serialized)

    def test_unbound_dictionary_metrics_remain_unknown_not_zero(self):
        rows = {r["metric_id"]: r for r in self.measure()["metric_rows"]}
        for name in diag._UNBOUND:
            self.assertIsNone(rows[name]["actual"])
            self.assertEqual(rows[name]["result"], "NOT_RUN_DICTIONARY_UNBOUND")
        for r in rows.values():
            self.assertIn(r["compatibility_status"], {"inferred", "extension"})
            self.assertIsNone(r["fantlab_display"])

    def test_source_or_frozen_digest_drift_fails_closed(self):
        changed = deepcopy(self.body_manifest)
        changed["literary_body_identity"]["raw_sha256"] = "0" * 64
        with self.assertRaisesRegex(ValueError, "saved Shishmareva body manifest"):
            self.measure(body=changed)
        changed_source = dict(self.observed)
        changed_source["wikitext"] = self.source + "private unexpected prose"
        with self.assertRaisesRegex(ValueError, "source content hash|source character count|identity drift"):
            self.measure(source=changed_source)

    def test_unexpected_metric_or_parity_claim_is_not_accepted(self):
        original = diag.analyze_deterministic_metrics
        def corrupt(text):
            result = original(text)
            result["metrics"]["fantlab.vocabulary.active_dictionary"]["value"] = 1
            return result
        with patch.object(diag, "analyze_deterministic_metrics", side_effect=corrupt):
            with self.assertRaisesRegex(ValueError, "dictionary-dependent"):
                self.measure()
        changed = deepcopy(self.body_manifest)
        changed["m2_contribution"] = 1
        with self.assertRaises(ValueError):
            self.measure(body=changed)

    def test_cli_create_only_and_exact_replay_does_not_overwrite(self):
        artifact = self.measure()
        with tempfile.TemporaryDirectory() as tmp:
            directory = Path(tmp)
            inventory = directory / "inventory.json"
            body = directory / "body.json"
            output = directory / "derived.json"
            inventory.write_text(json.dumps(self.inventory), encoding="utf-8")
            body.write_text(json.dumps(self.body_manifest), encoding="utf-8")
            args = ["--inventory", str(inventory), "--body-manifest", str(body),
                    "--output", str(output)]
            with patch.object(diag, "build_diagnostic", return_value=artifact):
                self.assertEqual(diag.main(["capture", *args]), 0)
                self.assertEqual(diag.main(["replay", *args]), 0)
                existing = output.read_bytes()
                with self.assertRaises(FileExistsError):
                    diag.main(["capture", *args])
                self.assertEqual(output.read_bytes(), existing)
                output.write_text("tampered", encoding="utf-8")
                with self.assertRaisesRegex(ValueError, "measurement differs"):
                    diag.main(["replay", *args])


if __name__ == "__main__":
    unittest.main()
