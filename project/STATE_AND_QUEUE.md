# STATE_AND_QUEUE — Scriptorium

STATE_REVISION: 234
PHASE: M1 — Deterministic FantLab surface
LAST_COMMITTED_RUN_AT: 2026-09-22T14:50:27Z
LAST_RESULT: SCRIP-CORPUS-060 / Issue #207 completed. Independent exact-head review `5279744953` re-read PR #208 at `ba0a03d1a7ddf9ee4ce712a0b486645605e90eb4` against unchanged `master@eea64f4f58af5f3bd30c31a55eacc2f30bf32243`, reviewed all 8 changed files, found no merge blocker or open review thread, and confirmed all 21 PR-triggered workflow runs settled `success`. PR #208 was marked Ready and squash-merged with expected-head protection as `00d3600c4f122a01d887677bd0da3ee5304bbebe`, closing Issue #207 completed.
LAST_VERIFIED_PROGRESS: The Perelman 1913 exact DjVu now canonically has both aggregate hidden-text evidence and an independently reviewed ordered source-free per-page count/digest map. The 218 records sum to 583,825 UTF-8 bytes / 326,992 Unicode characters and are bound by ordered record-set SHA-256 `c7981219680bd549c58f69f12a66d393a23e457c526c3140e1da915f023c3246`. This remains page-level provenance only: no literary-page selection has been made, the canonical OCR/body contract remains PDF-bound, and literary-body identity, >=300k admission, FantLab source identity and M2 remain closed.

## Current unit

```text
UNIT_ID:        SCRIP-CORPUS-060
ISSUE:          #207 (closed completed)
STATUS:         COMPLETE
PR:             #208 (independently reviewed; squash-merged as 00d3600c4f122a01d887677bd0da3ee5304bbebe)
NEXT_ACTION:    Resume normal-flow selection from the queue. Perelman now has an independently reviewed exact
                source-free page map, but any literary-body promotion still requires a separate evidence-bearing
                unit that justifies exact literary pages and binds the chosen carrier/extraction profile under a
                new contract version.
```

## Current milestone gate

M0 is closed. M1 remains open. General, dialogue, vocabulary and punctuation metric families are executable inferred candidates. POS has two explicitly separated surfaces: the 17-bucket work-page-compatible `scriptorium-pos-v1` production candidate and a diagnostic-only broader methodology surface with five additional AOT-backed categories while runtime `N` noun/cardinal ambiguity remains unresolved.

No retained work has an independently established FantLab analyzer-input identity, so M2 remains open at **0/5 source-matched works**. Public-source freezing, bibliographic compatibility, all-page OCR/text-layer counts, page maps, count proximity and diagnostic resemblance do not advance M2.

## Queue

Evaluate rows in priority order. Recovery/review-ready work and failing required checks preempt normal selection.

| Priority | Unit | Mode | Deliverable | Gate / dependency |
| --- | --- | --- | --- | --- |
| P2 | SCRIP-CORPUS continuation | corpus / provenance | Add or strengthen legally usable >=300k candidates, prioritizing diversity beyond 19th-century Russian classics when licensing/source identity is strong enough; Petersburg, Perelman and Darwin/Rachinsky have candidate-specific extraction/renderer work available | Preserve translation/edition identity and explicit legal provenance; renderer/OCR work must keep body/admission/FantLab/M2 gates closed until separately verified |

## Retained corpus / provenance status

Detailed evidence lives in `corpus/candidates/`, `benchmarks/`, `project/run-receipts/`, `project/CHANGELOG.md`, and `project/CHANGELOG.d/`; this file keeps only orientation-critical summaries.

- **Anna Karenina** — 239 pinned chapter revisions; 1,705,605 characters; SHA-256 `1dcf2af815f6288099f77a038d873690fb0dc72edf81d2094fd29f3d5a30c205`; FantLab source match unknown.
- **Resurrection** — 129 pinned chapter revisions; 890,835 characters; SHA-256 `2725a60a810d8aae4beff9dbc73ff85cf6da066b1c5272aaebf21addbe4ccaa0`; FantLab source match unknown.
- **Brothers Karamazov** — 98 admitted revisions; 1,810,351 characters; SHA-256 `26b9991c95b30d262c24ae38fb2333a58df588a62a4310f9e5c4b507dbce6`; FantLab source match unknown.
- **Silver Dove** — single revision `oldid=5588003`; 563,125 characters; SHA-256 `496dad8aadaca13f3ce6ef8560b53bcd32c75b5b03f28f13f7735303bb4f7183`; FantLab source match unknown.
- **Petersburg** — exact 632-page 1916 first-book-edition Commons PDF frozen at 3,621,459 bytes / SHA-256 `b08820ad1339894c6d20fbaa2367c11385492bf376d199f8de23c859ef6ddef5`; independently reviewed OCR/body promotion contract v1 SHA-256 `d338d8dc4d800b0fe28a848e383265ba9a0e720e75962f7f9e5733ad727a20d2`; literary-page selection, renderer/OCR bindings, body outputs, >=300k admission and FantLab identity remain open.
- **Hyperboloid of Engineer Garin** — `oldid=5014458`; frozen body 499,066 characters / 930,560 bytes; SHA-256 `a01c5eadef53b2437eff3abe6052bb7f7bf6f95737641558343363628da7f513`; print-edition/FantLab identity unresolved.
- **Aelita** — FantLab work 44822's 18 September 2022 input is 276,556 characters, 23,444 below the standing >=300k floor, so it cannot be an M2 seed. The materially revised public Wikisource source remains separately unmeasured; M2 weight zero.
- **We** — FantLab work 20055's 17 September 2022 input is 285,704 characters, 14,296 below the standing >=300k floor, so it cannot be an M2 seed. The public-domain Wikisource body is split across 40 record pages and remains unfrozen; M2 weight zero.
- **Shining World** — 34 advertised chapter links but only 19 pages exist; complete body unavailable from this route and FantLab match unknown.
- **Road to Nowhere** — primary Pravda-1965/lib.web route remains incomplete; distinct `az.lib.ru` route `oldid=5585836` is 442,656 characters / 825,899 bytes, SHA-256 `e33a28b8dcdb3ac339147c6587b27c182dd910784122b367db41bc93dfc2dbee`; neither is identified as FantLab input.
- **Running on Waves** — 36 literary pages frozen at 363,819 characters / SHA-256 `41a1ada3caabea2909976372ca6312fb8a478f2d0d87c088f304fcb30c52fdbc`. Source-free 27-row deterministic and dialogue-policy diagnostics are independently reviewed. Current-v1 author remarks are 34.563165459722235% of dialogue non-whitespace but 12.4046723291002% of total non-whitespace, only 0.08532767089980098 pp below FantLab's displayed 12.49%; this remains a denominator hypothesis, not parity. FantLab source identity remains unknown.
- **The White Guard** — Wikisource mixes two bibliographic source families across chapters 1–11 and 12–20; body remains unfrozen.
- **The Twelve Chairs** — 410 exact Page identities and exact Commons PDF (77,978,350 bytes; SHA-256 `5a82f8101f9c17dfafcf8b45dc9ed5a7cdfa12a3e88d18bd0f0987e4fcd51eb4`) plus fail-closed surface/profile are frozen. 30 template shapes / 602 invocations and 410 `<references/>` remain unresolved; body/>=300k/FantLab identity remain open.
- **The Life of Klim Samgin** — candidate-specific source graph, fail-closed extractor, per-part/composite body identities and provenance are frozen; exact historical MediaWiki-core/Poem deployment and FantLab input identity remain unresolved.
- **Children of Captain Grant — Beketova translation** — 1,095,467 characters / 2,040,240 bytes; SHA-256 `4931eba535a4ef3989ac905d895258f00db57029e488d98511db50a7ce4d1161`; clears >=300k with explicit source/PD evidence. No FantLab result/input identity for this translation; M2 weight zero.
- **On the Origin of Species — Rachinsky translation** — 418 exact Page identities, 388-literary/30-apparatus composition, exact-388 markup inventory, backing scan identity, render profile and semantic/replay contracts are retained. Exact recursive dependency closure is still empty/unfrozen; all 43 semantic shapes remain unresolved, `ё` remains priority 1 at 2,227 calls, and renderer/body/>=300k/FantLab/M2 remain closed.
- **Entertaining Physics, Book 1 — Perelman 1913 first edition** — exact PDF frozen at 28,168,847 bytes / SHA-256 `3d87d22a42ad949654265e066f81211d7831e32c8b62b96c967cd4cd33e7ed61`; OCR/body promotion contract v1 SHA-256 `f709f2fd298252c3edaf8eaf04fc53955186d48df1f2c2b24d1962d1729ee7e5` remains bound to the PDF. Exact DjVu companion frozen at 2,982,171 bytes / SHA-256 `f1db2166ae0cb5d420aad445f00d90cb09ac0b97e19fc8ece16d9b8ecf9e2462`. Its pinned `djvutxt` hidden-text layer is 583,825 UTF-8 bytes / 326,992 characters over 218/218 pages, raw/normalized SHA-256 `4c9235a78b40ea4737ec4463c1e772727cb31198509d05a24472e8d9075319b8`. SCRIP-CORPUS-060 adds an independently reviewed ordered 218-record source-free page count/digest map with record-set SHA-256 `c7981219680bd549c58f69f12a66d393a23e457c526c3140e1da915f023c3246`. Literary pages are still unselected; PDF↔DjVu equivalence, OCR correctness, canonical carrier, selected body/>=300k, work-specific FantLab identity and M2 remain open.

## Deterministic / morphology findings

- Frozen Anna diagnostics still show large character/word differences from FantLab; numeric-token and lexical-hyphen probes do not explain the word gap.
- Running on Waves has frozen-body full-work and independently reviewed exact-body dialogue-policy diagnostics. Word count is +2,793 vs FantLab display and dash frequency is +10.03235110617089 per 1,000 words. The dialogue probe sharply raises total-text denominator semantics as a follow-up hypothesis while remaining source-unmatched non-parity evidence.
- `scriptorium-punctuation-v2` removes internal ASCII-hyphen double counting, but dash-rate parity remains unresolved.
- Dialogue author-remark / denominator semantics remain unresolved; SCRIP-CORPUS-058 does not alter production semantics.
- FantLab dictionary/version, homonym selection, word-boundary semantics and service-word aggregation remain unknown.
- `pylem==0.0.18` is pinned by exact sdist SHA-256 `66c0d13414006a803f200979540fcee9653738701c14496a418db67542b26515` plus source/dictionary provenance.
- Runtime `N` loses noun/cardinal distinction. Five additional methodology-only AOT categories remain diagnostic and are not silently folded into the work-page-compatible production view.

## Public repository representation

- Static publication remains source-free and deterministic; publication tests reject forbidden source-prose keys.
- Public corpus navigation exposes retained candidates with provenance boundaries rather than parity claims.
- Running on Waves exposes both the source-free exact-body 27-row deterministic diagnostic and a source-free dialogue-policy sensitivity artifact with explicit hypothesis labeling.
- `corpus/candidates/screenings/` exposes source-free pre-admission decisions for Aelita and Zamyatin's *We* without collapsing distinct public-source identities.
- Beketova and Running on Waves expose >=300k frozen bodies while FantLab/M2 remain closed; Petersburg exposes exact 1916 scan identity plus a fail-closed OCR/body promotion contract.
- The Twelve Chairs exposes exact-surface rendering decisions plus unresolved template/reference counts without claiming renderer/body equivalence.
- Darwin/Rachinsky exposes source graph/render/replay contracts while recursive template closure and body admission remain explicitly open.
- Klim Samgin exposes its source graph, extractor, body identities and structured provenance; FantLab source match remains unknown.
- The Perelman 1913 candidate now canonically exposes exact source-free PDF/DjVu carrier identities, its unchanged PDF-bound OCR/body promotion contract, an all-pages hidden-text diagnostic, and an independently reviewed 218-record source-free page count/digest map. Visitors can inspect page-level extraction evidence without source prose while literary-page selection, body/>=300k and FantLab gates remain explicitly closed.
- Live Pages deployment remains disabled behind `SCRIPTORIUM_PAGES_DEPLOY_ENABLED=true` plus repository Pages administration.

## Known risks / blockers

1. FantLab analyzer-input bytes/edition identity remain undisclosed for retained benchmark works; M2 remains 0/5.
2. FantLab corrective coefficients, parser details, word-boundary semantics, dash classifier and dialogue grammar/denominators remain partly unpublished.
3. FantLab dictionary/version, homonym selection/prediction and service-word aggregation remain unknown.
4. pylem runtime `N` loses noun/cardinal distinction; methodology-only categories remain diagnostic.
5. Frozen public-source candidates remain unmatched to FantLab input and therefore cannot advance M2.
6. Petersburg scan identity and a fail-closed source-free promotion contract are exact, but literary-page selection, reproducible renderer/OCR bindings, frozen body and >=300k admission remain open.
7. Shining World's primary route is incomplete; Road to Nowhere's primary route is not a complete route witness.
8. Running on Waves clears >=300k and has exact-body deterministic plus dialogue-policy diagnostics, but FantLab analyzer-input/source identity remains unknown; the near denominator match cannot select production semantics by itself.
9. Klim Samgin still lacks exact historical MediaWiki-core/Poem deployment equivalence and FantLab input identity.
10. Beketova *Children of Captain Grant* clears >=300k but lacks a matching FantLab linguistic-result/input identity.
11. The 1928 *Twelve Chairs* route still has unresolved template/reference semantics, inter-page composition, body identity and FantLab source identity.
12. Darwin/Rachinsky `{{ё}}` has documented semantics and a corrected live-transclusion model, but exact replay-time recursive dependency identities are not yet bound; body/>=300k and FantLab identity remain open.
13. Pages live activation remains a repository-admin effect and is off.
14. Perelman 1913 now has exact PDF/DjVu identities, reproducible hidden-text evidence and an independently reviewed source-free 218-page count/digest map. The map makes later page selection reviewable but does not select literary pages, prove PDF↔DjVu equivalence/OCR correctness, change the PDF-bound canonical contract carrier, freeze a literary body, prove selected-body >=300k, establish work-specific FantLab identity or advance M2.
15. Zamyatin *We* has a useful public-domain source-family lead, but the work-index revision does not freeze the 40 linked body pages and FantLab work 20055 is permanently below the current M2 size floor.
