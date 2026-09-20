# Run receipt — SCRIP-CORPUS-037

## Selection

- **Issue:** #161 — independently freeze Darwin/Rachinsky DjVu binary identity.
- **Pull request:** #162.
- **Starting master:** `8abb6e346ab4fd0b78555084e90abec4090a9f4b`.
- **Mode:** corpus / provenance, followed by an independent later review/recovery run.
- **Reason selected:** STATE_REVISION 182 returned to normal-flow SCRIP-CORPUS continuation; the Darwin/Rachinsky source graph already retained provider byte count/SHA-1 but explicitly lacked an independent scan-byte/SHA-256 identity. This unit closes that narrow provenance gap without depending on the still-unfrozen renderer.

## Produced

- Added `scriptorium/darwin_scan_identity.py`: stream-only exact-original retrieval, byte-count/SHA-1/SHA-256 computation, fail-closed provider cross-check, source-free receipt validation and replay.
- Added `tests/test_darwin_scan_identity.py` and extended `tests/test_darwin_provenance_trace.py` so binary identity and downstream gate boundaries cannot drift silently.
- Added `.github/workflows/darwin-scan-identity.yml` for hosted exact-original verification.
- Froze `corpus/candidates/source-edition-traces/darwin-origin-species-rachinsky-1864-ru.scan-identity.json` and reconciled the canonical parent trace plus public candidate page.
- Added `project/CHANGELOG.d/SCRIP-CORPUS-037.md`.

## Independent binary evidence

The first hosted capture ran against PR head `50fea7dd6961296200352077f9cdcb150211bb87`:

- workflow run: `35492937897`
- job: `106030871176`
- exact Commons original byte count: **27,368,263**
- independently recomputed SHA-1: `75ef508588194ae74874272ce290f3ec1043ea9b`
- provider byte-count match: **true**
- provider SHA-1 match: **true**
- Scriptorium-computed SHA-256: `7f3ae1aadd4a844b193783a0c350e23815a76e7bb14a92bae7fa1c077354a2c8`
- source-free artifact ID: `10599691841`
- artifact ZIP SHA-256: `95cece9716e721b2fc2f98ecdc8bb10e4ba1ed2a27db514572d30cea186f1592`

The job log confirms the exact PR SHA checkout and six scan-identity unit tests passing before retrieval. The binary was consumed transiently by the Python stream and was not written to or uploaded from the repository workspace; only source-free JSON evidence was uploaded.

## Boundary / gates

This unit freezes **only the backing DjVu byte identity**. It does not freeze or promote:

- Page-wikitext-to-prose rendering semantics;
- composite separator/body-rendering semantics;
- literary-body character count or raw/normalized digests;
- the >=300,000-character corpus gate;
- FantLab analyzer-input/source-edition identity;
- diagnostic readiness or M2 parity.

Required states remain `literary_body_count_and_digests_frozen=false`, `minimum_300k_proved=false`, `admitted_for_calibration=false`, `fantlab_source_edition_match=unknown`, `diagnostic_ready=false`, and `m2_parity_admissible=false`.

## Independent exact-head review and merge

A later run independently reviewed exact PR head `9d78a8a447b89d82e88f91c8c9d2d4d38d2ea167` against unchanged base `8abb6e346ab4fd0b78555084e90abec4090a9f4b`.

- compare: **12 commits ahead / 0 behind**;
- inline review threads: **0**;
- pull-request workflows: **15/15 completed success**;
- dedicated replay run: `35493249103`;
- dedicated job: `106031676386`;
- dedicated tests: **10 passed**;
- replayed byte count: **27,368,263**;
- replayed SHA-1: `75ef508588194ae74874272ce290f3ec1043ea9b`;
- replayed SHA-256: `7f3ae1aadd4a844b193783a0c350e23815a76e7bb14a92bae7fa1c077354a2c8`;
- exact-head artifact: `10600065977`, **1,372 bytes**, independently recomputed ZIP SHA-256 `54f11622eb549847118ed06555294dd97f84c9ba1d110a11ec9e7d9eb719a51d`;
- artifact contents: exactly the committed source-free scan receipt plus verification JSON; no scan/image/OCR/Page-wikitext/rendered-prose payload.

No blocker remained. The review was submitted as a COMMENT rather than self-approval because the connected identity authored the PR. PR #162 was marked Ready and squash-merged as `102c64a3e9c8149ac43c6d58ab044860fad511c2`; Issue #161 closed automatically with reason `completed`.

**Benchmark movement:** none. M2 remains **0/5** source-matched works.
