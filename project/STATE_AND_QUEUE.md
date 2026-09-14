# STATE_AND_QUEUE — Scriptorium

STATE_REVISION: 53
PHASE: M1 — Deterministic FantLab surface
LAST_COMMITTED_RUN_AT: 2026-09-14T07:52:43Z
LAST_RESULT: SCRIP-DIALOGUE-002 independently reviewed on exact head 2dd86cc159dc87e09185b532a3727ee0797c6e38 and squash-merged as 25555ba1b719ac2dae8bc340701433ce16f8ed64. The source-free dialogue sensitivity diagnostic is now on master; production `scriptorium-dialogue-v1` is unchanged, FantLab source identity remains unknown, and M2 remains 0/5 source-matched works.
LAST_VERIFIED_PROGRESS: Independent review found no blocking defect. PR #46 was 10 commits ahead / 0 behind master, mergeable and non-draft. Frozen run 34818880313 checked out the exact head, used Python 3.13.15, passed 103/103 standard-library tests, replayed all 239 pinned Wikisource revisions and uploaded derived evidence only. Independently downloaded artifact 10337900179 matched GitHub SHA-256 48550ddceba52f0f57a31168ff214bee371d9a338551c76dce2b43add29755b8, contained exactly one derived JSON, bound itself to the exact head and preserved `fantlab_source_edition_match=unknown`, `diagnostic_only`, `m2_parity_admissible=false`. Exact-head Pages run 34818880306 succeeded with deploy skipped. PR #46 was squash-merged as 25555ba1b719ac2dae8bc340701433ce16f8ed64; Issue #45 closed completed and master push Pages run 34819812044 completed successfully.

## Current unit

```text
UNIT_ID:        SCRIP-DIALOGUE-002
ISSUE:          #45
STATUS:         DONE
PR:             #46
MERGED_COMMIT:  25555ba1b719ac2dae8bc340701433ce16f8ed64
NEXT_ACTION:    Re-check SCRIP-MORPH-003 provider/runtime executability first. If native
                pinned pylem/provider execution is still unavailable, select
                SCRIP-REPRO-006 and pursue a second source-edition trace or stronger
                source-matching evidence for a retained >=300k FantLab candidate.
```

## Current milestone gate

M0 is closed. M1 remains open. General, dialogue, vocabulary and punctuation families are executable inferred candidates. POS aggregation has a versioned provider-neutral candidate artifact, but native pinned pylem/provider execution identity remains unverified. The benchmark harness has one reproducibly frozen full-work *Anna Karenina* diagnostic, but its FantLab analyzer-input edition is unknown. SCRIP-DIALOGUE-002 is merged as diagnostic-only sensitivity evidence; it changes no production dialogue semantics. The M2 reproduction gate remains **0/5 source-matched works**.

## Queue

Evaluate rows in priority order and skip dependencies that are not executable.

| Priority | Unit | Mode | Deliverable | Gate / dependency |
| --- | --- | --- | --- | --- |
| P1 | SCRIP-MORPH-003 | implementation | Bind pinned pylem/provider execution and wire POS artifacts into diagnostic benchmark comparison | SCRIP-MORPH-002; verified provider/runtime provenance; currently blocked because the execution container has no installed pylem and cannot resolve required GitHub/PyPI package hosts |
| P2 | SCRIP-DIALOGUE-002 | analyzer core / reproduction | Investigate the author-text-inside-dialogue gap via inspectable delimiter and denominator sensitivity without fitting the source-unmatched target | DONE in Issue #45 / PR #46; merged as 25555ba1b719ac2dae8bc340701433ce16f8ed64 |
| P3 | SCRIP-REPRO-006 | benchmark / reproduction | After dialogue review, pursue a second source-edition trace or stronger source-matching evidence for a retained >=300k FantLab candidate | Requires a legally usable candidate and immutable source identity evidence; must not infer FantLab input bytes from bibliographic resemblance |
| P4 | SCRIP-SITE-005 | public representation | Add the next honest derived showcase slice only after a newly verified metric/corpus capability creates useful public material | Must publish derived/provenance data only; no source prose or parity overclaim |

## Evidence already established

### FantLab / benchmark boundary

- FantLab article 374 publicly lists mean narration/dialogue sentence length, dialogue share, author text inside dialogue, vocabulary, POS and punctuation surfaces, while stating that some implementation details/corrective coefficients remain unpublished know-how.
- `fantlab-2022-v1` is the frozen compatibility contract. `scriptorium-benchmark-v1` records source/legal identity, hashes, analyzer configuration, expected/actual values and deltas.
- Exact integer `pass`/`fail` requires admissible exact source identity. Decimal/rate comparisons remain unresolved until display precision/rounding behavior is independently established.
- The retained five-work parity seed remains **0/5 source-matched**. Diagnostic resemblance is never parity.

### Frozen Anna Karenina source identity

- FantLab work 270306 reports its 19 September 2022 analysis as 1,692,647 characters and 253,275 words, with dialogue share 35.12% and author text inside dialogue 17.02%, but the public surface does not disclose analyzer-input edition or bytes.
- Russian Wikisource identifies the public transcription via FEB as Tolstoy, *Anna Karenina*, Nauka 1970, pp. 5–684 and marks the literary work public domain. The work is an eight-part, 239-chapter composite.
- `corpus/candidates/source-edition-traces/tolstoy-anna-karenina-ru.revisions.json` records all 239 revision identities in source-free packed form. `scriptorium/wikisource_replay.py` re-fetches those exact revisions and verifies each identity before reconstructing the composite in memory.
- Frozen composite identity: 1,705,605 characters including spaces; 3,072,993 UTF-8 bytes; raw and `scriptorium-text-v1` normalized SHA-256 `1dcf2af815f6288099f77a038d873690fb0dc72edf81d2094fd29f3d5a30c205`.
- `fantlab_source_edition_match=unknown`, `diagnostic_comparison_admissible=true` only for reproducible diagnostics, and `m2_parity_admissible=false`.

### Existing full-work diagnostic

- General diagnostic: characters +12,958; words +16,083; mean word length +0.03255 characters; mean sentence length -0.17415 characters relative to FantLab.
- Dialogue diagnostic before SCRIP-DIALOGUE-002: narration mean sentence length +0.67997 characters, dialogue mean -1.00362 characters, dialogue share -0.14537 percentage points, author text inside dialogue +21.37204 percentage points.
- Vocabulary surface unique words are +20,603 relative to FantLab; dictionary-dependent values remain unresolved because FantLab dictionary identity is unknown.
- POS remains absent because native pinned pylem/provider execution is still `not_run`.

### Word / punctuation policy findings

- `SCRIP-TEXT-004` showed numeric-only tokens explain only 17 of the +16,083 word gap and U+2010/U+2011 lexical-connector treatment changes the frozen candidate word count by zero.
- `SCRIP-PUNCT-002` merged `scriptorium-punctuation-v2`: ASCII `-` retained inside a `scriptorium-text-v1` word token is no longer double-counted as dash punctuation; token-external ASCII hyphen-minus and U+2010..U+2014 remain inferred dash candidates.
- Frozen punctuation-v2 diagnostic remains about +14.913 dash events per 1000 current words relative to FantLab, so the hyphen fix is an internal consistency rule rather than parity evidence.

### Dialogue diagnostic — SCRIP-DIALOGUE-002

- Production `scriptorium-dialogue-v1` still treats dash-led LF-delimited paragraphs as dialogue and alternates every internal whitespace-dash-whitespace separator as speech -> author text -> speech.
- `scriptorium-dialogue-policy-diagnostic-v1` is a separate source-free sensitivity probe. It records current v1 remark counts plus a narrower opener probe that accepts comma/question/exclamation/ellipsis-shaped speech boundaries and then consumes the next internal separator as the closer.
- The probe reports only counts, context buckets and percentages; it does not retain source prose and does not change production dialogue semantics.
- Denominator sensitivity is explicit: current and boundary-filtered author-remark numerators are measured both over dialogue non-whitespace characters and over whole-text non-whitespace characters.
- Frozen candidate results: current v1 author text over dialogue is 38.3920% versus FantLab 17.02% (+21.3720 pp); the punctuation-shaped opener probe is 35.2367% (+18.2167 pp). Whole-text denominator variants are 13.4275% and 12.3239%, below the FantLab reference, so denominator semantics remain a material unresolved axis.
- The candidate contains 4,434 dialogue paragraphs and 5,353 internal separators. The narrower probe removes 197 candidate author-remark spans and 15,646 non-whitespace remark characters, explaining only about 3.155 pp of the dialogue-denominator gap.
- Every variant remains `diagnostic_only`; numerical closeness cannot establish FantLab semantics while the analyzer-input edition is unknown.
- Exact-head hosted review passed 103/103 tests and the 239-revision replay; artifact `10337900179` is derived-only and source-free. PR #46 is merged with no production profile versioning.

### Morphology compatibility

- `pylem==0.0.18` remains the selected AOT-lineage compatibility candidate with pinned source/dictionary provenance.
- Fifteen runtime strings have direct candidate mappings. Runtime `N` collapses noun/cardinal; extra categories and FantLab homonym/prediction behavior remain unresolved.
- Native provider execution remains infrastructure-blocked in the current execution container; this is not a pylem failure.

### Public repository representation

- Two derived *Anna Karenina* excerpt showcases remain public, explicitly short/non-corpus/non-parity, with no source prose committed.
- The repository contains source-free full-work and word/dash diagnostics linked from public docs; SCRIP-DIALOGUE-002 extends the hosted source-free diagnostic but does not itself activate or expand live Pages.
- `docs/DIALOGUE_MODEL.md` now documents the merged diagnostic boundary and denominator/delimiter uncertainty for repository visitors.
- `scriptorium-publication-manifest-v1`, `scriptorium-static-site-v1` and the gated Pages build/upload workflow remain fail-closed. Live deployment remains intentionally disabled behind `SCRIPTORIUM_PAGES_DEPLOY_ENABLED=true` plus repository Pages administration.

## Known risks / blockers

1. FantLab analyzer-input bytes are undisclosed; M2 remains 0/5 source-matched works.
2. FantLab corrective coefficients and parser details are partly unpublished.
3. Word-boundary semantics remain unproven after simple numeric/hyphen probes explained little of the full-work gap.
4. FantLab's actual hyphen/dash classifier remains unpublished.
5. Dialogue author-remark grammar/denominator semantics remain unknown; SCRIP-DIALOGUE-002 is diagnostic only.
6. FantLab dictionary/version identity is unknown.
7. Native pylem build/runtime provenance is unavailable in the current container.
8. AOT/POS noun-cardinal collision, extra-category folding and homonym/prediction selection remain unresolved.
9. Work-specific copyright/provenance evidence remains mandatory; source prose is not committed by default.
10. Pages activation is a separate owner/admin effect and remains off.

## Run selection rule

On each wake:

1. resolve `CURRENT_UNIT` review/recovery before new work;
2. inspect the exact PR head, checks and comments relevant to that unit;
3. otherwise re-check P1 provider/runtime executability, then choose the first dependency-satisfied queue row;
4. create/search the corresponding issue before implementation;
5. do exactly one bounded unit and update this file plus the project changelog/benchmark or provenance record in the same semantic change.

Do not create parallel units merely because another wake occurred.
