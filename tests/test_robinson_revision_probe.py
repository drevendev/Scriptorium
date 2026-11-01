from hashlib import sha256
import json
import tempfile
from pathlib import Path
import unittest
from unittest.mock import patch

from scriptorium.robinson_revision_probe import (
    REVISION_BY_WORK,
    _observe_revision,
    main,
    probe_pair,
)


def _screening():
    return {
        "schema_version": "scriptorium-translation-pair-screening-v1",
        "witnesses": [
            {
                "work_id": work_id,
                "revision_oldid": revid,
                "source_revision": f"https://ru.wikisource.org/w/index.php?oldid={revid}",
            }
            for work_id, revid in REVISION_BY_WORK.items()
        ],
    }


def _response(revid, source="{{Отексте}}\n== Глава 1 ==\nСекретный литературный текст ѣ.\n[[Категория:Книги]]"):
    return {"query": {"pages": [{
        "pageid": 2500 + revid,
        "title": f"Робинзон/{revid}",
        "revisions": [{
            "revid": revid,
            "timestamp": "2026-01-01T00:00:00Z",
            "sha1": "a" * 40,
            "slots": {"main": {"contentmodel": "wikitext", "content": source}},
        }],
    }]}}


def _query(params):
    return _response(int(params["revids"]))


class RobinsonRevisionProbeTests(unittest.TestCase):
    def test_exact_pair_produces_only_source_free_revision_inventory(self):
        result = probe_pair(_screening(), query=_query)
        self.assertEqual(result["status"], "REVISION_WIKITEXT_INVENTORY_ONLY")
        self.assertEqual(len(result["witnesses"]), 2)
        self.assertEqual({x["revision_id"] for x in result["witnesses"]}, set(REVISION_BY_WORK.values()))
        self.assertFalse(result["both_literary_bodies_frozen"])
        self.assertEqual(result["m2_contribution"], 0)
        for witness in result["witnesses"]:
            source = _response(witness["revision_id"])["query"]["pages"][0]["revisions"][0]["slots"]["main"]["content"]
            self.assertEqual(witness["wikitext_sha256"], sha256(source.encode("utf-8")).hexdigest())
            self.assertEqual(witness["wikitext_characters_including_spaces"], len(source))
            self.assertEqual(witness["markup_inventory"]["headings"], 1)
            self.assertEqual(witness["markup_inventory"]["category_links"], 1)
            self.assertIsNone(witness["literary_body_sha256"])
            self.assertIsNone(witness["literary_characters_including_spaces"])
            self.assertFalse(witness["corpus_threshold_verified"])
            self.assertFalse(witness["m2_parity_admissible"])
        serialized = json.dumps(result, ensure_ascii=False)
        self.assertNotIn("Секретный литературный текст", serialized)
        self.assertNotIn("{{Отексте}}", serialized)

    def test_mixed_transclusion_is_not_mistaken_for_literary_body(self):
        observed = _observe_revision(
            5041937,
            query=lambda p: _response(
                5041937,
                "{{:Робинзон/Глава}}<pages index='x'/><noinclude>proof</noinclude>"
            ),
        )
        self.assertEqual(observed["markup_inventory"]["transclusion_openers"], 1)
        self.assertEqual(observed["markup_inventory"]["pages_tags"], 1)
        self.assertEqual(observed["markup_inventory"]["inclusion_tags"], 2)
        self.assertIsNone(observed["literary_characters_including_spaces"])

    def test_rejects_wrong_witness_revision_url_or_input_shape(self):
        for mutation in (
            lambda s: s["witnesses"][0].update(revision_oldid=1),
            lambda s: s["witnesses"][0].update(source_revision="https://evil.example/w/index.php?oldid=5041937"),
            lambda s: s["witnesses"][0].update(source_revision="https://evil@ru.wikisource.org/w/index.php?oldid=5041937"),
            lambda s: s["witnesses"][0].update(source_revision="https://ru.wikisource.org/w/index.php?oldid=5041937&action=raw"),
            lambda s: s["witnesses"].append(s["witnesses"][0]),
            lambda s: s.update(schema_version="other"),
        ):
            screening = _screening()
            mutation(screening)
            with self.subTest(screening=screening), self.assertRaises(ValueError):
                probe_pair(screening, query=_query)

    def test_rejects_stale_or_missing_revision_content(self):
        for mutation in (
            lambda p: p["query"]["pages"][0]["revisions"][0].update(revid=1),
            lambda p: p["query"]["pages"][0]["revisions"][0]["slots"]["main"].pop("content"),
            lambda p: p["query"]["pages"][0]["revisions"][0].update(sha1="not-sha"),
            lambda p: p.update(error={"code": "notfound"}),
            lambda p: p["query"]["pages"].append({}),
        ):
            payload = _response(5041937)
            mutation(payload)
            with self.subTest(payload=payload), self.assertRaises(ValueError):
                _observe_revision(5041937, query=lambda _: payload)

    def test_cli_fails_before_writing_and_never_overwrites(self):
        with tempfile.TemporaryDirectory() as temp:
            source = Path(temp) / "screening.json"
            output = Path(temp) / "probe.json"
            source.write_text(json.dumps(_screening()), encoding="utf-8")
            with patch("scriptorium.robinson_revision_probe._api_query", side_effect=_query):
                self.assertEqual(main(["--screening", str(source), "--output", str(output)]), 0)
                original = output.read_bytes()
                with self.assertRaises(FileExistsError):
                    main(["--screening", str(source), "--output", str(output)])
            self.assertEqual(output.read_bytes(), original)
            self.assertEqual(json.loads(original)["m2_contribution"], 0)


if __name__ == "__main__":
    unittest.main()
