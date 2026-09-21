# SCRIP-CORPUS-050 run receipt

- Unit: `SCRIP-CORPUS-050`
- Issue: #187
- Base at selection: `master@644a1db54f637222bf603865bd1bde4045ed89c5`
- Branch: `scrip-corpus-050-perelman-1913-provenance`
- Mode: corpus / provenance
- Scope: source-safe provenance lead only; no PDF byte replay, OCR or literary-body construction

## Decision

The P2 corpus/provenance queue asks Scriptorium to strengthen legally usable >=300k candidates while deliberately diversifying beyond nineteenth-century fiction. This run selected Yakov Perelman's 1913 *Занимательная физика. Книга 1* because it adds Russian popular-science/nonfiction and has a concrete public-domain first-edition scan surface.

The evidence supports a provenance lead, not corpus admission:

1. FantLab work `191634` establishes the catalogue identity, title/year/language/work kind. A work-specific linguistic-analysis surface was not independently established, so no `/lp` result or numeric benchmark is recorded.
2. Wikimedia Commons permanent file-description revision `oldid=1045983412` identifies the first 1913 P. P. Soikin edition, the author, 223 pages and explicit public-domain status.
3. The retained Commons surface reports 28,168,847 bytes and SHA-1 `3c616f547ff283a2cafd1ac26b448a8e8013f648` for the current file revision at 2021-09-03 09:12 UTC, whose note says pages 193–194 were added.
4. Those binary fields remain provider-declared metadata. This run did not independently stream the PDF, so it records no Scriptorium SHA-256 and does not claim that the direct file URL or the description revision pins immutable PDF bytes.
5. No OCR/body exists, so the >=300,000-character admission rule is not yet proved for this exact edition.

## Durable artifacts

- `corpus/candidates/perelman-entertaining-physics-book1-1913-ru.md`
- `corpus/candidates/source-edition-traces/perelman-entertaining-physics-book1-1913-ru.json`
- `project/CHANGELOG.d/SCRIP-CORPUS-050.md`
- this receipt

No PDF bytes, page images, OCR or literary prose are stored.

## Verification

Verification in this bounded unit is source/contract verification rather than OCR or analyzer execution:

- the machine trace is strict JSON and mirrors the public candidate's closed-gate claims;
- the permanent Commons revision and FantLab catalogue locator are recorded explicitly;
- provider-reported binary metadata is labelled as such rather than promoted to independently replayed identity;
- all calibration, >=300k, FantLab-source-match, diagnostic and M2 booleans remain false/unknown.

Fresh pull-request checks on the final exact head are the next repository verification layer. Because this wake authors the substantive provenance change, the pull request must remain Draft for an independent later review even if CI is green.

## Gates and handoff

Benchmark movement: none. M2 remains **0/5 source-matched works**.

A later bounded unit may independently stream/hash the exact Commons original, then define a fail-closed OCR/body contract. It must keep calibration admission closed until the frozen literary body itself proves >=300,000 characters, and must separately prove a real FantLab linguistic-analysis/input identity before any diagnostic or parity claim.
