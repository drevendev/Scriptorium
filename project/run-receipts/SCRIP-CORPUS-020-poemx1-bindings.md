# Run receipt — SCRIP-CORPUS-020 concrete `poemx1` invocation bindings

- Issue: #109
- Draft PR: #115
- Branch: `scriptorium/scrip-corpus-020-poemx1-bindings`
- Base `master`: `ae8fa2944ca60432589def4dc0f5804feb16795e`
- Unit class: corpus / provenance / MediaWiki historical-expansion reconstruction
- Benchmark movement: none; M2 remains 0/5 source-matched works

## Bounded unit

Source-freeze the six concrete `poemx1` invocation argument/frame bindings in pinned Klim Samgin Part 2 dependency oldid `2366546`, binding only the observed call shapes to the already-frozen literal `Poemx1` parameter surface. Do not recursively expand inserted argument wikitext, execute parser functions, render `#tag:poem`, infer historical render equivalence, resolve Part 2, or create a literary-body digest.

## Produced

- `scriptorium/mediawiki_template_invocation.py` — conservative source-free template-call binding model for this bounded layer.
- `tests/test_mediawiki_template_invocation.py` — synthetic regression coverage for anonymous/named numbering, whitespace, duplicates, nested pipes, fail-closed dynamic names, source-free identities and dependency digest drift.
- `.github/workflows/klim-samgin-template-bindings.yml` — exact-head replay that re-fetches oldid `2366546`, verifies its frozen identity, regenerates binding evidence and byte-compares it to the committed manifest.
- `corpus/candidates/source-edition-traces/gorky-klim-samgin-ru.poemx1-template.bindings.json` — source-free concrete invocation/frame evidence.
- Public candidate and machine-readable provenance surfaces updated to expose the new boundary without source prose or parity claims.

## Exact-source discovery

The six real calls all have the same binding shape:

- exactly two anonymous arguments and zero named arguments;
- parameter `1` is explicitly defined empty in all six;
- parameter `2` is defined and non-empty in all six;
- `3`, `fixed`, `poem`, `small`, and `width` are omitted in all six;
- no duplicate assignments;
- no effective binding names outside the frozen template parameter surface;
- 12 assignments total.

Invocation SHA-256 identities, in source order:

1. `0f09f7a30447022f3fda19c24f159fa234f09d06d127e5d222ed1d7b4e0f6112`
2. `f4c7e9828d49f1c6fe38774eaa2133af3a2dd495164492e1b91605519361993d`
3. `0331a13a921cdf3f49a1b4f634cf00fc11c0abdc61f79bd108f78eb0e3dd4f16`
4. `cf4eab4577e2ac2bc9dcd09835875411734ab9d5abb41c8f2be327757f278aa6`
5. `9bb1d32c5d20c4e151c290190458be336cc22c91921029057dc8dea5cbacd81b`
6. `a0d6aaed7764c3239b7ca3af7b40bb6f697ec4d1a27632f2848ee0db3aa98b26`

The committed artifact stores offsets, counts and digests only; literary argument prose is not committed.

## Verification history

The first authored-head dedicated workflow, run `35261242215` on `3369b4c496e6c218f85d6fcb21a05c665475328a`, passed **213 standard-library tests**, re-fetched and verified exact dependency oldid `2366546`, and successfully generated the source-free manifest. Its final comparison failed intentionally because no expected binding artifact had yet been committed; that generated evidence was the source of the committed artifact.

After committing the generated record, dedicated run `35261480315` on `f2c9ccc9ca6e2060055ef8410691f20f9b91d7c1` completed successfully and byte-compared the fresh exact-source generation to the committed manifest. Pages run `35261480309` on the same head also completed successfully.

Final exact-head verification after durable-state reconciliation is recorded in PR #115 without changing the code head.

## Boundary / next trigger

PR #115 remains Draft for an independent later-run review and must not be self-merged by this authoring run. Issue #109 remains open.

After a clean independent review/merge, continue the historical MediaWiki layer under the now-frozen frame shape: parameter `1` defined empty, parameter `2` defined non-empty, all other observed surface names omitted. Reproduce only the evidenced `#expr`, `#if`, `#ifeq`, `#iferror`, and `#tag:poem` behavior while keeping recursive inserted-value semantics and the inferred historical-template anchor explicit. Do not claim resolved Part 2 bytes until that expansion replays deterministically.

`fantlab_source_edition_match=unknown`, `diagnostic_ready=false`, `gate_ready=false`, `m2_parity_admissible=false`.
