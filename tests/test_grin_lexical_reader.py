"""Public numeric-only Grin Reader: exact frozen CI evidence and no source prose."""
from __future__ import annotations
import copy
from html.parser import HTMLParser
import json
from pathlib import Path
import unittest

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "assets/grin-lexical-diagnostic.json"
PAGE = ROOT / "lexical-grin.html"
AGG = {
    "shared_form_count": 5901,
    "left_only_form_count": 11043,
    "right_only_form_count": 8505,
    "eligible_form_count": 3094,
    "excluded_rare_form_count": 22355,
    "balanced_form_count": 1719,
    "left_dominant_form_count": 769,
    "right_dominant_form_count": 606,
    "type_jaccard_percent": 23.187552,
    "token_distribution_overlap_percent": 59.843147,
    "jensen_shannon_divergence_bits": 0.293793,
}
DIGESTS = (
    "e33a28b8dcdb3ac339147c6587b27c182dd910784122b367db41bc93dfc2dbee",
    "41a1ada3caabea2909976372ca6312fb8a478f2d0d87c088f304fcb30c52fdbc",
)
CI_ZIP = "6c8ab5c170024554e0d92ba116acf0cf028d3bb6abba49e2fb8a86d99a7e2117"
CI_JSON = "90b80850c4a3c7f376bdb4c8deb704c8eac495b3c26b89a5a3c767ae0fbc5d36"


def validate(doc):
    if type(doc) is not dict or set(doc) != {
        "schema_version", "status", "source_text_included", "per_form_data_included",
        "corpus_admission", "m2_parity_admissible", "fantlab_analyzer_input_match",
        "compatibility_status", "publication_scope", "provenance", "works",
        "aggregate", "methodology",
    }:
        raise ValueError("unapproved public projection structure")
    exact = {
        "schema_version": "scriptorium-grin-lexical-reader-diagnostic-v1",
        "status": "DIAGNOSTIC_ONLY", "source_text_included": False,
        "per_form_data_included": False, "corpus_admission": "NOT_VERIFIED",
        "m2_parity_admissible": False, "fantlab_analyzer_input_match": "UNKNOWN",
        "compatibility_status": "extension",
        "publication_scope": "public numeric aggregates only; original local contrast is NOT public-release-ready",
    }
    if any(type(doc[k]) is not type(v) or doc[k] != v for k, v in exact.items()):
        raise ValueError("incorrect publication/science scope")
    provenance = doc["provenance"]
    if (type(provenance) is not dict or set(provenance) != {
        "source_pr", "source_commit", "reviewed_merge_commit", "ci_run_id",
        "ci_artifact_id", "ci_zip_sha256", "ci_json_sha256", "rights_basis",
    } or provenance["ci_run_id"] != 45009800452
        or provenance["ci_artifact_id"] != 14749396260
        or provenance["source_pr"] != 613
        or provenance["source_commit"] != "f8b445fc1754906dd3a135740212a3ddb31717fe"
        or provenance["reviewed_merge_commit"] != "13350f47986d942e6998181320ed0c89ac8489e9"
        or provenance["ci_zip_sha256"] != CI_ZIP
        or provenance["ci_json_sha256"] != CI_JSON
        or not provenance["rights_basis"].startswith("Public-domain original Russian works")):
        raise ValueError("unreviewed CI provenance")
    works = doc["works"]
    if type(works) is not list or len(works) != 2:
        raise ValueError("expected two pinned works")
    expected = (
        ("grin-road-nowhere", 442656, 65072, 16944, DIGESTS[0],
         "grin-road-nowhere-azlib-oldid-5585836"),
        ("grin-running-waves", 363819, 55778, 14406, DIGESTS[1],
         "grin-running-waves-detlit-1965-revision-composite"),
    )
    for work, (identity, chars, tokens, types, digest, edition) in zip(works, expected):
        if (type(work) is not dict or set(work) - {
            "id","title","author","edition_id","source_url","normalized_sha256",
            "characters_including_spaces","word_tokens","distinct_forms",
            "literary_page_revisions","language",
        } or set(work) not in (
            {"id","title","author","edition_id","source_url","normalized_sha256",
             "characters_including_spaces","word_tokens","distinct_forms","language"},
            {"id","title","author","edition_id","source_url","normalized_sha256",
             "characters_including_spaces","word_tokens","distinct_forms",
             "literary_page_revisions","language"},
        )
            or work["id"] != identity or work["edition_id"] != edition
            or work["normalized_sha256"] != digest or work["language"] != "ru"
            or type(work["characters_including_spaces"]) is not int
            or type(work["word_tokens"]) is not int
            or type(work["distinct_forms"]) is not int
            or (work["characters_including_spaces"],work["word_tokens"],work["distinct_forms"])
               != (chars,tokens,types)
            or work["author"] != "Александр Грин"
            or not work["source_url"].startswith("https://ru.wikisource.org/")):
            raise ValueError("unverified work edition")
    if works[0]["title"] != "Дорога в никуда" or works[1]["title"] != "Бегущая по волнам":
        raise ValueError("title drift")
    if works[0].get("literary_page_revisions") is not None or works[1].get("literary_page_revisions") != 36:
        raise ValueError("page count drift")
    if (type(doc["aggregate"]) is not dict or set(doc["aggregate"]) != set(AGG)
        or any(type(doc["aggregate"][key]) is not type(val) or doc["aggregate"][key] != val
               for key, val in AGG.items())):
        raise ValueError("aggregate measurement drift")
    a = doc["aggregate"]
    if (a["shared_form_count"] + a["left_only_form_count"] != works[0]["distinct_forms"]
        or a["shared_form_count"] + a["right_only_form_count"] != works[1]["distinct_forms"]
        or abs(100 * a["shared_form_count"] /
               (a["shared_form_count"] + a["left_only_form_count"] +
                a["right_only_form_count"]) - a["type_jaccard_percent"]) > 0.000001):
        raise ValueError("inconsistent lexical type denominators")
    method = doc["methodology"]
    if (type(method) is not dict or set(method) != {
        "version","vocabulary_profile","normalization_profile","identity","jaccard",
        "token_overlap","divergence","dominance",
    } or method["version"] != "scriptorium-lexical-aggregate-contrast-v1"
        or method["vocabulary_profile"] != "scriptorium-vocabulary-v1"
        or method["normalization_profile"] != "scriptorium-text-v1"
        or not method["identity"].startswith("NFC + Unicode casefold")):
        raise ValueError("unverified lexical method")
    return doc


class Pages(HTMLParser):
    def __init__(self, html):
        super().__init__()
        self.ids = []
        self.links = []
        self.feed(html)

    def handle_starttag(self, tag, attrs):
        values = dict(attrs)
        if "id" in values:
            self.ids.append(values["id"])
        if tag == "a":
            self.links.append(values.get("href"))


class GrinLexicalReaderTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.doc = json.loads(DATA.read_text(encoding="utf-8"))
        cls.html = PAGE.read_text(encoding="utf-8")

    def test_exact_source_free_json_and_equations(self):
        d = validate(self.doc)
        self.assertEqual(len(d["works"]), 2)
        self.assertEqual(d["aggregate"]["shared_form_count"], 5901)
        self.assertNotIn('"source_text":', DATA.read_text(encoding="utf-8"))
        self.assertNotIn('"word_forms":', DATA.read_text(encoding="utf-8"))

    def test_tamper_and_leakage_are_rejected(self):
        for section, name, value in (
            ("aggregate", "shared_form_count", 5902),
            ("aggregate", "type_jaccard_percent", True),
            ("aggregate", "jensen_shannon_divergence_bits", 1.5),
            ("provenance", "ci_json_sha256", "0" * 64),
            ("methodology", "version", "unreviewed"),
            (None, "corpus_admission", "ADMITTED"),
            (None, "source_text_included", True),
        ):
            fake = copy.deepcopy(self.doc)
            (fake[section] if section else fake)[name] = value
            with self.subTest(field=name), self.assertRaises(ValueError):
                validate(fake)
        for name in ("source_text", "word_forms", "rare_word_hashes"):
            fake = copy.deepcopy(self.doc)
            fake[name] = ["secret"]
            with self.subTest(leak=name), self.assertRaises(ValueError):
                validate(fake)

    def test_chart_and_numeric_table_match_pinned_receipt(self):
        d = validate(self.doc)
        text = self.html
        a = d["aggregate"]
        for value in ("5 901", "11 043", "8 505", "65 072", "55 778",
                      "442 656", "363 819", "16 944", "14 406",
                      "23,19%", "59,84%", "0,29", "769", "606"):
            self.assertIn(value, text)
        union = a["shared_form_count"] + a["left_only_form_count"] + a["right_only_form_count"]
        for v in (a["left_only_form_count"], a["shared_form_count"], a["right_only_form_count"]):
            self.assertIn(f'width:{100*v/union:.6f}%', text)
        self.assertIn('id="lex-type-chart"', text)
        self.assertIn('id="lex-token-chart"', text)
        self.assertIn('id="lex-exact-table"', text)
        self.assertIn('role="img"', text)
        self.assertIn("aria-label=", text)
        self.assertIn("NOT_VERIFIED", text)
        self.assertIn("M2: <strong>0/5</strong>", text)
        self.assertIn(CI_ZIP, text)
        self.assertIn(CI_JSON, text)
        for sha in DIGESTS:
            self.assertIn(sha, text)
        self.assertNotIn("<script", text.lower())
        parsed = Pages(text)
        self.assertEqual(len(parsed.ids), len(set(parsed.ids)))
        self.assertIn("./assets/grin-lexical-diagnostic.json", parsed.links)
        self.assertIn("./#books", parsed.links)
        self.assertIn("#methodology", parsed.links)

    def test_branch_pages_and_reader_discovery(self):
        index = (ROOT / "index.html").read_text(encoding="utf-8")
        readme = (ROOT / "README.md").read_text(encoding="utf-8")
        audit = (ROOT / "scriptorium/branch_pages_audit.py").read_text(encoding="utf-8")
        workflow = (ROOT / ".github/workflows/pages.yml").read_text(encoding="utf-8")
        self.assertIn('href="./lexical-grin.html"', index)
        self.assertIn("lexical-grin.html", readme)
        self.assertIn('"lexical-grin.html"', audit)
        self.assertIn('"assets/grin-lexical-diagnostic.json"', audit)
        for file in ("lexical-grin.html", "assets/grin-lexical-diagnostic.json"):
            self.assertIn(f"cp {file} build/branch-root-preview/{file}", workflow)
            self.assertIn(f"test -s build/branch-root-preview/{file}", workflow)
            self.assertIn(f"cmp {file} build/branch-root-preview/{file}", workflow)
        self.assertIn("node tests/pages_grin_lexical_browser.cjs", workflow)


if __name__ == "__main__":
    unittest.main()
