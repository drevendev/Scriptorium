# STATE_AND_QUEUE — Scriptorium

STATE_REVISION: 108
PHASE: M1 — Deterministic FantLab surface
LAST_COMMITTED_RUN_AT: 2026-09-16T22:47:59Z
LAST_RESULT: SCRIP-CORPUS-016 / Issue #101 / PR #102 was independently reviewed at exact head `bf41149bdd9996249db01ec9da9889376a80d057`. The source-specific Hyperboloid extraction/replay implementation and all four current-head workflows were healthy, but review found a blocking machine-readable provenance inconsistency: `corpus/candidates/fantlab-parity-v1.json` still described the candidate as unfrozen. This recovery unit repairs that catalog row to reference the committed revision/body manifests, 499066-character frozen body and SHA-256 `a01c5eadef53b2437eff3abe6052bb7f7bf6f95737641558343363628da7f513`, removes the false unfrozen blocker, and preserves the unresolved FantLab/print-edition boundary. PR #102 remains unmerged and requires fresh exact-head checks plus a later independent review of the repaired head.
LAST_VERIFIED_PROGRESS: The independent review of `bf41149bdd9996249db01ec9da9889376a80d057` confirmed the fail-closed/source-free extraction contract and green runs `35156488833` (Hyperboloid replay), `35156488806` (Pages), `35156488898` (frozen diagnostic) and `35156488923` (pinned provider), but correctly blocked merge because the central catalog contradicted the newly frozen revision/body manifests. The repair synchronizes `source_revision_manifest`, `source_body_manifest`, `source_identity_status=public_candidate_frozen`, 499066 characters / 930560 bytes and the frozen body digest while retaining `fantlab_source_edition_match=unknown`, `diagnostic_ready=false`, `gate_ready=false`. Fresh checks on the repaired head are required before merge; no success is claimed for that repaired head in this state commit. M2 remains 0/5.

## Current unit

```text
UNIT_ID:        SCRIP-CORPUS-016
ISSUE:          #101
STATUS:         REVIEW_PENDING / REPAIR_AUTHORED
PR:             #102
AUTHORED_BASE:   d76c5403d62ec85c022efe4def93883eef550da3
NEXT_ACTION:    Require fresh exact-head checks after the catalog-sync repair, including
                Hyperboloid source/body replay and Pages. Then perform a later independent
                review of the repaired exact head before any merge. Preserve the frozen
                public-source identity, but keep direct print-edition identity and
                `fantlab_source_edition_match` unknown; M2 stays 0/5.
```

## Current milestone gate

M0 is closed. M1 remains open. General, dialogue, vocabulary and punctuation metric families are executable inferred candidates. POS has two explicitly separated surfaces: the 17-bucket work-page-compatible `scriptorium-pos-v1` production candidate and a diagnostic-only broader methodology surface with five additional AOT-backed categories while runtime `N` noun/cardinal ambiguity remains unresolved.

No retained work has an independently established FantLab analyzer-input identity, so M2 remains open at **0/5 source-matched works**. Public-source freezing, bibliographic compatibility and diagnostic resemblance do not advance M2.

## Queue

Evaluate rows in priority order. Recovery/review-ready work and failing required checks preempt normal selection.

| Priority | Unit | Mode | Deliverable | Gate / dependency |
| --- | --- | --- | --- | --- |
| P0 | SCRIP-CORPUS-016 repaired-head review | recovery / review | Verify the catalog-sync repair on the exact PR #102 head; merge only after current checks are green and a later independent review finds no blocker | Repaired head must preserve source-free manifests and keep FantLab source identity unknown |
| P2 | SCRIP-CORPUS continuation | corpus / provenance | Add or strengthen legally usable >=300k candidates, prioritizing diversity beyond 19th-century Russian classics when licensing/source identity is strong enough | Preserve translation/edition identity and explicit legal provenance |

## Retained corpus / provenance status

Detailed evidence lives in `corpus/candidates/`, `benchmarks/`, `project/run-receipts/`, `project/CHANGELOG.md`, and `project/CHANGELOG.d/`; this state file keeps only the orientation-critical summary.

- **Anna Karenina** — frozen public-source candidate: 239 pinned chapter revisions; composite 1,705,605 characters; SHA-256 `1dcf2af815f6288099f77a038d873690fb0dc72edf81d2094fd29f3d5a30c205`; FantLab source match unknown.
- **Resurrection** — frozen public-source candidate: 129 pinned chapter revisions; composite 890,835 characters; SHA-256 `2725a60a810d8aae4beff9dbc73ff85cf6da066b1c5272aaebf21addbe4ccaa0`; FantLab source match unknown.
- **Brothers Karamazov** — frozen public-source candidate: 98 admitted revisions; composite 1,810,351 characters; SHA-256 `26b9991c95b30d262c24ae38fb2332333a58df588a62a4310f9e5c4b507dbce6`; FantLab source match unknown.
- **Silver Dove** — frozen single-revision public-source candidate at `oldid=5588003`; composite 563,125 characters; SHA-256 `496dad8aadaca13f3ce6ef8560b53bcd32c75b5b03f28f13f7735303bb4f7183`; FantLab source match unknown.
- **Petersburg** — first-1916-edition facsimile lead; Commons description revision is pinned but PDF bytes/OCR identity are not; no binary/source match claim.
- **Hyperboloid of Engineer Garin** — frozen single-revision public-source candidate at Russian Wikisource `oldid=5014458`: page ID `1022517`, wikitext SHA-256 `fa0b099bba2d0f0e6ce395a16de76317afcd8bec8b23b52e455f97a9726a4de9`; versioned `scriptorium-hyperboloid-wikisource-body-v1` extraction reproduces 499066 characters / 930560 bytes with raw and normalized SHA-256 `a01c5eadef53b2437eff3abe6052bb7f7bf6f95737641558343363628da7f513`. Direct print-edition identity remains unresolved and FantLab source match is unknown.
- **Shining World** — 1965-source Wikisource family with 34 chapter subpages; chapter identities/composite remain unfrozen.
- **Road to Nowhere** — primary Pravda-1965 source family remains unfrozen. The distinct `az.lib.ru` single-page route at `oldid=5585836` now has a source-free frozen **revision-wikitext** identity (page ID `1003775`; SHA-256 `f47b9b05d06dc2f5c6e2642d0822e6db68128386e4f1374b9188206a69fef11b`), but deterministic literary-body extraction/body digests are not frozen and neither route is identified as FantLab input.
- **Running on Waves** — Detskaya literatura 1965 source-cited family with 35 chapters plus epilogue; literary subpage identities/composite remain unfrozen.
- **The White Guard** — Wikisource explicitly mixes two bibliographic source families across chapters 1–11 and 12–20; all 20 chapter identities/composite remain unfrozen.
- **The Twelve Chairs** — keep 40-chapter later 1938/1961 editorial family distinct from 41-chapter 1928 first standalone edition; neither literary body is frozen, and coauthorship prevents individual-author attribution without an explicit VOICE model.

## Deterministic / morphology findings

- Frozen Anna diagnostics still show large character/word differences from FantLab; numeric-token and lexical-hyphen probes do not explain the word gap.
- `scriptorium-punctuation-v2` removes internal ASCII-hyphen double counting, but dash-rate parity remains unresolved.
- Dialogue author-remark / denominator semantics remain unresolved.
- FantLab dictionary/version, homonym selection, word-boundary semantics and service-word aggregation remain unknown.
- `pylem==0.0.18` is pinned by exact sdist SHA-256 `66c0d13414006a803f200979540fcee9653738701c14496a418db67542b26515` plus source/dictionary provenance.
- Runtime `N` loses noun/cardinal distinction. Five additional methodology-only AOT categories remain diagnostic and are not silently folded into the work-page-compatible production view.

## Public repository representation

- Static publication remains source-free and deterministic; publication tests reject forbidden source-prose keys.
- Public corpus navigation exposes the retained frozen and trace-only candidates with provenance boundaries rather than parity claims.
- SCRIP-CORPUS-016 upgrades the public Hyperboloid entry from revision-container-only identity to a frozen source-free literary-body identity with exact counts/digests and an explicit fail-closed extraction profile, while preserving the unresolved print-edition and FantLab-input boundary.
- The repaired machine-readable candidate catalog now agrees with the Hyperboloid trace/body manifests and no longer advertises the candidate as `traced_not_frozen`.
- Live Pages deployment remains disabled behind `SCRIPTORIUM_PAGES_DEPLOY_ENABLED=true` plus repository Pages administration.

## Known risks / blockers

1. FantLab analyzer-input bytes/edition identity remain undisclosed for retained benchmark works; M2 remains 0/5.
2. FantLab corrective coefficients, parser details, word-boundary semantics, dash classifier and dialogue grammar/denominators remain partly unpublished.
3. FantLab dictionary/version, homonym selection/prediction and service-word aggregation remain unknown.
4. pylem runtime `N` loses noun/cardinal distinction; methodology-only categories are diagnostic until their visible work-page relation is evidenced.
5. Frozen public-source candidates remain unmatched to FantLab input and therefore cannot advance M2.
6. Petersburg lacks a Scriptorium-recorded PDF snapshot digest and deterministic OCR/page-extraction identity.
7. Hyperboloid now has a frozen revision and deterministic frozen literary-body identity, but no direct bibliographic print-edition identity and no FantLab analyzer-input match; Shining World, Running on Waves, White Guard and Twelve Chairs remain trace-only/unfrozen at the literary-body level.
8. Road to Nowhere now has a frozen alternate revision-wikitext identity, but the primary 1965 literary family and the alternate route's literary-body extraction/body digests remain unfrozen; FantLab input remains undisclosed.
9. Pages live activation remains a repository-admin effect and is off.
