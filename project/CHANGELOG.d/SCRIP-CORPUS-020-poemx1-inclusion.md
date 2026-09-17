# SCRIP-CORPUS-020 — `poemx1` partial-transclusion semantics

- Date: 2026-09-17
- Issue: #109
- PR: #113 (merged)
- Merge commit: `5894878398a8ceba952279c69aaf9b5ab8ebae81`
- Status: `POEMX1_INCLUSION_MERGED_CONTINUATION_OPEN`
- Scope: bounded corpus/provenance prerequisite; no literary-body or M2 promotion.

Scriptorium now has a source-free implementation of the documented MediaWiki partial-transclusion control layer. The profile applies `noinclude`, `includeonly` and `onlyinclude` selection semantics and fails closed on malformed control markup and `nowiki`, whose special MediaWiki behavior is outside this bounded profile. The implementation is backed by focused standard-library tests and cites the official MediaWiki `Help:Transclusion` / `Help:Templates` semantics.

Applied to the pinned inferred historical anchor `Шаблон:Poemx1` oldid `5142743`, exact replay evidence records two `noinclude` pairs, one `includeonly` pair and no `onlyinclude` pair. After inclusion selection the raw `doc` invocation, documentation `templatedata` surface and raw `PAGENAME` occurrence disappear from the effective transclusion graph. No ordinary template transclusion or magic-word dependency remains.

The remaining unresolved graph is `#expr` x2, `#if` x5, `#ifeq` x5, `#iferror` x1, and `#tag` x1 targeting `poem`. The source-free artifact is `corpus/candidates/source-edition-traces/gorky-klim-samgin-ru.poemx1-template.transclusion.json`; the dedicated historical-template workflow re-fetches oldid `5142743`, regenerates the artifact and byte-compares it with the committed record.

The first authored-head run `35237044297` passed all **198** standard-library tests, historical revision capture, raw-shape probe and inclusion preprocessing, then deliberately failed at final byte comparison because the hand-authored artifact had incorrectly retained `PAGENAME`. Workflow-generated evidence established that `PAGENAME` lies in excluded content, and the artifact/public wording were repaired. Final exact head `0ecc213bed00e0d3d6a07cfc9df5b61531cd38c6` then passed workflows `35237513685` (historical template dependency), `35237513588` (Klim source revisions), `35237513275` (Pages), `35237513456` (frozen diagnostic), and `35237513785` (pinned pylem provider).

An independent later-run review found no blocking defect, re-checked the official MediaWiki semantics, confirmed the PR was 15 commits ahead / 0 behind with 9 changed files and no inline review threads, marked PR #113 Ready, and squash-merged it as `5894878398a8ceba952279c69aaf9b5ab8ebae81`.

This does **not** establish template parameter/frame expansion, parser-function behavior, `#tag:poem` rendering, historical render equivalence, resolved Part 2 bytes, literary-body extraction/composition, or FantLab input identity. Issue #109 remains open. M2 remains **0/5 source-matched works**.

Next trigger: continue Issue #109 with only the evidenced remaining parameter/frame/parser/extension layer; do not record resolved Part 2 or composite body digests until that expansion replays deterministically.
