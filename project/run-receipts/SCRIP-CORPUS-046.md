# Run receipt — SCRIP-CORPUS-046

Status: `REVIEW_PENDING`

Issue: #179  
Draft PR: #180  
Base at selection: `master@11a06cb619e53810cb7cf3daa104488b28262613`

## Unit

Freeze a deterministic source-free priority backlog for the unresolved Darwin/Rachinsky 1864 rendering-semantic surface already frozen by SCRIP-CORPUS-045. This unit prioritizes evidence work; it does not resolve template/reference/math/inter-page semantics or implement a renderer.

## Produced

- `scriptorium/darwin_semantic_backlog.py` — validates the existing render profile against its frozen surface, preserves every unresolved shape, groups them by evidence track, ranks them deterministically, and validates the derived backlog.
- `darwin-origin-species-rachinsky-1864-ru.semantic-backlog.json` — canonical source-free backlog, SHA-256 `4ec4f84566f5f3f8dccd1945906d1a782f4532547a13cadc8570cb5b682bdcb2`.
- `tests/test_darwin_semantic_backlog.py` — rebuild, coverage, deterministic-next-target, drift and gate-boundary regressions.
- `.github/workflows/darwin-semantic-backlog.yml` — exact-head deterministic rebuild/artifact verification.
- public companion page `corpus/candidates/darwin-origin-species-rachinsky-1864-ru-semantic-backlog.md`.

## Frozen findings

The backlog preserves exactly 5 unresolved tag shapes / 518 tag tokens and 38 unresolved template shapes / 4,583 invocations. Tracks are provider-template 37 shapes / 4,579 occurrences, provider-reference 3 / 466, provider-math 2 / 52, and inter-page 1 / 4.

The deterministic next research target is template `ё`, arity 0 positional / 0 named, with 2,227 observed invocations. Its `semantic_status` remains `unresolved`; the ranking is not evidence of its behavior.

## Verification / repair history

The first PR-triggered run on head `b69bce39a35297c305c8267868fecbb2577d7787` correctly failed because one regression expected the wrong existing validator error string (`profile digest drift` versus `Darwin/Rachinsky rendering profile drift`). The test expectation was repaired in commit `e62e4401807037afdeec2d0714bd5176e94da24b`; no production boundary was weakened. Final exact-head workflow settlement is recorded in the PR handoff comment after all authored commits.

## Gates

No Page wikitext, template arguments, rendered prose, OCR, scan bytes or literary text are persisted. `renderer_semantics_complete=false`, `renderer_implementation_ready=false`, `inter_page_composition_frozen=false`, `literary_body_count_and_digests_frozen=false`, `minimum_300k_proved=false`, `admitted_for_calibration=false`, `fantlab_source_edition_match=unknown`, `diagnostic_ready=false`, and `m2_parity_admissible=false`. M2 remains 0/5.

## Handoff

Do not merge from this authored run. A later independent wake must read PR #180 at its exact final head, inspect all settled checks and the source-free artifact, review the diff, and only then decide Ready/merge. If accepted, the next renderer-research slice should investigate template `ё` with independent provider/history evidence rather than inferring semantics from its name.
