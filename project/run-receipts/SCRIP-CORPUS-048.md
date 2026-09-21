# SCRIP-CORPUS-048 run receipt

- Unit: `SCRIP-CORPUS-048`
- Issue: #183 (closed completed)
- Pull request: #184 (squash-merged as `634331346f1afadd26c054f9f09b6ada71d964b2`)
- Base: `master@c2bb1bfe693867b44f8a6bf48e94e0a31cee99ad`
- Authored branch: `scrip-corpus-048-template-dependency-model`
- Exact reviewed PR head: `cb725ba8f8df5cc0ebdacbf0441ff6451a1c94c0`
- Independent review: COMMENT review `5265215135`

## Decision advanced

Official MediaWiki rendering/transclusion documentation corrects the prior research prerequisite for Darwin/Rachinsky `{{ё}}`: an old Page `oldid` fixes the Page revision/wikitext identity, but it does not pin historical template revisions for the rendered view. The dependency identity that matters to a deterministic replay is the exact template graph used by the chosen replay environment, unless Scriptorium deliberately supplies its own version-pinned expansion mechanism.

Source-free evidence is pinned to:

- MediaWiki `Help:History`, permanent revision `oldid=8524540` (2026-07-25);
- MediaWiki `Transclusion/en`, permanent revision `oldid=8551508` (2026-08-09), including the versioned-transclusion gap reference `T31051`;
- Russian Wikisource `Шаблон:ЕЁ/Документация`, `oldid=5090323`;
- Russian Wikisource `Справка:Вычитка`, `oldid=5731079`.

The deterministic evidence artifact is schema `scriptorium-darwin-template-yo-documentation-evidence-v2`, canonical SHA-256 `d92bdfcad71aaa8a50f9f35b5b1ada462ed41619400c40576d0603cf154877dc`.

## Independent review and verification

The later judgement run re-read exact head `cb725ba8f8df5cc0ebdacbf0441ff6451a1c94c0` against unchanged base `c2bb1bfe693867b44f8a6bf48e94e0a31cee99ad`: 8 commits ahead / 0 behind, 8 changed files, no review threads. All 15 PR-triggered workflows settled `success`.

Dedicated run `35580775932`, job `106272898196`, checked out the exact reviewed SHA, passed 10 template-yo evidence tests plus 5 semantic-backlog regressions, reproduced canonical evidence SHA-256 `d92bdfcad71aaa8a50f9f35b5b1ada462ed41619400c40576d0603cf154877dc`, and uploaded artifact `10630062217`.

The artifact was independently downloaded and verified as a 1,965-byte ZIP with SHA-256 `023392ca893de3a8ac9e3eb04e160a4fdc0b1deed0e5ac6b530043547e6c6a2d`. It contains exactly one 4,307-byte source-free JSON with SHA-256 `dd5dba3cb20827f3b163a59ca133e82e997158faf5f0be3506690c0a8d4b61ad`; recomputing its canonical self-digest reproduced `d92bdfcad71aaa8a50f9f35b5b1ada462ed41619400c40576d0603cf154877dc`.

Pages run `35580775985`, job `106272898492`, checked out the same exact head, passed the full 391-test standard-library suite, canonical site build and deterministic rebuild; deployment remained intentionally skipped.

No merge blockers were found. PR #184 was marked Ready and squash-merged with an expected-head guard as `634331346f1afadd26c054f9f09b6ada71d964b2`, which closed Issue #183 completed.

## Boundary preserved

`{{ё}}` remains `semantic_status=unresolved`; no render-profile row is promoted or removed from the semantic backlog. All 43 unresolved shapes remain present. The next prerequisite is to freeze exact `Шаблон:ё` / `Шаблон:ЕЁ` revisions and nested dependencies used by the selected replay environment at analysis time, or use an explicitly version-pinned expansion mechanism and validate its conditional outputs.

No Page prose, template source bodies, rendered literary prose, OCR or scan bytes were committed. `renderer_semantics_complete=false`, `renderer_implementation_ready=false`, `inter_page_composition_frozen=false`, `literary_body_count_and_digests_frozen=false`, `minimum_300k_proved=false`, `admitted_for_calibration=false`, `diagnostic_ready=false`, `m2_parity_admissible=false`, and `fantlab_source_edition_match=unknown` remain unchanged. M2 remains 0/5.

## Handoff

SCRIP-CORPUS-048 is complete. Resume normal-flow selection from the queue. A later bounded Darwin/Rachinsky renderer unit may freeze the exact replay-time `Шаблон:ё` / `Шаблон:ЕЁ` dependency graph (including nested dependencies) or implement explicit version-pinned expansion before any renderer-profile promotion.
