# 2026-11-04 — Immutable source replay reliability (PR candidate)

- Share bounded explicit-throttle handling between composite and single-page
  MediaWiki reads (#424), preserving exact requested revisions and caller checks.
- Reject coerced revision IDs and type-confused packed/single-page evidence (#425).
  Five acceptance defects were reproduced on exact master before repair.
- Preserve existing single-page regressions, add 38 offline transport/identity
  tests and document the source-free response/error and total-wait boundaries.
- Reconcile existing Drive handoffs without duplicating implemented POS/White
  Guard/page-ID work or manufacturing content from an empty QA document.
- No source body, corpus measurement, profile, tolerance, license, deployment or
  milestone gate change. M2 0/5. Authored candidate requires later fresh acceptance.
