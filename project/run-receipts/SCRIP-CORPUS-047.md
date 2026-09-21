# Run receipt — SCRIP-CORPUS-047

## Unit

- Issue: #181 — freeze Darwin/Rachinsky `{{ё}}` documentation evidence boundary.
- Base at selection: `master@ead874a699c9f1a98c100974835f1ffd6601a21e`.
- Branch: `scrip-corpus-047-darwin-yo-evidence`.
- Mode: bounded corpus/provenance + renderer-prerequisite research.

## Research evidence

Official Russian Wikisource documentation at `Шаблон:ЕЁ/Документация`, permanent revision `oldid=5090323` (2024-01-11), documents no-argument `{{ё}}` as a conditional lowercase shorthand: forced yoification -> `ё`; otherwise -> `е`. Current `Справка:Вычитка` separately describes `{{ё}}` / `{{ё!}}` as the yoification mechanism used to support two finished-text variants.

The retained Darwin Page-revision evidence predates that documentation revision. The deterministic witness selected from shard 01 is Page sequence 11 / revision `3358032` / `2018-08-13T19:18:33Z` / MediaWiki SHA-1 `3fe692545a92d2103d667ce02dd7237889fa2ccc`. Therefore current official documentation is useful semantic evidence but is not proof of historical template/dependency equivalence for the frozen Page revisions.

## Produced

- `scriptorium/darwin_template_yo_evidence.py`
- `tests/test_darwin_template_yo_evidence.py`
- `.github/workflows/darwin-template-yo-evidence.yml`
- source-free structured evidence `corpus/candidates/source-edition-traces/darwin-origin-species-rachinsky-1864-ru.template-yo-evidence.json`
- public semantic-backlog companion update
- changelog/state handoff for independent review

Canonical evidence SHA-256: `3c0af5dfe8d23cd6d47ce2f92b30c58b83e352df692c18e6d4f59a14928eb06a`.

## Boundary / gates

The render profile and existing semantic backlog are intentionally unchanged. Template `ё` remains unresolved in the renderer profile/backlog because historical template revision/dependency identity is not yet frozen. All 43 unresolved shapes remain. Renderer implementation/equivalence, inter-page composition, literary-body counts/digests, >=300k admission, FantLab source match, diagnostic readiness and M2 parity remain closed; M2 remains 0/5.

## Verification handoff

The authored unit must be handed off as a Draft PR. Exact-head workflow results and artifact identity are appended after the PR head is settled. This authored run does not self-approve or merge the change.
