# SCRIP-CORPUS-020 — bounded Poem render surface

- Re-opened Issue #109 after the previous prerequisite merge had mechanically closed it even though the canonical queue still required continuation.
- Added `scriptorium.mediawiki_poem_render_surface`, a fail-closed candidate-specific reconstruction for the six exact Klim Samgin `poemx1` parameter-2 values.
- Re-fetch/replay now proves that all six values contain zero additional conservative MediaWiki-core parser-sensitive constructs: no template/parameter opens, HTML angle brackets, table starts, horizontal rules, behavior switches, headings, internal links, apostrophe markup, external-link starts, raw protocols, magic-link tokens, language-converter opens, or entity references.
- The reached Poem branches are correspondingly narrow: no indentation, leading-space, horizontal-rule or trim branch; nine observed newlines map to nine protected breaks, no attributes or `compact` flag are present, and each result is wrapped in a `poem` div.
- Frozen source-free post-unstrip fragment identities total 534 characters / 799 UTF-8 bytes across six fragments. Per-fragment SHA-256 identities live in `gorky-klim-samgin-ru.poem-render-surface.json`; literary prose is not committed.
- Evidence remains explicitly inferred/candidate-specific: upstream Poem commit `03b3694613e23efa1254d8bbbb98121efaef2cb0` is a reconstruction anchor, the MediaWiki core source is semantic guidance rather than historical deployment identity, and no historical Wikisource render equivalence or resolved Part 2 body is claimed.
- Draft PR #121 carries the slice for independent later-run review. M2 remains 0/5.
