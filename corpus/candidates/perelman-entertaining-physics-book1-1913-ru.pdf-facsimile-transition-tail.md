# Perelman 1913 — exact-PDF numbered-body transition and tail anchors

This companion records a bounded, source-free visual inspection of transient renders from Scriptorium's already frozen 1913 Soikin PDF carrier. The PDF identity was reverified before rendering: **223 pages**, **28,168,847 bytes**, SHA-1 `3c616f547ff283a2cafd1ac26b448a8e8013f648`, SHA-256 `3d87d22a42ad949654265e066f81211d7831e32c8b62b96c967cd4cd33e7ed61`.

No PDF or rendered page-image bytes are committed. Authoring workflow run `35905965911` checked out the exact authored head, downloaded and hash-verified the PDF, rendered only carrier pages 9–13 and 217–223 with `pdftoppm` 24.02.0 at 120 dpi, deleted the PDF, and uploaded the JPEGs as a one-day review artifact. The repository retains only source-free observations and digests.

Canonical machine evidence: [`source-edition-traces/perelman-entertaining-physics-book1-1913-ru.pdf-facsimile-transition-tail.json`](source-edition-traces/perelman-entertaining-physics-book1-1913-ru.pdf-facsimile-transition-tail.json). Its physical SHA-256 is `d518b8f3a00511cf3b7c0199923705c0df9339004be0d759198a5f72cb5a79e5`.

## Direct observations

Only labels visible in the transient exact-carrier renders are retained. `No printed label visible` is an observation about the rendered page, not an inference about neighbouring pages.

| PDF carrier page | Directly observed surface | Visible printed page label |
| ---: | --- | ---: |
| 9 | front-matter illustration | no printed label visible |
| 10 | Chapter I, numbered-body start | `1` |
| 11 | numbered body text | `2` |
| 12 | numbered body text with diagrams | `3` |
| 13 | numbered body text with diagram | `4` |
| 217 | numbered body text with figure | `208` |
| 218 | numbered body text with figure | `209` |
| 219 | numbered body text | `210` |
| 220 | numbered body text | `211` |
| 221 | unnumbered concluding body text with an end ornament | no printed label visible |
| 222 | publisher advertisement | no printed label visible |
| 223 | publisher advertisement | no printed page label visible |

Carrier page 223 also has a handwritten or stamped `30356` above the advertisement. It is explicitly **not** treated as a printed page label.

## What this changes

The numbered-body transition is now directly anchored: carrier page **10 → printed page 1**, preceded by the observed front-matter illustration on carrier page 9. The terminal numbered sequence is also directly anchored: carrier pages **217–220 → printed pages 208–211**. Carrier page 221 visibly continues body text without a printed page number and ends with an ornament; carrier pages 222–223 are publisher advertisements.

This is stronger evidence than page-count arithmetic and it advances two narrow mapping facts: `body_start_carrier_page_proved=true` at page 10 and `numbered_body_end_carrier_page_proved=true` at page 220.

It still does **not** establish a complete carrier map. The observed endpoints happen to be compatible with a simple one-page offset over the numbered body, but Scriptorium does not promote that compatibility into an asserted rule for the unobserved interior. In particular, the exact PDF's 2021 history says printed pages 193–194 were added later, so an internal-anchor audit around that region is a useful next check before binding a complete literary-page selection.

## Closed gates

The complete bibliographic-to-carrier mapping remains open. No canonical extraction carrier is selected, no PDF↔DjVu page equivalence is claimed, OCR correctness is unverified, no literary body is frozen, the selected-body `>=300k` rule is unproved, and FantLab analyzer-input identity remains unknown. `diagnostic_ready=false`, `m2_parity_admissible=false`, and M2 remains 0/5.

A later unit may independently review the exact-head transient renders and then audit bounded interior anchors—especially around the later-added printed pages 193–194—before any complete range or extraction contract is bound.
