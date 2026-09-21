# SCRIP-CORPUS-048 run receipt

- Unit: `SCRIP-CORPUS-048`
- Issue: #183
- Pull request: #184 (Draft; authored in this run and intentionally left for independent later review)
- Base: `master@c2bb1bfe693867b44f8a6bf48e94e0a31cee99ad`
- Authored branch: `scrip-corpus-048-template-dependency-model`
- Pre-receipt authored head: `76f54850bdcd24771ae2dd081a3c632a3b19257a`
- Exact final PR head and settled CI/artifact evidence are recorded in the PR handoff comment after the final commit.

## Decision advanced

Official MediaWiki rendering/transclusion documentation corrects the prior research prerequisite for Darwin/Rachinsky `{{ё}}`: an old Page `oldid` fixes the Page revision/wikitext identity, but it does not pin historical template revisions for the rendered view. The dependency identity that matters to a deterministic replay is the exact template graph used by the chosen replay environment, unless Scriptorium deliberately supplies its own version-pinned expansion mechanism.

Source-free evidence is pinned to:

- MediaWiki `Help:History`, permanent revision `oldid=8524540` (2026-07-25);
- MediaWiki `Transclusion/en`, permanent revision `oldid=8551508` (2026-08-09), including the versioned-transclusion gap reference `T31051`;
- Russian Wikisource `Шаблон:ЕЁ/Документация`, `oldid=5090323`;
- Russian Wikisource `Справка:Вычитка`, `oldid=5731079`.

The deterministic evidence artifact is advanced to schema `scriptorium-darwin-template-yo-documentation-evidence-v2`, canonical SHA-256 `d92bdfcad71aaa8a50f9f35b5b1ada462ed41619400c40576d0603cf154877dc`.

## Boundary preserved

`{{ё}}` remains `semantic_status=unresolved`; no render-profile row is promoted or removed from the semantic backlog. All 43 unresolved shapes remain present. The next prerequisite is to freeze exact `Шаблон:ё` / `Шаблон:ЕЁ` revisions and nested dependencies used by the selected replay environment at analysis time, or use an explicitly version-pinned expansion mechanism and validate its conditional outputs.

No Page prose, template source bodies, rendered literary prose, OCR or scan bytes were committed. `renderer_semantics_complete=false`, `renderer_implementation_ready=false`, `inter_page_composition_frozen=false`, `literary_body_count_and_digests_frozen=false`, `minimum_300k_proved=false`, `admitted_for_calibration=false`, `diagnostic_ready=false`, `m2_parity_admissible=false`, and `fantlab_source_edition_match=unknown` remain unchanged. M2 remains 0/5.

## Handoff

This run authored the substantive correction and therefore does not self-approve, mark Ready or merge PR #184. A later independent run must re-read the exact final head, inspect settled PR-triggered checks and independently verify the source-free rebuilt artifact before judgement.
