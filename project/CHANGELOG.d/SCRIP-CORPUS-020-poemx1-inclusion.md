# SCRIP-CORPUS-020 — `poemx1` partial-transclusion semantics

- Date: 2026-09-17
- Issue: #109
- Draft PR: #113
- Status: `POEMX1_INCLUSION_AUTHORED_REVIEW_PENDING`
- Scope: bounded corpus/provenance prerequisite; no literary-body or M2 promotion.

Scriptorium now has a source-free implementation of the documented MediaWiki partial-transclusion control layer. The profile applies `noinclude`, `includeonly` and `onlyinclude` selection semantics and fails closed on malformed control markup and `nowiki`, whose special MediaWiki behavior is outside this bounded profile. The implementation is backed by focused standard-library tests and cites the official MediaWiki `Help:Transclusion` / `Help:Templates` semantics.

Applied to the pinned inferred historical anchor `Шаблон:Poemx1` oldid `5142743`, exact replay evidence records two `noinclude` pairs, one `includeonly` pair and no `onlyinclude` pair. After inclusion selection the raw `doc` invocation and documentation `templatedata` surface disappear from the effective transclusion graph. No ordinary template transclusion remains.

The remaining unresolved graph is `#expr` x2, `#if` x5, `#ifeq` x5, `#iferror` x1, `#tag` x1 targeting `poem`, and `PAGENAME` x1. The source-free artifact is `corpus/candidates/source-edition-traces/gorky-klim-samgin-ru.poemx1-template.transclusion.json`; the dedicated historical-template workflow re-fetches oldid `5142743`, regenerates the artifact and byte-compares it with the committed record.

This does **not** establish template parameter/frame expansion, magic-word expansion, parser-function behavior, `#tag:poem` rendering, historical render equivalence, resolved Part 2 bytes, literary-body extraction/composition, or FantLab input identity. Issue #109 remains open. M2 remains **0/5 source-matched works**.

Next trigger: an independent later-run review of exact PR #113 head and checks. If clean, merge the bounded prerequisite without closing #109, then continue only with the evidenced remaining parser/magic-word/extension layer.
