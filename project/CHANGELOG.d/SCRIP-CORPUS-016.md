# SCRIP-CORPUS-016 — freeze Hyperboloid literary-body identity

Status: REVIEW_PENDING / READY_FOR_INDEPENDENT_REVIEW

Issue #101 / PR #102 strengthen `tolstoy-hyperboloid-garin-wikisource-ru` from a frozen MediaWiki revision container into a reproducibly frozen public literary-body identity without changing the unresolved FantLab boundary.

## Change

- Added `scriptorium.hyperboloid_freeze`, a source-specific fail-closed extractor/replayer for exact Russian Wikisource revision `oldid=5014458`.
- Added source-free structural probing used to derive and then enforce the exact observed single-page markup contract rather than guessing from another Wikisource work shape.
- Added standard-library tests covering observed-shape extraction, fail-closed markup/scaffold drift, source-free body manifests, exact revision drift and exact body replay drift.
- Extended the existing Hyperboloid source workflow so a fresh exact revision fetch must still match the committed revision identity, then must reproduce the committed literary-body manifest byte-for-byte and replay it successfully.
- Added source-free body manifest `corpus/candidates/source-edition-traces/tolstoy-hyperboloid-garin-wikisource-ru.body.json`.
- Promoted the canonical trace and public corpus README from `revision_wikitext_frozen_body_unfrozen` to `frozen_source_identity_unmatched_to_fantlab` while keeping print-edition identity and FantLab analyzer-input identity unresolved.

## Frozen public body

The exact pinned revision remains page ID `1022517`, oldid `5014458`, timestamp `2023-08-30T20:13:01Z`, MediaWiki SHA-1 `605afeabc38e4f5948371afdf976f586edbf1955`, and wikitext SHA-256 `fa0b099bba2d0f0e6ce395a16de76317afcd8bec8b23b52e455f97a9726a4de9`.

Under extraction profile `scriptorium-hyperboloid-wikisource-body-v1`, the derived public literary body is `499066` characters / `930560` UTF-8 bytes. Raw and `scriptorium-text-v1` normalized SHA-256 are both `a01c5eadef53b2437eff3abe6052bb7f7bf6f95737641558343363628da7f513`. No source prose is committed.

FantLab displays `495539` characters, `3527` fewer than the frozen public candidate. The delta is retained as evidence of non-identity or differing extraction/counting policy; it is not used to tune the extractor and does not establish a source match.

## Verification

Bootstrap exact-head run `35155623478` on `be66ec664a4aba2231a283f0d3914480eb768818` passed the full 171-test standard-library suite, fresh exact revision capture, committed revision-manifest comparison/replay, source-free structure probe, deterministic literary-body capture, source-free assertions and artifact upload. It produced the exact body identity later committed in the repository.

After the body manifest, provenance, public README and durable state were committed, exact authored head `cbd56ee2b23e5205d0a251a9be55c71820618138` was fully green: Hyperboloid source/body replay `35156176512`, Pages deterministic build `35156176530`, frozen diagnostic `35156176472`, and pinned-provider regression `35156176486` all completed successfully. The Hyperboloid run freshly re-fetched `oldid=5014458`, compared the committed revision manifest, reproduced the committed body manifest byte-for-byte, replayed it, passed source-free assertions, and passed the complete standard-library suite. PR #102 was then marked Ready for review and remains intentionally unmerged for a later independent judgement.

## Gate

`fantlab_source_edition_match=unknown`, `diagnostic_ready=false`, `gate_ready=false`, `m2_parity_admissible=false`. M2 remains `0/5` source-matched works. Public-source freezing cannot advance the reproduction gate by itself.
