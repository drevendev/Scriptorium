# SCRIP-CORPUS-049 — freeze `{{ё}}` version-pinned replay contract

- Official MediaWiki `API:Expandtemplates/ru` permanent revision `oldid=6729113` is retained as source-free API evidence: `revid` supplies revision context for `{{REVISIONID}}` and similar variables; it is not treated as a historical transcluded-template version pin.
- TemplateSandbox title/text substitution is recorded as a useful direct override but not as proof that a recursively expanded dependency graph is closed; `Help:ExpandTemplates` documents recursive expansion.
- A new fail-closed replay contract requires exact source-free identities for `Шаблон:ё`, `Шаблон:ЕЁ` and every nested template/module dependency: title, revision ID, revision timestamp and MediaWiki content SHA-1. Any live/unbound dependency keeps the closure open.
- Canonical contract schema `scriptorium-darwin-template-yo-replay-contract-v1` has SHA-256 `9ac0e52c8253ef523aefe9fd54b8e90edf69095ac6f7c45ac2a0bbd584049e2b`; this unit intentionally binds zero dependency revisions and verifies no replay outputs.
- `{{ё}}` remains unresolved. The render profile/backlog are unchanged; renderer/body/>=300k/FantLab/diagnostic/M2 gates remain closed and M2 remains 0/5.
