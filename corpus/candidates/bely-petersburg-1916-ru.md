# Andrei Bely — Petersburg (1916 first book edition)

Candidate ID: `bely-petersburg-1916-ru`

This retained candidate is the **1916 first book edition** of Andrei Bely's *Petersburg*, represented by the 632-page Wikimedia Commons facsimile already recorded in Scriptorium's provenance trace. It is deliberately kept distinct from Bely's materially revised **1922** edition.

## Frozen scan identity

**SCRIP-CORPUS-038 / merged PR #164** independently streamed the exact Commons original without writing the PDF into the repository. The source-free frozen binary identity is:

- byte count: **3,621,459**;
- SHA-1: **`682476934dd6ed49c6bbcdb0720127c1812ff477`**;
- SHA-256: **`b08820ad1339894c6d20fbaa2367c11385492bf376d199f8de23c859ef6ddef5`**.

The hosted capture also established that the previously retained Commons Page Information hash `682476934dd6ed49c6bbcdb0720127c1812ff477` equals the SHA-1 of this exact current PDF byte stream. Scriptorium records that equality as independently verified for this snapshot rather than assuming a general meaning for Commons metadata fields.

Independent exact-head review of `11ca95744ce0b28c213d21b2221a6fc1f6d6b831` found all **15/15** pull-request workflows successful. Dedicated run `35498451938`, job `106045731420`, replayed the exact original and reproduced the byte count/SHA-1/SHA-256. Review independently downloaded artifact `10601673060`, recomputed its 1,313-byte ZIP SHA-256 as `1ceb12a969e98e46178c785a956a70c63b4517b16660c1ba99278e6a9f83c0b2`, and confirmed it contains only the committed source-free receipt plus verification JSON. PR #164 was then squash-merged as `fac5aab20f5426e1d3e01853027222c5cd8c04ed`.

No PDF bytes, page images, OCR, or literary source text are committed. The durable receipt stores only the locator, edition identity, byte count, hashes, and closed-gate metadata.

## OCR/body promotion boundary

**SCRIP-CORPUS-056 / Issue #199** defines source-free contract `scriptorium-petersburg-1916-ocr-body-contract-v1`, cryptographically bound to the exact frozen PDF above. Its canonical SHA-256 is **`d338d8dc4d800b0fe28a848e383265ba9a0e720e75962f7f9e5733ad727a20d2`**.

The contract freezes only future composition semantics: ascending PDF-page order, stripping trailing newlines per selected page, joining pages with two LF characters, UTF-8 raw-body encoding, and `scriptorium-text-v1` normalization. Literary-page selection, rasterizer identity/settings, OCR engine/language-data/settings, and raw/normalized body outputs deliberately remain **unbound**. A later extraction profile must use a new independently evidenced contract version rather than silently mutating v1.

## Rights and edition boundary

The retained Commons file description identifies the facsimile as the first 1916 book publication and marks the work public domain. That source/legal evidence is retained in the structured trace. The candidate is not collapsed with a generic source-less transcription or the revised 1922 Berlin edition.

## Extraction-strategy preflight

**SCRIP-CORPUS-087** adds a source-free preflight before choosing direct PDF text extraction versus raster OCR. On 24 September 2026 the official Commons surface still exposed the frozen candidate as a 632-page PDF facsimile of the first 1916 book edition, with the current file history rooted at the 20 March 2016 upload, explicit public-domain notice, PDF format 1.6, and a current-file no-overwrite notice.

Two provider PDF screenshots were inspected directly: the title-page surface at carrier page 1 and a prose surface at carrier page 21, where printed folio 19 is visible. Those previews visibly look like facsimile page imagery, but that fact **does not prove that the PDF lacks a hidden text layer**. Conversely, the provider metadata does not prove that a usable embedded text layer exists.

That historical preflight did not choose an extraction method. On 28 November, merged #666 independently measured all 632 physical pages of the exact PDF using Poppler 24.02.0: zero extracted code points, zero non-whitespace pages. The [accepted receipt](https://github.com/drevendev/Scriptorium/issues/651#issuecomment-7236203713) establishes this tool's extraction outcome, not absence of every possible PDF text representation. Decision: **bounded OCR experiment**.

Canonical source-free evidence: [`source-edition-traces/bely-petersburg-1916-ru.extraction-preflight.json`](source-edition-traces/bely-petersburg-1916-ru.extraction-preflight.json), physical SHA-256 **`093f251cb8d03846a5158a1ac29d4b66e1796a7cc2bc65a77ade3d9e3cebcff1`**.

## Bounded OCR sample (candidate)

The new sample compares Russian Tesseract PSM 3 (automatic layout) and 6 (single block), OEM 1, on grayscale 300 DPI rasters of physical pages 1, 21, 22, 160, 320, 480 and 600. Page 1 is a title control; remaining sampled page scopes require independent classification. The receipt records tool and language-model hashes, raster hashes, OCR counts and inter-mode edit distances, not recognized text. Agreement does not establish accuracy. Private reference input is optional, raster-hash-bound and never uploaded by the workflow. CER/WER numerators and denominators retain historical spelling, case and punctuation after NFC and whitespace collapse; caller-supplied references are not independently verified by the program. References must be full-page transcriptions of the rendered region. Whole-volume OCR remains held until independently scan-checked representative references and layout quality evidence exist.

Local command (requires Poppler, Tesseract and Russian language data):

```sh
python -m scriptorium.petersburg_ocr_sample /private/carrier.pdf --tessdata /usr/share/tesseract-ocr/5/tessdata
```

Optional `--private-references` accepts a private JSON object keyed by physical page number, each value containing `raster_sha256` and `transcription`. Keep this input outside the repository. The v1 body promotion contract remains unchanged.

## Matched-model OCR comparison (candidate)

Merged #667 established a seven-page stock Russian OCR baseline, not scan-checked accuracy. Both stock modes emitted zero pre-reform glyphs. The follow-through holds rasterizer, pages, 300 DPI grayscale, OEM 1 and PSM 6 constant while comparing stock `rus` with [Iskra `orus`](https://github.com/AButon-8/iskra_ocr/tree/02f34dc42af9f78d022848e83e103b182c9af134) (locusclassicus and AButon-8, Apache-2.0; [license](https://github.com/AButon-8/iskra_ocr/blob/02f34dc42af9f78d022848e83e103b182c9af134/LICENSE)). The latter is trained on historical newspaper material, not this novel. The exact model is pinned by byte size and Git blob identity, with SHA-256 calculated on retrieval. Neither model nor scans are committed.

`python -m scriptorium.petersburg_ocr_models /private/carrier.pdf --stock-tessdata /usr/share/tesseract-ocr/5/tessdata --iskra-tessdata /private/iskra`

Optional `--private-references` uses the same full-page raster-bound reference mapping as the previous sample. For independently scan-checked references, the harness reports character/word edit numerators and reference denominators and case-sensitive per-glyph reference and matched counts under a deterministic minimum-edit alignment. Unmatched output counts are not glyph retention. No references available in the hosted replay: accuracy remains NOT_RUN and zero reference occurrences are not inferred. The title control is not a body sample. Representative manual reference collation (including typography, historical letters actually present and page boundaries), layout, literary-body and all admission/parity gates remain open.


## Private region-matched reference evaluation (candidate)

Merged #668 compared seven identical full-page PNG rasters; no scan-checked accuracy
was measured. A short transcription must **not** be compared to a whole-page OCR output.
The separate region harness now makes a lossless grayscale PGM crop from the pinned PDF
at 300 DPI (different encoding from the full-page PNG diagnostic). Both models receive
the exact same crop, OEM 1 and PSM 7 for a single line or PSM 6 for a block. Physical page 1
is strictly a title control. Other sampled page scopes are caller classifications, not
independently established literary-body boundaries.

Private preparation example (coordinates are illustrative, not verified scan positions):

```sh
python -m scriptorium.petersburg_ocr_regions /private/carrier.pdf prepare --page 21 --box 100 200 900 100 --private-crop /private/line.pgm
```

Open the private crop and transcribe **all and only** the visible text independently of
OCR, retaining case, punctuation and pre-reform spelling. Choose complete nonoverlapping
lines or blocks, including difficult typography and historical glyphs; exclude clipped
letters. For evaluation, create a private JSON list from each preparation receipt:
keep `physical_page`, `box`, `page_sha256`, and `crop_sha256`; remove `dpi`; add
`scope` (BODY_LINE, BODY_BLOCK or TITLE_CONTROL) and `transcription`.
Never commit or upload these references/crops. Then run:

```sh
python -m scriptorium.petersburg_ocr_regions /private/carrier.pdf compare --stock-tessdata /usr/share/tesseract-ocr/5/tessdata --iskra-tessdata /private/iskra --private-references /private/regions.json
```

The tool refuses drift in the exact carrier, full PGM or crop bytes before OCR, rejects
invalid/out-of-bounds regions and duplicate region identities, and emits only hashes,
coordinates, segmentation, tool/model identities and aligned error/glyph counts.
It reports each region separately, not a pooled score over potentially overlapping crops.
A zero reference occurrence is not evidence of retention; the caller's transcription
and scope remain unverified by the program. Actual scan-checked reference accuracy is
NOT_RUN until independent manual evidence is available. No admission, body freeze, rights
or FantLab parity gate changes.

## What is still open

Defining the promotion contract does **not** freeze the literary text. Scriptorium still needs an independently evidenced bound contract version with exact literary-page selection and reproducible rasterizer/OCR identities/settings, then a frozen extracted body with character count and raw/normalized digests and proof that that frozen body itself clears the **300,000-character** corpus threshold.

FantLab reports 944,182 characters for its 19 September 2022 analysis of work 293513, but it does not disclose the analyzed edition or immutable input bytes. Therefore `fantlab_source_edition_match=unknown`, `diagnostic_ready=false`, `gate_ready=false`, and `m2_parity_admissible=false`. This candidate contributes **0** to the M2 source-matched-work gate.

## Canonical evidence

- [`source-edition-traces/bely-petersburg-1916-ru.json`](source-edition-traces/bely-petersburg-1916-ru.json) — edition/legal provenance, frozen scan identity, promotion boundary, and admission/FantLab boundaries.
- [`source-edition-traces/bely-petersburg-1916-ru.scan-identity.json`](source-edition-traces/bely-petersburg-1916-ru.scan-identity.json) — source-free exact PDF byte identity.
- [`source-edition-traces/bely-petersburg-1916-ru.ocr-contract.json`](source-edition-traces/bely-petersburg-1916-ru.ocr-contract.json) — source-free fail-closed OCR/body promotion contract v1.
- [`../../scriptorium/petersburg_scan_identity.py`](../../scriptorium/petersburg_scan_identity.py) — streaming capture/replay implementation that never persists the PDF.
- [`../../scriptorium/petersburg_ocr_contract.py`](../../scriptorium/petersburg_ocr_contract.py) — fail-closed contract validator.

A later unit may bind OCR/extraction only in a new independently evidenced contract version; it must not promote corpus or FantLab parity gates until the literary body is independently verified.
