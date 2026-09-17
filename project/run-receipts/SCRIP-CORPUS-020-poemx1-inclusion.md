# Run receipt — SCRIP-CORPUS-020 `poemx1` inclusion semantics

- Date: 2026-09-17
- Issue: #109
- PR: #113 (merged)
- Branch: `scrip-corpus-020-poemx1-inclusion-semantics`
- Base at selection: `d33e8e7b89530487c493c9283ce48ff9613f121a`
- Reviewed exact head: `0ecc213bed00e0d3d6a07cfc9df5b61531cd38c6`
- Merge commit: `5894878398a8ceba952279c69aaf9b5ab8ebae81`
- Result: `POEMX1_INCLUSION_MERGED_CONTINUATION_OPEN`

## Bounded unit

Apply and freeze the documented MediaWiki `noinclude` / `includeonly` / `onlyinclude` transclusion-selection layer to pinned `Шаблон:Poemx1` oldid `5142743`, then derive the effective unresolved dependency classes without attempting parser-function or extension rendering.

## Evidence and implementation

Official MediaWiki help documents the relevant semantics: `noinclude` is excluded from transclusion; `includeonly` participates; if `onlyinclude` is present, content outside it is discarded even when wrapped in `includeonly`. `scriptorium/mediawiki_transclusion.py` implements only this selection layer. It rejects malformed/crossing control tags and fails closed on `nowiki` because MediaWiki assigns special inclusion behavior inside `nowiki` that is outside this bounded profile.

Focused standard-library tests cover `noinclude` removal, `includeonly` retention, `onlyinclude` precedence/multiple blocks, self-closing controls, malformed/nowiki fail-closed behavior, source-free manifest boundaries, and dependency classification.

The pinned source-free observed contract is:

- source template: `Шаблон:Poemx1`, oldid `5142743`, wikitext SHA-256 `fa7e35686da5ce4c62986a7e8bfc72f2dba067118218d656b2f0983e5cfa06db`
- control tags: `noinclude` pairs x2; `includeonly` pairs x1; `onlyinclude` pairs x0
- effective ordinary template transclusions: none (`doc` is excluded)
- effective magic-word dependencies: none (the raw `PAGENAME` occurrence is also excluded)
- unresolved parser functions: `#expr` x2, `#if` x5, `#ifeq` x5, `#iferror` x1, `#tag` x1
- unresolved extension target: `poem` x1
- remaining HTML-like `div` tags: x6

The dedicated workflow fetches exact oldid `5142743`, regenerates the source-free post-inclusion artifact and byte-compares it with `gorky-klim-samgin-ru.poemx1-template.transclusion.json` in addition to replaying the existing historical revision/shape evidence.

## Fail-closed correction during authoring

Initial authored-head workflow `35237044297` checked out `087771d0449698a22a422255d75c409c061fd553`, passed **198** standard-library tests, required the six-`poemx1` Part 2 shape, re-resolved historical oldid `5142743`, regenerated the raw shape and successfully applied the inclusion profile. The final byte comparison then failed because the first hand-authored post-inclusion artifact had retained `PAGENAME` while the generated artifact correctly had `magic_word_counts = {}`. Exact replay established that `PAGENAME` is inside excluded content, and the artifact plus public/durable wording were repaired from that evidence.

## Independent later-run review and merge

Independent review used exact head `0ecc213bed00e0d3d6a07cfc9df5b61531cd38c6`. The PR was mergeable, 15 commits ahead / 0 behind `master`, changed the expected 9 files and had no inline review threads. Official MediaWiki help was re-checked and supported the bounded control semantics used by the implementation.

All five exact-head workflows were successful:

- `35237513685` — Klim Samgin historical template dependency
- `35237513588` — Klim Samgin source revisions
- `35237513275` — Scriptorium Pages
- `35237513456` — Scriptorium frozen diagnostic
- `35237513785` — Scriptorium pinned pylem provider

The dedicated historical-template job checked out exact head `0ecc213bed00e0d3d6a07cfc9df5b61531cd38c6`, re-resolved oldid `5142743`, regenerated raw-shape and post-inclusion evidence, byte-compared committed evidence, and replayed the exact historical revision. No blocking review defect was found. PR #113 was marked Ready and squash-merged as `5894878398a8ceba952279c69aaf9b5ab8ebae81`.

## Boundary

`historical_render_equivalence_proven=false`. Parameter/frame expansion, parser functions, `#tag:poem`, resolved Part 2 bytes, candidate literary extraction/composition and raw/normalized body digests remain unfrozen. `fantlab_source_edition_match=unknown`; M2 remains **0/5**.

## Next action

Continue Issue #109 with the remaining evidenced MediaWiki parameter/frame/parser/extension layer. Only after deterministic replay of that expansion should resolved Part 2 bytes and the fail-closed four-part literary-body identity be recorded.
