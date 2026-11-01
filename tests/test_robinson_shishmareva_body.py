"""Offline positive/negative tests for a source-free, fail-closed translation body."""

import json
from pathlib import Path
import unittest

from scriptorium.robinson_shishmareva_body import (
    CANDIDATE_ID, SCHEMA, build_manifest,
    extract_literary_body, replay_manifest, _check_inventory,
)


def sample(story="Я родился в 1632 году.\n\nВторой абзац."):
    return (
        "{{Отексте|ПЕРЕВОДЧИК=Мария Андреевна Шишмарёва|ИСТОЧНИК="
        "{{книга|издательство=ACADEMIA|год=1935}}}}\n"
        "{{эпиграф||Подзаголовок моряка из Йорка.}}\n\n"
        f"{story}\n"
        "<blockquote>{{h3|Дневник|caps=1}}\nСтрока дневника.</blockquote>\n"
        "{{Razr2|Пятница}}. Да.\n"
        "В тексте<ref>Редакторское примечание, не роман.</ref> конец.\n"
        "{{примечания|title=}}\n"
        + "\n".join(f"[[Категория:Тест {n}]]" for n in range(5))
    )


class ShishmarevaTests(unittest.TestCase):
    def test_extract_preserves_narrative_subtitle_dialogue_and_diary(self):
        text = extract_literary_body(sample("А" * 300_010))
        self.assertGreater(len(text), 300_000)
        for part in ("Подзаголовок моряка", "А" * 100, "Дневник", "Пятница", "Строка дневника"):
            self.assertIn(part, text)
        for artifact in ("Отексте", "ACADEMIA", "Категория:", "примечания", "Редакторское примечание", "<blockquote>", "<ref>", "{{"):
            self.assertNotIn(artifact, text)

    def test_rejects_metadata_trailing_notes_or_page_transclusion_drift(self):
        base = sample("Б" * 300_100)
        for changed in (
            base.replace("{{Отексте", "{{Другое", 1),
            base.replace("Шишмарёва", "Журавская", 1),
            base.replace("{{эпиграф", "{{Другое", 1),
            base.replace("{{примечания|title=}}", "", 1),
            base.replace("[[Категория:Тест 4]]", "[[Категория:Тест 4]]НЕОЖИДАННО", 1),
            base.replace("<blockquote>", "", 1),
            base.replace("{{Razr2|Пятница}}", "{{Unfamiliar|Пятница}}", 1),
            base.replace("В тексте", "<pages index='unfrozen' />В тексте", 1),
            base.replace("<ref>", "<ref name='open'>", 1).replace("</ref>", "", 1),
        ):
            with self.subTest(kind=changed[:30]), self.assertRaises((ValueError, TypeError)):
                extract_literary_body(changed)

    def test_rejects_short_story(self):
        with self.assertRaisesRegex(ValueError, "below 300000"):
            extract_literary_body(sample())

    def test_immutable_inventory_is_not_fabricated(self):
        with self.assertRaisesRegex(ValueError, "unsupported revision inventory"):
            _check_inventory({"schema_version": "wrong"})
        record = json.loads(Path("corpus/candidates/source-edition-traces/defoe-robinson-crusoe-translation-pair-ru.revision-inventory.json").read_text(encoding="utf-8"))
        witness = next(w for w in record["witnesses"] if w["work_id"] == CANDIDATE_ID)
        fetched = dict(
            title=witness["title"], page_id=witness["page_id"], revision_id=witness["revision_id"],
            revision_timestamp=witness["timestamp_utc"], mediawiki_sha1=witness["mediawiki_sha1"],
            wikitext_sha256="0" * 64, wikitext_character_count=12, wikitext_utf8_byte_count=12,
            wikitext="secret source",
        )
        with self.assertRaisesRegex(ValueError, "exact source identity drift"):
            build_manifest(record, fetcher=lambda **_: fetched.copy())

    def test_replay_does_not_accept_fake_parity_or_book_identity(self):
        with self.assertRaisesRegex(ValueError, "unsupported Shishmareva"):
            replay_manifest({}, {"schema_version": "invalid"})
        with self.assertRaisesRegex(ValueError, "parity claim"):
            replay_manifest({}, {"schema_version": SCHEMA, "candidate_id": CANDIDATE_ID,
                                 "m2_contribution": 1, "m2_parity_admissible": True})


if __name__ == "__main__":
    unittest.main()
