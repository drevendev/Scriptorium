# Corpus candidates

This directory stores **metadata and derived identity only**, not book text. Candidate admission follows the repository corpus rule: a calibration/benchmark work must have at least 300,000 characters including spaces and a documented legal basis. A legally usable public transcription is not automatically the text FantLab analyzed; source identity and parity remain separate claims.

## Anna Karenina diagnostic candidate

`tolstoy-anna-karenina-ru` now has a reproducibly frozen Russian Wikisource/FEB candidate. The committed revision manifest records all 239 chapter revision IDs, revision timestamps, MediaWiki SHA-1 identities, the deterministic `scriptorium-wikisource-body-v1` extraction contract, the `scriptorium-wikisource-composite-v1` composition order, and composite hashes. No source prose is committed.

The frozen composite contains **1,705,605 characters including spaces** and has raw and `scriptorium-text-v1` normalized SHA-256 `1dcf2af815f6288099f77a038d873690fb0dc72edf81d2094fd29f3d5a30c205`. FantLab displays **1,692,647 characters** for its 2022 analysis, a difference of **12,958 characters**. That difference is diagnostic evidence only: FantLab does not disclose the edition or bytes of its uploaded analyzer input, and its display/counting normalization may also differ.

Therefore the candidate is ready for a **diagnostic field-by-field comparison**, but `fantlab_source_edition_match` remains `unknown`, it is not M2 parity evidence, and the reproduction gate remains **0/5 source-matched works** until independent evidence ties FantLab's analyzer input to the same frozen source.

Canonical evidence:

- `source-edition-traces/tolstoy-anna-karenina-ru.json` — provenance, legal/source boundary, admissibility and next evidence.
- `source-edition-traces/tolstoy-anna-karenina-ru.revisions.json` — packed source-free 239-revision identity and composite hashes.
- `../../scriptorium/wikisource_freeze.py` — deterministic fetch/extraction/composition implementation.
