"""Capture source-free Page revision witnesses for the accepted partial scan union."""
from __future__ import annotations

import argparse
from hashlib import sha1, sha256
from html.parser import HTMLParser
import json
from pathlib import Path
import re
import sys

from .kropotkin_body_preflight import SCAN, REVISION_IDS
from .kropotkin_revisions import _identities
from .wikisource_freeze import _api_query

# Independently accepted #630: 27 literal routes, not full book coverage.
PAGES = tuple(range(23, 348))
BATCH_SIZE = 4
SCHEMA = "scriptorium-kropotkin-page-witnesses-v1"

# Accepted #631, run 45495675600, artifact 14967284843; scan order 23–347.
# Full source-free JSON SHA-256 (not ZIP hash), including final newline.
ACCEPTED_RECEIPT_SHA256 = "de958cdeae0ed4d7b9e4f6adbc5f78b0a3b8761fa767b67abeb40d3ed961e303"
PINNED_PAGE_IDS = (
    5779450, 5718718, 3374375, 3374376, 3374377, 3374423, 3374424, 3374425, 3374426, 3374475,
    3374476, 3374477, 3374478, 3374479, 3374480, 3374481, 3374482, 3374483, 3374526, 3374527,
    3374528, 3374529, 3374530, 3374531, 3374532, 3374533, 3374534, 3374535, 3374536, 5830063,
    3374537, 3374538, 3374539, 3374540, 3374541, 3374542, 3374543, 3374544, 3374545, 3374546,
    3374547, 3374548, 3374549, 3374550, 3374551, 3374552, 3374553, 3374554, 3374555, 3374556,
    3374557, 3374558, 3374559, 3374560, 3374561, 3374562, 3374563, 3374564, 3374565, 3374566,
    3374567, 3374568, 3374569, 3374570, 3374571, 3374572, 3374573, 3374590, 3374591, 3374592,
    3374593, 3374594, 3374595, 3374596, 5779457, 3374598, 3374599, 3374226, 3479119, 3374228,
    3374229, 3374230, 3374231, 3374232, 3374233, 3374234, 3374235, 3374236, 3374237, 3374238,
    3374239, 3374240, 3374241, 3374242, 3374243, 3374244, 3374245, 3374246, 3374247, 3374248,
    3374249, 3374250, 3374251, 3374252, 3374253, 3374254, 3374255, 3374256, 3374257, 3374258,
    3374259, 3374260, 3374261, 3479121, 3374263, 3374279, 3374280, 3374281, 3374282, 3374283,
    3374284, 3374285, 3374286, 4050590, 4050588, 3374289, 3374290, 3479122, 3374292, 3374293,
    3374294, 3374295, 4050597, 4050602, 3479123, 3479125, 3374300, 3374301, 3479126, 3479127,
    3374304, 3374305, 3374306, 3374307, 3374308, 3374309, 3374310, 3374311, 5811030, 3374312,
    3374313, 3374314, 3374315, 3374316, 3374317, 3374318, 3374319, 3374320, 3374321, 3374322,
    3374328, 4050748, 3374330, 3374331, 3374332, 3374333, 3374334, 3374335, 3374336, 3374337,
    5718716, 3374339, 3374340, 3374341, 3374342, 3374343, 3374344, 3374345, 3374346, 3374347,
    5799626, 3374348, 3374349, 3374350, 3374351, 3374352, 3374353, 3374354, 3374355, 3374356,
    5718717, 3374358, 3374359, 3374360, 3374361, 3374362, 3374363, 3374364, 3374365, 3374366,
    3374367, 3374368, 3374369, 3374370, 3374371, 3374372, 3374378, 3374379, 3374380, 3374381,
    3374382, 3374383, 3374384, 5360556, 5771009, 3374387, 3374388, 3374389, 3374390, 3374391,
    3374392, 3374393, 3374394, 3374395, 3374396, 3374397, 3374398, 3374399, 3374400, 3374401,
    3374402, 3374403, 3374404, 3374405, 3374406, 3374407, 3374408, 3374409, 3374410, 3374411,
    3374412, 3374413, 3374414, 3374415, 3479139, 3374417, 3374418, 3374419, 3374420, 3374421,
    3374422, 5832287, 3374428, 3374429, 3374430, 3374431, 3374432, 3374433, 3374434, 3374435,
    3374436, 3374437, 3374438, 3374439, 3374440, 3374441, 3374443, 3374444, 3374445, 3374446,
    3374447, 3374448, 3374449, 3374450, 3374451, 5351136, 3479145, 3479146, 3374456, 3374457,
    3374458, 3479147, 3374460, 3374461, 3374462, 3374463, 3374464, 3374465, 5789420, 5828129,
    4051954, 3479154, 5788614, 3374471, 3479158, 3374473, 5797878, 3374484, 5829572, 5779452,
    5800987, 3374488, 5814090, 3374490, 3374491, 5810875, 4052171, 3374494, 3479171, 3479172,
    3374497, 4051616, 5800299, 5792236, 3374501, 3374502, 3479179, 5791473, 5833070, 3374506,
    3374507, 3479185, 3374509, 3374510, 5779455,
)


# #633 accepted candidate additions; public Page permanent links observed 2026-11-25.
FRONT_PAGES = (5, *range(11, 23))
FRONT_IDS = (3479106, 5825141, 3479109, 3479110, 3374274, 3374275,
             3374276, 3374277, 3374278, 3374324, 3374325, 3374326, 3374327)
FRONT_SELECTOR_SHA256 = "b5a5900fd912365e6ff6f52e6cbbf62d047465ed52f34661a7f27611ad2c7348"


class _Markers(HTMLParser):
    """Lexical observation only, not proof of effective section transclusion."""

    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.markers = []
        self.unresolved = 0

    def handle_starttag(self, tag, attrs):
        if tag != "section":
            return
        if len(attrs) != 1:
            self.unresolved += 1
            return
        kind, label = attrs[0]
        if (kind not in {"begin", "end"} or not isinstance(label, str)
                or not label.strip() or len(label) > 256
                or any(c in label for c in "{}<>|")
                or any(ord(c) < 32 for c in label)):
            self.unresolved += 1
            return
        self.markers.append({"kind": kind, "label_sha256":
                             sha256(label.encode("utf-8")).hexdigest()})


def observe(source):
    raw = source.encode("utf-8")
    parser = _Markers()
    parser.feed(source)
    parser.close()
    return {
        "wikitext_sha256": sha256(raw).hexdigest(),
        "wikitext_utf8_bytes": len(raw),
        "literal_section_markers": parser.markers,
        "unresolved_section_tags": parser.unresolved,
        "raw_section_openings": len(re.findall(r"<\s*section\b", source, re.I)),
        "raw_nowiki_openings": len(re.findall(r"<\s*nowiki\b", source, re.I)),
        "raw_template_openings": source.count("{{"),
        "raw_ref_openings": len(re.findall(r"<\s*ref\b", source, re.I)),
    }


def _capture_rows(query, scans, pins, reserved):
    if pins and (set(pins) != set(scans) or len(set(pins.values())) != len(scans)):
        raise ValueError("invalid pinned Page revision inventory")
    rows = []
    seen = set(reserved)
    for offset in range(0, len(scans), BATCH_SIZE):
        expected = {f"Страница:{SCAN}/{n}": n
                    for n in scans[offset:offset + BATCH_SIZE]}
        revisions = {title: pins.get(n) for title, n in expected.items()}
        selector = ({"revids": "|".join(map(str, revisions.values()))}
                    if pins else {"titles": "|".join(expected)})
        payload = query({"action": "query", "prop": "revisions", **selector,
                         "rvprop": "ids|timestamp|sha1|content", "rvslots": "main"})
        identities = _identities(payload, revisions)
        pages = {p["title"]: p for p in payload["query"]["pages"]}
        for row in identities:
            rid = row["revision_id"]
            if rid in seen:
                raise ValueError("duplicate Page revision identity")
            seen.add(rid)
            page = pages[row["title"]]
            if page.get("ns") != 104 or "redirect" in page:
                raise ValueError("unexpected Page namespace or redirect")
            rev = page["revisions"][0]
            source = rev.get("slots", {}).get("main", {}).get("content")
            if not isinstance(source, str) or not source:
                raise ValueError("missing Page source")
            if sha1(source.encode("utf-8")).hexdigest() != row["mediawiki_sha1"]:
                raise ValueError("Page source digest mismatch")
            rows.append({**row, "scan_page": expected[row["title"]], **observe(source)})
    return rows


def capture(query=_api_query, *, pinned=False):
    pins = dict(zip(PAGES, PINNED_PAGE_IDS, strict=True)) if pinned else {}
    rows = _capture_rows(query, PAGES, pins, REVISION_IDS)
    return {
        "schema": SCHEMA,
        "candidate_id": "kropotkin-mutual-aid-baturinsky-1907-ru",
        "selector_acceptance_pr": 630,
        "selector_receipt_sha256": "264c6cfc876c5e03d8948f19d96c19911db300349b18dc20621bc667f84a05c7",
        "candidate_scan_pages": list(PAGES),
        "page_count": len(rows),
        "pages": rows,
        "unresolved_route_count": 2,
        "complete_page_inventory": False,
        "effective_page_graph_verified": False,
        "transclusion_dependencies_frozen": False,
        "notes_boundary_verified": False,
        "body_frozen": False,
        "body_characters": None,
        "source_text_retained": False,
        "fantlab_input_identity": "unknown",
        "m2_parity_admissible": False,
    }


def capture_frontmatter(query=_api_query):
    """Capture the 13 public-link pins separately; never alter the accepted v1 receipt."""
    pins = dict(zip(FRONT_PAGES, FRONT_IDS, strict=True))
    if set(FRONT_PAGES) & set(PAGES) or sorted((*FRONT_PAGES, *PAGES)) != [5, *range(11, 348)]:
        raise ValueError("front-matter inventory differs from accepted v3 selectors")
    rows = _capture_rows(query, FRONT_PAGES, pins, (*REVISION_IDS, *PINNED_PAGE_IDS))
    return {
        "schema": "scriptorium-kropotkin-frontmatter-witnesses-v1",
        "candidate_id": "kropotkin-mutual-aid-baturinsky-1907-ru",
        "selector_acceptance_pr": 633,
        "selector_receipt_sha256": FRONT_SELECTOR_SHA256,
        "partial_receipt_sha256": ACCEPTED_RECEIPT_SHA256,
        "candidate_scan_pages": list(FRONT_PAGES),
        "page_count": len(rows),
        "pages": rows,
        "combined_candidate_scan_count": len(FRONT_PAGES) + len(PAGES),
        "effective_page_graph_verified": False,
        "transclusion_dependencies_frozen": False,
        "notes_boundary_verified": False,
        "body_frozen": False,
        "body_characters": None,
        "source_text_retained": False,
        "fantlab_input_identity": "unknown",
        "m2_parity_admissible": False,
    }


def serialize_receipt(result, *, require_accepted=False):
    serialized = json.dumps(result, ensure_ascii=False, sort_keys=True, indent=2) + "\n"
    if require_accepted and sha256(serialized.encode("utf-8")).hexdigest() != ACCEPTED_RECEIPT_SHA256:
        raise ValueError("pinned Page receipt differs from accepted evidence")
    return serialized


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path, required=True)
    mode = parser.add_mutually_exclusive_group()
    mode.add_argument("--frontmatter", action="store_true",
                      help="Fetch exact front-matter Page pins and emit a separate receipt")
    mode.add_argument("--replay", action="store_true",
                        help="Fetch exact accepted revisions and require the accepted receipt digest")
    args = parser.parse_args(argv)
    try:
        result = capture_frontmatter() if args.frontmatter else capture(pinned=args.replay)
        serialized = serialize_receipt(result, require_accepted=args.replay)
        with args.output.open("x", encoding="utf-8", newline="\n") as stream:
            stream.write(serialized)
    except Exception:
        print("Partial Kropotkin Page capture failed; no verified receipt.", file=sys.stderr)
        return 2
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
