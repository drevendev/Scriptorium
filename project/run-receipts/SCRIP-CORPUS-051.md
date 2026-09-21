# Run receipt — SCRIP-CORPUS-051

Date: 2026-09-21
Mode: corpus / provenance
Issue: #189 (closed completed)
Pull request: #190 (independently reviewed; squash-merged as `834606c494b2c1aac94cc75f6ebf4b0c816e0d9d`)
Base at selection: `5262067b7fda3d7cb2b3aa898f719fbf588c705d`

## Selection

The repository had no open PRs or issues and `STATE_AND_QUEUE.md` returned to the P2 `SCRIP-CORPUS continuation` row. SCRIP-CORPUS-050 had retained the Perelman 1913 popular-science candidate with a frozen bibliographic/legal description surface but an explicitly unfrozen PDF byte identity. The next bounded evidence step was executable without changing milestone policy: independently stream the exact current Commons original, freeze source-free digests, and keep every literary-body/FantLab gate closed.

## Evidence and production

Fresh Commons evidence still exposed the current 2021-09-03 file revision as 223 pages / 28,168,847 bytes with provider SHA-1 `3c616f547ff283a2cafd1ac26b448a8e8013f648`; the permanent description `oldid=1045983412` remains a separate bibliographic/legal surface.

The local automation runtime could not resolve `upload.wikimedia.org`. This was treated as a scoped network limitation, not as evidence about the file. Initial authored head `1e7e41821d98f770887ffabcc1dd57866e899de0` therefore added a fail-closed transient streamer plus a hosted capture workflow.

GitHub Actions run `35641285926`, job `106470938299`:

- checked out exact head `1e7e41821d98f770887ffabcc1dd57866e899de0`;
- passed 7 focused scan-identity tests;
- independently streamed the exact current Commons original;
- reproduced byte count `28168847` and SHA-1 `3c616f547ff283a2cafd1ac26b448a8e8013f648`;
- established SHA-256 `3d87d22a42ad949654265e066f81211d7831e32c8b62b96c967cd4cd33e7ed61`;
- uploaded only the source-free JSON capture as artifact `10658576419` (941-byte ZIP, ZIP SHA-256 `a2814db9f4755db8dff262c171502a903c329977bfbf9e8b47716d40c37341b5`).

The authored follow-up committed the source-free receipt, bound the machine provenance trace and public candidate page to that byte identity, added provenance regressions, and changed the dedicated workflow from capture mode to replay/verify mode.

## Independent review and merge

Independent review `5271171588` re-read final exact head `75d6a862e9ed31ff4c9d71d2a3524569ab21c0ec` against unchanged base `5262067b7fda3d7cb2b3aa898f719fbf588c705d`. The branch was 2 commits ahead / 0 behind with 10 changed files, mergeable, and had no review threads. No merge blockers were found.

All 15 PR-triggered workflow runs returned for that exact head settled `success`. Dedicated replay run `35642318440` / job `106474350077` checked out the reviewed SHA, passed 11 focused scan/provenance tests, re-streamed the exact Commons original, and reproduced byte count `28168847`, SHA-1 `3c616f547ff283a2cafd1ac26b448a8e8013f648`, and SHA-256 `3d87d22a42ad949654265e066f81211d7831e32c8b62b96c967cd4cd33e7ed61`.

Artifact `10658293142` was independently downloaded and inspected. Its ZIP is 1,551 bytes with SHA-256 `b7422205be15b395bfad9cf61b47060db688ae201824834dedfea5fb400296cb`; it contains exactly the source-free committed receipt plus the source-free verification JSON, and no scan bytes, images, OCR, or literary source text. Pages run `35642318393` checked out the same reviewed SHA, passed the full 419-test standard-library suite, canonical static-site build and deterministic rebuild; live deployment remained policy-skipped.

PR #190 was marked Ready and squash-merged as `834606c494b2c1aac94cc75f6ebf4b0c816e0d9d`; Issue #189 closed automatically as completed.

## Gate judgement

Advanced:

- exact current Commons PDF byte identity for the retained 1913 first-edition candidate;
- source-free SHA-256 and provider SHA-1/byte-count cross-check;
- public provenance representation of the binary freeze.

Not advanced:

- PDF/source-byte publication;
- page-selection or OCR profile;
- literary-body identity/count/digests;
- >=300,000-character calibration admission;
- work-specific FantLab linguistic-analysis surface or analyzer-input/source-edition identity;
- diagnostics, parity, or M2. M2 remains 0/5.

## Handoff

SCRIP-CORPUS-051 is complete. Resume normal-flow selection from the P2 `SCRIP-CORPUS continuation` queue. A later bounded Perelman unit may define and verify a deterministic page-selection/OCR/body contract over this frozen scan identity; keep >=300k, FantLab diagnostic/source-match, and M2 gates closed until separately proved.
