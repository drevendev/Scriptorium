"""Source-bound ninth measured Reader book: no prose, no parity inflation."""
from copy import deepcopy
from hashlib import sha1
import json
from pathlib import Path
import unittest

ROOT=Path(__file__).resolve().parents[1]
RAW=ROOT/"corpus/candidates/diagnostics/goncharov-oblomov-ru.json"
DATA=ROOT/"assets/evidence-snapshot.json"
BODY_SHA="144a5ea17195e7ce10d69a5855a67781510dac51fd44237e1bc856536c3b3887"

def check(artifact,book):
    assert artifact["candidate_id"] == book["candidate_id"] == "goncharov-oblomov-azlib-ru"
    assert artifact["source"]["revision_id"] == book["source_revision_id"] == 5724579
    assert artifact["source"]["legal_basis"] == "public_domain_author_died_1891"
    assert artifact["gates"]["source_text_committed"] is False
    assert artifact["gates"]["complete_chapter_inventory"] is True
    assert artifact["gates"]["source_edition_print_collation"] == "NOT_RUN"
    assert artifact["gates"]["fantlab_input_identity"] == "UNKNOWN"
    assert artifact["gates"]["m2_parity_admissible"] is False
    assert artifact["gates"]["m2_weight"] == 0
    assert artifact["body"]["raw_sha256"] == book["source_sha256"] == BODY_SHA
    assert artifact["body"]["characters_including_spaces"] == 930248
    assert book["edition_id"] == "ru-wikisource-az-lib-oldid-5724579"
    assert book["original_language"] == book["language"] == "ru"
    assert book["text_status"] == "measured"
    assert book["measured"] == 24 and book["unavailable"] == 5
    rows=artifact["metric_rows"]
    assert len(rows) == len(book["metrics"]) == 29
    assert len({r["metric_id"] for r in rows}) == 29
    assert sum(r["actual"] is not None for r in rows) == 24
    assert sum(r["actual"] is None for r in rows) == 5
    assert all(r["fantlab_display"] is None for r in rows)
    assert book["profiles"] == artifact["scriptorium"]["profiles"]
    for row,m in zip(rows,book["metrics"]):
        assert m["id"] == row["metric_id"]
        assert m["actual"] == row["actual"]
        assert m["reference"] is None
        assert m["status"] == ("measured" if row["actual"] is not None else "not_run")
        assert m["kind"] == ("extension" if row["compatibility_status"] == "extension" else "candidate")

class OblomovReaderTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.artifact=json.loads(RAW.read_text(encoding="utf-8"))
        cls.catalog=json.loads(DATA.read_text(encoding="utf-8"))
        cls.book=next(b for b in cls.catalog["books"] if b["key"]=="oblomov")
    def test_real_evidence_without_prose(self):
        check(self.artifact,self.book)
        raw=RAW.read_bytes()
        self.assertEqual(self.book["blob_sha1"],sha1(b"blob "+str(len(raw)).encode()+b"\0"+raw).hexdigest())
        self.assertNotIn("literary_body",self.artifact)
        self.assertNotIn("wikitext",self.artifact)
        html=(ROOT/"index.html").read_text(encoding="utf-8")
        self.assertIn('data-status="measured" data-catalog-key="oblomov"',html)
        self.assertIn('data-book="oblomov"',html)
        self.assertIn('<tr><th scope="row">Обломов</th><td>41.849119265457624</td><td>%</td></tr>',html)
        self.assertEqual(self.catalog["counts"]["metrics_total"],240)
        self.assertEqual(self.catalog["counts"]["numeric_total"],201)
        self.assertEqual(self.catalog["counts"]["unavailable_total"],39)
        self.assertEqual(self.catalog["counts"]["m2_source_matched"],0)
    def test_tampering_rejected(self):
        for change in (
          lambda a,b: a["gates"].__setitem__("m2_parity_admissible",True),
          lambda a,b: a["source"].__setitem__("revision_id",1),
          lambda a,b: b.__setitem__("source_sha256","0"*64),
          lambda a,b: b["metrics"][4].__setitem__("actual",42),
          lambda a,b: b["metrics"][0].__setitem__("reference",0),
        ):
            a,b=deepcopy(self.artifact),deepcopy(self.book)
            change(a,b)
            with self.assertRaises(AssertionError):
                check(a,b)

if __name__=="__main__":
    unittest.main()
