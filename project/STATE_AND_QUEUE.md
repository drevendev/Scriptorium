# STATE_AND_QUEUE — Scriptorium

STATE_REVISION: 50
PHASE: M1 — Deterministic FantLab surface
LAST_COMMITTED_RUN_AT: 2026-09-14T05:00:00Z
LAST_RESULT: SCRIP-PUNCT-002 authored on PR #44. The new inferred punctuation-v2 policy removes the internal double role where ASCII hyphen-minus retained inside a current text-v1 word token was also counted as dash punctuation. Aggregate/schema identities are versioned forward; no FantLab parity claim moved.
LAST_VERIFIED_PROGRESS: Re-oriented from master b612c0de4e2b72af611b9ea74ade3632d84b6c0e. SCRIP-MORPH-003 remains infrastructure not_run: the execution container has no installed pylem and DNS still fails for github.com, pypi.org and files.pythonhosted.org. FantLab article 374 still publishes only punctuation-frequency scope, while public work surfaces label the `-` row as `тире`; no public hyphen/dash classifier was found. SCRIP-PUNCT-002 therefore resolves only Scriptorium's internal consistency boundary: token-internal ASCII hyphens retained by scriptorium-text-v1 are lexical connectors for punctuation-v2 and are not simultaneously counted as dash events. PR #44 exact authored head 3d41f9f858435ff14ca88437fb731c8507d4d65e queued hosted frozen-diagnostic run 34808009137 and Pages run 34808009168; independent exact-head review is still required before merge.

## Current unit

```text
UNIT_ID:        SCRIP-PUNCT-002
ISSUE:          #43
STATUS:         REVIEW
PR:             #44
AUTHORED_HEAD:  3d41f9f858435ff14ca88437fb731c8507d4d65e
NEXT_ACTION:    Do not merge from the authoring run. On the next wake, re-read PR #44,
                inspect its exact current head, review comments/threads and hosted
                checks. Independently verify punctuation-v2 lexical-hyphen behavior,
                schema/profile versioning, historical-v1 artifact preservation and the
                frozen diagnostic boundary. Merge only if that exact head is clean.
```

## Current milestone gate

M0 is closed. M1 remains open. General, dialogue, vocabulary and punctuation families are executable inferred candidates. POS aggregation has a versioned provider-neutral candidate artifact, but native pinned pylem/provider execution identity remains unverified. The benchmark harness has one reproducibly frozen full-work Anna Karenina diagnostic, but its FantLab analyzer-input edition is unknown. SCRIP-PUNCT-002 versions punctuation semantics forward without claiming FantLab's hidden hyphen/dash rule. The M2 reproduction gate remains **0/5 source-matched works**.

## Queue

Evaluate rows in priority order and skip dependencies that are not executable. A `REVIEW` current unit preempts selecting a new row.

| Priority | Unit | Mode | Deliverable | Gate / dependency |
| --- | --- | --- | --- | --- |
| P1 | SCRIP-MORPH-003 | implementation | Bind pinned pylem/provider execution and wire POS artifacts into diagnostic benchmark comparison | SCRIP-MORPH-002; verified provider/runtime provenance; currently blocked because the execution container has no installed pylem and cannot resolve required GitHub/PyPI package hosts |
| P2 | SCRIP-PUNCT-002 | analyzer core / reproduction | Resolve the inspectable lexical-hyphen-versus-dash event overlap under a versioned punctuation policy, using public methodology and independent tests rather than fitting the unmatched Anna Karenina target | Authored as Issue #43 / PR #44; independent exact-head review required before merge |
| P3 | SCRIP-DIALOGUE-002 | analyzer core / reproduction | Investigate the +21.372 percentage-point author-text-inside-dialogue gap, including delimiter recognition and denominator semantics, with bounded tests and diagnostic evidence | SCRIP-REPRO-005 merged; do not tune to one unmatched source as parity proof |

## Evidence already established

### FantLab / benchmark boundary

- FantLab's public methodology exposes deterministic/general, dialogue, vocabulary, POS and punctuation surfaces but acknowledges unpublished corrective coefficients/know-how. Similarity is never parity by itself.
- For punctuation specifically, article 374 says the analyzer measures frequencies of known punctuation marks, while public work pages render a `-` row labelled `тире`; no public rule has been found that distinguishes lexical hyphens from dash punctuation.
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
- Punctuation-v1 diagnostic: dash was +20.89370 per 1000 Scriptorium words and comma -9.54543 per 1000 words. Several other rates were numerically closer, but remain unresolved diagnostic resemblance.
- Vocabulary diagnostic: surface-form unique vocabulary is 33,373 versus FantLab's 12,770 (+20,603). Dictionary-dependent values remain not_run/unresolved because FantLab's dictionary identity is unknown.
- POS remains absent because native pinned pylem/provider execution is still `not_run`.

### Word/dash policy sensitivity — SCRIP-TEXT-004

- Historical committed `scriptorium-text-policy-diagnostic-v1` is source-free sensitivity evidence, not a FantLab compatibility profile. Its variants cannot promote parity.
- Current `scriptorium-text-v1` counts 269,358 words. Only 17 are numeric-only tokens; excluding them leaves 269,341, still +16,066 versus FantLab. Treating U+2010/U+2011 as lexical connectors changes the frozen candidate count by zero because neither glyph occurs.
- Under historical `scriptorium-punctuation-v1`, the frozen candidate had 12,545 dash-family glyphs: 10,933 U+2014 em dashes plus 1,612 ASCII hyphen-minus glyphs; U+2010/U+2011/U+2012/U+2013 do not occur in the candidate.
- Of the 1,612 ASCII hyphens, 1,607 sit directly between letters and 1,611 are internal to current word tokens. That exposed a real inspectable policy overlap: the same glyph was lexical inside a word and simultaneously counted as punctuation.
- Excluding all current token-internal ASCII hyphens would reduce the candidate dash count to 10,934 and the rate to 40.59282 per 1000 current words, still +14.91282 relative to FantLab's displayed 25.68. Thus lexical-hyphen overlap explains only part of the diagnostic gap and cannot establish FantLab's rule.

### Punctuation v2 candidate — SCRIP-PUNCT-002

- PR #44 versions the aggregate artifact to `scriptorium-metrics-v4` / `scriptorium-deterministic-metrics-v4` and punctuation semantics to `scriptorium-punctuation-v2`; the historical v3 schema and punctuation-v1 evidence remain untouched.
- Punctuation-v2 derives lexical ASCII-hyphen positions from the exact current `scriptorium-text-v1` token spans. If ASCII `-` is retained inside a word token, that glyph is not also counted as a dash punctuation event.
- Token-external ASCII hyphen-minus and U+2010..U+2014 remain inferred dash candidates. Greedy compound punctuation and all non-dash rows are unchanged.
- The rule is an internal consistency invariant, not a linguistic assertion that every token-internal hyphen is lexically correct and not a reconstruction of FantLab's unpublished classifier.
- The source-free policy diagnostic is versioned forward to v2 for newly generated evidence and explicitly distinguishes the legacy punctuation-v1 all-glyph baseline from current punctuation-v2. The committed historical v1 artifact is intentionally not rewritten without replay.
- No production word-token semantics changed. No source-edition gate changed. M2 remains 0/5.

### Deterministic analyzer surface

- `scriptorium-text-v1` provides deterministic NFC/newline normalization and word/sentence candidate spans; compatibility remains inferred.
- `scriptorium-dialogue-v1`, `scriptorium-vocabulary-v1`, `scriptorium-metrics-v4` and `scriptorium-deterministic-metrics-v4` provide the current general/dialogue/vocabulary/punctuation surface when PR #44 is reviewed and merged; master remains on v3/v1 until then.
- Dictionary-dependent vocabulary values remain non-parity because FantLab's production dictionary/version is unknown.
- `scriptorium-pos-v1` / `scriptorium-pos-metrics-v1` provides provider-neutral POS aggregation with explicit unresolved categories and text/runtime identity. Native pylem provider provenance is still `not_run`.

### Morphology compatibility

- `pylem==0.0.18` remains the selected AOT-lineage compatibility candidate with pinned source/dictionary provenance.
- Fifteen runtime strings have direct candidate mappings. Runtime `N` collapses noun/cardinal; extra categories and FantLab homonym/prediction behavior remain unresolved.
- No heuristic is accepted merely to force runtime output into FantLab's displayed buckets.
- Native provider execution remains infrastructure-blocked in the current execution container; this is not a pylem failure.

### Public repository representation

- Two derived Anna Karenina excerpt showcases remain public, explicitly short/non-corpus/non-parity, with no source prose committed.
- The repository contains a source-free full-work Anna Karenina diagnostic artifact and a historical source-free word/dash policy-sensitivity artifact linked from the public README. Both state source identity is unknown and M2 inadmissible.
- `docs/METRIC_PROFILE.md` on PR #44 exposes the punctuation-v2 rule and its uncertainty boundary to repository visitors without rewriting historical artifacts.
- `scriptorium-publication-manifest-v1`, `scriptorium-static-site-v1` and the gated Pages build/upload workflow remain fail-closed on unsupported publication semantics.
- Live deployment remains intentionally disabled behind `SCRIPTORIUM_PAGES_DEPLOY_ENABLED=true` and repository Pages administration is a separate owner/admin effect.

## Known risks / blockers

1. **FantLab source identity:** public results do not disclose analyzer-input bytes; M2 remains 0/5 until independent evidence closes source matching.
2. **Hidden algorithm details:** FantLab corrective coefficients and implementation choices are partly unpublished.
3. **Text-boundary/counting inference:** tested numeric-only and Unicode-hyphen token variants explain only 17 and 0 words respectively of the +16,083 diagnostic gap; exact word-boundary semantics remain unproven.
4. **Dash punctuation semantics:** Scriptorium punctuation-v2 removes the internal lexical-hyphen/dash double role, but FantLab's actual hyphen/dash classifier remains unpublished and a large source-unmatched diagnostic gap remains.
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
