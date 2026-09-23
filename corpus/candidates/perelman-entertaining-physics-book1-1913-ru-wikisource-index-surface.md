# Perelman 1913 — Russian Wikisource index-surface observation

Candidate: [`perelman-entertaining-physics-book1-1913-ru.md`](perelman-entertaining-physics-book1-1913-ru.md)  
Unit: `SCRIP-CORPUS-071`  
Observation date: `2026-09-23`

## What was checked

Scriptorium re-read the current first-party Wikimedia Commons file surfaces for both already frozen Perelman 1913 carriers:

- PDF: https://commons.wikimedia.org/wiki/File:Перельман_Я.И._Занимательная_физика._Книга_1_(1913).pdf
- DjVu: https://commons.wikimedia.org/wiki/File:Перельман_Я.И._Занимательная_физика._Книга_1_(1913).djvu

The current PDF surface classifies the file under **`PDF files in Russian without index page in Russian Wikisource`**. The current DjVu surface classifies the companion under **`DjVu files in Russian without index page in Russian Wikisource`**.

The machine-readable source-free observation is:

- [`source-edition-traces/perelman-entertaining-physics-book1-1913-ru.wikisource-index-surface.json`](source-edition-traces/perelman-entertaining-physics-book1-1913-ru.wikisource-index-surface.json)
- canonical payload SHA-256: `46803a34fb018f204588f798aca9b928393c37b54518f8adba36b790d6c33d77`

The artifact is bound to the already frozen carrier identities:

- PDF: 223 pages, SHA-256 `3d87d22a42ad949654265e066f81211d7831e32c8b62b96c967cd4cd33e7ed61`
- DjVu: 218 pages, SHA-256 `f1db2166ae0cb5d420aad445f00d90cb09ac0b97e19fc8ece16d9b8ecf9e2462`

## Decision

This closes one tempting but currently unsupported mapping route: Scriptorium must **not assume a current Russian Wikisource ProofreadPage Index/page-label surface exists for either frozen carrier**.

That matters because SCRIP-CORPUS-061 already rejected bibliographic page-count subtraction as a carrier-page selector. A later mapping unit must therefore use one of these evidence-bearing routes:

1. exact-carrier facsimile evidence;
2. exact-carrier internal page-label/structure evidence; or
3. a directly identified first-party Russian Wikisource Index surface if one later exists.

The Commons category observation is deliberately bounded. It does **not** prove that an Index page never existed historically, that one cannot be created later, or that a page mapping can be inferred from the 223/218 carrier counts.

## Unchanged gates

Nothing in this observation:

- proves PDF↔DjVu page equivalence;
- selects literary pages;
- changes the PDF-bound canonical OCR/body carrier;
- verifies OCR correctness;
- freezes a literary body;
- proves the selected-body `>=300,000` rule;
- identifies FantLab analyzer-input bytes or source edition; or
- advances M2.

`fantlab_source_edition_match=unknown`, `diagnostic_ready=false`, `m2_parity_admissible=false`, and M2 remains **0/5**.
