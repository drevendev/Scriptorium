"""Public metric catalogue must remain an exact view of the analysis contract."""
from __future__ import annotations

import contextlib
import io
import json
from pathlib import Path
import tempfile
import unittest

from scriptorium import cli, metric_catalog
from scriptorium.metric_labels import METRIC_LABELS
from scriptorium.metrics import METRIC_CONTRACT_ID, METRIC_DEFINITIONS


class MetricCatalogTests(unittest.TestCase):
    def test_all_registered_ids_units_evidence_and_dictionary_gates(self):
        result = metric_catalog.build_catalog()
        self.assertEqual(result["metric_contract_id"], METRIC_CONTRACT_ID)
        self.assertEqual(result["scientific_claim"], "DEFINITIONS_ONLY_NOT_FANTLAB_PARITY")
        rows = result["metrics"]
        self.assertEqual(len(rows), 29)
        self.assertEqual([row["id"] for row in rows], sorted(METRIC_DEFINITIONS))
        for row in rows:
            self.assertEqual(row["label"], METRIC_LABELS[row["id"]])
            self.assertEqual(
                (row["unit"], row["definition_evidence"], row["compatibility_status"]),
                METRIC_DEFINITIONS[row["id"]],
            )
        self.assertEqual(sum(row["dictionary_required"] for row in rows), 5)
        self.assertEqual(sum(row["compatibility_status"] == "extension" for row in rows), 1)

    def test_single_metric_json_and_text_from_installed_dispatch(self):
        metric_id = "fantlab.dialogue.share_percent"
        for fmt in ("json", "text"):
            out = io.StringIO()
            with contextlib.redirect_stdout(out):
                self.assertEqual(cli.main(["metrics", metric_id, "--format", fmt]), 0)
            text = out.getvalue()
            self.assertIn(metric_id, text)
            if fmt == "json":
                document = json.loads(text)
                self.assertEqual(len(document["metrics"]), 1)
                self.assertEqual(document["metrics"][0]["unit"], "percent")
            else:
                self.assertIn("NOT source-matched FantLab parity", text)
                self.assertIn("Dialogue character share", text)

    def test_lookup_rejects_invented_or_private_id_without_echo(self):
        bad_id = "PRIVATE_LOCAL_PATH/metric"
        self.assertRaises(ValueError, metric_catalog.build_catalog, bad_id)
        error = io.StringIO()
        with contextlib.redirect_stderr(error), self.assertRaises(SystemExit) as caught:
            cli.main(["metrics", bad_id])
        self.assertEqual(caught.exception.code, 2)
        self.assertNotIn(bad_id, error.getvalue())

    def test_create_only_json_output_and_reproducible_no_network_payload(self):
        with tempfile.TemporaryDirectory() as temporary:
            target = Path(temporary) / "definitions.json"
            self.assertEqual(cli.main(["metrics", "--format", "json", "--output", str(target)]), 0)
            original = target.read_bytes()
            self.assertEqual(json.loads(original)["metrics"], metric_catalog.build_catalog()["metrics"])
            self.assertNotIn(b"manuscript", original.lower())
            error = io.StringIO()
            with contextlib.redirect_stderr(error), self.assertRaises(SystemExit) as caught:
                cli.main(["metrics", "--format", "json", "--output", str(target)])
            self.assertEqual(caught.exception.code, 2)
            self.assertEqual(target.read_bytes(), original)
            self.assertNotIn(temporary, error.getvalue())


if __name__ == "__main__":
    unittest.main()
