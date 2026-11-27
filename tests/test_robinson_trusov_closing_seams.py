import json
import unittest

from scriptorium.robinson_trusov_closing_seams import (
    PINS, capture, diagnose, diagnose_pages, digest, literal_branches,
    wrapper_signature, page151_branches,
)
from scriptorium.robinson_trusov_content import transclusion_input


def page(a, b):
    return "<noinclude>header</noinclude>{{ВАР|" + a + "|" + b + "}}<noinclude>footer</noinclude>"


def fixture():
    return {
        148: page("First. <noinclude>the</noinclude>", "First. <noinclude>an</noinclude>"),
        149: page("the beginning unfinished.", "an introduction unfinished."),
        150: page("<noinclude>nished</noinclude> Next ending.",
                  "<noinclude>nished</noinclude> More ending."),
        151: page("<noinclude>ing</noinclude> Final sentence.",
                  "<noinclude>ing</noinclude> Last sentence."),
    }



def special_page151():
    return ("<noinclude>header</noinclude>{{ вар |"
            "<noinclude>ing</noinclude><!--PRIVATE_LEFT--> Final sentence.|"
            "<!--PRIVATE_RIGHT--><noinclude>ing</noinclude> Last sentence."
            "}}<noinclude><!--PRIVATE_FOOTER-->footer</noinclude>")


class ClosingSeamTests(unittest.TestCase):
    def test_six_literal_seams_and_source_free_endings(self):
        seams, endings = diagnose_pages(fixture())
        self.assertEqual([x["excluded_letters"] for x in seams], [3, 2, 6, 6, 3, 3])
        self.assertEqual([x["owner"] for x in seams], ["right"] * 2 + ["left"] * 4)
        self.assertTrue(all(x["ends_in_sentence_punctuation"] for x in endings))
        self.assertNotIn("unfinished", json.dumps([seams, endings]))
        self.assertNotIn("Final sentence", json.dumps([seams, endings]))

    def test_refuse_wrong_owner_duplicate_and_unrelated_note(self):
        for left, right, edge, count in (
            ("First <noinclude>the</noinclude>", "other words.", "trailing", 3),
            ("First the <noinclude>the</noinclude>", "the rest.", "trailing", 3),
            ("First <noinclude>the</noinclude>", "there.", "trailing", 3),
            ("unfinished.", "<noinclude>nished</noinclude> nished again.", "leading", 6),
            ("nished.", "<noinclude>nished</noinclude> other.", "leading", 6),
            ("unfinished.", "<noinclude>nished</noinclude> other <noinclude>note</noinclude>.", "leading", 6),
            ("unfinished.", "<noinclude>note 1</noinclude> other.", "leading", 6),
        ):
            with self.subTest(edge=edge, count=count):
                with self.assertRaises(ValueError):
                    diagnose(left, right, edge=edge, letters=count)

    def test_closing_seam_refusals_cover_both_branches_and_later_joins(self):
        raws = fixture()
        raws[148] = page("First. <noinclude>the</noinclude>PRIVATE_SUFFIX",
                         "First.")
        raws[150] = page("<noinclude>broken</noinclude> Next ending.",
                         "<noinclude>nished</noinclude> More ending.")
        with self.assertRaisesRegex(ValueError, "closing seam ownership") as caught:
            diagnose_pages(raws)
        message = str(caught.exception)
        self.assertNotIn("PRIVATE_SUFFIX", message)
        self.assertNotIn("broken", message)
        self.assertNotIn("unfinished", message)
        report = json.loads(message.split(": ", 1)[1])
        self.assertEqual(report["successful_assertions"], 3)
        rows = report["refusals"]
        self.assertEqual([(r["left_page"], r["right_page"], r["branch_index"],
                           r["expected_edge_page"], r["expected_edge_revision"],
                           r["reason"]) for r in rows], [
            (148, 149, 0, 148, PINS[148], "EDGE_NOINCLUDE_MISSING"),
            (148, 149, 1, 148, PINS[148], "EDGE_NOINCLUDE_MISSING"),
            (149, 150, 0, 150, PINS[150], "COUNT_OR_OWNERSHIP"),
        ])
        first = rows[0]["left_trailing"]
        self.assertEqual(first["shape"], "ADDITIONAL_EDGE_STRUCTURE")
        self.assertEqual(first["pair_count"], 1)
        pair, = first["pairs"]
        self.assertTrue(pair["exact_tags"])
        self.assertTrue(pair["letter_only_body"])
        self.assertFalse(pair["at_expected_edge"])
        self.assertEqual(pair["suffix_counts"]["characters"], len("PRIVATE_SUFFIX"))
        self.assertEqual(pair["suffix_counts"]["letters"], len("PRIVATESUFFIX"))
        self.assertEqual(rows[1]["left_trailing"]["shape"], "ABSENT")
        self.assertEqual(rows[2]["right_leading"]["shape"], "STRICT_MATCH")

    def test_closing_seam_nonliteral_scope_still_refused(self):
        for markup in ("<noinclude >the</noinclude>",
                       "<noinclude><b>the</b></noinclude>"):
            with self.subTest(markup=markup):
                raws = fixture()
                raws[148] = page("First. " + markup,
                                 "First. <noinclude>an</noinclude>")
                with self.assertRaisesRegex(ValueError, "closing seam ownership") as caught:
                    diagnose_pages(raws)
                report = json.loads(str(caught.exception).split(": ", 1)[1])
                self.assertEqual(report["successful_assertions"], 5)
                row, = report["refusals"]
                self.assertEqual(row["reason"], "EDGE_NOINCLUDE_MISSING")
                self.assertEqual(row["left_trailing"]["shape"], "NONLITERAL_SCOPE")
                self.assertNotIn(markup, str(caught.exception))

    def test_refuse_unexpected_var_shape_and_end(self):
        for raw in ("plain", page("a", "b") + "extra body",
                    page("a", "b") + "{{ВАР|c|d}}", page("a|extra", "b")):
            with self.assertRaises(ValueError):
                literal_branches(raw)
        raw = fixture()
        raw[151] = raw[151].replace("Final sentence.", "Final sentence")
        with self.assertRaisesRegex(ValueError, "punctuation"):
            diagnose_pages(raw)

    def test_refusals_locate_all_pinned_pages_without_source(self):
        raw = fixture()
        raw[148] = page("PRIVATE_MARKER {{other|x}}", "plain")
        raw[151] = page("one", "two") + "PRIVATE_OUTER"
        with self.assertRaisesRegex(ValueError, "structural refusal") as caught:
            diagnose_pages(dict(reversed(list(raw.items()))))
        message = str(caught.exception)
        self.assertNotIn("PRIVATE_MARKER", message)
        self.assertNotIn("PRIVATE_OUTER", message)
        self.assertNotIn("other", message)
        rows = json.loads(message.split(": ", 1)[1])
        self.assertEqual([(x["page_sequence"], x["revision_id"], x["reason"])
                          for x in rows], [
            (148, PINS[148], "VAR_MATCH_COUNT"),
            (151, PINS[151], "OUTER_SCOPE_OR_INCLUSION_REFUSED"),
        ])
        self.assertEqual(rows[0]["raw_structure"]["var_starts"], 1)
        self.assertEqual(rows[0]["raw_structure"]["template_opens"], 2)
        self.assertEqual(rows[0]["raw_structure"]["literal_var_matches"], 0)
        self.assertEqual(rows[1]["transclusion_structure"]["literal_var_matches"], 1)
        self.assertTrue(all(x["transclusion_structure"]["noinclude_opens"] == 0
                            for x in rows))

    def test_page151_signature_distinguishes_comment_and_delimiter_order(self):
        raw = fixture()
        raw[151] = page("PRIVATE_A<!--PRIVATE_COMMENT {-->",
                        "PRIVATE_B<!--PRIVATE_OTHER }-->")
        with self.assertRaisesRegex(ValueError, "structural refusal") as caught:
            diagnose_pages(raw)
        message = str(caught.exception)
        self.assertNotIn("PRIVATE", message)
        row, = json.loads(message.split(": ", 1)[1])
        self.assertEqual(row["page_sequence"], 151)
        expected = ["VAR_OPEN_EXACT", {"kind": "COMMENT", "braces": 1, "pipes": 0},
                    "PIPE", {"kind": "COMMENT", "braces": 1, "pipes": 0}, "CLOSE"]
        self.assertEqual(row["transclusion_wrapper_signature"],
                         {"events": expected, "truncated": False})
        self.assertEqual(row["raw_wrapper_signature"]["events"],
                         ["NOINCLUDE_OPEN", "NOINCLUDE_CLOSE", *expected,
                          "NOINCLUDE_OPEN", "NOINCLUDE_CLOSE"])
        # The observation is not permission to accept the previously refused wrapper.
        with self.assertRaises(ValueError):
            literal_branches(raw[151])

    def test_wrapper_signature_nonexact_open_and_bounded_events(self):
        self.assertEqual(wrapper_signature("{{ ВАР |one|two}}}")["events"],
                         ["VAR_OPEN_NONEXACT", "PIPE", "CLOSE", "RIGHT_BRACE"])
        self.assertEqual(wrapper_signature("|" * 33),
                         {"events": ["PIPE"] * 32, "truncated": True})
        with self.assertRaises(ValueError):
            literal_branches("{{ ВАР |one|two}}")


    def test_pinned_leaf_candidate_preserves_both_seam_owners(self):
        raws = fixture()
        raws[151] = special_page151()
        branches, opener = page151_branches(raws[151])
        self.assertEqual(opener, "{{ вар |")
        self.assertEqual(branches, ("<noinclude>ing</noinclude> Final sentence.",
                                    "<noinclude>ing</noinclude> Last sentence."))
        seams, endings = diagnose_pages(raws)
        self.assertEqual([x["excluded_letters"] for x in seams], [3, 2, 6, 6, 3, 3])
        self.assertTrue(all(x["owner_matches"] for x in seams))
        self.assertTrue(all(x["ends_in_sentence_punctuation"] for x in endings))
        self.assertNotIn("PRIVATE", json.dumps([seams, endings]))
        with self.assertRaises(ValueError):
            literal_branches(raws[151])

    def test_pinned_leaf_preserves_literal_gap_and_whitespace(self):
        original = special_page151()
        for gap in (" First clause,\n  second clause.  ", " First clause."):
            with self.subTest(gap=gap):
                raws = fixture()
                raws[151] = original.replace("<!--PRIVATE_LEFT-->", gap + "<!--PRIVATE_LEFT-->")
                branches, _ = page151_branches(raws[151])
                expected = "<noinclude>ing</noinclude>" + gap + " Final sentence."
                self.assertEqual(branches[0].encode("utf-8"), expected.encode("utf-8"))
                self.assertEqual(transclusion_input(branches[0]), gap + " Final sentence.")
                seams, endings = diagnose_pages(raws)
                self.assertEqual([x["excluded_letters"] for x in seams], [3, 2, 6, 6, 3, 3])
                self.assertEqual(endings[0]["candidate_characters_including_spaces"],
                                 len((gap + " Final sentence.").strip()))
                self.assertNotIn("First clause", json.dumps([seams, endings]))

    def test_pinned_leaf_refuses_lexical_join_across_comment(self):
        for left, right in (("word", "word"), ("a", "\u0301"), ("word-", "word"),
                            ("word'", "word")):
            raw = special_page151().replace("<!--PRIVATE_LEFT--> Final",
                                             " " + left + "<!--PRIVATE_LEFT-->" + right)
            with self.subTest(left=left, right=right):
                with self.assertRaisesRegex(ValueError, "PAGE151_COMMENT_TOKEN_JOIN"):
                    page151_branches(raw)

    def test_pinned_leaf_candidate_refuses_unobserved_shapes(self):
        original = special_page151()
        for raw in (
            original.replace("PRIVATE_LEFT", "PRIVATE_LEFT|"),
            original.replace("PRIVATE_RIGHT", "PRIVATE_RIGHT{"),
            original.replace("<!--PRIVATE_LEFT-->", "<!--PRIVATE_LEFT--><!--extra-->"),
            original.replace("<noinclude>ing</noinclude><!--PRIVATE_LEFT-->",
                             "<!--PRIVATE_LEFT--><noinclude>ing</noinclude>"),
            original.replace("<!--PRIVATE_LEFT--> Final", " Final<!--PRIVATE_LEFT-->word"),
            original.replace("<!--PRIVATE_LEFT-->", " <b>gap</b><!--PRIVATE_LEFT-->"),
            original.replace("{{ вар |", "{{ OTHER |"),
            original.replace("{{ вар |", "{{ВАР|"),
            original.replace("footer</noinclude>", "footer</noinclude>extra"),
        ):
            with self.subTest(case=raw.count("<!--")):
                with self.assertRaises(ValueError):
                    page151_branches(raw)
        raws = fixture()
        raws[151] = original.replace("<noinclude>ing</noinclude>", "<noinclude>bad</noinclude>", 1)
        with self.assertRaisesRegex(ValueError, "ownership"):
            diagnose_pages(raws)
        raws = fixture()
        raws[150] = original
        with self.assertRaisesRegex(ValueError, "structural refusal"):
            diagnose_pages(raws)

    def test_page151_diagnose_retains_actual_reason_with_matching_signatures(self):
        original = special_page151()
        cases = (
            (original.replace("{{ вар |", "{{ вар |PRIVATE_PREFIX"),
             "PAGE151_LEADING_PREFIX_NONSPACE", 0),
            (original.replace("<noinclude>ing</noinclude>", "<noinclude >ing</noinclude>", 1),
             "PAGE151_LEADING_TAG_VARIANT", 0),
            (original.replace("<noinclude>ing</noinclude>", "<noinclude><b>ing</b></noinclude>", 1),
             "PAGE151_LEADING_BODY_MARKUP", 0),
            (original.replace("<!--PRIVATE_RIGHT--><noinclude>", "<!--PRIVATE_RIGHT-->PRIVATE_PREFIX<noinclude>"),
             "PAGE151_LEADING_PREFIX_NONSPACE", 1),
            (original.replace("<!--PRIVATE_LEFT--> Final", " PRIVATE_GAP<!--PRIVATE_LEFT-->Final"),
             "PAGE151_COMMENT_TOKEN_JOIN", 0),
            (original.replace("<!--PRIVATE_RIGHT-->", "PRIVATE_GAP<!--PRIVATE_RIGHT-->"),
             "PAGE151_COMMENT_PREFIX_NONSPACE", 1),
            (original.replace("<noinclude>ing</noinclude>", "<noinclude>123</noinclude>", 1),
             "PAGE151_EDGE_SCOPE", 0),
            (original.replace("<!--PRIVATE_RIGHT--><noinclude>ing</noinclude>",
                              "<!--PRIVATE_RIGHT--><noinclude>123</noinclude>"),
             "PAGE151_EDGE_SCOPE", 1),
        )
        for invalid, reason, index in cases:
            with self.subTest(reason=reason, index=index):
                self.assertEqual(wrapper_signature(invalid), wrapper_signature(original))
                self.assertEqual(wrapper_signature(transclusion_input(invalid)),
                                 wrapper_signature(transclusion_input(original)))
                raws = fixture()
                raws[151] = invalid
                with self.assertRaisesRegex(ValueError, "structural refusal") as caught:
                    diagnose_pages(raws)
                message = str(caught.exception)
                self.assertNotIn("PRIVATE", message)
                self.assertNotIn("123", message)
                row, = json.loads(message.split(": ", 1)[1])
                self.assertEqual((row["page_sequence"], row["revision_id"]), (151, PINS[151]))
                self.assertEqual(row["raw_structure"]["literal_var_matches"], 0)
                self.assertEqual(row["reason"], reason)
                self.assertEqual(row["page151_reason"], reason)
                self.assertEqual(row["branch_index"], index)
                if reason in ("PAGE151_LEADING_PREFIX_NONSPACE",
                              "PAGE151_COMMENT_PREFIX_NONSPACE",
                              "PAGE151_LEADING_BODY_MARKUP"):
                    self.assertEqual(set(row["fragment_counts"]), {
                        "whitespace", "letters", "digits", "apostrophes",
                        "angle_brackets", "other",
                    })
                    self.assertGreater(row["fragment_counts"]["letters"], 0)
                    self.assertTrue(all(type(n) is int for n in row["fragment_counts"].values()))
                else:
                    self.assertNotIn("fragment_counts", row)

    def test_exact_pins_and_preflight_tamper(self):
        raw = fixture()
        raw[151] = special_page151().replace("<!--PRIVATE_LEFT-->", " A clause.  <!--PRIVATE_LEFT-->")
        graph, prior, rows = {"pages": []}, {"pages": [], "source_page_graph_sha256": "a"*64}, []
        for n, rid in PINS.items():
            pin = {"page_sequence": n, "revision_id": rid, "page_id": n,
                   "title": str(n), "timestamp_utc": "2023-08-17T00:00:00Z",
                   "mediawiki_sha1": "b"*40}
            graph["pages"].append(pin)
            source = raw[n]
            candidate = transclusion_input(source)
            prior["pages"].append({"page_sequence": n, "revision_id": rid,
                "wikitext_sha256": digest(source), "wikitext_utf8_bytes": len(source.encode()),
                "transclusion_input_sha256": digest(candidate),
                "transclusion_input_characters_including_spaces": len(candidate)})
            rows.append({"pageid": n, "title": str(n), "revisions": [{
                "revid": rid, "timestamp": pin["timestamp_utc"], "sha1": pin["mediawiki_sha1"],
                "slots": {"main": {"content": source}}}]})
        def query(params):
            self.assertEqual(params["revids"], "|".join(map(str, PINS.values())))
            return {"query": {"pages": list(reversed(rows))}}
        result = capture(graph, prior, query=query)
        self.assertEqual([p["revision_id"] for p in result["pages"]], list(PINS.values()))
        self.assertEqual(len(result["seams"]), 6)
        self.assertEqual(result["page151_var_opener"], "{{ вар |")
        self.assertEqual(result["page151_branch_comments_removed"], 2)
        self.assertNotIn("PRIVATE", json.dumps(result))
        self.assertFalse(result["corpus_admitted"])
        self.assertEqual(result["facing_errata_excluded_by_full_collation"], "NOT_VERIFIED")
        prior["pages"][0]["wikitext_sha256"] = "0"*64
        with self.assertRaisesRegex(ValueError, "byte drift"):
            capture(graph, prior, query=query)


if __name__ == "__main__":
    unittest.main()
