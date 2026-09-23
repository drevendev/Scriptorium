# SCRIP-CORPUS-070 run receipt

## Selection

- Mode: corpus / provenance research within the P2 SCRIP-CORPUS continuation.
- Base: `master@85a4ce4d6855dbe3c3b2ce1c31871fe4c47e2a9a`.
- Issue: #229 (open).
- Pull request: #230 (Draft; independent review/merge pending).
- Reason: the rolling queue explicitly prioritizes diversity beyond 19th-century Russian classics, and the retained Perelman 1913 candidate is a legally explicit popular-science/nonfiction lead whose FantLab catalogue identity existed without durable evidence about the current work-specific linguistic-analysis surface.

## Research observation

- Re-read FantLab work `191634` (`Занимательная физика. Книга 1`) on the current first-party work page on 2026-09-23.
- The target page exposes neither the `Лингвистический анализ текста` block nor the `подробные результаты анализа` link.
- Positive control FantLab work `13729` (`Час Быка`) exposes both markers and links to `https://fantlab.ru/work13729/lp`.
- The linked positive-control analysis is dated 18 September 2022 and reports 877,398 characters, confirming that the observation method can see FantLab's published analysis surface when it is present.
- This is dated negative public-surface evidence only; it does not prove that FantLab never analyzed Perelman work `191634` or that no non-linked/private result exists.

## Produced

- Added source-free machine evidence `corpus/candidates/source-edition-traces/perelman-entertaining-physics-book1-1913-ru.fantlab-analysis-surface.json`.
- Canonical payload SHA-256 excluding the self-digest field: `f903653e799f0797d661208cbb5d06658fea275cab95d2c1c8ca586042165b9f`.
- Added public companion `corpus/candidates/perelman-entertaining-physics-book1-1913-ru-fantlab-analysis-surface.md`.
- Added this run receipt, changelog fragment and durable state handoff.

## Decision / gates

- Perelman 1913 remains a public-domain popular-science/nonfiction corpus/provenance/showcase lead.
- It is not a current M2 parity seed because no work-specific FantLab linguistic-analysis result is established on the observed first-party surface.
- `fantlab_source_edition_match=unknown`
- `diagnostic_ready=false`
- `m2_parity_admissible=false`
- literary-page selection remains unbound
- PDF↔DjVu equivalence and OCR correctness remain unproved
- literary body remains unfrozen and selected-body >=300k remains unproved
- FantLab analyzer-input identity remains unknown
- M2 remains 0/5

## Handoff

PR #230 stays Draft. A later wake should independently review the exact final PR head, recompute the canonical payload digest, verify that the positive-control/negative-target distinction is accurately represented, ensure no source prose or parity promotion slipped in, inspect settled checks, and merge only if the fail-closed boundaries remain intact.
