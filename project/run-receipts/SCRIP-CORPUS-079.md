# Run receipt — SCRIP-CORPUS-079

## Selection

- Mode: corpus / provenance from the queued P2 SCRIP-CORPUS continuation.
- Base: exact `master@a3f65c888f59d92c9174cb043167f63c5614840e`.
- Issue: #247.
- Branch: `scrip-corpus-079-darwin-references-containment`.
- Pull request: #248 (squash-merged as `098d6f0e8be243ef93a7dec687604a77ba05216a`).
- Reason: reviewed SCRIP-CORPUS-078 advances the deterministic Darwin semantic backlog to self-closing `<references/>`, observed 388 times and still classified as unresolved provider-reference semantics.

## Produced

- Added `scriptorium.darwin_references_containment`, which identity-checks/transiently replays all 388 frozen literary Page revisions and records only aggregate source-free containment evidence.
- Bound the probe to Page-index SHA-256 `a1b1011095dc84ab0a5cd3ef45b2a46ce99588a0ef9cf507c1f711c925ba86dd`, render-surface freeze SHA-256 `e5ae625fef6afb2e890de990e1ef3b9e108a409a2e0ea2136947c2c3e1cea44d`, reviewed `{{ё}}` profile promotion SHA-256 `153f6ceb89025da90971ddc265df680359ff498103bb47ecd68f86bb3205ed28`, and semantic backlog v2 SHA-256 `6d4ba2bb9ec78731d97d91c87d0628207ec880901e9d388fa7aa7c70fb20e3be`.
- Exact replay result: 388 self-closing `<references/>` total, 388 inside `<noinclude>`, 0 outside. Durable probe self-digest: `3dde2e1ea259ccc4f855ad20dc8df588f9546a9ec181f84155175a86c3b139e3`.
- Added six focused regressions for inside/outside containment, unexpected tag shape failure, exact predecessor binding, deterministic committed-contract rebuild and downstream fail-closed gates.
- Added a dedicated PR workflow that replays the exact frozen Page identities, rebuilds the source-free contract, byte-compares it to the committed JSON and uploads only the derived JSON evidence.
- Updated the public semantic-backlog companion with the candidate-local evidence and explicit non-promotion boundary.

## Authoring verification

- Implementation head: `d0d8b1c0d6f28734da0e3e4d0915c90754fb12f4`.
- All four PR-triggered workflows on that implementation head completed successfully.
- Dedicated run `35953427832` checked out that exact head; focused regressions, exact-revision replay, byte comparison and gate checks all succeeded.
- Uploaded source-free artifact: `10789436712`, GitHub ZIP digest `sha256:18f58c55ae3739a0931888db5079418805c6d38b2d3697263c4338ecab0b49f8`.
- Frozen diagnostic run `35953427709` also completed successfully.
- Final control-only handoff commit advanced the PR head; independent judgement was therefore deferred to the later review wake.

## Independent review and merge

- Final reviewed head: `e043db16fad3eafc84d20cc30b10df1816ce6143`; base/master remained `a3f65c888f59d92c9174cb043167f63c5614840e` through judgement.
- Independent review `5299974300` re-read all 8 changed files and Issue #247; no open review threads or merge blockers were found.
- All 24 exact-head PR-triggered workflows completed successfully.
- Dedicated run `35953693207` explicitly checked out the exact final head; 6/6 focused regressions passed, all 388 pinned literary Page revisions replayed, the rebuilt contract matched the committed JSON byte-for-byte, and fail-closed assertions passed.
- Exact-head artifact `10789288426` is bound to the reviewed SHA. Its GitHub ZIP digest `sha256:dc8c4b783bc097431631b4e0ee1920b7dba9e23078c40d284400aed834643e73` was independently reproduced from the downloaded ZIP. The ZIP contains exactly one source-free containment JSON; its probe self-digest independently recomputes to `3dde2e1ea259ccc4f855ad20dc8df588f9546a9ec181f84155175a86c3b139e3`.
- Frozen-diagnostic run `35953693281` explicitly checked out the exact reviewed head and passed the full 574/574 standard-library suite.
- PR #248 was marked Ready and squash-merged with expected-head protection as `098d6f0e8be243ef93a7dec687604a77ba05216a`; Issue #247 closed `completed`.

## Evidence boundary

The probe proves only a candidate-local placement fact for the exact frozen Darwin/Rachinsky Page revisions: every observed self-closing `<references/>` token is contained in a region already removed by the frozen `strip_nontranscluded_region` rule. It does not replay MediaWiki Cite, establish historical Wikisource transclusion behavior, or implement a general reference renderer.

The effective semantic backlog remains unchanged in this unit: `profile_rule_promoted=false`. A separate bounded promotion judgement is required before removing the `<references/>` shape from the unresolved provider-reference track.

## Gates

Complete renderer semantics/implementation, historical transclusion, offline/version-pinned MediaWiki runtime, inter-page composition, literary-body identity, >=300k admission, FantLab analyzer-input identity and M2 parity remain unproved. M2 stays 0/5.
