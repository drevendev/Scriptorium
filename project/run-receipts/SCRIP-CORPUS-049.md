# SCRIP-CORPUS-049 run receipt

- Unit: `SCRIP-CORPUS-049`
- Issue: #185
- Pull request: #186 (Draft; authored work, independent later review required)
- Base at selection: `master@dfd1eec6f559deb06adc1b3d37b0c8143f72a355`
- Authored implementation/state head verified before this receipt commit: `819beb850637286448da8988584c23f2a00e9adf`
- Final review head: read from PR #186 after this metadata-only receipt commit; do not infer it from this receipt.

## Decision

Official MediaWiki `API:Expandtemplates/ru` revision `oldid=6729113` documents `revid` as revision context for `{{REVISIONID}}` and similar variables, not as a historical transcluded-template version selector. TemplateSandbox direct title/text substitution is useful for controlled overrides but is not accepted as evidence that a recursively expanded dependency graph is closed. `Help:ExpandTemplates` documents recursive expansion.

The new source-free `scriptorium-darwin-template-yo-replay-contract-v1` therefore requires exact title, revision ID, revision timestamp and MediaWiki content SHA-1 for `Шаблон:ё`, `Шаблон:ЕЁ` and every nested template/module dependency before replay closure can be claimed. The committed contract intentionally binds zero dependencies and records no verified output hashes.

Canonical contract SHA-256: `9ac0e52c8253ef523aefe9fd54b8e90edf69095ac6f7c45ac2a0bbd584049e2b`.

## Verification

On exact authored head `819beb850637286448da8988584c23f2a00e9adf`, all 15 PR-triggered workflows settled `success`. `Scriptorium Pages` run `35591427137`, job `106306456624`, checked out that exact SHA, passed **400 tests, all OK** including all 9 new replay-contract tests, then passed canonical site build and deterministic rebuild. `Darwin/Rachinsky 1864 template yo evidence`, `Scriptorium frozen diagnostic`, and `Scriptorium pinned pylem provider` also settled `success` on the same head.

## Gates

`{{ё}}` remains `semantic_status=unresolved`; all 43 unresolved shapes remain in the backlog. `dependency_closure_complete=false`, both forced/non-forced replay-output hashes remain null, and renderer implementation/equivalence, inter-page composition, literary-body count/digests, >=300k admission, FantLab source match, diagnostic readiness and M2 parity remain closed. M2 remains 0/5.

## Handoff

PR #186 remains Draft because this run authored the substantive change. The next wake must independently re-read the exact current PR head and settled checks before any Ready/merge decision. No template source bodies, Page prose, rendered literary prose, OCR or scan bytes were committed.
