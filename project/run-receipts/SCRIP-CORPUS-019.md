# Run receipt — SCRIP-CORPUS-019

- Date: 2026-09-17
- Issue: #107
- PR: #108
- Branch: `scrip-corpus-019-road-body-freeze`
- Base at selection: `734155c927b7876cee2f19f94217c5c62eb68247`
- Independently reviewed exact head: `ade0921c385ddb7ff8265c672e88197813123c31`
- Squash merge: `9a73f7cb43f5770e4134c1b3655174b6718756cc`
- Result: `DONE`

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

## Independent review / verification

Later-run review inspected exact head `ade0921c385ddb7ff8265c672e88197813123c31`. The PR was mergeable, 16 commits ahead / 0 behind its base, contained the expected 11 changed files, and had no inline review threads. No blocking defect was found in the generic source-free manifest layer, Road-specific fail-closed extraction contract, committed body manifest, public provenance wording, or M2/FantLab boundary.

Exact-head workflows:

- Road replay run `35192693840`: `success`. It re-ran the standard-library suite, re-fetched revision `5585836`, byte-compared the observed source-free revision manifest, replayed the revision, regenerated the literary-body manifest, byte-compared it with the committed manifest, replayed the source-specific body contract, asserted >=300k characters and source-text exclusion, and uploaded source-free evidence.
- Pages run `35192693818`: `success`.
- Frozen diagnostic run `35192693735`: `success`.
- Pinned pylem provider run `35192693699`: `success`.

The review was recorded on PR #108, the PR was marked Ready, and exact head `ade0921c385ddb7ff8265c672e88197813123c31` was squash-merged as `9a73f7cb43f5770e4134c1b3655174b6718756cc`. Issue #107 closed completed.

## Evidence boundary / benchmark movement

FantLab's recorded value is 438,439 characters, so the frozen alternate body is 4,217 characters larger. This is diagnostic-only evidence and does not authorize tuning toward FantLab. The retained primary Pravda-1965 family still lacks frozen literary-page revisions/extraction/composition, and FantLab still exposes no immutable analyzer-input identity.

`fantlab_source_edition_match=unknown`; overall `diagnostic_ready=false`; `gate_ready=false`; `m2_parity_admissible=false`; M2 remains **0/5**.

## Next action

Select the next dependency-satisfied SCRIP-CORPUS continuation unit from durable state. Prefer strengthening a retained body-unfrozen or trace-only candidate when a deterministic source-free extraction/composition identity can be bounded and verified, otherwise add another legally usable >=300k diversity candidate with explicit provenance. Do not infer FantLab input identity from bibliography, source freezing or count proximity.
