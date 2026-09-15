# STATE_AND_QUEUE — Scriptorium

STATE_REVISION: 74
PHASE: M1 — Deterministic FantLab surface
LAST_COMMITTED_RUN_AT: 2026-09-15T08:50:20Z
LAST_RESULT: SCRIP-REPRO-009 / Issue #66 / PR #67 received an independent exact-head review with no blocking defect and was squash-merged as `e7913f5f58852683d79c07f19db8ec4d6f4d8f9d`. The merged unit freezes retained >=300k candidate `dostoevsky-brothers-karamazov-ru` at 98 exact Russian Wikisource revisions under versioned fail-closed extraction/composition semantics, while committing only source-free identity metadata and composite hashes. FantLab source-edition match remains unknown, diagnostic comparison remains disabled, M2 parity is inadmissible, and benchmark movement remains 0/5 source-matched works. Issue #66 closed completed.
LAST_VERIFIED_PROGRESS: Independent review of exact head `35163ab1ee3cbe9113357e8161e9fc29146d280a` confirmed the PR was cleanly mergeable against unchanged master, with eight expected files changed and no PR comments, submitted reviews or review threads. Exact-head runs `34947463077` (Brothers Karamazov replay), `34947463185` (Pages), `34947463116` (frozen diagnostic), and `34947463138` (pinned pylem provider) all succeeded. Replay used Python 3.13.15, passed 151/151 standard-library tests, fetched all 98 exact pinned revisions and reproduced the committed 1,810,351-character / 3,261,432-byte composite with raw and `scriptorium-text-v1` normalized SHA-256 `26b9991c95b30d262c24ae38fb2332333a58df588a62a4310f9e5c4b507dbce6`. Independently downloaded artifact `10387807120` contained exactly one source-free replay receipt; its archive SHA-256 matched GitHub at `f9c1ba0c71ccf8029b1de3d1f610b4b78a89c3ca00464323ab8dbfa86bf611af`. The 3,244-character delta from FantLab remains non-identity evidence only.

## Current unit

```text
UNIT_ID:        SCRIP-REPRO-009
ISSUE:          #66
STATUS:         DONE
PR:             #67
MERGED_COMMIT:  e7913f5f58852683d79c07f19db8ec4d6f4d8f9d
NEXT_ACTION:    Select the SCRIP-MORPH continuation as the highest-priority
                dependency-satisfied normal-flow unit. Investigate the next largest
                unresolved morphology axis with inspectable evidence while preserving
                the fail-closed boundaries around runtime N, extra-category folding,
                FantLab homonym selection, dictionary identity and service-word
                aggregation. Do not promote any provider heuristic without benchmark evidence.
```

## Current milestone gate

M0 is closed. M1 remains open. General, dialogue, vocabulary and punctuation families are executable inferred candidates. POS aggregation has a versioned provider-neutral artifact, reviewed exact-pylem frozen-work transport, reviewed source-free undefined-reason decomposition, and reviewed provider-side homonym-weight diagnostics. The repository publishes a reviewed source-free full-work Anna Karenina morphology showcase. Anna Karenina, Resurrection and Brothers Karamazov now each have immutable public-source candidates, but M2 remains open at **0/5 source-matched works** because no retained FantLab analyzer-input edition/byte identity is independently established.

## Queue

Evaluate rows in priority order and skip dependencies that are not executable. Recovery/review-ready work and failing required checks preempt normal selection.

| Priority | Unit | Mode | Deliverable | Gate / dependency |
| --- | --- | --- | --- | --- |
| P1 | SCRIP-MORPH continuation | analyzer core / reproduction | Investigate the next largest unresolved morphology axis with inspectable evidence, without guessing runtime `N`, extra-category folding, FantLab homonym selection, dictionary identity or service-word aggregation | M006 merged; provider homonym-weight signal is diagnostic only |
| P2 | SCRIP-CORPUS continuation | corpus / provenance | Add or strengthen legally usable >=300k candidates, prioritizing diversity beyond 19th-century Russian classics when licensing/source identity is strong enough | Preserve translation identity and explicit legal provenance |

## Evidence already established

### FantLab / reproduction boundary

- `fantlab-2022-v1` is the frozen compatibility contract. FantLab publicly documents broad metric families while leaving some coefficients/parser details unpublished.
- Exact integer parity is admissible only with exact source-edition identity, legal basis and immutable text digest. Decimal/rate parity additionally requires independently established display-rounding behavior.
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
- The exact public-source inventory is now frozen at 98 independently revision-pinned segments: one work-index authorial front matter segment, one author preface, 93 book chapters and three epilogue chapters. Navigation-only book/epilogue wrappers are excluded.
- Source identities are stored compactly as 98 revision IDs, timestamps and MediaWiki SHA-1 values; no source prose is committed. Exact replay must reproduce the same composite identity.
- `scriptorium-wikisource-karamazov-body-v7` handles only source-observed markup shapes: Wikisource editor notes are excluded; level-5/6 literary headings retain visible text; numeric line-start `Indent` inside observed `Poem1` is layout-only; unambiguous three-argument `Опечатка` (`О1`/`О2`/`О3`) emits corrected text; zero-argument `NB` preserves its visible `NB` marker. Broader shapes fail closed.
- Composite identity: 1,810,351 characters; 3,261,432 UTF-8 bytes; raw and `scriptorium-text-v1` normalized SHA-256 `26b9991c95b30d262c24ae38fb2332333a58df588a62a4310f9e5c4b507dbce6`.
- The frozen candidate is 3,244 characters above FantLab's displayed count. This does not establish edition identity or explain the delta; it is an explicit source-mismatch/unknown-policy signal.
- FantLab's current TXT excerpt route redirects to a LitRes trial endpoint (`art=171949`) and remains inadmissible as analyzer-input identity evidence.
- `source_identity_status=public_candidate_frozen`, `fantlab_source_edition_match=unknown`, `diagnostic_ready=false`, `gate_ready=false`, `diagnostic_comparison_admissible=false`, and `m2_parity_admissible=false`.

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
- The reviewed frozen Anna Karenina POS diagnostic contains 269,358 Scriptorium word tokens: 117,554 conservatively defined and 151,804 undefined.
- Reviewed undefined decomposition: 55,081 `runtime_n_only`, 19,670 `runtime_n_mixed`, 10,677 `extra_runtime_only`, 7,120 `extra_runtime_mixed`, 59,254 `direct_cross_bucket_ambiguity`, and 2 `no_analysis`.
- Runtime `N` is present in 74,751 undefined rows. Extra-category presence includes ADJ_SHORT 10,126, INFINITIVE 8,230, PARTICIPLE_SHORT 1,100, COLLOC 350 and POSL 0; these are candidate-presence counts, not justified FantLab folds.
- FantLab partition deltas on the unmatched Anna candidate are +16,083 words, -70,685 defined POS words and +86,768 undefined POS words; source/tokenization mismatch prevents attribution to one morphology rule.
- Pinned pylem exposes `homonym_weight`, `word_weight` and `predicted`; only 5,972 / 59,254 direct cross-bucket ambiguity rows have a unique maximum FantLab-shaped bucket, so provider weights do not justify a FantLab homonym-selection rule.
- Production homonym selection was not changed. FantLab dictionary identity, homonym selection, noun/cardinal recovery, extra-category folding and service-word aggregation remain unresolved.

### Public repository representation

- The static renderer/publication manifest remain fail-closed and source-free. Public material includes two short Anna Karenina derived showcases, a provenance-only Resurrection page, and a full-work Anna Karenina morphology diagnostic page.
- The full-work morphology page exposes reviewed aggregate values only, identifies the frozen source digest and explicitly preserves `diagnostic_only`, source-match `unknown`, M2 `false` and unchanged production POS semantics.
- Corpus navigation now documents the frozen Brothers Karamazov public identity and exact source-free manifest, but no derived full-work analysis is published for it because FantLab source match and diagnostic admissibility remain unresolved.
- Publication contract tests scan provenance artifacts for forbidden source-prose keys; Pages builds are reproducible.
- Live deployment remains disabled behind `SCRIPTORIUM_PAGES_DEPLOY_ENABLED=true` plus repository Pages administration.

## Known risks / blockers

1. FantLab analyzer-input bytes/edition identity remain undisclosed for retained benchmark works; M2 remains 0/5.
2. FantLab corrective coefficients, parser details, exact word-boundary semantics, dash classifier and dialogue grammar/denominators remain partly unpublished.
3. FantLab dictionary/version, homonym-selection/prediction behavior and service-word folding remain unknown.
4. pylem runtime `N` loses noun/cardinal distinction; five extra runtime categories still lack justified FantLab folding.
5. Provider no-analysis is negligible, but known conservative policy boundaries account for nearly all current frozen-work undefined rows; provider homonym weights still do not justify a FantLab selection rule.
6. The exact pinned pylem source requires an isolated legacy toolchain; changing that lane requires new evidence rather than silently patching upstream bytes.
7. Brothers Karamazov now has a frozen public-source identity, but no evidence ties FantLab's uploaded 2022 analyzer input to those same bytes; diagnostic comparison and M2 parity therefore remain disabled.
8. Pages live activation is a repository-admin effect and remains off.

## Run selection rule

On each wake:

1. resolve interrupted/review-ready work or failing required checks before new selection;
2. inspect the exact PR head, checks, comments and artifacts for any recovery unit;
3. otherwise choose the first dependency-satisfied queue row, applying the standing rolling allocation when multiple normal-flow units are eligible;
4. create/search the corresponding issue before implementation;
5. do exactly one bounded unit and update this file plus the relevant changelog/benchmark/provenance record;
6. do not infer parity or unblock M2 from provider executability, diagnostic resemblance, provider-only homonym weights, bibliographic resemblance, public-source freezing or excerpt-delivery routes.
