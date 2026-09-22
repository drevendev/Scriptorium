# Run receipt — SCRIP-CORPUS-063

- **Unit:** SCRIP-CORPUS-063 — canonicalize Darwin `{{ё}}` replay root identity
- **Issue:** #213 (closed completed)
- **Pull request:** #214 (independently reviewed and squash-merged as `004beda91f30c7765fef68beb15222a888004584`)
- **Base:** `master@e03bc63d9b7747fcae8f704f097357bb6ad12160`
- **Reviewed head:** `9063f8471bdb55a69436c8f8f0b5113afa449094`
- **Branch:** `scrip-corpus-063-darwin-yo-canonical-root`
- **Scope:** `drevendev/Scriptorium` only

## Produced

This bounded correctness/provenance slice repairs the exact template-root identity required by the Darwin/Rachinsky version-pinned replay contract before any recursive dependency binding is attempted.

MediaWiki `Manual:Page naming/en` permanent revision `8270202` documents default first-character capitalization and canonical page-name form. Russian Wikisource permanent revision `5687302` identifies the shorthand template page canonically as `Шаблон:Ё`; permanent revision `3684646` identifies the conditional root as `Шаблон:ЕЁ`. The source invocation spelling remains `{{ё}}`, but exact replay dependency identity now requires canonical page title `Шаблон:Ё`.

The replay contract is upgraded to `scriptorium-darwin-template-yo-replay-contract-v2` and regenerated source-free with contract SHA-256 `9b2e8914a5b4c3518ef331c27dc09a6a30d4d6433e90169c677348048f3dcd52`. Root-page observations intentionally record `mediawiki_sha1_bound=false`: this unit does not claim complete dependency identity or recursive closure.

## Verification

Authoring-time focused standard-library verification passed **19/19** `test_darwin_template_yo_replay_contract` tests. Coverage includes exact canonical contract rebuild, pinned title-canonicalization evidence, canonical root observations, explicit rejection of lowercase `Шаблон:ё` as a complete-closure root, stale discovery-digest rejection, graph-edge exactness, source-prose rejection and all downstream gate guards.

Independent later-run review `5283588406` re-read all **7 changed files** at exact head `9063f8471bdb55a69436c8f8f0b5113afa449094` against unchanged `master@e03bc63d9b7747fcae8f704f097357bb6ad12160`; the branch was 7 commits ahead / 0 behind, no open review thread remained, and no merge blocker was found. All **21/21** PR-triggered workflow runs on that exact SHA settled `success`.

Dedicated Darwin/Rachinsky run `35777100385` checked out the exact reviewed head, ran the template-yo evidence/backlog regressions, deterministically rebuilt and compared the source-free evidence, and completed `success`. Fresh official MediaWiki documentation also still confirms default first-character capitalization/canonicalization, consistent with canonical dependency root `Шаблон:Ё` while invocation spelling remains `{{ё}}`.

PR #214 was then marked Ready and squash-merged with expected-head protection as `004beda91f30c7765fef68beb15222a888004584`; Issue #213 closed automatically as completed.

## Gates / completion

- `dependency_closure_complete=false`
- root MediaWiki content SHA-1 identities are not yet bound
- recursive direct-dependency closure remains unfrozen
- deterministic forced/non-forced outputs remain unverified
- renderer rule promotion remains false
- literary-body / >=300k admission remains false
- `fantlab_source_edition_match=unknown`
- `m2_parity_admissible=false`
- M2 remains **0/5**

This unit is complete. Resume normal-flow selection from the canonical queue; the next Darwin/Rachinsky replay slice must bind exact content SHA-1 identities and recursive discovery evidence before any renderer/body/parity promotion.
