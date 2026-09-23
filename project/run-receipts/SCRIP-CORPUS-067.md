# Run receipt — SCRIP-CORPUS-067

- **Unit:** SCRIP-CORPUS-067 — capture controlled `Модуль:String` replay observation
- **Issue:** #222 (closed completed)
- **Pull request:** #223 (independently reviewed; squash-merged as `42eb7392d0f91c68f100258d2d304fbe01ec4b46`)
- **Authoring base:** `master@c2dc938049e77327691c06ae3be99f8f77efc6b2`
- **Reviewed head:** `de30a72308920ae35ccb64a97f43d8dd09530abd`
- **Branch:** `scrip-corpus-067-module-string-observation`
- **Scope:** `drevendev/Scriptorium` only

## Produced

The bounded unit implements the next provenance prerequisite from reviewed SCRIP-CORPUS-066 without backdating a child dependency from caller/root timestamps. A new source-free builder/validator accepts only a controlled metadata-only MediaWiki response and records the canonical dependency title, exact revision ID, revision timestamp, MediaWiki SHA-1, API-server observation time and exact query semantics. It is cryptographically bound to reviewed replay contract v4 SHA-256 `f5a021fe544bb74f8f7a493bf20c7005f5a79c9c7b78eb10c86ff93a86b26e64` and selection policy SHA-256 `4a58b70d5935f4455e58a929c6c1b6cc6a527d7b9d63121e0023501055889855`.

The PR workflow queries Russian Wikisource with `curtimestamp=1`, `titles=Модуль:String`, `rvprop=ids|timestamp|sha1`, and no source-content field. It uploads only the derived source-free observation and keeps the existing v4/root verification intact.

The first controlled PR-head observation was captured by workflow run `35824984270` at exact implementation head `ac66046276c2167bcf92c03fd7cc7c71afbd6228`:

- canonical title: `Модуль:String`
- exact revision: `3684569`
- revision timestamp: `2019-06-04T20:18:11Z`
- MediaWiki SHA-1: `a34727a1e4ec3c4b4c7ec556c94991f75442d99c`
- API server observation time: `2026-09-23T06:03:11Z`
- observation SHA-256: `e60fc5e4f59164e98114024a4464f377f0684673be979e0fe18ed7b1fb9070bc`

That exact source-free observation is committed as `corpus/candidates/source-edition-traces/darwin-origin-species-rachinsky-1864-ru.module-string-observation-v1.json`. It deliberately records `module_string_identity_observed=true` and `module_string_identity_bound=false`: a point-in-time current revision observation is not historical-transclusion provenance and does not silently rewrite replay contract v4.

## Verification

- Initial dedicated workflow run `35824984270` checked out exact implementation SHA `ac66046276c2167bcf92c03fd7cc7c71afbd6228` and completed 32 focused tests before the committed-artifact reconciliation commit.
- Final exact-head dedicated workflow run `35825414712` checked out `de30a72308920ae35ccb64a97f43d8dd09530abd` and completed **33/33** focused regressions successfully, including the committed observation validation.
- All **21/21** PR-triggered workflows on the exact reviewed head completed with `success`.
- v4 rebuilt byte-for-byte to canonical SHA-256 `f5a021fe544bb74f8f7a493bf20c7005f5a79c9c7b78eb10c86ff93a86b26e64`.
- selection policy validated at canonical SHA-256 `4a58b70d5935f4455e58a929c6c1b6cc6a527d7b9d63121e0023501055889855`.
- both exact historical root revisions were re-queried and source-free scan observations matched the frozen v4 contract.
- the final exact-head workflow repeated the metadata-only module observation and again obtained `Модуль:String@3684569`, revision timestamp `2019-06-04T20:18:11Z`, MediaWiki SHA-1 `a34727a1e4ec3c4b4c7ec556c94991f75442d99c`; its fresh observation digest differed only because the recorded API `curtimestamp` changed.
- independent review `5287770865` found no merge blocker or open review thread after re-reading all 8 changed files and current MediaWiki API evidence.

## Merge / durable result

PR #223 was marked Ready and squash-merged with expected-head protection as `42eb7392d0f91c68f100258d2d304fbe01ec4b46`, closing Issue #222 completed. Bookkeeping advanced canonical state to `STATE_REVISION: 249` and returned the queue to normal-flow SCRIP-CORPUS continuation.

## Gates / handoff

- `Модуль:String` exact identity is **observed but not yet bound** into a replay contract.
- Caller/root timestamps remain forbidden dependency revision selectors.
- `dependency_closure_complete=false`.
- forced/non-forced output verification remains open.
- renderer rule promotion remains false.
- literary-body / >=300k admission remains false.
- `fantlab_source_edition_match=unknown`.
- `m2_parity_admissible=false`.
- M2 remains **0/5**.

SCRIP-CORPUS-067 is complete. A later bounded Darwin replay unit may explicitly select/bind the observed `Модуль:String@3684569` identity (or another separately justified revision) into a successor contract and recursively freeze that exact module revision's direct dependencies. The retained point-in-time observation must not be reinterpreted as historical transclusion provenance.
