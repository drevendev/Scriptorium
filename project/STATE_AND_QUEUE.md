# STATE_AND_QUEUE — Scriptorium

STATE_REVISION: 106
PHASE: M1 — Deterministic FantLab surface
LAST_COMMITTED_RUN_AT: 2026-09-16T20:48:38Z
LAST_RESULT: SCRIP-CORPUS-015 / Issue #99 / PR #100 received an independent later-run exact-head review of `239c9bf358f376a49598f2808f6a32b7c07bb15a` with no blocking defect and was squash-merged as `9e27cedca58a884af283ad56d76056c59725e64b`; Issue #99 closed completed. The merged unit freezes source-free MediaWiki revision-wikitext identity for `tolstoy-hyperboloid-garin-wikisource-ru` while keeping deterministic literary-body extraction/digests, bibliographic print-edition identity and FantLab analyzer-input identity explicitly distinct and unresolved.
LAST_VERIFIED_PROGRESS: Immediately before merge, current `master` was unchanged from the authored base `b58598f7e54d8849369077ad07ad0628ad5e38d9`; PR #100 was 6 commits ahead / 0 behind with exactly six expected provenance/replay files and no inline review threads. Exact-head runs `35143599234` (Hyperboloid source revision) and `35143599189` (Scriptorium Pages) completed successfully. The replay run passed the full standard-library suite, fresh pinned capture, byte-for-byte comparison with the committed manifest and replay; Pages passed the full suite, canonical build and deterministic rebuild. The manifest records page ID `1022517`, revision `5014458`, timestamp `2023-08-30T20:13:01Z`, MediaWiki SHA-1 `605afeabc38e4f5948371afdf976f586edbf1955`, 502280 wikitext characters / 934455 UTF-8 bytes, and SHA-256 `fa0b099bba2d0f0e6ce395a16de76317afcd8bec8b23b52e455f97a9726a4de9` without committing source prose. This does not establish a frozen literary body or FantLab source match; M2 remains 0/5.

## Current unit

```text
UNIT_ID:        SCRIP-CORPUS-015
ISSUE:          #99
STATUS:         DONE
PR:             #100
MERGED_COMMIT:  9e27cedca58a884af283ad56d76056c59725e64b
NEXT_ACTION:    Select the next dependency-satisfied SCRIP-CORPUS continuation unit.
                Prefer another legally usable >=300k diversity candidate or stronger
                independent source-identity evidence for an existing candidate. When a
                revision/container identity is frozen, keep literary-body extraction and
                raw/normalized body digests separate until deterministically reproduced.
                Never infer FantLab input identity from bibliography, title, count
                proximity or public-source freezing.
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
- **Hyperboloid of Engineer Garin** — the Russian Wikisource `az.lib.ru` route at `oldid=5014458` has a source-free frozen **revision-wikitext** identity (page ID `1022517`; SHA-256 `fa0b099bba2d0f0e6ce395a16de76317afcd8bec8b23b52e455f97a9726a4de9`) plus a 1939-derived Moscow-1958 textual-family lead. Deterministic literary-body extraction/body digests, direct print-edition identity and FantLab source match remain unfrozen/unknown.
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
- SCRIP-CORPUS-015 adds a frozen source-free revision-wikitext manifest and dedicated replay workflow for Hyperboloid of Engineer Garin, while explicitly refusing to present revision/container identity as a frozen literary body or FantLab source match.
- Live Pages deployment remains disabled behind `SCRIPTORIUM_PAGES_DEPLOY_ENABLED=true` plus repository Pages administration.

## Known risks / blockers

1. FantLab analyzer-input bytes/edition identity remain undisclosed for retained benchmark works; M2 remains 0/5.
2. FantLab corrective coefficients, parser details, word-boundary semantics, dash classifier and dialogue grammar/denominators remain partly unpublished.
3. FantLab dictionary/version, homonym selection/prediction and service-word aggregation remain unknown.
4. pylem runtime `N` loses noun/cardinal distinction; methodology-only categories are diagnostic until their visible work-page relation is evidenced.
5. Frozen public-source candidates remain unmatched to FantLab input and therefore cannot advance M2.
6. Petersburg lacks a Scriptorium-recorded PDF snapshot digest and deterministic OCR/page-extraction identity.
7. Hyperboloid now has a frozen revision-wikitext identity but no deterministic literary-body extraction/body digests or direct print-edition identity; Shining World, Running on Waves, White Guard and Twelve Chairs remain trace-only/unfrozen at the literary-body level.
8. Road to Nowhere now has a frozen alternate revision-wikitext identity, but the primary 1965 literary family and the alternate route's literary-body extraction/body digests remain unfrozen; FantLab input remains undisclosed.
9. Pages live activation remains a repository-admin effect and is off.
