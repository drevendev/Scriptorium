# STATE_AND_QUEUE — Scriptorium

STATE_REVISION: 43
PHASE: M1 — Deterministic FantLab surface
LAST_COMMITTED_RUN_AT: 2026-09-13T22:04:00Z
LAST_RESULT: SCRIP-REPRO-004 authored as Issue #37 / PR #38. The legally usable Russian Wikisource/FEB Anna Karenina candidate is now frozen as a source-free 239-revision composite with deterministic extraction/composition and immutable raw/normalized identity. It is diagnostic-ready but not source-matched to FantLab; M2 remains 0/5.
LAST_VERIFIED_PROGRESS: Hosted research receipt run 34785638797 on authored head 45b073fbdf415120bf27ec850f3410e482a4f125 passed 85/85 tests, canonical site build/rebuild, all 239 chapter extraction contracts, revision-manifest generation and artifact upload. Artifact 10326711163 matched GitHub SHA-256 9155f8d4d39cb4fc1ac0b8c9188626efb84b1183d3d1cc32349d943b986052aa. The frozen composite has 1,705,605 characters including spaces, 3,072,993 UTF-8 bytes, and raw plus scriptorium-text-v1 normalized SHA-256 1dcf2af815f6288099f77a038d873690fb0dc72edf81d2094fd29f3d5a30c205. Temporary network-research workflow steps were removed before review; production Pages workflow content is restored byte-for-byte to master. A committed regression validates the packed source-free revision manifest.

## Current unit

```text
UNIT_ID:        SCRIP-REPRO-004
ISSUE:          #37
STATUS:         REVIEW
PR:             #38
MERGED_COMMIT:  none
NEXT_ACTION:    Independently review PR #38 exact final head. Require the production
                Pages workflow to equal master, full hosted standard-library suite/site
                build to pass on that head, all committed candidate/provenance JSON to
                parse, the 239-revision packed manifest to remain source-prose-free, and
                FantLab source-edition/M2 gates to remain unknown/false. Merge only if
                those checks pass. After merge, re-check SCRIP-MORPH-003 executability;
                if still blocked, SCRIP-REPRO-005 may run diagnostic deterministic metrics
                against the frozen candidate without treating resemblance as parity.
```

## Current milestone gate

M0 is closed. M1 remains open. General, dialogue, vocabulary and punctuation families are executable inferred candidates. POS aggregation has a versioned provider-neutral candidate artifact, but native pylem/provider execution identity remains unverified. The benchmark harness can compare implemented deterministic fields, but the M2 reproduction gate still requires at least five legally usable, source-matched works and currently remains **0/5**.

## Queue

Resolve the current REVIEW unit before selecting new work. Afterwards evaluate rows in priority order and skip dependencies that are not executable.

| Priority | Unit | Mode | Deliverable | Gate / dependency |
| --- | --- | --- | --- | --- |
| P1 | SCRIP-MORPH-003 | implementation | Bind pinned pylem/provider execution and wire POS artifacts into diagnostic benchmark comparison | SCRIP-MORPH-002; verified provider/runtime provenance; currently blocked because the execution container has no installed pylem and cannot resolve required GitHub/PyPI package hosts |
| P2 | SCRIP-REPRO-004 | research / benchmark | Freeze the Anna Karenina public candidate as a 239-revision source-free composite with deterministic extraction/composition and immutable identity | Authored in PR #38; independent exact-head review required |
| P3 | SCRIP-REPRO-005 | benchmark / reproduction | Run implemented deterministic Scriptorium metrics against the frozen Anna Karenina candidate and record field-by-field diagnostic deltas, including investigation of the character-count gap | SCRIP-REPRO-004 merged; diagnostic-only while FantLab analyzer-input identity remains unproven |

## Evidence already established

### FantLab / benchmark boundary

- FantLab's public methodology exposes deterministic/general, dialogue, vocabulary, POS and punctuation surfaces but acknowledges unpublished corrective coefficients/know-how. Similarity is never parity by itself.
- `fantlab-2022-v1` is the frozen compatibility contract. `scriptorium-benchmark-v1` records source/legal identity, hashes, analyzer configuration, expected/actual values and deltas.
- Exact integer `pass`/`fail` requires admissible exact source identity. Decimal/rate comparisons remain `unresolved_precision` until formatting/rounding behavior is independently established.
- The retained five-work parity seed remains 0/5 source-matched. A frozen public candidate may support diagnostics without satisfying M2.

### Anna Karenina source identity

- FantLab work 270306 reports its 19 September 2022 analysis as 1,692,647 characters and 253,275 words, but the public surface does not disclose analyzer-input edition or bytes.
- `corpus/candidates/source-edition-traces/tolstoy-anna-karenina-ru.json` keeps `fantlab_source_edition_match=unknown` and `m2_parity_admissible=false`.
- Russian Wikisource identifies the public transcription via FEB as Tolstoy, *Anna Karenina*, Nauka 1970, pp. 5–684 and marks the literary work public domain. The work is an eight-part, 239-chapter composite.
- `scriptorium/wikisource_freeze.py` defines the deterministic source-research contract. It fetches explicit chapter revisions, accepts only the narrowly observed Wikisource wrapper/template variants, fails closed on unsupported markup, strips navigation/notes/ref wrappers, and composes chapters in fixed part/chapter order with `\n\n` separators.
- `corpus/candidates/source-edition-traces/tolstoy-anna-karenina-ru.revisions.json` records all 239 revision IDs, timestamp offsets and MediaWiki SHA-1 identities in packed source-free form plus the composite identity. Novel prose is not committed.
- Frozen composite identity: 1,705,605 characters including spaces; 3,072,993 UTF-8 bytes; raw SHA-256 and `scriptorium-text-v1` normalized SHA-256 both `1dcf2af815f6288099f77a038d873690fb0dc72edf81d2094fd29f3d5a30c205`.
- The frozen candidate is 12,958 characters longer than FantLab's displayed count. This is a diagnostic fact, not proof of source mismatch or counting behavior; both source bytes and FantLab normalization/counting details remain potentially different.
- `diagnostic_comparison_admissible=true` now means deterministic comparison may run against this reproducible public candidate. It does **not** mean FantLab source identity is known.

### Deterministic analyzer surface

- `scriptorium-text-v1` provides deterministic NFC/newline normalization and word/sentence candidate spans; compatibility remains inferred.
- `scriptorium-dialogue-v1`, `scriptorium-punctuation-v1`, `scriptorium-vocabulary-v1`, `scriptorium-metrics-v3` and `scriptorium-deterministic-metrics-v3` provide the currently implemented general/dialogue/vocabulary/punctuation surface.
- Dictionary-dependent vocabulary values remain non-parity because FantLab's production dictionary identity is unknown.
- `scriptorium-pos-v1` / `scriptorium-pos-metrics-v1` provides provider-neutral POS aggregation with explicit unresolved categories and text/runtime identity. Native pylem provider provenance is still `not_run`.

### Morphology compatibility

- `pylem==0.0.18` remains the selected AOT-lineage compatibility candidate, pinned with its source/dictionary provenance in repository records.
- Pinned pylem exposes 15 runtime strings with direct candidate mappings. Runtime `N` collapses noun/cardinal; several extra categories and FantLab homonym/prediction behavior remain unresolved.
- No heuristic is accepted merely to force the runtime into FantLab's displayed buckets.
- Native provider execution remains infrastructure-blocked in the current execution container; this is not a pylem failure.

### Public repository representation

- Two derived Anna Karenina excerpt showcases remain public, explicitly short/non-corpus/non-parity, with no source prose committed.
- `scriptorium-publication-manifest-v1`, `scriptorium-static-site-v1` and the gated Pages build/upload workflow are merged and fail closed on unsupported publication semantics.
- Publication triggers cover all renderer-supported canonical roots. Build/upload has passed hosted checks on PR/master; deployment remains intentionally disabled behind `SCRIPTORIUM_PAGES_DEPLOY_ENABLED=true` and repository Pages administration is a separate owner/admin effect.
- SCRIP-REPRO-004 does not change public Pages content or activate deployment.

## Known risks / blockers

1. **FantLab source identity:** the uploaded analyzer input behind public results is not disclosed for the retained corpus candidates; M2 stays 0/5 until independent evidence closes this gap.
2. **Hidden algorithm details:** FantLab corrective coefficients and some implementation choices are unpublished.
3. **Text-boundary/counting inference:** exact normalization, tokenization, sentence boundaries and displayed character-count semantics are not proven equivalent.
4. **Vocabulary dictionary identity:** FantLab's production dictionary/version is unknown.
5. **Morphology provider runtime:** native pylem build/runtime provenance remains unavailable in the current container.
6. **AOT/POS ambiguity:** noun/cardinal runtime collision, extra-category folding and homonym/prediction selection remain unresolved.
7. **Copyright:** web availability is not permission; work-specific legal evidence remains mandatory and source prose is not committed by default.
8. **Hosted CI scope:** the Pages workflow is publication/analyzer scoped, not a universal repository CI replacement.
9. **Pages activation:** code/workflow is merged but live deployment remains deliberately unactivated.

## Run selection rule

On each wake:

1. resolve `CURRENT_UNIT` review/recovery before new work;
2. inspect the exact PR head, checks and comments relevant to that unit;
3. otherwise choose the first dependency-satisfied queue row;
4. create/search the corresponding issue before implementation;
5. do exactly one bounded unit and update this file plus the project changelog/benchmark or provenance record in the same semantic change.

Do not create parallel units merely because another wake occurred.
