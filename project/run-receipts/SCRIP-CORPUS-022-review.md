# Run receipt — SCRIP-CORPUS-022 final review

- Issue: #131 (closed completed)
- PR: #132 (merged)
- Reviewed exact head: `fc92445d106862466545fecbefe2784f3ed2d817`
- Merge commit: `6ba097134047e3cf065337818f41535a9d6e684d`
- Mode: recovery / independent review
- Result: clean exact-head review; PR marked Ready and squash-merged.

## Re-orientation

The run read `AGENTS.md`, `project/PROJECT_MANIFEST.md`, `project/STATE_AND_QUEUE.md`, the current Issue #131 / PR #132 state, review threads, and exact-head CI before judging the change. The PR was 12 commits ahead / 0 behind `master`, mergeable, Draft, and had no inline review threads.

## Verification

All **13** pull-request workflows on exact head `fc92445d106862466545fecbefe2784f3ed2d817` completed successfully. `Scriptorium Pages` run `35399003997`, job `105774341626`, explicitly checked out that SHA, ran **267 tests** successfully, built the canonical static site, verified a deterministic rebuild, and uploaded only the generated Pages artifact. The pinned-pylem workflow was also green.

Independent inspection confirmed that the deterministic route-manifest builder and tests fail closed on title/excluded-route/capture-scope drift and that no literary prose is committed. The top-level corpus README, dedicated candidate page, structured trace and committed route manifest now consistently distinguish route topology from literary-page/body identity.

A fresh provenance cross-check confirmed that the Wikisource category permanent revision points to `oldid=4715419` and the public category surface lists the retained route family, while FantLab edition `12637` describes the 1965 Detskaya literatura volume and places *Running on Waves* on pp. 77–276. This remains bibliographic evidence only, not a FantLab analyzer-input match.

## Decision

No blocking defect remained. A COMMENT review recorded the exact-head evidence; PR #132 was marked Ready and squash-merged with expected-head protection as `6ba097134047e3cf065337818f41535a9d6e684d`. GitHub then closed Issue #131 as completed.

## Gate / public-representation effect

The merged repository now exposes an inspectable source-free 36-title route witness and an explicit excluded 1980/`az.lib.ru` route boundary for Running on Waves. Exact literary-page revisions, literary-body extraction/composition, composite digests and FantLab analyzer-input identity remain unfrozen/unknown. `fantlab_source_edition_match=unknown`, `diagnostic_ready=false`, `gate_ready=false`, `m2_parity_admissible=false`; M2 stays **0/5**. No benchmark parity movement occurred.
