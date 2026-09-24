# Darwin/Rachinsky 1864 — `{{ё}}` controlled output replay

This source-free companion is the successor to the reviewed three-node dependency closure in `darwin-origin-species-rachinsky-1864-ru-template-yo-direct-dependencies.md`. It narrows one unresolved renderer question: whether zero-argument `{{ё}}` produces the documented lowercase outputs under the exact dependency identities selected by Scriptorium.

## Replay boundary

The reviewed predecessor contract binds exactly:

```text
Шаблон:Ё@5687302 -> Шаблон:ЕЁ@3684646 -> Модуль:String@3684569
```

MediaWiki `revid` is **not** used as a recursive dependency selector. Instead, exact-head CI opens an identity-stable provider window: immediately before any expansion it requires the current Russian Wikisource revisions of all three recursively discovered nodes to equal those reviewed identities; after both mode replays it performs the same check again. Any revision drift fails closed.

The replay then calls `action=expandtemplates` only as the renderer for `{{ё}}`, twice per mode. The forced context is `О происхождении видов (Дарвин; Рачинский)/1864 (ВТ:Ё)` and the non-forced context is `О происхождении видов (Дарвин; Рачинский)/1864`. These contexts deliberately avoid `SUBPAGENAME=ВТ:Ё`, so the selected `Модуль:String` path is exercised rather than bypassed.

Semantic output identity is defined as Unicode NFC followed by removal of surrounding Unicode whitespace. The committed v6 contract freezes the documented single-character targets and their UTF-8 SHA-256 identities:

- forced yoification: `ё`, SHA-256 `30fbc377ae9122edc2cdbed70b9261817d196eca8db96ac8bfa4cfaf412667ac`;
- non-forced yoification: `е`, SHA-256 `259f56cb715ba3a3f1ca41a4ff1972cca698cb49eef1ae018dff325507da8b26`.

Canonical source-free successor:

- [`source-edition-traces/darwin-origin-species-rachinsky-1864-ru.template-yo-replay-contract-v6.json`](source-edition-traces/darwin-origin-species-rachinsky-1864-ru.template-yo-replay-contract-v6.json)
- schema: `scriptorium-darwin-template-yo-replay-contract-v6`
- contract SHA-256: `c317eb5247701f0ad860811e9349f4e6f42274e72e8856eecb8a9aff610f988f`
- builder/validator: [`../../scriptorium/darwin_template_yo_replay_contract_v6.py`](../../scriptorium/darwin_template_yo_replay_contract_v6.py)
- exact-head replay workflow: [`../../.github/workflows/darwin-template-yo-output-replay.yml`](../../.github/workflows/darwin-template-yo-output-replay.yml)

## What this can and cannot prove

A successful exact-head replay verifies the two zero-argument semantic outputs for this selected snapshot while the provider's recursively discovered current dependency identities are exactly the reviewed v5 graph. It does **not** prove which template/module revisions were historically transcluded when the 1864 Page transcriptions were saved, and it is not a general offline or permanently version-pinned MediaWiki runtime.

This unit deliberately stops before render-profile mutation. Even after output replay succeeds, `render_profile_rule_promoted=false` and `backlog_item_removed=false`; changing the frozen 388-Page render decision profile and semantic backlog is a separate bounded judgement unit. Complete renderer semantics, renderer implementation, inter-page composition, literary-body identity, the >=300k admission check, FantLab input identity and M2 parity remain closed. M2 remains **0/5**.

No Page prose, template source, Lua source, rendered literary prose, OCR or scan bytes are committed. The workflow uploads only the deterministic v6 contract plus a compact source-free replay receipt for later independent review.
