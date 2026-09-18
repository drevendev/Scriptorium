# Run receipt — SCRIP-CORPUS-020 literary-body identity review

Date: 2026-09-18
Issue: #109
Reviewed PR: #127
Reviewed head: `1e32c4592afccf9290552b5daeb15a4d9c21933f`
Merged commit: `7bf0dd79bde5e9df76a4b96ebe56f4792c49e23e`

## Selection

Recovery/review-ready work preempted normal queue selection. Draft PR #127 was the current P0 continuation named by `project/STATE_AND_QUEUE.md`.

## Independent review evidence

- PR #127 was 6 commits ahead / 0 behind `master` and mergeable.
- No submitted reviews or inline review threads existed before this review.
- All 13 pull-request workflows associated with exact head `1e32c4592afccf9290552b5daeb15a4d9c21933f` completed successfully.
- Dedicated literary-body workflow run `35353299444`, job `105626415840`, explicitly checked out the exact head.
- The job ran 255 standard-library tests successfully.
- It re-fetched the four pinned parent revisions plus the pinned Part 2 dependency, regenerated the source-free literary-body manifest, compared it byte-for-byte with the committed artifact using `cmp`, and replay-validated it.
- The committed identity remains source-free and bounded as `candidate_specific_inferred_reconstruction`; historical Russian Wikisource MediaWiki/Poem deployment equivalence remains unproven.
- `fantlab_source_edition_match=unknown`, `gate_ready=false`, and `m2_parity_admissible=false` remain unchanged.

## Result

No blocking defect was found. PR #127 was marked Ready and squash-merged as `7bf0dd79bde5e9df76a4b96ebe56f4792c49e23e`.

The merged canonical source-free composite remains 3,810,618 characters / 6,958,930 UTF-8 bytes with raw and `scriptorium-text-v1` SHA-256 `4f8b61e05cf7d96485d9edc0854d99d994da6ba146fabc3f6a3d509110ce4288`.

M2 remains 0/5. The structured provenance trace still describes the literary body as unfrozen and is therefore the next bounded reconciliation target; it must be updated without implying FantLab analyzer-input/source-edition equivalence.
