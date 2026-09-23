# SCRIP-CORPUS-071 — Perelman Russian Wikisource index-surface boundary

- Selected the retained 1913 Perelman popular-science candidate from the P2 corpus/provenance continuation because its next extraction step requires exact page-label/facsimile evidence rather than page-count inference.
- Re-read the current first-party Wikimedia Commons PDF and DjVu file surfaces on 2026-09-23.
- The PDF surface currently classifies the frozen carrier under `PDF files in Russian without index page in Russian Wikisource`; the DjVu surface currently classifies the companion under `DjVu files in Russian without index page in Russian Wikisource`.
- Added source-free machine evidence `perelman-entertaining-physics-book1-1913-ru.wikisource-index-surface.json`, canonical payload SHA-256 `46803a34fb018f204588f798aca9b928393c37b54518f8adba36b790d6c33d77`, bound to the already frozen PDF/DjVu identities.
- Added a public companion explaining the narrow operational decision: Scriptorium must not assume a current Russian Wikisource ProofreadPage Index/page-label authority exists for either carrier.
- The observation is deliberately current-surface-only. It does not prove an Index never existed historically, cannot be created later, or that carrier pages can be mapped by subtracting bibliographic page counts.
- SCRIP-CORPUS-061's rejection of page-count arithmetic remains unchanged. The next mapping evidence must come from exact-carrier facsimile/internal page-label evidence or a directly identified first-party Russian Wikisource Index surface if one later exists.
- PDF↔DjVu equivalence, literary-page selection, canonical extraction carrier, OCR correctness, literary-body freeze, selected-body >=300k proof, FantLab analyzer-input identity, diagnostic readiness and M2 remain closed; M2 stays 0/5.
- Issue #231 / Draft PR #232 carries the authored unit for independent exact-head judgement; merge is deliberately deferred to a later wake.
