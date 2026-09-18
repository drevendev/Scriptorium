# Run receipt — SCRIP-CORPUS-020 body extraction surface

- Issue: #109
- Draft PR: #123
- Base revision: `78f168b86c6b7563a5f37f164b29234ddc4fc5f1`
- Selection reason: correctness/recovery prerequisite before the queued literary-body extractor. The merged Part 2 target substitution did not establish that the parent source was template-free.
- Durable artifact: `corpus/candidates/source-edition-traces/gorky-klim-samgin-ru.body-surface.json`
- Replay implementation: `scriptorium/klim_samgin_body_surface.py`
- Dedicated workflow: `Klim Samgin body extraction surface`

## Verified evidence

The exact pinned parent revisions remain Parts 1–4 at oldids `5733765`, `5198033`, `5138882`, `5724453`. Live source-free replay records seven direct parent-level `poemx1` calls: five in Part 1 and two in Part 2. Every call has two anonymous arguments, no named arguments, explicitly empty parameter `1`, and non-empty parameter `2`.

Part 2's direct calls are at parent offsets `25519..25540` and `25568..26321`; the frozen target-only `#lst` call is at `581758..581810`. They do not overlap, therefore target-only substitution preserves both direct parent calls. The existing Part 2 resolution remains valid as a target-substitution identity, but it must not be interpreted as a template-free parent or literary-body identity.

Across all four parent revisions the frozen handler surface is: `Жизнь Клима Самгина` ×4, direct `poemx1` ×7, `примечания` ×2, `Ко` ×1, target-only `#lst` ×1; HTML-tag occurrences `center` ×6, `ref` ×10, `nowiki` ×50; Part 1 level-three headings ×5; one trailing category per parent; no tables.

Initial exact-source generation run `35317530945` on `c6fe334c496bc67c71641ec09732fc1c006047c2` completed successfully, including the standard-library suite, exact four-revision replay, canonical artifact generation and artifact upload (`10534919689`). The generated source-free JSON was used as the committed evidence record and is now covered by focused tests and byte comparison in the dedicated workflow.

## Claim boundary

No source prose is committed. This unit does **not** freeze any literary body, deterministic four-part composition, raw/normalized composite digest, historical Russian Wikisource MediaWiki/Poem deployment, or FantLab analyzer-input identity. `fantlab_source_edition_match=unknown`, `diagnostic_ready=false`, `gate_ready=false`, `m2_parity_admissible=false`; M2 remains 0/5.

## Next trigger

After independent later-run review and merge of PR #123, implement fail-closed literary extraction against the frozen surface, then deterministic `1 -> 2 -> 3 -> 4` composition. The extractor must explicitly handle the seven direct parent `poemx1` calls rather than assuming PR #122 removed them.
