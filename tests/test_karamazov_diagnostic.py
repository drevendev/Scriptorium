"""Pinned Karamazov field diagnostics: scientific boundaries and drift rejection."""
from __future__ import annotations

from copy import deepcopy
from contextlib import ExitStack
from hashlib import sha256
import json
from pathlib import Path
import tempfile
import unittest
from unittest.mock import Mock, patch

from scriptorium import karamazov_diagnostic as diag
from scriptorium import karamazov_freeze as freeze


def synthetic_sources():
    records = {}
    for row in freeze.expected_segments():
        if row["kind"] == "front_matter":
            text = """{{Отексте
|АВТОР=[[Фёдор Михайлович Достоевский]]
|ИСТОЧНИК={{книга|заглавие=Собрание сочинений}}
}}__NOEDITSECTION__
{{right|''Посвящается Анне Григорьевне Достоевской''}}
{{эпиграф2|Строка эпиграфа.|Источник эпиграфа|60}}
== Оглавление ==
* [[Навигационная ссылка]]
"""
            revision_id = freeze.SOURCE_WORK_INDEX_REVISION_ID
        elif row["kind"] == "author_preface":
            text = (
                "{{Отексте|АВТОР=[[Фёдор Михайлович Достоевский]]}}\n"
                "== От автора ==\n<onlyinclude>"
                + ("Слово повести. " * 700)
                + "</onlyinclude>\n[[Категория:Братья Карамазовы (Достоевский)]]"
            )
            revision_id = 8_000_000 + row["ordinal"]
        else:
            text = (
                "{{Отексте|АВТОР=[[Фёдор Михайлович Достоевский]]}}"
                "__NOTOC____NOEDITSECTION__\n<center>''Заголовок''</center>\n"
                + "== Глава ==\n<div class='indent' style='text-align:justify'>"
                + ("Слово повести. " * 700)
                + "</div>"
            )
            revision_id = 8_000_000 + row["ordinal"]
        records[row["title"]] = {
            "revision_id": revision_id,
            "timestamp": "2026-01-01T00:00:00Z",
            "mediawiki_sha1": sha256(str(row["ordinal"]).encode()).hexdigest()[:40],
            "wikitext": text,
        }
    return records


class KaramazovDiagnosticTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.records = synthetic_sources()
        cls.manifest = freeze.build_manifest(fetcher=lambda rows: cls.records)
        cls.replayed = {title: row["wikitext"] for title, row in cls.records.items()}

    def fixture(self, manifest=None, sources=None):
        with ExitStack() as stack:
            body = self.manifest["composite_identity"]
            stack.enter_context(patch.object(
                diag, "FROZEN_BODY_CHARACTERS", body["character_count_including_spaces"]
            ))
            stack.enter_context(patch.object(
                diag, "FROZEN_BODY_SHA256", body["raw_sha256"]
            ))
            return diag.build_diagnostic(
                manifest if manifest is not None else self.manifest,
                fetcher=lambda _: sources if sources is not None else self.replayed,
            )

    def test_retained_manifest_pins_and_fantlab_references(self):
        root = Path(__file__).resolve().parents[1]
        source = json.loads((root / (
            "corpus/candidates/source-edition-traces/"
            "dostoevsky-brothers-karamazov-ru.revisions.json"
        )).read_text(encoding="utf-8"))
        identity = source["composite_identity"]
        self.assertEqual(identity["raw_sha256"], diag.FROZEN_BODY_SHA256)
        self.assertEqual(identity["normalized_sha256"], diag.FROZEN_BODY_SHA256)
        self.assertEqual(identity["character_count_including_spaces"], diag.FROZEN_BODY_CHARACTERS)
        self.assertEqual(diag.FANTLAB_REFERENCES, {
            "fantlab.general.characters": "1807107",
            "fantlab.general.words": "281507",
        })
        self.assertEqual(diag.FANTLAB_DATE, "2022-09-18")

    def test_real_metrics_with_nulls_and_no_source_prose(self):
        artifact = self.fixture()
        rows = {row["metric_id"]: row for row in artifact["metric_rows"]}
        self.assertEqual(len(rows), 29)
        self.assertGreaterEqual(sum(row["actual"] is not None for row in rows.values()), 21)
        self.assertLessEqual(sum(row["actual"] is not None for row in rows.values()), 24)
        self.assertEqual(
            rows["fantlab.general.characters"]["actual"],
            self.manifest["composite_identity"]["character_count_including_spaces"]
        )
        self.assertEqual(
            rows["fantlab.general.characters"]["result"], "DIAGNOSTIC_SOURCE_UNMATCHED"
        )
        self.assertEqual(
            rows["fantlab.general.characters"]["actual_minus_fantlab_display"],
            self.manifest["composite_identity"]["character_count_including_spaces"] - 1807107
        )
        self.assertIsNone(rows["fantlab.dialogue.share_percent"]["fantlab_display"])
        self.assertEqual(
            rows["fantlab.vocabulary.uasz_10000"]["result"], "NOT_RUN_DICTIONARY_UNBOUND"
        )
        self.assertIsNone(rows["fantlab.vocabulary.uasz_10000"]["actual"])
        self.assertFalse(artifact["gates"]["m2_parity_admissible"])
        self.assertEqual(artifact["gates"]["m2_weight"], 0)
        self.assertEqual(artifact["gates"]["fantlab_source_edition_match"], "unknown")
        self.assertIs(artifact["source_text_committed"], False)
        payload = diag.render_json(artifact)
        self.assertNotIn("Слово повести", payload)
        self.assertNotIn("wikitext", payload.lower())
        self.assertEqual(payload, diag.render_json(deepcopy(artifact)))
        self.assertEqual(json.loads(payload), artifact)

    def test_manifest_tamper_fails_before_fetching_sources(self):
        tampered = deepcopy(self.manifest)
        tampered["composite_identity"]["raw_sha256"] = "0" * 64
        fetcher = Mock()
        with patch.object(
            diag, "FROZEN_BODY_CHARACTERS",
            self.manifest["composite_identity"]["character_count_including_spaces"],
        ):
            with self.assertRaisesRegex(ValueError, "canonical frozen pins"):
                diag.build_diagnostic(tampered, fetcher=fetcher)
        fetcher.assert_not_called()

    def test_unexpected_source_inventory_rejected_before_metrics(self):
        subset = dict(list(self.replayed.items())[:-1])
        with patch.object(diag, "analyze_deterministic_metrics") as analyzer:
            with self.assertRaisesRegex(ValueError, "source inventory mismatch"):
                self.fixture(sources=subset)
            analyzer.assert_not_called()

    def test_source_drift_rejected_before_metrics(self):
        changed = dict(self.replayed)
        title = freeze.expected_segments()[5]["title"]
        changed[title] = changed[title].replace("Слово повести", "Новая повесть", 1)
        with patch.object(diag, "analyze_deterministic_metrics") as analyzer:
            with self.assertRaisesRegex(ValueError, "frozen composite identity drift"):
                self.fixture(sources=changed)
            analyzer.assert_not_called()

    def test_create_only_deterministic_receipt(self):
        data = {"candidate_id": freeze.CANDIDATE_ID, "source_text_committed": False}
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "fields.json"
            diag.write_new(path, data)
            original = path.read_bytes()
            with self.assertRaises(FileExistsError):
                diag.write_new(path, data)
            self.assertEqual(path.read_bytes(), original)


if __name__ == "__main__":
    unittest.main()
