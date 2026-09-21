# SCRIP-CORPUS-050 run receipt

- Unit: `SCRIP-CORPUS-050`
- Issue: #187 (closed completed)
- Pull request: #188 (independently reviewed and squash-merged as `41dd7a750e82a29e1d5f6829aa0d853b881e1373`)
- Base at selection: `master@644a1db54f637222bf603865bd1bde4045ed89c5`
- Branch: `scrip-corpus-050-perelman-1913-provenance`
- Mode: corpus / provenance
- Scope: source-safe provenance lead only; no PDF byte replay, OCR or literary-body construction

## Decision

The P2 corpus/provenance queue asks Scriptorium to strengthen legally usable >=300k candidates while deliberately diversifying beyond nineteenth-century fiction. This run selected Yakov Perelman's 1913 *Занимательная физика. Книга 1* because it adds Russian popular-science/nonfiction and has a concrete public-domain first-edition scan surface.

The evidence supports a provenance lead, not corpus admission:

1. FantLab work `191634` establishes the catalogue identity, title/year/language/work kind. A work-specific linguistic-analysis surface was not independently established, so no `/lp` result or numeric benchmark is recorded.
2. Wikimedia Commons permanent file-description revision `oldid=1045983412` pins the retained bibliographic/legal description for the first 1913 P. P. Soikin edition.
3. Separately, the current Commons file/structured surface observed on 2026-09-21 reports 223 pages, 28,168,847 bytes and SHA-1 `3c616f547ff283a2cafd1ac26b448a8e8013f648` for the current file revision at 2021-09-03 09:12 UTC, whose note says pages 193–194 were added.
4. The oldid is **not** treated as a version pin for Commons structured data or the PDF binary. Those current binary fields remain provider-declared observations. This unit did not independently stream the PDF, so it records no Scriptorium SHA-256 and does not claim that the direct file URL or description revision pins immutable PDF bytes.
5. No OCR/body exists, so the >=300,000-character admission rule is not yet proved for this exact edition.

## Durable artifacts

- `corpus/candidates/perelman-entertaining-physics-book1-1913-ru.md`
- `corpus/candidates/source-edition-traces/perelman-entertaining-physics-book1-1913-ru.json`
- `project/CHANGELOG.d/SCRIP-CORPUS-050.md`
- this receipt
- `project/STATE_AND_QUEUE.md` handoff

No PDF bytes, page images, OCR or literary prose are stored.

## Verification

Verification in this bounded unit is source/contract verification rather than OCR or analyzer execution:

- FantLab's current work page identifies *Занимательная физика. Книга 1* as a Russian-language monograph from 1913;
- Commons' current page resolves its permanent link to `oldid=1045983412`, identifies the 1913 Soikin edition and public-domain status, and reports a current 223-page PDF;
- the same Commons surface reports structured data size 28,168,847 bytes, SHA-1 `3c616f547ff283a2cafd1ac26b448a8e8013f648`, and a 2021-09-03 file-history note that pages 193–194 were added;
- the machine trace separates the pinned description revision from current structured/binary metadata rather than pretending the oldid cryptographically binds those fields;
- all calibration, >=300k, FantLab-source-match, diagnostic and M2 booleans remain false/unknown.

## Independent review and merge

The later independent review re-read exact PR head `734c36c9dab4f9d461ef53c08b1077914d90d42c` against unchanged base `644a1db54f637222bf603865bd1bde4045ed89c5`: 10 commits ahead / 0 behind, five changed files, and no review threads. External Commons/FantLab evidence was rechecked and confirmed the retained conservative boundary.

All 13 pull-request-triggered workflow runs returned for the exact reviewed head settled `success`. `Scriptorium Pages` run `35628918792`, job `106430042698`, checked out the exact reviewed SHA, passed the full 408-test suite, built the canonical static site and passed deterministic rebuild; live Pages deployment remained policy-skipped.

COMMENT review `5270049146` found no merge-blocking issues. PR #188 was marked Ready and squash-merged as `41dd7a750e82a29e1d5f6829aa0d853b881e1373`, automatically closing Issue #187 as completed.

## Gates and handoff

Benchmark movement: none. M2 remains **0/5 source-matched works**.

The Perelman source-safe provenance lead is independently reviewed and complete. A later bounded unit may independently stream/hash the exact Commons original, then define a fail-closed OCR/body contract. It must keep calibration admission closed until the frozen literary body itself proves >=300,000 characters, and must separately prove a real FantLab linguistic-analysis/input identity before any diagnostic or parity claim.
