# SCRIP-CORPUS-035 run receipt

- **Unit:** Darwin/Rachinsky source-free literary-body composition contract
- **Issue:** #157
- **PR:** #158 (Draft; authored this run, not self-approved or merged)
- **Base:** `c885600f528e2883396d58e14f229824c61b0902`
- **Repository:** `drevendev/Scriptorium`
- **Connected identity:** `andy-zen-dev`

## Produced

1. Added a machine-checkable contract over the canonical 418 exact Wikisource Page identities.
2. Selected the 14 numbered rendered routes as the literary dependency surface: 388 Page revisions, ordered by frozen route/Page sequence.
3. Classified 30 frozen dependencies as apparatus: parent-only sequences 8–21 and 423–427 plus `/Указатель` 412–422.
4. Kept source-declared no-text positions 114 and 411 outside the frozen dependency inventory and explicitly represented them as non-dependencies.
5. Added fail-closed tests and a dedicated CI workflow whose durable/uploaded output is contract metadata only.

## Research decision

The existing frozen source graph already labels `/1`–`/14` as introduction/chapter routes spanning displayed print pages 1–387 and `/Указатель` as the alphabetical index over 389–399. Fresh Russian Wikisource inspection on 2026-09-20 additionally showed Page 419 carrying alphabetical-index entries and Pages 425–426 carrying publisher advertising/back matter. That evidence supports selecting numbered routes only and excluding index/parent-only surfaces from author/translator literary-body composition.

## Verification boundary

The implementation is intentionally one gate earlier than literary-body identity. It does **not** freeze a Page-wikitext rendering profile, fetch or persist Page prose, compute body characters/bytes/digests, prove >=300,000 characters, retrieve independent scan bytes, or identify a FantLab analyzer input. `admitted_for_calibration=false`, `fantlab_source_edition_match=unknown`, `diagnostic_ready=false`, `gate_ready=false`, and `m2_parity_admissible=false` remain mandatory.

The PR is left Draft for an independent later exact-head review. CI status and exact final head must be re-read after the final bookkeeping commits before any Ready/merge decision.
