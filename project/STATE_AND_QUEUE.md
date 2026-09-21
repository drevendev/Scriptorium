# STATE_AND_QUEUE — Scriptorium

STATE_REVISION: 217
PHASE: M1 — Deterministic FantLab surface
LAST_COMMITTED_RUN_AT: 2026-09-21T21:47:00Z
LAST_RESULT: SCRIP-CORPUS-052 / Issue #191 recovery repair in Draft PR #192. Independent settlement of authored head `1d43935ba62f9d175d2bc981ec2284a302ab0289` found required CI failures: Pages run `35654095114` ran 426 tests and Perelman scan run `35654095223` ran 11 focused tests; both failed on the same two stale `tests/test_perelman_provenance_trace.py` assertions after the contract-defined status and next-evidence wording changed. This wake repaired those assertions and strengthened trace-to-contract binding checks for exact contract version/path/SHA-256 and unbound page/rasterization/OCR/body state. Independent diff review also found and corrected a branch-only Road to Nowhere SHA-256 transcription regression. Fresh hosted settlement and a later independent judgement are required before Ready/merge.
LAST_VERIFIED_PROGRESS: Perelman's exact scan identity retains versioned source-free OCR/body promotion contract v1 at canonical SHA-256 `f709f2fd298252c3edaf8eaf04fc53955186d48df1f2c2b24d1962d1729ee7e5`; recovery now keeps its provenance integration tests synchronized with that boundary. No PDF bytes, page images, OCR or source prose are retained. Page selection, renderer/OCR identity, literary-body digests/count, >=300k admission, work-specific FantLab linguistic-analysis/input identity, diagnostic readiness and M2 remain deliberately unverified. M2 remains 0/5.

## Current unit

```text
UNIT_ID:        SCRIP-CORPUS-052
ISSUE:          #191 (open)
STATUS:         REVIEW_PENDING
PR:             #192 (Draft; recovery repair authored in latest wake)
NEXT_ACTION:    Wait for fresh hosted checks on the repaired exact final head to settle, then independently review that
                exact head in a later wake. Do not merge from the repair-authoring wake. If accepted, a later Perelman
                unit may bind exact literary-page selection and reproducible renderer/OCR identities/settings under a
                new contract version, then freeze source-free body counts/digests and evaluate >=300k. Keep
                FantLab/diagnostic/M2 gates closed until separately proved.
```

## Current milestone gate

M0 is closed. M1 remains open. General, dialogue, vocabulary and punctuation metric families are executable inferred candidates. POS has two explicitly separated surfaces: the 17-bucket work-page-compatible `scriptorium-pos-v1` production candidate and a diagnostic-only broader methodology surface with five additional AOT-backed categories while runtime `N` noun/cardinal ambiguity remains unresolved.

No retained work has an independently established FantLab analyzer-input identity, so M2 remains open at **0/5 source-matched works**. Public-source freezing, bibliographic compatibility, count proximity and diagnostic resemblance do not advance M2.

## Queue

Evaluate rows in priority order. Recovery/review-ready work and failing required checks preempt normal selection.

| Priority | Unit | Mode | Deliverable | Gate / dependency |
| --- | --- | --- | --- | --- |
| P1 | SCRIP-CORPUS-052 review/merge recovery | review / corpus provenance | Independently review repaired Draft PR #192 at its exact settled head; verify source-free contract/provenance synchronization, repaired repository-wide tests, public wording and checks, then Ready/merge only if no blocker remains | This row preempts new production while #192 is open; latest wake authored substantive repair and must not self-approve |
| P2 | SCRIP-CORPUS continuation | corpus / provenance | Add or strengthen legally usable >=300k candidates, prioritizing diversity beyond 19th-century Russian classics when licensing/source identity is strong enough; Petersburg's frozen scan and Darwin/Rachinsky's frozen source/surface/scan/profile identities make separate candidate-specific OCR/renderer units executable when selected | Preserve translation/edition identity and explicit legal provenance; renderer/OCR work must keep body/admission/FantLab/M2 gates closed until separately verified |

## Retained corpus / provenance status

Detailed evidence lives in `corpus/candidates/`, `benchmarks/`, `project/run-receipts/`, `project/CHANGELOG.md`, and `project/CHANGELOG.d/`; this file keeps only the orientation-critical summary.

- **Anna Karenina** — 239 pinned chapter revisions; 1,705,605 characters; SHA-256 `1dcf2af815f6288099f77a038d873690fb0dc72edf81d2094fd29f3d5a30c205`; FantLab source match unknown.
- **Resurrection** — 129 pinned chapter revisions; 890,835 characters; SHA-256 `2725a60a810d8aae4beff9dbc73ff85cf6da066b1c5272aaebf21addbe4ccaa0`; FantLab source match unknown.
- **Brothers Karamazov** — 98 admitted revisions; 1,810,351 characters; SHA-256 `26b9991c95b30d262c24ae38fb2333a58df588a62a4310f9e5c4b507dbce6`; FantLab source match unknown.
- **Silver Dove** — single revision `oldid=5588003`; 563,125 characters; SHA-256 `496dad8aadaca13f3ce6ef8560b53bcd32c75b5b03f28f13f7735303bb4f7183`; FantLab source match unknown.
- **Petersburg** — SCRIP-CORPUS-038 complete. Exact 632-page 1916 first-book-edition Commons PDF: 3,621,459 bytes, SHA-1 `682476934dd6ed49c6bbcdb0720127c1812ff477`, SHA-256 `b08820ad1339894c6d20fbaa2367c11385492bf376d199f8de23c859ef6ddef5`; distinct from 1922. OCR/page selection/body/>=300k/FantLab identity remain open.
- **Hyperboloid of Engineer Garin** — `oldid=5014458`; frozen body 499,066 characters / 930,560 bytes; SHA-256 `a01c5eadef53b2437eff3abe6052bb7f7bf6f95737641558343363628da7f513`; print-edition/FantLab identity unresolved.
- **Shining World** — 34 advertised chapter links but only 19 pages exist; complete body unavailable from this route and FantLab match unknown.
- **Road to Nowhere** — primary Pravda-1965/lib.web route remains incomplete; distinct `az.lib.ru` route `oldid=5585836` is 442,656 characters / 825,899 bytes, SHA-256 `e33a28b8dcdb3ac339147c6587b27c182dd910784122b367db41bc93dfc2dbee`; neither is identified as FantLab input.
- **Running on Waves** — SCRIP-CORPUS-028 complete. Detskaya literatura 1965 family: 36 literary pages, 363,819 characters / 656,239 bytes, SHA-256 `41a1ada3caabea2909976372ca6312fb8a478f2d0d87c088f304fcb30c52fdbc`; clears >=300k. FantLab shows 360,987 characters but source match remains unknown. Separate 1980 route stays distinct.
- **The White Guard** — Wikisource mixes two bibliographic source families across chapters 1–11 and 12–20; body remains unfrozen.
- **The Twelve Chairs** — SCRIP-CORPUS-044 complete. 410 exact Page identities and exact Commons PDF (77,978,350 bytes; SHA-1 `4ab6aa42c3517169e99c1177b6fb6412cfe9187d`; SHA-256 `5a82f8101f9c17dfafcf8b45dc9ed5a7cdfa12a3e88d18bd0f0987e4fcd51eb4`) plus fail-closed surface/profile are frozen. 30 template shapes / 602 invocations and 410 `<references/>` remain unresolved; body/>=300k/FantLab identity remain open.
- **The Life of Klim Samgin** — candidate-specific source graph, fail-closed extractor, per-part/composite body identities and provenance are frozen; exact historical MediaWiki/Poem deployment and FantLab input identity remain unresolved.
- **Children of Captain Grant — Beketova translation** — 1,095,467 characters / 2,040,240 bytes; SHA-256 `4931eba535a4ef3989ac905d895258f00db57029e488d98511db50a7ce4d1161`; clears >=300k with explicit source/PD evidence. No FantLab result/input identity for this translation; M2 weight zero.
- **On the Origin of Species — Rachinsky translation** — 418 exact Page identities, 388-literary/30-apparatus composition, exact-388 markup inventory, backing scan identity, render profile SHA-256 `2ebcfea51282505c28824f54f6a1795bd7e87e2f958ac59f5c843e68c2066f3d`, semantic backlog SHA-256 `4ec4f84566f5f3f8dccd1945906d1a782f4532547a13cadc8570cb5b682bdcb2`, and documentation evidence SHA-256 `d92bdfcad71aaa8a50f9f35b5b1ada462ed41619400c40576d0603cf154877dc` are retained. SCRIP-CORPUS-049 is independently reviewed and complete on master with replay contract SHA-256 `35bed756f4fafa4f443315c09d04a35c66441eb2249eced3c7540ac20c981afe`: `expandtemplates.revid` is context, not version pin; exact recursive dependency closure is still empty/unfrozen, and any future complete closure must carry per-node source-free discovery proof whose SHA-256 is recomputed from exact node revision identity plus direct-dependency set and whose child relations exactly match the graph. All 43 semantic shapes remain unresolved, `ё` remains priority 1 at 2,227 calls, and renderer/body/>=300k/FantLab/M2 remain closed.
- **Entertaining Physics, Book 1 — Perelman 1913 first edition** — SCRIP-CORPUS-051 independently froze the current Commons PDF at 28,168,847 bytes, SHA-1 `3c616f547ff283a2cafd1ac26b448a8e8013f648`, SHA-256 `3d87d22a42ad949654265e066f81211d7831e32c8b62b96c967cd4cd33e7ed61`; description `oldid=1045983412` remains bibliographic/legal provenance only. SCRIP-CORPUS-052 defines source-free OCR/body promotion contract v1, SHA-256 `f709f2fd298252c3edaf8eaf04fc53955186d48df1f2c2b24d1962d1729ee7e5`, and its recovery repair synchronizes provenance tests with that contract, but page selection, renderer/OCR bindings, body outputs, >=300k, work-specific FantLab identity and M2 remain open pending later independent review of PR #192.

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
- Beketova and Running on Waves expose >=300k frozen bodies while FantLab/M2 remain closed; Petersburg exposes exact 1916 PDF identity while OCR/body gates remain open.
- The Twelve Chairs exposes exact-surface rendering decisions plus unresolved template/reference counts without claiming renderer/body equivalence.
- The Darwin/Rachinsky semantic-backlog companion now separates documented conditional `{{ё}}` semantics, the oldid/live-transclusion model, and the fail-closed replay contract. It explicitly records that `expandtemplates.revid` is not accepted as a template-version pin, recursive dependency closure is still empty, and future per-node discovery digests are recomputed from exact revision identity plus direct-dependency set before edge agreement can satisfy closure.
- Klim Samgin exposes its source graph, extractor, body identities and structured provenance; FantLab source match remains unknown.
- The Perelman 1913 public candidate exposes the exact scan identity plus source-free OCR/body promotion contract v1. The contract makes the next evidence requirements inspectable while keeping page selection, OCR toolchain, body/>=300k and FantLab gates explicitly unverified; no scan or book text is published.
- Live Pages deployment remains disabled behind `SCRIPTORIUM_PAGES_DEPLOY_ENABLED=true` plus repository Pages administration.

## Known risks / blockers

1. FantLab analyzer-input bytes/edition identity remain undisclosed for retained benchmark works; M2 remains 0/5.
2. FantLab corrective coefficients, parser details, word-boundary semantics, dash classifier and dialogue grammar/denominators remain partly unpublished.
3. FantLab dictionary/version, homonym selection/prediction and service-word aggregation remain unknown.
4. pylem runtime `N` loses noun/cardinal distinction; methodology-only categories remain diagnostic.
5. Frozen public-source candidates remain unmatched to FantLab input and therefore cannot advance M2.
6. Petersburg scan identity is exact but deterministic OCR/body/>=300k admission remains unfrozen.
7. Shining World's primary route is incomplete; Road to Nowhere's primary route is not a complete route witness.
8. Running on Waves clears >=300k but FantLab analyzer-input/source identity remains unknown.
9. Klim Samgin still lacks exact historical MediaWiki-core/Poem deployment equivalence and FantLab input identity.
10. Beketova *Children of Captain Grant* clears >=300k but lacks a matching FantLab linguistic-result/input identity.
11. The 1928 *Twelve Chairs* route still has unresolved template/reference semantics, inter-page composition, body identity and FantLab source identity.
12. Darwin/Rachinsky `{{ё}}` has documented semantics and a corrected live-transclusion model, but exact replay-time recursive dependency identities are not yet bound. `expandtemplates.revid` is only revision context, a single TemplateSandbox override is insufficient to prove closure, and complete closure requires revision-pinned recursive-expansion provenance plus per-node discovery evidence whose digest is bound to exact revision identity and direct-dependency set. Both forced/non-forced replay outputs remain unverified; body/>=300k and FantLab identity remain open.
13. Pages live activation remains a repository-admin effect and is off.
14. Perelman 1913 has an exact independently streamed PDF identity and a fail-closed source-free OCR/body promotion protocol, but the v1 profile is intentionally unbound: exact literary-page selection, reproducible renderer/OCR identities/settings, body outputs, >=300k admission and work-specific FantLab identity remain unverified.
