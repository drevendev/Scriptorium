# SCRIP-CORPUS-028 — Running on Waves literary-body freeze

- Recovered Draft PR #144 after its required candidate workflow failed closed on source-observed Wikisource templates.
- Added source-free CI diagnostics that enumerate only template names/arities and synthetic expansion behavior, never literary prose; pinned workflow actions by exact commit SHA.
- Added candidate-specific fail-closed rendering for only the template shapes observed in the 36 exact pinned 1965-source revisions: numeric `roman`, zero-argument `^`, bounded `poem1`, `razr`/`razr2`, combining acute/grave marks, `Так в тексте`, and corrected-text `опечатка2`. Unobserved names/shapes remain rejected.
- Defined the literary-body composition as exact frozen route order `/1` through `/35`, then `/Эпилог`, separated by two newlines. Plain observed `<poem>` wrappers are treated as layout only after bounded `poem1` reduction.
- Live source-free capture produced a 36-page composite of **363,819 characters including spaces / 656,239 UTF-8 bytes**, raw and `scriptorium-text-v1` normalized SHA-256 **`41a1ada3caabea2909976372ca6312fb8a478f2d0d87c088f304fcb30c52fdbc`**. The body clears the >=300k general calibration/profile threshold.
- Committed the exact source-free per-page/composite identity as `corpus/candidates/source-edition-traces/grin-running-on-waves-ru.literary-body.json`; no literary text is committed.
- Reconciled the candidate page and structured provenance. FantLab's displayed count is 360,987 characters, **2,832 lower** than the frozen public candidate, but `fantlab_source_edition_match=unknown`, `diagnostic_ready=false`, `gate_ready=false`, `m2_parity_admissible=false`; M2 remains **0/5**.
- The distinct Wikisource `/Версия 2` (`az.lib.ru` / Pravda 1980) remains excluded and non-composable with the retained Detskaya literatura 1965 route.
- Substantial authored PR #144 remains Draft for independent exact-head review; this run does not self-approve or merge it.
