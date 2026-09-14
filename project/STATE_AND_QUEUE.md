# STATE_AND_QUEUE — Scriptorium

STATE_REVISION: 58
PHASE: M1 — Deterministic FantLab surface
LAST_COMMITTED_RUN_AT: 2026-09-14T12:03:00Z
LAST_RESULT: SCRIP-SITE-005 authored in Issue #52 / PR #53. A source-free provenance-only publication slice now exposes the frozen 129-revision Resurrection candidate through the deterministic static renderer while preserving FantLab source-edition match as unknown, diagnostic-only benchmark admissibility and M2 parity inadmissibility. The PR remains open for independent exact-head review; live Pages deployment remains disabled.
LAST_VERIFIED_PROGRESS: The authored branch is based on master 06c5e9f2c9fb674752af4472f95211fac39c7cf6. It adds `public-artifacts/tolstoy-resurrection-ru-provenance.json`, an explicit `scriptorium-work-provenance-showcase-v1` renderer contract, canonical cross-checks against the frozen source trace, fail-closed promotion tests, README navigation and publication-source trigger coverage. Native pylem/provider execution was re-checked before selection and remains infrastructure `not_run`: pylem is absent from the execution runtime and the required GitHub/PyPI package hosts are not DNS-resolvable from that runtime. Hosted exact-head PR evidence is pending after this state commit and must be judged by a later wake before merge.

## Current unit

```text
UNIT_ID:        SCRIP-SITE-005
ISSUE:          #52
STATUS:         REVIEW
PR:             #53
BRANCH:         scrip-site-005-resurrection-provenance
BASE_COMMIT:    06c5e9f2c9fb674752af4472f95211fac39c7cf6
NEXT_ACTION:    Independently inspect the exact final PR #53 head, changed-file surface,
                review threads and hosted Pages/reproduction workflow evidence. Verify
                generated output contains the provenance-only Resurrection page and no
                source prose. Merge only if all fail-closed source-match/parity/publication
                boundaries remain intact. Do not self-approve from this authoring run.
```

## Current milestone gate

M0 is closed. M1 remains open. General, dialogue, vocabulary and punctuation families are executable inferred candidates. POS aggregation has a versioned provider-neutral candidate artifact, but native pinned pylem/provider execution identity remains unverified. The benchmark harness has one reproducibly frozen full-work *Anna Karenina* diagnostic whose FantLab analyzer-input edition is unknown. `tolstoy-resurrection-ru` is a second reproducibly frozen public-domain candidate with 129 pinned chapter revisions and deterministic composite identity, but FantLab source identity remains unknown. The M2 reproduction gate remains **0/5 source-matched works**.

## Queue

Evaluate rows in priority order and skip dependencies that are not executable. Recovery/review-ready work preempts new selection.

| Priority | Unit | Mode | Deliverable | Gate / dependency |
| --- | --- | --- | --- | --- |
| P1 | SCRIP-MORPH-003 | implementation | Bind pinned pylem/provider execution and wire POS artifacts into diagnostic benchmark comparison | SCRIP-MORPH-002; verified provider/runtime provenance; currently blocked because the execution runtime has no installed pylem and cannot resolve required GitHub/PyPI package hosts |
| P2 | SCRIP-DIALOGUE-002 | analyzer core / reproduction | Investigate author-text-inside-dialogue gap via inspectable delimiter and denominator sensitivity | DONE in Issue #45 / PR #46; merged as 25555ba1b719ac2dae8bc340701433ce16f8ed64 |
| P3 | SCRIP-REPRO-006 | benchmark / reproduction | Pursue a second source-edition trace or stronger source-matching evidence for a retained >=300k FantLab candidate | DONE in Issue #47 / PR #48; merged as f7a6937bb89b6a44ff21e8193c38c1c70af9aa01 |
| P4 | SCRIP-REPRO-007 | benchmark / reproduction | Freeze Resurrection by pinning/replaying all 129 chapter revisions and recording composite identities | DONE in Issue #50 / PR #51; merged as d31ab4417d979fd141df31d400d4fa5156adf274; source match remains unknown |
| P5 | SCRIP-SITE-005 | public representation | Publish the newly frozen Resurrection capability as derived/provenance-only public material | REVIEW in Issue #52 / PR #53; no source prose, source-match/parity promotion or Pages activation allowed |

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
- The 9,591-character difference from FantLab's displayed count is not source-match evidence. `fantlab_source_edition_match=unknown`, diagnostic-only comparison remains allowed, `m2_parity_admissible=false`.
- FantLab's work-page TXT route is volatile and redirects to LitRes trial content; it is excluded from analyzer-input identity evidence.

### Existing full-work diagnostic

- Anna Karenina diagnostic: characters +12,958; words +16,083; mean word length +0.03255 characters; mean sentence length -0.17415 characters relative to FantLab.
- Dialogue: narration mean sentence length +0.67997 characters, dialogue mean -1.00362 characters, dialogue share -0.14537 percentage points, author text inside dialogue +21.37204 percentage points before the sensitivity probe.
- Surface-form unique vocabulary is +20,603 relative to FantLab; dictionary-dependent values remain unresolved because FantLab dictionary identity is unknown.
- POS actuals remain absent because native pinned pylem/provider execution is still `not_run`.

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

- `pylem==0.0.18` remains the selected AOT-lineage compatibility candidate with pinned source/dictionary provenance.
- Fifteen runtime strings have direct candidate mappings. Runtime `N` collapses noun/cardinal; extra categories and FantLab homonym/prediction behavior remain unresolved.
- Native provider execution remains infrastructure-blocked in the current execution runtime; this is not a pylem failure.

### Public repository representation

- Two derived *Anna Karenina* excerpt showcases remain allow-listed, explicitly short/non-corpus/non-parity and source-free.
- `scriptorium-publication-manifest-v1`, `scriptorium-static-site-v1` and the gated Pages workflow remain fail-closed. Live deployment is disabled behind `SCRIPTORIUM_PAGES_DEPLOY_ENABLED=true` plus repository Pages administration.
- SCRIP-SITE-005 adds one provenance-only *Resurrection* public artifact whose canonical fields are cross-checked against the frozen source trace. The renderer rejects source-match, parity or compatibility promotion and does not publish source prose.
- Pages trigger coverage now includes `corpus/candidates/source-edition-traces/**` in addition to all renderer artifact roots, so provenance-source changes cannot silently bypass the publication build.

## Known risks / blockers

1. FantLab analyzer-input bytes are undisclosed; M2 remains 0/5 source-matched works.
2. FantLab corrective coefficients and parser details are partly unpublished.
3. Word-boundary semantics remain unproven after simple numeric/hyphen probes explained little of the full-work gap.
4. FantLab's actual hyphen/dash classifier remains unpublished.
5. Dialogue author-remark grammar/denominator semantics remain unknown.
6. FantLab dictionary/version identity is unknown.
7. Native pylem build/runtime provenance is unavailable in the current execution runtime.
8. AOT/POS noun-cardinal collision, extra-category folding and homonym/prediction selection remain unresolved.
9. The frozen Resurrection candidate's relationship to FantLab's uploaded analyzer input is unknown; its 9,591-character display delta must not be fitted or promoted to source-match evidence.
10. Work-specific copyright/provenance evidence remains mandatory; source prose is not committed by default.
11. Pages activation is a separate owner/admin effect and remains off.

## Run selection rule

On each wake:

1. resolve `CURRENT_UNIT` review/recovery before new work;
2. inspect the exact PR head, checks and comments relevant to that unit;
3. otherwise re-check P1 provider/runtime executability, then choose the first dependency-satisfied queue row;
4. create/search the corresponding issue before implementation;
5. do exactly one bounded unit and update this file plus the project changelog/benchmark or provenance record in the same semantic change.

Do not create parallel units merely because another wake occurred.
