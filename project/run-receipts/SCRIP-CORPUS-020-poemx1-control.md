# Run receipt — SCRIP-CORPUS-020 `poemx1` control flow

- Date: 2026-09-17
- Issue: #109
- PR: #116 (Draft)
- Base at selection: `master@3f2312675aca5d1fe60a716c818b45110d874761`
- Authored semantic head verified: `23b3152f8bf97decdcf95a0021c950682cfd4125`
- Mode: corpus / provenance correctness

## Selected bounded unit

Resolve only the parser-control branches forced by the already-frozen six `poemx1` invocation frames, rather than implementing every parser function appearing in the static template inventory.

## Produced

1. Added `scriptorium/mediawiki_poemx1_control.py`, a fail-closed candidate-specific reducer tied to pinned `Poemx1` oldid `5142743`, its exact wikitext digest, the post-inclusion input digest, static construct inventory, literal parameter surface and six concrete binding shapes.
2. Added standard-library regression tests for exact branch decisions and fail-closed drift detection.
3. Added `gorky-klim-samgin-ru.poemx1-template.control.json`, containing only source-free frame states, invocation digests, reachable/unreachable construct counts and branch decisions.
4. Added a dedicated exact-head workflow that regenerates and byte-compares the control artifact.
5. Updated the public Klim candidate page and machine-readable provenance trace so the repository no longer implies that dead `#expr` / `#iferror` branches remain required work.
6. Advanced durable state to revision 129 and retained M2 at 0/5.

## Evidence and verification

Current official MediaWiki ParserFunctions documentation was re-checked during the run: `#if` treats empty or whitespace-only input as false; ParserFunctions trim leading/trailing whitespace; non-numeric `#ifeq` operands compare as case-sensitive text. MediaWiki magic-word documentation confirms `#tag` invokes XML-style parser/extension tags and that extension tags in non-selected conditional paths are not parsed.

Exact semantic head `23b3152f8bf97decdcf95a0021c950682cfd4125` completed successfully on:

- `35273911005` — Klim Samgin poemx1 control flow
- `35273911132` — Klim Samgin poemx1 invocation bindings
- `35273911079` — Klim Samgin historical template dependency
- `35273911025` — Klim Samgin source revisions
- `35273911000` — Scriptorium Pages
- `35273911044` — Scriptorium frozen diagnostic

The dedicated control job checked out the exact semantic head, ran the full standard-library suite, regenerated the source-free control manifest from committed prerequisite artifacts and byte-compared it to the committed evidence. PR #116 was mergeable and had no inline review threads at authored-head verification.

## Result / boundary

For all six frozen frames, reachable template control is `#if` x4, `#ifeq` x3 and `#tag` x1. The two `#expr` calls, the one `#iferror`, one `#if` and two `#ifeq` occurrences are unreachable. The remaining live historical expansion path is `#tag:poem` with parameter `2` as content; recursive parameter-2 expansion and poem-extension rendering remain unresolved.

No resolved Part 2 bytes, historical render equivalence, literary-body composite, FantLab source identity or M2 advancement is claimed. PR #116 remains Draft for independent later-run review and must not be self-merged from this authoring run.
