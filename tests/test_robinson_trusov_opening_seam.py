import json
import unittest

from scriptorium.robinson_trusov_content import transclusion_input
from scriptorium.robinson_trusov_opening_seam import capture, diagnose, digest


class OpeningSeamTests(unittest.TestCase):
    def test_exact_excluded_continuation(self):
        first = "<noinclude>heading</noinclude>Opening privateword."
        second = "<noinclude>header</noinclude>\n<noinclude>word.</noinclude> Next sentence."
        result = diagnose(first, second)
        self.assertEqual(result, {
            "classification": "PAGE_BOUNDARY_CONTINUATION_NOINCLUDE",
            "excluded_letters": 4, "excluded_punctuation": 1,
            "left_suffix_matches": True, "right_prefix_repeats": False,
        })
        self.assertNotIn("word.", json.dumps(result))

    def test_refuse_unmatched_repeated_or_nonleading_span(self):
        header = "<noinclude>header</noinclude>"
        for left, right, status in [
            ("Other.", header + "<noinclude>word.</noinclude> Next.",
             "SCOPE_HYPOTHESIS_REFUSED"),
            ("privateword.", header + "<noinclude>word.</noinclude> word. Next.",
             "SCOPE_HYPOTHESIS_REFUSED"),
            ("privateword.", header + "Body <noinclude>word.</noinclude> Next.",
             "NO_ELIGIBLE_LEADING_SPAN"),
            ("privateword.", header + "<noinclude>{{word}}</noinclude> Next.",
             "NO_ELIGIBLE_LEADING_SPAN"),
        ]:
            with self.subTest(status=status):
                self.assertEqual(diagnose(left, right)["classification"], status)

    def test_capture_verifies_both_raw_and_transclusion_digests(self):
        texts = {2: "privateword.", 3: "<noinclude>header</noinclude>"
                 "<noinclude>word.</noinclude> Next."}
        graph = {"pages": []}
        preflight = {"source_page_graph_sha256": "a"*64, "pages": []}
        rows = []
        for n, raw in texts.items():
            p = {"page_sequence": n, "revision_id": n+100, "page_id": n+200,
                 "title": f"Page:{n}", "timestamp_utc": "2023-08-17T00:00:00Z",
                 "mediawiki_sha1": "b"*40}
            graph["pages"].append(p)
            candidate = transclusion_input(raw)
            preflight["pages"].append({
                "page_sequence": n, "revision_id": n+100, "wikitext_sha256": digest(raw),
                "wikitext_utf8_bytes": len(raw.encode("utf-8")),
                "transclusion_input_sha256": digest(candidate),
                "transclusion_input_characters_including_spaces": len(candidate)})
            rows.append({"pageid": n+200, "title": p["title"], "revisions": [{
                "revid": n+100, "timestamp": p["timestamp_utc"], "sha1": p["mediawiki_sha1"],
                "slots": {"main": {"content": raw}}}]})
        calls = []
        def query(params):
            calls.append(params["revids"])
            return {"query": {"pages": list(reversed(rows))}}
        report = capture(graph, preflight, query=query)
        self.assertEqual(calls, ["102|103"])
        self.assertEqual([p["page_sequence"] for p in report["pages"]], [2, 3])
        self.assertNotIn("privateword", json.dumps(report))
        self.assertFalse(report["corpus_admitted"])
        for key in ("wikitext_sha256", "transclusion_input_sha256"):
            with self.subTest(key=key):
                old = preflight["pages"][0][key]
                preflight["pages"][0][key] = "0"*64
                with self.assertRaisesRegex(ValueError, "preflight byte drift"):
                    capture(graph, preflight, query=query)
                preflight["pages"][0][key] = old
        rows[0]["revisions"][0]["sha1"] = "0"*40
        with self.assertRaisesRegex(ValueError, "identity drift"):
            capture(graph, preflight, query=query)


if __name__ == "__main__":
    unittest.main()
