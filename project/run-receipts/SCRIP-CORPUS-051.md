# Run receipt — SCRIP-CORPUS-051

Date: 2026-09-21
Mode: corpus / provenance
Issue: #189
Pull request: #190 (Draft)
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

The authored follow-up commits the source-free receipt, binds the machine provenance trace and public candidate page to that byte identity, adds provenance regressions, and changes the dedicated workflow from capture mode to replay/verify mode.

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

PR #190 remains Draft because this run authored the substantive provenance change. The next independent wake must re-read the final exact head, inspect settled PR workflows, confirm that the committed receipt is replayed rather than refreshed, and verify that no OCR/body/FantLab gate was promoted. If clean, a later run may mark Ready and merge.
