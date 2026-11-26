"""Replay only the three scan-observed closing seams of the 1775 Trusov Page graph.

The two literal VAR arguments are inspected separately, not rendered. Never
emit a word, continuation, or digest of a short span. Full body remains unknown.
"""
from __future__ import annotations

import argparse
from hashlib import sha256
from enum import Enum
import json
from pathlib import Path
import re

from .robinson_trusov_content import transclusion_input, verify_receipt
from .robinson_trusov_pages import verify_frozen_graph
from .single_page_revision import _api_query

SCHEMA = "scriptorium-trusov-closing-seams-v1"
PINS = {148: 4958660, 149: 4958661, 150: 4958663, 151: 4958664}
VAR = re.compile(r"\{\{ВАР\|([^{}|]*)\|([^{}|]*)\}\}")
LEADING = re.compile(r"\A\s*<noinclude>([^<>]*)</noinclude>", re.I)
TRAILING = re.compile(r"<noinclude>([^<>]*)</noinclude>\s*\Z", re.I)
FIRST_WORD = re.compile(r"\A\s*([^\W\d_]+)")
LAST_WORD = re.compile(r"([^\W\d_]+)[^\w]*\Z")


_WRAPPER_TOKENS = re.compile(
    r"<!--[\s\S]*?-->|<!--|-->|{{\s*ВАР\s*\||"
    r"</?noinclude\b[^>]*>|{{|}}|[{}|]", re.I
)


def wrapper_signature(value):
    """Bounded delimiter/comment order only; no literal text or span hashes."""
    events = []
    for match in _WRAPPER_TOKENS.finditer(value):
        if len(events) == 32:
            return {"events": events, "truncated": True}
        token = match.group()
        if token.startswith("<!--") and token.endswith("-->"):
            events.append({"kind": "COMMENT", "braces": token.count("{") + token.count("}"),
                           "pipes": token.count("|")})
        elif token.startswith("{{") and token.endswith("|"):
            events.append("VAR_OPEN_EXACT" if token == "{{ВАР|" else "VAR_OPEN_NONEXACT")
        elif token.lower().startswith("<noinclude"):
            events.append("NOINCLUDE_OPEN")
        elif token.lower().startswith("</noinclude"):
            events.append("NOINCLUDE_CLOSE")
        else:
            events.append({"{{": "OTHER_OPEN", "}}": "CLOSE", "{": "LEFT_BRACE",
                           "}": "RIGHT_BRACE", "|": "PIPE", "<!--": "COMMENT_OPEN",
                           "-->": "COMMENT_CLOSE"}[token])
    return {"events": events, "truncated": False}


def digest(text):
    return sha256(text.encode("utf-8")).hexdigest()


def literal_branches(raw):
    """Accept exactly one literal VAR in the scoped Page, with no other body."""
    matches = list(VAR.finditer(raw))
    if len(matches) != 1:
        raise ValueError("closing Page VAR shape differs")
    match = matches[0]
    if transclusion_input(raw).strip() != transclusion_input(match.group()).strip():
        raise ValueError("closing Page has unaccounted outer scope")
    return match.groups()


def edge_scope(branch, edge):
    """Isolate one plain noinclude at its declared edge; refuse other spans."""
    match = (LEADING if edge == "leading" else TRAILING).search(branch)
    if match is None:
        raise ValueError("expected closing edge noinclude missing")
    token = match.group(1).strip()
    if not token or len(token) > 32 or not all(c.isalpha() for c in token):
        raise ValueError("closing edge is not a short letter-only continuation")
    body = transclusion_input(branch)
    # Require precisely the expected edge removal; an unrelated hidden note
    # must not silently disappear in the scoped branch.
    if body != branch[:match.start()].lstrip() + branch[match.end():].rstrip():
        if body.strip() != (branch[:match.start()] + branch[match.end():]).strip():
            raise ValueError("additional closing edge scope")
    if re.search(r"</?noinclude\b", branch[:match.start()] + branch[match.end():], re.I):
        raise ValueError("additional closing noinclude span")
    if any(c in body for c in "<>{}[]") or "''" in body:
        raise ValueError("closing branch has unresolved markup")
    return token, body


def plain_branch(branch):
    if any(c in branch for c in "<>{}[]") or "''" in branch or not branch.strip():
        raise ValueError("unexpected closing branch markup")
    return branch


def diagnose(left, right, *, edge, letters):
    """Check exact ownership in one orthography, without publishing the token."""
    if edge == "trailing":
        token, left_body = edge_scope(left, edge)
        # The next branch may have an independent leading span only when
        # explicitly authorized by the caller; here this seam requires none.
        right_body = plain_branch(right)
    elif edge == "leading":
        token, right_body = edge_scope(right, edge)
        # The preceding Page can have its own leading continuation from
        # a different seam (Page 150); exclude it only via the same strict gate.
        left_body = edge_scope(left, "leading")[1] if LEADING.match(left) else plain_branch(left)
    else:
        raise ValueError("unknown closing seam direction")
    first, last = FIRST_WORD.match(right_body), LAST_WORD.search(left_body)
    if first is None or last is None:
        raise ValueError("closing seam has no lexical boundary")
    left_word, right_word = last.group(1), first.group(1)
    if edge == "trailing":
        owner_matches = right_word == token
        duplicate = left_word == token
    else:
        owner_matches = len(left_word) > len(token) and left_word.endswith(token)
        duplicate = right_word.startswith(token)
    if len(token) != letters or not owner_matches or duplicate:
        raise ValueError("closing seam count or ownership differs from scan observation")
    return {"excluded_letters": len(token), "excluded_edge": edge,
            "owner": "right" if edge == "trailing" else "left",
            "owner_matches": True, "duplicate_at_other_boundary": False}



# The pinned Page 151 has a noncanonical VAR opener and exactly two
# delimiter-free branch comments, in opposite order around the leading
# noinclude spans. This is a local seam experiment, not a VAR renderer.
_PAGE151_VAR = re.compile(
    r"(?P<opener>\{\{[ \t\r\n]*[Вв][Аа][Рр][ \t\r\n]*\|)"
    r"(?P<left>[^{}|]*)\|(?P<right>[^{}|]*)\}\}"
)
_PAGE151_COMMENT = re.compile(r"<!--[^{}|<>]*?-->")
_PAGE151_COMMENT_EVENT = {"kind": "COMMENT", "braces": 0, "pipes": 0}
_PAGE151_RAW_EVENTS = [
    "NOINCLUDE_OPEN", "NOINCLUDE_CLOSE", "VAR_OPEN_NONEXACT",
    "NOINCLUDE_OPEN", "NOINCLUDE_CLOSE", _PAGE151_COMMENT_EVENT,
    "PIPE", _PAGE151_COMMENT_EVENT, "NOINCLUDE_OPEN", "NOINCLUDE_CLOSE",
    "CLOSE", "NOINCLUDE_OPEN", _PAGE151_COMMENT_EVENT, "NOINCLUDE_CLOSE",
]
_PAGE151_SCOPED_EVENTS = [
    "VAR_OPEN_NONEXACT", _PAGE151_COMMENT_EVENT, "PIPE",
    _PAGE151_COMMENT_EVENT, "CLOSE",
]


class _Page151Reason(str, Enum):
    RAW_ORDER = "PAGE151_RAW_ORDER"
    SCOPED_ORDER = "PAGE151_SCOPED_ORDER"
    OPENER_GRAMMAR = "PAGE151_OPENER_GRAMMAR"
    OPENER_VARIANT = "PAGE151_OPENER_VARIANT"
    OUTER_SCOPE = "PAGE151_OUTER_SCOPE"
    COMMENT_SHAPE = "PAGE151_COMMENT_SHAPE"
    LEADING_UNCLASSIFIED = "PAGE151_LEADING_UNCLASSIFIED"
    LEADING_PREFIX_NONSPACE = "PAGE151_LEADING_PREFIX_NONSPACE"
    LEADING_TAG_VARIANT = "PAGE151_LEADING_TAG_VARIANT"
    LEADING_BODY_MARKUP = "PAGE151_LEADING_BODY_MARKUP"
    COMMENT_OVERLAP = "PAGE151_COMMENT_OVERLAP"
    COMMENT_GAP = "PAGE151_COMMENT_GAP"
    COMMENT_PREFIX_NONSPACE = "PAGE151_COMMENT_PREFIX_NONSPACE"
    EDGE_SCOPE = "PAGE151_EDGE_SCOPE"
    COMMENT_PROJECTION = "PAGE151_COMMENT_PROJECTION"


class _Page151Refusal(ValueError):
    """Only fixed reason codes and a literal branch index may escape."""
    def __init__(self, reason: _Page151Reason, branch_index=None, *, fragment=None):
        self.reason = reason
        self.branch_index = branch_index
        # Fixed character categories only; never preserve the fragment.
        self.fragment_counts = None if fragment is None else {
            "whitespace": sum(c.isspace() for c in fragment),
            "letters": sum(c.isalpha() for c in fragment),
            "digits": sum(c.isdigit() for c in fragment),
            "apostrophes": fragment.count("'"),
            "angle_brackets": fragment.count("<") + fragment.count(">"),
            "other": sum(not (c.isspace() or c.isalpha() or c.isdigit()
                              or c in "'<>") for c in fragment),
        }
        super().__init__(reason.value)


def _page151_leading_refusal(branch, index):
    """Classify a strict leading miss without accepting alternative markup."""
    observed = re.search(
        r"(?P<open><noinclude\b[^>]*>)(?P<body>.*?)"
        r"(?P<close></noinclude\b[^>]*>)", branch, re.I | re.S,
    )
    if observed is None:
        return _Page151Refusal(_Page151Reason.LEADING_UNCLASSIFIED, index)
    prefix = branch[:observed.start()]
    if prefix.strip():
        return _Page151Refusal(_Page151Reason.LEADING_PREFIX_NONSPACE, index,
                               fragment=prefix)
    if (observed.group("open").lower() != "<noinclude>"
            or observed.group("close").lower() != "</noinclude>"):
        return _Page151Refusal(_Page151Reason.LEADING_TAG_VARIANT, index)
    body = observed.group("body")
    if "<" in body or ">" in body:
        return _Page151Refusal(_Page151Reason.LEADING_BODY_MARKUP, index,
                               fragment=body)
    return _Page151Refusal(_Page151Reason.LEADING_UNCLASSIFIED, index)


def page151_branches(raw):
    """Candidate seam-only projection of the observed pinned leaf shape.

    Capture checks the original bytes first. Inspect the actual bounded
    opener token at runtime: only case and ASCII whitespace may differ.
    Remove one comment at each branch's leading continuation boundary,
    never arbitrary interior comments or general template markup.
    """
    if wrapper_signature(raw) != {"events": _PAGE151_RAW_EVENTS, "truncated": False}:
        raise _Page151Refusal(_Page151Reason.RAW_ORDER)
    scoped = transclusion_input(raw)
    if wrapper_signature(scoped) != {"events": _PAGE151_SCOPED_EVENTS, "truncated": False}:
        raise _Page151Refusal(_Page151Reason.SCOPED_ORDER)
    matches = list(_PAGE151_VAR.finditer(raw))
    if len(matches) != 1:
        raise _Page151Refusal(_Page151Reason.OPENER_GRAMMAR)
    match = matches[0]
    opener = match.group("opener")
    if opener == "{{ВАР|" or len(opener) > 32:
        raise _Page151Refusal(_Page151Reason.OPENER_VARIANT)
    if scoped.strip() != transclusion_input(match.group()).strip():
        raise _Page151Refusal(_Page151Reason.OUTER_SCOPE)
    cleaned = []
    for i, branch in enumerate((match.group("left"), match.group("right"))):
        comments = list(_PAGE151_COMMENT.finditer(branch))
        if len(comments) != 1:
            raise _Page151Refusal(_Page151Reason.COMMENT_SHAPE, i)
        comment = comments[0]
        if i == 0:
            leading = LEADING.match(branch)
            if leading is None:
                raise _page151_leading_refusal(branch, i)
            if comment.start() < leading.end():
                raise _Page151Refusal(_Page151Reason.COMMENT_OVERLAP, i)
            gap = branch[leading.end():comment.start()]
            if gap.strip():
                raise _Page151Refusal(_Page151Reason.COMMENT_GAP, i, fragment=gap)
        else:
            prefix = branch[:comment.start()]
            if prefix.strip():
                raise _Page151Refusal(_Page151Reason.COMMENT_PREFIX_NONSPACE, i,
                                      fragment=prefix)
            tail = branch[comment.end():]
            if LEADING.match(tail) is None:
                raise _page151_leading_refusal(tail, i)
        candidate = branch[:comment.start()] + branch[comment.end():]
        # Validate all other markup and continuation rules independently.
        try:
            edge_scope(candidate, "leading")
        except ValueError:
            raise _Page151Refusal(_Page151Reason.EDGE_SCOPE, i) from None
        try:
            same_projection = transclusion_input(candidate) == (
                transclusion_input(branch).replace(comment.group(), "", 1)
            )
        except ValueError:
            raise _Page151Refusal(_Page151Reason.COMMENT_PROJECTION, i) from None
        if not same_projection:
            raise _Page151Refusal(_Page151Reason.COMMENT_PROJECTION, i)
        cleaned.append(candidate)
    return tuple(cleaned), opener


def diagnose_pages(raws):
    if set(raws) != set(PINS):
        raise ValueError("closing Page coverage incomplete")
    branches, refusals = {}, []
    for n in sorted(raws):
        raw = raws[n]
        try:
            try:
                branches[n] = literal_branches(raw)
            except ValueError:
                if n != 151:
                    raise
                branches[n], _ = page151_branches(raw)
        except ValueError as refusal:
            # Report only fixed structural counts from already pinned inputs.
            # Never log literal arguments, template names other than VAR, or
            # short-span digests. A refusal still fails the hosted replay.
            scoped = transclusion_input(raw)
            def counts(value):
                return {
                    "var_starts": len(re.findall(r"\{\{\s*ВАР\s*\|", value)),
                    "literal_var_matches": len(list(VAR.finditer(value))),
                    "template_opens": value.count("{{"),
                    "template_closes": value.count("}}"),
                    "pipes": value.count("|"),
                    "noinclude_opens": len(re.findall(r"<noinclude\b", value, re.I)),
                    "includeonly_opens": len(re.findall(r"<includeonly\b", value, re.I)),
                    "html_comments": value.count("<!--"),
                }
            refusals.append({
                "page_sequence": n, "revision_id": PINS[n],
                "reason": ("VAR_MATCH_COUNT" if len(list(VAR.finditer(raw))) != 1
                           else "OUTER_SCOPE_OR_INCLUSION_REFUSED"),
                "raw_structure": counts(raw),
                "transclusion_structure": counts(scoped),
            })
            # Page 151 is the only observed refusal on the prior exact head.
            # Do not interpret or remove comments or repair delimiters here.
            if n == 151:
                refusals[-1]["raw_wrapper_signature"] = wrapper_signature(raw)
                refusals[-1]["transclusion_wrapper_signature"] = wrapper_signature(scoped)
                # A noncanonical opener necessarily misses the strict regex;
                # retain the actual specialized failure instead of relabeling it.
                if isinstance(refusal, _Page151Refusal):
                    refusals[-1]["page151_reason"] = refusal.reason.value
                    refusals[-1]["branch_index"] = refusal.branch_index
                    if refusal.fragment_counts is not None:
                        refusals[-1]["fragment_counts"] = refusal.fragment_counts
                    if "VAR_OPEN_NONEXACT" in refusals[-1]["raw_wrapper_signature"]["events"]:
                        refusals[-1]["reason"] = refusal.reason.value
    if refusals:
        raise ValueError("closing Page structural refusal: " +
                         json.dumps(refusals, sort_keys=True))
    results = []
    for left, right, edge, counts in ((148, 149, "trailing", (3, 2)),
                                     (149, 150, "leading", (6, 6)),
                                     (150, 151, "leading", (3, 3))):
        for i, orthography in enumerate(("pre_reform", "modern")):
            result = diagnose(branches[left][i], branches[right][i],
                              edge=edge, letters=counts[i])
            results.append({"left_page": left, "right_page": right,
                            "literal_branch": orthography, **result})
    # Only a terminal punctuation observation, not independent scan collation.
    endings = []
    for i, orthography in enumerate(("pre_reform", "modern")):
        _, final = edge_scope(branches[151][i], "leading")
        if final.rstrip()[-1:] not in (".", "!", "?", "…"):
            raise ValueError("closing Page final punctuation differs")
        endings.append({"literal_branch": orthography,
                        "candidate_characters_including_spaces": len(final.strip()),
                        "ends_in_sentence_punctuation": True})
    return results, endings


def capture(graph, preflight, *, query=_api_query):
    selected = [p for p in graph["pages"] if p["page_sequence"] in PINS]
    if {p["page_sequence"]: p["revision_id"] for p in selected} != PINS or len(selected) != 4:
        raise ValueError("closing Page graph identity drift")
    expected = {p["revision_id"]: p for p in selected}
    prior = {p["page_sequence"]: p for p in preflight["pages"]}
    response = query({"action": "query", "prop": "revisions",
                      "revids": "|".join(map(str, expected)),
                      "rvprop": "ids|timestamp|sha1|content", "rvslots": "main"})
    rows = response.get("query", {}).get("pages")
    if not isinstance(rows, list) or len(rows) != 4:
        raise ValueError("closing Page response incomplete")
    raws, identities = {}, []
    for page in rows:
        revisions = page.get("revisions")
        if not isinstance(revisions, list) or len(revisions) != 1:
            raise ValueError("ambiguous closing Page revision")
        rev = revisions[0]
        pin = expected.get(rev.get("revid"))
        if pin is None or pin["page_sequence"] in raws or (
                page.get("pageid"), page.get("title"), rev.get("timestamp"), rev.get("sha1")
        ) != (pin["page_id"], pin["title"], pin["timestamp_utc"], pin["mediawiki_sha1"]):
            raise ValueError("closing Page identity drift")
        n = pin["page_sequence"]
        main = rev.get("slots", {}).get("main", {})
        raw = main.get("content")
        if (not isinstance(raw, str) or not raw.strip() or len(raw.encode("utf-8")) > 200_000
                or main.get("contentmodel", "wikitext") not in ("wikitext", "proofread-page")):
            raise ValueError("invalid closing Page bytes")
        candidate = transclusion_input(raw)
        old = prior[n]
        if (old["revision_id"], old["wikitext_sha256"], old["wikitext_utf8_bytes"],
                old["transclusion_input_sha256"],
                old["transclusion_input_characters_including_spaces"]) != (
                pin["revision_id"], digest(raw), len(raw.encode("utf-8")),
                digest(candidate), len(candidate)):
            raise ValueError("closing Page preflight byte drift")
        raws[n] = raw
        identities.append({"page_sequence": n, "revision_id": pin["revision_id"],
                           "source_mediawiki_sha1": pin["mediawiki_sha1"],
                           "wikitext_sha256": digest(raw),
                           "transclusion_input_sha256": digest(candidate)})
    seams, endings = diagnose_pages(raws)
    report = {"schema_version": SCHEMA, "source_page_graph_sha256": preflight["source_page_graph_sha256"],
            "pages": sorted(identities, key=lambda p: p["page_sequence"]),
            "seams": seams, "final_branch_observations": endings,
            "printed_ending_scope": "MANUAL_SCAN_OBSERVATION_ONLY",
            "facing_errata_excluded_by_full_collation": "NOT_VERIFIED",
            "historical_render_equivalence_proven": False,
            "full_literary_body": "NOT_VERIFIED", "source_text_committed": False,
            "corpus_admitted": False, "m2_parity_admissible": False}
    # Report only the exact bounded syntax token, never comment or prose.
    if wrapper_signature(raws[151]) == {"events": _PAGE151_RAW_EVENTS, "truncated": False}:
        _, opener = page151_branches(raws[151])
        report["page151_var_opener"] = opener
        report["page151_branch_comments_removed"] = 2
    return report


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    for name in ("graph", "receipt", "preflight", "preflight-receipt", "output"):
        parser.add_argument("--" + name, required=True, type=Path)
    args = parser.parse_args()
    if args.output.exists() or args.output.resolve() in {
            p.resolve() for p in (args.graph, args.receipt, args.preflight, args.preflight_receipt)}:
        parser.error("output must be new and distinct")
    graph = verify_frozen_graph(args.graph, args.receipt)
    preflight = verify_receipt(args.preflight, args.preflight_receipt, graph)
    if sha256(args.graph.read_bytes()).hexdigest() != preflight["source_page_graph_sha256"]:
        raise ValueError("closing Page graph digest drift")
    report = capture(graph, preflight)
    with args.output.open("x", encoding="utf-8") as out:
        json.dump(report, out, ensure_ascii=False, sort_keys=True, indent=2)
        out.write("\n")
    print("Closing seams:", report["seams"], "; full body NOT_VERIFIED")


if __name__ == "__main__":
    main()
