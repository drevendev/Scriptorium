# SCRIP-CORPUS-069 run receipt

## Selection

- Mode: corpus / provenance durability recovery within the P2 SCRIP-CORPUS continuation.
- Base: `master@35a67871f086ba9fde017f8b69b29ade1434e6b5`.
- Issue: #227 (closed completed).
- Pull request: #228 (independently reviewed; squash-merged as `27a71622c12a3babbc76e6f8652f8bada17705e1`).
- Final reviewed head: `a23e59e68f4f249da3f22cc9ecc77a15eeab9327`.
- Review: `5289993577`.
- Reason: reviewed SCRIP-CORPUS-068 probe evidence was machine-readable only as a seven-day Actions artifact; repository prose retained its digest/summary but not the exact canonical JSON.

## Produced

- Added canonical source-free `darwin-origin-species-rachinsky-1864-ru.module-string-dependency-probe-v1.json` with embedded probe SHA-256 `e27a2af9f01c760f995c633e296e1d5825642d4c4bcbeb5fba8ae0a697c234cb`.
- Added focused freeze regressions that recompute the embedded digest, assert exact `Модуль:String@3684569` identity and source-free payload, and keep semantic/downstream gates closed.
- Updated the exact-revision CI probe to regenerate the source-free JSON from transient Wikisource source, delete the raw response, and byte-compare the derived JSON with the committed canonical freeze before upload.
- Updated public provenance and durable project state.

## Verification

- Independent exact-head review re-read all 7 changed files and found no merge blocker or open review thread.
- Recomputed canonical-object `probe_sha256` over the committed JSON excluding its self-digest field: `e27a2af9f01c760f995c633e296e1d5825642d4c4bcbeb5fba8ae0a697c234cb`.
- The committed JSON file bytes hash to `f0926b94f96dbb0c93d69fc72a4d771ac1d5afe4fa1a98eb76b470313af57038`.
- All 22 PR-triggered workflows for exact head `a23e59e68f4f249da3f22cc9ecc77a15eeab9327` settled `success` before merge.
- Dedicated workflow `35845962574` checked out the exact reviewed SHA, ran 18 probe/observation/freeze tests, regenerated exact `Модуль:String@3684569` source-free output from transient Wikisource source, deleted the raw response, and passed byte-for-byte `cmp` against the committed canonical JSON. Both compared files had physical SHA-256 `f0926b94f96dbb0c93d69fc72a4d771ac1d5afe4fa1a98eb76b470313af57038`.
- The live result still reports no static wiki-module dependencies, no non-wiki require literals and no dynamic/unsupported direct-loader calls under the bounded scanner, while `semantic_dependency_closure_proved=false` remains explicit.

## Independent review / merge

- Review `5289993577` judged exact head `a23e59e68f4f249da3f22cc9ecc77a15eeab9327` against unchanged base `master@35a67871f086ba9fde017f8b69b29ade1434e6b5`.
- PR #228 was marked Ready and squash-merged with expected-head protection as `27a71622c12a3babbc76e6f8652f8bada17705e1`.
- Issue #227 closed automatically as `completed`.

## Gates / non-claims

- `module_string_identity_bound=false`
- `semantic_dependency_closure_proved=false`
- `dependency_closure_complete=false`
- forced/non-forced outputs remain unverified
- renderer/body/>=300k/FantLab/M2 gates remain closed
- M2 remains 0/5

This unit does not claim historical transclusion provenance, recursive semantic closure, renderer equivalence or FantLab parity. SCRIP-CORPUS-069 is complete; resume normal-flow selection from the canonical P2 corpus/provenance queue.
