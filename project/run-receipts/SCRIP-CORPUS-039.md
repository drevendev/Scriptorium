# Run receipt — SCRIP-CORPUS-039

Status: `AUTHORED_PENDING_INDEPENDENT_REVIEW`
Issue: #165
Pull request: #166 (Draft)
Base master at selection: `df2d302183f36cc14e9ac7b5ad7dff6506739e3c`

## Selected bounded unit

Freeze exact source-free revision identities for all 410 Page-namespace dependencies referenced by the already frozen 1928 *Zemlya i Fabrika* parent route graph for Ilf and Petrov's *The Twelve Chairs*. Preserve the later 1938/1961 editorial family as distinct and leave the literary-body/FantLab gates closed.

## Produced

- Added a deterministic Page topology/capture/replay helper plus synthetic no-network tests.
- Added a hosted exact-head capture/replay workflow.
- Captured exactly 410 Page sequence/revision ID/timestamp/MediaWiki SHA-1 identity rows and committed them as three digest-bound source-free shards plus an index.
- Kept scan-index gaps 150–151 and 314–315 outside the dependency set and explicitly unclassified.
- Reconciled the 1928 source graph, canonical candidate trace and public candidate page.

## Hosted evidence

Initial capture on PR head `a8cef7d15c55722ad3abd62a2f4211d42583059f`:

- workflow run: `35503562530`
- job: `106059457719`
- exact Page identity count: **410**
- capture artifact: `10603441105`
- artifact size: **19,925 bytes**
- artifact ZIP SHA-256: `431558255b168e99f26ac7f5567bda7bb30d69288120b34f918ad3d0e50062c9`
- capture JSON SHA-256: `e5182724d8188fca48807c58720d17f1e40e55b121d1b172fa414e317859420c`

Pinned replay on authored head `abaf6e3f2ee8fa95df6ba36d08775360415bad8d`:

- workflow run: `35503833620`
- job: `106060165964`
- full standard-library suite: **331 tests passed**
- replayed exact identities: **410/410**
- committed index SHA-256: `c1e3280984e640b8fe739a752ff49a3327633f49b52a635bd2d2d1e6a09f538f`
- source-free replay artifact: `10602883416`, **531 bytes**
- replay artifact ZIP SHA-256: `b8d219c901ba6f7261b149bd12e5f8c6e8e6cf193e862d25bb938fd797b17190`

The replay receipt asserts `identity_replay_match=true`, `source_text_included=false`, `literary_body_frozen=false`, `admitted_for_calibration=false`, `fantlab_source_edition_match=unknown`, `diagnostic_ready=false`, and `m2_parity_admissible=false`.

## Closed boundaries

No Page wikitext, OCR, rendered prose, scan/PDF bytes or extracted literary source text are committed. This unit does not freeze or promote the candidate-specific rendering/extraction contract, literary-body composition/count/digests, Scriptorium-proven >=300k admission, PDF byte identity, FantLab analyzer-input/source-edition identity, diagnostic readiness or M2 parity.

A later run must independently review the final exact PR head and settled CI before marking #166 Ready or merging it. Benchmark movement: none. M2 remains **0/5**.
