# STATE_AND_QUEUE — Scriptorium

STATE_REVISION: 129
PHASE: M1 — Deterministic FantLab surface
LAST_COMMITTED_RUN_AT: 2026-09-17T21:02:00Z
LAST_RESULT: SCRIP-CORPUS-020 / Issue #109 / draft PR #116 authored a bounded source-free parser-control prerequisite for the six frozen `poemx1` calls. Exact semantic head `23b3152f8bf97decdcf95a0021c950682cfd4125` validates the pinned template/transclusion/parameter/binding identities and resolves only branch choices forced by the shared frame (`1` defined empty, `2` defined non-empty, `3/fixed/poem/small/width` omitted): reachable counts are `#if` x4, `#ifeq` x3 and `#tag` x1; both `#expr` calls, the `#iferror` call, one `#if` and two `#ifeq` occurrences are unreachable. The one live unresolved operation is `#tag:poem` with parameter `2`; recursive expansion of that argument, poem-extension rendering, resolved Part 2 bytes, historical render equivalence, literary-body identity and FantLab source equivalence remain explicitly unresolved.
LAST_VERIFIED_PROGRESS: On exact semantic head `23b3152f8bf97decdcf95a0021c950682cfd4125`, workflows `35273911005` (new Klim poemx1 control flow), `35273911132` (invocation bindings), `35273911079` (historical template dependency), `35273911025` (Klim source revisions), `35273911000` (Pages), and `35273911044` (frozen diagnostic) all completed successfully. The dedicated control job checked out that exact head, ran the full standard-library suite, regenerated `gorky-klim-samgin-ru.poemx1-template.control.json` from the committed transclusion/parameter/binding evidence, and byte-compared it to the committed source-free artifact. PR #116 is Draft, mergeable, and has no inline review threads. Current official MediaWiki documentation was re-checked: `#if` treats whitespace-only input as empty, ParserFunctions trim leading/trailing whitespace, non-numeric `#ifeq` operands compare as case-sensitive text, and `#tag` invokes parser/extension tags while unselected conditional paths are not parsed. No FantLab source identity was promoted and M2 remains 0/5.

## Current unit

```text
UNIT_ID:        SCRIP-CORPUS-020
ISSUE:          #109
STATUS:         POEMX1_CONTROL_FLOW_AUTHORED_REVIEW_PENDING
PR:             #116 (draft)
MERGED_COMMIT:  none
NEXT_ACTION:    Independently review exact head of PR #116. If the bounded control-flow evidence remains green and no
                blocking defect is found, merge it without closing Issue #109. The next continuation is then only the one
                live historical expansion path: recursive expansion of parameter 2 as required by #tag:poem plus the
                evidenced poem-extension behavior. Do not manufacture #expr/#iferror implementation work for branches
                proven unreachable under all six frozen calls, and do not claim resolved Part 2 bytes until the live tag
                path replays deterministically. Only then proceed to fail-closed four-part extraction/composition.
```

## Current milestone gate

M0 is closed. M1 remains open. General, dialogue, vocabulary and punctuation metric families are executable inferred candidates. POS has two explicitly separated surfaces: the 17-bucket work-page-compatible `scriptorium-pos-v1` production candidate and a diagnostic-only broader methodology surface with five additional AOT-backed categories while runtime `N` noun/cardinal ambiguity remains unresolved.

No retained work has an independently established FantLab analyzer-input identity, so M2 remains open at **0/5 source-matched works**. Public-source freezing, bibliographic compatibility and diagnostic resemblance do not advance M2.

## Queue

Evaluate rows in priority order. Recovery/review-ready work and failing required checks preempt normal selection.

| Priority | Unit | Mode | Deliverable | Gate / dependency |
| --- | --- | --- | --- | --- |
| P0 | SCRIP-CORPUS-020 / PR #116 | review / provenance | Independently review exact-head poemx1 parser-control evidence; merge only if checks/evidence remain clean, leaving #109 open | Authoring run must not self-approve substantial change |
| P1 | SCRIP-CORPUS-020 continuation | corpus / provenance | Reproduce the one live `#tag:poem` path, including only the recursive parameter-2 expansion and poem-extension behavior required by the frozen calls | Historical template revision remains an inferred as-of anchor; render equivalence must not be guessed; dead `#expr` / `#iferror` paths are not required work |
| P2 | SCRIP-CORPUS continuation | corpus / provenance | Add or strengthen legally usable >=300k candidates, prioritizing diversity beyond 19th-century Russian classics when licensing/source identity is strong enough | Preserve translation/edition identity and explicit legal provenance |

## Retained corpus / provenance status

Detailed evidence lives in `corpus/candidates/`, `benchmarks/`, `project/run-receipts/`, `project/CHANGELOG.md`, and `project/CHANGELOG.d/`; this state file keeps only the orientation-critical summary.

- **Anna Karenina** — frozen public-source candidate: 239 pinned chapter revisions; composite 1,705,605 characters; SHA-256 `1dcf2af815f6288099f77a038d873690fb0dc72edf81d2094fd29f3d5a30c205`; FantLab source match unknown.
- **Resurrection** — frozen public-source candidate: 129 pinned chapter revisions; composite 890,835 characters; SHA-256 `2725a60a810d8aae4beff9dbc73ff85cf6da066b1c5272aaebf21addbe4ccaa0`; FantLab source match unknown.
- **Brothers Karamazov** — frozen public-source candidate: 98 admitted revisions; composite 1,810,351 characters; SHA-256 `26b9991c95b30d262c24ae38fb2332333a58df588a62a4310f9e5c4b507dbce6`; FantLab source match unknown.
- **Silver Dove** — frozen single-revision public-source candidate at `oldid=5588003`; composite 563,125 characters; SHA-256 `496dad8aadaca13f3ce6ef8560b53bcd32c75b5b03f28f13f7735303bb4f7183`; FantLab source match unknown.
- **Petersburg** — first-1916-edition facsimile lead; Commons description revision is pinned but PDF bytes/OCR identity are not; no binary/source match claim.
- **Hyperboloid of Engineer Garin** — frozen single-revision public-source candidate at Russian Wikisource `oldid=5014458`: page ID `1022517`, wikitext SHA-256 `fa0b099bba2d0f0e6ce395a16de76317afcd8bec8b23b52e455f97a9726a4de9`; versioned `scriptorium-hyperboloid-wikisource-body-v1` extraction reproduces 499066 characters / 930560 bytes with raw and normalized SHA-256 `a01c5eadef53b2437eff3abe6052bb7f7bf6f95737641558343363628da7f513`. Direct print-edition identity remains unresolved and FantLab source match is unknown.
- **Shining World** — 1965-source Wikisource family with 34 chapter subpages; chapter identities/composite remain unfrozen.
- **Road to Nowhere** — primary Pravda-1965 source family remains unfrozen. The distinct `az.lib.ru` single-page route at `oldid=5585836` now has replay-frozen revision-wikitext and literary-body identities under `scriptorium-road-nowhere-alt-wikisource-body-v1`: 442,656 characters / 825,899 bytes, raw and normalized SHA-256 `e33a28b8dcdb3ac339147c6587b27c182dd910784122b367db41bc93dfc2dbee`. FantLab displays 438,439 characters; the +4,217 delta is diagnostic-only. Neither route is identified as FantLab input.
- **Running on Waves** — Detskaya literatura 1965 source-cited family with 35 chapters plus epilogue; literary subpage identities/composite remain unfrozen.
- **The White Guard** — Wikisource explicitly mixes two bibliographic source families across chapters 1–11 and 12–20; all 20 chapter identities/composite remain unfrozen.
- **The Twelve Chairs** — keep 40-chapter later 1938/1961 editorial family distinct from 41-chapter 1928 first standalone edition; neither literary body is frozen, and coauthorship prevents individual-author attribution without an explicit VOICE model.
- **The Life of Klim Samgin** — four exact Russian Wikisource parent revisions are replay-frozen at oldids `5733765`, `5198033`, `5138882`, `5724453`; ordered parent revision-wikitext identity SHA-256 `54beabd28d8459bc6a0f1d83187dca56067e337999688d32c809d34340105577`, totaling 3,228,790 parent wikitext characters / 5,902,920 UTF-8 bytes. Part 2's target dependency is replay-frozen at oldid `2366546`, wikitext SHA-256 `173054997b54b96241adc07aeb6f76624beb497f94602452d7f9e4e57b0c6996`; PR #111 froze the exact target-only `#lst` invocation/placement and upstream full-target-template-DOM semantic branch. PR #112 froze the deterministic as-of reconstruction identity for `Шаблон:Poemx1` at oldid `5142743`, wikitext SHA-256 `fa7e35686da5ce4c62986a7e8bfc72f2dba067118218d656b2f0983e5cfa06db`, without claiming historical render equivalence. PR #113 applied documented partial-transclusion controls and froze an effective graph with no ordinary templates or magic words: `#expr` x2, `#if` x5, `#ifeq` x5, `#iferror` x1, `#tag` x1 targeting `poem`. PR #114 froze post-selection input SHA-256 `86ad628a9d8fc3d904fd513a1b4335f4e9f816ceedfa2af736e8e3a94e32ffbf` and the 21-reference literal parameter surface across `1`, `2`, `3`, `fixed`, `poem`, `small`, and `width`. Merged PR #115 source-freezes all six concrete invocation/frame bindings: each call has two anonymous arguments, `1` explicitly empty and `2` non-empty; `3`, `fixed`, `poem`, `small`, and `width` are omitted in every call; no duplicate or out-of-surface binding exists. Draft PR #116 now resolves the control graph forced by that shared frame: reached `#if` x4, `#ifeq` x3 and `#tag` x1; both `#expr` calls and `#iferror` are unreachable, along with one `#if` and two `#ifeq` occurrences. Recursive expansion of parameter `2` and live `#tag:poem` extension rendering remain unresolved. Resolved Part 2 identity, literary extraction/composition and composite digests remain unfrozen. FantLab source identity remains unknown and main parity-catalog admission remains deferred.

## Deterministic / morphology findings

- Frozen Anna diagnostics still show large character/word differences from FantLab; numeric-token and lexical-hyphen probes do not explain the word gap.
- `scriptorium-punctuation-v2` removes internal ASCII-hyphen double counting, but dash-rate parity remains unresolved.
- Dialogue author-remark / denominator semantics remain unresolved.
- FantLab dictionary/version, homonym selection, word-boundary semantics and service-word aggregation remain unknown.
- `pylem==0.0.18` is pinned by exact sdist SHA-256 `66c0d13414006a803f200979540fcee9653738701c14496a418db67542b26515` plus source/dictionary provenance.
- Runtime `N` loses noun/cardinal distinction. Five additional methodology-only AOT categories remain diagnostic and are not silently folded into the work-page-compatible production view.

## Public repository representation

- Static publication remains source-free and deterministic; publication tests reject forbidden source-prose keys.
- Public corpus navigation exposes retained candidates with provenance boundaries rather than parity claims.
- SCRIP-CORPUS-016 upgrades the public Hyperboloid entry to a frozen source-free literary-body identity with exact counts/digests and an explicit fail-closed extraction profile while preserving the unresolved print-edition and FantLab-input boundary.
- The repaired machine-readable candidate catalog agrees with the Hyperboloid trace/body manifests and no longer advertises the candidate as `traced_not_frozen`.
- SCRIP-CORPUS-017 adds the standalone public Klim Samgin candidate page and provenance trace.
- SCRIP-CORPUS-018 strengthens that page/trace with exact per-part revision identities and an ordered revision-set digest while explicitly retaining the body-unfrozen and FantLab-unknown boundary. It intentionally does not change the main parity catalog.
- SCRIP-CORPUS-019 upgrades the Road to Nowhere public entry and provenance trace with a replay-frozen source-free alternate-body identity while explicitly leaving the retained primary Pravda-1965 family and FantLab-input identity unresolved.
- SCRIP-CORPUS-020 first pinned the Klim Part 2 dependency, PR #111 corrected the public explanation to target-only `#lst`, PR #112 exposed the exact source-free `poemx1` as-of anchor, PR #113 exposed the post-inclusion effective dependency boundary, PR #114 exposed the literal parameter surface, merged PR #115 exposed concrete invocation/frame binding, and draft PR #116 now exposes source-free control reachability. The public candidate and trace show that `#expr`/`#iferror` are dead for all six frozen frames and that `#tag:poem` with parameter `2` is the sole live unresolved template operation. Historical render equivalence and Part 2/body identity remain explicit unresolved boundaries.
- Live Pages deployment remains disabled behind `SCRIPTORIUM_PAGES_DEPLOY_ENABLED=true` plus repository Pages administration.

## Known risks / blockers

1. FantLab analyzer-input bytes/edition identity remain undisclosed for retained benchmark works; M2 remains 0/5.
2. FantLab corrective coefficients, parser details, word-boundary semantics, dash classifier and dialogue grammar/denominators remain partly unpublished.
3. FantLab dictionary/version, homonym selection/prediction and service-word aggregation remain unknown.
4. pylem runtime `N` loses noun/cardinal distinction; methodology-only categories are diagnostic until their visible work-page relation is evidenced.
5. Frozen public-source candidates remain unmatched to FantLab input and therefore cannot advance M2.
6. Petersburg lacks a Scriptorium-recorded PDF snapshot digest and deterministic OCR/page-extraction identity.
7. Hyperboloid has a frozen revision and deterministic frozen literary-body identity but no direct bibliographic print-edition identity and no FantLab analyzer-input match; Shining World, Running on Waves, White Guard and Twelve Chairs remain trace-only/unfrozen at the literary-body level.
8. Road to Nowhere now has a frozen alternate revision and deterministic frozen alternate literary-body identity, but the primary Pravda-1965 literary family remains unfrozen and no evidence ties either route to FantLab input.
9. Klim Samgin's parent/dependency revisions, target-only `#lst` semantics, inferred historical `poemx1` revision, inclusion controls, post-selection digest, literal parameter-reference/default surface, six concrete invocation bindings and frozen-frame `#if`/`#ifeq` control reachability are now source-freezeable. Both `#expr` calls and `#iferror` are unreachable for all six frozen frames; the remaining live historical expansion boundary is recursive expansion of parameter `2` plus `#tag:poem` extension behavior. Resolved Part 2 bytes, candidate-specific extraction/composition and composite raw/normalized body digests remain unfrozen; no historical render or FantLab-input identity may be inferred yet.
10. Pages live activation remains a repository-admin effect and is off.
