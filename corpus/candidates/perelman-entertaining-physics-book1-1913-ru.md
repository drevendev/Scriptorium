# Yakov Perelman — Entertaining Physics, Book 1 (1913 first edition)

Candidate ID: `perelman-entertaining-physics-book1-1913-ru`

This retained provenance lead adds **early-20th-century Russian popular science** to Scriptorium's corpus research. FantLab catalogues Yakov Perelman's *Занимательная физика. Книга 1* as work `191634`, a Russian-language monograph first published in 1913. This record keeps that catalogue identity separate from source-byte and linguistic-analysis identity: no work-specific FantLab analyzer input has been established.

## Frozen public source surface

The retained bibliographic/legal source is Wikimedia Commons file-description revision **`oldid=1045983412`** for `Перельман Я.И. Занимательная физика. Книга 1 (1913).pdf`. Its description identifies the edition as **Занимательная физика. Кн. 1. СПб., Изд-во П. П. Сойкина, 1913**, names Yakov Isidorovich Perelman (1882–1942), and carries the public-domain licensing surface.

The Commons current file-history revision is **3 September 2021, 09:12 UTC** and notes that pages **193–194 were added**. The current file surface reports **223 pages**, **28,168,847 bytes**, and SHA-1 **`3c616f547ff283a2cafd1ac26b448a8e8013f648`**.

SCRIP-CORPUS-051 independently streamed that exact current Commons original in hosted CI without persisting the PDF. The streamed bytes reproduced the provider-reported byte count and SHA-1 and established the Scriptorium byte identity:

- exact byte count: **28,168,847 bytes**;
- SHA-1: **`3c616f547ff283a2cafd1ac26b448a8e8013f648`**;
- SHA-256: **`3d87d22a42ad949654265e066f81211d7831e32c8b62b96c967cd4cd33e7ed61`**.

The source-free receipt is [`source-edition-traces/perelman-entertaining-physics-book1-1913-ru.scan-identity.json`](source-edition-traces/perelman-entertaining-physics-book1-1913-ru.scan-identity.json). Ordinary PR verification re-streams the original and fails closed if any byte changes.

## Identity boundary

The permanent Commons `oldid` pins only the file-description revision and its bibliographic/legal assertions; it is not treated as a binary version pin. Conversely, the scan receipt freezes the bytes independently observed from the exact original URL. The direct `upload.wikimedia.org` locator is a retrieval locator, not itself immutable identity: the frozen byte count and digests are the durable identity.

This is a **scan-binary freeze, not an OCR or literary-body freeze**. No PDF bytes, page images, OCR or literary source text are stored in this repository or uploaded as evidence. No page-selection/OCR profile, raw or normalized literary body, character count or body digest has been frozen. Therefore the exact edition has **not yet proved the >=300,000-character calibration rule from a Scriptorium body**.

## OCR/body promotion boundary

SCRIP-CORPUS-052 defines a source-free, versioned promotion contract bound to the exact frozen scan: [`source-edition-traces/perelman-entertaining-physics-book1-1913-ru.ocr-contract.json`](source-edition-traces/perelman-entertaining-physics-book1-1913-ru.ocr-contract.json). Its canonical SHA-256 is **`f709f2fd298252c3edaf8eaf04fc53955186d48df1f2c2b24d1962d1729ee7e5`**.

The v1 contract deliberately remains **unbound** for literary-page selection, rasterizer identity/settings, OCR engine/language-data identity/settings, and all body outputs. It does freeze the future composition policy: selected PDF pages must be ordered by ascending PDF page number, trailing newlines are stripped per page, pages are joined with two LF characters, raw output is UTF-8, and normalization uses `scriptorium-text-v1`. The validator rejects scan-identity drift, shape drift, invented page/toolchain bindings, source-text payload keys, non-null body outputs, and premature >=300k/calibration/FantLab/M2 promotion. A real bound extraction profile must therefore arrive as a new independently evidenced contract version rather than mutating v1 in place.

## FantLab boundary

FantLab work `191634` confirms catalogue identity and the 1913 work date only. A work-specific linguistic-analysis artifact and its analyzer-input edition/bytes remain unestablished. `fantlab_source_edition_match=unknown`, `diagnostic_ready=false`, and `m2_parity_admissible=false`.

## What is still open

The next candidate-specific evidence step is to establish exact literary-page selection and reproducible renderer/OCR toolchain identities over the frozen PDF, then freeze source-free raw/normalized body counts and digests under a new contract version. Only that frozen literary body can prove or reject the >=300,000-character rule. Any later FantLab comparison must independently establish a real work-specific linguistic-analysis surface and analyzer-input/source-edition identity.

## Canonical evidence

- [`source-edition-traces/perelman-entertaining-physics-book1-1913-ru.json`](source-edition-traces/perelman-entertaining-physics-book1-1913-ru.json) — source/legal/catalogue provenance and closed-gate machine record.
- [`source-edition-traces/perelman-entertaining-physics-book1-1913-ru.scan-identity.json`](source-edition-traces/perelman-entertaining-physics-book1-1913-ru.scan-identity.json) — exact current PDF byte identity and closed-gate receipt.
- [`source-edition-traces/perelman-entertaining-physics-book1-1913-ru.ocr-contract.json`](source-edition-traces/perelman-entertaining-physics-book1-1913-ru.ocr-contract.json) — source-free fail-closed OCR/body promotion contract; page selection and OCR toolchain remain unbound.
- [`../../scriptorium/perelman_scan_identity.py`](../../scriptorium/perelman_scan_identity.py) — transient streaming capture/replay implementation.
- [`../../scriptorium/perelman_ocr_contract.py`](../../scriptorium/perelman_ocr_contract.py) — contract validator and canonical digest implementation.
- Wikimedia Commons permanent description revision: `https://commons.wikimedia.org/w/index.php?title=File:Перельман_Я.И._Занимательная_физика._Книга_1_(1913).pdf&oldid=1045983412`.
- FantLab catalogue work: `https://fantlab.ru/work191634`.
