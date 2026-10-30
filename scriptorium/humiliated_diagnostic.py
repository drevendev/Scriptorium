"""Measure a revision-pinned full Russian Humiliated and Insulted text.

Fetch only an exact public-domain Wikisource revision, discard comments and
markup, and output source-free deterministic observations. The resulting
measurements are DIAGNOSTIC ONLY, never a FantLab input/parity match.
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

PROFILE = "scriptorium-humiliated-azlib-literary-measurement-v1"
CANDIDATE = "dostoevsky-humiliated-and-insulted-azlib-ru"
TITLE = "Униженные и оскорбленные (Достоевский)/Версия 2"
REVISION_ID = 5611473
SOURCE_URL = (
    "https://ru.wikisource.org/w/index.php?"
    "title=Униженные_и_оскорбленные_(Достоевский)/Версия_2&oldid=5611473"
)
SOURCE_WITNESS = "az.lib.ru"
BODY_MINIMUM = 300_000
_ROMANS = ("I", "II", "III", "IV", "V", "VI", "VII", "VIII", "IX", "X", "XI", "XII", "XIII", "XIV", "XV")
_PARTS = ("ЧАСТЬ ПЕРВАЯ", "ЧАСТЬ ВТОРАЯ", "ЧАСТЬ ТРЕТЬЯ", "ЧАСТЬ ЧЕТВЕРТАЯ")
_CHAPTERS = (15, 11, 10, 9)
_HEADINGS = re.compile(r"(?m)^===\s*([^\n]*?)\s*===\s*$")
# The pinned Wikisource heading spells "и оскорбленные" with U+00A0.
# Match only its harmless space variants; never rewrite the literary body.
_TITLE_HEADING = re.compile(
    r"(?m)^===[ \t]*Униженные[ \t\u00a0]+и[ \t\u00a0]+оскорбленные[ \t\u00a0]*===[ \t]*$"
)
_UNBOUND = frozenset({
    "fantlab.vocabulary.active_dictionary", "fantlab.vocabulary.active_nondictionary",
    "fantlab.vocabulary.uasz_3000", "fantlab.vocabulary.uasz_10000",
    "fantlab.vocabulary.uasz_100000",
})


def expected_headings() -> tuple[str, ...]:
    sequence = ["Униженные и оскорбленные"]
    for part, count in zip(_PARTS, _CHAPTERS):
        sequence.append(part)
        sequence.extend("Глава " + ordinal for ordinal in _ROMANS[:count])
    sequence.extend(("ЭПИЛОГ", "Последние воспоминания"))
    return tuple(sequence)


def extract_literary_body(wikitext: str) -> str:
    """Return full four-part novel and epilogue; reject altered boundaries.

    Comments are editorial material, not novel prose, and must not contaminate
    metrics. The chapter inventory/anchors are checked before trimming labels.
    """
    if not isinstance(wikitext, str):
        raise TypeError("pinned Wikisource page must be text")
    title_match = _TITLE_HEADING.search(wikitext)
    if title_match is None:
        raise ValueError("missing exact novel source template/title")
    preface = wikitext[:title_match.start()]
    remainder = wikitext[title_match.end():]
    if not preface.lstrip().startswith("{{Отексте"):
        raise ValueError("missing exact novel source template/title")
    if not re.search(r"\|\s*ЛИЦЕНЗИЯ\s*=\s*PD-old(?:-70)?(?:\s|\|)", preface):
        raise ValueError("missing public-domain source notice")
    for witness in ("Достоевский", "1861", SOURCE_WITNESS):
        if witness not in preface:
            raise ValueError("missing source bibliographic witness: " + witness)
    novel, found, comments = remainder.partition("=== Комментарии ===")
    if not found or "Буданова" not in comments or "Впервые опубликовано" not in comments:
        raise ValueError("missing editorial-commentary boundary")
    if "=== Комментарии ===" in comments:
        raise ValueError("duplicate commentary boundary")
    observed = tuple(
        match.group(1).strip().replace("\u00a0", " ")
        for match in _HEADINGS.finditer(wikitext[title_match.start():title_match.end()] + novel)
    )
    if observed != expected_headings():
        raise ValueError("incomplete, duplicated or reordered four-part/epilogue heading inventory")
    start = novel.find("=== Глава I ===")
    if start < 0 or "Роман в" not in novel[:start]:
        raise ValueError("missing literary preface and opening chapter")
    body = _HEADINGS.sub("\n", novel[start:])
    # Apostrophes only mark emphasis in this pinned Wikisource family; the
    # resulting body retains native punctuation, case and all other spacing.
    body = re.sub(r"'{2,5}", "", body).strip() + "\n"
    markers = ("{{", "}}", "[[", "]]", "<ref", "</", "<br", "<center")
    unexpected = {mark: body.count(mark) for mark in markers if mark in body}
    if unexpected:
        # Expose marker categories/counts only, never a prose snippet or location.
        html_closers = sorted(set(re.findall(r"</([A-Za-z][A-Za-z0-9]*)", body)))
        raise ValueError("unexpanded wiki/HTML markup in novel body: " + repr(unexpected)
                         + "; closing_tag_names=" + repr(html_closers))
    if "Прошлого года, двадцать второго марта" not in body[:350]:
        raise ValueError("beginning of novel was not retained")
    if "навеки счастливы вместе" not in " ".join(body[-1300:].split()):
        raise ValueError("ending of epilogue was not retained")
    if len(body) < BODY_MINIMUM:
        raise ValueError("full literary body below 300000 characters including spaces")
    return body


def build_diagnostic(*, fetcher: Callable[..., dict[str, object]] = fetch_pinned_wikitext) -> dict[str, object]:
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
        or type(source.get("page_id")) is not int or source["page_id"] <= 0
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
        or not isinstance(metrics, dict) or len(metrics) != 29
    ):
        raise ValueError("deterministic profile/metric contract drift")
    if metrics.get("fantlab.general.characters", {}).get("value") != len(normalized):
        raise ValueError("character count differs from normalized body")
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
            raise ValueError("unbound dictionary-dependent field unexpectedly measured")
        rows.append({
            "metric_id": metric_id, "actual": value,
            "unit": metric.get("unit"), "compatibility_status": metric.get("compatibility_status"),
            "fantlab_display": None,
            "result": ("NOT_RUN_DICTIONARY_UNBOUND" if metric_id in _UNBOUND else
                       "UNAVAILABLE_NO_OBSERVATIONS" if value is None else
                       "MEASURED_REFERENCE_UNAVAILABLE"),
        })
    return {
        "version": PROFILE, "candidate_id": CANDIDATE,
        "display_author": "Фёдор Михайлович Достоевский",
        "display_title": "Униженные и оскорбленные",
        "original_language": "ru", "analysis_language": "ru", "translator": None,
        "source": {
            "url": SOURCE_URL, "witness": SOURCE_WITNESS, "revision_id": REVISION_ID,
            "page_id": source["page_id"], "revision_timestamp": source["revision_timestamp"],
            "mediawiki_sha1": source["mediawiki_sha1"],
            "wikitext_sha256": source["wikitext_sha256"],
            "legal_basis": "public_domain_original_author_died_1881",
            "reported_edition": "Wikisource az.lib.ru import; print edition not collated",
            "edition_identity_independently_matched": False,
        },
        "body": {
            "characters_including_spaces": len(body),
            "raw_sha256": sha256(body.encode("utf-8")).hexdigest(),
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
            "complete_chapter_inventory": True,
            "minimum_300000_characters": True,
            "source_text_committed": False,
            "fantlab_input_identity": "UNKNOWN",
            "comparison_class": "DIAGNOSTIC_ONLY",
            "m2_parity_admissible": False,
            "m2_weight": 0,
            "source_edition_print_collation": "NOT_RUN",
        },
    }


def render_json(artifact: Mapping[str, object]) -> str:
    return json.dumps(artifact, ensure_ascii=False, sort_keys=True, indent=2, allow_nan=False) + "\n"


def main(argv: Sequence[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path, required=True,
                        help="Create-only source-free derived JSON; never full novel prose")
    args = parser.parse_args(argv)
    artifact = build_diagnostic()
    args.output.parent.mkdir(parents=True, exist_ok=True)
    with args.output.open("x", encoding="utf-8") as handle:
        handle.write(render_json(artifact))
    print("HUMILIATED_MEASURED=PASS; characters="
          + str(artifact["body"]["characters_including_spaces"])
          + "; fields=29; FantLab_input=UNKNOWN; M2=0/5")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
