# STATE_AND_QUEUE — Scriptorium

STATE_REVISION: 79
PHASE: M1 — Deterministic FantLab surface
LAST_COMMITTED_RUN_AT: 2026-09-15T13:58:32Z
LAST_RESULT: SCRIP-CORPUS-002 / Issue #73 / PR #74 authored a source-free corpus/provenance slice for Andrei Bely's `Серебряный голубь` as the first retained candidate deliberately chosen to diversify the seed beyond nineteenth-century Russian classics. FantLab work 293515 reports a 19 September 2022 linguistic analysis at 549,050 characters / 83,369 words. Russian Wikisource explicitly marks the complete one-page work public domain in Russia, cites Bely's 1990 two-volume collected edition (vol. 1, pp. 377–642), credits V. Esaulov's 2006 electronic version, and exposes permanent full-work revision `oldid=5588003`. The candidate remains `traced_not_frozen`: no extraction/hash freeze or FantLab source identity is claimed, the FantLab 1910 versus Wikisource 1909 publication-year discrepancy remains unresolved, and M2 remains 0/5 source-matched works.
LAST_VERIFIED_PROGRESS: Fresh source research verified FantLab's published threshold count and analysis date, the Wikisource public-domain notice and bibliographic source citation, and the permanent one-page revision boundary. The authored repository changes add `bely-silver-dove-ru` to the candidate catalog, add `corpus/candidates/source-edition-traces/bely-silver-dove-ru.json`, document the candidate in corpus navigation, and record the unit in `project/CHANGELOG.d/SCRIP-CORPUS-002.md`. PR #74 was opened from unchanged master `66f904e33fe094b416de577ce4c803dffaef563c`; this authoring run does not independently judge or merge its own substantive provenance change. Exact-head checks/review remain the next action.

## Current unit

```text
UNIT_ID:        SCRIP-CORPUS-002
ISSUE:          #73
STATUS:         REVIEW
PR:             #74
HEAD_BRANCH:    scrip-corpus-002-bely-silver-dove
NEXT_ACTION:    Independently review the exact current head of PR #74. Re-check the
                FantLab threshold/date, Wikisource legal/bibliographic/permanent-revision
                evidence, JSON/catalog integrity, changed-file boundary and any hosted
                checks. Merge only if the source-match claims remain fail-closed; then
                close Issue #73 completed and record review evidence. Do not treat the
                permanent public revision as a frozen analyzer input without an explicit
                extraction/hash replay.
```

## Current milestone gate

M0 is closed. M1 remains open. General, dialogue, vocabulary and punctuation families are executable inferred candidates. POS has two explicitly separated surfaces: the 17-bucket work-page-compatible `scriptorium-pos-v1` production candidate, and the diagnostic-only full FantLab methodology surface covering the five additional source-backed AOT categories while leaving runtime `N` unresolved. SCRIP-MORPH-008 now has independently reviewed and merged provider-executed frozen Anna aggregate evidence for the latter surface and exposes only those source-free aggregate values in the public morphology showcase; this does not establish how the five categories relate to the current FantLab work-page table. Anna Karenina, Resurrection and Brothers Karamazov each have immutable public-source candidates. Silver Dove adds a legally usable >=300k early-twentieth-century modernist candidate with a permanent single-page public revision but is not yet extraction/hash-frozen. M2 remains open at **0/5 source-matched works** because no retained FantLab analyzer-input edition/byte identity is independently established.

## Queue

Evaluate rows in priority order and skip dependencies that are not executable. Recovery/review-ready work and failing required checks preempt normal selection.

| Priority | Unit | Mode | Deliverable | Gate / dependency |
| --- | --- | --- | --- | --- |
| P2 | SCRIP-CORPUS continuation | corpus / provenance | Add or strengthen legally usable >=300k candidates, prioritizing diversity beyond 19th-century Russian classics when licensing/source identity is strong enough | Preserve translation identity and explicit legal provenance |

## Evidence already established

### FantLab / reproduction boundary

- `fantlab-2022-v1` is the frozen compatibility contract. FantLab publicly documents broad metric families while leaving some coefficients/parser details unpublished.
- Exact integer parity is admissible only with exact source-edition identity, legal basis and immutable digest. Decimal/rate parity additionally requires independently established display-rounding behavior.
- The retained parity seed remains **0/5 source-matched works**. Diagnostic resemblance and public-source freezing never advance M2 by themselves.

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

### Frozen Brothers Karamazov candidate

- FantLab work 168951 reports its 18 September 2022 analysis at 1,807,107 characters and 281,507 words but does not disclose analyzer-input edition/bytes.
- Russian Wikisource identifies its transcription source as Dostoevsky, *Collected Works in 15 volumes*, Leningrad: Nauka, 1991, volumes 9-10 and links the Russian Virtual Library electronic edition; RVB independently confirms parts I-III in volume 9 and part IV plus epilogue in volume 10.
- The exact public-source inventory is frozen at 98 independently revision-pinned segments: one work-index authorial front matter segment, one author preface, 93 book chapters and three epilogue chapters. Navigation-only book/epilogue wrappers are excluded.
- Source identities are stored compactly as 98 revision IDs, timestamps and MediaWiki SHA-1 values; no source prose is committed. Exact replay must reproduce the same composite identity.
- `scriptorium-wikisource-karamazov-body-v7` handles only source-observed markup shapes: Wikisource editor notes are excluded; level-5/6 literary headings retain visible text; numeric line-start `Indent` inside observed `Poem1` is layout-only; unambiguous three-argument `Опечатка` (`О1`/`О2`/`О3`) emits corrected text; zero-argument `NB` preserves its visible `NB` marker. Broader shapes fail closed.
- Composite identity: 1,810,351 characters; 3,261,432 UTF-8 bytes; raw and `scriptorium-text-v1` normalized SHA-256 `26b9991c95b30d262c24ae38fb2332333a58df588a62a4310f9e5c4b507dbce6`.
- The frozen candidate is 3,244 characters above FantLab's displayed count. This does not establish edition identity or explain the delta; it is an explicit source-mismatch/unknown-policy signal.
- FantLab's current TXT excerpt route redirects to a LitRes trial endpoint (`art=171949`) and remains inadmissible as analyzer-input identity evidence.
- `source_identity_status=public_candidate_frozen`, `fantlab_source_edition_match=unknown`, `diagnostic_ready=false`, `gate_ready=false`, `diagnostic_comparison_admissible=false`, and `m2_parity_admissible=false`.

### Silver Dove modernist candidate

- FantLab work 293515 reports its 19 September 2022 linguistic analysis at 549,050 characters and 83,369 words, clearing the >=300,000-character corpus threshold.
- Russian Wikisource publishes the complete work on one page, explicitly marks the literary work public domain in Russia, cites Andrei Bely, *Works in two volumes*, Moscow: Khudozhestvennaya literatura, 1990, volume 1, pp. 377–642, and credits V. Esaulov's electronic version dated 19 August 2006.
- The complete public page has permanent revision `oldid=5588003` (30 July 2025 21:54). That revision identity is durable provenance but is not yet a Scriptorium frozen text candidate because no versioned extraction contract/raw-normalized hash replay has been committed.
- FantLab labels the work a 1910 novel while the current Wikisource metadata says publication 1909. The discrepancy remains explicitly unresolved; Scriptorium does not infer serial-versus-book chronology or source identity from it.
- `source_identity_status=traced_not_frozen`, `fantlab_source_edition_match=unknown`, `diagnostic_ready=false`, `gate_ready=false`, and `m2_parity_admissible=false`.

### Deterministic metric findings

- Frozen Anna Karenina diagnostic deltas include characters +12,958 and words +16,083 relative to FantLab; simple numeric-token and lexical-hyphen probes explain little of the word gap.
- `scriptorium-punctuation-v2` removes internal ASCII-hyphen double counting, but the frozen dash rate still materially exceeds FantLab.
- Dialogue author-remark/denominator semantics remain unresolved: production-v1 author text inside dialogue is 38.3920% versus FantLab 17.02%, and tested sensitivity variants do not establish parity.
- FantLab dictionary identity is unknown, so dictionary-dependent vocabulary metrics remain unresolved.

### Morphology compatibility

- `pylem==0.0.18` is pinned by exact sdist SHA-256 `66c0d13414006a803f200979540fcee9653738701c14496a418db67542b26515` plus pinned source/dictionary provenance.
- Fifteen runtime strings map directly to the observed 17-bucket work-page surface as inferred candidates. Runtime `N` collapses noun/cardinal and stays unresolved.
- FantLab article 374 separately documents the full 22-category POS methodology. The five additional categories map directly at the pinned AOT runtime boundary as `POSL -> postposition`, `COLLOC -> phrasal_verb`, `ADJ_SHORT -> short_adjective`, `PARTICIPLE_SHORT -> short_participle`, and `INFINITIVE -> infinitive`.
- The relation between those five documented methodology categories and the narrower current work-page presentation is **unknown**. Scriptorium must not infer a fold merely from their absence in the visible table.
- `scriptorium-pos-v1` remains unchanged: it resolves a token only when all supplied analyses map to the same direct observed work-page bucket. Empty analyses, `N`, methodology-only categories, unknown codes and cross-bucket homonyms remain undefined there.
- `scriptorium-fantlab-methodology-pos-diagnostic-v1` is a separate diagnostic-only view. It may resolve the five source-backed methodology categories when candidate analyses unanimously map to one methodology bucket, while runtime `N` and cross-category homonyms remain undefined.
- Exact pylem 0.0.18 executability is verified in the isolated Ubuntu 22.04 / Python 3.9 lane; the modern Scriptorium contract suite remains on Ubuntu 24.04 / Python 3.13.
- The reviewed frozen Anna Karenina POS diagnostic contains 269,358 Scriptorium word tokens: 117,554 conservatively defined and 151,804 undefined on the 17-bucket work-page surface.
- Reviewed undefined decomposition: 55,081 `runtime_n_only`, 19,670 `runtime_n_mixed`, 10,677 `extra_runtime_only`, 7,120 `extra_runtime_mixed`, 59,254 `direct_cross_bucket_ambiguity`, and 2 `no_analysis`.
- Runtime `N` is present in 74,751 undefined rows. Methodology-only candidate presence includes ADJ_SHORT 10,126, INFINITIVE 8,230, PARTICIPLE_SHORT 1,100, COLLOC 350 and POSL 0; these are candidate-presence counts, not current work-page folds.
- SCRIP-MORPH-008 provider replay defines 127,909 rows on the documented methodology surface and leaves 141,449 undefined, adding exactly 10,355 resolved rows over the 117,554-defined work-page-compatible view. The direct extra-category counts are infinitive 7,607, short adjective 1,874, short participle 718, phrasal verb/collocation 156 and postposition 0. These are diagnostic counts from the frozen public candidate and pinned provider, not evidence of FantLab work-page folding or source parity.
- The methodology aggregate is bound to runtime-analysis SHA-256 `00cb365eeb6e187362cb1cb54acc6718c230791df18013702907dfee6446d69d`, so the published counts cannot silently refer to a different runtime-candidate matrix under the same text identity.
- FantLab partition deltas on the unmatched Anna candidate are +16,083 words, -70,685 defined POS words and +86,768 undefined POS words; source/tokenization mismatch prevents attribution to one morphology rule.
- Pinned pylem exposes `homonym_weight`, `word_weight` and `predicted`; only 5,972 / 59,254 direct cross-bucket ambiguity rows have a unique maximum FantLab-shaped bucket, so provider weights do not justify a FantLab homonym-selection rule.
- Production homonym selection was not changed. FantLab dictionary identity, homonym selection, noun/cardinal recovery, current work-page relation for methodology-only categories and service-word aggregation remain unresolved.

### Public repository representation

- The static renderer/publication manifest remain fail-closed and source-free. Public material includes two short Anna Karenina derived showcases, a provenance-only Resurrection page, and a full-work Anna Karenina morphology diagnostic page.
- The full-work morphology page exposes reviewed M005/M006 aggregates plus the independently reviewed SCRIP-MORPH-008 aggregate-only 22-category methodology diagnostic, identifies the frozen source digest and explicitly preserves `diagnostic_only`, source-match `unknown`, M2 `false`, unresolved work-page relation and unchanged production POS semantics.
- The methodology public slice exposes only aggregate counts and runtime-analysis identity; it publishes no source prose, normalized text, tokens or candidate rows.
- Corpus navigation documents the frozen Brothers Karamazov public identity and exact source-free manifest plus the new traced Silver Dove modernist candidate. No derived full-work analysis is published for either unmatched candidate.
- Publication contract tests scan provenance artifacts for forbidden source-prose keys; Pages builds are reproducible.
- Live deployment remains disabled behind `SCRIPTORIUM_PAGES_DEPLOY_ENABLED=true` plus repository Pages administration.

## Known risks / blockers

1. FantLab analyzer-input bytes/edition identity remain undisclosed for retained benchmark works; M2 remains 0/5.
2. FantLab corrective coefficients, parser details, exact word-boundary semantics, dash classifier and dialogue grammar/denominators remain partly unpublished.
3. FantLab dictionary/version, homonym-selection/prediction behavior and service-word aggregation remain unknown.
4. pylem runtime `N` loses noun/cardinal distinction; the five additional methodology categories are source-backed and now measured diagnostically on frozen Anna, but their relation to the current 17-bucket work-page presentation remains unknown.
5. Provider no-analysis is negligible, but known conservative policy boundaries account for nearly all current frozen-work undefined rows; provider homonym weights still do not justify a FantLab selection rule.
6. The exact pinned pylem source requires an isolated legacy toolchain; changing that lane requires new evidence rather than silently patching upstream bytes.
7. Brothers Karamazov has a frozen public-source identity, but no evidence ties FantLab's uploaded 2022 analyzer input to those same bytes; diagnostic comparison and M2 parity therefore remain disabled.
8. Silver Dove has strong legal/bibliographic provenance and a permanent single-page revision, but still requires a versioned extraction/hash freeze and independent FantLab analyzer-input provenance before diagnostics or M2 evidence can be admitted; the 1909/1910 publication metadata discrepancy remains unresolved.
9. Pages live activation is a repository-admin effect and remains off.

## Run selection rule

On each wake:

1. resolve interrupted/review-ready work or failing required checks before new selection;
2. inspect the exact PR head, checks, comments and artifacts for any recovery unit;
3. otherwise choose the first dependency-satisfied queue row, applying the standing rolling allocation when multiple normal-flow units are eligible;
4. create/search the corresponding issue before implementation;
5. do exactly one bounded unit and update this file plus the relevant changelog/benchmark/provenance record;
6. do not infer parity or unblock M2 from provider executability, diagnostic resemblance, provider-only homonym weights, methodology-category identity/counts, bibliographic resemblance, public-source freezing or excerpt-delivery routes.
