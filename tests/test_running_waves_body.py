from __future__ import annotations

import copy
import json
from pathlib import Path
import unittest

from scriptorium.running_waves_body import (
    MINIMUM_CORPUS_CHARACTERS,
    build_manifest,
    expand_running_waves_templates,
    replay_manifest,
    source_manifest_sha256,
    validate_manifest,
)


ROOT = Path(__file__).resolve().parents[1]
SOURCE_MANIFEST_PATH = (
    ROOT
    / "corpus"
    / "candidates"
    / "source-edition-traces"
    / "grin-running-on-waves-ru.source-revisions.json"
)


def load_source_manifest() -> dict[str, object]:
    value = json.loads(SOURCE_MANIFEST_PATH.read_text(encoding="utf-8"))
    assert isinstance(value, dict)
    return value


def synthetic_fetcher(identities):
    rows = tuple(identities)
    records: dict[str, str] = {}
    for row in rows:
        ordinal = int(row["ordinal"])
        # Deliberately large enough that 36 pages clear the >=300k corpus gate.
        paragraph = (f"Страница {ordinal}. Литературный текст для проверки. " * 220).strip()
        records[str(row["title"])] = f'<div class="text">{paragraph}</div>'
    return records


class RunningWavesBodyTests(unittest.TestCase):
    def test_source_manifest_digest_is_canonical_and_stable(self) -> None:
        source = load_source_manifest()
        digest = source_manifest_sha256(source)
        self.assertEqual(len(digest), 64)
        self.assertEqual(digest, source_manifest_sha256(copy.deepcopy(source)))

    def test_candidate_template_renderer_matches_frozen_observed_shapes(self) -> None:
        source = (
            '<div class="text">{{roman|24}}{{^}} '
            '{{poem1||<poem>Строка первая.\nСтрока вторая.</poem>|}} '
            '{{razr|Разрядка}} {{razr2|Ещё}} '
            'ударе{{акут}}ние грави{{Гравис}}с '
            '{{опечатка2|ошипка|ошибка}} '
            '{{Так в тексте|исходное}} '
            '{{Так в тексте|слово{{акут}}|подсказка}}</div>'
        )
        rendered = expand_running_waves_templates(source)
        self.assertIn("XXIV", rendered)
        self.assertNotIn("{{^}}", rendered)
        self.assertIn("Строка первая.\nСтрока вторая.", rendered)
        self.assertNotIn("<poem>", rendered.lower())
        self.assertIn("Разрядка", rendered)
        self.assertIn("ударе\u0301ние", rendered)
        self.assertIn("грави\u0300с", rendered)
        self.assertIn("ошибка", rendered)
        self.assertNotIn("ошипка", rendered)
        self.assertIn("слово\u0301", rendered)
        self.assertNotIn("подсказка", rendered)
        self.assertNotIn("{{", rendered)

    def test_candidate_template_renderer_rejects_unobserved_shapes(self) -> None:
        unsupported = (
            '<div class="text">'
            '{{roman|IV}} {{^|2em}} {{poem1|Заголовок|Текст|}} '
            '{{опечатка2|a|b|comment}} {{Так в тексте|a|b|c}}'
            '</div>'
        )
        rendered = expand_running_waves_templates(unsupported)
        self.assertIn("{{roman|IV}}", rendered)
        self.assertIn("{{^|2em}}", rendered)
        self.assertIn("{{poem1|Заголовок|Текст|}}", rendered)
        self.assertIn("{{опечатка2|a|b|comment}}", rendered)
        self.assertIn("{{Так в тексте|a|b|c}}", rendered)

    def test_build_manifest_is_source_free_and_replayable(self) -> None:
        source = load_source_manifest()
        manifest = build_manifest(source, fetcher=synthetic_fetcher)
        identities = validate_manifest(manifest, source)

        self.assertEqual(len(identities), 36)
        self.assertEqual(len(manifest["per_page_identities"]), 36)
        self.assertGreaterEqual(
            manifest["composite_identity"]["character_count_including_spaces"],
            MINIMUM_CORPUS_CHARACTERS,
        )
        self.assertTrue(manifest["corpus_admission"]["character_threshold_met"])
        self.assertFalse(manifest["corpus_admission"]["m2_parity_admissible"])

        serialized = json.dumps(manifest, ensure_ascii=False)
        self.assertNotIn("Литературный текст для проверки", serialized)
        self.assertNotIn("wikitext", serialized.lower())

        receipt = replay_manifest(manifest, source, fetcher=synthetic_fetcher)
        self.assertTrue(receipt["verified"])
        self.assertEqual(receipt["verified_literary_page_count"], 36)
        self.assertFalse(receipt["m2_parity_admissible"])

    def test_extraction_fails_closed_on_unsupported_template(self) -> None:
        source = load_source_manifest()

        def broken_fetcher(identities):
            records = synthetic_fetcher(identities)
            first = str(next(iter(identities))["title"])
            records[first] = '<div class="text">До {{неподдерживаемый|шаблон}} после.</div>'
            return records

        with self.assertRaisesRegex(ValueError, "failed to extract literary body"):
            build_manifest(source, fetcher=broken_fetcher)

    def test_extraction_fails_closed_on_supported_name_with_unobserved_shape(self) -> None:
        source = load_source_manifest()

        def broken_fetcher(identities):
            records = synthetic_fetcher(identities)
            first = str(next(iter(identities))["title"])
            records[first] = '<div class="text">{{poem1|Новый заголовок|Текст|}}</div>'
            return records

        with self.assertRaisesRegex(ValueError, "failed to extract literary body"):
            build_manifest(source, fetcher=broken_fetcher)

    def test_replay_rejects_derived_identity_drift(self) -> None:
        source = load_source_manifest()
        manifest = build_manifest(source, fetcher=synthetic_fetcher)
        tampered = copy.deepcopy(manifest)
        tampered["per_page_identities"][0]["character_count_including_spaces"] += 1

        with self.assertRaisesRegex(ValueError, "frozen literary-page identity drift"):
            replay_manifest(tampered, source, fetcher=synthetic_fetcher)

    def test_validation_rejects_source_manifest_binding_drift(self) -> None:
        source = load_source_manifest()
        manifest = build_manifest(source, fetcher=synthetic_fetcher)
        changed_source = copy.deepcopy(source)
        changed_source["bibliographic_source"] = "unexpected"

        with self.assertRaises(ValueError):
            validate_manifest(manifest, changed_source)


if __name__ == "__main__":
    unittest.main()
