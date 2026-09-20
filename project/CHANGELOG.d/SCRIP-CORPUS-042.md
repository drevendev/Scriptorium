# SCRIP-CORPUS-042 — freeze Twelve Chairs gap composition membership

- Opened Issue #171 and Draft PR #172 for one source-free provenance unit on the retained 1928 *Zemlya i Fabrika* *Twelve Chairs* family.
- Added `scriptorium.twelve_chairs_gap_membership` and a frozen `gap-membership.json` decision bound to the exact 410-Page sharded identity manifest plus the reviewed four-gap audit.
- The current Scriptorium composition surface remains exactly the three frozen canonical parent routes: pages 8–149, 152–313 and 316–421, for 410 pinned Page dependencies.
- Gap pages 150, 151, 314 and 315 are all frozen as excluded from that composition surface because none is transcluded by the canonical part routes. Pages 150/314 remain `nonempty_body_unclassified`; their exclusion is explicitly not a semantic claim that printed-page content is non-literary. Pages 151/315 retain `no_transcluded_body`.
- Added deterministic fail-closed regression coverage: the decision rebuilds from committed source-free evidence, rejects gap-audit drift, preserves the unchanged 410 dependency inventory and keeps all body/admission/FantLab/M2 gates closed.
- Reconciled the dedicated public candidate page and machine-readable source graph/edition trace to expose the new membership boundary without claiming a literary-body freeze.
- No Page wikitext, OCR, rendered prose, PDF/image bytes or literary text is committed. Page rendering/extraction, inter-page composition/separators, literary-body counts/digests, Scriptorium-proven >=300k admission, FantLab source identity, diagnostics and M2 parity remain unfrozen/unknown.
- Benchmark movement: none; M2 remains 0/5 source-matched works.
