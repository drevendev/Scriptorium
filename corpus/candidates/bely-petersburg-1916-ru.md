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
