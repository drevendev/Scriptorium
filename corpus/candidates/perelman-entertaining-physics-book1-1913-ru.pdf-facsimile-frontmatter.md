# Perelman 1913 — exact-PDF front-matter facsimile anchors

This companion records a deliberately small set of **directly observed** page anchors from the Wikimedia Commons preview of Scriptorium's already frozen 1913 Soikin PDF carrier. It is source-free: no PDF bytes, page images, OCR output, hidden text or literary prose are stored here.

The carrier identity remains the one independently frozen earlier by Scriptorium: **223 pages**, **28,168,847 bytes**, SHA-1 `3c616f547ff283a2cafd1ac26b448a8e8013f648`, SHA-256 `3d87d22a42ad949654265e066f81211d7831e32c8b62b96c967cd4cd33e7ed61`. On 2026-09-23 the current Commons file surface still reported the same page count, byte count and SHA-1, and identified the current revision as the 3 September 2021 file that added pages 193–194.

## Direct observations

The observations below come from 500-pixel Commons-generated previews. `No label visible` means exactly that: no printed page label was visibly observed in that preview. It is **not** a claim that a higher-resolution scan contains no mark.

| PDF carrier page | Observed surface | Visible printed page label |
| ---: | --- | --- |
| 4 | preface page | no label visible |
| 5 | apparently blank page | no label visible |
| 6 | table of contents | `V` |
| 8 | table of contents | `VII` |
| 9 | front-matter illustration | no label visible |

Canonical machine evidence: [`source-edition-traces/perelman-entertaining-physics-book1-1913-ru.pdf-facsimile-frontmatter.json`](source-edition-traces/perelman-entertaining-physics-book1-1913-ru.pdf-facsimile-frontmatter.json). Its physical SHA-256 is `12bf560c02b66275a30331cf0274a410041ac916ef21c4ff840d0e55524b7ff8`.

## What this changes

Two exact anchor pairs are now retained rather than inferred: **carrier page 6 → printed `V`** and **carrier page 8 → printed `VII`**. The surrounding directly observed surfaces also show that front matter includes an unlabelled-looking preface/blank leaf and a full-page illustration. This is useful evidence for later page mapping, but it is intentionally not promoted into a complete offset rule.

Carrier page 7 is **not** represented in the canonical artifact, and no `VI` mapping is inferred for it. Likewise, the illustration on carrier page 9 is **not** labelled `VIII` by inference, and the numbered-body start is not guessed to be carrier page 10. Missing anchors remain unknown until directly observed and independently reviewed.

## Closed gates

This partial front-matter observation does **not** establish a complete bibliographic-to-carrier mapping, the numbered-body start or end, literary-page selection, PDF↔DjVu page equivalence, a canonical extraction carrier, OCR correctness, a frozen literary body, the `>=300k` rule, FantLab analyzer-input identity, diagnostic readiness, or M2 parity admissibility. M2 remains 0/5.

The next admissible Perelman step is another bounded facsimile unit around the numbered-body transition and tail/end matter, followed by independent review before any full carrier-page selection is bound.
