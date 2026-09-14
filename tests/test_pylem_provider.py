import unittest
from pathlib import Path

from scriptorium.pylem_provider import (
    KNOWN_RUNTIME_POS,
    PYLEM_RUNTIME_PROFILE,
    PYLEM_VERSION,
    analyze_pos_with_holder,
    runtime_candidates_from_holder,
)


class _Analysis:
    def __init__(self, part_of_speech):
        self.part_of_speech = part_of_speech


class _Holder:
    def __init__(self, rows):
        self._rows = rows

    def lemmatize(self, word):
        return tuple(_Analysis(value) for value in self._rows.get(word, ()))


class PylemProviderUnitTests(unittest.TestCase):
    def test_candidate_order_and_ambiguity_are_preserved(self):
        holder = _Holder(
            {
                "Красный": ("A", "A"),
                "дом": ("N",),
                "спит": ("V", "A"),
            }
        )
        self.assertEqual(
            runtime_candidates_from_holder("Красный дом спит.", holder),
            (("A", "A"), ("N",), ("V", "A")),
        )

    def test_missing_analysis_remains_empty_and_therefore_undefined(self):
        holder = _Holder({"Красный": ("A",)})
        artifact = analyze_pos_with_holder("Красный неизвестный.", holder)
        self.assertEqual(artifact["runtime_profile"], PYLEM_RUNTIME_PROFILE)
        self.assertEqual(artifact["metrics"]["defined"]["count"], 1)
        self.assertEqual(artifact["metrics"]["undefined"]["count"], 1)

    def test_known_unresolved_codes_are_preserved_for_aggregator(self):
        holder = _Holder({"Дом": ("N",), "краток": ("ADJ_SHORT",)})
        artifact = analyze_pos_with_holder("Дом краток.", holder)
        self.assertEqual(artifact["metrics"]["defined"]["count"], 0)
        self.assertEqual(artifact["metrics"]["undefined"]["count"], 2)
        self.assertIn("N", KNOWN_RUNTIME_POS)
        self.assertIn("ADJ_SHORT", KNOWN_RUNTIME_POS)

    def test_unknown_or_blank_runtime_values_fail_closed(self):
        with self.assertRaisesRegex(RuntimeError, "unknown runtime POS"):
            runtime_candidates_from_holder("слово", _Holder({"слово": ("NEW_POS",)}))
        with self.assertRaisesRegex(RuntimeError, "blank/non-string"):
            runtime_candidates_from_holder("слово", _Holder({"слово": ("  ",)}))
        with self.assertRaisesRegex(RuntimeError, "blank/non-string"):
            runtime_candidates_from_holder("слово", _Holder({"слово": (None,)}))

    def test_hash_pinned_requirement_and_hosted_workflow_contract(self):
        root = Path(__file__).resolve().parents[1]
        requirement = (root / "requirements/pylem-0.0.18.txt").read_text(encoding="utf-8")
        workflow = (root / ".github/workflows/morphology-provider.yml").read_text(
            encoding="utf-8"
        )
        probe = (root / "tools/pylem_runtime_probe.py").read_text(encoding="utf-8")

        self.assertEqual(PYLEM_VERSION, "0.0.18")
        self.assertEqual(PYLEM_RUNTIME_PROFILE, "pylem-0.0.18-python39-sidecar-v1")
        self.assertIn("pylem==0.0.18", requirement)
        self.assertIn(
            "sha256:66c0d13414006a803f200979540fcee9653738701c14496a418db67542b26515",
            requirement,
        )
        self.assertIn("permissions:\n  contents: read", workflow)
        self.assertIn("ref: ${{ github.event.pull_request.head.sha || github.sha }}", workflow)
        self.assertIn('python-version: "3.13"', workflow)
        self.assertIn('python-version: "3.9"', workflow)
        self.assertIn("--no-deps --require-hashes", workflow)
        self.assertIn("python -m unittest discover -s tests -v", workflow)
        self.assertIn("python tools/pylem_runtime_probe.py", workflow)
        self.assertIn("build/morph/pylem-runtime-receipt.json", workflow)
        self.assertNotIn("secrets.", workflow)
        self.assertNotIn("scriptorium", probe)
        self.assertIn('"source_text_included": False', probe)
        self.assertNotIn("TOKENS,", probe)


if __name__ == "__main__":
    unittest.main()
