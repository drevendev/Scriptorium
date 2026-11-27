"""Synthetic missing-folio marker and preservation checks."""
import unittest
from html import escape

from scriptorium.robinson_trusov_missing_folios import compare, partition, marker_shape, LABELS, WRAPPERS, CarrierView
from scriptorium.robinson_trusov_content import transclusion_input


class MissingFolioTests(unittest.TestCase):
    def setUp(self):
        self.middle = "\n\n".join(["Первый пример.", "Второй пример.", "Третий пример.",
                                   "Четвёртый пример.", "Пятый пример.", "Шестой пример,"]) + " "
        self.tail = "который продолжается."
        self.raw = "<noinclude>header</noinclude>" + WRAPPERS[0] + self.middle + WRAPPERS[1] + self.tail
        self.body = transclusion_input(self.raw)
        self.left = "До начала."
        self.right = "После конца."
        self.rendered = self.left + " " + self.body + " " + self.right

    def test_both_markers_excluded_without_text_loss(self):
        self.assertEqual(partition(self.raw), (self.middle, self.tail))
        r = compare(self.raw, self.body, self.body, self.left, self.right, self.rendered)
        self.assertEqual(r["lanes"]["raw"]["marker_counts"], [1, 1])
        for lane in ("transclusion", "projected", "rendered"):
            self.assertEqual(r["lanes"][lane]["paragraph_matches"], [1] * 6)
            self.assertEqual(r["lanes"][lane]["marker_counts"], [0, 0])
            self.assertEqual(r["lanes"][lane]["second_marker_continuation_matches"], 1)

    def test_duplicate_or_missing_marker_refused(self):
        for raw in (self.raw + WRAPPERS[0], self.raw.replace(WRAPPERS[1], "")):
            with self.assertRaises(ValueError):
                partition(raw)

    def test_moved_marker_and_join_refused(self):
        with self.assertRaises(ValueError):
            partition(self.raw.replace(", " + WRAPPERS[1], "," + WRAPPERS[1]))

    def test_marker_layout_variants_preserve_exact_body(self):
        raw = self.raw.replace(WRAPPERS[0], "<noinclude>\n;" + LABELS[0] + "\n</noinclude>")
        raw = raw.replace(WRAPPERS[1], "<noinclude>\r\n; \t" + LABELS[1] + "\t</noinclude>")
        self.assertEqual(partition(raw), (self.middle, self.tail))
        self.assertEqual(transclusion_input(raw), self.body)
        report = compare(raw, self.body, self.body, self.left, self.right, self.rendered)
        self.assertEqual(report["marker_shape"]["label_counts"], [1, 1])
        self.assertEqual([row["exact_block_matches"] for row in report["marker_shape"]["labels"]], [1, 1])

    def test_marker_shape_refuses_other_content_or_scope(self):
        for changed in (
            "<noinclude> ;" + LABELS[0] + " лишнее</noinclude>",
            "<noinclude> :" + LABELS[0] + "</noinclude>",
            "<noinclude><b>;" + LABELS[0] + "</b></noinclude>",
            "<noinclude><!-- ;" + LABELS[0] + " --></noinclude>",
            "; " + LABELS[0],
            "<noinclude> ;" + LABELS[0].replace("210-211", "210–211") + "</noinclude>",
        ):
            with self.subTest(changed=changed):
                with self.assertRaises(ValueError):
                    partition(self.raw.replace(WRAPPERS[0], changed))

    def test_reordered_markers_refused(self):
        raw = self.raw.replace(WRAPPERS[0], WRAPPERS[1], 1)
        pos = raw.rfind(WRAPPERS[1])
        raw = raw[:pos] + WRAPPERS[0] + raw[pos + len(WRAPPERS[1]):]
        with self.assertRaisesRegex(ValueError, "marker order drift"):
            partition(raw)

    def test_shape_refusal_does_not_emit_source(self):
        raw = self.raw.replace(WRAPPERS[0], "<noinclude> ;" + LABELS[0] + " секрет</noinclude>")
        with self.assertRaises(ValueError) as err:
            partition(raw)
        self.assertNotIn("секрет", str(err.exception))
        self.assertNotIn(self.middle, str(err.exception))
        shape = marker_shape(raw)
        self.assertEqual(shape["labels"][0]["suffix"]["other"], 6)
        self.assertEqual(shape["labels"][0]["exact_block_matches"], 0)

    def test_projection_loss_refused(self):
        with self.assertRaises(ValueError):
            compare(self.raw, self.body, self.body[:-1], self.left, self.right, self.rendered)

    def test_duplicate_rendered_passage_reported(self):
        r = compare(self.raw, self.body, self.body, self.left, self.right, self.rendered + " " + self.body)
        self.assertEqual(r["lanes"]["rendered"]["whole_page_matches"], 2)

    def test_rendered_intersections_distinguish_partial_paragraphs(self):
        # One raw line-break run can represent several actual HTML paragraphs.
        middle = "хвост слова.\nНовый абзац.\nНачало фразы, "
        tail = "которая продолжается."
        raw = WRAPPERS[0] + middle + WRAPPERS[1] + tail
        body = transclusion_input(raw)
        left, right = "Это пред", "Дальше."
        html = ('<div class="mw-parser-output"><p>Это предхвост слова.</p>'
                '<p>Новый абзац.</p><p>Начало фразы, которая продолжается. Дальше.</p></div>')
        view = CarrierView()
        view.feed(html)
        view.close()
        report = compare(raw, body, body, left, right, "".join(view.parts),
                         paragraph_spans=view.paragraph_spans())
        self.assertEqual(report["raw_blank_line_pieces"], 1)
        self.assertEqual(report["raw_lf_break_runs"], [1, 1])
        self.assertEqual(report["rendered_paragraphs"]["status"], "COVERED")
        self.assertEqual(report["rendered_paragraphs"]["intersected_count"], 3)
        self.assertEqual(report["rendered_paragraphs"]["complete_count"], 1)
        self.assertTrue(report["rendered_paragraphs"]["leading_partial"])
        self.assertTrue(report["rendered_paragraphs"]["trailing_partial"])
        self.assertEqual(report["current_render_edge_joins"]["left"]["selected"], "DIRECT")
        self.assertEqual(report["current_render_edge_joins"]["right"]["selected"], "SPACE")
        for lane in ("raw", "transclusion", "projected", "rendered"):
            self.assertEqual(report["lanes"][lane]["rendered_intersection_matches"], [1, 1, 1])
        for lane in ("transclusion", "projected", "rendered"):
            self.assertEqual(report["lanes"][lane]["whole_page_matches"], 1)
            self.assertEqual(report["lanes"][lane]["left_edge_matches"], 1)
            self.assertEqual(report["lanes"][lane]["right_edge_matches"], 1)
            self.assertEqual(report["lanes"][lane]["second_marker_continuation_matches"], 1)

    def test_rendered_paragraph_coverage_and_duplicate_refused(self):
        for tag, repetitions, expected in (
            ("div", 1, "INCOMPLETE_PARAGRAPH_COVERAGE"),
            ("p", 2, "SLICE_NOT_UNIQUE"),
        ):
            with self.subTest(tag=tag, repetitions=repetitions):
                view = CarrierView()
                html = '<div class="mw-parser-output">' + (
                    f"<{tag}>" + escape(self.body) + f"</{tag}>"
                ) * repetitions + "</div>"
                view.feed(html)
                view.close()
                report = compare(self.raw, self.body, self.body, self.left, self.right,
                                 "".join(view.parts), paragraph_spans=view.paragraph_spans())
                self.assertEqual(report["rendered_paragraphs"]["status"], expected)

    def test_ambiguous_edge_join_stays_unknown(self):
        rendered = self.rendered + " " + self.left + self.body
        report = compare(self.raw, self.body, self.body, self.left, self.right, rendered)
        self.assertIsNone(report["current_render_edge_joins"]["left"]["selected"])
        self.assertIsNone(report["lanes"]["rendered"]["left_edge_matches"])

    def test_pinned_left_hyphen_retained_only_carrier_omits(self):
        middle = "ложение продолжается.\n\nСледующая фраза, "
        tail = "которая закончилась."
        raw = WRAPPERS[0] + middle + WRAPPERS[1] + tail
        body = transclusion_input(raw)
        left = "Это пред-"
        left_raw = "<noinclude>header</noinclude>" + left + "<noinclude>footer</noinclude>"
        right = "Дальше."
        rendered = "Это пред" + body + " " + right
        report = compare(raw, body, body, left, right, rendered,
                         pinned_left_source=(left_raw, left))
        self.assertEqual(report["current_render_edge_joins"]["left"], {
            "matches": {"DIRECT": 0, "SPACE": 0, "HYPHEN_OMITTED_DIRECT": 1,
                        "HYPHEN_OMITTED_SPACE": 0}, "selected": "HYPHEN_OMITTED_DIRECT"})
        self.assertTrue(report["pinned_left_hyphen"]["projected_retained"])
        self.assertEqual(report["left_edge_comparison"], "SOURCE_LITERAL_CARRIER_OMISSION")
        for lane in ("transclusion", "projected", "rendered"):
            self.assertEqual(report["lanes"][lane]["left_edge_matches"], 1)
        self.assertEqual(transclusion_input(left_raw), left)
        self.assertNotIn(middle, str(report))
        self.assertIsNone(compare(raw, body, body, left, right, rendered)
                          ["current_render_edge_joins"]["left"]["selected"])

    def test_pinned_left_hyphen_refuses_wrong_scope_or_shape(self):
        middle = "ложение.\n\nНачало, "
        raw = WRAPPERS[0] + middle + WRAPPERS[1] + "которое завершилось."
        body = transclusion_input(raw)
        for left_raw, scoped, left in (
            ("Это пред-", "Это пред-", "Это пред-"),
            ("Это пред--<noinclude>footer</noinclude>", "Это пред--", "Это пред--"),
            ("Это пред<noinclude>-</noinclude>", "Это пред", "Это пред-"),
            ("Это пред-<noinclude>footer</noinclude>", "Это пред-", "Это пред"),
        ):
            with self.subTest(case=left_raw):
                with self.assertRaises(ValueError):
                    compare(raw, body, body, left, "Дальше.", "Это пред" + body,
                            pinned_left_source=(left_raw, scoped))

    def test_pinned_left_hyphen_wrong_separator_or_ambiguity(self):
        middle = "ложение продолжается, "
        raw = WRAPPERS[0] + middle + WRAPPERS[1] + "которое завершилось."
        body = transclusion_input(raw)
        left = "Это пред-"
        left_raw = left + "<noinclude>footer</noinclude>"
        right = "Дальше."
        good = "Это пред" + body + " " + right
        for carrier in ("Это пред " + body + " " + right,
                        good + " " + good,
                        good + " " + left + body,
                        good + " " + left + " " + body):
            report = compare(raw, body, body, left, right, carrier,
                             pinned_left_source=(left_raw, left))
            self.assertIsNone(report["current_render_edge_joins"]["left"]["selected"])
            self.assertIsNone(report["lanes"]["rendered"]["left_edge_matches"])

    def test_no_prose_in_report(self):
        r = compare(self.raw, self.body, self.body, self.left, self.right, self.rendered)
        self.assertNotIn(self.middle, str(r))
        self.assertNotIn(self.tail, str(r))


if __name__ == "__main__":
    unittest.main()
