# Run receipt — SCRIP-CORPUS-034

Date: 2026-09-19
Issue: #155 (closed completed)
Pull request: #156 (`scrip-corpus-034-darwin-page-revisions`, squash-merged)
Mode: normal-flow P2 corpus/provenance strengthening, followed by independent recovery/review

## Selected bounded unit

Freeze the exact source-free revision identities of all 418 Russian Wikisource Page-namespace dependencies already selected by the merged Darwin/Rachinsky 1864 topology, and add deterministic replay evidence without committing source prose or promoting literary-body, corpus-admission or FantLab claims.

## Production and recovery

The first implementation attempted to query 40 long Cyrillic Page titles per MediaWiki GET. Hosted CI failed with HTTP 414 (`URI Too Long`), so the same bounded unit was recovered rather than abandoned or broadened. Capture batching was reduced to 8 titles, keeping requests below the observed server URI limit.

The repaired hosted Darwin workflow run **35471807464**, job **105973987426**, checked out exact head **`db4d5657af3e13548324eb1a101bc6c13a7aa382`**, ran **291 tests — OK**, and captured **418** source-free identities using `rvprop=ids|timestamp|sha1`. The capture contains exactly the frozen included sequence set, excludes source-declared no-text sequences 114 and 411, and contains no source-text field.

The uploaded capture artifact is **10592834383**. Its ZIP SHA-256 is **`1fe9319448ea932a57c48378381e111cbcd6c7e8ca902d162aea1b93f675a014`**; the extracted verbose capture JSON SHA-256 is **`8979500217049380826c2d8c304dd94dc214087e3c356c16f5779e559115b375`**.

## Durable result

- Added `scriptorium/darwin_page_freeze.py` for exact topology-bound Page identity capture/replay with source-free row validation.
- Added `scriptorium/darwin_page_shards.py` to validate four digest-pinned compact identity shards and replay the exact revision IDs against MediaWiki.
- Added focused tests for topology cardinality, no-text exclusions, source-payload rejection, gate closure, committed shard digests/inventory and replay identity matching.
- Added `.github/workflows/darwin-page-revisions.yml` for exact-head hosted capture/replay.
- Committed **418 exact Page revision identities** as four source-free shards plus an authoritative index. Each tuple contains only Page sequence, revision ID, timestamp and MediaWiki SHA-1.
- Updated the public Darwin/Rachinsky candidate page and structured source-edition trace to expose the stronger identity freeze while explicitly preserving the remaining gates.
- Added this receipt and semantic changelog fragment and advanced canonical state for stateless recovery.

## Independent exact-head review

A later stateless wake independently resolved PR #156 at exact head **`dd1cd6083e44cd4bfeac8df932a50721a3e41cad`** against unchanged base **`3aa62c1dac2a9f7b4b4449d753226267eed61160`**. The comparison was **17 commits ahead / 0 behind**, the PR was mergeable, and there were no inline review threads.

All 15 changed paths were inspected by type: hosted workflow, capture/replay implementation, sharded-manifest loader, focused tests, four identity shards, authoritative index, public candidate/provenance records, state, changelog and this receipt. No literary source prose, OCR, rendered Page payload, scan bytes or downstream-gate promotion was found.

All **15/15** pull-request-triggered workflows on the exact reviewed head completed **successfully**. `Darwin Rachinsky Page revision identities` run **35472282171**, job **105975295568**, checked out that exact SHA, used Python 3.13.15, ran **293 tests — OK**, replayed all 418 pinned revisions against MediaWiki and emitted `identity_replay_match=true`, `source_text_included=false`, `literary_body_frozen=false`, `admitted_for_calibration=false`, `fantlab_source_edition_match=unknown`, and `m2_parity_admissible=false`.

Exact-head replay artifact **10593275396** is **538 bytes** with SHA-256 **`82008b4c69a7c4d65f874d5595a6494405ba527c9f0fe5d2091f311c91c9ef9a`**. `Scriptorium Pages` and `Scriptorium pinned pylem provider` were also green on the reviewed SHA.

No blocking defect was found. The PR was marked Ready and squash-merged as **`a8429d82a33e3a0e2606c72a398343b00d604da8`**; Issue #155 closed completed.

## Freeze boundary

Frozen by this unit:

- the exact 418 included Page-sequence set derived from the previously merged transclusion topology;
- exact revision ID, revision timestamp and MediaWiki SHA-1 for every included Page dependency;
- source-free capture artifact provenance and four committed shard SHA-256 digests;
- deterministic fail-closed validation/replay contract for those identities.

Still unfrozen:

- Page wikitext/OCR/rendered literary prose as a committed payload;
- candidate-specific literary-body extraction/composition semantics and apparatus decisions;
- literary-body character count, raw/normalized digests and >=300k admission;
- independently retrieved DjVu bytes and Scriptorium-computed binary SHA-256;
- FantLab analyzer-input/source-edition identity for the Rachinsky translation.

## Gate status

- `admitted_for_calibration=false`
- `fantlab_source_edition_match=unknown`
- `diagnostic_ready=false`
- `gate_ready=false`
- `m2_parity_admissible=false`
- M2 remains **0/5 source-matched works**

## Handoff

SCRIP-CORPUS-034 is complete and canonical in `master`. Resume normal-flow P2 corpus/provenance work. For Darwin/Rachinsky, the next evidence-bearing unit is a candidate-specific fail-closed literary-body extraction/composition contract over the frozen 418 Page identities, followed by body count/digests and >=300k admission only if independently demonstrated. Independent scan-byte SHA-256 and FantLab source/analyzer-input matching remain separate gates.
