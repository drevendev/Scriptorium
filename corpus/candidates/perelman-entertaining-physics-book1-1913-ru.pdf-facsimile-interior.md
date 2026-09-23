# Perelman 1913 — exact-PDF restored-page interior audit

This companion records a bounded, source-free visual audit of Scriptorium's frozen 1913 Soikin PDF around the pages that the current Commons file history says were added on 3 September 2021: printed pages **193–194**. Before rendering, the workflow reverified the carrier as **223 pages**, **28,168,847 bytes**, SHA-1 `3c616f547ff283a2cafd1ac26b448a8e8013f648`, SHA-256 `3d87d22a42ad949654265e066f81211d7831e32c8b62b96c967cd4cd33e7ed61`.

No PDF or rendered page-image bytes are committed. Authoring workflow run `35918820460` checked out the authored branch, downloaded and hash-verified the exact PDF, rendered only carrier pages 199–206 for this interior audit with `pdftoppm` at 120 dpi, deleted the PDF, and uploaded the review images as a one-day transient artifact `10775613969`. The independently downloaded artifact ZIP had SHA-256 `d543e7cc0374a8d89d7a820df6fd525438121da38270e62a084d1f8882bbfebd`; its retained render manifest has SHA-256 `ad09df0a7583092dc2ddf71af25c0f0d014cf5dfe680d806a2962a9243cef667`.

Canonical machine evidence: [`source-edition-traces/perelman-entertaining-physics-book1-1913-ru.pdf-facsimile-interior.json`](source-edition-traces/perelman-entertaining-physics-book1-1913-ru.pdf-facsimile-interior.json). Its physical SHA-256 is `b19be5e8b3fe83546dd65a73770b91f71124b13c709de8142ead29cb78fbc319`.

## Direct observations

Only printed page labels directly visible in the transient exact-carrier renders are retained.

| PDF carrier page | Visible printed page label | Note |
| ---: | ---: | --- |
| 199 | `190` | numbered body surface |
| 200 | `191` | numbered body surface |
| 201 | `192` | numbered body surface |
| 202 | `193` | restored-page region |
| 203 | `194` | restored-page region |
| 204 | `195` | numbered body surface |
| 205 | `196` | numbered body surface |
| 206 | `197` | numbered body surface |

The targeted seam is therefore directly observed as continuous across carrier pages **202–203 → printed pages 193–194**, with the bounded audited window **199–206 → 190–197**. Inside this window, `carrier_page - printed_page = 9` for every directly inspected page.

## What this changes — and what it does not

This resolves the narrow restoration-seam question: the current exact PDF places the restored printed pages 193–194 in a locally continuous numbered sequence rather than introducing an observed numbering discontinuity in the audited window.

It does **not** establish a global `+9` rule for every unobserved interior page. Scriptorium retains `global_carrier_minus_printed_offset_asserted=false`, `bibliographic_to_carrier_mapping_complete=false`, `complete_numbered_body_range_proved=false`, and `mapping_may_be_extrapolated_between_observed_anchors=false`. The earlier direct endpoint anchors and this interior window are compatible, but compatibility is not substituted for evidence over unobserved pages.

## Closed gates

No canonical extraction carrier is selected, no PDF↔DjVu page equivalence is claimed, OCR correctness is unverified, no literary-page selection or body is frozen, the selected-body `>=300k` rule is unproved, and FantLab analyzer-input identity remains unknown. `diagnostic_ready=false`, `m2_parity_admissible=false`, and M2 remains 0/5.

A later independent review should inspect the exact-head transient artifact and the retained source-free evidence. If accepted, further mapping work should continue with additional bounded direct anchors or a separately justified complete-map proof rather than interpolating the remaining unobserved interior.
