# Run receipt — SCRIP-CORPUS-081

Status: COMPLETE

## Orientation

- Connected GitHub identity: `andy-zen-dev`.
- Repository: `drevendev/Scriptorium`; write permission available.
- Exact authoring base: `404a9b2c0b6c0153f315b09a8bbef5935c5bf879`.
- Exact final authored head: `c5e2c4c89ddf7d6f5090843ce1d546e5e7ad92e1`.
- Issue: #251.
- PR: #252.

## Produced

- Revision-pinned source-free `{{ВАР}}` documentation/implementation-module evidence.
- Deterministic builder/validator and eight focused regressions.
- Public semantic-backlog companion update.
- No render-profile or semantic-backlog promotion.

Evidence SHA-256: `321ced32bb7ffc75829b6fbb5255bce3243641a80c21ad4e2b7bb7a25138502d`.

## Research evidence

- `Шаблон:ВАР/Документация@5711068` documents parameter 1 as pre-reform text and parameter 2 as modern text and identifies `Модуль:Дореформенная орфография` as the implementation module.
- `Модуль:Дореформенная орфография@5721277` has separate Page/non-Page behavior and directly requires `Module:Header` for non-Page title classification.
- Independent review rechecked the current Russian Wikisource documentation and module surfaces; both corroborated the retained semantic statements while not supplying historical-transclusion or candidate-context replay proof.

## Evidence boundary

This unit does not freeze the live `Шаблон:ВАР` root, `Module:Header` revision/nested closure, candidate mainspace title/context, historical transclusion, or an offline/version-pinned MediaWiki runtime. `ВАР` remains unresolved; no render-profile or semantic-backlog promotion occurs.

## Verification

- Independent review `5301756253` re-read all 8 changed files at exact head `c5e2c4c89ddf7d6f5090843ce1d546e5e7ad92e1` against unchanged base `404a9b2c0b6c0153f315b09a8bbef5935c5bf879`; no merge blocker or open review thread was found.
- All 24 PR-triggered workflow runs visible for that exact head completed `success`.
- Dedicated exact-head run `35973919107` checked out the exact SHA, passed 8/8 focused regressions, deterministically rebuilt the committed evidence and verified evidence SHA-256 `321ced32bb7ffc75829b6fbb5255bce3243641a80c21ad4e2b7bb7a25138502d`.
- Artifact `10796629637` independently re-hashed to ZIP SHA-256 `2c0a57380a94aa114c5c8e7bea340af59800f782108c070e50e3e5901d7db83a`, matching GitHub; the contained JSON self-digest independently recomputed to the committed evidence digest.
- Frozen diagnostic run `35973919110` completed `success`; both replay jobs and their standard-library test steps were green.

## Merge

PR #252 was marked Ready after the independent judgement and squash-merged with expected-head protection as `9639f1bace28a4a7ddef84ff4e04390a9de23e23`. Issue #251 closed completed.

## Next action

Resume normal-flow P2 SCRIP-CORPUS selection. Any later `ВАР` promotion requires a separately bounded unit that freezes the exact template/module/Header replay-time dependency graph and replays the candidate mainspace title/context.

## Gates

`renderer_semantics_complete`, `renderer_implementation_ready`, `inter_page_composition_frozen`, `literary_body_count_and_digests_frozen`, `minimum_300k_proved`, `admitted_for_calibration`, `diagnostic_ready`, and `m2_parity_admissible` remain false; `fantlab_source_edition_match=unknown`. M2 remains 0/5.
