# SCRIP-CORPUS-020 — Klim Samgin hidden transclusion prerequisite

- Issue: #109
- PR: #110
- Status: `PREREQUISITE_MERGED_CONTINUATION_OPEN`
- Merge commit: `c6d49b19f7f9d64b014b60f4ba76c5d542938fdc`
- Reviewed exact head: `69811ae047553ffea7bfa89a94d77656ddf30366`
- Scope: corpus/provenance strengthening and source-graph correctness; no FantLab source-match or M2 promotion.

## Change

A source-free structural probe of the four already pinned Russian Wikisource parent revisions for Maxim Gorky's *The Life of Klim Samgin* found that Part 2 (`oldid=5198033`) contains an unversioned `#lst` labeled-section reference to `Жизнь Клима Самгина (Горький)/Часть 2/part2`. This means the four parent oldids alone do not freeze the complete literary source graph and a composite literary-body identity must not be claimed from them.

Scriptorium now independently pins the discovered dependency at page ID `580081`, revision `2366546`, timestamp `2016-11-29T05:49:23Z`, MediaWiki SHA-1 `899c3d348b8550486c2c6774b84bc3ff55495f43`, **583,889 wikitext characters / 1,058,733 UTF-8 bytes**, and wikitext SHA-256 `173054997b54b96241adc07aeb6f76624beb497f94602452d7f9e4e57b0c6996`. No source prose is committed.

The dedicated Klim workflow re-fetches, byte-compares and replays the four parent revisions plus this hidden dependency, and a source-free source-shape probe exposes parser-function dependencies so future extraction cannot silently depend on mutable current transclusions. Unit tests bind the dependency manifest and keep literary-body/composition flags fail-closed.

Public candidate/provenance surfaces state the stronger source-graph identity while explicitly refusing a literary-body freeze until the exact `#lst` labeled-section selection/placement semantics and the four-part extraction/composition contract are implemented and replayed.

## Independent review and merge

A later run independently reviewed exact head `69811ae047553ffea7bfa89a94d77656ddf30366`. The PR was mergeable, 14 commits ahead / 0 behind master, changed 10 expected files and had no inline review threads. No blocking defect was found.

Exact-head workflows were all successful: Klim source-graph replay `35203034786`, Scriptorium Pages `35203034809`, frozen diagnostic `35203034787`, and pinned pylem provider `35203034757`. The Klim job ran 183 standard-library tests, re-captured and byte-compared all five pinned revisions, replayed them exactly, and reported the expected Part 2 `lst_transclusion_targets` entry without emitting source prose.

PR #110 was marked Ready and squash-merged as `c6d49b19f7f9d64b014b60f4ba76c5d542938fdc`.

## Boundary / next trigger

Issue #109 intentionally remains open. The next implementation step is to freeze the exact labeled-section semantics used by the Part 2 invocation, then define fail-closed per-part extraction and deterministic Part 1 -> Part 2 -> Part 3 -> Part 4 composition before recording any raw or `scriptorium-text-v1` literary-body digest.

`fantlab_source_edition_match=unknown`, `diagnostic_ready=false`, `gate_ready=false`, `m2_parity_admissible=false`; M2 remains **0/5 source-matched works**.
