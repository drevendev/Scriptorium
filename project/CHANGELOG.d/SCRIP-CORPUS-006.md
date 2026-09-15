# SCRIP-CORPUS-006 — Hyperboloid bibliographic provenance strengthening

Issue: #81  
PR: #82  
Mode: corpus / provenance

## Decision

Strengthen `tolstoy-hyperboloid-garin-wikisource-ru` with a concrete 1958 Goslitizdat volume-4 bibliographic lead while keeping it explicitly non-identifying.

Direct evidence for the retained public candidate is unchanged: Russian Wikisource permanent revision `oldid=5014458` is a stable reviewed public-domain locator, cites `az.lib.ru`, and the work text says the novel was written in 1926–1927 and revised with new chapters in 1937. FantLab reports the 18 September 2022 linguistic analysis at 495,539 characters / 69,126 words, but does not disclose analyzer-input edition or bytes.

New collateral evidence narrows the next research target without crossing the source-identity gate:

- Russian Wikisource `Союз пяти (Толстой)`, a sibling A. N. Tolstoy page citing `az.lib.ru`, identifies its text source as A. N. Tolstoy, *Collected Works in ten volumes*, vol. 4, *Emigrants. Hyperboloid of Engineer Garin*, Moscow: Goslitizdat, 1958.
- Russian Wikisource `Случай на Бассейной улице (Толстой)`, another sibling Tolstoy page in the az.lib.ru import lineage, cites the same 1958 volume 4.
- FantLab bibliographic commentary on the novel independently identifies the same 1958 volume as a real *Hyperboloid of Engineer Garin* edition context.

These facts make the 1958 volume a testable edition-family lead. They do not prove that the Hyperboloid Wikisource/az.lib transcription was produced from that volume: the Hyperboloid page itself still names only `az.lib.ru`, and sibling-page provenance cannot establish the bytes or exact text identity of another page. They also say nothing about FantLab's undisclosed analyzer input.

## Gate effect

No parity or diagnostic gate advances:

- `bibliographic_source_identity` remains unset;
- `source_identity_status=traced_not_frozen`;
- `fantlab_source_edition_match=unknown`;
- `diagnostic_ready=false`;
- `gate_ready=false`;
- `m2_parity_admissible=false`;
- M2 remains **0/5 source-matched works**.

No source prose is committed. The next evidence path is to freeze the exact Wikisource revision/body identity and independently test the 1958 volume lead with a direct source statement rather than infer it from sibling metadata.

## Independent later-run review and merge

Exact-head review of `b3440047603d43f898ac5389cbde7a7b2ab1f1d3` found no blocking defect. The branch remained 4 commits ahead / 0 behind base `7aafd6a175bd6bc2716014a554b242cbca76bcc1`, changed only the four expected corpus/provenance/state files, and had no submitted reviews, review threads, or pre-existing PR discussion before the review receipt.

Required exact-head evidence was green: Pages run `35028225864` passed the standard-library suite, canonical site build, and deterministic rebuild; pinned-provider run `35028225888` passed the provider contract, exact hash-pinned `pylem==0.0.18` Python 3.9 native smoke, and frozen Anna sidecar replay.

Fresh source verification reconfirmed the evidence classification rather than strengthening it beyond what the PR claims: both sibling Wikisource pages explicitly cite the 1958 Goslitizdat volume 4 as their text source, and FantLab independently identifies that volume as a real Hyperboloid edition context. The Hyperboloid page itself still does not cite that volume, so the lead remains non-identifying and all source-match, diagnostic, gate-readiness, and M2 boundaries remain closed.

PR #82 was squash-merged as `3643b358859d3c875b83fc5af30dbe423fbb4d69`; Issue #81 closed completed.
