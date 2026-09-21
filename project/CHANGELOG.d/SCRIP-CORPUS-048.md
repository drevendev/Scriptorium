# SCRIP-CORPUS-048 — correct `{{ё}}` oldid dependency model

- Official MediaWiki `Help:History` revision `oldid=8524540` establishes that viewing an old page revision uses current template/image versions; page `oldid` therefore freezes Page wikitext, not transcluded template revisions.
- Official MediaWiki `Transclusion/en` revision `oldid=8551508` describes transclusion as a live link and references the lack of versioned transclusion support (`T31051`).
- The Darwin/Rachinsky `{{ё}}` evidence schema is advanced to `scriptorium-darwin-template-yo-documentation-evidence-v2`, canonical SHA-256 `d92bdfcad71aaa8a50f9f35b5b1ada462ed41619400c40576d0603cf154877dc`.
- The obsolete prerequisite to look up `Шаблон:ё` / `Шаблон:ЕЁ` at retained Page-save timestamps is removed. The correct next prerequisite is an exact replay-time dependency freeze (including nested dependencies), or an explicitly version-pinned template-expansion mechanism.
- Independent review `5265215135` re-read exact head `cb725ba8f8df5cc0ebdacbf0441ff6451a1c94c0`, confirmed all 15 PR-triggered workflows `success`, independently verified artifact `10630062217`, and found no merge blockers. PR #184 was squash-merged as `634331346f1afadd26c054f9f09b6ada71d964b2`, closing Issue #183 completed.
- `{{ё}}` remains unresolved. The render profile/backlog are unchanged; renderer/body/>=300k/FantLab/diagnostic/M2 gates remain closed and M2 remains 0/5.
