# Run receipt — SCRIP-CORPUS-082

Status: COMPLETE

## Orientation

- Connected GitHub identity: `andy-zen-dev`.
- Repository: `drevendev/Scriptorium`; write permission available.
- Exact authoring base: `bd291227733155672f8dd6d9d3a634348615cdbe`.
- Exact final authored head: `5d396d3647d69779a0e321727bb6a0561a93d60b`.
- Issue: #253.
- PR: #254.

## Produced

- Source-free `{{ВАР}}` provider-drift contract after observing `Модуль:Header@5746249` later than the pinned VAR implementation module `5721277`.
- Deterministic replay only of the observed Header title-classification rule for the retained Darwin mainspace title, yielding `isPRS=false` and therefore second/modern-argument selection if the pinned module's non-Page branch is reached.
- Focused regressions plus a public source-free provider-drift companion.
- No render-profile or semantic-backlog promotion.

Evidence SHA-256: `6126adbc966c7120ca487fb940bd0e01aafa0d7350d332e6422edbf8b3846cb8`.

## Research evidence

- `Модуль:Header@5746249` is a 2026-09-10 Russian Wikisource revision, later than the already pinned `Модуль:Дореформенная орфография@5721277`.
- A 2026-09-08 Russian Wikisource forum discussion explicitly raised whether `{{ВАР}}` had broken after Header-related changes and noted the orthography module's Header dependency. This is retained only as provider-drift risk, not proof of a production outage.
- The observed Header `parse_title(..., "isPRS")` rule classifies retained title `О происхождении видов (Дарвин; Рачинский)/1864 (ВТ:Ё)` as `isPRS=false`.

## Evidence boundary

This unit does not freeze the live `Шаблон:ВАР` root revision, Header MediaWiki SHA-1, execution-relevant nested dependency closure, complete `{{ВАР}}` invocation replay, historical transclusion identity or an offline/version-pinned MediaWiki runtime. `ВАР` remains unresolved at 388 invocations; effective unresolved counts remain 4 tag shapes / 130 tokens and 37 template shapes / 2,356 invocations. Renderer promotion, literary-body identity, >=300k admission, FantLab analyzer-input identity and parity remain closed.

## Verification

- Independent review `5302746201` re-read all 7 changed files at exact head `5d396d3647d69779a0e321727bb6a0561a93d60b` against unchanged base `bd291227733155672f8dd6d9d3a634348615cdbe`; no merge blocker or open review thread was found.
- Fresh Russian Wikisource evidence independently corroborated the observed Header revision/date, the provider-drift warning boundary and the pinned orthography module's dependency on Header title classification.
- The committed source-free evidence self-digest independently recomputed to `6126adbc966c7120ca487fb940bd0e01aafa0d7350d332e6422edbf8b3846cb8`.
- All 22 PR-triggered workflow runs visible for that exact head completed `success`.
- Frozen-diagnostic run `35979105385` checked out the exact SHA; both jobs completed their standard-library test and frozen replay steps successfully.

## Merge

PR #254 was marked Ready after independent judgement and squash-merged with expected-head protection as `1e55d987b44b7159aaf0f6c308e4dee98f954e15`. Issue #253 closed completed.

## Next action

Resume normal-flow P2 SCRIP-CORPUS selection. A subsequent Darwin/Rachinsky `{{ВАР}}` replay unit must deliberately choose one coherent snapshot and freeze exact `Шаблон:ВАР`, `Модуль:Дореформенная орфография`, `Module:Header` identities including MediaWiki SHA-1 and the execution-relevant nested closure before replaying the candidate invocation. A later live Header must not be silently substituted as historical/equivalent provenance.

## Gates

`renderer_semantics_complete`, `renderer_implementation_ready`, `inter_page_composition_frozen`, `literary_body_count_and_digests_frozen`, `minimum_300k_proved`, `admitted_for_calibration`, `diagnostic_ready`, and `m2_parity_admissible` remain false; `fantlab_source_edition_match=unknown`. M2 remains 0/5.
