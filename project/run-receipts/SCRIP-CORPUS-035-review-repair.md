# SCRIP-CORPUS-035 review-repair receipt

- **Issue:** #157
- **PR:** #158 (Draft)
- **Reviewed blocked head:** `b0e943c2c8efaa2a7ff4a7766a07061ca3f7c9c7`
- **Repository:** `drevendev/Scriptorium`
- **Connected identity:** `andy-zen-dev`

## Blocker recovered

Independent review found that the implementation/public candidate/state/changelog surfaces had advanced to the 388-literary / 30-apparatus composition contract, while the canonical structured provenance trace still claimed that the composition decision was unfrozen and told the next worker to define that contract again.

This recovery unit reconciles the structured trace with the already-authored contract and adds regression coverage. The trace now freezes only the selection/partition boundary:

- 418 exact Page dependencies remain identity-frozen;
- 388 dependencies from rendered numbered routes `/1`–`/14` are selected as literary inputs;
- 30 frozen dependencies are classified as apparatus;
- source-declared no-text 114 and 411 remain explicit non-dependencies.

## Gates deliberately unchanged

The recovery does **not** freeze Page-wikitext-to-prose rendering, separator/body-rendering semantics, literary-body count/digests, the >=300,000-character threshold, independent DjVu SHA-256, or FantLab analyzer-input identity. `admitted_for_calibration=false`, `fantlab.source_edition_match=unknown`, `diagnostic_ready=false`, `gate_ready=false`, and `m2_parity_admissible=false` remain required.

## Handoff

Because this run authored the repair, PR #158 remains Draft and is not self-approved or merged. The next recovery run must re-read the new exact head, verify the structured-provenance regression test and all exact-head CI, then independently decide whether to mark Ready and merge.
