# Run receipt — SCRIP-CORPUS-021

- Issue: #129
- Draft PR: #130
- Base: `master@b01ff06ccf29a63f524b3b0582ad27bf8b54380e`
- Unit: audit the retained *Shining World* Wikisource chapter inventory and freeze source-free identity for every existing advertised chapter target.

## Recovery

The first authored implementation assumed all 34 chapter links from the reviewed work index resolved. Its exact-head workflow correctly failed on a missing advertised target. The unit was repaired rather than bypassed: the inventory model now distinguishes `present` and `missing` titles and never invents revision metadata for red links.

## Verified source result

Dedicated run `35377889801`, job `105706840078`, checked out exact authored head `027c5d6420dedc0984e349ae7f175673feb31236`, passed **262 standard-library tests**, audited all 34 advertised titles without requesting chapter prose, and uploaded a source-free inventory artifact.

Observed inventory on 2026-09-18:

- advertised by index: 34 chapters (`16 + 11 + 7`);
- present: **19** — Part I chapters I–XVI and Part II chapters I–III;
- missing: **15** — Part II chapters IV–XI and Part III chapters I–VII;
- complete chapter-revision inventory frozen: **false**;
- source text committed: **false**.

For the 19 present pages the audit records exact revision ID, UTC timestamp and MediaWiki SHA-1. The committed artifact is `corpus/candidates/source-edition-traces/grin-shining-world-ru.source-inventory.json`. Exact-present revision replay is part of the dedicated workflow after the manifest is committed.

## Public/provenance movement

The structured candidate trace no longer says the work has 34 chapter subpages. It now distinguishes the reviewed index's 34 advertised links from the 19 existing pages and 15 missing targets, keeps the 1965 Pravda bibliographic family explicit, and forbids silent completion from RVB or another provider.

## Gate status

No FantLab source identity was established. No complete literary body or composite digest was produced. `fantlab_source_edition_match=unknown`, `diagnostic_ready=false`, `gate_ready=false`, `m2_parity_admissible=false`; M2 remains **0/5**.

## Handoff

PR #130 remains Draft for independent later-run review. Review must inspect the final exact-head workflows, confirm live inventory comparison + replay are green, and merge only if the fail-closed boundary remains intact. A later corpus unit may investigate a legally usable source-complete witness for the missing 15 chapters, but must preserve edition/provider identity instead of silently splicing texts.
