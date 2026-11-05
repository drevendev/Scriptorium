"""Source-free body extractability preflight for the pinned mixed-edition White Guard.

Never publishes Wikisource chapter prose or promotes the 1927/1989 mixed source
into one edition. An extraction preview is not a frozen literary body, corpus
admission, or FantLab input/metric parity.
"""
from __future__ import annotations

import argparse
from hashlib import sha256
from pathlib import Path
import re
import sys
from typing import Callable, Mapping

from .white_guard_delivery import MANIFEST_PATH, MANIFEST_SHA256, load_manifest
from .white_guard_revisions import SOURCE_FAMILY_1927, canonical_json_text, validate_manifest
from .wikisource_replay import fetch_pinned_chapter_revisions
from .wikisource_freeze import BODY_FAILURE_CODES, BodyExtractionError, extract_transcription_body

SCHEMA_VERSION = "scriptorium-white-guard-body-preflight-v3"
EXTRACTION_PROFILE = "scriptorium-wikisource-body-v1-preview-only"
MAX_CHAPTER_WIKITEXT_CHARACTERS = 2_000_000
MIN_CORPUS_CHARACTERS = 300_000

# A whitelisted source-family route, not a bound Index: or Page: revision.
PROOFREADPAGE_INDEX = "Дни Турбиных (Белая гвардия) (Булгаков, 1927).djvu"
_BODY_DIV = re.compile(r"""<div\s+class=["'](?:text|indent)["']\s*>(.*?)</div>""", re.I | re.S)
_PAGES_ONLY = re.compile(
    r"""<pages\s+index="(?P<index>[^"<>\r\n]+)"\s+from=(?P<first>[0-9]+)\s+to=(?P<last>[0-9]+)\s*/>""",
    re.I,
)


def _unfrozen_proofreadpage_range(wikitext: str) -> dict[str, object] | None:
    """Report a narrowly observed page range, never an extracted literary body.

    Reject extra attributes (including section/step/exclude), multiple routes,
    mixed text, invalid indexes and unbounded spans instead of guessing content.
    """
    bodies = _BODY_DIV.findall(wikitext)
    if len(bodies) != 1:
        return None
    match = _PAGES_ONLY.fullmatch(bodies[0].strip())
    if match is None or match.group("index") != PROOFREADPAGE_INDEX:
        return None
    first, last = int(match.group("first")), int(match.group("last"))
    if not 1 <= first <= last <= 4000 or last - first + 1 > 100:
        return None
    return {
        "index_title": PROOFREADPAGE_INDEX,
        "first_page": first,
        "last_page": last,
        "page_count": last - first + 1,
    }


def build_preflight(
    manifest_path: Path = Path(MANIFEST_PATH),
    *,
    fetcher: Callable[[tuple[dict[str, object], ...]], Mapping[str, str]] = fetch_pinned_chapter_revisions,
    extractor: Callable[[str], str] = extract_transcription_body,
) -> dict[str, object]:
    """Fetch exactly frozen revisions and audit body extraction without saving prose.

    Unsupported individual page structures are reported as safe status codes;
    missing/changed source identities are hard failures rather than partial data.
    This function must not emit or persist source text, including in exceptions.
    """
    manifest = load_manifest(manifest_path)
    identities = validate_manifest(manifest)
    expected_titles = {row["title"] for row in identities}
    fetched = fetcher(identities)
    if not isinstance(fetched, Mapping) or set(fetched) != expected_titles:
        raise ValueError("pinned chapter inventory mismatch")

    entries: list[dict[str, object]] = []
    candidates: list[str] = []
    for row, source in zip(manifest["pages"], (fetched[i["title"]] for i in identities), strict=True):
        if not isinstance(source, str) or len(source) > MAX_CHAPTER_WIKITEXT_CHARACTERS:
            raise ValueError("invalid or oversized pinned wikitext")
        raw = source.encode("utf-8")
        entry: dict[str, object] = {
            "chapter": row["chapter"],
            "source_family_id": row["source_family_id"],
            "revision_id": row["revision_id"],
            "wikitext_characters": len(source),
            "wikitext_sha256": sha256(raw).hexdigest(),
            "extraction_status": "UNSUPPORTED_MARKUP",
            "extraction_failure_code": None,
            "candidate_body_characters": None,
            "candidate_body_sha256": None,
            "proofreadpage_page_plan": None,
        }
        try:
            body = extractor(source)
            if not isinstance(body, str) or not body.strip() or len(body) > MAX_CHAPTER_WIKITEXT_CHARACTERS:
                raise ValueError("invalid candidate body")
        except BodyExtractionError as exc:
            # Never surface an unrecognized, possibly attacker-controlled error code.
            entry["extraction_failure_code"] = (
                exc.code if exc.code in BODY_FAILURE_CODES else "UNCLASSIFIED_ERROR"
            )
            if (entry["extraction_failure_code"] == "PROOFREADPAGE_UNPINNED"
                    and row["source_family_id"] == SOURCE_FAMILY_1927):
                entry["proofreadpage_page_plan"] = _unfrozen_proofreadpage_range(source)
        except Exception:
            # Catch unexpected parser faults only at the extractor boundary.
            # Provider/identity failures above remain hard failures; never emit
            # exception messages or provider text into a derived-only receipt.
            entry["extraction_failure_code"] = "UNCLASSIFIED_ERROR"
        else:
            entry["extraction_status"] = "CANDIDATE_ONLY"
            entry["candidate_body_characters"] = len(body)
            entry["candidate_body_sha256"] = sha256(body.encode("utf-8")).hexdigest()
            candidates.append(body)
        entries.append(entry)

    complete = len(candidates) == len(identities)
    # Only a full chapter set can have an observable composite identity. The
    # historic source partition nevertheless prevents claiming a single edition.
    composite = "\n\n".join(candidates) if complete else None
    size = len(composite) if composite is not None else None
    return {
        "schema_version": SCHEMA_VERSION,
        "candidate_id": manifest["candidate_id"],
        "manifest_sha256": MANIFEST_SHA256,
        "provider_replay": "VERIFIED_IDENTITIES" if fetcher is fetch_pinned_chapter_revisions else "INJECTED_FIXTURE",
        "extraction_profile": EXTRACTION_PROFILE,
        "chapter_count": len(identities),
        "candidate_chapter_count": len(candidates),
        "chapters": entries,
        "candidate_composite_characters_including_spaces": size,
        "candidate_composite_sha256": sha256(composite.encode("utf-8")).hexdigest() if composite is not None else None,
        "candidate_meets_size_threshold": (size >= MIN_CORPUS_CHARACTERS) if size is not None else None,
        "literary_body_extraction_frozen": False,
        "single_edition_identity": False,
        "fantlab_input_identity": "unknown",
        "m2_parity_admissible": False,
        "source_text_committed": False,
    }


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--manifest", type=Path, default=Path(MANIFEST_PATH))
    args = parser.parse_args(argv)
    try:
        receipt = build_preflight(args.manifest)
    except Exception:
        # Provider/manifest/programming failures fail closed, without tracebacks
        # containing potentially private source text or upstream error details.
        print("Pinned White Guard body preflight failed; no receipt issued.", file=sys.stderr)
        return 2
    print(canonical_json_text(receipt), end="")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
