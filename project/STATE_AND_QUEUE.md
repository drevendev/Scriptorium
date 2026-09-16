# STATE_AND_QUEUE — Scriptorium

STATE_REVISION: 93
PHASE: M1 — Deterministic FantLab surface
LAST_COMMITTED_RUN_AT: 2026-09-16T04:52:54Z
LAST_RESULT: SCRIP-CORPUS-008 / Issue #85 / PR #86 received an independent later-run review of exact head `35061e829d5b279aa45a29f32ff255516c45961a` with no blocking defect and was squash-merged as `84f4f4cea73a53d8ff01fe45000e6655e9f4cb5a`; Issue #85 closed completed. The merged unit adds Alexander Grin's `Блистающий мир` as a legally usable >=300,000-character diversity candidate with a source-cited 1965 Wikisource transcription family while keeping full-text identity unfrozen, FantLab input identity unknown, diagnostics/gate disabled, and M2 at 0/5.
LAST_VERIFIED_PROGRESS: Independent review confirmed unchanged base `c7da33834dd6df8017bc59d86b39b0d07ea480ab`, 7 commits ahead / 0 behind, exactly five expected corpus/provenance/public-navigation/state files, and no review threads. Fresh evidence reconfirmed FantLab's 18 September 2022 count at 306,240 characters / 43,678 words, Wikisource permanent locator `oldid=4186047`, Pravda 1965 vol. 3 pp. 66–214 provenance, 16+11+7 chapter navigation, sampled chapter-source repetition, RVB's 1921–1923 text-family cross-check, and the legal-use boundary. Exact-head runs `35053939844` (Pages) and `35053939843` (pinned provider) both completed successfully, including the standard-library suite, deterministic Pages rebuild, provider contract, exact hash-pinned `pylem==0.0.18` smoke and frozen Anna sidecar diagnostics.

## Current unit

```text
UNIT_ID:        SCRIP-CORPUS-008
ISSUE:          #85
STATUS:         DONE
PR:             #86
MERGED_COMMIT:  84f4f4cea73a53d8ff01fe45000e6655e9f4cb5a
NEXT_ACTION:    Select the next dependency-satisfied SCRIP-CORPUS continuation unit.
                Prefer another legally usable >=300k diversity candidate or stronger
                independent source-identity evidence for an existing candidate; keep
                translation and edition identity explicit and do not infer FantLab
                input identity from title, bibliography, chapter structure, count
                proximity or public-source freezing.
```

## Current milestone gate

M0 is closed. M1 remains open. General, dialogue, vocabulary and punctuation families are executable inferred candidates. POS has two explicitly separated surfaces: the 17-bucket work-page-compatible `scriptorium-pos-v1` production candidate, and the diagnostic-only full FantLab methodology surface covering five additional source-backed AOT categories while leaving runtime `N` unresolved. Anna Karenina, Resurrection, Brothers Karamazov and Silver Dove have immutable public-source candidates. Petersburg has an explicit but unfrozen 1916 edition lead. Hyperboloid of Engineer Garin has an early-Soviet SF/adventure trace plus a Moscow Goslitizdat 1958 volume-4 textual-family lead classified as 1939-fourth-edition-derived, but not tied directly to the Wikisource/az.lib transcription. `grin-shining-world-ru` adds a 1920s romantic-fantastic candidate with a source-cited 1965 Wikisource transcription family and reviewed work-index locator, but its 34 chapter identities remain unfrozen. No retained work has an independently established FantLab analyzer-input identity, so M2 remains open at **0/5 source-matched works**.

## Queue

Evaluate rows in priority order and skip dependencies that are not executable. Recovery/review-ready work and failing required checks preempt normal selection.

| Priority | Unit | Mode | Deliverable | Gate / dependency |
| --- | --- | --- | --- | --- |
| P2 | SCRIP-CORPUS continuation | corpus / provenance | Add or strengthen legally usable >=300k candidates, prioritizing diversity beyond 19th-century Russian classics when licensing/source identity is strong enough | Preserve translation/edition identity and explicit legal provenance |

## Evidence already established

### FantLab / reproduction boundary

- `fantlab-2022-v1` is the frozen compatibility contract. FantLab publicly documents broad metric families while leaving some coefficients/parser details unpublished.
- Exact integer parity is admissible only with exact source-edition identity, legal basis and immutable digest. Decimal/rate parity additionally requires independently established display-rounding behavior.
- The retained parity seed remains **0/5 source-matched works**. Diagnostic resemblance, bibliographic compatibility and public-source freezing never advance M2 by themselves.

### Frozen Anna Karenina candidate

- FantLab work 270306 reports 1,692,647 characters and 253,275 words on 19 September 2022 but does not disclose analyzer-input edition/bytes.
- Russian Wikisource/FEB replay uses 239 pinned chapter revisions under deterministic extraction/composition.
- Composite identity: 1,705,605 characters; raw/normalized SHA-256 `1dcf2af815f6288099f77a038d873690fb0dc72edf81d2094fd29f3d5a30c205`.
- `fantlab_source_edition_match=unknown`; comparisons remain diagnostic-only and M2-inadmissible.

### Frozen Resurrection candidate

- FantLab work 296603 reports 881,244 characters and 126,457 words; immutable analyzer-input identity is undisclosed.
- 129 Wikisource chapter revisions replay deterministically.
- Composite identity: 890,835 characters; raw/normalized SHA-256 `2725a60a810d8aae4beff9dbc73ff85cf6da066b1c5272aaebf21addbe4ccaa0`.
- The 9,591-character display delta is mismatch/unknown-policy evidence, not source identity.

### Frozen Brothers Karamazov candidate

- FantLab work 168951 reports 1,807,107 characters and 281,507 words on 18 September 2022.
- Wikisource/RVB provenance points to Dostoevsky's 15-volume collected works, Nauka 1991, vols. 9–10. A source-free manifest pins 98 admitted revisions under fail-closed extraction.
- Composite identity: 1,810,351 characters; raw/normalized SHA-256 `26b9991c95b30d262c24ae38fb2332333a58df588a62a4310f9e5c4b507dbce6`.
- The 3,244-character delta and LitRes trial excerpt route do not establish FantLab source identity; diagnostics/M2 remain disabled.

### Frozen Silver Dove modernist candidate

- FantLab work 293515 reports 549,050 characters and 83,369 words on 19 September 2022.
- Wikisource cites Andrei Bely, *Works in two volumes*, Moscow: Khudozhestvennaya literatura, 1990, vol. 1, pp. 377–642; exact revision `5588003` is frozen and replayed.
- Composite identity: 563,125 characters; raw/normalized SHA-256 `496dad8aadaca13f3ce6ef8560b53bcd32c75b5b03f28f13f7735303bb4f7183`.
- FantLab is 14,075 characters lower and the 1909/1910 publication discrepancy remains unresolved; no source match is inferred.

### Traced Petersburg 1916 modernist candidate

- FantLab work 293513 reports 944,182 characters and 130,217 words on 19 September 2022.
- Wikimedia Commons exposes a 632-page public-domain facsimile of the first 1916 book edition, distinct from Bely's materially revised 1922 text.
- PDF bytes/OCR/page extraction are not frozen; FantLab input relation remains unknown. `source_identity_status=traced_not_frozen`, diagnostics/M2 disabled.

### Traced Hyperboloid of Engineer Garin early-Soviet SF candidate

- FantLab work 44824 reports 495,539 characters and 69,126 words on 18 September 2022.
- Wikisource exposes stable revision oldid=5014458 and cites `az.lib.ru`, but does not directly identify the print edition behind the transcription.
- A Moscow Goslitizdat 1958 volume-4 lead is textologically classified through Krestinsky as 1939-fourth-edition-derived; a distinct Kyiv 1958 RSL record proves year-only matching unsafe.
- No direct evidence ties the public transcription, Moscow volume or FantLab analyzer input together. Literary-text digest/extraction remains unfrozen; diagnostics/M2 disabled.

### Traced Shining World 1920s romantic-fantastic candidate

- FantLab work 27340 reports **306,240 characters** and **43,678 words** on 18 September 2022, clearing the corpus threshold by 6,240 characters.
- Russian Wikisource exposes a reviewed/stable work index citing **A. S. Grin, Collected Works in six volumes, Moscow: Pravda, 1965, vol. 3, pp. 66–214 (`lib.web`)**. Permanent revision `oldid=4186047` pins the index only.
- The work is organized as 16 + 11 + 7 = **34 chapter subpages**. Sampled chapter pages repeat the 1965 source citation; Scriptorium does not claim every chapter source line was independently checked in this unit.
- Wikisource identifies Grin as 1880–1932 and lists *Shining World* as a 1923 lifetime publication. Its author rights notice says lifetime-published works are approximately public domain in the source country and separately warns that translations/later revisions may have different rights. Candidate scope is original Russian literary prose only; no source prose/editorial apparatus is committed.
- Russian Virtual Library independently exposes *Shining World* as a 1921–1923 work with the same three-part / 34-chapter structure; this is bibliographic/text-family corroboration only.
- `source_identity_status=traced_not_frozen`, `fantlab_source_edition_match=unknown`, `diagnostic_ready=false`, `gate_ready=false`, and `m2_parity_admissible=false`. A freeze requires all 34 exact chapter revisions, deterministic extraction/composition and raw/normalized composite digests.

### Deterministic metric findings

- Frozen Anna diagnostic deltas include characters +12,958 and words +16,083 relative to FantLab; numeric-token and lexical-hyphen probes explain little of the word gap.
- `scriptorium-punctuation-v2` removes internal ASCII-hyphen double counting, but frozen dash rate still materially exceeds FantLab.
- Dialogue author-remark/denominator semantics remain unresolved: production-v1 author text inside dialogue is 38.3920% versus FantLab 17.02%.
- FantLab dictionary identity remains unknown, so dictionary-dependent vocabulary metrics are unresolved.

### Morphology compatibility

- `pylem==0.0.18` is pinned by exact sdist SHA-256 `66c0d13414006a803f200979540fcee9653738701c14496a418db67542b26515` plus source/dictionary provenance.
- The 17-bucket work-page-compatible production view and the diagnostic 22-category methodology view remain separate. Runtime `N` loses noun/cardinal distinction.
- Five methodology-only source-backed mappings are `POSL -> postposition`, `COLLOC -> phrasal_verb`, `ADJ_SHORT -> short_adjective`, `PARTICIPLE_SHORT -> short_participle`, `INFINITIVE -> infinitive`; their relation to the narrower visible work-page table is unknown.
- Provider replay on frozen Anna defines 127,909 methodology-surface rows versus 117,554 on the conservative work-page-compatible view; this is diagnostic aggregate evidence, not FantLab folding/source-parity evidence.
- Production homonym selection is unchanged. FantLab dictionary identity, homonym selection, noun/cardinal recovery, service-word aggregation and current work-page relation for methodology-only categories remain unresolved.

### Public repository representation

- Static publication remains source-free and fail-closed; publication tests reject forbidden source-prose keys and Pages builds are deterministic.
- Public corpus navigation and parity catalog expose frozen identities for Anna, Resurrection, Brothers Karamazov and Silver Dove, trace-only provenance for Petersburg and Hyperboloid, and the trace-only `grin-shining-world-ru` candidate.
- SCRIP-CORPUS-008 adds the Grin candidate to the machine-readable catalog, a dedicated source-edition trace, and `corpus/candidates/README.md` while explicitly labeling the work-index locator as insufficient to freeze the 34-chapter literary text.
- No derived full-work analysis is published for unmatched trace-only candidates.
- Live Pages deployment remains disabled behind `SCRIPTORIUM_PAGES_DEPLOY_ENABLED=true` plus repository Pages administration.

## Known risks / blockers

1. FantLab analyzer-input bytes/edition identity remain undisclosed for retained benchmark works; M2 remains 0/5.
2. FantLab corrective coefficients, parser details, word-boundary semantics, dash classifier and dialogue grammar/denominators remain partly unpublished.
3. FantLab dictionary/version, homonym selection/prediction and service-word aggregation remain unknown.
4. pylem runtime `N` loses noun/cardinal distinction; methodology-only categories are measured diagnostically but their work-page relationship remains unknown.
5. Exact pinned pylem requires an isolated legacy toolchain; changing that lane requires new evidence.
6. Frozen public-source candidates remain unmatched to FantLab input and therefore cannot advance M2.
7. Petersburg has strong 1916 edition provenance but no frozen PDF/OCR identity and no FantLab source match.
8. Hyperboloid has a stable public revision and a 1939-derived Moscow-1958 textual-family lead, but no frozen literary identity, direct print mapping or FantLab source match; same-year editions are ambiguous.
9. Shining World has a source-cited reviewed work-index locator but its 34 chapter revisions/extraction/composite identity are not frozen and FantLab's input is undisclosed.
10. Pages live activation remains a repository-admin effect and is off.

## Run selection rule

On each wake:

1. resolve interrupted/review-ready work or failing required checks before new selection;
2. inspect the exact PR head, checks, comments and artifacts for any recovery/review unit;
3. otherwise choose the first dependency-satisfied queue row, applying the standing rolling allocation when multiple normal-flow units are eligible;
4. create/search the corresponding issue before implementation;
5. do exactly one bounded unit and update this file plus the relevant changelog/benchmark/provenance record;
6. do not infer parity or unblock M2 from provider executability, diagnostic resemblance, provider weights, methodology-category counts, bibliographic resemblance, public-source freezing, chapter-structure agreement or excerpt-delivery routes.
