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

## Resurrection diagnostic candidate

`tolstoy-resurrection-ru` is now a second reproducibly frozen public-domain candidate. Russian Wikisource identifies Alexey Komarov's library as its transcription source; Komarov's source page completes the citation as **L. N. Tolstoy, Collected Works in eight volumes, volume 6, Moscow: Lexika, 1996**. The work has **59 + 42 + 28 = 129 chapters**, and the committed source-free manifest pins every chapter revision ID, revision timestamp and MediaWiki SHA-1 identity in deterministic part/chapter order.

The frozen extraction uses the explicit `scriptorium-wikisource-resurrection-body-v1` contract because the source set contains two observed page shapes: some chapters wrap prose in one or more `text`/`indent` divs, while others place prose directly after the `Отексте` header. Exact-revision replay reconstructs a **890,835-character** composite with raw and `scriptorium-text-v1` normalized SHA-256 `2725a60a810d8aae4beff9dbc73ff85cf6da066b1c5272aaebf21addbe4ccaa0`. No source prose is committed.

FantLab's 19 September 2022 analysis displays **881,244 characters** and **126,457 words**, a character-count difference of **9,591** from this frozen public candidate. That difference is diagnostic-only: FantLab still discloses neither the analyzer-input edition nor immutable bytes, and its TXT excerpt link is not source-match evidence. `fantlab_source_edition_match` therefore remains `unknown`; the candidate may now support source-frozen diagnostic comparisons but not M2 parity evidence, so the reproduction gate remains **0/5 source-matched works**.

Canonical evidence:

- `source-edition-traces/tolstoy-resurrection-ru.json` — provenance, legal/source boundary, frozen identity and admissibility.
- `source-edition-traces/tolstoy-resurrection-ru.revisions.json` — compact source-free 129-revision identity and composite hashes.
- `../../scriptorium/resurrection_freeze.py` — versioned source-specific extraction and exact-revision replay implementation.

## Brothers Karamazov traced candidate

`dostoevsky-brothers-karamazov-ru` now has a strong bibliographic trace but is **not yet frozen for full-work diagnostics**. FantLab's 18 September 2022 analysis reports **1,807,107 characters** and **281,507 words**. Russian Wikisource identifies its public-domain transcription as Dostoevsky's **Collected Works in 15 volumes, Leningrad: Nauka, 1991, volumes 9-10** and links the Russian Virtual Library electronic edition. RVB independently confirms that volume 9 contains parts I-III and volume 10 contains part IV plus the epilogue, under the same 1991 Nauka edition.

The Wikisource work index has permanent revision `oldid=5616907`, but that revision does **not** freeze the novel bytes. Individual content pages have their own revisions; sampled Book I, Chapter I exposes independent revision `oldid=1224742`. The index lists an author preface, twelve books across four parts, and 96 numbered chapter/epilogue leaves, but a later freeze must verify the exact text-bearing inventory, page shapes, extraction rules and composition before recording composite hashes. The sampled chapter also reports no reviewed version, so transcription QA is kept separate from the otherwise strong bibliographic provenance.

FantLab's current TXT excerpt route redirects to a LitRes trial endpoint (`art=171949`). That route is recorded only as negative source-identity evidence: neither the excerpt nor the listed edition proves which uploaded bytes FantLab analyzed. Therefore `fantlab_source_edition_match=unknown`, `diagnostic_ready=false`, `m2_parity_admissible=false`, and M2 remains **0/5 source-matched works**.

Canonical evidence:

- `source-edition-traces/dostoevsky-brothers-karamazov-ru.json` — Wikisource/RVB/Nauka bibliographic chain, permanent-index boundary, legal basis, non-frozen structure and exact next evidence.
