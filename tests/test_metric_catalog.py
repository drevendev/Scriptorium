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

    def test_russian_labels_match_published_glossary_without_metric_drift(self):
        english = metric_catalog.build_catalog()
        russian = metric_catalog.build_catalog(language="ru")
        self.assertEqual(russian["label_language"], "ru")
        self.assertNotIn("label_language", english)
        self.assertEqual(len(russian["metrics"]), 29)
        glossary = (Path(__file__).resolve().parent.parent / "metrics.html").read_text(
            encoding="utf-8"
        )
        for en, ru in zip(english["metrics"], russian["metrics"], strict=True):
            self.assertEqual(en["id"], ru["id"])
            for field in ("unit", "definition_evidence", "compatibility_status",
                          "dictionary_required"):
                self.assertEqual(en[field], ru[field])
            self.assertIn(f'{ru["label"]}<code>{ru["id"]}</code>', glossary)
        self.assertEqual(
            russian["scientific_claim"], "DEFINITIONS_ONLY_NOT_FANTLAB_PARITY"
        )

    def test_russian_cli_text_json_and_invalid_locale(self):
        for fmt in ("text", "json"):
            output = io.StringIO()
            with contextlib.redirect_stdout(output):
                self.assertEqual(
                    cli.main(["metrics", "fantlab.dialogue.share_percent",
                              "--lang", "ru", "--format", fmt]), 0
                )
            rendered = output.getvalue()
            self.assertIn("Доля диалогов", rendered)
            if fmt == "text":
                self.assertIn("не подтверждают совпадение с FantLab", rendered)
                self.assertIn("[percent]", rendered)
            else:
                catalog = json.loads(rendered)
                self.assertEqual(catalog["label_language"], "ru")
                self.assertEqual(catalog["metrics"][0]["unit"], "percent")
        with self.assertRaisesRegex(ValueError, "language"):
            metric_catalog.build_catalog(language="xx")


if __name__ == "__main__":
    unittest.main()
