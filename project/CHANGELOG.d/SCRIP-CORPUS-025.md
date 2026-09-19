# SCRIP-CORPUS-025 — Beketova translation revision identity freeze

Date: 2026-09-19
Issue: #137
PR: #138

- Continued the retained `verne-children-captain-grant-beketova-ru` translation candidate rather than adding another trace-only work.
- Added a candidate-specific Actions workflow that uses the existing `scriptorium.single_page_revision` contract to fetch exact Russian Wikisource revision `oldid=5304880` and retain only source-free identity fields.
- Hosted bootstrap run `35419728091`, job `105834985697`, succeeded and produced artifact `10577820530` (`beketova-source-revision`), ZIP SHA-256 `215ab04fa6dd3697ef578a5ecad81e2dd195a12443f787afe45d15a88871fc62`.
- Independent artifact inspection found exactly one source-free JSON file. Its SHA-256 is `b14aa6dc2e8ab712edfb559e9cb825a6b12dc203fbd412b9ecfb9267f5e22740`; no source prose is present.
- Frozen revision identity: page ID `1012777`, revision `5304880`, timestamp `2025-02-25T02:24:10Z`, MediaWiki SHA-1 `256d816de6743031ea86f266ed004ee72240c200`, **1,107,187 wikitext characters**, **2,053,126 UTF-8 bytes**, wikitext SHA-256 `71bfbe889cfc91b7dd24831a6a8984f3ac8d010c90d329b99a8f43aa4e3181a0`.
- Corrected the earlier provenance timestamp from `02:24:00Z` to the exact API-reported `02:24:10Z` and reconciled the public candidate/provenance wording around the frozen revision identity.
- Kept the literary-body boundary fail-closed: the revision-wikitext measurements are not a literary-body character count, no candidate-specific body extractor/digests exist yet, and the work is not admitted for calibration solely from wikitext size.
- Translation identity remains distinct from the French original and other Russian translations. `fantlab_source_edition_match=unknown`, `diagnostic_ready=false`, `gate_ready=false`, `m2_parity_admissible=false`; M2 remains 0/5.
- PR #138 remains Draft for independent later exact-head review and safe merge; this authoring run does not self-approve or merge it.
