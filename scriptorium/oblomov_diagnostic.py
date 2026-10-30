"""Measure a revision-pinned full Russian Oblomov transcription without publishing prose.

This is a source-edition-bound Scriptorium diagnostic. It is NOT a FantLab
input match, benchmark PASS, verified printed-edition collation, or M2 parity.
"""
from __future__ import annotations

import argparse
from hashlib import sha256
import json
from math import isfinite
from pathlib import Path
import re
from typing import Callable, Mapping, Sequence

from .metrics import METRIC_CONTRACT_ID, SCHEMA_VERSION, analyze_deterministic_metrics
from .single_page_body import fetch_pinned_wikitext
from .text import normalize_text

PROFILE = "scriptorium-oblomov-azlib-literary-measurement-v1"
CANDIDATE = "goncharov-oblomov-azlib-ru"
TITLE = "Обломов (Гончаров)/Версия 2"
REVISION_ID = 5724579
SOURCE_URL = (
    "https://ru.wikisource.org/w/index.php?"
    "title=Обломов_(Гончаров)/Версия_2&oldid=5724579"
)
SOURCE_WITNESS = "http://az.lib.ru/g/goncharow_i_a/text_0020.shtml"
BODY_MINIMUM = 300_000
_CHAPTERS = (11, 12, 12, 11)
_ROMANS = ("I", "II", "III", "IV", "V", "VI", "VII", "VIII", "IX", "X", "XI", "XII")
_PARTS = ("ЧАСТЬ ПЕРВАЯ", "ЧАСТЬ ВТОРАЯ", "ЧАСТЬ ТРЕТЬЯ", "ЧАСТЬ ЧЕТВЕРТАЯ")
_HEADINGS = re.compile(r"(?m)^===\s*(.*?)\s*===\s*$")
_APPENDIX = re.compile(r"(?m)^''1857 и 1858[\u00a0 ]гг\.''")
_UNBOUND = frozenset({
    "fantlab.vocabulary.active_dictionary",
    "fantlab.vocabulary.active_nondictionary",
    "fantlab.vocabulary.uasz_3000",
    "fantlab.vocabulary.uasz_10000",
    "fantlab.vocabulary.uasz_100000",
})


def expected_headings() -> tuple[str, ...]:
    headings = ["Обломов"]
    for part_name, count in zip(_PARTS, _CHAPTERS):
        headings.append(part_name)
        for n in range(count):
            label = _ROMANS[n]
            if part_name == "ЧАСТЬ ПЕРВАЯ" and label == "IX":
                label = "IX Сон Обломова"
            headings.append(label)
    return tuple(headings)


def extract_literary_body(wikitext: str) -> str:
    """Exclude Wiki header, chapter labels, editorial footer and all markup."""
    if not isinstance(wikitext, str):
        raise TypeError("Wikisource revision content must be text")
    header, marker, remaining = wikitext.partition("=== Обломов ===")
    if not marker or not header.lstrip().startswith("{{Отексте"):
        raise ValueError("missing exact Oblomov source header")
    # These are properties of the pinned record, not a generic web access grant.
    if not re.search(r"\|\s*ЛИЦЕНЗИЯ\s*=\s*PD-old(?:\s|\|)", header):
        raise ValueError("missing public-domain source notice")
    for witness in ("Иван Александрович Гончаров", "1859", SOURCE_WITNESS):
        if witness not in header:
            raise ValueError("source bibliographic attribution drift")
    appendix = _APPENDIX.search(remaining)
    if appendix is None or _APPENDIX.search(remaining, appendix.end()) is not None:
        raise ValueError("missing or duplicate pinned editorial footer")
    afterword = remaining[appendix.start():]
    for witness in ("1954", "Впервые полностью опубликован", "[[Категория:"):
        if witness not in afterword:
            raise ValueError("pinned editorial witness missing: " + witness)
    before = remaining[:appendix.start()]
    preface = re.fullmatch(
        r"\s*<center>''Роман в[\u00a0 ]четырех частях''</center>\s*",
        before.split("=== ЧАСТЬ ПЕРВАЯ ===", 1)[0],
    )
    if preface is None:
        raise ValueError("unexpected literary title/preface layout")
    composed = "=== Обломов ===" + before
    observed = tuple(match.group(1).strip() for match in _HEADINGS.finditer(composed))
    if observed != expected_headings():
        raise ValueError("incomplete, reordered or changed four-part chapter inventory")
    body = _HEADINGS.sub("\n", before)
    body = re.sub(r"^\s*<center>.*?</center>\s*", "", body, flags=re.DOTALL)
    body = re.sub(r"'{2,5}", "", body).strip() + "\n"
    if any(token in body for token in ("{{", "}}", "[[", "]]", "<pages", "<ref", "<center", "</")):
        raise ValueError("unexpanded markup inside literary body")
    if "Гороховой улице" not in body[:400]:
        raise ValueError("beginning of novel was not retained")
    if not body.rstrip().endswith("И он рассказал ему, что здесь написано."):
        raise ValueError("end of novel was not retained")
    if len(body) < BODY_MINIMUM:
        raise ValueError("full literary body below 300000 characters including spaces")
    return body


def build_diagnostic(
    *,
    fetcher: Callable[..., dict[str, object]] = fetch_pinned_wikitext,
) -> dict[str, object]:
    """Replay exact revision and output source-free real measurements only."""
    observed = fetcher(title=TITLE, revision_id=REVISION_ID)
    if not isinstance(observed, dict):
        raise ValueError("invalid pinned source response")
    source = dict(observed)
    wikitext = source.pop("wikitext", None)
    if not isinstance(wikitext, str):
        raise ValueError("missing transient pinned literary source")
    encoded = wikitext.encode("utf-8")
    if (
        source.get("title") != TITLE
        or source.get("revision_id") != REVISION_ID
        or type(source.get("page_id")) is not int
        or source["page_id"] <= 0
        or not isinstance(source.get("revision_timestamp"), str)
        or not source["revision_timestamp"].endswith("Z")
        or not isinstance(source.get("mediawiki_sha1"), str)
        or not re.fullmatch(r"[0-9a-f]{40}", source["mediawiki_sha1"])
        or source.get("wikitext_character_count") != len(wikitext)
        or source.get("wikitext_utf8_byte_count") != len(encoded)
        or source.get("wikitext_sha256") != sha256(encoded).hexdigest()
    ):
        raise ValueError("pinned source identity drift before analysis")
    body = extract_literary_body(wikitext)
    analysis = analyze_deterministic_metrics(body)
    normalized = normalize_text(body)
    metrics = analysis.get("metrics")
    if (
        analysis.get("schema_version") != SCHEMA_VERSION
        or analysis.get("metric_contract_id") != METRIC_CONTRACT_ID
        or analysis.get("normalized_sha256") != sha256(normalized.encode("utf-8")).hexdigest()
        or analysis.get("dependencies", {}).get("vocabulary_dictionary") is not None
        or not isinstance(metrics, dict)
        or len(metrics) != 29
    ):
        raise ValueError("deterministic profile/metric contract drift")
    if metrics.get("fantlab.general.characters", {}).get("value") != len(normalized):
        raise ValueError("normalized literary character count differs from measured count")
    rows = []
    for metric_id, metric in sorted(metrics.items()):
        if not isinstance(metric, dict):
            raise ValueError("invalid deterministic metric row")
        value = metric.get("value")
        if value is not None and (type(value) not in (int, float) or not isfinite(value)):
            raise ValueError("invalid measured value")
        if value is None and metric_id not in _UNBOUND and not metric_id.startswith("fantlab.dialogue."):
            raise ValueError("unexpected missing deterministic measurement")
        if metric_id in _UNBOUND and value is not None:
            raise ValueError("dictionary-dependent field measured without a dictionary")
        status = (
            "NOT_RUN_DICTIONARY_UNBOUND" if metric_id in _UNBOUND else
            "UNAVAILABLE_NO_OBSERVATIONS" if value is None else
            "MEASURED_REFERENCE_UNAVAILABLE"
        )
        rows.append({
            "metric_id": metric_id, "actual": value,
            "unit": metric.get("unit"), "compatibility_status": metric.get("compatibility_status"),
            "fantlab_display": None, "result": status,
        })
    raw = body.encode("utf-8")
    return {
        "version": PROFILE, "candidate_id": CANDIDATE,
        "display_author": "Иван Александрович Гончаров", "display_title": "Обломов",
        "original_language": "ru", "analysis_language": "ru", "translator": None,
        "source": {
            "url": SOURCE_URL, "witness": SOURCE_WITNESS,
            "revision_id": REVISION_ID, "page_id": source["page_id"],
            "revision_timestamp": source["revision_timestamp"],
            "mediawiki_sha1": source["mediawiki_sha1"],
            "wikitext_sha256": source["wikitext_sha256"],
            "legal_basis": "public_domain_author_died_1891",
            "reported_edition": "az.lib.ru import; editorial note claims 1954 collation",
            "edition_identity_independently_matched": False,
        },
        "body": {
            "characters_including_spaces": len(body), "raw_sha256": sha256(raw).hexdigest(),
            "normalized_characters_including_spaces": len(normalized),
            "normalized_sha256": analysis["normalized_sha256"],
            "extraction_profile": PROFILE,
        },
        "scriptorium": {
            "schema_version": analysis["schema_version"],
            "metric_contract_id": analysis["metric_contract_id"],
            "profiles": analysis["profiles"],
            "vocabulary_dictionary_dependency": None,
        },
        "metric_rows": rows,
        "gates": {
            "complete_chapter_inventory": True, "minimum_300000_characters": True,
            "source_text_committed": False,
            "fantlab_input_identity": "UNKNOWN", "comparison_class": "DIAGNOSTIC_ONLY",
            "m2_parity_admissible": False, "m2_weight": 0,
            "source_edition_print_collation": "NOT_RUN",
        },
    }


def render_json(artifact: Mapping[str, object]) -> str:
    return json.dumps(artifact, ensure_ascii=False, sort_keys=True, indent=2, allow_nan=False) + "\n"


def main(argv: Sequence[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path, required=True, help="Create-only derived JSON; never raw prose")
    args = parser.parse_args(argv)
    artifact = build_diagnostic()
    args.output.parent.mkdir(parents=True, exist_ok=True)
    with args.output.open("x", encoding="utf-8") as output:
        output.write(render_json(artifact))
    print(
        "OBLOMOV_SOURCE_FREE_MEASURED=PASS; characters="
        + str(artifact["body"]["characters_including_spaces"])
        + "; fields=29; M2=0/5; FantLab_input=UNKNOWN"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
