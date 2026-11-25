"""Source-free, partial orthography experiment; never an extraction fallback."""
from __future__ import annotations

import argparse
from hashlib import sha1, sha256
import json
from pathlib import Path
import re
import sys

PROFILE = "russian-1918-letter-and-terminal-sign-preview-v1"
LETTERS = "А-Яа-яЁёѢѣІіѲѳѴѵ"
MAPPING = dict(zip("ѢѣІіѲѳ", "ЕеИиФф", strict=True))
# Izhitsa, grammatical endings, prefixes, names and other editorial decisions
# are deliberately not normalized by this narrow diagnostic.
WORDS = re.compile(r"(?<!\w)[" + LETTERS + r"]+(?!\w)")
HISTORICAL = "ѢѣІіѲѳѴѵ"
GAP_SPAN = "70b6d55149d88008834542a9181d45fb4adf2baa48dae26741221ec16a1f379e"


def digest(text):
    return sha256(text.encode("utf-8")).hexdigest()


def preview(text):
    """Partial mechanical operation on complete Cyrillic tokens only."""
    counts = {"yat": 0, "decimal_i": 0, "fita": 0, "terminal_hard_sign": 0}

    def word(match):
        value = match.group()
        for key, pair in (("yat", "Ѣѣ"), ("decimal_i", "Іі"), ("fita", "Ѳѳ")):
            counts[key] += sum(c in pair for c in value)
        result = "".join(MAPPING.get(c, c) for c in value)
        if len(result) > 1 and result[-1] in "Ъъ":
            result = result[:-1]
            counts["terminal_hard_sign"] += 1
        return result

    return WORDS.sub(word, text), counts


def summarize(historical, modern=None):
    candidate, changes = preview(historical)
    return {
        "profile": PROFILE,
        "historical_body_sha256": digest(historical),
        "historical_characters": len(historical),
        "candidate_sha256": digest(candidate),
        "candidate_characters": len(candidate),
        "rule_counts": changes,
        "remaining_historical_letters": sum(c in HISTORICAL for c in candidate),
        "modern_body_sha256": digest(modern) if modern is not None else None,
        "modern_characters": len(modern) if modern is not None else None,
        "exact_candidate_equals_modern": candidate == modern if modern is not None else None,
    }


def selector_key(plans):
    if len(plans) != 1 or plans[0]["status"] != "LITERAL_CANDIDATE":
        return None
    return (plans[0]["candidate_scan_pages"], plans[0]["section_label_sha256"])


def capture(selectors, gap, rendered, query):
    from .kropotkin_body_preflight import EXPECTED, SCAN, observe
    from .kropotkin_revisions import TITLE, _identities
    from .kropotkin_rendered import extract

    modern_gap, historical_gap = gap["variants"]
    if (modern_gap["revision_id"], historical_gap["revision_id"]) != (3485514, 3485499):
        raise ValueError("gap revision drift")
    if (modern_gap["rendered_status"] != "EMPTY_BODY"
            or historical_gap["rendered_status"] != "RENDERED_CANDIDATE"
            or historical_gap["rendered_body_characters"] != 676
            or any(v["lexical_section"].get("raw_span_sha256") != GAP_SPAN
                   for v in (modern_gap, historical_gap))
            or not gap["accepted_page_and_modern_route_replayed"]):
        raise ValueError("accepted gap evidence drift")

    selector_rows = {row["title"]: row for row in selectors["routes"]}
    modern_rows = {row["title"]: row for row in rendered["routes"]}
    rows = []
    for number in (12, 13, 14):
        modern_title = f"{TITLE}/Приложение/{number}"
        historical_title = f"{modern_title}/ДО"
        modern_id = EXPECTED[modern_title]
        historical_id = 3485499 if number == 13 else None
        # Control historical routes are discovered once, then read by exact ID.
        # They are diagnostic observations, not accepted or frozen source pins.
        if historical_id is None:
            found = query({"action": "query", "prop": "revisions", "titles": historical_title,
                           "rvprop": "ids|timestamp|sha1"})
            historical_id = _identities(found, {historical_title: None})[0]["revision_id"]
        raw = query({"action": "query", "prop": "revisions", "revids": str(historical_id),
                     "rvprop": "ids|timestamp|sha1|content", "rvslots": "main"})
        identity = _identities(raw, {historical_title: historical_id})[0]
        page = raw["query"]["pages"][0]
        source = page["revisions"][0].get("slots", {}).get("main", {}).get("content")
        if (page.get("ns") != 0 or "redirect" in page or not isinstance(source, str)
                or sha1(source.encode("utf-8")).hexdigest() != identity["mediawiki_sha1"]):
            raise ValueError("historical route source identity drift")
        historical_plan = selector_key(observe(source)["literal_page_selectors"])
        modern_plan = selector_key(selector_rows[modern_title]["literal_page_selectors"])
        if number == 13 and digest(source) != historical_gap["source_sha256"]:
            raise ValueError("historical gap route digest drift")
        row = {"appendix": number, "modern_revision_id": modern_id,
               "historical_identity": identity, "historical_source_sha256": digest(source),
               "historical_pin_status": "ACCEPTED_GAP_REVISION" if number == 13 else "OBSERVED_CONTROL",
               "same_literal_selector": historical_plan is not None and historical_plan == modern_plan,
               "status": "SELECTOR_MISMATCH", "projection": None}
        rows.append(row)
        if not row["same_literal_selector"]:
            continue

        def read(title, revision):
            parsed = query({"action": "parse", "oldid": str(revision),
                            "prop": "text|revid|templates", "disableeditsection": "1"}).get("parse", {})
            if (parsed.get("title") != title or parsed.get("revid") != revision
                    or not isinstance(parsed.get("text"), str)
                    or not isinstance(parsed.get("templates"), list)):
                raise ValueError("rendered identity drift")
            status, body, notes, note_items = extract(parsed["text"])
            prefix = f"Страница:{SCAN}/"
            reported = {d["title"] for d in parsed["templates"] if d.get("ns") == 104}
            expected = {prefix + str(n) for n in modern_plan[0]}
            return status, body, reported == expected, note_items

        old_status, old_body, old_pages, old_notes = read(historical_title, historical_id)
        new_status, new_body, new_pages, new_notes = read(modern_title, modern_id)
        row.update(historical_render_status=old_status, modern_render_status=new_status,
                   historical_reported_scans_match=old_pages, modern_reported_scans_match=new_pages,
                   historical_note_items=old_notes, modern_note_items=new_notes)
        previous = modern_rows[modern_title]
        if (previous["revision_id"] != modern_id or previous["status"] != new_status
                or previous["body_sha256"] != (digest(new_body) if new_body is not None else None)):
            raise ValueError("modern rendered witness drift")
        if number == 13 and (old_body is None or digest(old_body) != historical_gap["rendered_body_sha256"]):
            raise ValueError("historical rendered witness drift")
        if not old_pages or not new_pages or old_body is None:
            row["status"] = "RENDER_OR_SCAN_MISMATCH"
            continue
        if number != 13 and new_body is None:
            row["status"] = "CONTROL_BODY_UNAVAILABLE"
            continue
        if number == 13 and new_body is not None:
            raise ValueError("modern gap no longer empty")
        row["projection"] = summarize(old_body, new_body)
        row["status"] = "PARTIAL_ORTHOGRAPHY_PREVIEW"

    controls = [r for r in rows if r["appendix"] != 13]
    exact = sum(r["projection"] is not None and r["projection"]["exact_candidate_equals_modern"] is True
                for r in controls)
    return {"schema": "scriptorium-kropotkin-orthography-controls-v1",
            "profile": PROFILE, "rows": rows, "control_count": len(controls),
            "exact_control_matches": exact,
            "candidate_for_review_only": True, "scan_collation_verified": False,
            "corpus_normalization_accepted": False, "composite_constructed": False,
            "body_frozen": False, "body_characters": None, "source_text_retained": False,
            "effective_page_graph_verified": False, "notes_boundary_verified": False,
            "fantlab_input_identity": "unknown", "m2_parity_admissible": False}


def main(argv=None):
    from .kropotkin_page_witnesses import FRONT_SELECTOR_SHA256
    from .wikisource_freeze import _api_query
    parser = argparse.ArgumentParser(description=__doc__)
    for name in ("selectors", "gap", "rendered", "output"):
        parser.add_argument("--" + name, type=Path, required=True)
    args = parser.parse_args(argv)
    try:
        raw = args.selectors.read_bytes()
        if sha256(raw).hexdigest() != FRONT_SELECTOR_SHA256:
            raise ValueError("selector receipt drift")
        report = capture(json.loads(raw), json.loads(args.gap.read_bytes()),
                         json.loads(args.rendered.read_bytes()), _api_query)
        with args.output.open("x", encoding="utf-8", newline="\n") as stream:
            json.dump(report, stream, ensure_ascii=False, sort_keys=True, indent=2)
            stream.write("\n")
    except Exception:
        print("Orthography control experiment failed; no verified receipt.", file=sys.stderr)
        return 2
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
