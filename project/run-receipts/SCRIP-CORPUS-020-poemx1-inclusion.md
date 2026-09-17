# Run receipt — SCRIP-CORPUS-020 `poemx1` inclusion semantics

- Date: 2026-09-17
- Issue: #109
- PR: #113 (draft; independent review pending)
- Branch: `scrip-corpus-020-poemx1-inclusion-semantics`
- Base at selection: `d33e8e7b89530487c493c9283ce48ff9613f121a`
- Result: `POEMX1_INCLUSION_AUTHORED_REVIEW_PENDING`

## Bounded unit

Apply and freeze the documented MediaWiki `noinclude` / `includeonly` / `onlyinclude` transclusion-selection layer to pinned `Шаблон:Poemx1` oldid `5142743`, then derive the effective unresolved dependency classes without attempting parser-function or extension rendering.

## Evidence and implementation

Official MediaWiki help documents the relevant semantics: `noinclude` is excluded from transclusion; `includeonly` participates; if `onlyinclude` is present, content outside it is discarded even when wrapped in `includeonly`. `scriptorium/mediawiki_transclusion.py` implements only this selection layer. It rejects malformed/crossing control tags and fails closed on `nowiki` because MediaWiki assigns special inclusion behavior inside `nowiki` that is outside this bounded profile.

Six focused standard-library tests passed locally before the branch was published. They cover `noinclude` removal, `includeonly` retention, `onlyinclude` precedence/multiple blocks, self-closing controls, malformed/nowiki fail-closed behavior, source-free manifest boundaries, and dependency classification.

The pinned source-free observed contract is:

- source template: `Шаблон:Poemx1`, oldid `5142743`, wikitext SHA-256 `fa7e35686da5ce4c62986a7e8bfc72f2dba067118218d656b2f0983e5cfa06db`
- control tags: `noinclude` pairs x2; `includeonly` pairs x1; `onlyinclude` pairs x0
- effective ordinary template transclusions: none (`doc` is excluded)
- unresolved parser functions: `#expr` x2, `#if` x5, `#ifeq` x5, `#iferror` x1, `#tag` x1
- unresolved extension target: `poem` x1
- unresolved magic word: `PAGENAME` x1
- remaining HTML-like `div` tags: x6

The dedicated PR workflow now fetches exact oldid `5142743`, regenerates the source-free post-inclusion artifact and byte-compares it with `gorky-klim-samgin-ru.poemx1-template.transclusion.json` in addition to replaying the existing historical revision/shape evidence.

## Boundary

`historical_render_equivalence_proven=false`. Parameter/frame expansion, `PAGENAME`, parser functions, `#tag:poem`, resolved Part 2 bytes, candidate literary extraction/composition and raw/normalized body digests remain unfrozen. `fantlab_source_edition_match=unknown`; M2 remains **0/5**.

## Next action

Independent later-run exact-head review of draft PR #113 and all required checks. If clean, merge this prerequisite without closing Issue #109, then continue the remaining evidenced MediaWiki parser/magic-word/extension layer.
