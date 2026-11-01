# Robinson Crusoe — two attributed Russian translation witnesses

**SOURCE SCREENING ONLY (2026-11-01): NOT a measured comparison, corpus admission or FantLab parity.** Exact Wikisource revision pointers are confirmed; source wikitext/body bytes, SHA-256 and counts have NOT_RUN status.

## Evidence-backed source identities

| Witness | Edition and source | Scope / legal evidence |
| --- | --- | --- |
| **Yakov I. Trusov** (translation first published **1762–1764**) | Translation **from French**, in historical Russian orthography; **Imperial Academy of Sciences, St Petersburg, second edition 1775, vol. 1**. [Exact revision 5041937](https://ru.wikisource.org/w/index.php?oldid=5041937). | This source page declares **PD-old-70** for original and translation. It concludes the **first Robinson narrative**; 1775 **vol. 2** is a continuation and **must not** be appended to inflate the first-book body. |
| **Maria A. Shishmareva** (Wikisource displays **1928-12-22** for translation publication) | Russian translation associated with the English original; **ACADEMIA, Moscow–Leningrad, 1935, vol. 1**, edited by A. Frankovsky. [Exact revision 5634933](https://ru.wikisource.org/w/index.php?oldid=5634933). | Wikisource explicitly states that rights of original and translation have expired in Russia/life-plus-70 jurisdictions. **Exclude** separate editorial foreword and later volumes. |

The [Wikisource list of translations](https://ru.wikisource.org/w/index.php?oldid=5217952) separately lists Trusov, Langen, an anonymous 1880 version and Shishmareva. An **anonymous translator** does not satisfy the identified-translator goal; Langen's 1811 rendering also has a different, condensed narrative scope. Do not silently substitute them by matching a title.

**Scientific confounders:** Trusov used a **French intermediary**, unlike the English-original Shishmareva witness. Historical vs modern orthography, possible abridgment and editorial choices also affect lexical/sentence distributions. Without aligned coverage, even a future pair of valid measurements is **diagnostic**, not proof of intrinsic translator style. No FantLab analyzer-input identity was established.

**Rights limit:** The cited Wikisource pages make the described public-domain claims and indicate CC BY-SA terms for contributed site material. This is source evidence, not independent legal advice or a license for later edited modern editions. No full literary text may be committed to GitHub or Pages.

## Required executable checks before catalogue admission

1. Obtain **exact revision** bytes via an allowed MediaWiki source endpoint, recording provider SHA-1 when available, byte length, raw SHA-256 and tool versions. A rendered browser excerpt is not a source hash.
2. Freeze **body-only** extraction independently for each edition, failing closed on templates/markup and excluding Trusov vol. 2 and Shishmareva's editorial foreword; record raw/normalized SHA-256, exact character counts **including spaces**, and deterministic replay tests.
3. Verify **>=300,000 characters for EACH** separate translated body and document rights/edition identity before calibration admission. Neither character threshold nor body coverage is verified here.
4. Only then run the 29 deterministic metrics and source-free comparison with explicit intermediary/orthography caveats. No FantLab parity weight without independent analyzer-input identity. **M2 stays 0/5.**

Machine-readable record: [`source-edition-traces/defoe-robinson-crusoe-translation-pair-ru.json`](source-edition-traces/defoe-robinson-crusoe-translation-pair-ru.json). **No Reader measured-book card should be added from this screening alone.**


## Source-free exact-oldid inventory probe

A bounded first experiment is now implemented in
`scriptorium.robinson_revision_probe`. It requests exactly the two pinned
MediaWiki revisions by ID, verifies their returned IDs, timestamps and provider SHA-1,
then records wikitext SHA-256/byte count and an aggregate markup/transclusion inventory.
Only source-free JSON is written; no chapters, source prose or user manuscripts are
uploaded. Reproducible command (requires ordinary MediaWiki access):

```sh
python -m scriptorium.robinson_revision_probe \
  --screening corpus/candidates/source-edition-traces/defoe-robinson-crusoe-translation-pair-ru.json \
  --output build/repro/robinson-translations.revision-inventory.json
```

The scoped GitHub Actions workflow uploads only the derived inventory for inspection.
The existence of that workflow is not proof that its live fetch succeeded. The
wikitext length is **not** a body count; an oldid may reference an index or depend
on non-frozen transclusions. Independently inspected original narrative boundaries,
body hashes, >=300,000-character checks, measurements and parity all remain
**NOT_RUN** pending actual output and a separate fail-closed extraction contract.


### Verified exact-revision topology (GitHub Actions, 2026-11-01)

The scoped [CI run 41333954878](https://github.com/drevendev/Scriptorium/actions/runs/41333954878)
successfully fetched both oldids using the official MediaWiki API. The
[source-free replay inventory](source-edition-traces/defoe-robinson-crusoe-translation-pair-ru.revision-inventory.json)
records their provider SHA-1 and exact wikitext SHA-256; the workflow now
compares the live inventory byte-for-byte with this committed evidence.

| Exact revision | Revision wikitext (characters / UTF-8 bytes; **not book size**) | Observed structure | Immediate extraction consequence |
| --- | ---: | --- | --- |
| Trusov **5041937** | **1,516 / 2,397** | **1** `<pages>` tag, **2** template openers | The pinned top-level revision is only a small transclusion carrier; first map and freeze the scan-backed Page/Index dependency graph. Its **literary-body size is unknown**. |
| Shishmareva **5634933** | **575,223 / 1,036,654** | **0** `<pages>` tags, **19** template openers | A substantial single-revision wikitext body exists, but front matter, 19 templates and volume scope need an independently verified extraction contract. **575,223 is not an admitted literary-character count**. |

These observations separate the two executable paths: test Shishmareva's
literary boundary/markup and provenance first; scope Trusov's independent
historical scan/Page dependencies without making that difficult path a
prerequisite for measuring other eligible translations. Both bodies remain
**NOT_RUN** for extraction, SHA-256, >=300k and 29-metric analysis. M2 stays 0/5.
