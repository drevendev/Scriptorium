# Perelman 1913 — FantLab linguistic-analysis surface observation

Candidate: `perelman-entertaining-physics-book1-1913-ru`  
Unit: `SCRIP-CORPUS-070`  
Observation time: `2026-09-23T11:55:33Z`

## What was checked

Scriptorium re-read FantLab work `191634`, **Yakov Perelman — *Занимательная физика. Книга 1***, on the current public work page:

- https://fantlab.ru/work191634

The observed page identifies the work as a Russian-language monograph from 1913, but it does **not** expose the `Лингвистический анализ текста` block and does **not** expose the `подробные результаты анализа` link used by FantLab works with a published linguistic-analysis result.

The machine-readable source-free observation is:

- [`source-edition-traces/perelman-entertaining-physics-book1-1913-ru.fantlab-analysis-surface.json`](source-edition-traces/perelman-entertaining-physics-book1-1913-ru.fantlab-analysis-surface.json)
- canonical payload SHA-256: `f903653e799f0797d661208cbb5d06658fea275cab95d2c1c8ca586042165b9f`

## Positive control

The same observation method was checked against FantLab work `13729`, **Ivan Yefremov — *Час Быка***:

- https://fantlab.ru/work13729
- https://fantlab.ru/work13729/lp

That work page does expose the linguistic-analysis block and detailed-results link; its linked analysis surface identifies an analysis dated 18 September 2022 and reports 877,398 characters. This positive control makes the Perelman result a bounded page-surface observation rather than an inference from a failed guessed URL.

## Decision

This result strengthens, but does not broaden, the existing fail-closed boundary:

- no work-specific FantLab linguistic-analysis result is currently established for work `191634`;
- `fantlab_source_edition_match=unknown`;
- `diagnostic_ready=false`;
- `m2_parity_admissible=false` and M2 remains **0/5**;
- the 1913 Perelman edition remains valuable as a public-domain **popular-science / nonfiction corpus and showcase candidate**, not as a current M2 parity seed.

This is **not** proof that FantLab never analyzed the book. It is only a dated observation of the current first-party public work surface. A future run should re-open this question only if work `191634` gains a linguistic-analysis block/link or another first-party work-specific analysis surface is identified.

## Unchanged source/body gates

Nothing in this observation selects literary pages, proves PDF↔DjVu equivalence, validates OCR correctness, freezes a literary body, proves the selected-body `>=300,000` rule, or identifies FantLab analyzer-input bytes. The existing PDF-bound OCR/body promotion contract therefore remains unmodified and unpromoted.
