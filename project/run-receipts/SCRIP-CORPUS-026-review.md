# Run receipt — SCRIP-CORPUS-026 independent review

Date: 2026-09-19
Issue: #139
PR: #140
Mode: recovery / independent review
Result: exact-head review passed; PR merged; issue completed

## Reviewed exact head

`b0126f1d36d0fe8b2f8ce1e74b2d2da8f79cb85f`

The review re-read the repository control state and inspected the final PR diff, candidate-specific extractor/tests, source-free manifests, public/provenance wording, review threads and exact-head workflows. Master had not moved from PR base `f2413278df4e6bc70d48bb9eb2aa6425672d0e78`, so the review was not evaluating a stale branch relationship.

## Verification evidence

- PR #140 was mergeable and had no inline review threads.
- All 14 pull-request workflow runs associated with the exact head completed successfully.
- Candidate-specific run `35425572354`, job `105850791726`, checked out the exact head and completed the standard-library test suite; exact pinned source-revision capture/compare/replay; exact literary-body capture/compare/replay; source-free/fail-closed verification; and artifact upload.
- Its source-free artifact `10578759254` (`beketova-source-revision-and-body`) is bound to the reviewed head and has digest `sha256:6eb04993de0cf30b33cdf4e0e3da9b18722d48a5ee2efe9633b693901e276c01`.
- Pages run `35425572337`, build job `105850791667`, also checked out the exact head and passed the standard-library suite, canonical site build, deterministic rebuild, and Pages artifact upload. Live deployment remained intentionally skipped by repository policy/configuration.
- The committed body manifest remains source-free and binds exact revision `5304880` to extraction profile `scriptorium-beketova-captain-grant-wikisource-body-v1`, 1,095,467 characters including spaces, 2,040,240 UTF-8 bytes, and raw/normalized SHA-256 `4931eba535a4ef3989ac905d895258f00db57029e488d98511db50a7ce4d1161`.
- General corpus admission is justified only by the frozen literary body exceeding 300,000 characters plus retained legal/provenance evidence. No FantLab analyzer-input/source-edition identity is claimed; `fantlab_source_edition_match=unknown`, `diagnostic_ready=false`, `gate_ready=false`, `m2_parity_admissible=false`; M2 remains 0/5.

## Decision

No blocking defect was found. PR #140 was marked Ready and squash-merged with expected head SHA as `14f5a76ea3aa137554a6b320b49bba81f84bfbfa`. The `Closes #139` link closed Issue #139 as completed.

## Public representation

The merged corpus-root navigation, dedicated candidate page, structured provenance trace and source-free body manifest now expose the Beketova translation as a legally/provenance-qualified >=300k general Scriptorium corpus work while keeping translation identity and FantLab/M2 boundaries explicit. No source text was added to the repository.

## Benchmark movement

None. M2 remains 0/5 source-matched works.

## Next action

Re-apply the normal selection ladder. With #140 resolved and no known open recovery unit from this review, resume the highest-priority unblocked SCRIP-CORPUS continuation, preferring a legally usable >=300k diverse candidate or strengthening an existing twentieth/twenty-first-century, translated or nonfiction candidate without inferring a FantLab source match.
