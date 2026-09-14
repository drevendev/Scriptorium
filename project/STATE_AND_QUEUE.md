# STATE_AND_QUEUE — Scriptorium

STATE_REVISION: 60
PHASE: M1 — Deterministic FantLab surface
LAST_COMMITTED_RUN_AT: 2026-09-14T19:54:00Z
LAST_RESULT: SCRIP-MORPH-003 provider-execution slice independently reviewed, repaired for one stale documentation claim, re-verified on exact final head 8995b9d107ed1dbd9269254023c947a26d0490ce, and squash-merged as a46cdf73499cd4857ecdb9440936463514cb63ba. Exact hash-pinned pylem 0.0.18 native execution is now demonstrated on the isolated Ubuntu 22.04 / Python 3.9 compatibility lane while the main Scriptorium provider contract remains verified on Ubuntu 24.04 / Python 3.13. FantLab dictionary identity, homonym selection, noun/cardinal recovery and M2 parity remain unresolved.
LAST_VERIFIED_PROGRESS: Independent review found no blocking semantic defect in PR #55 and no review threads. The review did find one blocking documentation defect: docs/AOT_PYLEM_COMPATIBILITY.md still said native execution was not run after hosted execution had succeeded. That stale statement and the stale PR-body Python-version description were repaired without changing analyzer/provider semantics. Fresh exact-final-head runs then all passed: pinned-provider run 34889467872 passed the Python 3.13 full contract suite and the Ubuntu 22.04 / Python 3.9 exact-sdist install/native smoke; frozen-diagnostic run 34889467980 succeeded; Pages run 34889467982 succeeded. Final-head native artifact 10366241024 is 845 bytes with GitHub-recorded archive digest sha256:2015d94e4e3f7aee193575f0c57cf4db43d3ae21d55e006908b9fb7f25802dc8. The workflow asserts provider pylem 0.0.18, runtime profile pylem-0.0.18-python39-sidecar-v1, source_text_included=false, FantLab dictionary equivalence unknown and m2_parity_admissible=false. Issue #54 closed with the squash merge. Benchmark movement remains 0/5 source-matched works.

## Current unit

```text
UNIT_ID:        SCRIP-MORPH-003
ISSUE:          #54
STATUS:         DONE (provider execution slice)
PR:             #55
MERGED_COMMIT:  a46cdf73499cd4857ecdb9440936463514cb63ba
NEXT_ACTION:    Select the next bounded SCRIP-MORPH-003 continuation: wire the now-verified
                isolated pylem sidecar/provider output into source-free frozen-work POS
                diagnostic artifacts and benchmark comparison, preserving all ambiguity,
                source-match and M2 fail-closed boundaries. Do not treat provider
                executability as FantLab morphology parity.
```

## Current milestone gate

M0 is closed. M1 remains open. General, dialogue, vocabulary and punctuation families are executable inferred candidates. POS aggregation has a versioned provider-neutral candidate artifact, and exact hash-pinned pylem/provider execution provenance is now verified in an isolated legacy compatibility lane. Full frozen-work POS diagnostic transport/wiring has not yet landed. The benchmark harness has one reproducibly frozen full-work *Anna Karenina* diagnostic whose FantLab analyzer-input edition is unknown. `tolstoy-resurrection-ru` is a second reproducibly frozen public-domain candidate with 129 pinned chapter revisions and deterministic composite identity, but FantLab source identity remains unknown. The M2 reproduction gate remains **0/5 source-matched works**.

## Queue

Evaluate rows in priority order and skip dependencies that are not executable. Recovery/review-ready work preempts new selection.

| Priority | Unit | Mode | Deliverable | Gate / dependency |
| --- | --- | --- | --- | --- |
| P1 | SCRIP-MORPH-003 | implementation / reproduction | Wire verified pinned pylem sidecar/provider output into frozen diagnostic POS artifacts and benchmark comparison | SCRIP-MORPH-002; provider/runtime provenance established in Issue #54 / PR #55; next continuation is unblocked, while noun/cardinal, extra-category folding and FantLab homonym/dictionary behavior remain unresolved |
| P2 | SCRIP-DIALOGUE-002 | analyzer core / reproduction | Investigate author-text-inside-dialogue gap via inspectable delimiter and denominator sensitivity | DONE in Issue #45 / PR #46; merged as 25555ba1b719ac2dae8bc340701433ce16f8ed64 |
| P3 | SCRIP-REPRO-006 | benchmark / reproduction | Pursue a second source-edition trace or stronger source-matching evidence for a retained >=300k FantLab candidate | DONE in Issue #47 / PR #48; merged as f7a6937bb89b6a44ff21e8193c38c1c70af9aa01 |
| P4 | SCRIP-REPRO-007 | benchmark / reproduction | Freeze Resurrection by pinning/replaying all 129 chapter revisions and recording composite identities | DONE in Issue #50 / PR #51; merged as d31ab4417d979fd141df31d400d4fa5156adf274; source match remains unknown |
| P5 | SCRIP-SITE-005 | public representation | Publish the newly frozen Resurrection capability as derived/provenance-only public material | DONE in Issue #52 / PR #53; merged as 905ddd9b4f0f8665e3748bb6a0b70b4b39c0562d; source prose excluded, source match unknown, Pages activation unchanged |

## Evidence already established

### FantLab / reproduction boundary

- FantLab article 374 publicly lists sentence/dialogue, vocabulary, POS and punctuation surfaces while stating that some implementation details/corrective coefficients remain unpublished know-how.
- `fantlab-2022-v1` is the frozen compatibility contract. `scriptorium-benchmark-v1` records source/legal identity, hashes, analyzer configuration, expected/actual values and deltas.
- Exact integer `pass`/`fail` requires admissible exact source identity. Decimal/rate comparisons remain unresolved until display precision/rounding behavior is independently established.
- The retained five-work parity seed remains **0/5 source-matched**. Diagnostic resemblance is never parity.

### Frozen Anna Karenina candidate

- FantLab work 270306 reports its 19 September 2022 analysis as 1,692,647 characters and 253,275 words but does not disclose analyzer-input edition or bytes.
- Russian Wikisource identifies the public transcription via FEB as Tolstoy, *Anna Karenina*, Nauka 1970, pp. 5–684 and marks the literary work public domain.
- `corpus/candidates/source-edition-traces/tolstoy-anna-karenina-ru.revisions.json` freezes all 239 chapter revision identities. Exact replay verifies each revision before reconstructing the composite in memory.
- Frozen composite: 1,705,605 characters; 3,072,993 UTF-8 bytes; raw and `scriptorium-text-v1` normalized SHA-256 `1dcf2af815f6288099f77a038d873690fb0dc72edf81d2094fd29f3d5a30c205`.
- `fantlab_source_edition_match=unknown`; full-work comparisons are diagnostic only; M2 parity is inadmissible.

### Frozen Resurrection candidate

- FantLab work 296603 reports a 19 September 2022 analysis at 881,244 characters and 126,457 words but discloses neither source edition nor immutable analyzer-input bytes.
- Russian Wikisource identifies Alexey Komarov's library as the transcription source, exposes permanent work-index revision `oldid=5614128`, marks the literary work public domain, and traces to `Л. Н. Толстой. Собрание сочинений в восьми томах. Т. 6. М., "Лексика", 1996.`
- The source structure is 59 + 42 + 28 = 129 chapters. `corpus/candidates/source-edition-traces/tolstoy-resurrection-ru.revisions.json` pins every chapter revision ID, timestamp and MediaWiki SHA-1 without source prose.
- `scriptorium-wikisource-resurrection-body-v1` is the explicit source-specific extraction contract; `scriptorium-wikisource-composite-v1` fixes part/chapter order and separators.
- Frozen composite: 890,835 characters; 1,610,692 UTF-8 bytes; raw and normalized SHA-256 `2725a60a810d8aae4beff9dbc73ff85cf6da066b1c5272aaebf21addbe4ccaa0`.
- Independent exact-head review of SCRIP-REPRO-007 replayed all 129 revisions and reproduced the identity; the source-free replay artifact ZIP SHA-256 was `4b7cc1418db66c39a578dcce5165e7c421e08548c6ccc06cad979a324621c240`.
- SCRIP-SITE-005 now publishes a source-free provenance-only view of this frozen candidate. Its public artifact is cross-checked against the canonical trace and the renderer rejects source-match, M2-parity, compatibility or source-text promotion.
- The 9,591-character difference from FantLab's displayed count is not source-match evidence. `fantlab_source_edition_match=unknown`, diagnostic-only comparison remains allowed, `m2_parity_admissible=false`.
- FantLab's work-page TXT route is volatile and redirects to LitRes trial content; it is excluded from analyzer-input identity evidence.

### Existing full-work diagnostic

- Anna Karenina diagnostic: characters +12,958; words +16,083; mean word length +0.03255 characters; mean sentence length -0.17415 characters relative to FantLab.
- Dialogue: narration mean sentence length +0.67997 characters, dialogue mean -1.00362 characters, dialogue share -0.14537 percentage points, author text inside dialogue +21.37204 percentage points before the sensitivity probe.
- Surface-form unique vocabulary is +20,603 relative to FantLab; dictionary-dependent values remain unresolved because FantLab dictionary identity is unknown.
- POS actuals remain absent because the verified legacy provider has not yet been wired through a source-free sidecar transport into the frozen-work diagnostic; provider executability itself is now verified.

### Word / punctuation policy findings

- SCRIP-TEXT-004 showed numeric-only tokens explain only 17 of the +16,083 word gap and U+2010/U+2011 lexical-connector treatment changes the frozen candidate word count by zero.
- `scriptorium-punctuation-v2` no longer double-counts ASCII `-` already retained inside a `scriptorium-text-v1` word token as dash punctuation. Token-external ASCII hyphen-minus and U+2010..U+2014 remain inferred dash candidates.
- Frozen punctuation-v2 diagnostic remains about +14.913 dash events per 1000 current words relative to FantLab, so the change is internal consistency rather than parity evidence.

### Dialogue sensitivity

- `scriptorium-dialogue-policy-diagnostic-v1` is source-free and does not change production `scriptorium-dialogue-v1` semantics.
- Frozen candidate current-v1 author text over dialogue is 38.3920% versus FantLab 17.02% (+21.3720 pp); the punctuation-shaped opener probe is 35.2367% (+18.2167 pp).
- Whole-text denominator variants are 13.4275% and 12.3239%, below FantLab. Denominator semantics therefore remain a material unresolved axis.
- Every variant remains diagnostic-only because analyzer-input edition identity is unknown.

### Morphology compatibility

- `pylem==0.0.18` remains the selected AOT-lineage compatibility candidate with immutable sdist SHA-256 `66c0d13414006a803f200979540fcee9653738701c14496a418db67542b26515` and pinned source/dictionary provenance.
- Fifteen runtime strings have direct candidate mappings. Runtime `N` collapses noun/cardinal; five extra categories and FantLab homonym/prediction behavior remain unresolved.
- Hosted provider executability is verified. Exact-final-head run `34889467872` checked out `8995b9d107ed1dbd9269254023c947a26d0490ce`; its Ubuntu 24.04 / Python 3.13 contract job passed the complete standard-library suite, and its isolated Ubuntu 22.04 / Python 3.9 native job installed the hash-pinned sdist unchanged, executed the native smoke and uploaded the source-free receipt.
- Final-head runtime artifact `10366241024` is 845 bytes with GitHub-recorded archive digest `sha256:2015d94e4e3f7aee193575f0c57cf4db43d3ae21d55e006908b9fb7f25802dc8`. Its workflow contract keeps `fantlab_dictionary_equivalence=unknown` and `m2_parity_admissible=false`.
- The pinned legacy source is toolchain-sensitive: an Ubuntu 24.04 / GCC 13 native attempt failed inside vendored `morph_dict`; the compatibility lane therefore remains isolated on Ubuntu 22.04 / Python 3.9 rather than patching upstream bytes. This is a maintainability constraint, not an active provider-executability blocker.

### Public repository representation

- Two derived *Anna Karenina* excerpt showcases remain allow-listed, explicitly short/non-corpus/non-parity and source-free.
- `scriptorium-publication-manifest-v1`, `scriptorium-static-site-v1` and the gated Pages workflow remain fail-closed. Live deployment is disabled behind `SCRIPTORIUM_PAGES_DEPLOY_ENABLED=true` plus repository Pages administration.
- SCRIP-SITE-005 adds one provenance-only *Resurrection* public artifact whose canonical fields are cross-checked against the frozen source trace. The renderer rejects source-match, parity or compatibility promotion and does not publish source prose.
- Pages trigger coverage includes `corpus/candidates/source-edition-traces/**` in addition to all renderer artifact roots, so provenance-source changes cannot silently bypass the publication build.
- Exact-final-head Pages run `34889467982` also succeeded for PR #55; the live deployment gate remains unchanged and Pages administration is still a separate owner/admin effect.

## Known risks / blockers

1. FantLab analyzer-input bytes are undisclosed; M2 remains 0/5 source-matched works.
2. FantLab corrective coefficients and parser details are partly unpublished.
3. Word-boundary semantics remain unproven after simple numeric/hyphen probes explained little of the full-work gap.
4. FantLab's actual hyphen/dash classifier remains unpublished.
5. Dialogue author-remark grammar/denominator semantics remain unknown.
6. FantLab dictionary/version identity is unknown.
7. The verified pylem 0.0.18 compatibility backend is constrained to the isolated Ubuntu 22.04 / Python 3.9 lane because the pinned legacy source does not compile unchanged under the tested Ubuntu 24.04 / GCC 13 native toolchain.
8. AOT/POS noun-cardinal collision, extra-category folding and homonym/prediction selection remain unresolved.
9. The frozen Resurrection candidate's relationship to FantLab's uploaded analyzer input is unknown; its 9,591-character display delta must not be fitted or promoted to source-match evidence.
10. Work-specific copyright/provenance evidence remains mandatory; source prose is not committed by default.
11. Pages activation is a separate owner/admin effect and remains off.

## Run selection rule

On each wake:

1. resolve `CURRENT_UNIT` review/recovery before new work;
2. inspect the exact PR head, checks and comments relevant to that unit;
3. otherwise choose the first dependency-satisfied queue row, with P1 morphology now executable through its verified hosted compatibility lane;
4. create/search the corresponding issue before implementation;
5. do exactly one bounded unit and update this file plus the project changelog/benchmark or provenance record in the same semantic change.

Do not create parallel units merely because another wake occurred.
