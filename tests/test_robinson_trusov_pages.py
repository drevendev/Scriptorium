"""Source-free Trusov Page graph: positive, drift and safety regressions."""
import copy
from hashlib import sha256
import json
import unittest
from scriptorium.robinson_trusov_pages import capture, select_pages, validate, WORK_ID

SOURCE = '<pages index="Том 1.djvu" from="10" to="12" />'
TITLE = 'Жизнь и приключения Робинзона Круза, природного англичанина (Дефо; Трусов)/1775 (ДО)/1'
ANCHOR = '2023-09-03T17:55:09Z'


def inventory(source=SOURCE):
    raw = source.encode('utf-8')
    return {'schema_version':'scriptorium-robinson-revision-inventory-v1',
            'witnesses':[{'work_id':WORK_ID,'revision_id':5041937,'page_id':946461,
                'title':TITLE,'timestamp_utc':ANCHOR,'mediawiki_sha1':'a'*40,
                'wikitext_sha256':sha256(raw).hexdigest(),'wikitext_utf8_bytes':len(raw),
                'wikitext_characters_including_spaces':len(source)}]}


def mock_query(params):
    if 'revids' in params:
        return {'query':{'pages':[{'pageid':946461,'title':TITLE,'revisions':[{
            'revid':5041937,'timestamp':ANCHOR,'sha1':'a'*40,
            'slots':{'main':{'contentmodel':'wikitext','content':SOURCE}}
        }]}]}}
    titles = params['titles'].split('|')
    assert params['rvdir']=='older' and params['rvstart']==ANCHOR
    return {'query':{'pages':[{'pageid':900+i,'title':title,'revisions':[{
        'revid':1000+int(title.rsplit('/',1)[1]),'timestamp':'2022-01-01T00:00:00Z',
        'sha1':'b'*40}]} for i,title in enumerate(titles)]}}


class TrusovGraphTests(unittest.TestCase):
    def test_capture_is_ordered_and_source_free(self):
        artifact=capture(inventory(),query=mock_query)
        self.assertEqual(artifact['selection']['page_count'],3)
        self.assertEqual([r['page_sequence'] for r in artifact['pages']],[10,11,12])
        self.assertEqual(len(artifact['pages']),3)
        self.assertFalse(artifact['historical_render_equivalence_proven'])
        self.assertFalse(artifact['corpus_threshold_verified'])
        self.assertFalse(artifact['m2_parity_admissible'])
        self.assertNotIn(SOURCE,json.dumps(artifact,ensure_ascii=False))
        validate(artifact)

    def test_fail_closed_on_complex_or_unsafe_selectors(self):
        for value in ('<pages index="x.djvu" from="1" to="4" exclude="2" />',
            '<pages index="x.djvu" from="1" to="3" /><pages index="x.djvu" from="4" to="5"/>',
            '<pages index="x.djvu" from="1" />',
            '<pages index="x.djvu" from="11" to="9" />',
            '<pages index="x.djvu" from="1" to="751" />',
            '<pages index="evil|title.djvu" from="1" to="4" />',
            '<pages index="x.djvu" from="1" to="3" onlysection="chapter"/>'):
            with self.subTest(value=value), self.assertRaises(ValueError): select_pages(value)

    def test_carrier_must_match_pinned_source(self):
        bad=inventory();bad['witnesses'][0]['wikitext_sha256']='0'*64
        with self.assertRaisesRegex(ValueError,'carrier identity mismatch'):
            capture(bad,query=mock_query)

    def test_future_page_revision_is_not_historic(self):
        def future(params):
            result=mock_query(params)
            if 'titles' in params:
                result['query']['pages'][0]['revisions'][0]['timestamp']='2025-01-01T00:00:00Z'
            return result
        with self.assertRaisesRegex(ValueError,'historical Page revision'):
            capture(inventory(),query=future)

    def test_missing_page_prevents_partial_capture(self):
        def missing(params):
            result=mock_query(params)
            if 'titles' in params:
                result['query']['pages'].pop()
            return result
        with self.assertRaisesRegex(ValueError,'incomplete'):
            capture(inventory(),query=missing)

    def test_manifest_validation_rejects_injected_prose(self):
        record=capture(inventory(),query=mock_query)
        altered=copy.deepcopy(record)
        altered['pages'][0]['wikitext']='secret literary prose'
        with self.assertRaisesRegex(ValueError,'prose leakage'):
            validate(altered)
        altered=copy.deepcopy(record)
        altered['m2_parity_admissible']=True
        with self.assertRaisesRegex(ValueError,'scientific gate'):
            validate(altered)


if __name__ == '__main__':
    unittest.main()
