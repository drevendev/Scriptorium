# SCRIP-CORPUS-041 — source-free Twelve Chairs gap audit

- Opened Issue #169 and Draft PR #170 to inspect the four non-transcluded scan-index gaps in the retained 1928 *Zemlya i Fabrika* *Twelve Chairs* family without changing the frozen 410-Page dependency inventory.
- Added `scriptorium.twelve_chairs_gap_audit`, standard-library regression coverage, and a hosted exact-revision capture/replay workflow. Exact Page wikitext is read only transiently; persisted evidence contains identity, hashes/counts, conservative body-presence classes, and closed-gate flags only.
- Hosted capture run `35515025304` produced source-free artifact `10606587097` (1,576-byte ZIP, SHA-256 `8171ce8c0dcd6d9f20a117e22cc35d0cee4a04d30b4a24c3d8d9befeaf55daa6`). The capture JSON is 4,670 bytes with SHA-256 `f1ca4fb4b0ac475be548c0b51efc08b7c1acbbdca3484101de128501862386ad`.
- Frozen evidence shows pages 150 (`oldid=5702065`) and 314 (`oldid=5702066`) have nonempty transcluded bodies and therefore remain `nonempty_body_unclassified`; pages 151 (`oldid=5702062`) and 315 (`oldid=5701572`) have `no_transcluded_body` after removing comments and `<noinclude>` regions.
- Reconciled the public candidate page and machine-readable source graphs. No gap page is added to the 410 dependency set, and literary membership for nonempty pages 150/314 remains deliberately unfrozen.
- No Page wikitext, OCR, rendered prose, PDF/image bytes, or literary source text is committed. `literary_body_frozen=false`, `admitted_for_calibration=false`, `fantlab_source_edition_match=unknown`, `diagnostic_ready=false`, and `m2_parity_admissible=false`; benchmark movement is none and M2 remains 0/5.
- Authored work remains Draft and requires a later independent exact-head review before Ready/merge.
