# Run receipt — SCRIP-CORPUS-046

Status: `COMPLETE`

Issue: #179 (`closed`, `completed`)  
PR: #180 (`squash-merged`)  
Base at selection: `master@11a06cb619e53810cb7cf3daa104488b28262613`  
Final independently reviewed head: `6b9f17c8c2d86e1920c63017325deabecd68dab0`  
Squash merge: `10ae3c380bfe468e684625f912540392fff9dda1`

## Unit

Freeze a deterministic source-free priority backlog for the unresolved Darwin/Rachinsky 1864 rendering-semantic surface already frozen by SCRIP-CORPUS-045. This unit prioritizes evidence work; it does not resolve template/reference/math/inter-page semantics or implement a renderer.

## Produced

- `scriptorium/darwin_semantic_backlog.py` — validates the existing render profile against its frozen surface, preserves every unresolved shape, groups them by evidence track, ranks them deterministically, and validates the derived backlog.
- `darwin-origin-species-rachinsky-1864-ru.semantic-backlog.json` — canonical source-free backlog, SHA-256 `4ec4f84566f5f3f8dccd1945906d1a782f4532547a13cadc8570cb5b682bdcb2`.
- `tests/test_darwin_semantic_backlog.py` — rebuild, coverage, deterministic-next-target, drift and gate-boundary regressions.
- `.github/workflows/darwin-semantic-backlog.yml` — exact-head deterministic rebuild/artifact verification.
- public companion page `corpus/candidates/darwin-origin-species-rachinsky-1864-ru-semantic-backlog.md`.
- canonical candidate page `corpus/candidates/darwin-origin-species-rachinsky-1864-ru.md` links and summarizes the backlog while preserving closed downstream gates.
- `project/STATE_AND_QUEUE.md` records the unit as complete for stateless recovery.

## Frozen findings

The backlog preserves exactly 5 unresolved tag shapes / 518 tag tokens and 38 unresolved template shapes / 4,583 invocations. Tracks are provider-template 37 shapes / 4,579 occurrences, provider-reference 3 / 466, provider-math 2 / 52, and inter-page 1 / 4.

The deterministic next research target is template `ё`, arity 0 positional / 0 named, with 2,227 observed invocations. Its `semantic_status` remains `unresolved`; the ranking is not evidence of its behavior.

## Verification / repair history

The first PR-triggered run on head `b69bce39a35297c305c8267868fecbb2577d7787` correctly failed because one regression expected the wrong existing validator error string (`profile digest drift` versus `Darwin/Rachinsky rendering profile drift`). The test expectation was repaired in commit `e62e4401807037afdeec2d0714bd5176e94da24b`; no production boundary was weakened. The authored exact-head handoff for `b1e7e63afcf293cc31d827ea9a526cec216223ac` recorded the dedicated backlog workflow, Pages workflow and frozen diagnostic as green.

Independent review COMMENT `5262708679` on that exact authored head found two acceptance/recoverability blockers outside the backlog semantics: canonical state still pointed at completed SCRIP-CORPUS-045, and the canonical Darwin candidate page still called merged PR #178 Draft while omitting the new semantic-backlog artifact. Recovery commits repaired both surfaces and moved the final head to `6b9f17c8c2d86e1920c63017325deabecd68dab0`.

Independent exact-head review COMMENT `5263138005` then re-read the repaired head against unchanged `master@11a06cb619e53810cb7cf3daa104488b28262613`. The branch was 12 commits ahead / 0 behind with 9 changed files and no inline review threads. All 17 PR-triggered workflows were settled `success`.

Dedicated semantic-backlog run `35558923116` / job `106207897514` checked out the exact reviewed SHA, passed 5 backlog tests plus 7 render-profile regressions, and deterministically rebuilt the canonical backlog digest. Artifact `10621286959` was independently downloaded: 1,819-byte ZIP SHA-256 `ca48ccf69f1ca97a6447befa7ed9525cef56fa61d8e60897ecabcbf257d4861b`, containing only the 14,228-byte source-free JSON SHA-256 `ccd04869f0ade3aa7184ade3f6000ef8bc5d5ddc42cf376e1370ab4249a983f2`; its embedded canonical backlog SHA-256 independently recomputed to `4ec4f84566f5f3f8dccd1945906d1a782f4532547a13cadc8570cb5b682bdcb2`.

Pages run `35558923123` / job `106207907003` checked out the same exact SHA, passed the full 381-test standard-library suite, built the canonical static site, reproduced it deterministically, and intentionally skipped live deployment.

The final review was a COMMENT rather than self-approval. With no remaining blocker, PR #180 was marked Ready and squash-merged as `10ae3c380bfe468e684625f912540392fff9dda1`, automatically closing Issue #179 as `completed`.

## Gates

No Page wikitext, template arguments, rendered prose, OCR, scan bytes or literary text are persisted. `renderer_semantics_complete=false`, `renderer_implementation_ready=false`, `inter_page_composition_frozen=false`, `literary_body_count_and_digests_frozen=false`, `minimum_300k_proved=false`, `admitted_for_calibration=false`, `fantlab_source_edition_match=unknown`, `diagnostic_ready=false`, and `m2_parity_admissible=false`. M2 remains 0/5.

## Handoff

Resume normal-flow selection from the queue. If a later bounded Darwin/Rachinsky renderer-research unit is selected, investigate template `ё` using independent provider/history evidence rather than inferring semantics from its name or prevalence. Reference/math behavior and inter-page composition remain separate unresolved tracks; body identity, >=300k admission and FantLab/M2 gates remain closed until separately evidenced and reviewed.
