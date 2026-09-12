from hashlib import sha256
import json
from pathlib import Path
import tempfile
import unittest

from scriptorium.benchmark import build_comparison, main


REFERENCE = '''{
  "benchmark_id": "test-work-1",
  "reference": {
    "site": "FantLab",
    "url": "https://fantlab.ru/work1/lp",
    "analysis_date": "2022-09-19",
    "work_id": 1,
    "title": "Test",
    "author": "Author"
  },
  "expected": {
    "characters": 10,
    "words": 2,
    "mean_word_length_characters": 3.50,
    "mean_sentence_length_characters": 10.00,
    "punctuation_per_1000_words": {
      "comma": 500.00,
      "question": 10.30,
      "period": 500.00
    }
  }
}'''


class BenchmarkComparisonTests(unittest.TestCase):
    def test_exact_integer_match_passes_only_with_admissible_provenance(self):
        artifact = build_comparison(
            REFERENCE,
            "Кот, спит.".encode("utf-8"),
            scriptorium_revision="abc123",
            edition_match="exact",
            edition_label="exact test edition",
            source_reference="local:test",
            legal_basis="public_domain",
        )

        characters = artifact["metrics"]["fantlab.general.characters"]
        words = artifact["metrics"]["fantlab.general.words"]
        self.assertEqual(characters["comparison"]["result"], "pass")
        self.assertTrue(characters["comparison"]["numeric_match"])
        self.assertEqual(characters["comparison"]["raw_delta"], 0)
        self.assertEqual(words["comparison"]["result"], "pass")

    def test_integer_match_is_unresolved_without_exact_provenance(self):
        artifact = build_comparison(
            REFERENCE,
            "Кот, спит.".encode("utf-8"),
            scriptorium_revision="abc123",
            edition_match="unknown",
        )

        row = artifact["metrics"]["fantlab.general.characters"]
        self.assertTrue(row["comparison"]["numeric_match"])
        self.assertEqual(row["comparison"]["result"], "unresolved")
        self.assertIn("provenance", row["comparison"]["reason"])

    def test_exact_match_is_unresolved_without_edition_label(self):
        artifact = build_comparison(
            REFERENCE,
            "Кот, спит.".encode("utf-8"),
            scriptorium_revision="abc123",
            edition_match="exact",
            source_reference="local:test",
            legal_basis="public_domain",
        )

        row = artifact["metrics"]["fantlab.general.characters"]
        self.assertTrue(row["comparison"]["numeric_match"])
        self.assertEqual(row["comparison"]["result"], "unresolved")

    def test_exact_match_is_unresolved_without_source_reference(self):
        artifact = build_comparison(
            REFERENCE,
            "Кот, спит.".encode("utf-8"),
            scriptorium_revision="abc123",
            edition_match="exact",
            edition_label="exact test edition",
            legal_basis="public_domain",
        )

        row = artifact["metrics"]["fantlab.general.characters"]
        self.assertTrue(row["comparison"]["numeric_match"])
        self.assertEqual(row["comparison"]["result"], "unresolved")

    def test_integer_mismatch_fails_when_provenance_is_admissible(self):
        reference = REFERENCE.replace('"characters": 10', '"characters": 11')
        artifact = build_comparison(
            reference,
            "Кот, спит.".encode("utf-8"),
            scriptorium_revision="abc123",
            edition_match="exact",
            edition_label="exact test edition",
            source_reference="local:test",
            legal_basis="public_domain",
        )

        row = artifact["metrics"]["fantlab.general.characters"]
        self.assertFalse(row["comparison"]["numeric_match"])
        self.assertEqual(row["comparison"]["raw_delta"], -1)
        self.assertEqual(row["comparison"]["result"], "fail")

    def test_decimal_precision_remains_unresolved_and_lexeme_is_preserved(self):
        artifact = build_comparison(
            REFERENCE,
            "Кот, спит.".encode("utf-8"),
            scriptorium_revision="abc123",
            edition_match="exact",
            edition_label="exact test edition",
            source_reference="local:test",
            legal_basis="public_domain",
        )

        question = artifact["metrics"]["fantlab.punctuation.question.per_1000_words"]
        self.assertEqual(question["expected"]["display_text"], "10.30")
        self.assertIsNone(question["expected"]["display_places"])
        self.assertIsNone(question["comparison"]["numeric_match"])
        self.assertEqual(question["comparison"]["rule"], "unresolved_precision")
        self.assertEqual(question["comparison"]["result"], "unresolved")

    def test_source_hashes_bind_raw_bytes_and_normalized_text(self):
        source = "е\u0308\r\nТест.".encode("utf-8")
        reference = REFERENCE.replace('"characters": 10', '"characters": 7')
        artifact = build_comparison(
            reference,
            source,
            scriptorium_revision="abc123",
        )

        self.assertEqual(artifact["source_text"]["raw_sha256"], sha256(source).hexdigest())
        self.assertEqual(
            artifact["source_text"]["normalized_sha256"],
            "852e7a3dce82ea35581c89365ace4ea9e3dd22d754dd37f127c37de62392c349",
        )
        self.assertNotEqual(
            artifact["source_text"]["raw_sha256"],
            artifact["source_text"]["normalized_sha256"],
        )

    def test_unique_vocabulary_can_compare_without_dictionary_dependency(self):
        reference = json.loads(REFERENCE)
        reference["expected"]["unique_words"] = 2
        artifact = build_comparison(
            json.dumps(reference, ensure_ascii=False),
            "Кот, кот. Пёс!".encode("utf-8"),
            scriptorium_revision="abc123",
            edition_match="exact",
            edition_label="exact test edition",
            source_reference="local:test",
            legal_basis="public_domain",
        )

        row = artifact["metrics"]["fantlab.vocabulary.unique_words"]
        self.assertEqual(row["actual"]["raw_value"], 2)
        self.assertEqual(row["comparison"]["result"], "pass")
        self.assertIsNone(artifact["analyzer"]["dictionary_version"])

    def test_dictionary_counts_are_not_run_without_dictionary_dependency(self):
        reference = json.loads(REFERENCE)
        reference["expected"]["active_dictionary_vocabulary"] = 2
        reference["expected"]["active_non_dictionary_vocabulary"] = 0
        reference["expected"]["uasz_3000"] = 2.0
        artifact = build_comparison(
            json.dumps(reference, ensure_ascii=False),
            "Кот Пёс".encode("utf-8"),
            scriptorium_revision="abc123",
            edition_match="exact",
            edition_label="exact test edition",
            source_reference="local:test",
            legal_basis="public_domain",
        )

        active = artifact["metrics"]["fantlab.vocabulary.active_dictionary"]
        uasz = artifact["metrics"]["fantlab.vocabulary.uasz_3000"]
        self.assertIsNone(active["actual"]["raw_value"])
        self.assertEqual(active["comparison"]["result"], "not_run")
        self.assertIsNone(uasz["actual"]["raw_value"])
        self.assertEqual(uasz["comparison"]["result"], "unresolved")
        self.assertIn("no numeric value", uasz["comparison"]["reason"])

    def test_supplied_dictionary_is_reproducible_but_not_fantlab_admissible(self):
        reference = json.loads(REFERENCE)
        reference["expected"]["active_dictionary_vocabulary"] = 2
        reference["expected"]["active_non_dictionary_vocabulary"] = 1
        artifact = build_comparison(
            json.dumps(reference, ensure_ascii=False),
            "Кот кот Пёс дракон".encode("utf-8"),
            scriptorium_revision="abc123",
            edition_match="exact",
            edition_label="exact test edition",
            source_reference="local:test",
            legal_basis="public_domain",
            dictionary_words=["кот", "пёс"],
            dictionary_profile="test-dictionary-v1",
        )

        active = artifact["metrics"]["fantlab.vocabulary.active_dictionary"]
        nondictionary = artifact["metrics"]["fantlab.vocabulary.active_nondictionary"]
        self.assertEqual(active["actual"]["raw_value"], 2)
        self.assertEqual(nondictionary["actual"]["raw_value"], 1)
        self.assertEqual(active["comparison"]["result"], "unresolved")
        self.assertTrue(active["comparison"]["numeric_match"])
        self.assertIn("dictionary identity/version", active["comparison"]["reason"])
        self.assertRegex(
            artifact["analyzer"]["dictionary_version"],
            r"^test-dictionary-v1@sha256:[0-9a-f]{64}$",
        )

    def test_cli_writes_machine_readable_artifact(self):
        with tempfile.TemporaryDirectory() as tmp:
            directory = Path(tmp)
            reference_path = directory / "reference.json"
            text_path = directory / "text.txt"
            output_path = directory / "comparison.json"
            reference_path.write_text(REFERENCE, encoding="utf-8")
            text_path.write_text("Кот, спит.", encoding="utf-8")

            code = main(
                [
                    "--reference",
                    str(reference_path),
                    "--text",
                    str(text_path),
                    "--scriptorium-revision",
                    "abc123",
                    "--edition-match",
                    "exact",
                    "--edition-label",
                    "exact test edition",
                    "--source-reference",
                    "local:test",
                    "--legal-basis",
                    "public_domain",
                    "--output",
                    str(output_path),
                ]
            )

            self.assertEqual(code, 0)
            artifact = json.loads(output_path.read_text(encoding="utf-8"))
            self.assertEqual(artifact["schema_version"], "fantlab-benchmark-comparison-v1")
            self.assertEqual(artifact["metric_contract_id"], "fantlab-2022-v1")
            self.assertEqual(artifact["analyzer"]["scriptorium_revision"], "abc123")
            self.assertIn("fantlab.general.characters", artifact["metrics"])

    def test_reference_without_implemented_fields_is_rejected(self):
        reference = json.loads(REFERENCE)
        reference["expected"] = {"approx_pages": 1}
        with self.assertRaisesRegex(ValueError, "no currently implemented"):
            build_comparison(
                json.dumps(reference),
                b"text",
                scriptorium_revision="abc123",
            )


if __name__ == "__main__":
    unittest.main()
