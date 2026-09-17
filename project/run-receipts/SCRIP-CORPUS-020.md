# Run receipt — SCRIP-CORPUS-020

- Date: 2026-09-17
- Issue: #109
- PR: #112 — merged as `aae7290f6056831bd291ac8a7a59100bad0ff4e8`
- Branch: `agent/scriptorium-corpus-020-poemx1-history`
- Base at selection: `7798c76f80add8fac45db4aee3361b47f87cb7e4`
- Reviewed exact head: `4626bbeb0b99c12dd78c5d1b4e45e5a04581d72d`
- Result: `POEMX1_HISTORY_MERGED_CONTINUATION_OPEN`

## Selected bounded unit

Advance the open Klim Samgin source-graph boundary by freezing a deterministic historical revision identity for the `poemx1` template used six times by the already pinned Part 2 dependency. Do not reproduce or claim resolved MediaWiki expansion in the same unit; preserve the distinction between a deterministic as-of reconstruction anchor and historical render equivalence.

## Implementation

Added `scriptorium/template_history.py`, a source-free historical-template revision resolver. Its policy is `latest_revision_not_after_anchor_timestamp`. Capture stores only page/revision identity, counts and hashes; replay re-resolves the same as-of selection and separately fetches the exact selected oldid. The manifest explicitly records:

- `evidence_class = inferred_reconstruction_anchor`
- `historical_render_equivalence_proven = false`
- `template_expansion_reproduced = false`
- `source_text_committed = false`

Focused mocked tests cover query direction/anchor parameters, rejection of a revision newer than the anchor, title drift, source-free manifest boundaries, exact replay and selection/pinned-byte drift. The repository-wide standard-library suite now includes those tests.

A dedicated PR-head workflow `.github/workflows/klim-samgin-template-history.yml` first requires the existing Part 2 contract to retain exactly six `poemx1` invocations, then captures the historical template revision, probes source shape without prose, byte-compares the committed manifest/shape and replays the exact selected revision. Checkout and Python setup actions are full-SHA pinned and credentials are not persisted.

## Historical template evidence

Using pinned Part 2 oldid `5198033` and timestamp `2024-11-26T11:16:35Z` as the reconstruction anchor, live Russian Wikisource resolution selected `Шаблон:Poemx1`:

- page ID: `54236`
- oldid: `5142743`
- revision timestamp: `2024-06-02T02:25:12Z`
- MediaWiki SHA-1: `7b7da0fa04913bc902f6455addad437fc19d67d8`
- wikitext characters: `2412`
- UTF-8 bytes: `2918`
- wikitext SHA-256: `fa7e35686da5ce4c62986a7e8bfc72f2dba067118218d656b2f0983e5cfa06db`

The immutable source-free record is `corpus/candidates/source-edition-traces/gorky-klim-samgin-ru.poemx1-template.revision.json`.

## Source-shape evidence and correction

The first probe implementation was intentionally treated as diagnostic and was not committed as evidence because its simple double-brace regex could classify triple-brace parameter syntax as template openings. Before freezing shape evidence, the probe was repaired to require an exact double-brace opener (`(?<!\{)\{\{(?!\{)`), and parser functions plus the `PAGENAME` magic word were separated from ordinary template-shaped invocations.

The corrected source-free raw inventory for oldid `5142743` is committed as `gorky-klim-samgin-ru.poemx1-template.shape.json`:

- ordinary raw template-shaped invocations: `doc` x1
- parser functions: `#expr` x2, `#if` x5, `#ifeq` x5, `#iferror` x1, `#tag` x1
- magic words: `PAGENAME` x1
- HTML-like tags: `div` x6, `includeonly` x2, `noinclude` x4, `templatedata` x2

This artifact explicitly does **not** apply MediaWiki `noinclude` / `includeonly` / `onlyinclude` transclusion semantics and therefore does not claim that `doc` or any other raw construct is an effective transitive dependency.

## Verification / repair evidence

The first exact-head capture run `35223860049` completed successfully and ran **192** standard-library tests while establishing the selected template revision identity. A later strict replay run `35224056659` again passed all 192 tests, the Part 2 dependency guard, live template capture and the corrected v2 source-shape probe, then failed at the intended byte comparison because the newly hand-copied committed manifest had one malformed percent-encoded character sequence in `source_work_url`. That authored-data defect was repaired from the workflow's generated manifest, and the workflow was tightened so both manifest and shape artifacts are mandatory and byte-compared before exact replay.

Final exact-head run `35224478878` checked out `4626bbeb0b99c12dd78c5d1b4e45e5a04581d72d`, passed **192** standard-library tests, required the existing six-`poemx1` Part 2 shape, live-resolved the historical template revision, regenerated the corrected source-free raw-shape evidence, byte-compared both committed evidence files, and replayed exact oldid `5142743`. Exact-head Pages run `35224478838`, frozen diagnostic run `35224478864`, and pinned-pylem provider run `35224478848` also completed successfully.

## Independent review and merge

A later independent run re-read the exact PR head, 9-file scope, historical resolver, manifest validation/replay, source-free shape probe, public provenance wording and durable-state changes. PR #112 was mergeable, 14 commits ahead / 0 behind `master`, with no inline review threads. No blocking defect was found.

The review specifically preserved the uncertainty boundary: `inferred_reconstruction_anchor` is not historical render proof; `historical_render_equivalence_proven=false`; `template_expansion_reproduced=false`; and the raw source-shape artifact does not claim MediaWiki inclusion semantics or an effective dependency graph. Resolved Part 2/body identity, FantLab input identity and M2 admission remain unavailable.

PR #112 was marked Ready and squash-merged as `aae7290f6056831bd291ac8a7a59100bad0ff4e8`. Issue #109 remains open for continuation.

## Public representation

`corpus/candidates/gorky-klim-samgin-ru.md` exposes the exact `poemx1` as-of revision identity and the raw structural boundary. It states that the timestamp policy is inferred reconstruction evidence rather than proof of MediaWiki historical render state, and it keeps resolved Part 2/body identities unavailable.

No source prose was committed.

## Evidence boundary / benchmark movement

The new template anchor narrows the MediaWiki-expansion problem but does not produce a literary body. No resolved Part 2 wikitext identity, four-part extraction/composition identity, raw body digest or `scriptorium-text-v1` digest is recorded.

`fantlab_source_edition_match=unknown`; `diagnostic_ready=false`; `gate_ready=false`; `m2_parity_admissible=false`; M2 remains **0/5 source-matched works**.

## Next action

Continue Issue #109 in a later bounded unit by applying/freeze-testing MediaWiki `noinclude` / `includeonly` / `onlyinclude` semantics to pinned `poemx1`, determine the effective transclusion dependency graph, and reproduce only the evidenced parser-function / `#tag:poem` behavior before resolving Part 2 bytes. Keep historical render equivalence explicitly unproven until that expansion layer is deterministic.
