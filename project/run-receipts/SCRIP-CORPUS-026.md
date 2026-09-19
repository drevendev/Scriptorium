# Run receipt — SCRIP-CORPUS-026

Date: 2026-09-19
Issue: #139
PR: #140
Mode: corpus / provenance
Result: authored literary-body freeze and general-corpus admission, pending independent PR review

## Selected unit

Advance the retained Beketova Russian translation of *Children of Captain Grant* from an exact frozen source-revision identity to a deterministic source-free literary-body identity. This directly continues the durable P2 corpus/provenance queue and strengthens the translated-work diversity requirement without adding another trace-only candidate.

## Source-shape discovery

The generic single-page extractor first failed closed because exact revision `5304880` contains no generic transcription `<div>` wrapper. A temporary source-free hosted probe then established the exact observed topology without retaining prose:

- 11,028 wikitext lines;
- source/title scaffold through line 36;
- literary body begins at line 37;
- three level-3 part headings and 140 level-4 literary headings;
- eight trailing category lines at 11021–11028;
- the only templates (`Отексте`, `книга`, `uc`, `h`) and six `center` tags occur before the literary body;
- no `div`, `poem`, `noinclude`, `includeonly` or `onlyinclude` markers are present.

That evidence changed the implementation decision from reuse of the generic wrapper extractor to a narrow candidate-specific contract.

## Hosted verification

Bootstrap exact-head run `35425350073`, job `105850213235`, checked out `a6793410a3addc18afd895c5f490ddc9689f6492` and completed successfully. It ran **271 standard-library tests**, including four new candidate-specific tests; re-fetched and byte-identity-verified the already-frozen revision manifest; replayed the revision; applied `scriptorium-beketova-captain-grant-wikisource-body-v1`; checked the >=300,000-character threshold and non-parity gate; and uploaded only source-free JSON evidence.

The bootstrap artifact `10578549114` (`beketova-source-revision-and-body`) had uploaded ZIP SHA-256 `6d19fc09dac260434826bc19200be846eba1f01b20d30396a8052112f9b0758f`. The final workflow removes the temporary shape-probe artifact and requires byte-for-byte equality with the committed revision and body manifests plus an exact body replay.

Frozen literary-body identity:

- source revision: `oldid=5304880`, page ID `1012777`, timestamp `2025-02-25T02:24:10Z`;
- extraction profile: `scriptorium-beketova-captain-grant-wikisource-body-v1`;
- character count including spaces: `1,095,467`;
- UTF-8 byte count: `2,040,240`;
- raw SHA-256: `4931eba535a4ef3989ac905d895258f00db57029e488d98511db50a7ce4d1161`;
- normalization profile: `scriptorium-text-v1`;
- normalized character count including spaces: `1,095,467`;
- normalized SHA-256: `4931eba535a4ef3989ac905d895258f00db57029e488d98511db50a7ce4d1161`.

No source prose is committed or intentionally uploaded.

## Durable changes

- added `scriptorium/beketova_body.py` and fail-closed unit tests;
- extended the candidate-specific hosted replay workflow to verify both exact revision and exact body identities;
- committed `verne-children-captain-grant-beketova-ru.body.json` as source-free body evidence;
- reconciled the structured source-edition trace and dedicated public candidate page;
- updated `corpus/README.md` to expose the translated candidate's frozen body and general-corpus admission;
- advanced durable state to revision 161 and recorded this changelog/receipt.

## Gate boundary

The body itself now satisfies the >=300,000-character corpus rule and the retained Wikisource rights evidence explicitly covers the translation, so the candidate is admitted for general Scriptorium calibration/profile use. That does **not** establish a FantLab reference or analyzer-input/source-edition identity. No FantLab linguistic result attributable specifically to this translation was located in this unit.

`fantlab_source_edition_match=unknown`, `diagnostic_ready=false`, `gate_ready=false`, `m2_parity_admissible=false`; M2 remains 0/5.

## Next action

A later independent wake must review the final exact head of Draft PR #140 after all workflows settle, inspect the extraction contract, source-free replay evidence, public/provenance synchronization and corpus-admission boundary, and merge only if no blocker is found. The authoring wake deliberately does not mark Ready or self-merge.
