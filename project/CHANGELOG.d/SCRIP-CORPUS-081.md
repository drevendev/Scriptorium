# SCRIP-CORPUS-081 — Darwin `{{ВАР}}` documented semantics

- Selected the deterministic next Darwin/Rachinsky semantic slice from reviewed semantic-backlog-v3: template `ВАР`, 2 positional / 0 named arguments, 388 observed invocations.
- Pinned official Russian Wikisource documentation `Шаблон:ВАР/Документация@5711068`, which defines parameter 1 as pre-reform text, parameter 2 as modern text, and identifies `Модуль:Дореформенная орфография` as the implementation module.
- Pinned implementation module revision `Модуль:Дореформенная орфография@5721277`. Its `variative` path emits both variants in Page namespace; outside Page namespace it delegates title classification to `Module:Header.parse_title(..., "isPRS")` and then selects one argument.
- Added deterministic source-free builder/validator, committed evidence JSON and eight focused regressions. Evidence SHA-256: `321ced32bb7ffc75829b6fbb5255bce3243641a80c21ad4e2b7bb7a25138502d`.
- Updated the public Darwin semantic-backlog companion with the review-pending evidence boundary.
- **No promotion:** the live `Шаблон:ВАР` root, `Module:Header` revision/nested closure and candidate mainspace branch are not replay-frozen. `ВАР` therefore remains unresolved and effective backlog totals do not change.
- Issue #251; Draft PR #252. Independent review is required before Ready/merge.
- Historical transclusion, offline/version-pinned MediaWiki runtime, complete renderer/inter-page/body, >=300k, FantLab analyzer-input identity and M2 remain closed. M2 stays 0/5.
