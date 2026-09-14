# STATE_AND_QUEUE — Scriptorium

STATE_REVISION: 48
PHASE: M1 — Deterministic FantLab surface
LAST_COMMITTED_RUN_AT: 2026-09-14T02:58:00Z
LAST_RESULT: SCRIP-TEXT-004 authored as Issue #41 / PR #42. A source-free policy-sensitivity diagnostic now shows that tested numeric-token and Unicode-hyphen word variants explain essentially none of the +16,083-word gap, while lexical ASCII-hyphen overlap explains only part of the +20.894-dash-per-1000 gap. No compatibility semantics were changed; M2 remains 0/5 source-matched works.
LAST_VERIFIED_PROGRESS: PR #42 authored analysis head 2b31cd9aaa9daddc28649fe1a921904bba0f8aec passed hosted frozen-diagnostic run 34800715320 and Pages run 34800715298. The diagnostic workflow replayed all 239 frozen Anna Karenina revisions, passed the standard-library suite, emitted/uploaded source-free evidence artifact 10331456918, and kept source identity unknown/M2 inadmissible. Artifact ZIP SHA-256 5c4ec7c59a8feca75c087553b952f2af471b05e157476d55ce1e490f1116d285 was independently rechecked. SCRIP-MORPH-003 remains infrastructure not_run because pylem is absent and direct DNS resolution to GitHub/PyPI package hosts still fails in the execution container.

## Current unit

```text
UNIT_ID:        SCRIP-TEXT-004
ISSUE:          #41
STATUS:         REVIEW
PR:             #42
MERGED_COMMIT:  none
NEXT_ACTION:    Independently review the final PR #42 head. Verify that executable code
                remains fail-closed/source-free, inspect the exact hosted checks and
                policy-sensitivity artifact, and confirm no FantLab semantics were
                inferred from numerical closeness. If clean, squash-merge in that later
                run. After merge, re-check SCRIP-MORPH-003 before selecting new work.
```

## Current milestone gate

M0 is closed. M1 remains open. General, dialogue, vocabulary and punctuation families are executable inferred candidates. POS aggregation has a versioned provider-neutral candidate artifact, but native pinned pylem/provider execution identity remains unverified. The benchmark harness has one reproducibly frozen full-work Anna Karenina diagnostic, but its FantLab analyzer-input edition is unknown. SCRIP-TEXT-004 adds policy-sensitivity evidence without changing tokenizer or punctuation compatibility semantics. The M2 reproduction gate remains **0/5 source-matched works**.

## Queue

Evaluate rows in priority order and skip dependencies that are not executable.

| Priority | Unit | Mode | Deliverable | Gate / dependency |
| --- | --- | --- | --- | --- |
| P1 | SCRIP-MORPH-003 | implementation | Bind pinned pylem/provider execution and wire POS artifacts into diagnostic benchmark comparison | SCRIP-MORPH-002; verified provider/runtime provenance; currently blocked because the execution container has no installed pylem and cannot resolve required GitHub/PyPI package hosts |
| P2 | SCRIP-PUNCT-002 | analyzer core / reproduction | Resolve the inspectable lexical-hyphen-versus-dash event overlap under a versioned punctuation policy, using public methodology and independent tests rather than fitting the unmatched Anna Karenina target | SCRIP-TEXT-004 merged; current diagnostic shows 1,607 letter-letter ASCII hyphens are counted as dash events but removing them still leaves +14.928/1000 words; source match remains unknown |
| P3 | SCRIP-DIALOGUE-002 | analyzer core / reproduction | Investigate the +21.372 percentage-point author-text-inside-dialogue gap, including delimiter recognition and denominator semantics, with bounded tests and diagnostic evidence | SCRIP-REPRO-005 merged; do not tune to one unmatched source as parity proof |

## Evidence already established

### FantLab / benchmark boundary

- FantLab's public methodology exposes deterministic/general, dialogue, vocabulary, POS and punctuation surfaces but acknowledges unpublished corrective coefficients/know-how. Similarity is never parity by itself.
- `fantlab-2022-v1` is the frozen compatibility contract. `scriptorium-benchmark-v1` records source/legal identity, hashes, analyzer configuration, expected/actual values and deltas.
- Exact integer `pass`/`fail` requires admissible exact source identity. Decimal/rate comparisons remain unresolved until display precision/rounding behavior is independently established.
- The retained five-work parity seed remains **0/5 source-matched**. A frozen public candidate supports diagnostics only until analyzer-input identity is independently tied to the same bytes.

### Frozen Anna Karenina source identity

- FantLab work 270306 reports its 19 September 2022 analysis as 1,692,647 characters and 253,275 words, but the public surface does not disclose analyzer-input edition or bytes.
- Russian Wikisource identifies the public transcription via FEB as Tolstoy, *Anna Karenina*, Nauka 1970, pp. 5–684 and marks the literary work public domain. The work is an eight-part, 239-chapter composite.
- `corpus/candidates/source-edition-traces/tolstoy-anna-karenina-ru.revisions.json` records all 239 revision IDs, timestamps and MediaWiki SHA-1 identities in source-free packed form. `scriptorium/wikisource_replay.py` re-fetches those exact revisions, verifies each identity and reconstructs the composite in memory.
- Frozen composite identity: 1,705,605 characters including spaces; 3,072,993 UTF-8 bytes; raw and `scriptorium-text-v1` normalized SHA-256 `1dcf2af815f6288099f77a038d873690fb0dc72edf81d2094fd29f3d5a30c205`.
- `fantlab_source_edition_match=unknown`, `diagnostic_comparison_admissible=true` only for reproducible diagnostics, and `m2_parity_admissible=false`.

### First full-work diagnostic

- Exact-head hosted run 34794669740 passed 95/95 tests and replayed all 239 pinned revisions while preserving the frozen composite identity. No novel prose was committed or uploaded.
- General diagnostic: characters +12,958; words +16,083; mean word length +0.03255 characters; mean sentence length -0.17415 characters relative to FantLab.
- Dialogue diagnostic: narration mean sentence length +0.67997 characters, dialogue mean -1.00362 characters, dialogue share -0.14537 percentage points, author text inside dialogue +21.37204 percentage points.
- Punctuation diagnostic: dash is +20.89370 per 1000 Scriptorium words and comma is -9.54543 per 1000 words. Several other rates are numerically closer, but remain unresolved diagnostic resemblance.
- Vocabulary diagnostic: surface-form unique vocabulary is 33,373 versus FantLab's 12,770 (+20,603). Dictionary-dependent values remain not_run/unresolved because FantLab's dictionary identity is unknown.
- POS remains absent because native pinned pylem/provider execution is still `not_run`.

### Word/dash policy sensitivity — SCRIP-TEXT-004

- `scriptorium-text-policy-diagnostic-v1` is a source-free sensitivity surface, not a FantLab compatibility profile. Its variants are probes only and cannot promote parity.
- Hosted run 34800715320 on authored analysis head `2b31cd9aaa9daddc28649fe1a921904bba0f8aec` replayed the same 239 frozen revisions, ran the full standard-library suite successfully and uploaded derived artifact 10331456918. The artifact ZIP SHA-256 is `5c4ec7c59a8feca75c087553b952f2af471b05e157476d55ce1e490f1116d285` and contains no source prose.
- Current `scriptorium-text-v1` counts 269,358 words. Only 17 are numeric-only tokens; excluding them leaves 269,341, still +16,066 versus FantLab. Treating U+2010/U+2011 as lexical connectors changes the frozen candidate count by zero because neither glyph occurs. These tested variants do not explain the word gap and do not justify a tokenizer change.
- Current `scriptorium-punctuation-v1` counts 12,545 dash-family glyphs: 10,933 U+2014 em dashes plus 1,612 ASCII hyphen-minus glyphs; U+2010/U+2011/U+2012/U+2013 do not occur in the candidate.
- Of the 1,612 ASCII hyphens, 1,607 sit directly between letters and 1,611 are internal to current word tokens. That is a real inspectable policy overlap: the same glyph can be lexical inside a word and simultaneously counted as punctuation.
- Excluding all current token-internal ASCII hyphens would reduce the candidate dash count to 10,934 and the rate to 40.59282 per 1000 current words, still +14.91282 relative to FantLab's displayed 25.68. Thus lexical-hyphen overlap explains only part of the diagnostic gap and cannot establish FantLab's rule.
- No production tokenizer or punctuation semantics changed in SCRIP-TEXT-004. The next punctuation unit must resolve the internal consistency question from definitions/tests, not by optimizing against this source-unmatched work.

### Deterministic analyzer surface

- `scriptorium-text-v1` provides deterministic NFC/newline normalization and word/sentence candidate spans; compatibility remains inferred.
- `scriptorium-dialogue-v1`, `scriptorium-punctuation-v1`, `scriptorium-vocabulary-v1`, `scriptorium-metrics-v3` and `scriptorium-deterministic-metrics-v3` provide the currently implemented general/dialogue/vocabulary/punctuation surface.
- Dictionary-dependent vocabulary values remain non-parity because FantLab's production dictionary/version is unknown.
- `scriptorium-pos-v1` / `scriptorium-pos-metrics-v1` provides provider-neutral POS aggregation with explicit unresolved categories and text/runtime identity. Native pylem provider provenance is still `not_run`.

### Morphology compatibility

- `pylem==0.0.18` remains the selected AOT-lineage compatibility candidate with pinned source/dictionary provenance.
- Fifteen runtime strings have direct candidate mappings. Runtime `N` collapses noun/cardinal; extra categories and FantLab homonym/prediction behavior remain unresolved.
- No heuristic is accepted merely to force runtime output into FantLab's displayed buckets.
- Native provider execution remains infrastructure-blocked in the current execution container; this is not a pylem failure.

### Public repository representation

- Two derived Anna Karenina excerpt showcases remain public, explicitly short/non-corpus/non-parity, with no source prose committed.
- The repository contains a source-free full-work Anna Karenina diagnostic artifact and now a source-free word/dash policy-sensitivity artifact linked from the public README. Both state source identity is unknown and M2 inadmissible.
- `scriptorium-publication-manifest-v1`, `scriptorium-static-site-v1` and the gated Pages build/upload workflow remain fail-closed on unsupported publication semantics.
- PR #42 authored analysis head passed Pages run 34800715298; live deployment remains intentionally disabled behind `SCRIPTORIUM_PAGES_DEPLOY_ENABLED=true` and repository Pages administration is a separate owner/admin effect.

## Known risks / blockers

1. **FantLab source identity:** public results do not disclose analyzer-input bytes; M2 remains 0/5 until independent evidence closes source matching.
2. **Hidden algorithm details:** FantLab corrective coefficients and implementation choices are partly unpublished.
3. **Text-boundary/counting inference:** tested numeric-only and Unicode-hyphen token variants explain only 17 and 0 words respectively of the +16,083 diagnostic gap; exact word-boundary semantics remain unproven.
4. **Dash punctuation semantics:** 1,607 letter-letter ASCII hyphens are simultaneously word-internal and counted as dash punctuation under current candidates, but removing them still leaves a large diagnostic gap. FantLab's hyphen/dash rule is not publicly established.
5. **Dialogue author-remark semantics:** author-text-inside-dialogue differs by more than 21 percentage points on the unmatched frozen candidate.
6. **Vocabulary dictionary identity:** FantLab's production dictionary/version is unknown, and surface-form unique vocabulary is far from the public reference.
7. **Morphology provider runtime:** native pylem build/runtime provenance remains unavailable in the current container.
8. **AOT/POS ambiguity:** noun/cardinal runtime collision, extra-category folding and homonym/prediction selection remain unresolved.
9. **Copyright:** work-specific legal evidence remains mandatory and source prose is not committed by default.
10. **Pages activation:** code/workflow is merged but live deployment remains deliberately unactivated.

## Run selection rule

On each wake:

1. resolve `CURRENT_UNIT` review/recovery before new work;
2. inspect the exact PR head, checks and comments relevant to that unit;
3. otherwise choose the first dependency-satisfied queue row;
4. create/search the corresponding issue before implementation;
5. do exactly one bounded unit and update this file plus the project changelog/benchmark or provenance record in the same semantic change.

Do not create parallel units merely because another wake occurred.
