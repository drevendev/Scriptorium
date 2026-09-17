# STATE_AND_QUEUE — Scriptorium

STATE_REVISION: 112
PHASE: M1 — Deterministic FantLab surface
LAST_COMMITTED_RUN_AT: 2026-09-17T03:52:54Z
LAST_RESULT: SCRIP-CORPUS-017 / Issue #103 / PR #104 received an independent later-run exact-head review of repaired head `69744107743a6c0d7b35199dc8123c92dca2e13c` with no blocking defect, was marked Ready, and was squash-merged as `4240a9df5aae55c84a202327bbae6d3bef97e2df`; Issue #103 closed completed. The merged unit adds Maxim Gorky's *The Life of Klim Samgin* as a source-free provenance-qualified twentieth-century corpus lead and repairs public corpus navigation, while deliberately deferring parity-catalog admission until immutable revision/body identity is replay-frozen.
LAST_VERIFIED_PROGRESS: Immediately before merge, PR #104 was mergeable, 9 commits / 6 changed files, with no inline review threads. Repaired exact-head workflows `35175996990` (Scriptorium Pages) and `35175996991` (pinned pylem provider) both completed successfully. The six-file diff keeps README, candidate page, provenance trace, changelog fragment, state and receipt aligned on `trace_only`, `fantlab_source_edition_match=unknown`, diagnostics/gate disabled, no main parity-catalog admission and M2 0/5. Fresh FantLab verification still reports the retained 19 September 2022 analysis at 3,789,857 characters / 531,192 words.

## Current unit

```text
UNIT_ID:        SCRIP-CORPUS-017
ISSUE:          #103
STATUS:         DONE
PR:             #104
MERGED_COMMIT:  4240a9df5aae55c84a202327bbae6d3bef97e2df
NEXT_ACTION:    Select the next dependency-satisfied SCRIP-CORPUS continuation unit.
                Prefer strengthening a retained trace-only candidate into a replay-frozen
                immutable source/body identity when that can be bounded and verified, or
                add another legally usable >=300k diversity candidate when stronger
                evidence is available. Never infer FantLab input identity from title,
                bibliography, count proximity or public-source freezing.
```

## Current milestone gate

M0 is closed. M1 remains open. General, dialogue, vocabulary and punctuation metric families are executable inferred candidates. POS has two explicitly separated surfaces: the 17-bucket work-page-compatible `scriptorium-pos-v1` production candidate and a diagnostic-only broader methodology surface with five additional AOT-backed categories while runtime `N` noun/cardinal ambiguity remains unresolved.

No retained work has an independently established FantLab analyzer-input identity, so M2 remains open at **0/5 source-matched works**. Public-source freezing, bibliographic compatibility and diagnostic resemblance do not advance M2.

## Queue

Evaluate rows in priority order. Recovery/review-ready work and failing required checks preempt normal selection.

| Priority | Unit | Mode | Deliverable | Gate / dependency |
| --- | --- | --- | --- | --- |
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
- **The Life of Klim Samgin** — provenance-qualified lead: FantLab reports 3,789,857 characters / 531,192 words; Russian Wikisource marks the original Russian work public domain and exposes a four-part Library-Moshkov family with permanent part locators and GIKhL 1952/1953 source declarations. Status remains `trace_only`; immutable revision/body manifests, composite digests and FantLab source identity are not established, so main parity-catalog admission is deferred.

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
- SCRIP-CORPUS-017 adds a standalone public Klim Samgin candidate page plus a machine-readable provenance trace, and the repaired/merged navigation links both from `corpus/candidates/README.md`. It intentionally does not change the main parity catalog until an immutable four-part literary identity is replay-frozen.
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
9. Klim Samgin has four permanent part revision locators and strong public-domain/bibliographic provenance, but no replay-frozen revision/body manifest, extraction/composition profile or composite digest; it remains a lead rather than a catalog-admitted diagnostic candidate.
10. Pages live activation remains a repository-admin effect and is off.
