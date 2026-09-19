# Run receipt — SCRIP-CORPUS-030

Date: 2026-09-19
Issue: #147
Pull request: #148 (`scrip-corpus-030-darwin-rachinsky-1864`)
Mode: normal-flow P2 corpus/provenance diversification

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

## Verification and handoff

The committed JSON is source-free structured metadata and encodes the strict freeze/admission boundary. The public candidate note and corpus documentation repeat the same non-promotion rule. Draft PR #148 is intentionally left for a later independent exact-head review. That review must inspect the final diff and workflows, verify that no source prose/scan bytes were committed, confirm that page count is not promoted into threshold evidence, and preserve the Rachinsky-vs-Timiryazev/FantLab boundary before any merge.
