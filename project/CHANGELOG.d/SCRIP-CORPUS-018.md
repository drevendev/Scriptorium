# SCRIP-CORPUS-018 — Klim Samgin revision-wikitext freeze

- Issue: #105
- PR: #106
- Status: `DONE`
- Merged commit: `23925a0e8188937905bcf1e0250a4384b191c7e7`
- Scope: corpus / provenance strengthening; no literary-body extraction or FantLab parity promotion.

## Change

The retained Maxim Gorky *The Life of Klim Samgin* candidate now freezes the exact source-free revision-wikitext identity of all four Russian Wikisource literary part revisions already traced in SCRIP-CORPUS-017:

- part 1 — `oldid=5733765`, page ID `364224`, timestamp `2026-07-28T12:17:48Z`, MediaWiki SHA-1 `721b84af3fcdcdf14bad0e663b8e1ab1384cff9c`, wikitext SHA-256 `556dab4e3c66c8d597dd19f5db6ddae8c1eb52649a97025ff61d4ce388fad575`;
- part 2 — `oldid=5198033`, page ID `580077`, timestamp `2024-11-26T11:16:35Z`, MediaWiki SHA-1 `2d5b9de21f539d12b34c72caa62f228998eaf80c`, wikitext SHA-256 `34dc8bf7d1dc77f9aa1686ef0ac348101beac19ccd97d467ee3857e014ad8853`;
- part 3 — `oldid=5138882`, page ID `580070`, timestamp `2024-05-24T20:48:07Z`, MediaWiki SHA-1 `61d0ce66ce00bfed3c700d639388f1b6e6460e41`, wikitext SHA-256 `95d782223c9c6893131fbb2ed7a4a6c4b2c14aea074083721d9425b1d30c8182`;
- part 4 — `oldid=5724453`, page ID `580075`, timestamp `2026-06-21T18:58:09Z`, MediaWiki SHA-1 `9c87ed020620076786cdd46deeaffd0ab43bea1e`, wikitext SHA-256 `ce353961f4d76a7f6775456ce1df53d23f33c3073f2126c716fa69561d119bbb`.

The four revision containers total 3,228,790 wikitext characters / 5,902,920 UTF-8 bytes. Their deterministic part-ordered source-identity projection is bound by SHA-256 `54beabd28d8459bc6a0f1d83187dca56067e337999688d32c809d34340105577`.

A dedicated GitHub Actions workflow re-fetches every pinned revision, compares each observed source-free manifest byte-for-byte with the committed manifest, replays through `scriptorium.single_page_revision`, and verifies the ordered identity-set digest. Standard-library tests cover exact ordering, source-prose exclusion and the fail-closed evidence boundary.

## Review and merge

Independent later-run review of exact head `68a2dd51384ad6b0efbdff36ed2cf341897ea9ff` found no blocking defect. Before merge, PR #106 was mergeable, 14 commits ahead / 0 behind master, with 13 changed files and no inline review threads. Exact-head runs `35183988586` (Klim Samgin source revisions), `35183988845` (Scriptorium Pages), `35183988669` (frozen diagnostic), and `35183988582` (pinned pylem provider) all completed successfully. PR #106 was marked Ready and squash-merged as `23925a0e8188937905bcf1e0250a4384b191c7e7`; Issue #105 closed completed.

## Boundary

This unit freezes revision **wikitext containers**, not a composed literary body. Candidate-specific fail-closed extraction, literary composition, raw/`scriptorium-text-v1` composite body digests and FantLab analyzer-input identity remain unresolved. `fantlab_source_edition_match=unknown`, `diagnostic_ready=false`, `gate_ready=false`, `m2_parity_admissible=false`, and M2 remains 0/5.
