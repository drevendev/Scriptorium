# Run receipt — SCRIP-CORPUS-020 parameter-2 surface

- Issue: #109
- Pull request: #117
- Branch: `scrip-corpus-020-poem-content-surface`
- Base master at claim: `9c06bbbd3d511e8c3e9be67a7a02b6288a8dec64`
- Status: `AUTHORED_REVIEW_PENDING`
- Run date: 2026-09-18

## Selected bounded unit

Freeze the source-free recursive-expansion/render surface of the six exact `poemx1` parameter-2 values already bound to the pinned Klim Samgin Part 2 dependency. The unit answers whether further nested template/parser dependency resolution is required before historical `#tag:poem` rendering.

## Produced

- `scriptorium/mediawiki_poemx1_content.py` — fail-closed source-free revalidation and surface inventory.
- `tests/test_mediawiki_poemx1_content.py` — balance/drift/source-free/markup-surface coverage.
- `.github/workflows/klim-samgin-poem-content.yml` — exact-head refetch/regenerate/upload/byte-compare replay.
- `corpus/candidates/source-edition-traces/gorky-klim-samgin-ru.poemx1-content.json` — committed source-free observed evidence.
- synchronized public candidate page, machine-readable provenance trace, state and changelog receipt.

## Evidence

All six parameter-2 SHA-256 identities revalidate against the existing concrete-binding manifest. Aggregate observed surface: 324 characters, 589 UTF-8 bytes, 15 value-local lines, 9 newlines, 0 double-brace template/parser constructs, 0 triple-brace parameter constructs, 0 XML-like tags, 0 wikilinks, 0 external links, 0 apostrophe-markup runs, 0 leading-colon lines, 0 leading-space lines and 0 blank lines.

Therefore nested template/parser/tplarg expansion is identity for these exact values and no additional template dependency resolution is required. This does not reproduce Poem rendering or prove historical render equivalence.

## Verification

Discovery run `35279662523` on exact head `76ce460d9a9c7f9ee097266fd23e56d288124205` passed the full standard-library suite, exact pinned-dependency re-fetch, source-free manifest generation and artifact upload. Its only failure was the designed final comparison against an expected manifest that had not yet been committed. Artifact `10521941527` supplied the source-free observed manifest that was then committed verbatim. Fresh exact-head CI after durable/public synchronization is required before judgement.

## Remaining boundary

Issue #109 remains open. The next technical layer after independent review/merge is the sole live historical `#tag:poem` / Poem-extension behavior for the six exact values. Resolved Part 2 identity, four-part literary extraction/composition, raw/`scriptorium-text-v1` composite digests, FantLab analyzer-input identity and M2 advancement remain unclaimed.
