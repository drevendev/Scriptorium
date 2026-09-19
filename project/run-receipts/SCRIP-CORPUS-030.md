# Run receipt — SCRIP-CORPUS-030

Date: 2026-09-19
Issue: #147
Pull request: #148 (`scrip-corpus-030-darwin-rachinsky-1864`)
Mode: normal-flow P2 corpus/provenance diversification, followed by independent recovery/review

## Selected bounded unit

Register a source-free provenance slice for Charles Darwin's *On the Origin of Species* in Sergey A. Rachinsky's 1864 Russian translation, deliberately adding nonfiction/history-of-science diversity without claiming corpus admission, a frozen literary body, or FantLab parity.

## Evidence captured

Russian Wikisource identifies the retained family as **Ч. Дарвин. О происхождении видов**, translated by **Сергей Александрович Рачинский**, Saint Petersburg: **Издание книгопродавца А. И. Глазунова**, **1864**, **399 pages**.

Two permanent source-free route/bibliographic anchors are recorded:

- rendered edition-family parent `О происхождении видов (Дарвин; Рачинский)/1864 (ВТ:Ё)`, `oldid=5628021`;
- ProofreadPage index `Индекс:Дарвин - О происхождении видов, 1864.djvu`, `oldid=4494408`.

The ProofreadPage surface reports `Закончено — Все страницы вычитаны и проверены`. That is retained as source metadata/quality evidence only. It does not identify one immutable literary byte stream by itself.

The retained Wikisource work surface explicitly declares the work public domain in Russia and life-plus-70-or-less jurisdictions and states that, for a translation, exclusive rights have expired for all original/translation authors. This receipt records that source declaration as provenance evidence rather than independent legal advice.

FantLab work `969964` confirms a work-level entity for Darwin's 1859 monograph, but the currently exposed Russian translation is **K. Timiryazev**, not Rachinsky. No FantLab `/lp` result attributable to this Rachinsky translation or analyzer-input/source-edition identity was established.

## Durable result

- Added `corpus/candidates/darwin-origin-species-rachinsky-1864-ru.md`.
- Added `corpus/candidates/source-edition-traces/darwin-origin-species-rachinsky-1864-ru.json`.
- Added a Darwin/Rachinsky diversification section to `docs/CORPUS_CANDIDATES.md`.
- Added the semantic changelog fragment and advanced `STATE_AND_QUEUE` to revision 169 with independent exact-head review of Draft PR #148 as P0.
- No literary prose, Page-namespace source content, scan bytes, or OCR are committed.

## Freeze boundary

Frozen/retained at this stage:

- Rachinsky 1864 / Glazunov translation-edition identity;
- rendered parent revision locator `oldid=5628021`;
- ProofreadPage index revision locator `oldid=4494408`;
- displayed 399-page bibliography;
- observed completed-proofread status;
- explicit source rights statement for the work/translation.

Still unfrozen:

- exact revision identities of Page-namespace inputs used by the retained route;
- DjVu/PDF binary byte stream and digest;
- OCR/Page-markup extraction behavior;
- deterministic literary extraction/composition contract;
- literary-body character count plus raw/normalized digests;
- FantLab analyzer-input/source-edition identity.

## Corpus and gate status

The displayed **399 pages do not prove the >=300,000-character repository threshold**. No literary-body character count has been frozen, so this trace is retained as a high-value diversification lead but is **not admitted** to calibration/profile corpus yet.

- `admitted_for_calibration=false`
- `fantlab_source_edition_match=unknown`
- `diagnostic_ready=false`
- `gate_ready=false`
- `m2_parity_admissible=false`
- M2 remains **0/5 source-matched works**

## Independent exact-head review

A later run reviewed final authored head `dc58cd10574371e03b19481d2813d55208bc3060` against unchanged `master` base `17d78d5fd32ae24dc1e73aa529ad5995b5a6322a`.

- Compare result: 6 commits ahead / 0 behind; PR mergeable.
- Inline review threads: none.
- Exact-head workflows: all 13 pull-request-triggered runs completed successfully, including `Scriptorium Pages` run `35447501952`.
- `Scriptorium Pages` job `105908865130` checked out the exact head, ran the standard-library suite, built the canonical static site, verified deterministic rebuild, and uploaded the Pages artifact.
- Pages artifact `10585476252` has SHA-256 `9f4eaff8707c5378c88e1f4b63d243013dc65f9a8c417ba48b3aaa27a051d3fa`; independent artifact inspection found no Darwin/Rachinsky literary prose.
- Fresh source checks independently reconfirmed the Rachinsky/Glazunov 1864 bibliography, completed ProofreadPage status and explicit public-domain statement on Russian Wikisource.
- Fresh FantLab verification reconfirmed that work `969964` currently exposes a K. Timiryazev Russian translation, not Rachinsky.
- No blocking defect was found. The strict non-promotion boundary remains intact.

PR #148 was marked Ready and squash-merged as `e5fefb15d74fcd30786e2897a9900cfe47371032`; Issue #147 closed completed. M2 remains 0/5.
