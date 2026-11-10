# SCRIP-SITE — current deterministic metric publication

- Issue #479, PR #481. Extend the explicit work-showcase renderer contract from historical deterministic v1/v2 to v3/v4 without automatic enrollment of private input or corpus works.
- Pin v3/v4 schema, metric/profile identities, the exact 29 metric IDs, units, definition evidence and compatibility statuses. Reject forged/missing metrics, nonfinite or malformed values, missing dictionary provenance and unbound vocabulary results.
- Run the current v4 analyzer on a synthetic local text within a test-only publication manifest, test a version-labelled structural v3 fixture, preserve historical routes and verify negative cases leave the last valid static build untouched.
- Document versioned publication contract in the renderer guide and keep the canonical queue focused on this independently reviewable slice. Never claim source-matched FantLab parity or automatic manuscript publication.
- Acceptance pending: exact final-head full CI, deterministic Pages build, installed-wheel checks and later-run merge. Browser live-route/visual acceptance is separately tracked in #283/#285. M2 remains 0/5.
