# Run receipt — SCRIP-CORPUS-017

Status: `AUTHORED_REVIEW_PENDING`

Issue: #103  
Branch: `scrip-corpus-017-klim-samgin`  
Base master: `b88162e58c45821595f5b96649eb52b1b27f7965`

## Bounded unit

Qualify Maxim Gorky's *The Life of Klim Samgin* as a twentieth-century, legally usable >=300k provenance lead, preserving the distinction between stable public locators and an actually frozen literary-body identity.

## Evidence captured

- FantLab work `427585`: linguistic analysis dated 2022-09-19, 3,789,857 characters, 531,192 words.
- Russian Wikisource work index: original Russian work marked public domain, Library Moshkov named as electronic source, four-part structure, permanent index locator `oldid=5628161`.
- Literary part permanent locators: Part 1 `oldid=5733765`; Part 2 `oldid=5198033`; Part 3 `oldid=5138882`; Part 4 `oldid=5724453`.
- Part source declarations: GIKhL collected works, Moscow, 1952 vols. 19–21 and 1953 vol. 22.

## Evidence boundary

No source prose is committed. This run does not have MediaWiki revision timestamps/SHA-1 values or Scriptorium wikitext SHA-256 values for all four part revisions, does not define deterministic literary-body extraction/composition, and has no raw/normalized composite digest. Therefore the lead is `trace_only`, `fantlab_source_edition_match=unknown`, `diagnostic_ready=false`, `gate_ready=false`, and is deliberately not added to the main parity catalog yet. M2 remains 0/5.

## Verification expected before later merge judgement

- JSON parse succeeds for the new trace.
- Repository CI/Pages checks pass on the exact PR head.
- Later independent review confirms that trace, public candidate page and durable state make no stronger identity/parity claim than the evidence supports.
