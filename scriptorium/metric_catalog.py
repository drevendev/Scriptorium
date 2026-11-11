"""Offline, source-free catalogue of the installed deterministic metric contract.

This is a definition lookup, not a FantLab parity or calibration result.
"""
from __future__ import annotations

import argparse
import json
from pathlib import Path

from .analyze import _write_new
from .metric_labels import METRIC_LABELS, METRIC_LABELS_RU
from .metrics import METRIC_CONTRACT_ID, METRIC_DEFINITIONS

CATALOG_SCHEMA = "scriptorium-metric-catalog-v1"
_DICTIONARY_DEPENDENT = frozenset({
    "fantlab.vocabulary.active_dictionary",
    "fantlab.vocabulary.active_nondictionary",
    "fantlab.vocabulary.uasz_3000",
    "fantlab.vocabulary.uasz_10000",
    "fantlab.vocabulary.uasz_100000",
})

_UNITS_RU = {
    "characters": "символы",
    "words": "слова",
    "sentences": "предложения",
    "characters/word": "символов на слово",
    "characters/sentence": "символов на предложение",
    "percent": "проценты",
    "unique_dictionary_words/window": "уникальные словарные формы на окно",
    "occurrences/1000_words": "событий на 1 000 слов",
}
_EVIDENCE_RU = {
    "public_surface": "публичное поле",
    "public_definition": "публичное определение",
    "scriptorium_extension": "расширение Scriptorium",
}
_STATUS_RU = {
    "inferred": "предположительная реализация (inferred)",
    "extension": "расширение (extension)",
}


def build_catalog(metric_id: str | None = None, *, language: str = "en") -> dict[str, object]:
    """Describe only IDs actually registered by the installed extraction engine."""
    if (
        set(METRIC_LABELS) != set(METRIC_DEFINITIONS)
        or set(METRIC_LABELS_RU) != set(METRIC_DEFINITIONS)
        or len(METRIC_DEFINITIONS) != 29
    ):
        raise ValueError("installed metric catalogue does not match extraction contract")
    if language not in {"en", "ru"}:
        raise ValueError("unsupported metric catalogue language")
    labels = METRIC_LABELS_RU if language == "ru" else METRIC_LABELS
    if metric_id is not None and metric_id not in METRIC_DEFINITIONS:
        raise ValueError("unknown registered metric ID")
    ids = sorted(METRIC_DEFINITIONS) if metric_id is None else [metric_id]
    rows = []
    for name in ids:
        unit, evidence, status = METRIC_DEFINITIONS[name]
        rows.append({
            "id": name,
            "label": labels[name],
            "unit": unit,
            "definition_evidence": evidence,
            "compatibility_status": status,
            "dictionary_required": name in _DICTIONARY_DEPENDENT,
        })
    catalog = {
        "schema_version": CATALOG_SCHEMA,
        "metric_contract_id": METRIC_CONTRACT_ID,
        "scientific_claim": "DEFINITIONS_ONLY_NOT_FANTLAB_PARITY",
        "metrics": rows,
    }
    # Opt-in locale is explicit; default v1 JSON stays byte-for-byte stable.
    if language == "ru":
        catalog["label_language"] = "ru"
    return catalog


def render_text(catalog: dict[str, object]) -> str:
    """Readable plain text, without ANSI escapes or external assets."""
    rows = catalog["metrics"]
    if catalog.get("label_language") == "ru":
        lines = [
            f"Метрики Scriptorium · {catalog['metric_contract_id']}",
            "Определения не подтверждают совпадение с FantLab (M2: 0/5).",
            "Inferred — предположительная реализация; extension — собственное расширение.",
            "Словарные метрики могут быть недоступны без явно указанного словаря.",
            "",
        ]
        for row in rows:
            dictionary_note = " · нужен словарь" if row["dictionary_required"] else ""
            lines.append(f"{row['label']} ({row['id']})")
            lines.append(
                f"  {_UNITS_RU[row['unit']]} [{row['unit']}] · "
                f"{_STATUS_RU[row['compatibility_status']]} · "
                f"{_EVIDENCE_RU[row['definition_evidence']]}{dictionary_note}"
            )
        return "\n".join(lines) + "\n"
    lines = [
        f"Scriptorium metrics · {catalog['metric_contract_id']}",
        "Registered deterministic definitions; NOT source-matched FantLab parity.",
        "Public surface/definition = inferred candidate; Scriptorium extension = separate metric.",
        "Dictionary-required rows may be unavailable without a supplied dictionary.",
        "",
    ]
    for row in rows:
        dictionary_note = " · dictionary required" if row["dictionary_required"] else ""
        lines.append(f"{row['label']} ({row['id']})")
        lines.append(
            f"  {row['unit']} · {row['compatibility_status']} · "
            f"{row['definition_evidence']}{dictionary_note}"
        )
    return "\n".join(lines) + "\n"


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description="Inspect the 29 installed metric definitions, units and evidence; not FantLab parity."
    )
    parser.add_argument("metric_id", nargs="?", help="Optional exact registered metric ID")
    parser.add_argument("--format", choices=("text", "json"), default="text")
    parser.add_argument("--lang", choices=("en", "ru"), default="en",
                        help="Human labels in English (default) or Russian")
    parser.add_argument("--output", type=Path, help="Create a new source-free output file")
    args = parser.parse_args(argv)
    try:
        catalog = build_catalog(args.metric_id, language=args.lang)
        rendered = (
            json.dumps(catalog, ensure_ascii=False, indent=2, sort_keys=True) + "\n"
            if args.format == "json" else render_text(catalog)
        )
        if args.output is None:
            print(rendered, end="")
        else:
            _write_new(args.output, rendered)
    except FileExistsError:
        parser.error("metric catalogue output already exists; choose another destination")
    except ValueError:
        parser.error("unknown or inconsistent installed metric catalogue")
    except OSError:
        parser.error("unable to create metric catalogue output")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
