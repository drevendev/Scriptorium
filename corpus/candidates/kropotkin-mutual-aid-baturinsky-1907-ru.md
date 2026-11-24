# Kropotkin — Mutual Aid, Baturinsky translation (1907)

Status: traced candidate; route identity capture implemented, provider execution pending. Issue #627.

## Edition and reuse

- Author P. A. Kropotkin (1842–1921), translator V. Baturinsky (1850–1930); original English. Russian edition: St Petersburg, Znanie, 1907. Do not conflate the 1902 translation publication date with the 1907 witness.
- [Work index oldid 5808217](https://ru.wikisource.org/w/index.php?oldid=5808217), modern orthography; [scan index oldid 5571086](https://ru.wikisource.org/w/index.php?oldid=5571086). The latter marks all pages proofread but not all validated. The work index explicitly marks both work and translation public domain in Russia and life-plus-70-or-less jurisdictions. Wikisource CC BY-SA and applicable reuse terms remain relevant. Publish only source-free measurements and attribution.
- Observed 2026-11-24: work index advertises preface, introduction, eight chapters, conclusion, eighteen appendices and a separate alphabetical index. The appendix routes use numbered subpages. The pinned work index actually advertises appendix III with `/ДО`, as verified by the index source and rendered link. The separate modern `/Приложение/3` page links to this historical variant. Capture both distinct revision identities, require that link from the pinned modern revision, and use only the modern route in the 29-route analysis inventory. See [index](https://ru.wikisource.org/w/index.php?title=Взаимная_помощь_как_фактор_эволюции_(Кропоткин_1907)&oldid=5808217) and [modern appendix III](https://ru.wikisource.org/wiki/Взаимная_помощь_как_фактор_эволюции_(Кропоткин_1907)/Приложение/3). The pre-reform orthography edition is a separate route, not a substitute.

## Executable preflight

`python -m scriptorium.kropotkin_revisions --output build/repro/kropotkin-route-identities.json`

Create the parent directory first. The capture checks the pinned work-index link inventory, fetches exact index revision metadata and current identities for the 29 modern prose routes plus the separately recorded historical appendix III target, excludes the alphabetical index, and records no source prose. Receipt schema v2 records the explicit route exception. The first provider run (45407909788, head 5923be1) failed the index inventory check; the revised capture must pass live CI before acceptance. It fails on absent or duplicate routes or invalid revision metadata; output is create-only. A dedicated PR workflow produces a source-free artifact for independent acceptance. Offline tests use synthetic provider records only.

Route identity is not transcluded Page/template identity: pin those dependencies and verify a deterministic literary body, including the preface, notes and appendix boundary, before measuring length. No claim of a complete body, >=300000 characters, source-matched FantLab analysis or corpus admission. The candidate does not count toward M5 or M2. The live capture has not run locally (DNS unavailable).
