# Run receipt — SCRIP-CORPUS-019

- Date: 2026-09-17
- Issue: #107
- PR: #108
- Branch: `scrip-corpus-019-road-body-freeze`
- Base at selection: `734155c927b7876cee2f19f94217c5c62eb68247`
- Exact verified substantive head: `67d3bf542a0de33b72b41f7a1a549cb2899e3292`
- Result: `REVIEW_PENDING`

## Selected bounded unit

Strengthen the retained Alexander Grin *Road to Nowhere* candidate by freezing the literary-body identity of the already revision-frozen alternate Russian Wikisource `az.lib.ru` route (`oldid=5585836`) without collapsing it into the source-cited Pravda-1965 primary family or FantLab's undisclosed analyzer input.

## Produced

1. Added reusable `scriptorium.single_page_body` source-free body-manifest/replay machinery that verifies the exact frozen revision before invoking an extractor.
2. Added `scriptorium.road_nowhere_freeze` with a candidate-specific fail-closed source-shape contract derived from the pinned revision rather than from current mutable page rendering.
3. Added unit tests for source-free manifests, exact revision drift, replay, and unsupported source-shape drift.
4. Extended the dedicated Road workflow to re-fetch/compare/replay the exact revision and committed literary-body manifest.
5. Committed `grin-road-nowhere-ru.alternate-body.json` with no source prose.
6. Synchronized `grin-road-nowhere-ru.json` and public corpus navigation to the stronger alternate-route evidence while keeping the primary family trace-only.

## Frozen alternate identity

- page ID: `1003775`
- revision: `5585836`
- timestamp: `2025-07-30T20:33:01Z`
- MediaWiki SHA-1: `135933c3b9155bddb0356d0eb9644d11f55ba870`
- revision-wikitext SHA-256: `f47b9b05d06dc2f5c6e2642d0822e6db68128386e4f1374b9188206a69fef11b`
- extraction profile: `scriptorium-road-nowhere-alt-wikisource-body-v1`
- literary-body characters including spaces: `442656`
- literary-body UTF-8 bytes: `825899`
- raw SHA-256: `e33a28b8dcdb3ac339147c6587b27c182dd910784122b367db41bc93dfc2dbee`
- normalization profile: `scriptorium-text-v1`
- normalized characters: `442656`
- normalized SHA-256: `e33a28b8dcdb3ac339147c6587b27c182dd910784122b367db41bc93dfc2dbee`
- source text committed: `false`

## Verification

Exact substantive head `67d3bf542a0de33b72b41f7a1a549cb2899e3292`:

- Road replay run `35192521006`: `success`. It re-fetched revision `5585836`, byte-compared the observed source-free revision manifest, replayed the revision, regenerated the literary-body manifest, byte-compared it with the committed manifest, replayed the source-specific body contract, asserted >=300k characters and source-text exclusion, and uploaded source-free evidence.
- Pages run `35192520928`: `success`.
- Frozen diagnostic run `35192520936`: `success`.
- The dedicated Road job ran the complete standard-library suite before live recapture; the code-bearing workflow path reached 182 passing tests.

The initial generic one-page renderer correctly failed closed on this direct-page Wikisource source shape. A source-free probe of the exact pinned revision established the bounded contract (one leading `Отексте` scaffold; 27 level-three headings; five trailing category links; no post-scaffold templates/HTML/bold-italic markup), after which the candidate-specific extractor was implemented and verified. Intermediate failing checks were repaired before the final exact-head green evidence above.

## Evidence boundary / benchmark movement

FantLab's recorded value is 438,439 characters, so the frozen alternate body is 4,217 characters larger. This is diagnostic-only evidence and does not authorize tuning toward FantLab. The retained primary Pravda-1965 family still lacks frozen literary-page revisions/extraction/composition, and FantLab still exposes no immutable analyzer-input identity.

`fantlab_source_edition_match=unknown`; overall `diagnostic_ready=false`; `gate_ready=false`; `m2_parity_admissible=false`; M2 remains **0/5**.

## Next action

Independent later-run review of PR #108 at its then-current exact head. Confirm the committed body manifest replays byte-for-byte, review the source-specific extraction boundary and public provenance wording, inspect changed-file scope/threads, and merge only if exact-head required checks remain green. Do not select another normal-flow unit first.
