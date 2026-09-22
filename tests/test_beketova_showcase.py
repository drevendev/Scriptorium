from __future__ import annotations

from copy import deepcopy
import json
from pathlib import Path
import unittest

from scriptorium.beketova_showcase import SHOWCASE_METRICS, SHOWCASE_VERSION, build_showcase


ROOT = Path(__file__).resolve().parents[1]
REVISION_MANIFEST = ROOT / "corpus/candidates/source-edition-traces/verne-children-captain-grant-beketova-ru.revision.json"
BODY_MANIFEST = ROOT / "corpus/candidates/source-edition-traces/verne-children-captain-grant-beketova-ru.body.json"


class BeketovaShowcaseTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.revision = json.loads(REVISION_MANIFEST.read_text(encoding="utf-8"))
        cls.body = json.loads(BODY_MANIFEST.read_text(encoding="utf-8"))
        cls.fixture = (
            "Глава первая. Это длинная строка повествования с несколькими словами.\n\n"
            "— Добрый день! — сказал путешественник. — Куда мы идём?\n\n"
            "Ответ последовал сразу, и путь продолжился. " * 2500
        )

    def test_builds_source_free_showcase_with_closed_parity_gate(self) -> None:
        artifact = build_showcase(
            self.revision,
            self.body,
            body_loader=lambda _: self.fixture,
            enforce_canonical_body=False,
        )
        self.assertEqual(SHOWCASE_VERSION, artifact["showcase_version"])
        self.assertFalse(artifact["source_text_committed"])
        self.assertEqual(len(SHOWCASE_METRICS), len(artifact["metrics"]))
        self.assertTrue(artifact["gates"]["showcase_ready"])
        self.assertEqual("unknown", artifact["gates"]["fantlab_source_edition_match"])
        self.assertFalse(artifact["gates"]["gate_ready"])
        self.assertFalse(artifact["gates"]["m2_parity_admissible"])
        self.assertEqual(0, artifact["gates"]["m2_weight"])
        self.assertFalse(artifact["interpretation"]["fantlab_comparison_performed"])

    def test_serialization_contains_no_fixture_prose(self) -> None:
        artifact = build_showcase(
            self.revision,
            self.body,
            body_loader=lambda _: self.fixture,
            enforce_canonical_body=False,
        )
        serialized = json.dumps(artifact, ensure_ascii=False).lower()
        for leaked in ("путешественник", "куда мы идём", "wikitext", "literary_text", "source_prose"):
            self.assertNotIn(leaked, serialized)

    def test_body_manifest_drift_fails_closed(self) -> None:
        corrupted = deepcopy(self.body)
        corrupted["literary_body_identity"]["raw_sha256"] = "not-a-sha256"
        with self.assertRaisesRegex(ValueError, "raw_sha256"):
            build_showcase(
                self.revision,
                corrupted,
                body_loader=lambda _: self.fixture,
                enforce_canonical_body=False,
            )

    def test_canonical_guard_rejects_fixture_body(self) -> None:
        with self.assertRaisesRegex(ValueError, "frozen Beketova body identity drift"):
            build_showcase(self.revision, self.body, body_loader=lambda _: self.fixture)


if __name__ == "__main__":
    unittest.main()
