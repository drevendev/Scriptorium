# Run receipt — SCRIP-CORPUS-018

## Selection

- Selected from `SCRIP-CORPUS continuation` after re-orienting from `AGENTS.md`, `PROJECT_MANIFEST.md`, `STATE_AND_QUEUE.md` revision 112 and the changelog.
- No review-ready or interrupted Scriptorium work preempted normal selection.
- The state preference to strengthen a retained trace-only candidate was applied to `gorky-klim-samgin-ru`.
- Issue: #105. PR: #106.
- Base master at selection: `4b1116ad53a8d39833a4d096ef289f1a5e5f65fb`.

## Produced

Hosted bootstrap capture on PR head `eea2ef6016c9425992d693a7a4bf2599e816b883` used the existing source-free `scriptorium.single_page_revision` contract against the four already-retained permanent part revisions. It produced exact source identities without retaining prose:

| Part | page ID | revision | timestamp | wikitext chars | UTF-8 bytes | wikitext SHA-256 |
| ---: | ---: | ---: | --- | ---: | ---: | --- |
| 1 | 364224 | 5733765 | 2026-07-28T12:17:48Z | 964649 | 1745139 | `556dab4e3c66c8d597dd19f5db6ddae8c1eb52649a97025ff61d4ce388fad575` |
| 2 | 580077 | 5198033 | 2024-11-26T11:16:35Z | 581888 | 1054386 | `34dc8bf7d1dc77f9aa1686ef0ac348101beac19ccd97d467ee3857e014ad8853` |
| 3 | 580070 | 5138882 | 2024-05-24T20:48:07Z | 681084 | 1234670 | `95d782223c9c6893131fbb2ed7a4a6c4b2c14aea074083721d9425b1d30c8182` |
| 4 | 580075 | 5724453 | 2026-06-21T18:58:09Z | 1001169 | 1868725 | `ce353961f4d76a7f6775456ce1df53d23f33c3073f2126c716fa69561d119bbb` |

The committed four-part set uses deterministic part order 1→4. The canonical ordered source-identity projection has SHA-256 `54beabd28d8459bc6a0f1d83187dca56067e337999688d32c809d34340105577`; revision containers total 3,228,790 characters / 5,902,920 UTF-8 bytes.

Added:
- four exact per-part `scriptorium-single-page-source-revision-v1` manifests;
- `gorky-klim-samgin-ru.revisions.json`, which binds deterministic order and source-identity digest while explicitly keeping literary-body/composite identity false;
- dedicated replay workflow with exact committed-vs-observed comparison;
- standard-library tests for order, digest, source-prose exclusion and fail-closed parity flags;
- synchronized source-free provenance trace and public candidate page;
- durable changelog/state/receipt bookkeeping.

## Verification

Bootstrap workflow run `35183557851`, job `105080693934`, passed the then-current 171-test standard-library suite and captured all four exact revisions successfully. The hosted receipt itself contained only source-free identities; uploaded bootstrap artifact SHA-256 was `f4e266200b496faf051c448a1d755bb89640dd017fa9587dd377f4c32f1ae757`.

The final authored exact head was `68a2dd51384ad6b0efbdff36ed2cf341897ea9ff`. Dedicated run `35183988586` completed successfully: it ran 173 standard-library tests, re-captured all four pinned revisions, compared every observed source-free manifest byte-for-byte with the committed manifest, replayed each exact revision, verified the deterministic ordered revision-set digest and uploaded source-free capture/replay evidence. Exact-head runs `35183988845` (Scriptorium Pages), `35183988669` (frozen diagnostic), and `35183988582` (pinned pylem provider) also completed successfully.

A later independent run reviewed the exact head against Issue #105, the 13-file / 14-commit diff, current public provenance, workflow results and the fail-closed evidence boundary. No blocking defect or inline review thread remained. PR #106 was marked Ready and squash-merged as `23925a0e8188937905bcf1e0250a4384b191c7e7`; Issue #105 closed completed.

## Evidence boundary

No source prose is committed. Revision-wikitext identity is frozen; deterministic literary-body extraction/composition and raw/normalized composite body digests are not. FantLab does not disclose its analyzer-input edition or bytes, so `fantlab_source_edition_match=unknown`, `diagnostic_ready=false`, `gate_ready=false`, `m2_parity_admissible=false`, and M2 remains **0/5 source-matched works**.
