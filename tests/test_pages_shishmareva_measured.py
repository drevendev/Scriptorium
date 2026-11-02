"""Eleventh Reader edition must exactly match merged source-free Shishmareva data."""
from copy import deepcopy
from hashlib import sha1
import json
from pathlib import Path
import unittest

ROOT = Path(__file__).resolve().parents[1]
PATH = ROOT / "corpus/candidates/diagnostics/defoe-robinson-crusoe-shishmareva-1935-ru.measured.json"
SNAP = ROOT / "assets/evidence-snapshot.json"
SOURCE_SHA = "61e63ea9ca9329808073a04044e00d98ef8ccaf5f5f38b3beaab52ffd237be2f"
BLOB_SHA = "0afd42fe5825b7eb6b07ca209aef963e006f333b"


def check(artifact, book):
    assert book["key"] == "shishmareva"
    assert artifact["candidate_id"] == book["candidate_id"] == "defoe-robinson-shishmareva-1935-vol1-ru"
    assert artifact["source"]["revision_id"] == book["source_revision_id"] == 5634933
    assert artifact["body"]["characters_including_spaces"] == 572587
    assert artifact["body"]["raw_sha256"] == book["source_sha256"] == SOURCE_SHA
    assert artifact["body"]["normalized_sha256"] == SOURCE_SHA
    assert artifact["gates"]["source_text_committed"] is False
    assert artifact["gates"]["literary_body_source_replay"] is True
    assert artifact["gates"]["minimum_300000_characters"] is True
    assert artifact["gates"]["print_edition_collation"] == "NOT_RUN"
    assert artifact["gates"]["fantlab_input_identity"] == "UNKNOWN"
    assert artifact["gates"]["comparison_class"] == "DIAGNOSTIC_ONLY"
    assert artifact["gates"]["m2_parity_admissible"] is False
    assert artifact["gates"]["m2_weight"] == 0
    assert artifact["gates"]["comparison_with_trusov"] == "NOT_RUN"
    assert book["blob_sha1"] == BLOB_SHA
    assert book["original_language"] == "en"
    assert book["language"] == "ru"
    assert book["edition_id"] == "ru-shishmareva-academia-1935-vol1-oldid-5634933"
    assert book["family_id"] == "defoe-robinson-crusoe-first-narrative"
    assert book["translator"] == {
        "id": "maria-shishmareva",
        "name": "Мария Шишмарёва",
        "authority_trace": "corpus/candidates/source-edition-traces/defoe-robinson-crusoe-translation-pair-ru.json"
    }
    assert book["text_status"] == "measured"
    assert book["measured"] == 24 and book["unavailable"] == 5
    rows = artifact["metric_rows"]
    assert len(rows) == len(book["metrics"]) == 29
    assert len({m["metric_id"] for m in rows}) == 29
    assert sum(m["actual"] is not None for m in rows) == 24
    assert sum(m["actual"] is None for m in rows) == 5
    assert book["profiles"] == artifact["scriptorium"]["profiles"]
    for row, metric in zip(rows, book["metrics"]):
        assert row["metric_id"] == metric["id"]
        assert row["actual"] == metric["actual"]
        assert row["fantlab_display"] is None and metric["reference"] is None
        assert metric["status"] == ("measured" if row["actual"] is not None else "not_run")
        assert metric["kind"] == ("extension" if row["compatibility_status"] == "extension" else "candidate")
        if row["actual"] is None:
            assert row["result"] == "NOT_RUN_DICTIONARY_UNBOUND"


class ShishmarevaReaderTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.artifact = json.loads(PATH.read_text(encoding="utf-8"))
        cls.catalog = json.loads(SNAP.read_text(encoding="utf-8"))
        cls.book = next(b for b in cls.catalog["books"] if b["key"] == "shishmareva")

    def test_exact_source_translation_and_metric_identity(self):
        raw = PATH.read_bytes()
        self.assertEqual(sha1(b"blob " + str(len(raw)).encode() + b"\0" + raw).hexdigest(), BLOB_SHA)
        check(self.artifact, self.book)
        self.assertNotIn("literary_body", self.artifact)
        self.assertNotIn("wikitext", self.artifact)
        actual = {m["id"]: m["actual"] for m in self.book["metrics"]}
        self.assertEqual(actual["fantlab.general.characters"], 572587)
        self.assertEqual(actual["fantlab.general.words"], 93704)
        self.assertEqual(actual["scriptorium.general.sentences"], 4382)
        self.assertEqual(actual["fantlab.vocabulary.unique_words"], 16739)
        self.assertEqual(actual["fantlab.dialogue.share_percent"], 0.2405145502922629)

    def test_site_and_csv_retain_real_translation(self):
        html = (ROOT / "index.html").read_text(encoding="utf-8")
        csv = (ROOT / "assets/scriptorium-ru-measured-metrics.csv").read_text(encoding="utf-8-sig")
        self.assertIn('data-status="measured" data-catalog-key="shishmareva"', html)
        self.assertIn('data-book="shishmareva"', html)
        self.assertIn('<tr><th scope="row">Робинзон Крузо · Шишмарёва</th><td>0.2405145502922629</td><td>%</td></tr>', html)
        self.assertIn("Мария Шишмарёва", html)
        self.assertIn("Скачать все 298 полей (CSV)", html)
        self.assertEqual(self.catalog["counts"], {
            "work_count": 13, "measured_works": 11, "awaiting_measurement": 2,
            "metrics_total": 298, "numeric_total": 249, "unavailable_total": 49,
            "m2_source_matched": 0
        })
        self.assertEqual(self.catalog["comparability"]["m2_parity_admissible"], False)
        self.assertEqual(csv.count('"shishmareva"'), 29)
        self.assertIn('"maria-shishmareva","Мария Шишмарёва"', csv)
        self.assertNotIn("Трусов" + " (измерено)", html)

    def test_mutations_fail_closed(self):
        for mutate in (
            lambda a, b: a["gates"].__setitem__("m2_parity_admissible", True),
            lambda a, b: a["gates"].__setitem__("source_text_committed", True),
            lambda a, b: a["source"].__setitem__("revision_id", 1),
            lambda a, b: b.__setitem__("source_sha256", "0" * 64),
            lambda a, b: b.__setitem__("original_language", "ru"),
            lambda a, b: b.__setitem__("translator", None),
            lambda a, b: b["metrics"][4].__setitem__("actual", 0),
            lambda a, b: b["metrics"][0].__setitem__("reference", 0),
            lambda a, b: b["metrics"][0].__setitem__("kind", "extension"),
        ):
            a, b = deepcopy(self.artifact), deepcopy(self.book)
            mutate(a, b)
            with self.assertRaises(AssertionError):
                check(a, b)


if __name__ == "__main__":
    unittest.main()
