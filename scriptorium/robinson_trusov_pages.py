"""Resolve the pinned Trusov ProofreadPage dependency identities without prose.

The historical selection policy (latest Page revision no later than the carrier
save) is a *reconstruction*, not proof of MediaWiki's 2023 rendered state.
"""
from __future__ import annotations

import argparse
from hashlib import sha256
from html.parser import HTMLParser
import json
from pathlib import Path
import re
from typing import Callable, Mapping, Sequence

from .single_page_revision import _api_query
from .template_history import _parse_utc_timestamp

SCHEMA = "scriptorium-robinson-trusov-page-dependencies-v1"
WORK_ID = "defoe-robinson-trusov-1775-vol1-ru"
CARRIER_REVISION = 5041937
MAX_PAGES = 750
BATCH_SIZE = 8
_HEX = re.compile(r"[0-9a-f]{40}\Z")
_TAG = re.compile(r"<\s*pages\b[^>]*>", re.I)


class _PageTagParser(HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=False)
        self.tags: list[list[tuple[str, str | None]]] = []

    def handle_starttag(self, tag, attrs):
        if tag.lower() == "pages":
            self.tags.append(attrs)

    def handle_startendtag(self, tag, attrs):
        self.handle_starttag(tag, attrs)


def select_pages(wikitext: str) -> dict[str, object]:
    """Fail closed on unknown selectors, overlapping/implicit ranges or bad index."""
    parsed = _PageTagParser()
    parsed.feed(wikitext)
    if len(parsed.tags) != 1 or len(_TAG.findall(wikitext)) != 1:
        raise ValueError("expected exactly one ProofreadPage <pages> tag")
    pairs = parsed.tags[0]
    if len(pairs) != 3 or {k for k, _ in pairs} != {"index", "from", "to"}:
        raise ValueError("unsupported ProofreadPage selection attributes")
    attrs = dict(pairs)
    index = attrs["index"]
    if (not isinstance(index, str) or not (index.endswith(".djvu") or index.endswith(".pdf"))
        or len(index) > 200 or any(ch in index for ch in "\r\n<>|{}#")):
        raise ValueError("unrecognized ProofreadPage index identity")
    for key in ("from", "to"):
        if not isinstance(attrs[key], str) or not re.fullmatch(r"[1-9][0-9]{0,3}", attrs[key]):
            raise ValueError(f"invalid ProofreadPage {key} boundary")
    first, last = int(attrs["from"]), int(attrs["to"])
    if last < first or last - first + 1 > MAX_PAGES:
        raise ValueError("invalid or excessive ProofreadPage page interval")
    return {"index": index, "from": first, "to": last,
            "page_count": last - first + 1, "pages": list(range(first, last + 1))}


def _carrier_source(inventory: Mapping[str, object], query: Callable[..., dict]) -> tuple[str, dict]:
    if inventory.get("schema_version") != "scriptorium-robinson-revision-inventory-v1":
        raise ValueError("unrecognized exact-revision inventory")
    witnesses = inventory.get("witnesses")
    if not isinstance(witnesses, list):
        raise ValueError("missing witnesses")
    rows = [row for row in witnesses if isinstance(row, dict) and row.get("work_id") == WORK_ID]
    if len(rows) != 1:
        raise ValueError("missing or duplicated Trusov witness")
    row = rows[0]
    if row.get("revision_id") != CARRIER_REVISION:
        raise ValueError("Trusov oldid drift")
    payload = query({"action": "query", "prop": "revisions", "revids": str(CARRIER_REVISION),
                     "rvprop": "ids|timestamp|sha1|content", "rvslots": "main"})
    q = payload.get("query") if isinstance(payload, dict) and "error" not in payload else None
    pages = q.get("pages") if isinstance(q, dict) else None
    if not isinstance(pages, list) or len(pages) != 1 or not isinstance(pages[0], dict):
        raise ValueError("missing carrier page")
    page = pages[0]
    revisions = page.get("revisions")
    if not isinstance(revisions, list) or len(revisions) != 1 or not isinstance(revisions[0], dict):
        raise ValueError("missing carrier revision")
    rev = revisions[0]
    main = rev.get("slots", {}).get("main", {}) if isinstance(rev.get("slots"), dict) else {}
    source = main.get("content") if isinstance(main, dict) else None
    if not isinstance(source, str) or main.get("contentmodel", "wikitext") != "wikitext":
        raise ValueError("unexpected carrier source content model")
    identity = {"revision_id": rev.get("revid"), "page_id": page.get("pageid"),
                "title": page.get("title"), "timestamp_utc": rev.get("timestamp"),
                "mediawiki_sha1": rev.get("sha1"),
                "wikitext_sha256": sha256(source.encode("utf-8")).hexdigest(),
                "wikitext_utf8_bytes": len(source.encode("utf-8")),
                "wikitext_characters_including_spaces": len(source)}
    if any(identity[k] != row.get(k) for k in identity):
        raise ValueError("pinned Trusov carrier identity mismatch")
    if not _HEX.fullmatch(str(identity["mediawiki_sha1"])):
        raise ValueError("invalid carrier MediaWiki SHA-1")
    _parse_utc_timestamp(identity["timestamp_utc"])
    return source, identity


def _historical_pages(selection: Mapping[str, object], anchor: str,
                      query: Callable[..., dict]) -> list[dict[str, object]]:
    """Batch current identities, then resolve newer Pages singly at the anchor.

    MediaWiki rejects rvstart/rvlimit with multiple titles (rvmultpages).
    An already-old current Page needs no history query; a newer one does.
    """
    expected = [f"Страница:{selection['index']}/{num}" for num in selection["pages"]]
    results: dict[str, dict[str, object]] = {}
    anchor_dt = _parse_utc_timestamp(anchor)

    def one_identity(page: object, title: str) -> dict[str, object]:
        if not isinstance(page, dict) or page.get("title") != title or page.get("missing"):
            raise ValueError("unexpected/missing historical Page")
        revisions = page.get("revisions")
        if not isinstance(revisions, list) or len(revisions) != 1 or not isinstance(revisions[0], dict):
            raise ValueError("missing/duplicated Page revision")
        rev = revisions[0]
        revision_id, timestamp, provider_sha = rev.get("revid"), rev.get("timestamp"), rev.get("sha1")
        if (type(revision_id) is not int or revision_id <= 0
            or not isinstance(timestamp, str)
            or not isinstance(provider_sha, str) or not _HEX.fullmatch(provider_sha)
            or type(page.get("pageid")) is not int or page["pageid"] <= 0):
            raise ValueError("invalid historical Page revision identity")
        _parse_utc_timestamp(timestamp)
        return {"title": title, "page_id": page["pageid"],
                "revision_id": revision_id, "timestamp_utc": timestamp,
                "mediawiki_sha1": provider_sha}

    for off in range(0, len(expected), BATCH_SIZE):
        titles = expected[off:off + BATCH_SIZE]
        payload = query({"action": "query", "prop": "revisions", "titles": "|".join(titles),
                         "rvprop": "ids|timestamp|sha1", "redirects": "0"})
        q = payload.get("query") if isinstance(payload, dict) and "error" not in payload else None
        pages = q.get("pages") if isinstance(q, dict) else None
        if not isinstance(pages, list) or len(pages) != len(titles):
            raise ValueError("incomplete current Page inventory")
        pages_by_title = {}
        for page in pages:
            title = page.get("title") if isinstance(page, dict) else None
            if title not in titles or title in pages_by_title:
                raise ValueError("unexpected/duplicate current Page")
            pages_by_title[title] = page
        for title in titles:
            current = one_identity(pages_by_title[title], title)
            selected = current
            if _parse_utc_timestamp(current["timestamp_utc"]) > anchor_dt:
                historical = query({"action": "query", "prop": "revisions", "titles": title,
                                    "rvprop": "ids|timestamp|sha1", "rvlimit": "1",
                                    "rvstart": anchor, "rvdir": "older", "redirects": "0"})
                hq = historical.get("query") if isinstance(historical, dict) and "error" not in historical else None
                history_pages = hq.get("pages") if isinstance(hq, dict) else None
                if not isinstance(history_pages, list) or len(history_pages) != 1:
                    raise ValueError("historical single-Page query unavailable")
                selected = one_identity(history_pages[0], title)
                if selected["page_id"] != current["page_id"]:
                    raise ValueError("historical Page identity changed")
            if _parse_utc_timestamp(selected["timestamp_utc"]) > anchor_dt:
                raise ValueError("historical Page revision newer than anchor")
            if title in results:
                raise ValueError("duplicate Page title in selected graph")
            results[title] = selected
    if set(results) != set(expected) or len({v["revision_id"] for v in results.values()}) != len(expected):
        raise ValueError("historical Page graph incomplete/duplicate")
    return [{"page_sequence": n, **results[t]} for n, t in zip(selection["pages"], expected)]


def capture(inventory: Mapping[str, object], *, query: Callable[..., dict] = _api_query) -> dict:
    source, identity = _carrier_source(inventory, query)
    selection = select_pages(source)
    records = _historical_pages(selection, identity["timestamp_utc"], query)
    result = {"schema_version": SCHEMA, "candidate_id": WORK_ID,
              "carrier": identity,
              "selection": {k: v for k, v in selection.items() if k != "pages"},
              "selection_policy": "latest_page_revision_at_or_before_carrier_save",
              "historical_render_equivalence_proven": False,
              "page_revision_identities_frozen": True,
              "pages": records, "source_text_committed": False,
              "literary_body_sha256": None, "literary_characters_including_spaces": None,
              "corpus_threshold_verified": False, "admitted_for_calibration": False,
              "fantlab_input_identity": "UNKNOWN", "m2_parity_admissible": False}
    validate(result)
    return result


def validate(result: Mapping[str, object]) -> None:
    if result.get("schema_version") != SCHEMA or result.get("candidate_id") != WORK_ID:
        raise ValueError("unsupported Trusov graph")
    if set(result) != {"admitted_for_calibration", "candidate_id", "carrier",
                          "corpus_threshold_verified", "fantlab_input_identity",
                          "historical_render_equivalence_proven", "literary_body_sha256",
                          "literary_characters_including_spaces", "m2_parity_admissible",
                          "page_revision_identities_frozen", "pages", "schema_version",
                          "selection", "selection_policy", "source_text_committed"}:
        raise ValueError("unexpected source-free graph shape or prose leakage")
    for key, value in {"historical_render_equivalence_proven": False,
                       "source_text_committed": False,
                       "literary_body_sha256": None, "literary_characters_including_spaces": None,
                       "corpus_threshold_verified": False, "admitted_for_calibration": False,
                       "fantlab_input_identity": "UNKNOWN", "m2_parity_admissible": False}.items():
        if result.get(key, "ABSENT") != value:
            raise ValueError(f"invalid scientific gate: {key}")
    if result.get("selection_policy") != "latest_page_revision_at_or_before_carrier_save":
        raise ValueError("unknown historical resolution policy")
    if result.get("page_revision_identities_frozen") is not True:
        raise ValueError("unfrozen historical Page graph")
    carrier, selection, records = result.get("carrier"), result.get("selection"), result.get("pages")
    if not isinstance(carrier, dict) or carrier.get("revision_id") != CARRIER_REVISION:
        raise ValueError("carrier changed")
    if not isinstance(selection, dict) or set(selection) != {"index", "from", "to", "page_count"}:
        raise ValueError("selection keys invalid")
    if not isinstance(records, list) or not records:
        raise ValueError("Page graph missing")
    reconstructed = select_pages(f'<pages index="{selection["index"]}" from="{selection["from"]}" to="{selection["to"]}" />')
    if reconstructed["page_count"] != selection["page_count"] or len(records) != selection["page_count"]:
        raise ValueError("Page graph/selector count mismatch")
    anchor = _parse_utc_timestamp(carrier.get("timestamp_utc"))
    allowed = {"page_sequence", "title", "page_id", "revision_id", "timestamp_utc", "mediawiki_sha1"}
    for n, row in zip(reconstructed["pages"], records):
        if not isinstance(row, dict) or set(row) != allowed:
            raise ValueError("Page revision shape drift or prose leakage")
        if row.get("page_sequence") != n or row.get("title") != f"Страница:{selection['index']}/{n}":
            raise ValueError("Page order or index mismatch")
        if type(row.get("revision_id")) is not int or row["revision_id"] <= 0:
            raise ValueError("invalid Page revision")
        if type(row.get("page_id")) is not int or row["page_id"] <= 0:
            raise ValueError("invalid Page identity")
        if not _HEX.fullmatch(str(row.get("mediawiki_sha1"))):
            raise ValueError("invalid provider digest")
        if _parse_utc_timestamp(row.get("timestamp_utc")) > anchor:
            raise ValueError("Page revision newer than carrier")
    if len({r["revision_id"] for r in records}) != len(records):
        raise ValueError("duplicate Page revision")
    if len({r["page_id"] for r in records}) != len(records):
        raise ValueError("duplicate Page identity")



def verify_frozen_graph(manifest: Path, receipt_file: Path) -> dict:
    """Offline, exact-byte verification of the source-free historical graph.

    A verified graph proves selected revision identities, NOT historical render
    equivalence, whole-book extraction, print collation, 300k size or parity.
    """
    raw = manifest.read_bytes()
    graph = json.loads(raw)
    validate(graph)
    receipt = json.loads(receipt_file.read_text(encoding="utf-8"))
    if (receipt.get("schema_version") != "scriptorium-robinson-trusov-page-graph-receipt-v1"
        or receipt.get("candidate_id") != WORK_ID
        or receipt.get("graph_in_git") is not True):
        raise ValueError("unrecognized or uncommitted Page graph receipt")
    if (sha256(raw).hexdigest() != receipt.get("full_source_free_graph_sha256")
        or len(raw) != receipt.get("full_graph_size_bytes")):
        raise ValueError("source-free Page graph digest/size mismatch")
    if (graph["carrier"]["revision_id"] != receipt.get("carrier_oldid")
        or graph["carrier"]["wikitext_sha256"] != receipt.get("carrier_wikitext_sha256")
        or graph["carrier"]["timestamp_utc"] != receipt.get("carrier_timestamp_utc")
        or graph["selection"]["index"] != receipt.get("proofreadpage_index")
        or [graph["selection"]["from"], graph["selection"]["to"]] != receipt.get("page_range_inclusive")
        or len(graph["pages"]) != receipt.get("page_revision_count")
        or len({p["page_id"] for p in graph["pages"]}) != receipt.get("distinct_page_ids")
        or graph["selection_policy"] != receipt.get("historical_selection_policy")):
        raise ValueError("source-free Page graph receipt identity mismatch")
    for selected, expected in ((graph["pages"][0], receipt.get("first_page")),
                               (graph["pages"][-1], receipt.get("last_page"))):
        if not isinstance(expected, dict) or any(
            selected.get(src) != expected.get(dst)
            for src, dst in (("page_sequence", "sequence"), ("page_id", "page_id"),
                             ("revision_id", "oldid"), ("mediawiki_sha1", "mediawiki_sha1"))
        ):
            raise ValueError("Page graph receipt boundary mismatch")
    return graph


def main(argv: Sequence[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    sub = parser.add_subparsers(dest="command", required=True)
    p = sub.add_parser("capture")
    p.add_argument("--inventory", type=Path, required=True)
    p.add_argument("--output", type=Path, required=True)
    p = sub.add_parser("replay")
    p.add_argument("--inventory", type=Path, required=True)
    p.add_argument("--manifest", type=Path, required=True)
    p = sub.add_parser("verify")
    p.add_argument("--manifest", type=Path, required=True)
    p.add_argument("--receipt", type=Path, required=True)
    args = parser.parse_args(argv)
    if args.command == "verify":
        verified = verify_frozen_graph(args.manifest, args.receipt)
        print(f"Verified {len(verified['pages'])} frozen source-free Page identities; literary body NOT_RUN")
        return 0
    inventory = json.loads(args.inventory.read_text(encoding="utf-8"))
    if args.command == "capture":
        if args.inventory.resolve() == args.output.resolve():
            parser.error("refuse to overwrite inventory")
        result = capture(inventory)
        args.output.parent.mkdir(parents=True, exist_ok=True)
        with args.output.open("x", encoding="utf-8") as out:
            out.write(json.dumps(result, ensure_ascii=False, indent=2, sort_keys=True) + "\n")
    else:
        saved = json.loads(args.manifest.read_text(encoding="utf-8"))
        validate(saved)
        if capture(inventory) != saved:
            raise ValueError("historical Page revisions differ from saved graph")
        print("Historical Page identity graph matched, render and body remain unverified")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
