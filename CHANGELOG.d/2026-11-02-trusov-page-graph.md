# Trusov 1775: fail-closed historical Page dependency resolver

- Added a source-free, deterministic capture/replay CLI for the `oldid=5041937` Trusov first-volume ProofreadPage dependencies.
- Validates pinned parent oldid, provider SHA-1, UTF-8 SHA-256 and exact wikitext size against the accepted 2026-11-01 inventory.
- Requires one explicit bounded index/from/to selector, rejects ambiguous markup and missing/duplicate or newer-than-anchor Page revisions. After live CI revealed MediaWiki's multi-title `rvstart` restriction, batch current identities and resolve any post-anchor Page revisions by individual historical queries.
- Uses 2023-09-03T17:55:09Z as an **inferred** as-of-save reconstruction anchor; no historical render-cache equivalence, literary-body identity, size threshold, 29-field analysis or FantLab parity is claimed.
- Added six local positive/negative regressions, scoped real-source CI and a source-free artifact path; live CI capture still needs verification.
