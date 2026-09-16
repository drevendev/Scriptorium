# SCRIP-CORPUS-016 run receipt

- Date: 2026-09-17
- Issue: #101
- PR: #102
- Base revision: `d76c5403d62ec85c022efe4def93883eef550da3`
- Authored branch: `scrip-corpus-016-hyperboloid-body`
- Status: REVIEW_PENDING
- Selection reason: no interrupted claim or review-ready Scriptorium PR preempted selection at orientation time; the queue exposed only `SCRIP-CORPUS continuation`, and the retained Hyperboloid trace explicitly named deterministic literary-body extraction plus raw/normalized digests as its next evidence step.

## Produced

- Added `scriptorium/hyperboloid_freeze.py` with a source-specific fail-closed exact-revision body extraction/replay contract.
- Added `scriptorium/hyperboloid_probe.py` to inspect exact pinned markup shape without retaining literary prose.
- Added `tests/test_hyperboloid_freeze.py`.
- Extended `.github/workflows/hyperboloid-source-revision.yml` so exact revision identity, body capture, committed body-manifest comparison/replay and source-free artifact checks run together.
- Added `corpus/candidates/source-edition-traces/tolstoy-hyperboloid-garin-wikisource-ru.body.json`.
- Updated the canonical Hyperboloid trace and public corpus README to expose a frozen public body while retaining the print-edition/FantLab boundary.
- Added `project/CHANGELOG.d/SCRIP-CORPUS-016.md` and this durable run receipt.

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

## Verification

Bootstrap exact-head run `35155623478` at `be66ec664a4aba2231a283f0d3914480eb768818` passed 171 standard-library tests, fresh pinned revision capture, byte-for-byte committed revision-manifest comparison, revision replay, source-free structure probing, deterministic body capture, source-free assertions and artifact upload. Artifact ID `10471235096` had zip SHA-256 `e2bc943cd50643c99ba8535f97ef8c31f55edfb2f945c29cfb88713444b148eb`.

That run emitted the body identity above. The committed body manifest and later bookkeeping still require final exact-head workflow verification before PR #102 is marked review-ready.

## FantLab / benchmark boundary

FantLab work `44824` displays `495539` characters and `69126` words. The frozen public body is `3527` characters larger. This is evidence of non-identity or differing source/extraction/counting policy, not source-match evidence.

The `az.lib.ru` transcription still has no direct bibliographic print-edition identity. The Moscow Goslitizdat 1958 / 1939-derived textual family remains a lead only, and FantLab does not disclose the analyzer-input edition or immutable bytes. Therefore `fantlab_source_edition_match=unknown`, `diagnostic_ready=false`, `gate_ready=false`, `m2_parity_admissible=false`, and M2 remains `0/5`.

## Next wake

If final exact-head CI is green, perform an independent review of PR #102 before merge. Verify that the source-specific extraction contract remains fail-closed, committed public artifacts contain no source prose, the body manifest reproduces byte-for-byte from oldid `5014458`, and no public-source freeze is promoted to FantLab source parity.
