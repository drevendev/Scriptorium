"""Synthetic missing-folio marker and preservation checks."""
import unittest

from scriptorium.robinson_trusov_missing_folios import compare, partition, WRAPPERS
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

    def test_projection_loss_refused(self):
        with self.assertRaises(ValueError):
            compare(self.raw, self.body, self.body[:-1], self.left, self.right, self.rendered)

    def test_duplicate_rendered_passage_reported(self):
        r = compare(self.raw, self.body, self.body, self.left, self.right, self.rendered + " " + self.body)
        self.assertEqual(r["lanes"]["rendered"]["whole_page_matches"], 2)

    def test_no_prose_in_report(self):
        r = compare(self.raw, self.body, self.body, self.left, self.right, self.rendered)
        self.assertNotIn(self.middle, str(r))
        self.assertNotIn(self.tail, str(r))


if __name__ == "__main__":
    unittest.main()
