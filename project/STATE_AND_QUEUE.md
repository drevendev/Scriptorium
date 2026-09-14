# STATE_AND_QUEUE — Scriptorium

STATE_REVISION: 46
PHASE: M1 — Deterministic FantLab surface
LAST_COMMITTED_RUN_AT: 2026-09-14T00:57:00Z
LAST_RESULT: SCRIP-REPRO-005 was authored as Issue #39 / PR #40. Exact replay of the 239 frozen Anna Karenina Wikisource revisions succeeded on hosted analysis head 9ba8f36440b15fc41374209437048ae2e486d579, the current deterministic metric families were compared against FantLab work 270306, and the source-free diagnostic deltas were committed. FantLab analyzer-input identity remains unknown and M2 remains 0/5 source-matched works.
LAST_VERIFIED_PROGRESS: Hosted frozen-diagnostic run 34794221625 on Python 3.13.15 passed 95/95 standard-library tests, replayed all 239 recorded revisions with title/timestamp/MediaWiki-SHA-1 and composite-identity validation, and emitted the derived diagnostic evidence. The same authored head passed Pages run 34794221544 including canonical build, byte-identical rebuild and artifact upload; deployment was skipped. Diagnostic highlights are +12,958 characters, +16,083 words, +21.372 percentage points author-text-inside-dialogue and +20.894 dashes per 1000 Scriptorium words relative to FantLab; all remain diagnostic-only because source identity is unproven.

## Current unit

```text
UNIT_ID:        SCRIP-REPRO-005
ISSUE:          #39
STATUS:         REVIEW
PR:             #40
ANALYSIS_HEAD:  9ba8f36440b15fc41374209437048ae2e486d579
NEXT_ACTION:    Independently review the final PR #40 head. Verify that the FantLab
                reference, exact-revision replay, source-free diagnostic artifact and
                workflow preserve the unknown-source/M2-fail-closed boundary; inspect
                hosted checks on the exact final head and confirm no novel prose is
                committed or uploaded. Merge only if that later review is clean. After
                the current unit resolves, re-check SCRIP-MORPH-003 executability before
                selecting the next queue row.
```

## Current milestone gate

M0 is closed. M1 remains open. General, dialogue, vocabulary and punctuation families are executable inferred candidates. POS aggregation has a versioned provider-neutral candidate artifact, but native pylem/provider execution identity remains unverified. The benchmark harness now has its first full-work diagnostic against a reproducibly frozen public-domain candidate. That diagnostic exposes concrete compatibility deltas but does not satisfy M2 because FantLab's analyzer-input edition remains unknown. The M2 reproduction gate still requires at least five legally usable, source-matched works and remains **0/5**.

## Queue

Evaluate rows in priority order and skip dependencies that are not executable. Current REVIEW work preempts this table.

| Priority | Unit | Mode | Deliverable | Gate / dependency |
| --- | --- | --- | --- | --- |
| P1 | SCRIP-MORPH-003 | implementation | Bind pinned pylem/provider execution and wire POS artifacts into diagnostic benchmark comparison | SCRIP-MORPH-002; verified provider/runtime provenance; currently blocked because the execution container has no installed pylem and cannot resolve required GitHub/PyPI package hosts |
| P2 | SCRIP-TEXT-004 | analyzer core / reproduction | Investigate the +16,083-word and +20.894-dashes-per-1000 diagnostic gaps on the frozen Anna Karenina candidate; separate source-edition uncertainty from inspectable token/dash policy effects and change candidate semantics only when evidence supports it | SCRIP-REPRO-005 merged; diagnostic-only while FantLab analyzer-input identity remains unproven |
| P3 | SCRIP-DIALOGUE-002 | analyzer core / reproduction | Investigate the +21.372 percentage-point author-text-inside-dialogue gap, including delimiter recognition and denominator semantics, with bounded tests and diagnostic evidence | SCRIP-REPRO-005 merged; do not tune to one unmatched source as parity proof |

## Evidence already established

### FantLab / benchmark boundary

- FantLab's public methodology exposes deterministic/general, dialogue, vocabulary, POS and punctuation surfaces but acknowledges unpublished corrective coefficients/know-how. Similarity is never parity by itself.
- `fantlab-2022-v1` is the frozen compatibility contract. `scriptorium-benchmark-v1` records source/legal identity, hashes, analyzer configuration, expected/actual values and deltas.
- Exact integer `pass`/`fail` requires admissible exact source identity. Decimal/rate comparisons remain `unresolved_precision` until formatting/rounding behavior is independently established.
- The retained five-work parity seed remains 0/5 source-matched. A frozen public candidate may support diagnostics without satisfying M2.
- `benchmarks/fantlab/work270306.json` captures the public 19 September 2022 Anna Karenina reference. `benchmarks/fantlab/work270306-wikisource-diagnostic.json` records source-free results from the first full frozen replay; its boundary is explicitly `diagnostic_only`, `fantlab_source_edition_match=unknown`, `m2_parity_admissible=false`.

### Anna Karenina source identity

- FantLab work 270306 reports its 19 September 2022 analysis as 1,692,647 characters and 253,275 words, but the public surface does not disclose analyzer-input edition or bytes.
- `corpus/candidates/source-edition-traces/tolstoy-anna-karenina-ru.json` keeps `fantlab_source_edition_match=unknown` and `m2_parity_admissible=false`.
- Russian Wikisource identifies the public transcription via FEB as Tolstoy, *Anna Karenina*, Nauka 1970, pp. 5–684 and marks the literary work public domain. The work is an eight-part, 239-chapter composite.
- `scriptorium/wikisource_freeze.py` defines the deterministic source-research contract. It fetches chapter revisions, accepts only narrowly observed Wikisource wrapper/template variants, fails closed on unsupported markup, strips navigation/notes/ref wrappers, and composes chapters in fixed part/chapter order with `\n\n` separators.
- The expanded captured receipt uses `scriptorium-source-revision-manifest-v1`; the canonical packed source-free artifact uses distinct `scriptorium-source-revision-packed-manifest-v1`. `scriptorium/source_revision_manifest.py` deterministically packs and decodes the canonical representation.
- `corpus/candidates/source-edition-traces/tolstoy-anna-karenina-ru.revisions.json` records all 239 revision IDs, timestamp offsets and MediaWiki SHA-1 identities in packed source-free form plus the composite identity. Its `captured_identity_sha256` binds the ordered title/revision/timestamp/SHA-1 projection to research artifact 10326711163. Novel prose is not committed.
- Frozen composite identity: 1,705,605 characters including spaces; 3,072,993 UTF-8 bytes; raw SHA-256 and `scriptorium-text-v1` normalized SHA-256 both `1dcf2af815f6288099f77a038d873690fb0dc72edf81d2094fd29f3d5a30c205`.
- `scriptorium/wikisource_replay.py` now re-fetches the exact recorded revision IDs, verifies title/timestamp/MediaWiki SHA-1 for every chapter, reconstructs the composite in memory and fails closed unless the committed composite identity is reproduced exactly.
- The frozen candidate is 12,958 characters longer than FantLab's displayed count. The first full diagnostic also finds 269,358 Scriptorium words versus FantLab's 253,275 (+16,083). These are diagnostic facts, not proof of source mismatch or FantLab counting behavior.
- `diagnostic_comparison_admissible=true` means deterministic comparison may run against this reproducible public candidate. It does **not** mean FantLab source identity is known.

### First full-work diagnostic

- Hosted run 34794221625 checked out analysis head `9ba8f36440b15fc41374209437048ae2e486d579`, passed 95/95 tests, replayed the exact frozen source and produced derived comparison data without persisting or uploading source prose.
- General diagnostic: characters +12,958; words +16,083; mean word length +0.03255 characters; mean sentence length -0.17415 characters relative to FantLab.
- Dialogue diagnostic: narration mean sentence length +0.67997 characters, dialogue mean -1.00362 characters, dialogue share -0.14537 percentage points, author text inside dialogue +21.37204 percentage points.
- Punctuation diagnostic: several rates are numerically close, but dash is +20.89370 per 1000 Scriptorium words and comma is -9.54543 per 1000 Scriptorium words. These gaps justify inspecting token/dash policy rather than tuning blindly.
- Vocabulary diagnostic: surface-form unique vocabulary is 33,373 versus FantLab's 12,770 (+20,603). Dictionary-dependent values remain null/not-run because FantLab's dictionary identity is unknown and no substitute dictionary was supplied.
- POS is deliberately absent from this diagnostic because native pinned pylem/provider execution remains `not_run`.
- All numeric rows remain unresolved or not-run as appropriate. Numeric closeness, including the exact zero delta for triple-exclamation frequency, does not promote any field to reproduced status without source identity and display/rounding evidence.

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
- The repository now also contains a source-free full-work diagnostic artifact for the frozen Anna Karenina candidate. It exposes concrete expected/actual/delta evidence while labeling source identity unknown and M2 inadmissible.
- `scriptorium-publication-manifest-v1`, `scriptorium-static-site-v1` and the gated Pages build/upload workflow are merged and fail closed on unsupported publication semantics.
- Publication triggers cover all renderer-supported canonical roots. Build/upload has passed hosted checks on PR/master; deployment remains intentionally disabled behind `SCRIPTORIUM_PAGES_DEPLOY_ENABLED=true` and repository Pages administration is a separate owner/admin effect.
- SCRIP-REPRO-005 does not activate Pages deployment and does not add source prose to publication output.

## Known risks / blockers

1. **FantLab source identity:** the uploaded analyzer input behind public results is not disclosed for the retained corpus candidates; M2 stays 0/5 until independent evidence closes this gap.
2. **Hidden algorithm details:** FantLab corrective coefficients and some implementation choices are unpublished.
3. **Text-boundary/counting inference:** the first full diagnostic now demonstrates material word-count and dash-policy gaps in addition to the known character gap; exact normalization, tokenization, sentence boundaries and displayed character-count semantics remain unproven.
4. **Dialogue author-remark semantics:** author-text-inside-dialogue differs by more than 21 percentage points on the unmatched frozen candidate; current delimiter/denominator semantics require investigation before any compatibility claim.
5. **Vocabulary dictionary identity:** FantLab's production dictionary/version is unknown, and the current surface-form unique-vocabulary candidate is far from the public reference.
6. **Morphology provider runtime:** native pylem build/runtime provenance remains unavailable in the current container.
7. **AOT/POS ambiguity:** noun/cardinal runtime collision, extra-category folding and homonym/prediction selection remain unresolved.
8. **Copyright:** web availability is not permission; work-specific legal evidence remains mandatory and source prose is not committed by default.
9. **Hosted CI scope:** the Pages workflow is publication/analyzer scoped, not a universal repository CI replacement. SCRIP-REPRO-005 adds a bounded frozen-source integration workflow for this diagnostic path.
10. **Pages activation:** code/workflow is merged but live deployment remains deliberately unactivated.

## Run selection rule

On each wake:

1. resolve `CURRENT_UNIT` review/recovery before new work;
2. inspect the exact PR head, checks and comments relevant to that unit;
3. otherwise choose the first dependency-satisfied queue row;
4. create/search the corresponding issue before implementation;
5. do exactly one bounded unit and update this file plus the project changelog/benchmark or provenance record in the same semantic change.

Do not create parallel units merely because another wake occurred.
