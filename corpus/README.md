# Scriptorium corpus

Scriptorium's public corpus surface stores **source-free provenance, text identities and derived analysis**, not unlicensed book text. Calibration/benchmark and author-profile admission requires an exact literary-body count of at least 300,000 characters including spaces plus a clear public-domain/open-license/permission basis.

The detailed retained-candidate catalogue is in [`candidates/README.md`](candidates/README.md). Source-free machine-readable provenance lives under [`candidates/source-edition-traces/`](candidates/source-edition-traces/).

## Translation candidates

- [`verne-children-captain-grant-beketova-ru`](candidates/verne-children-captain-grant-beketova-ru.md) — Jules Verne's *Children of Captain Grant* in Alexandra A. Beketova's Russian translation. Russian Wikisource provides a permanent Detgiz-1955 / `az.lib.ru` source witness and explicit public-domain statement covering the translation. Scriptorium replay-freezes exact revision `oldid=5304880` plus a candidate-specific fail-closed literary body of **1,095,467 characters / 2,040,240 UTF-8 bytes**, SHA-256 `4931eba535a4ef3989ac905d895258f00db57029e488d98511db50a7ce4d1161`. It therefore clears the >=300k literary-character rule for general Scriptorium calibration/profile use, while FantLab analyzer-input/source-edition identity remains unknown and contributes no M2 parity weight.
- [`darwin-origin-species-rachinsky-1864-ru`](candidates/darwin-origin-species-rachinsky-1864-ru.md) — Charles Darwin's *On the Origin of Species* in Sergey A. Rachinsky's 1864 Russian translation. The public source graph and all **418** exact Wikisource Page revision identities are source-free frozen; **388** dependencies are literary and **30** are apparatus. The backing Commons DjVu is independently frozen as 27,368,263 bytes with SHA-256 `7f3ae1aadd4a844b193783a0c350e23815a76e7bb14a92bae7fa1c077354a2c8`, but Page-wikitext rendering, literary-body counts/digests, >=300k admission and FantLab source identity remain deliberately unfrozen, so this candidate is **not yet admitted**.

Translations are always distinct work identities: translator, edition/transcription provenance, exact source digest and derived analysis belong to that translation, not to the source-language work or to other translations.

## Modernist source candidates

- [`bely-petersburg-1916-ru`](candidates/bely-petersburg-1916-ru.md) — Andrei Bely's *Petersburg* in the **1916 first book edition**, kept distinct from the materially revised 1922 edition. Scriptorium independently streams and replay-verifies the exact public-domain Wikimedia Commons facsimile as **3,621,459 bytes**, SHA-1 `682476934dd6ed49c6bbcdb0720127c1812ff477`, SHA-256 `b08820ad1339894c6d20fbaa2367c11385492bf376d199f8de23c859ef6ddef5`. No PDF, OCR or literary source text is stored. OCR/extraction, literary-body count/digests, >=300k admission, FantLab source match and M2 parity remain open.
