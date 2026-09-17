"""Source-free MediaWiki partial-transclusion preprocessing evidence.

This module implements only the documented ``noinclude`` / ``includeonly`` /
``onlyinclude`` selection layer. It intentionally stops before template
parameter expansion, magic words, parser functions, extension tags, or normal
MediaWiki parsing. The implementation is fail-closed for malformed control-tag
markup and for ``nowiki`` because MediaWiki gives inclusion tags special rules
inside nowiki that are outside this bounded profile.
"""
from __future__ import annotations

from collections import Counter
from hashlib import sha256
import re
from typing import Mapping

PROFILE_VERSION = "scriptorium-mediawiki-transclusion-controls-v1"
MANIFEST_VERSION = "scriptorium-template-transclusion-shape-v1"
MEDIAWIKI_HELP_TRANSCLUSION = "https://www.mediawiki.org/wiki/Help:Transclusion"
MEDIAWIKI_HELP_TEMPLATES = "https://www.mediawiki.org/wiki/Help:Templates"

_CONTROL_RE = re.compile(
    r"<\s*(?P<close>/)?\s*(?P<tag>noinclude|includeonly|onlyinclude)\s*(?P<self>/)?\s*>",
    re.IGNORECASE,
)
_NOWIKI_RE = re.compile(r"<\s*/?\s*nowiki\b", re.IGNORECASE)
_TEMPLATE_OPEN_RE = re.compile(r"(?<!\{)\{\{(?!\{)\s*([^|{}\n]+)")
_HTML_TAG_RE = re.compile(r"</?\s*([A-Za-z][A-Za-z0-9]*)\b")
_TAG_TARGET_RE = re.compile(r"(?<!\{)\{\{(?!\{)\s*#tag\s*:\s*([^|{}\n]+)", re.IGNORECASE)
_MAGIC_WORDS = {"PAGENAME"}


def _sha256_text(value: str) -> str:
    return sha256(value.encode("utf-8")).hexdigest()


def preprocess_for_transclusion(wikitext: str) -> tuple[str, dict[str, int]]:
    """Apply the documented partial-transclusion control-tag selection layer.

    If at least one paired ``onlyinclude`` block exists, only text inside an
    ``onlyinclude`` context is eligible. ``noinclude`` content is always
    excluded from transclusion, while ``includeonly`` content is eligible and
    the control tags themselves are removed.
    """
    if not isinstance(wikitext, str):
        raise TypeError("wikitext must be str")
    if _NOWIKI_RE.search(wikitext):
        raise ValueError("nowiki requires MediaWiki-specific inclusion handling outside this profile")

    tokens = list(_CONTROL_RE.finditer(wikitext))
    stack: list[str] = []
    pair_counts: Counter[str] = Counter()
    self_counts: Counter[str] = Counter()
    onlyinclude_pairs = 0
    for match in tokens:
        tag = match.group("tag").lower()
        is_close = bool(match.group("close"))
        is_self = bool(match.group("self"))
        if is_close and is_self:
            raise ValueError("control tag cannot be both closing and self-closing")
        if is_self:
            self_counts[tag] += 1
            continue
        if is_close:
            if not stack or stack[-1] != tag:
                raise ValueError(f"malformed or crossing MediaWiki control tag: {tag}")
            stack.pop()
            pair_counts[tag] += 1
            if tag == "onlyinclude":
                onlyinclude_pairs += 1
        else:
            stack.append(tag)
    if stack:
        raise ValueError(f"unclosed MediaWiki control tag: {stack[-1]}")

    has_onlyinclude = onlyinclude_pairs > 0
    depths = {"noinclude": 0, "includeonly": 0, "onlyinclude": 0}
    out: list[str] = []
    cursor = 0

    def eligible() -> bool:
        if depths["noinclude"] > 0:
            return False
        if has_onlyinclude and depths["onlyinclude"] == 0:
            return False
        return True

    for match in tokens:
        if eligible():
            out.append(wikitext[cursor:match.start()])
        tag = match.group("tag").lower()
        is_close = bool(match.group("close"))
        is_self = bool(match.group("self"))
        if not is_self:
            if is_close:
                depths[tag] -= 1
                if depths[tag] < 0:
                    raise AssertionError("validated control-tag depth underflow")
            else:
                depths[tag] += 1
        cursor = match.end()
    if eligible():
        out.append(wikitext[cursor:])

    counts = {
        "noinclude_pairs": pair_counts["noinclude"],
        "includeonly_pairs": pair_counts["includeonly"],
        "onlyinclude_pairs": pair_counts["onlyinclude"],
        "noinclude_self_closing": self_counts["noinclude"],
        "includeonly_self_closing": self_counts["includeonly"],
        "onlyinclude_self_closing": self_counts["onlyinclude"],
    }
    return "".join(out), counts


def classify_effective_dependencies(transclusion_input: str) -> dict[str, object]:
    """Classify unresolved double-brace constructs after inclusion selection."""
    templates: Counter[str] = Counter()
    parser_functions: Counter[str] = Counter()
    magic_words: Counter[str] = Counter()
    for match in _TEMPLATE_OPEN_RE.finditer(transclusion_input):
        raw = match.group(1).strip()
        if not raw:
            continue
        if raw.startswith("#"):
            parser_functions[raw.split(":", 1)[0].lower()] += 1
        elif raw.upper() in _MAGIC_WORDS:
            magic_words[raw.upper()] += 1
        else:
            templates[raw] += 1
    extension_targets = Counter(
        match.group(1).strip().lower() for match in _TAG_TARGET_RE.finditer(transclusion_input)
        if match.group(1).strip()
    )
    html_tags = Counter(match.group(1).lower() for match in _HTML_TAG_RE.finditer(transclusion_input))
    return {
        "ordinary_template_counts": dict(sorted(templates.items())),
        "parser_function_counts": dict(sorted(parser_functions.items())),
        "magic_word_counts": dict(sorted(magic_words.items())),
        "extension_tag_targets": dict(sorted(extension_targets.items())),
        "html_tag_name_counts": dict(sorted(html_tags.items())),
    }


def build_transclusion_shape_manifest(
    *,
    candidate_id: str,
    revision_identity: Mapping[str, object],
    wikitext: str,
    research_date: str,
) -> dict[str, object]:
    if not isinstance(candidate_id, str) or not candidate_id:
        raise ValueError("candidate_id must be non-empty")
    if not isinstance(revision_identity, Mapping):
        raise TypeError("revision_identity must be a mapping")
    required = ("title", "revision_id", "wikitext_sha256")
    for key in required:
        if key not in revision_identity:
            raise ValueError(f"revision identity missing {key}")
    if _sha256_text(wikitext) != revision_identity["wikitext_sha256"]:
        raise ValueError("pinned template wikitext digest drift before transclusion preprocessing")
    transclusion_input, control_counts = preprocess_for_transclusion(wikitext)
    graph = classify_effective_dependencies(transclusion_input)
    return {
        "manifest_version": MANIFEST_VERSION,
        "candidate_id": candidate_id,
        "research_date": research_date,
        "source_revision": {
            "title": revision_identity["title"],
            "revision_id": revision_identity["revision_id"],
            "wikitext_sha256": revision_identity["wikitext_sha256"],
        },
        "preprocessing_profile": PROFILE_VERSION,
        "semantics_evidence": [
            {
                "url": MEDIAWIKI_HELP_TRANSCLUSION,
                "claim": "noinclude is excluded; includeonly is included; onlyinclude limits transclusion to onlyinclude content",
            },
            {
                "url": MEDIAWIKI_HELP_TEMPLATES,
                "claim": "onlyinclude takes precedence over content outside onlyinclude, including includeonly outside it",
            },
        ],
        "control_tag_counts": control_counts,
        "effective_dependency_graph": graph,
        "capture_scope": {
            "partial_transclusion_control_semantics_reproduced": True,
            "effective_dependency_graph_frozen": True,
            "transclusion_input_digest_recorded": False,
            "template_parameter_expansion_reproduced": False,
            "magic_word_expansion_reproduced": False,
            "parser_function_expansion_reproduced": False,
            "extension_tag_expansion_reproduced": False,
            "historical_render_equivalence_proven": False,
            "source_text_committed": False,
        },
        "boundary": (
            "This artifact freezes only the documented partial-transclusion selection layer and the "
            "remaining unresolved dependency classes for the pinned template revision. It does not "
            "claim MediaWiki parser expansion, extension-tag rendering, or historical render equivalence."
        ),
        "source_text_included": False,
    }
