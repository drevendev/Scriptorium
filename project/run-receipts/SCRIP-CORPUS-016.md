# SCRIP-CORPUS-016 run receipt

- Date: 2026-09-17
- Issue: #101
- PR: #102
- Base revision: `d76c5403d62ec85c022efe4def93883eef550da3`
- Authored branch: `scrip-corpus-016-hyperboloid-body`
- Reviewed exact head: `9fa268604dde91a078bc403a50d24fc2394b9bf5`
- Merged commit: `055e5c789ed65bc48eaaeb19bf007ad3400d1380`
- Status: DONE
- Selection reason: recovery/review-ready work preempted normal corpus selection. A prior independent review found a blocking contradiction between the newly frozen Hyperboloid revision/body manifests and the still-stale machine-readable candidate catalog. The authored repair synchronized that catalog and deliberately left PR #102 for a later independent exact-head review; this run performed that review and merged only after the repaired head remained green and internally consistent.

## Produced

- Added `scriptorium/hyperboloid_freeze.py` with a source-specific fail-closed exact-revision body extraction/replay contract.
- Added `scriptorium/hyperboloid_probe.py` to inspect exact pinned markup shape without retaining literary prose.
- Added `tests/test_hyperboloid_freeze.py`.
- Extended `.github/workflows/hyperboloid-source-revision.yml` so exact revision identity, body capture, committed body-manifest comparison/replay and source-free artifact checks run together.
- Added `corpus/candidates/source-edition-traces/tolstoy-hyperboloid-garin-wikisource-ru.body.json`.
- Updated the canonical Hyperboloid trace and public corpus README to expose a frozen public body while retaining the print-edition/FantLab boundary.
- Repaired `corpus/candidates/fantlab-parity-v1.json` after independent review found it still advertised the candidate as unfrozen.
- Independently reviewed repaired exact head `9fa268604dde91a078bc403a50d24fc2394b9bf5`, promoted PR #102 from Draft, and squash-merged it after all required evidence remained green.
- Reconciled durable project state and changelog after merge so the next wake sees SCRIP-CORPUS-016 as complete.

## Exact public-source identity

Revision container:

- page ID: `1022517`
- revision ID: `5014458`
- timestamp: `2023-08-30T20:13:01Z`
- MediaWiki SHA-1: `605afeabc38e4f5948371afdf976f586edbf1955`
- wikitext characters: `502280`
- wikitext UTF-8 bytes: `934455`
- wikitext SHA-256: `fa0b099bba2d0f0e6ce395a16de76317afcd8bec8b23b52e455f97a9726a4de9`

Frozen literary body under `scriptorium-hyperboloid-wikisource-body-v1`:

- characters including spaces: `499066`
- UTF-8 bytes: `930560`
- normalization profile: `scriptorium-text-v1`
- raw SHA-256: `a01c5eadef53b2437eff3abe6052bb7f7bf6f95737641558343363628da7f513`
- normalized characters including spaces: `499066`
- normalized SHA-256: `a01c5eadef53b2437eff3abe6052bb7f7bf6f95737641558343363628da7f513`
- source prose committed: `false`

The observed exact source shape is one leading `Отексте` metadata scaffold followed by direct prose rather than a `div.text` wrapper, 132 level-three headings, 9 trailing categories, 13 wikilinks, 44 bold/italic markers, tags `br:18`, `sup:18`, `u:18`, and 9 nested `sup/u` pairs. The two HTML comments occur inside the leading metadata scaffold and are excluded before literary extraction. Any inventory/source-shape drift fails closed.

## Verification history

Bootstrap exact-head run `35155623478` at `be66ec664a4aba2231a283f0d3914480eb768818` passed 171 standard-library tests, fresh pinned revision capture, byte-for-byte committed revision-manifest comparison, revision replay, source-free structure probing, deterministic body capture, source-free assertions and artifact upload. Artifact ID `10471235096` had zip SHA-256 `e2bc943cd50643c99ba8535f97ef8c31f55edfb2f945c29cfb88713444b148eb`.

After the body manifest, provenance, public README and durable state were committed, exact authored head `cbd56ee2b23e5205d0a251a9be55c71820618138` was fully green. `Hyperboloid source revision` run `35156176512`, `Scriptorium Pages` run `35156176530`, `Scriptorium frozen diagnostic` run `35156176472`, and `Scriptorium pinned pylem provider` run `35156176486` all succeeded.

A later independent review of exact head `bf41149bdd9996249db01ec9da9889376a80d057` reconfirmed the core implementation and green current-head runs `35156488833` (Hyperboloid replay), `35156488806` (Pages), `35156488898` (frozen diagnostic), and `35156488923` (pinned provider), but blocked merge because the central catalog still said `source_identity_status=traced_not_frozen` and retained a false blocker that the revision/body identities were not recorded.

The catalog-sync repair produced exact head `9fa268604dde91a078bc403a50d24fc2394b9bf5`. Fresh runs `35159779198` (Hyperboloid source/body replay), `35159779188` (Pages), `35159779182` (frozen diagnostic), and `35159779183` (pinned provider) all completed successfully. The Hyperboloid job ran the standard-library suite, re-fetched exact `oldid=5014458`, matched/replayed the committed revision identity, reproduced the committed body manifest byte-for-byte, passed the source-free structure probe and source-free/fail-closed assertions, and uploaded derived/replay evidence.

Immediately before the final independent review and merge, current `master` remained `d76c5403d62ec85c022efe4def93883eef550da3`; repaired PR #102 was 21 commits ahead / 0 behind, mergeable, changed exactly the 11 expected unit files, and had no inline review threads. The independent review found no remaining blocking defect. PR #102 was promoted from Draft and squash-merged with the expected-head guard as `055e5c789ed65bc48eaaeb19bf007ad3400d1380`; Issue #101 then closed completed.

## Catalog-sync repair

The repaired Hyperboloid catalog row records:

- `source_revision_manifest=corpus/candidates/source-edition-traces/tolstoy-hyperboloid-garin-wikisource-ru.revision.json`;
- `source_body_manifest=corpus/candidates/source-edition-traces/tolstoy-hyperboloid-garin-wikisource-ru.body.json`;
- `source_identity_status=public_candidate_frozen`;
- `frozen_candidate_characters=499066`;
- `frozen_candidate_bytes=930560`;
- `frozen_candidate_sha256=a01c5eadef53b2437eff3abe6052bb7f7bf6f95737641558343363628da7f513`.

The stale unfrozen blocker is removed. The row still keeps `fantlab_source_edition_match=unknown`, `diagnostic_ready=false`, `gate_ready=false`, and retains the real unresolved boundaries: FantLab analyzer-input identity is undisclosed, the frozen body differs from FantLab's displayed count by 3527 characters, and the `az.lib.ru` transcription is not independently tied to a specific 1927/1937/1939 print edition.

## FantLab / benchmark boundary

FantLab work `44824` displays `495539` characters and `69126` words. The frozen public body is `3527` characters larger. This is evidence of non-identity or differing source/extraction/counting policy, not source-match evidence.

The `az.lib.ru` transcription still has no direct bibliographic print-edition identity. The Moscow Goslitizdat 1958 / 1939-derived textual family remains a lead only, and FantLab does not disclose the analyzer-input edition or immutable bytes. Therefore `fantlab_source_edition_match=unknown`, `diagnostic_ready=false`, `gate_ready=false`, `m2_parity_admissible=false`, and M2 remains `0/5`.

## Next wake

Select the next dependency-satisfied SCRIP-CORPUS continuation unit from durable state. Prefer another legally usable >=300k diversity candidate or stronger independent source-identity evidence for an existing candidate. Keep public-source freezing, bibliographic leads and FantLab analyzer-input identity separate; never advance M2 from count proximity or title/edition plausibility.
