# Run receipt — SCRIP-CORPUS-064

- **Unit:** SCRIP-CORPUS-064 — bind exact MediaWiki SHA-1 identities for Darwin `{{ё}}` replay roots
- **Issue:** #215 (closed completed)
- **Pull request:** #216 (independently reviewed; squash-merged as `71571633819111790243a3a99591eea314be2f6f`)
- **Base:** `master@f8a0732ac3732510406fff7e4fe3b082b31b74ac`
- **Reviewed head:** `e7de3024fdda2c6afc9e12884112a5d849c56938`
- **Branch:** `scrip-corpus-064-bind-yo-root-sha1`
- **Scope:** `drevendev/Scriptorium` only

## Produced

This bounded provenance slice advances only the exact identity of the two canonical replay roots selected by the independently reviewed v2 contract. A read-only Russian Wikisource Action API query requested exact revision IDs with `rvprop=ids|timestamp|sha1` and no content payload.

The frozen source-free identities are:

- `Шаблон:Ё@5687302`, timestamp `2026-01-21T12:32:10Z`, MediaWiki SHA-1 `963c1796d693d5451cf0c0897c35bd7e5b327ae1`;
- `Шаблон:ЕЁ@3684646`, timestamp `2019-06-04T20:49:40Z`, MediaWiki SHA-1 `435bb2a412d8fb5962ccd5adc0ac2e03412fe109`.

The first hosted probe received HTTP 429. No bypass was attempted: the probe was retried with bounded curl retries, timeout, and an explicit project User-Agent; run `35789352220` then returned the exact metadata successfully. The temporary probe workflow was removed after the values were captured.

A narrow successor `scriptorium-darwin-template-yo-replay-contract-v3` validates the reviewed v2 predecessor SHA-256 `9b2e8914a5b4c3518ef331c27dc09a6a30d4d6433e90169c677348048f3dcd52`, binds only those two root identities, and preserves all downstream gates. Canonical v3 contract SHA-256 is `8caa144d9f4c0b9a8149c1822bd79d168d212dea14d72079c3259d55e5e03c8c`.

## Verification and independent judgement

Authoring workflow run `35790144199` checked out authoring head `6f19a361934b7970b92ec2d2f71f18d849070cef` and completed `success`. It ran **26/26** v2+v3 replay-contract regressions, deterministically rebuilt the v3 artifact and byte-compared it with the committed JSON, then re-queried exact Russian Wikisource revision metadata and matched both title/timestamp/SHA-1 identities. Its uploaded artifact contained only the source-free v3 JSON.

Independent review `5284802535` then re-read all **8 changed files** on exact final head `e7de3024fdda2c6afc9e12884112a5d849c56938` against unchanged `master@f8a0732ac3732510406fff7e4fe3b082b31b74ac`, found no merge blocker and found no open review thread. All **21/21** PR-triggered workflows on that exact head settled `success`. Dedicated exact-head run `35790329660` checked out the reviewed SHA, ran the v2+v3 replay-contract regressions, deterministically rebuilt and byte-compared the source-free v3 contract, and freshly re-queried both exact root revisions with metadata-only `ids|timestamp|sha1`, matching the committed identities.

PR #216 was marked Ready and squash-merged with expected-head protection as `71571633819111790243a3a99591eea314be2f6f`, automatically closing Issue #215 as completed.

## Gates / handoff

- `root_identities_bound=true`
- `dependency_closure_complete=false`
- direct-dependency discovery evidence remains absent for both roots
- recursive template/module closure remains unfrozen
- deterministic forced/non-forced outputs remain unverified
- renderer rule promotion remains false; `ё` remains unresolved in the backlog
- literary-body / >=300k admission remains false
- `fantlab_source_edition_match=unknown`
- `m2_parity_admissible=false`
- M2 remains **0/5**

SCRIP-CORPUS-064 is complete. Normal-flow selection may resume from the queue; the next Darwin/Rachinsky evidence-bearing step is direct-dependency discovery and recursive closure, not renderer/body/FantLab promotion.
