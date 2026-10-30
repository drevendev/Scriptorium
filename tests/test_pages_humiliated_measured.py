"""The tenth Reader novel must equal its retained CI artifact, never a parity claim."""
from copy import deepcopy
from hashlib import sha1, sha256
import json
from pathlib import Path
import unittest

ROOT=Path(__file__).resolve().parents[1]
RAW=ROOT/"corpus/candidates/diagnostics/dostoevsky-humiliated-and-insulted-ru.retained.json"
DATA=ROOT/"assets/evidence-snapshot.json"
JSON_SHA256="bcd4e9cde2aa75364ef458749c9b1f26b72b75e1ab8df0d70c4fc6f3f018a634"
BODY_SHA256="ffc6825db7f442c7df93136e8ddf90ce44be8801cdbaa727d5fe642db3fad8fa"

def check(artifact,book):
    assert artifact["candidate_id"] == book["candidate_id"] == "dostoevsky-humiliated-and-insulted-azlib-ru"
    assert artifact["source"]["revision_id"] == book["source_revision_id"] == 5611473
    assert artifact["source"]["legal_basis"] == "public_domain_original_author_died_1881"
    assert artifact["gates"]["source_text_committed"] is False
    assert artifact["gates"]["complete_chapter_inventory"] is True
    assert artifact["gates"]["minimum_300000_characters"] is True
    assert artifact["gates"]["source_edition_print_collation"] == "NOT_RUN"
    assert artifact["gates"]["fantlab_input_identity"] == "UNKNOWN"
    assert artifact["gates"]["comparison_class"] == "DIAGNOSTIC_ONLY"
    assert artifact["gates"]["m2_parity_admissible"] is False
    assert artifact["gates"]["m2_weight"] == 0
    assert artifact["body"]["raw_sha256"] == book["source_sha256"] == BODY_SHA256
    assert artifact["body"]["characters_including_spaces"] == 713925
    assert book["edition_id"] == "ru-wikisource-az-lib-oldid-5611473"
    assert book["original_language"] == book["language"] == "ru"
    assert book["translator"] is None and artifact["translator"] is None
    assert book["text_status"] == "measured"
    assert book["measured"] == 24 and book["unavailable"] == 5
    rows=artifact["metric_rows"]
    assert len(rows) == len(book["metrics"]) == 29
    assert len({r["metric_id"] for r in rows}) == 29
    assert sum(r["actual"] is not None for r in rows) == 24
    assert sum(r["actual"] is None for r in rows) == 5
    assert all(r["fantlab_display"] is None for r in rows)
    assert book["profiles"] == artifact["scriptorium"]["profiles"]
    for row,metric in zip(rows,book["metrics"]):
        assert metric["id"] == row["metric_id"]
        assert metric["actual"] == row["actual"]
        assert metric["reference"] is None
        assert metric["status"] == ("measured" if row["actual"] is not None else "not_run")
        assert metric["kind"] == ("extension" if row["compatibility_status"] == "extension" else "candidate")

class HumiliatedReaderTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.artifact=json.loads(RAW.read_text(encoding="utf-8"))
        cls.catalog=json.loads(DATA.read_text(encoding="utf-8"))
        cls.book=next(b for b in cls.catalog["books"] if b["key"]=="humiliated")
    def test_exact_pinned_source_and_metrics(self):
        raw=RAW.read_bytes()
        self.assertEqual(len(raw),9843)
        self.assertEqual(sha256(raw).hexdigest(),JSON_SHA256)
        self.assertEqual(self.book["blob_sha1"],sha1(b"blob "+str(len(raw)).encode()+b"\0"+raw).hexdigest())
        check(self.artifact,self.book)
        self.assertNotIn("literary_body",self.artifact)
        self.assertNotIn("wikitext",self.artifact)
        observations={m["id"]:m["actual"] for m in self.book["metrics"]}
        self.assertEqual(observations["fantlab.general.words"],118157)
        self.assertEqual(observations["fantlab.vocabulary.unique_words"],17066)
        self.assertEqual(observations["scriptorium.general.sentences"],10381)
        self.assertEqual(observations["fantlab.dialogue.share_percent"],56.66327827623132)
    def test_static_reader_and_csv_counts(self):
        html=(ROOT/"index.html").read_text(encoding="utf-8")
        self.assertIn('data-status="measured" data-catalog-key="humiliated"',html)
        self.assertIn('data-book="humiliated"',html)
        self.assertIn('<tr><th scope="row">Униженные и оскорбленные</th><td>56.66327827623132</td><td>%</td></tr>',html)
        self.assertIn("Скачать все 269 полей (CSV)",html)
        self.assertEqual(self.catalog["counts"],{
          "work_count":12,"measured_works":10,"awaiting_measurement":2,
          "metrics_total":269,"numeric_total":225,"unavailable_total":44,"m2_source_matched":0
        })
        self.assertEqual([b["key"] for b in self.catalog["books"] if b["text_status"]!="measured"],["petersburg","darwin"])
    def test_tampering_refused(self):
        for mutate in (
          lambda a,b:a["gates"].__setitem__("m2_parity_admissible",True),
          lambda a,b:a["gates"].__setitem__("source_text_committed",True),
          lambda a,b:a["source"].__setitem__("revision_id",1),
          lambda a,b:b.__setitem__("source_sha256","0"*64),
          lambda a,b:b["metrics"][4].__setitem__("actual",0),
          lambda a,b:b["metrics"][0].__setitem__("reference",0),
          lambda a,b:b.__setitem__("translator",{"id":"fake","name":"fake"}),
        ):
            a,b=deepcopy(self.artifact),deepcopy(self.book)
            mutate(a,b)
            with self.assertRaises(AssertionError):check(a,b)

if __name__=="__main__":
    unittest.main()
