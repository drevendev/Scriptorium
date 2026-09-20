# Andrei Bely — Petersburg (1916 first book edition)

Candidate ID: `bely-petersburg-1916-ru`

This retained candidate is the **1916 first book edition** of Andrei Bely's *Petersburg*, represented by the 632-page Wikimedia Commons facsimile already recorded in Scriptorium's provenance trace. It is deliberately kept distinct from Bely's materially revised **1922** edition.

## Frozen scan identity

**SCRIP-CORPUS-038 / Draft PR #164** independently streamed the exact Commons original without writing the PDF into the repository. The source-free frozen binary identity is:

- byte count: **3,621,459**;
- SHA-1: **`682476934dd6ed49c6bbcdb0720127c1812ff477`**;
- SHA-256: **`b08820ad1339894c6d20fbaa2367c11385492bf376d199f8de23c859ef6ddef5`**.

The hosted capture also established that the previously retained Commons Page Information hash `682476934dd6ed49c6bbcdb0720127c1812ff477` equals the SHA-1 of this exact current PDF byte stream. Scriptorium records that equality as independently verified for this snapshot rather than assuming a general meaning for Commons metadata fields.

No PDF bytes, page images, OCR, or literary source text are committed. The durable receipt stores only the locator, edition identity, byte count, hashes, and closed-gate metadata.

## Rights and edition boundary

The retained Commons file description identifies the facsimile as the first 1916 book publication and marks the work public domain. That source/legal evidence is retained in the structured trace. The candidate is not collapsed with a generic source-less transcription or the revised 1922 Berlin edition.

## What is still open

Freezing the scan binary does **not** freeze the literary text. Scriptorium still needs a candidate-specific fail-closed literary-page/OCR extraction contract, a frozen extracted body with character count and raw/normalized digests, and proof that that frozen body itself clears the **300,000-character** corpus threshold.

FantLab reports 944,182 characters for its 19 September 2022 analysis of work 293513, but it does not disclose the analyzed edition or immutable input bytes. Therefore `fantlab_source_edition_match=unknown`, `diagnostic_ready=false`, `gate_ready=false`, and `m2_parity_admissible=false`. This candidate contributes **0** to the M2 source-matched-work gate.

## Canonical evidence

- [`source-edition-traces/bely-petersburg-1916-ru.json`](source-edition-traces/bely-petersburg-1916-ru.json) — edition/legal provenance, frozen scan identity, and admission/FantLab boundaries.
- [`source-edition-traces/bely-petersburg-1916-ru.scan-identity.json`](source-edition-traces/bely-petersburg-1916-ru.scan-identity.json) — source-free exact PDF byte identity.
- [`../../scriptorium/petersburg_scan_identity.py`](../../scriptorium/petersburg_scan_identity.py) — streaming capture/replay implementation that never persists the PDF.

A later unit may define OCR/extraction only against this exact frozen scan identity; it must not promote corpus or FantLab parity gates until the literary body is independently verified.
