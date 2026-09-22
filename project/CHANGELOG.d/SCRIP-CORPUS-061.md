# SCRIP-CORPUS-061 — Perelman 1913 pagination evidence

- Froze a source-free bibliographic pagination record for *Entertaining Physics, Book 1* (1913), bound to the already exact 223-page PDF and 218-page DjVu carrier identities.
- Recorded the Russian State Library catalogue collation **`VIII, 211, [1] с.`** separately from the independent Google Books / Google Play Books **212-page** display instead of normalizing those surfaces into a guessed single pagination model.
- Made the resulting engineering decision explicit and machine-validated: page-count arithmetic cannot select literary carrier pages. In particular, `218 - 212 = 6` is not evidence that six DjVu pages are non-literary because neither bibliographic surface maps printed pagination to exact carrier pages.
- Added fail-closed validation, focused regressions and a dedicated read-only PR workflow. Source text, page images and carrier bytes are not retained in the new artifact.
- Kept PDF↔DjVu page equivalence, literary-page selection, canonical extraction carrier, literary-body identity, >=300k admission, FantLab source identity, diagnostics and M2 closed.
- The next candidate-specific evidence step is an exact facsimile/page-label mapping on a deliberately chosen frozen carrier; only then may a later contract version bind literary pages and freeze a body.
