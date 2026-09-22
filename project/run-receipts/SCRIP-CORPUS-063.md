# Run receipt — SCRIP-CORPUS-063

- **Unit:** SCRIP-CORPUS-063 — canonicalize Darwin `{{ё}}` replay root identity
- **Issue:** #213
- **Pull request:** #214 (Draft; independent review pending)
- **Base:** `master@e03bc63d9b7747fcae8f704f097357bb6ad12160`
- **Branch:** `scrip-corpus-063-darwin-yo-canonical-root`
- **Scope:** `drevendev/Scriptorium` only

## Produced

This bounded correctness/provenance slice repairs the exact template-root identity required by the Darwin/Rachinsky version-pinned replay contract before any recursive dependency binding is attempted.

MediaWiki `Manual:Page naming/en` permanent revision `8270202` documents default first-character capitalization and canonical page-name form. Russian Wikisource permanent revision `5687302` identifies the shorthand template page canonically as `Шаблон:Ё`; permanent revision `3684646` identifies the conditional root as `Шаблон:ЕЁ`. The source invocation spelling remains `{{ё}}`, but exact replay dependency identity now requires canonical page title `Шаблон:Ё`.

The replay contract is upgraded to `scriptorium-darwin-template-yo-replay-contract-v2` and regenerated source-free with contract SHA-256 `9b2e8914a5b4c3518ef331c27dc09a6a30d4d6433e90169c677348048f3dcd52`. Root-page observations intentionally record `mediawiki_sha1_bound=false`: this unit does not claim complete dependency identity or recursive closure.

## Verification

Focused local standard-library verification passes **19/19** `test_darwin_template_yo_replay_contract` tests. Coverage includes exact canonical contract rebuild, pinned title-canonicalization evidence, canonical root observations, explicit rejection of lowercase `Шаблон:ё` as a complete-closure root, stale discovery-digest rejection, graph-edge exactness, source-prose rejection and all downstream gate guards.

Hosted PR checks and exact-head review are intentionally left for the next independent judgement run because this wake authored the substantive contract correction.

## Gates / handoff

- `dependency_closure_complete=false`
- root MediaWiki content SHA-1 identities are not yet bound
- recursive direct-dependency closure remains unfrozen
- deterministic forced/non-forced outputs remain unverified
- renderer rule promotion remains false
- literary-body / >=300k admission remains false
- `fantlab_source_edition_match=unknown`
- `m2_parity_admissible=false`
- M2 remains **0/5**

Next action: independently review Draft PR #214 at its exact final head against the then-current `master`, inspect hosted checks, and only mark Ready/merge if the canonical-title correction and fail-closed gates remain sound.
