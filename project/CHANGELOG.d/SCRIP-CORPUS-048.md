# SCRIP-CORPUS-048 — correct `{{ё}}` oldid dependency model

- Official MediaWiki `Help:History` revision `oldid=8524540` establishes that viewing an old page revision uses current template/image versions; page `oldid` therefore freezes Page wikitext, not transcluded template revisions.
- Official MediaWiki `Transclusion/en` revision `oldid=8551508` describes transclusion as a live link and references the lack of versioned transclusion support (`T31051`).
- The Darwin/Rachinsky `{{ё}}` evidence schema is advanced to `scriptorium-darwin-template-yo-documentation-evidence-v2`, canonical SHA-256 `d92bdfcad71aaa8a50f9f35b5b1ada462ed41619400c40576d0603cf154877dc`.
- The obsolete prerequisite to look up `Шаблон:ё` / `Шаблон:ЕЁ` at retained Page-save timestamps is removed. The correct next prerequisite is an exact replay-time dependency freeze (including nested dependencies), or an explicitly version-pinned template-expansion mechanism.
- `{{ё}}` remains unresolved. The render profile/backlog are unchanged; renderer/body/>=300k/FantLab/diagnostic/M2 gates remain closed and M2 remains 0/5.
