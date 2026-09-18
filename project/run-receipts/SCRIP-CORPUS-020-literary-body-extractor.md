# Run receipt — SCRIP-CORPUS-020 literary-body extractor

Date: 2026-09-18
Issue: #109
Draft PR: #126
Baseline master: `99b4016f8e53c06bf694bc1e6c282560c01b056e`
Authoring evidence head: `86abd1483ac3f1d2ff1c5dac89715c6ef6b3a798`

## Bounded unit

Implement and live-verify a candidate-specific, fail-closed literary-body extraction/composition path for the four pinned Russian Wikisource parts of *The Life of Klim Samgin*. Do not freeze/merge the generated body identity in the same authoring run; leave the substantial change as Draft for independent later-run judgement.

## Production

- Replays parent oldids `5733765`, `5198033`, `5138882`, `5724453` plus Part 2 dependency oldid `2366546` against their committed source-free revision manifests.
- Revalidates the merged structural/body-surface, direct-parent `poemx1`, target-only `#lst`, and Part 2 resolution contracts before extraction.
- Replaces exactly seven direct-parent and six dependency `poemx1` calls with the already-frozen exact plain parameter-2 literary values. No generic MediaWiki template parser is introduced.
- Applies bounded partial-transclusion semantics to the dependency after those exact substitutions. Live replay observes `noinclude_pairs=1`, `includeonly_pairs=1`, and zero `onlyinclude` controls.
- Handles only the already-observed Klim scaffolding/markup and fails closed on unmodelled active markup. Literal authorial angle brackets and `nowiki` literals are preserved as text rather than misclassified as tags.
- Defines deterministic composition as Parts `1 -> 2 -> 3 -> 4` joined by `\n\n`.
- Added a dedicated exact-head workflow that runs the complete standard-library suite, re-fetches the pinned source graph, derives a source-free manifest in the runner, and uploads only that manifest.

## Verification

Two live-replay failures were used as correctness discoveries rather than bypassed: the generic single-page extractor falsely treated literal leading `|`/`!` as table syntax for this candidate, and the first Part 2 pass exposed still-live `noinclude`/`includeonly` controls. The candidate renderer was narrowed to actual table delimiters and the existing partial-transclusion processor was inserted at the dependency boundary.

Dedicated run `35340711309`, job `105585727013`, checked out exact head `86abd1483ac3f1d2ff1c5dac89715c6ef6b3a798`, ran **254 tests successfully**, re-fetched all five pinned revisions, completed the four-part live extraction, and uploaded source-free artifact `10544478043`. The observed output was:

- Part 1: 964,215 characters / 1,744,650 UTF-8 bytes; SHA-256 `1a41cef4b2383a149077da372d9a44ab48c3b2616064da6c1ab5f01a6062f4c8`.
- Part 2: 1,164,870 characters / 2,111,745 UTF-8 bytes; SHA-256 `75896b6a0a87bc10087ececbeb919077de58c628f646aab8994cf653edc15794`.
- Part 3: 680,940 characters / 1,234,441 UTF-8 bytes; SHA-256 `7dc6030381371cdcff5a27a872ab1fd6c49840655e3ce11a45d647ea0bf208ab`.
- Part 4: 1,000,587 characters / 1,868,088 UTF-8 bytes; SHA-256 `237b2119e04bdf8c02dded3d138fda457d8f423012d2abe9d752a07c038c8948`.
- Composite: 3,810,618 characters / 6,958,930 UTF-8 bytes; raw and `scriptorium-text-v1` SHA-256 `4f8b61e05cf7d96485d9edc0854d99d994da6ba146fabc3f6a3d509110ce4288`.

The source-free identity manifest is intentionally **not committed yet**. Independent later-run review must inspect #126 and the successful live evidence before capturing those values as canonical.

## Gate boundary / next trigger

`evidence_class` remains `candidate_specific_inferred_reconstruction`. Historical Russian Wikisource MediaWiki-core/Poem deployment equivalence is not proven, FantLab analyzer-input identity is unknown, and the observed digest does not advance parity. **M2 remains 0/5.**

Next trigger: independently review Draft PR #126, its exact-head checks and generated source-free artifact; if clean, capture the canonical source-free literary-body manifest (or request changes) before any merge or FantLab field-by-field diagnostic.
