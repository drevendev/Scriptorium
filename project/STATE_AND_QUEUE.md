# STATE_AND_QUEUE — Scriptorium

STATE_REVISION: 71
PHASE: M1 — Deterministic FantLab surface
LAST_COMMITTED_RUN_AT: 2026-09-15T05:57:00Z
LAST_RESULT: SCRIP-REPRO-008 / Issue #64 / PR #65 authored a durable source-edition trace for retained >=300k candidate `dostoevsky-brothers-karamazov-ru`. Official-source research now binds the public transcription bibliographically from Russian Wikisource through the Russian Virtual Library to Dostoevsky, Collected Works in 15 volumes, Leningrad: Nauka, 1991, volumes 9-10. Wikisource work-index revision 5616907 is recorded, while sampled Book I Chapter I has independent revision 1224742, proving the index oldid does not freeze the novel bytes. The candidate remains `traced_not_frozen`; diagnostic comparison is disabled, FantLab source-edition match is unknown, M2 parity is inadmissible, and benchmark movement remains 0/5 source-matched works. The substantive PR is intentionally unmerged pending independent exact-head review.
LAST_VERIFIED_PROGRESS: Fresh evidence reconfirmed FantLab work 168951's 18 September 2022 analysis at 1,807,107 characters and 281,507 words, but the public analysis surface still does not disclose analyzer-input edition or bytes. The current FantLab TXT excerpt route redirects to a LitRes trial endpoint and is explicitly excluded from source-identity evidence. Wikisource cites the 1991 Nauka volumes 9-10 and links RVB; RVB independently places parts I-III in volume 9 and part IV plus epilogue in volume 10 under that edition. The Wikisource index exposes an author preface, twelve books across four parts and 96 numbered chapter/epilogue leaves, but the exact text-bearing inventory, wrapper participation, extraction semantics, per-leaf revisions and composite hashes remain unfrozen. No source prose is committed. This state commit creates a newer PR head, so a later review must require fresh exact-final-head checks before merge. Benchmark movement remains 0/5 source-matched works.

## Current unit

```text
UNIT_ID:        SCRIP-REPRO-008
ISSUE:          #64
STATUS:         REVIEW
PR:             #65
BASE_REVISION:  257b35ea507e659d45f7c597f8ebb90df5cbb214
NEXT_ACTION:    Independently review the exact final PR head, changed-file surface,
                comments/threads and hosted checks. Confirm that the trace accurately
                preserves the Wikisource -> RVB -> Nauka 1991 vols. 9-10 provenance
                chain, that work-index revision 5616907 is not mistaken for leaf-byte
                identity, and that no source prose or source-match/parity promotion was
                introduced. Merge only if those boundaries hold; otherwise repair the
                exact defect.
```

## Current milestone gate

M0 is closed. M1 remains open. General, dialogue, vocabulary and punctuation families are executable inferred candidates. POS aggregation has a versioned provider-neutral artifact, reviewed exact-pylem frozen-work transport, reviewed source-free undefined-reason decomposition, and reviewed provider-side homonym-weight diagnostics. The repository now also publishes a reviewed source-free full-work Anna Karenina morphology showcase. M2 remains open at **0/5 source-matched works** because no retained FantLab analyzer-input edition/byte identity is independently established.

## Queue

Evaluate rows in priority order and skip dependencies that are not executable. Recovery/review-ready work and failing required checks preempt normal selection.

| Priority | Unit | Mode | Deliverable | Gate / dependency |
| --- | --- | --- | --- | --- |
| P0 | SCRIP-REPRO-008 | review / benchmark provenance | Independently review and, if exact-head evidence is clean, merge PR #65 Brothers Karamazov source-edition trace | Issue #64 / PR #65 open; authored substantive unit must not self-merge |
| P1 | SCRIP-REPRO-009 | benchmark / provenance | Verify and freeze the complete Brothers Karamazov text-bearing Wikisource leaf inventory, exact revisions, source-specific extraction/composition and composite hashes without source prose | Depends on SCRIP-REPRO-008 merge; public candidate remains `traced_not_frozen` |
| P2 | SCRIP-MORPH continuation | analyzer core / reproduction | Investigate the next largest unresolved morphology axis with inspectable evidence, without guessing runtime `N`, extra-category folding, FantLab homonym selection, dictionary identity or service-word aggregation | M006 merged; provider homonym-weight signal is diagnostic only |
| P3 | SCRIP-CORPUS continuation | corpus / provenance | Add or strengthen legally usable >=300k candidates, prioritizing diversity beyond 19th-century Russian classics when licensing/source identity is strong enough | Preserve translation identity and explicit legal provenance |

## Evidence already established

### FantLab / reproduction boundary

- `fantlab-2022-v1` is the frozen compatibility contract. FantLab publicly documents broad metric families while leaving some coefficients/parser details unpublished.
- Exact integer parity is admissible only with exact source-edition identity, legal basis and immutable text digest. Decimal/rate parity additionally requires independently established display-rounding behavior.
- The retained parity seed remains **0/5 source-matched works**. Diagnostic resemblance never advances M2.

### Frozen Anna Karenina candidate

- FantLab work 270306 reports its 19 September 2022 analysis at 1,692,647 characters and 253,275 words but does not disclose analyzer-input edition/bytes.
- The frozen Russian Wikisource/FEB candidate replays 239 pinned chapter revisions deterministically.
- Composite identity: 1,705,605 characters; 3,072,993 UTF-8 bytes; raw and `scriptorium-text-v1` normalized SHA-256 `1dcf2af815f6288099f77a038d873690fb0dc72edf81d2094fd29f3d5a30c205`.
- `fantlab_source_edition_match=unknown`; every full-work comparison remains diagnostic-only and M2-inadmissible.

### Frozen Resurrection candidate

- FantLab work 296603 reports 881,244 characters and 126,457 words but does not disclose immutable analyzer-input identity.
- 129 Wikisource chapter revisions are pinned and replayed under explicit extraction/composition contracts.
- Composite identity: 890,835 characters; 1,610,692 UTF-8 bytes; raw/normalized SHA-256 `2725a60a810d8aae4beff9dbc73ff85cf6da066b1c5272aaebf21addbe4ccaa0`.
- Source match remains unknown; the 9,591-character display delta is not identity evidence.

### Brothers Karamazov traced candidate

- FantLab work 168951 reports its 18 September 2022 analysis at 1,807,107 characters and 281,507 words but does not disclose analyzer-input edition/bytes.
- Russian Wikisource identifies its transcription source as Dostoevsky, *Collected Works in 15 volumes*, Leningrad: Nauka, 1991, volumes 9-10 and links the Russian Virtual Library electronic edition.
- RVB independently identifies volume 9 as the 1991 Nauka edition containing parts I-III and volume 10 as the same edition containing part IV plus epilogue; the electronic publication is identified as RVB version 3.0 dated 27 January 2017.
- Wikisource permanent work-index revision `oldid=5616907` freezes only the index. Sampled Book I Chapter I exposes its own permanent revision `oldid=1224742`, so the index revision cannot stand in for full-text byte identity.
- The index exposes an author preface, twelve books across four parts and 96 numbered chapter/epilogue leaves. This is an observed structure, not yet a canonical text-bearing inventory: wrapper participation and exact leaf set still require verification before a composition contract can be frozen.
- The sampled chapter reports no reviewed version. This is recorded as transcription-QA evidence and does not weaken the separate bibliographic provenance/legal-basis claim.
- FantLab's current TXT excerpt route redirects to a LitRes trial endpoint (`art=171949`); that behavior is explicitly inadmissible as analyzer-input identity evidence.
- `source_identity_status=traced_not_frozen`, `fantlab_source_edition_match=unknown`, `diagnostic_ready=false`, `gate_ready=false`, and `m2_parity_admissible=false`.

### Deterministic metric findings

- Frozen Anna Karenina diagnostic deltas include characters +12,958 and words +16,083 relative to FantLab; simple numeric-token and lexical-hyphen probes explain little of the word gap.
- `scriptorium-punctuation-v2` removes internal ASCII-hyphen double counting, but the frozen dash rate still materially exceeds FantLab.
- Dialogue author-remark/denominator semantics remain unresolved: production-v1 author text inside dialogue is 38.3920% versus FantLab 17.02%, and tested sensitivity variants do not establish parity.
- FantLab dictionary identity is unknown, so dictionary-dependent vocabulary metrics remain unresolved.

### Morphology compatibility

- `pylem==0.0.18` is pinned by exact sdist SHA-256 `66c0d13414006a803f200979540fcee9653738701c14496a418db67542b26515` plus pinned source/dictionary provenance.
- Fifteen runtime strings map directly as inferred candidates. Runtime `N` collapses noun/cardinal; `POSL`, `COLLOC`, `ADJ_SHORT`, `PARTICIPLE_SHORT` and `INFINITIVE` remain unresolved extra categories.
- `scriptorium-pos-v1` resolves a token only when all supplied analyses map to the same direct FantLab-shaped bucket. Empty analyses, `N`, extra categories, unknown codes and cross-bucket homonyms remain undefined.
- Exact pylem 0.0.18 executability is verified in the isolated Ubuntu 22.04 / Python 3.9 lane; the modern Scriptorium contract suite remains on Ubuntu 24.04 / Python 3.13.
- The reviewed frozen POS diagnostic contains 269,358 Scriptorium word tokens: 117,554 conservatively defined and 151,804 undefined. Noun/cardinal remain zero by design because `N` is unresolved.
- Reviewed undefined decomposition: 55,081 `runtime_n_only`, 19,670 `runtime_n_mixed`, 10,677 `extra_runtime_only`, 7,120 `extra_runtime_mixed`, 59,254 `direct_cross_bucket_ambiguity`, and 2 `no_analysis`. Thus 151,802 / 151,804 undefined rows are withheld by known conservative policy boundaries rather than provider no-analysis.
- Runtime `N` is present in 74,751 undefined rows. Extra-category presence includes ADJ_SHORT 10,126, INFINITIVE 8,230, PARTICIPLE_SHORT 1,100, COLLOC 350 and POSL 0. These are candidate-presence counts, not justified FantLab folds.
- FantLab partition deltas on the unmatched frozen candidate are +16,083 words, -70,685 defined POS words and +86,768 undefined POS words. These cannot be attributed to one morphology rule while source/tokenization identity differs.
- Pinned pylem exposes `homonym_weight`, `word_weight` and `predicted`; its pinned `morph_dict` loads literature homonym statistics by default. This establishes provider-signal provenance only, not FantLab policy/dictionary identity.
- Reviewed M006 evidence covers all 59,254 direct cross-bucket ambiguity rows. Homonym-weight metadata is complete, but only 5,972 rows (10.0786%) have a unique maximum FantLab-shaped bucket; 53,282 tie and 45,832 have all bucket maxima at zero.
- Production homonym selection was not changed. FantLab dictionary identity, homonym selection, noun/cardinal recovery, extra-category folding and service-word aggregation remain unresolved.

### Public repository representation

- The static renderer/publication manifest remain fail-closed and source-free. Public material includes two short Anna Karenina derived showcases, a provenance-only Resurrection page, and a full-work Anna Karenina morphology diagnostic page.
- The full-work morphology page exposes reviewed aggregate values only, identifies the frozen source digest and explicitly preserves `diagnostic_only`, source-match `unknown`, M2 `false` and unchanged production POS semantics.
- Publication contract tests scan provenance artifacts for forbidden source-prose keys; Pages builds are reproducible.
- Live deployment remains disabled behind `SCRIPTORIUM_PAGES_DEPLOY_ENABLED=true` plus repository Pages administration.

## Known risks / blockers

1. FantLab analyzer-input bytes/edition identity remain undisclosed for retained benchmark works; M2 remains 0/5.
2. FantLab corrective coefficients, parser details, exact word-boundary semantics, dash classifier and dialogue grammar/denominators remain partly unpublished.
3. FantLab dictionary/version, homonym-selection/prediction behavior and service-word folding remain unknown.
4. pylem runtime `N` loses noun/cardinal distinction; five extra runtime categories still lack justified FantLab folding.
5. Provider no-analysis is negligible, but known conservative policy boundaries account for nearly all current frozen-work undefined rows; provider homonym weights still do not justify a FantLab selection rule.
6. The exact pinned pylem source requires an isolated legacy toolchain; changing that lane requires new evidence rather than silently patching upstream bytes.
7. Brothers Karamazov now has strong public bibliographic provenance but no frozen full-text identity; the complete text-bearing subpage inventory/extraction/composition must be established before diagnostics.
8. Pages live activation is a repository-admin effect and remains off.

## Run selection rule

On each wake:

1. resolve interrupted/review-ready work or failing required checks before new selection;
2. inspect the exact PR head, checks, comments and artifacts for any recovery unit;
3. otherwise choose the first dependency-satisfied queue row, applying the standing rolling allocation when multiple normal-flow units are eligible;
4. create/search the corresponding issue before implementation;
5. do exactly one bounded unit and update this file plus the relevant changelog/benchmark/provenance record;
6. do not infer parity or unblock M2 from provider executability, diagnostic resemblance, provider-only homonym weights, bibliographic resemblance or excerpt-delivery routes.
