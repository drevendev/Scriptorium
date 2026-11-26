import json
import unittest

from scriptorium.robinson_trusov_content import transclusion_input
from scriptorium.robinson_trusov_opening_seam import (
    capture, diagnose, digest, opening_layout, spacing_target_observation,
)


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


    def test_layout_partition_preserves_count_and_excludes_title(self):
        prefix = "{{^}}\n{{heading|36|TITLE}} {{heading|36|A}}\n" \
                 "{{heading|36|B}} {{heading|38|C D}}\n{{^}}"
        body = "Private narrative.\nSecond paragraph."
        result = opening_layout(prefix + "\n" + body + " ")
        self.assertEqual(result["heading_calls"], 4)
        self.assertEqual(result["spacing_calls"], 2)
        self.assertEqual(result["title_nonspace_characters"], 9)
        self.assertEqual(result["body_candidate_characters_including_spaces"], len(body))
        self.assertEqual(result["input_characters_including_spaces"],
                         result["layout_prefix_characters"]
                         + result["body_candidate_characters_including_spaces"]
                         + result["body_edge_whitespace_characters"])
        self.assertNotIn("Private", json.dumps(result))
        for changed in (prefix.replace("{{^}}", "{{^|1em}}", 1),
                        prefix.replace("heading|38", "heading|36"),
                        prefix.replace("TITLE", "lower"),
                        prefix + "{{unknown}}"):
            with self.assertRaises(ValueError):
                opening_layout(changed + body)
        with self.assertRaises(ValueError):
            opening_layout(prefix)

    def test_spacing_target_revisions_and_refusal(self):
        raw = "<div style=margin-top:{{#if:{{{1|}}}|{{{1}}}|2em}}></div><noinclude>doc</noinclude>"
        revisions = [
            {"revid": rid, "timestamp": timestamp, "sha1": "a"*40,
             "slots": {"main": {"content": raw}}}
            for rid, timestamp in ((4937800, "2023-07-23T15:49:01Z"),
                                   (5183352, "2024-10-03T16:40:01Z"))]
        def query(params):
            self.assertEqual(params["revids"], "4937800|5183352")
            return {"query": {"pages": [{"title": "Шаблон:^", "pageid": 123,
                                        "revisions": list(reversed(revisions))}]}}
        result = spacing_target_observation(query=query)
        self.assertTrue(result["target_bytes_equal"])
        self.assertEqual(result["historical_redirect_bytes"], "NOT_VERIFIED")
        self.assertFalse(result["historical_render_equivalence_proven"])
        self.assertNotIn("<div", json.dumps(result))
        revisions[1]["slots"]["main"]["content"] = raw.replace("doc", "other")
        with self.assertRaisesRegex(ValueError, "bytes differ"):
            spacing_target_observation(query=query)
        revisions[1]["slots"]["main"]["content"] = raw.replace("2em", "3em")
        with self.assertRaisesRegex(ValueError, "surface differs"):
            spacing_target_observation(query=query)


if __name__ == "__main__":
    unittest.main()
