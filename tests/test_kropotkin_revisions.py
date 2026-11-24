import unittest
from scriptorium import kropotkin_revisions as k


def page(title, rid):
    return {"title": title, "revisions": [{"revid": rid, "timestamp": "2026-01-01T00:00:00Z", "sha1": "a" * 40}]}


def provider(params):
    if params["action"] == "parse":
        rid = int(params["oldid"])
        titles = (*k.ADVERTISED_ROUTES, k.EXCLUDED) if rid == k.INDEX_ID else (k.ADVERTISED_III,)
        return {"parse": {"revid": rid, "links": [{"title": t, "ns": 0} for t in titles]}}
    assert params["rvprop"] == "ids|timestamp|sha1"
    if "revids" in params:
        pages = [page(k.SCAN_TITLE, k.SCAN_ID), page(k.TITLE, k.INDEX_ID)]
    else:
        pages = [page(t, i + 1) for i, t in enumerate((*k.ROUTES, k.ADVERTISED_III))][::-1]
    return {"query": {"pages": pages}}


class KropotkinRevisionsTests(unittest.TestCase):
    def test_complete_ordered_source_free_capture(self):
        result = k.capture(provider)
        self.assertEqual(len(result["routes"]), 29)
        self.assertEqual([r["title"] for r in result["routes"]], list(k.ROUTES))
        self.assertEqual([r["revision_id"] for r in result["anchors"]], [k.INDEX_ID, k.SCAN_ID])
        self.assertEqual(result["index_route_exception"]["selected_modern_title"], k.MODERN_III)
        self.assertEqual(result["index_route_exception"]["advertised_historical_identity"]["title"], k.ADVERTISED_III)
        self.assertNotIn(k.ADVERTISED_III, [r["title"] for r in result["routes"]])
        self.assertIsNone(result["body_characters"])
        self.assertFalse(result["m2_parity_admissible"])
        self.assertFalse(result["body_frozen"])
        self.assertEqual(result, k.capture(provider))

    def test_index_drift_rejected(self):
        def changed(params):
            result = provider(params)
            if params["action"] == "parse":
                result["parse"]["links"].pop()
            return result
        with self.assertRaises(ValueError):
            k.capture(changed)

    def test_missing_route_rejected(self):
        def changed(params):
            result = provider(params)
            if "titles" in params:
                result["query"]["pages"].pop()
            return result
        with self.assertRaises(ValueError):
            k.capture(changed)

    def test_invalid_revision_rejected(self):
        for key, val in [("revid", True), ("timestamp", "2026-02-30T00:00:00Z"), ("sha1", "bad")]:
            with self.subTest(key=key):
                def changed(params):
                    result = provider(params)
                    if "titles" in params:
                        result["query"]["pages"][0]["revisions"][0][key] = val
                    return result
                with self.assertRaises(ValueError):
                    k.capture(changed)

    def test_duplicate_revision_rejected(self):
        def changed(params):
            result = provider(params)
            if "titles" in params:
                pages = result["query"]["pages"]
                pages[0]["revisions"][0]["revid"] = pages[1]["revisions"][0]["revid"]
            return result
        with self.assertRaises(ValueError):
            k.capture(changed)

    def test_modern_link_to_historical_required(self):
        def changed(params):
            result = provider(params)
            if params["action"] == "parse" and int(params["oldid"]) != k.INDEX_ID:
                result["parse"]["links"] = []
            return result
        with self.assertRaisesRegex(ValueError, "modern appendix III lacks link"):
            k.capture(changed)

    def test_index_variant_drift_rejected(self):
        def changed(params):
            result = provider(params)
            if params["action"] == "parse" and int(params["oldid"]) == k.INDEX_ID:
                for link in result["parse"]["links"]:
                    if link["title"] == k.ADVERTISED_III:
                        link["title"] = k.MODERN_III
            return result
        with self.assertRaisesRegex(ValueError, "Приложение/3/ДО"):
            k.capture(changed)
