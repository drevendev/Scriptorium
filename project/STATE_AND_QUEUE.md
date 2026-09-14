# STATE_AND_QUEUE — Scriptorium

STATE_REVISION: 57
PHASE: M1 — Deterministic FantLab surface
LAST_COMMITTED_RUN_AT: 2026-09-14T11:24:00Z
LAST_RESULT: SCRIP-REPRO-007 independently reviewed on exact head 71aa90c32d0785d1f275bca6be1e022c2da1e301 and squash-merged as d31ab4417d979fd141df31d400d4fa5156adf274. The Resurrection public-domain candidate is now frozen on master as 129 exact Russian Wikisource revisions with source-specific extraction, immutable composite identity and replay-only verification. FantLab analyzer-input identity remains unknown and M2 remains 0/5 source-matched works.
LAST_VERIFIED_PROGRESS: Independent review found no blocking defect. PR #51 was 20 commits ahead / 0 behind master, mergeable and non-draft, with no review threads. Exact-head frozen-diagnostic run 34837032042 checked out 71aa90c32d0785d1f275bca6be1e022c2da1e301, used Python 3.13.15, passed 107/107 standard-library tests in the Resurrection replay job, replayed all 129 pinned revisions and reproduced the 890,835-character / 1,610,692-byte composite with raw and scriptorium-text-v1 normalized SHA-256 2725a60a810d8aae4beff9dbc73ff85cf6da066b1c5272aaebf21addbe4ccaa0. Exact-head artifact 10344417869 is a single source-free replay receipt; GitHub and independent download agree on ZIP SHA-256 4b7cc1418db66c39a578dcce5165e7c421e08548c6ccc06cad979a324621c240. Exact-head Pages run 34837032048 passed test/build/byte-identical rebuild/upload and skipped deployment. Searches over the committed revision manifest found no wikitext/prose/source_text payload keys. The merged trace remains fantlab_source_edition_match=unknown, diagnostic-only and m2_parity_admissible=false. Issue #50 closed completed with the merge. The squash merge commit had no hosted workflow run at bookkeeping time; this is recorded as no post-merge CI run, not as green CI.

## Current unit

```text
UNIT_ID:        SCRIP-REPRO-007
ISSUE:          #50
STATUS:         DONE
PR:             #51
MERGED_COMMIT:  d31ab4417d979fd141df31d400d4fa5156adf274
NEXT_ACTION:    Re-check SCRIP-MORPH-003 provider/runtime executability first. If native
                pinned pylem/provider execution is still unavailable, select SCRIP-SITE-005
                as the next dependency-satisfied queue row and expose the newly frozen
                Resurrection capability only through derived/provenance data, with no
                source prose or parity overclaim.
```

## Current milestone gate

M0 is closed. M1 remains open. General, dialogue, vocabulary and punctuation families are executable inferred candidates. POS aggregation has a versioned provider-neutral candidate artifact, but native pinned pylem/provider execution identity remains unverified. The benchmark harness has one reproducibly frozen full-work *Anna Karenina* diagnostic whose FantLab analyzer-input edition is unknown. `tolstoy-resurrection-ru` is now a second reproducibly frozen public-domain candidate with 129 pinned chapter revisions and deterministic composite identity, but FantLab source identity remains unknown. The M2 reproduction gate remains **0/5 source-matched works**.

## Queue

Evaluate rows in priority order and skip dependencies that are not executable.

| Priority | Unit | Mode | Deliverable | Gate / dependency |
| --- | --- | --- | --- | --- |
| P1 | SCRIP-MORPH-003 | implementation | Bind pinned pylem/provider execution and wire POS artifacts into diagnostic benchmark comparison | SCRIP-MORPH-002; verified provider/runtime provenance; currently blocked because the execution container has no installed pylem and cannot resolve required GitHub/PyPI package hosts |
| P2 | SCRIP-DIALOGUE-002 | analyzer core / reproduction | Investigate the author-text-inside-dialogue gap via inspectable delimiter and denominator sensitivity without fitting the source-unmatched target | DONE in Issue #45 / PR #46; merged as 25555ba1b719ac2dae8bc340701433ce16f8ed64 |
| P3 | SCRIP-REPRO-006 | benchmark / reproduction | Pursue a second source-edition trace or stronger source-matching evidence for a retained >=300k FantLab candidate | DONE in Issue #47 / PR #48; merged as f7a6937bb89b6a44ff21e8193c38c1c70af9aa01 |
| P4 | SCRIP-REPRO-007 | benchmark / reproduction | Freeze the retained Resurrection public candidate by pinning/replaying all 129 chapter revisions and recording composite raw/normalized identities before any full-work diagnostic | DONE in Issue #50 / PR #51; merged as d31ab4417d979fd141df31d400d4fa5156adf274; source prose remains uncommitted; FantLab source match remains unknown and M2 inadmissible |
| P5 | SCRIP-SITE-005 | public representation | Add the next honest derived showcase slice only after a newly verified metric/corpus capability creates useful public material | Frozen Resurrection candidate now supplies a verified corpus/provenance capability; publish derived/provenance data only, no source prose or parity overclaim |

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

### Frozen Resurrection source identity — SCRIP-REPRO-006 / SCRIP-REPRO-007

- FantLab work 296603 reports a 19 September 2022 analysis at 881,244 characters and 126,457 words, but its analysis surface discloses neither source edition nor immutable analyzer-input bytes.
- Russian Wikisource identifies Alexey Komarov's library as the transcription source, exposes permanent work-index revision `oldid=5614128`, and marks the literary work public domain. Komarov completes the citation as `Л. Н. Толстой. Собрание сочинений в восьми томах. Т. 6. М., "Лексика", 1996.`
- Wikisource and Komarov expose the same three-part structure: 59 + 42 + 28 = 129 chapters. `corpus/candidates/source-edition-traces/tolstoy-resurrection-ru.revisions.json` now pins all 129 chapter revision IDs, timestamps and MediaWiki SHA-1 identities without source prose.
- The source contains heterogeneous page scaffolding: observed early chapters can contain multiple `text`/`indent` div bodies while other chapters place prose directly after the `Отексте` header. `scriptorium-wikisource-resurrection-body-v1` makes that source-specific extraction decision explicit and versioned instead of changing the existing Anna contract.
- Frozen composite identity: 890,835 characters including spaces; 1,610,692 UTF-8 bytes; raw and `scriptorium-text-v1` normalized SHA-256 `2725a60a810d8aae4beff9dbc73ff85cf6da066b1c5272aaebf21addbe4ccaa0`.
- Hosted capture/replay on authored head `aeb07a66a6a1d3e62656b44a345429367294f24a` passed 107/107 tests and exact-revision replay. Artifact `10344631133` is source-free; independent download confirmed ZIP SHA-256 `379d193e016661350ca9e2bc11332480ea4d77307ca550180818f66fb3411fcd` and manifest file SHA-256 `0914ed84614a2e050ea79bf467511a2fcceef33d0d18d86c72dfe28039cde720`.
- Independent exact-head review of `71aa90c32d0785d1f275bca6be1e022c2da1e301` passed 107/107 tests plus exact 129-revision replay in hosted run `34837032042`; source-free replay artifact `10344417869` has ZIP SHA-256 `4b7cc1418db66c39a578dcce5165e7c421e08548c6ccc06cad979a324621c240`.
- The frozen candidate differs from FantLab's displayed character count by 9,591. That delta is not source-match evidence. `fantlab_source_edition_match=unknown`, `diagnostic_comparison_admissible=true` only for source-frozen diagnostics, and `m2_parity_admissible=false`.
- The FantLab work-page TXT route is volatile and redirects to LitRes trial content; it remains excluded from analyzer-input identity evidence.

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
- `docs/DIALOGUE_MODEL.md` documents the merged diagnostic boundary and denominator/delimiter uncertainty for repository visitors.
- `corpus/candidates/README.md` now exposes both frozen public-domain full-work candidates, their immutable identities and explicit source-match boundaries. The new Resurrection manifest contains only revision identities and derived composite hashes, never source prose.
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
9. The Resurrection public candidate is frozen, but its relationship to FantLab's uploaded analyzer input is unknown; a 9,591-character display delta must not be fitted or promoted to source-match evidence.
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
