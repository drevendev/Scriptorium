# Candidate: Fyodor Dostoevsky — *Humiliated and Insulted* (1861), Russian original

**State:** executable, revision-pinned **measurement proposal**, not an admitted tenth measured work. Until the hosted exact-source replay succeeds, both the extracted literary length and all numerical values are **NOT_RUN**. No FantLab input identity or parity is claimed.

## Source and rights

- Original Russian novel: **Фёдор Михайлович Достоевский, «Униженные и оскорбленные»** (1861); author died in 1881.
- [Russian Wikisource permanent oldid=5611473](https://ru.wikisource.org/w/index.php?title=Униженные_и_оскорбленные_(Достоевский)/Версия_2&oldid=5611473), last modified 2025-08-29, identifies az.lib.ru as the imported source and expressly marks the original-language text public domain in Russia and life+70 jurisdictions. A separate print-edition collation has **not** been performed.
- The rendered permanent revision visibly contains four parts, 15/11/10/9 numbered chapters, an epilogue and a distinct **Комментарии** section. Editorial comments are **excluded** before measurement; the module also verifies the novel's opening and final-epilogue anchor.
- Exact raw wikitext and normalized literary-body hashes are computed by hosted replay and must be retained along with revision/page identity **before** counting this as measured work. Neither hash is invented from HTML snippets or metadata.

## Executable measurement

```sh
python -m unittest discover -s tests -p test_humiliated_diagnostic.py -v
python -m scriptorium.humiliated_diagnostic --output /tmp/humiliated-measured.json
```

The executable uses the existing MediaWiki exact-revision client and deterministic 29-field analyzer. It fail-closes on revision identity, public-domain notice, bibliographic anchors, missing/reordered chapter inventory, editorial-commentary boundary, size below 300,000 characters including spaces, unexpanded markup and unexpected metric/profile changes. Create-only output includes **derived metrics, source identities/digests, units, versioned profiles and explicit NOT_RUN** for the five dictionary-dependent fields; it never writes prose to the repository or Pages.

The dedicated GitHub Actions workflow retains only derived JSON for independent verification. If the current parser fails against the oldid's actual wikitext, record the concrete safe structural error and fix this **same branch** before declaring the work measured; do not relax safety/source gates or publish fabricated counts. The public Reader's nine measured works are unchanged by this proposal. FantLab analyzer input **UNKNOWN**, numeric comparisons **DIAGNOSTIC_ONLY**, **M2 0/5**.
