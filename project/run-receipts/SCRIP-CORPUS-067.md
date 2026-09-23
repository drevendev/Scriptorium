# Run receipt — SCRIP-CORPUS-067

- **Unit:** SCRIP-CORPUS-067 — capture controlled `Модуль:String` replay observation
- **Issue:** #222 (open)
- **Pull request:** #223 (Draft; independent exact-head judgement required)
- **Authoring base:** `master@c2dc938049e77327691c06ae3be99f8f77efc6b2`
- **Branch:** `scrip-corpus-067-module-string-observation`
- **Scope:** `drevendev/Scriptorium` only

## Produced

The bounded unit implements the next provenance prerequisite from reviewed SCRIP-CORPUS-066 without backdating a child dependency from caller/root timestamps. A new source-free builder/validator accepts only a controlled metadata-only MediaWiki response and records the canonical dependency title, exact revision ID, revision timestamp, MediaWiki SHA-1, API-server observation time and exact query semantics. It is cryptographically bound to reviewed replay contract v4 SHA-256 `f5a021fe544bb74f8f7a493bf20c7005f5a79c9c7b78eb10c86ff93a86b26e64` and selection policy SHA-256 `4a58b70d5935f4455e58a929c6c1b6cc6a527d7b9d63121e0023501055889855`.

The PR workflow now queries Russian Wikisource with `curtimestamp=1`, `titles=Модуль:String`, `rvprop=ids|timestamp|sha1`, and no source-content field. It uploads only the derived source-free observation and keeps the existing v4/root verification intact.

The first controlled PR-head observation was captured by workflow run `35824984270` at exact implementation head `ac66046276c2167bcf92c03fd7cc7c71afbd6228`:

- canonical title: `Модуль:String`
- exact revision: `3684569`
- revision timestamp: `2019-06-04T20:18:11Z`
- MediaWiki SHA-1: `a34727a1e4ec3c4b4c7ec556c94991f75442d99c`
- API server observation time: `2026-09-23T06:03:11Z`
- observation SHA-256: `e60fc5e4f59164e98114024a4464f377f0684673be979e0fe18ed7b1fb9070bc`

That exact source-free observation is committed as `corpus/candidates/source-edition-traces/darwin-origin-species-rachinsky-1864-ru.module-string-observation-v1.json`. It deliberately records `module_string_identity_observed=true` and `module_string_identity_bound=false`: a point-in-time current revision observation is not historical-transclusion provenance and does not silently rewrite replay contract v4.

## Verification

- Dedicated workflow run `35824984270` checked out exact implementation SHA `ac66046276c2167bcf92c03fd7cc7c71afbd6228`.
- The focused suite completed **32/32** tests successfully before reconciliation of the committed observation artifact; the follow-up exact-head workflow is expected to include the added committed-artifact regression.
- v4 rebuilt byte-for-byte to canonical SHA-256 `f5a021fe544bb74f8f7a493bf20c7005f5a79c9c7b78eb10c86ff93a86b26e64`.
- selection policy validated at canonical SHA-256 `4a58b70d5935f4455e58a929c6c1b6cc6a527d7b9d63121e0023501055889855`.
- both exact historical root revisions were re-queried and source-free scan observations matched the frozen v4 contract.
- the controlled module observation artifact was uploaded as Actions artifact `10734758059`; ZIP SHA-256 `c5a070d7cb3ade23d7a8a97a561392802ce81fdf519563aafacb6c1c00b0d4ff`.

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

SCRIP-CORPUS-067 is authored in Draft PR #223. After all exact-head PR checks settle, the next wake should independently review the complete head and either merge or repair. Only after reviewed merge may a later bounded unit decide whether to bind the observed `Модуль:String@3684569` identity into a successor replay contract and recursively freeze that exact module revision's direct dependencies.
