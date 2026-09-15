# SCRIP-CORPUS-003 — freeze the Silver Dove public candidate

- Issue: #75
- PR: #76
- Scope: corpus / provenance; no FantLab parity promotion.
- Added the source-specific, fail-closed `scriptorium-wikisource-silver-dove-body-v1` extractor for Russian Wikisource full-work revision `5588003` of *Серебряный голубь*. The contract strips the leading page/bibliographic scaffold, empty level-three layout markup, the trailing Wikisource editorial publication note and category links while preserving the authorial preface and literary headings. Unsupported remaining templates/markup continue to fail closed through the shared Wikisource renderer.
- Captured the exact public revision at `2025-07-30T21:54:23Z`: MediaWiki SHA-1 `629893aa2acaa55979114a8bfc2a8882fd43f2a8`, wikitext SHA-256 `a611080e4dd1295336c3d8c7c78fc7a077608b247c9e96d7ae0a989fc256381a`. No source prose is committed.
- The frozen public candidate contains 563,125 characters including spaces / 1,039,363 UTF-8 bytes. Raw and `scriptorium-text-v1` normalized SHA-256 are both `496dad8aadaca13f3ce6ef8560b53bcd32c75b5b03f28f13f7735303bb4f7183`.
- FantLab displays 549,050 characters, a 14,075-character delta. This is recorded as evidence of non-identity or differing extraction/counting policy, not as a normalization target or source-match proof.
- The committed manifest keeps `fantlab_source_edition_match=unknown`, `diagnostic_comparison_admissible=false`, and `m2_parity_admissible=false`; the 1909/1910 publication-date discrepancy remains unresolved.
- Added a dedicated exact-revision replay workflow. The successful capture/replay run `34992478190` executed 162 standard-library tests, reproduced the pinned source-free identity, and uploaded only a short-lived source-free manifest/receipt artifact (`10405159628`, archive SHA-256 `5793d1eb213e30a082bf24c632d9167a29f67f1e1b8c3b1c98cdecdbd2991e81`). The workflow is then tightened to replay the committed manifest rather than recapture mutable current state.
- Public corpus navigation and the machine-readable parity catalog now expose the frozen source identity while explicitly keeping diagnostics and M2 closed.
