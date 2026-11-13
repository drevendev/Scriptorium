"""Original-coordinate provenance is opt-in and cannot alter text-v1 spans."""
import unittest

from scriptorium.source_spans import normalize_with_provenance, OriginalSpan, PROVENANCE_PROFILE
from scriptorium.text import normalize_text, word_tokens, sentence_spans


class SourceProvenanceTests(unittest.TestCase):
    def test_requested_newline_and_composition_example(self):
        raw = "A\r\ne\u0301"
        result = normalize_with_provenance(raw)
        self.assertEqual(result.profile, PROVENANCE_PROFILE)
        self.assertEqual(result.normalized, "A\né")
        self.assertEqual(result.normalized, normalize_text(raw))
        self.assertEqual(result.original_span(0, 1), OriginalSpan(0, 1, True))
        self.assertEqual(result.original_span(1, 2), OriginalSpan(1, 3, True))
        self.assertEqual(result.original_span(2, 3), OriginalSpan(3, 5, True))
        self.assertEqual(result.original_span(0, 3), OriginalSpan(0, 5, True))

    def test_empty_and_preserved_text(self):
        empty = normalize_with_provenance("")
        self.assertEqual(empty.source_ranges, ())
        self.assertEqual(empty.safe_boundaries, (True,))
        with self.assertRaises(ValueError):
            empty.original_span(0, 0)
        raw = "  Ёж!\t\n"
        value = normalize_with_provenance(raw)
        self.assertEqual(value.normalized, raw)
        self.assertEqual(value.source_ranges, tuple((i, i+1) for i in range(len(raw))))
        self.assertEqual(value.original_span(2, 4), OriginalSpan(2, 4, True))

    def test_crlf_cr_and_lf_boundaries(self):
        raw = "x\r\ny\rz\n"
        value = normalize_with_provenance(raw)
        self.assertEqual(value.normalized, "x\ny\nz\n")
        self.assertEqual(value.original_span(1, 2), OriginalSpan(1, 3, True))
        self.assertEqual(value.original_span(3, 4), OriginalSpan(4, 5, True))
        self.assertEqual(value.original_span(5, 6), OriginalSpan(6, 7, True))

    def test_canonical_reordering_is_ambiguous_inside_but_exact_as_whole(self):
        raw = "a\u0315\u0300"
        value = normalize_with_provenance(raw)
        self.assertEqual(value.normalized, "à\u0315")
        self.assertEqual(value.original_span(0, 1), OriginalSpan(0, 3, False))
        self.assertEqual(value.original_span(1, 2), OriginalSpan(1, 2, False))
        self.assertEqual(value.original_span(0, 2), OriginalSpan(0, 3, True))

    def test_hangul_jamo_composition(self):
        raw = "\u1100\u1161\u11A8"
        value = normalize_with_provenance(raw)
        self.assertEqual(value.normalized, "각")
        self.assertEqual(value.original_span(0, 1), OriginalSpan(0, 3, True))
        self.assertEqual(normalize_with_provenance("각").original_span(0, 1), OriginalSpan(0, 1, True))

    def test_reordered_accent_from_existing_composition(self):
        raw = "é\u0323"
        value = normalize_with_provenance(raw)
        self.assertEqual(value.normalized, "ẹ\u0301")
        self.assertFalse(value.original_span(0, 1).exact)
        self.assertFalse(value.original_span(1, 2).exact)
        self.assertTrue(value.original_span(0, 2).exact)

    def test_refuse_false_offsets_and_non_string_source(self):
        with self.assertRaises(TypeError):
            normalize_with_provenance(b"raw")
        result = normalize_with_provenance("A\r\ne\u0301")
        for start, end in ((-1, 1), (1, 1), (2, 1), (0, 4), (True, 1), (0, 1.0)):
            with self.subTest(start=start, end=end), self.assertRaises(ValueError):
                result.original_span(start, end)

    def test_real_token_and_sentence_consumer_preserves_normalized_offsets(self):
        raw = "A\r\ne\u0301."
        provenance = normalize_with_provenance(raw)
        words = word_tokens(raw)
        self.assertEqual([(w.text, w.start, w.end) for w in words],
                         [("A", 0, 1), ("é", 2, 3)])
        self.assertEqual([(provenance.original_span(w.start, w.end).start,
                           provenance.original_span(w.start, w.end).end)
                          for w in words], [(0, 1), (3, 5)])
        sentences = sentence_spans(raw)
        self.assertEqual([(s.text, s.start, s.end) for s in sentences],
                         [("A\né.", 0, 4)])
        self.assertEqual(provenance.original_span(0, 4), OriginalSpan(0, 6, True))

    def test_tricky_canonical_composition_is_not_misclassified_as_exact(self):
        raw = "Å\u1100\r\u0334Å\u1100\u0334X\u1161\u0323ç\u0315çç\u0301\u0302\u0308\u0345\u0327\u0323"
        result = normalize_with_provenance(raw)
        self.assertEqual(result.normalized, normalize_text(raw))
        self.assertEqual(result.original_span(0, len(result.normalized)),
                         OriginalSpan(0, len(raw), True))
        for i in range(len(result.normalized)):
            mapped = result.original_span(i, i + 1)
            if mapped.exact:
                self.assertEqual(normalize_text(raw[mapped.start:mapped.end]),
                                 result.normalized[i:i+1])

    def test_determinism(self):
        raw = "А\r\nе\u0301!\r\u1100\u1161"
        self.assertEqual(normalize_with_provenance(raw), normalize_with_provenance(raw))


if __name__ == "__main__":
    unittest.main()
