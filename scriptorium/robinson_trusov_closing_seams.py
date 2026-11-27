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
import unicodedata

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
    COMMENT_TOKEN_JOIN = "PAGE151_COMMENT_TOKEN_JOIN"
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
    Remove only the two recognized comments in this pinned leaf shape.
    Preserve the complete literal gap after branch zero's leading span;
    refuse a comment cut that would join lexical tokens.
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
            # The pinned replay observed a nonempty literal gap here.
            # Keep it byte-for-byte; only the recognized comment is removed.
            gap = branch[leading.end():comment.start()]
            suffix = branch[comment.end():]
            def word_edge(c):
                return (unicodedata.category(c)[0] in "LMN"
                        or unicodedata.category(c) == "Pd" or c in "_'’")
            if gap and suffix and word_edge(gap[-1]) and word_edge(suffix[0]):
                raise _Page151Refusal(_Page151Reason.COMMENT_TOKEN_JOIN, i)
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



# Observation only: broader tag matching never authorizes a continuation.
_OBSERVED_NOINCLUDE = re.compile(
    r"(?P<open><noinclude\b[^>]*>)(?P<body>.*?)"
    r"(?P<close></noinclude\b[^>]*>)", re.I | re.S,
)


def _fragment_counts(value):
    return {
        "characters": len(value),
        "whitespace": sum(c.isspace() for c in value),
        "letters": sum(c.isalpha() for c in value),
        "digits": sum(c.isdigit() for c in value),
        "angle_brackets": value.count("<") + value.count(">"),
        "apostrophes": value.count("'"),
        "other": sum(not (c.isspace() or c.isalpha() or c.isdigit()
                          or c in "<>'") for c in value),
    }


def _edge_observation(branch, edge):
    """Summarize a failed edge's shape without accepting or logging prose."""
    strict = (LEADING if edge == "leading" else TRAILING).search(branch)
    opens = len(re.findall(r"<noinclude\b", branch, re.I))
    closes = len(re.findall(r"</noinclude\b", branch, re.I))
    matches = list(_OBSERVED_NOINCLUDE.finditer(branch))
    pairs = []
    for match in matches[:4]:
        prefix, body, suffix = (branch[:match.start()], match.group("body"),
                                branch[match.end():])
        pairs.append({
            "exact_tags": (match.group("open").lower() == "<noinclude>"
                           and match.group("close").lower() == "</noinclude>"),
            "body_counts": _fragment_counts(body),
            "prefix_counts": _fragment_counts(prefix),
            "suffix_counts": _fragment_counts(suffix),
            "at_expected_edge": not (prefix if edge == "leading" else suffix).strip(),
            "letter_only_body": bool(body.strip()) and body.strip().isalpha(),
        })
    if strict is not None:
        shape = "STRICT_MATCH"
    elif not opens and not closes:
        shape = "ABSENT"
    elif not matches or opens != closes or len(matches) != opens:
        shape = "UNPAIRED_OR_NESTED"
    elif any(p["exact_tags"] and p["body_counts"]["angle_brackets"] == 0
             for p in pairs):
        shape = "ADDITIONAL_EDGE_STRUCTURE"
    else:
        shape = "NONLITERAL_SCOPE"
    return {"shape": shape, "opens": opens, "closes": closes,
            "pair_count": len(matches), "pairs": pairs,
            "truncated": len(matches) > len(pairs)}



# The previous pinned replay observed one additional angle pair in each
# branch of Pages 148 and 150. A whitespace-only HTML comment is a candidate
# explanation, not a fact inferred from counts. Verify the token and its
# position at runtime after capture has bound the original bytes.
_FORMATTING_SIDES = {(148, 0): "after", (148, 1): "before",
                     (150, 0): "after", (150, 1): "before"}
_BLANK_COMMENT = re.compile(r"<!--[ \t\r\n]{0,2}-->")
_RESIDUAL_TOKEN = re.compile(r"<!--[\s\S]*?-->|<[^<>]*>|[<>]")


def _formatting_candidate(page, index, branch):
    """Remove only one verified blank edge comment; never normalize prose."""
    report = {"page_sequence": page, "revision_id": PINS[page],
              "branch_index": index, "classification": "NOT_APPLICABLE",
              "tokens": [], "removed_characters": 0}
    side = _FORMATTING_SIDES.get((page, index))
    if side is None:
        return branch, report
    pairs = list(_OBSERVED_NOINCLUDE.finditer(branch))
    if len(pairs) != 1:
        report["classification"] = "NO_UNIQUE_EDGE_PAIR"
        return branch, report
    pair = pairs[0]
    fragments = (("before", branch[:pair.start()], 0),
                 ("after", branch[pair.end():], pair.end()))
    tokens = []
    for where, fragment, offset in fragments:
        for match in _RESIDUAL_TOKEN.finditer(fragment):
            token = match.group()
            before = not fragment[:match.start()].strip()
            after = not fragment[match.end():].strip()
            kind = ("BLANK_COMMENT" if _BLANK_COMMENT.fullmatch(token)
                    else "OTHER_COMMENT" if token.startswith("<!--")
                    else "OTHER_ANGLE_MARKUP")
            position = ("ONLY" if before and after else "START" if before
                        else "END" if after else "INTERIOR")
            tokens.append((offset + match.start(), offset + match.end(),
                           {"side": where, "position": position, "kind": kind,
                            "characters": len(token)}))
            if len(tokens) > 4:
                report["classification"] = "TOO_MANY_TOKENS"
                report["tokens"] = [item[2] for item in tokens[:4]]
                return branch, report
    report["tokens"] = [item[2] for item in tokens]
    if not tokens:
        report["classification"] = "NO_RESIDUAL_TOKEN"
        return branch, report
    report["classification"] = "UNSUPPORTED_FORMATTING"
    if len(tokens) != 1:
        return branch, report
    start, end, observed = tokens[0]
    if observed["kind"] != "BLANK_COMMENT" or observed["side"] != side:
        return branch, report
    # The two short fragments were entirely nonliterary in the exact
    # preceding replay (9 and 8 characters respectively). Require the
    # entire side to be this single blank comment plus ASCII whitespace.
    short_side = {(148, 0): 9, (150, 1): 8}.get((page, index))
    if short_side is not None:
        fragment = next(value for where, value, _ in fragments if where == side)
        if len(fragment) != short_side or observed["position"] != "ONLY":
            return branch, report
        if any(c not in " \t\r\n" for c in fragment.replace(branch[start:end], "", 1)):
            return branch, report
    elif observed["position"] == "INTERIOR":
        # An in-body token requires its own independently justified scope.
        return branch, report
    candidate = branch[:start] + branch[end:]
    try:
        # All existing lexical, noinclude and residual-markup rules still
        # apply to the candidate. Compare the two projections exactly.
        edge = "trailing" if page == 148 else "leading"
        edge_scope(candidate, edge)
        projected = transclusion_input(branch)
        token = branch[start:end]
        if projected.count(token) != 1:
            return branch, report
        if transclusion_input(candidate) != projected.replace(token, "", 1):
            return branch, report
    except ValueError:
        return branch, report
    report["classification"] = "VERIFIED_BLANK_EDGE_COMMENT"
    report["removed_characters"] = end - start
    return candidate, report



# Page 149 has no noinclude scope. The prior pinned run refused both
# traversals at plain_branch, after all four adjacent blank edge comments
# had been verified. Inspect the same literal branch once for both joins.
_PAGE149_TOKEN = re.compile(
    r"<!--[\s\S]*?-->|<[^<>]*>|[<>]|'{2,}|[\[\]{}]+"
)


def _page149_candidate(index, branch):
    """Bounded observation and strictly verified blank-edge candidate only."""
    report = {"page_sequence": 149, "revision_id": PINS[149],
              "branch_index": index, "classification": "NO_RESIDUAL_TOKEN",
              "shared_by_joins": [[148, 149], [149, 150]],
              "token_count": 0, "tokens": [], "removed_characters": 0}
    matches = list(_PAGE149_TOKEN.finditer(branch))
    report["token_count"] = len(matches)
    if not matches:
        return branch, report
    report["classification"] = "UNSUPPORTED_PAGE149_MARKUP"
    # Lexical positions are relative to literal text, excluding the
    # observed tokens (including any letters inside comments/tags).
    fragments = []
    cursor = 0
    for match in matches:
        fragments.append(branch[cursor:match.start()])
        cursor = match.end()
    fragments.append(branch[cursor:])
    lexical = [any(c.isalpha() or c.isdigit() for c in x) for x in fragments]
    for i, match in enumerate(matches[:8]):
        token = match.group()
        if _BLANK_COMMENT.fullmatch(token):
            kind = "BLANK_COMMENT"
        elif token.startswith("<!--"):
            kind = "OTHER_COMMENT"
        elif re.fullmatch(r"</?noinclude\b[^>]*>", token, re.I):
            kind = "NOINCLUDE"
        elif re.fullmatch(r"<br\s*/?>", token, re.I):
            kind = "BREAK_TAG"
        elif token.startswith("<") or token == ">":
            kind = "OTHER_ANGLE_MARKUP"
        elif token.startswith("'"):
            kind = "APOSTROPHE_RUN"
        else:
            kind = "BRACKET_OR_BRACE"
        before, after = any(lexical[:i+1]), any(lexical[i+1:])
        position = ("INTERIOR" if before and after else "END" if before
                    else "START" if after else "NO_LEXICAL_TEXT")
        report["tokens"].append({"kind": kind, "characters": len(token),
                                 "position": position})
    report["truncated"] = len(matches) > 8
    # The adjacent leaves proved eight-character blank comments.
    # Accept this exact class only if the current pinned bytes independently
    # prove one such token at an outer edge of the otherwise plain branch.
    if len(matches) != 1:
        return branch, report
    match = matches[0]
    token = match.group()
    if len(token) != 8 or not _BLANK_COMMENT.fullmatch(token):
        return branch, report
    prefix, suffix = branch[:match.start()], branch[match.end():]
    if not (all(c in " \t\r\n" for c in prefix)
            or all(c in " \t\r\n" for c in suffix)):
        return branch, report
    candidate = prefix + suffix
    try:
        plain_branch(candidate)
        original = transclusion_input(branch)
        if original != branch or transclusion_input(candidate) != candidate:
            return branch, report
        if original.count(token) != 1 or original.replace(token, "", 1) != candidate:
            return branch, report
    except ValueError:
        return branch, report
    report["classification"] = "VERIFIED_PAGE149_BLANK_EDGE_COMMENT"
    report["removed_characters"] = len(token)
    return candidate, report


# Only fixed reason codes may reach a hosted log; unexpected ValueErrors
# remain refusals and their original message is never propagated.
_SEAM_REASONS = {
    "expected closing edge noinclude missing": "EDGE_NOINCLUDE_MISSING",
    "closing edge is not a short letter-only continuation": "EDGE_TOKEN_NOT_LITERAL",
    "additional closing edge scope": "ADDITIONAL_EDGE_SCOPE",
    "additional closing noinclude span": "ADDITIONAL_NOINCLUDE",
    "closing branch has unresolved markup": "UNRESOLVED_EDGE_MARKUP",
    "unexpected closing branch markup": "UNEXPECTED_BRANCH_MARKUP",
    "unknown closing seam direction": "UNKNOWN_DIRECTION",
    "closing seam has no lexical boundary": "MISSING_LEXICAL_BOUNDARY",
    "closing seam count or ownership differs from scan observation": "COUNT_OR_OWNERSHIP",
}


def _seam_observation(left, right, i, edge, letters, branches, refusal):
    expected_page = left if edge == "trailing" else right
    return {
        "left_page": left, "right_page": right,
        "branch_index": i, "expected_edge": edge,
        "expected_letters": letters, "expected_edge_page": expected_page,
        "expected_edge_revision": PINS[expected_page],
        "reason": _SEAM_REASONS.get(str(refusal), "UNCLASSIFIED_REFUSAL"),
        "left_trailing": _edge_observation(branches[left][i], "trailing"),
        "left_leading": _edge_observation(branches[left][i], "leading"),
        "right_leading": _edge_observation(branches[right][i], "leading"),
        "right_trailing": _edge_observation(branches[right][i], "trailing"),
    }


def diagnose_pages(raws, *, body_observer=None):
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
    formatting = []
    for n in (148, 150):
        cleaned = []
        for i, branch in enumerate(branches[n]):
            candidate, observation = _formatting_candidate(n, i, branch)
            cleaned.append(candidate)
            formatting.append(observation)
        branches[n] = tuple(cleaned)
    page149 = []
    cleaned = []
    for i, branch in enumerate(branches[149]):
        candidate, observation = _page149_candidate(i, branch)
        cleaned.append(candidate)
        page149.append(observation)
    branches[149] = tuple(cleaned)
    results, seam_refusals = [], []
    for left, right, edge, counts in ((148, 149, "trailing", (3, 2)),
                                     (149, 150, "leading", (6, 6)),
                                     (150, 151, "leading", (3, 3))):
        for i, orthography in enumerate(("pre_reform", "modern")):
            try:
                result = diagnose(branches[left][i], branches[right][i],
                                  edge=edge, letters=counts[i])
            except ValueError as refusal:
                seam_refusals.append(_seam_observation(
                    left, right, i, edge, counts[i], branches, refusal))
                continue
            results.append({"left_page": left, "right_page": right,
                            "literal_branch": orthography, **result})
    # Inspect all six independent assertions on the same pinned bytes, but
    # never return a partial report or admit a body if any assertion failed.
    if seam_refusals:
        raise ValueError("closing seam ownership or structure refusal: " +
                         json.dumps({"refusals": seam_refusals,
                                     "successful_assertions": len(results),
                                     "formatting_observations": formatting,
                                     "page149_observations": page149},
                                    sort_keys=True))
    # Only a terminal punctuation observation, not independent scan collation.
    endings = []
    for i, orthography in enumerate(("pre_reform", "modern")):
        _, final = edge_scope(branches[151][i], "leading")
        if final.rstrip()[-1:] not in (".", "!", "?", "…"):
            raise ValueError("closing Page final punctuation differs")
        endings.append({"literal_branch": orthography,
                        "candidate_characters_including_spaces": len(final.strip()),
                        "ends_in_sentence_punctuation": True})
    if body_observer is not None:
        # Only after every ownership assertion and terminal check passed.
        for n in sorted(branches):
            for i, branch in enumerate(branches[n]):
                if n == 149:
                    scoped = standalone = plain_branch(branch)
                else:
                    edge = "trailing" if n == 148 else "leading"
                    _, scoped = edge_scope(branch, edge)
                    match = (TRAILING if edge == "trailing" else LEADING).search(branch)
                    # Standalone retains the continuation; only the exact tags
                    # are removed. This is a literal candidate, not rendering.
                    # Scope patterns allow case variants. Use the actual
                    # matched span to preserve surrounding whitespace.
                    standalone = (branch[:match.start()] +
                                  re.sub(r"</?noinclude>", "", match.group(), flags=re.I) +
                                  branch[match.end():])
                body_observer(n, i, scoped, standalone)
    return results, endings


def compare_render_candidate(literal, rendered):
    """Counts-only comparison; alignment is diagnostic, never collation."""
    from .robinson_trusov_boundary_render import nonspace_edit_summary
    left = "".join(literal.split())
    row = {"literal_characters": len(literal),
           "literal_nonspace_characters": len(left),
           "rendered_nonspace_characters": None,
           "classification": "RENDER_REFUSED",
           "nonspace_edit_summary": {"status": "RENDER_REFUSED"}}
    if rendered is not None:
        right = "".join(rendered.split())
        row.update(
            rendered_nonspace_characters=len(right),
            classification=("COLLAPSED_EQUAL" if literal.split() == rendered.split()
                            else "NONSPACE_EQUAL_ONLY" if left == right
                            else "NONSPACE_DIFFERS"),
            nonspace_edit_summary=nonspace_edit_summary(literal, rendered),
        )
    return row


def _combined_view(first, second, rendered):
    """Exact nonspace placement, not subsequence alignment or a VAR renderer.

    Enumerate both orders, requiring two disjoint contiguous occurrences.
    Saturate at two placements; ambiguous matches never yield a residual.
    The second return value stays in memory only for cross-Page equality.
    """
    a, b = ("".join(x.split()) for x in (first, second))
    row = {"classification": "RENDER_REFUSED", "order": None,
           "branch_nonspace_characters": [len(a), len(b)],
           "rendered_nonspace_characters": None, "placement_count_capped": None,
           "residual_regions": None}
    if rendered is None:
        return row, None
    view = "".join(rendered.split())
    row["rendered_nonspace_characters"] = len(view)
    if max(len(a), len(b), len(view)) > 8192:
        row["classification"] = "SIZE_LIMIT"
        return row, None
    if not a or not b:
        row["classification"] = "EMPTY_BRANCH"
        return row, None
    placements = []
    for order, x, y in (("PRE_REFORM_THEN_MODERN", a, b),
                        ("MODERN_THEN_PRE_REFORM", b, a)):
        start = view.find(x)
        while start != -1:
            end = start + len(x)
            other = view.find(y, end)
            while other != -1:
                placements.append((order, start, end, other, other + len(y)))
                if len(placements) == 2:
                    row.update(classification="AMBIGUOUS_PLACEMENT",
                               placement_count_capped=2)
                    return row, None
                other = view.find(y, other + 1)
            start = view.find(x, start + 1)
    row["placement_count_capped"] = len(placements)
    if not placements:
        row["classification"] = "NO_ORDERED_DISJOINT_PLACEMENT"
        return row, None
    order, start, end, other, finish = placements[0]
    residual = (view[:start], view[end:other], view[finish:])
    regions = []
    for name, value in zip(("prefix", "between", "suffix"), residual, strict=True):
        counts = dict.fromkeys("LMNPSZC", 0)
        for char in value:
            counts[unicodedata.category(char)[0]] += 1
        regions.append({"region": name, "nonspace_characters": len(value),
                        "unicode_categories": counts})
    row.update(classification="UNIQUE_ORDERED_PLACEMENT", order=order,
               residual_regions=regions)
    return row, residual


def _residual_equality(residuals):
    """Compare actual region strings in memory, never publish text or hashes."""
    if len(residuals) != len(PINS) or any(x is None for x in residuals):
        return "NOT_ESTABLISHED"
    return ("ALL_FOUR_REGION_STRINGS_EQUAL" if all(x == residuals[0] for x in residuals)
            else "REGION_STRINGS_DIFFER")


MODULE_TITLE = "Модуль:Дореформенная орфография"
MODULE_REVISION = 5721277
MODULE_LABEL = "Тот же текст в современной орфографии"


def _layout_label(query):
    """Read a pinned public module, not a presumed historical dependency."""
    result = query({"action": "query", "prop": "revisions",
                    "revids": str(MODULE_REVISION),
                    "rvprop": "ids|sha1|content", "rvslots": "main"})
    pages = result.get("query", {}).get("pages")
    if not isinstance(pages, list) or len(pages) != 1:
        raise ValueError("closing layout module response incomplete")
    page = pages[0]
    revisions = page.get("revisions")
    if (page.get("title") != MODULE_TITLE or type(page.get("pageid")) is not int
            or page["pageid"] <= 0 or not isinstance(revisions, list)
            or len(revisions) != 1):
        raise ValueError("closing layout module identity drift")
    rev = revisions[0]
    main = rev.get("slots", {}).get("main", {})
    raw = main.get("content")
    if (rev.get("revid") != MODULE_REVISION or main.get("contentmodel") != "Scribunto"
            or not re.fullmatch(r"[0-9a-f]{40}", rev.get("sha1") or "")
            or not isinstance(raw, str) or len(raw.encode("utf-8")) > 200_000):
        raise ValueError("closing layout module revision drift")
    labels = re.findall(r'<div class="newspell"[^<>]*>([^<>]+)</div>', raw)
    if len(labels) != 1 or labels[0].split() != MODULE_LABEL.split():
        raise ValueError("closing layout module label drift")
    label = "".join(labels[0].split())
    return label, {"revision_id": MODULE_REVISION, "page_id": page["pageid"],
                   "nonspace_characters": len(label)}


def _layout_residuals(n, values, standalone, transcluded, label):
    """Exact region identity; no residual strings or short-span hashes escape.

    The two scopes differ only by their already verified continuation at
    the declared edge. Do not use length subtraction as identity proof.
    """
    expected = {148: (3, 2), 149: (0, 0), 150: (6, 6), 151: (3, 3)}[n]
    leading, trailing = [], []
    for (scoped, whole), count in zip(values, expected, strict=True):
        scoped, whole = ("".join(x.split()) for x in (scoped, whole))
        if not scoped or len(whole) - len(scoped) != count:
            raise ValueError("closing layout continuation count drift")
        if n == 148:
            if not whole.startswith(scoped):
                raise ValueError("closing layout trailing continuation drift")
            leading.append("")
            trailing.append(whole[len(scoped):])
        elif n in (150, 151):
            if not whole.endswith(scoped):
                raise ValueError("closing layout leading continuation drift")
            leading.append(whole[:count])
            trailing.append("")
        else:
            if whole != scoped:
                raise ValueError("closing layout plain scope drift")
            leading.append("")
            trailing.append("")
        if any(not ch.isalpha() for ch in leading[-1] + trailing[-1]):
            raise ValueError("closing layout nonletter continuation")
    def status(observed, target):
        if observed is None:
            return "NOT_ESTABLISHED"
        return "MATCH" if observed == target else "MISMATCH"
    return {
        "standalone_module_label": status(standalone, ("", label, "")),
        "transcluded_label_and_continuations": status(
            transcluded, (leading[0], trailing[0] + label + leading[1], trailing[1])),
        "continuation_nonspace_characters": list(expected),
    }


def compare_current_closing_views(selected, candidates, *, query, verify_layout=False):
    """Compare both literal branches against current pinned Page views."""
    from .robinson_trusov_boundary_render import _observe
    if set(candidates) != {(n, i) for n in PINS for i in (0, 1)}:
        raise ValueError("closing comparison candidate coverage incomplete")
    rows = []
    label, module = _layout_label(query) if verify_layout else (None, None)
    residuals = {"transcluded_scope": [], "standalone_scope": []}
    for pin in sorted(selected, key=lambda p: p["page_sequence"]):
        n = pin["page_sequence"]
        result = query({"action": "parse", "oldid": str(pin["revision_id"]),
                        "prop": "text|revid", "disableeditsection": "1"}).get("parse", {})
        if (result.get("revid"), result.get("pageid"), result.get("title")) != (
                pin["revision_id"], pin["page_id"], pin["title"]):
            raise ValueError("closing Page render identity drift")
        observation, rendered = _observe(result.get("text"), scope_counts=True)
        combined = {}
        for index, scope in enumerate(residuals):
            combined[scope], residual = _combined_view(
                candidates[n, 0][index], candidates[n, 1][index], rendered)
            residuals[scope].append(residual)
        layout = None
        if verify_layout:
            # Only the known branch order supports the declared edge equation.
            layout = _layout_residuals(
                n, [candidates[n, i] for i in (0, 1)],
                residuals["standalone_scope"][-1] if combined["standalone_scope"]["order"] == "PRE_REFORM_THEN_MODERN" else None,
                residuals["transcluded_scope"][-1] if combined["transcluded_scope"]["order"] == "PRE_REFORM_THEN_MODERN" else None,
                label)
        rows.append({
            "layout_identity": layout,
            "combined_branches": combined,
            "page_sequence": n, "revision_id": pin["revision_id"],
            "source_mediawiki_sha1": pin["mediawiki_sha1"],
            "render_status": observation["status"],
            "rendered_characters": observation["candidate_characters"],
            "skipped_body_nonspace_characters": observation["skipped_body_nonspace_characters"],
            "branches": [
                {"literal_branch": name,
                 "transcluded_scope": compare_render_candidate(candidates[n, i][0], rendered),
                 "standalone_scope": compare_render_candidate(candidates[n, i][1], rendered)}
                for i, name in enumerate(("pre_reform", "modern"))
            ],
        })
    return {"scope": "CURRENT_PAGE_VIEW_VS_LITERAL_CLOSING_SCOPE_DIAGNOSTIC",
            "pages": rows, "combined_residual_cross_page_equality": {
                scope: _residual_equality(values) for scope, values in residuals.items()},
            "layout_module": module,
            "combined_residual_layout_identity": (
                "ALL_FOUR_STANDALONE_MATCH_MODULE_LABEL"
                if verify_layout and len(rows) == len(PINS) and all(
                    p["layout_identity"]["standalone_module_label"] == "MATCH" for p in rows)
                else "NOT_VERIFIED"),
            "transcluded_residual_layout_identity": (
                "ALL_FOUR_MATCH_LABEL_AND_CONTINUATIONS"
                if verify_layout and len(rows) == len(PINS) and all(
                    p["layout_identity"]["transcluded_label_and_continuations"] == "MATCH" for p in rows)
                else "NOT_VERIFIED"),
            "historical_render_equivalence_proven": False,
            "scan_collation_verified": False, "full_literary_body": "NOT_VERIFIED",
            "corpus_admitted": False, "m2_parity_admissible": False,
            "source_text_committed": False}


def capture(graph, preflight, *, query=_api_query, compare_current=False):
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
    candidates = {}
    def observe(n, i, scoped, standalone):
        candidates[n, i] = (scoped, standalone)
    seams, endings = diagnose_pages(raws, body_observer=observe if compare_current else None)
    report = {"schema_version": SCHEMA, "source_page_graph_sha256": preflight["source_page_graph_sha256"],
            "pages": sorted(identities, key=lambda p: p["page_sequence"]),
            "seams": seams, "final_branch_observations": endings,
            "printed_ending_scope": "MANUAL_SCAN_OBSERVATION_ONLY",
            "facing_errata_excluded_by_full_collation": "NOT_VERIFIED",
            "historical_render_equivalence_proven": False,
            "full_literary_body": "NOT_VERIFIED", "source_text_committed": False,
            "corpus_admitted": False, "m2_parity_admissible": False}
    report["formatting_observations"] = [
        _formatting_candidate(n, i, branch)[1]
        for n in (148, 150)
        for i, branch in enumerate(literal_branches(raws[n]))
    ]
    report["page149_observations"] = [
        _page149_candidate(i, branch)[1]
        for i, branch in enumerate(literal_branches(raws[149]))
    ]
    # Report only the exact bounded syntax token, never comment or prose.
    if wrapper_signature(raws[151]) == {"events": _PAGE151_RAW_EVENTS, "truncated": False}:
        _, opener = page151_branches(raws[151])
        report["page151_var_opener"] = opener
        report["page151_branch_comments_removed"] = 2
    if compare_current:
        report["current_page_view_comparison"] = compare_current_closing_views(
            selected, candidates, query=query, verify_layout=True)
    return report


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    for name in ("graph", "receipt", "preflight", "preflight-receipt", "output"):
        parser.add_argument("--" + name, required=True, type=Path)
    parser.add_argument("--compare-current", action="store_true")
    args = parser.parse_args()
    if args.output.exists() or args.output.resolve() in {
            p.resolve() for p in (args.graph, args.receipt, args.preflight, args.preflight_receipt)}:
        parser.error("output must be new and distinct")
    graph = verify_frozen_graph(args.graph, args.receipt)
    preflight = verify_receipt(args.preflight, args.preflight_receipt, graph)
    if sha256(args.graph.read_bytes()).hexdigest() != preflight["source_page_graph_sha256"]:
        raise ValueError("closing Page graph digest drift")
    report = capture(graph, preflight, compare_current=args.compare_current)
    with args.output.open("x", encoding="utf-8") as out:
        json.dump(report, out, ensure_ascii=False, sort_keys=True, indent=2)
        out.write("\n")
    print("Closing seams:", report["seams"], "; full body NOT_VERIFIED")


if __name__ == "__main__":
    main()
