# Private ingestion and readable evidence — 2026-11-09

Owner-requested interactive batch, PR #478, based on master d1e596591ae5adacb7e58734eca9bab653e3cc3d. Newly authored changes remain subject to later fresh acceptance; no merge or live publication is claimed here.

- #476: raw href whitespace/controls and percent syntax are validated before urlsplit/unquote; invalid authorities and empty query/fragment components fail with controlled errors. Encoded spaces, NFC Cyrillic and literal percent names retain single-pass decoding.
- #477: validate original ZIP member names, not only Python's potentially NUL-truncated filename, including unreferenced members.
- Add per-document XML depth 128 / element count 100000 bounds and incremental UTF-8 body accounting, including chapter separators. Keep existing archive/expanded-byte limits and accepted-input extraction profile/receipt identities.
- #480 / partial #283: scoped voice evidence-table foreground fixes specified-color contrast from approximately 1.17:1 to 12.51:1. Explicit focus-visible rings cover scroll regions and source disclosures, including forced colors. Preserve no-JS tables, charts and all measurements.
- Add 19 extraction/real-CLI test methods and three stylesheet/HTML regressions. Existing package CI additionally runs the EPUB tests against the installed wheel outside checkout. Local extraction/accessibility subset: 20 PASS; full canonical/installed results belong to exact-head GitHub CI.
- Document the supported EPUB subset in docs/EPUB_VALIDATION.md. No new dependency, donor code, manuscript text, morphology substitution, corpus admission or parity claim. M2 0/5; M3 remains open.

Drive reconciliation: the Compare003 mean-integrity handoff is already implemented in current compare.py and linked to #279; POS handoff is represented by #287; CORPUS-087 is already marked reconciled to #422. A distinct unimplemented old SCRIP-SITE-008 schema-publication proposal was revalidated against current metrics.py/site_renderer.py and recorded as #479, not confused with the already delivered #271 route.

Runtime boundary: local GitHub clone failed DNS resolution. Chromium navigation to the actual local preview returned net::ERR_BLOCKED_BY_ADMINISTRATOR; no policy bypass was attempted. VISUAL_NOT_VERIFIED and LIVE_VERIFIED=UNVERIFIED remain scoped to browser/publication acceptance (#283/#285), not proof the live site is broken.
