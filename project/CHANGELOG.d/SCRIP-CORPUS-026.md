# SCRIP-CORPUS-026 — Beketova translation literary-body freeze

Date: 2026-09-19
Issue: #139
PR: #140

- Continued the retained `verne-children-captain-grant-beketova-ru` translation rather than adding another trace-only candidate.
- Replayed exact Russian Wikisource revision `oldid=5304880` and established that its observed source is a direct one-page transcription rather than the generic `<div class="text">` shape: 11,028 lines, source/title scaffold through line 36, three level-3 part headings, 140 level-4 literary headings, and eight trailing category lines.
- Added candidate-specific fail-closed extraction profile `scriptorium-beketova-captain-grant-wikisource-body-v1`. It binds the exact observed scaffold/heading/category topology, rejects unsupported in-body template/tag/external-link/table drift, renders only the bounded supported visible markup through the shared extraction layer, and never persists source prose.
- Hosted bootstrap run `35425350073`, job `105850213235`, on exact head `a6793410a3addc18afd895c5f490ddc9689f6492` completed successfully with **271 standard-library tests**. It re-fetched and replay-verified the exact revision identity, captured the literary-body identity, verified the source-free boundary and uploaded source-free evidence.
- Frozen literary body: **1,095,467 characters including spaces**, **2,040,240 UTF-8 bytes**, raw SHA-256 `4931eba535a4ef3989ac905d895258f00db57029e488d98511db50a7ce4d1161`; `scriptorium-text-v1` normalization preserves the same count and SHA-256.
- The exact body therefore clears the repository >=300,000-character rule and is admitted for general Scriptorium calibration/profile use. This is not FantLab parity admission.
- Reconciled the structured trace, dedicated candidate page and corpus-root navigation around the frozen body and translation identity. No book text is committed.
- No FantLab linguistic result or analyzer-input/source-edition identity is established for this specific Beketova translation. `fantlab_source_edition_match=unknown`, `diagnostic_ready=false`, `gate_ready=false`, `m2_parity_admissible=false`; M2 remains 0/5.
- PR #140 remains Draft for independent later exact-head review and safe merge; this authoring run does not self-approve or merge it.
