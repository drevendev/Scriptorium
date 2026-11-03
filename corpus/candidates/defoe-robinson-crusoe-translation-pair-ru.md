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

## Trusov 1775: historical Page dependency capture (PR candidate)

The pinned Trusov carrier is a 1,516-character **transclusion** page, not a
1,516-character book. `scriptorium.robinson_trusov_pages` fetches exact
`oldid=5041937` bytes, verifies them against the accepted revision inventory,
and parses exactly one unambiguous [ProofreadPage selector](https://www.mediawiki.org/wiki/Help:Extension:ProofreadPage/Pages_tag/en).
Unknown selectors fail closed instead of guessing a historical edition's coverage.
Page-namespace revisions are selected using the deterministic historical policy
**latest revision not later than carrier-save 2023-09-03 17:55:09 UTC**,
using batched current-page lookup and single-title historical fallback (required by the MediaWiki API). Only Page titles, oldids, timestamps, provider SHA-1
and selector metadata are retained; Wikisource prose stays in process memory.

```sh
python -m scriptorium.robinson_trusov_pages capture \
  --inventory corpus/candidates/source-edition-traces/defoe-robinson-crusoe-translation-pair-ru.revision-inventory.json \
  --output build/repro/trusov-1775.historical-pages.json
python -m scriptorium.robinson_trusov_pages replay \
  --inventory corpus/candidates/source-edition-traces/defoe-robinson-crusoe-translation-pair-ru.revision-inventory.json \
  --manifest build/repro/trusov-1775.historical-pages.json
```

**Scientific limit:** this as-of-save selection is a reproducible historical
hypothesis, **not** proof of MediaWiki parser-cache/render equivalence or print
edition collation. The proposed real-source workflow must successfully capture
the graph before claiming frozen Page identities. No literary-body SHA-256,
>=300,000-character admission, 29-field analysis, translation comparison or
FantLab parity is established by this tool. Volume 2 is excluded; M2 remains 0/5.

### Live graph capture verified in PR #396 (2026-11-02)

[Exact-head CI run 41375340104](https://github.com/drevendev/Scriptorium/actions/runs/41375340104)
successfully captured the pinned carrier's ProofreadPage index
**`Жизнь и приключения Робинзона Круза. Часть 1. Пер. Я. Трусовым, 1775.pdf`**
and **150 distinct Page-revision identities, pages 2–151 inclusive**.
All 150 selected Page revisions date to **2023-08-17**, earlier than the
carrier's 2023-09-03 save. The full **source-free JSON** (56,594 bytes,
SHA-256 `d2104ad33fc15ddb8479c13b9fdbe0abf94f8418e76c02261a803b79130ebaa4`)
is stored temporarily as the run's `robinson-trusov-historical-pages` artifact.
The [durable receipt](source-edition-traces/defoe-robinson-crusoe-trusov-1775-ru.page-graph-receipt.json)
preserves the checksum, selection, first/last revision identities and scientific gates.
CI checks the reproduced full graph against that checksum.

**Historical note:** this warning applied only to the early #396 draft. The full 150-Page graph is now committed in Git and checked against its receipt. None of these 150 pinned Page identities proves literary-body coverage,
transclusion rendering fidelity, the 300k threshold or FantLab parity.

The complete 150-Page *source-free historical identity graph* is now durably frozen at [`source-edition-traces/defoe-robinson-crusoe-trusov-1775-ru.page-graph.json`](source-edition-traces/defoe-robinson-crusoe-trusov-1775-ru.page-graph.json) and checksummed against the adjacent receipt; replay locally without Wikisource access using `python -m scriptorium.robinson_trusov_pages verify --manifest corpus/candidates/source-edition-traces/defoe-robinson-crusoe-trusov-1775-ru.page-graph.json --receipt corpus/candidates/source-edition-traces/defoe-robinson-crusoe-trusov-1775-ru.page-graph-receipt.json`. Exact-source *live* replay remains an explicit optional/manual action because provider 429 cannot be accepted as graph mismatch. Neither offline validity nor a historical revision selection proves the 1775 printed literary text, full volume, >=300k threshold or FantLab parity.

## Exact historical Page content preflight (new PR candidate)

`scriptorium.robinson_trusov_content` consumes the committed #396 graph and uses batched MediaWiki `revids` queries to verify all 150 exact historical Page sources by oldid, page ID, title, timestamp and provider SHA-1. It emits per-Page wikitext/transclusion-input SHA-256, derived character counts and unresolved markup totals **without retaining or uploading any Page prose**. Only explicit `noinclude` spans and `includeonly` wrappers are handled. Unknown `onlyinclude` or unbalanced inclusion tags fail closed.

The resulting concatenation is deliberately **unrendered transclusion input**, not a normalized literary body. It contains unresolved templates, links, HTML and synthetic page breaks. Any 300,000-character comparison against these counts is invalid for corpus admission. Full literary extraction, printed volume collation, FantLab input identity and 29-field analysis remain `NOT_RUN`. Initial CI must verify live pinned-page content before recording numeric results.

```sh
python -m scriptorium.robinson_trusov_content \
  --graph corpus/candidates/source-edition-traces/defoe-robinson-crusoe-trusov-1775-ru.page-graph.json \
  --receipt corpus/candidates/source-edition-traces/defoe-robinson-crusoe-trusov-1775-ru.page-graph-receipt.json \
  --output build/repro/trusov-1775.content-preflight.json
```

## Pinned template-shape audit (new PR candidate)

The accepted #397 preflight confirms **34 of 150** Page inputs still contain
**64 unexpanded double-brace openers**. The source-bound template-shape audit
reuses the exact historical oldid and provider-identity checks, classifies
balanced calls, nested braces and argument *counts* while keeping argument
values, raw Page prose and literary text entirely transient. Unsupported or
dynamic template titles are represented by hashes; unclassified triple-brace
openers remain explicit. This is **not template expansion or historical
rendering**, and does not verify page-joining semantics, literary coverage,
300,000 characters, admission or FantLab input identity.

The modified preflight workflow obtains the frozen Page source **once** and
writes both the original byte-for-byte receipt-checked preflight and the new
source-free shape inventory. To run a local live capture with ordinary
Wikisource access:

```sh
python -m scriptorium.robinson_trusov_template_shapes \
  --graph corpus/candidates/source-edition-traces/defoe-robinson-crusoe-trusov-1775-ru.page-graph.json \
  --receipt corpus/candidates/source-edition-traces/defoe-robinson-crusoe-trusov-1775-ru.page-graph-receipt.json \
  --preflight-output build/repro/trusov-1775.content-preflight.json \
  --output build/repro/trusov-1775.template-shapes.json
```

The [exact-head live capture](https://github.com/drevendev/Scriptorium/actions/runs/41402787490)
classified all **64** unresolved openers on **34 of 150 Pages**:
**30 `heading`**, **28 `nop`**, **4 `ВАР`**, and **2 parser/dynamic
unresolved invocations**, with **zero** other unclassified openers. The
[retained source-free summary](diagnostics/defoe-robinson-crusoe-trusov-1775-ru.template-shapes-summary.json)
records the complete report SHA-256
`e27a3eff597a359c3d34e2c15cacb09d1b597fb3651c39ea5b76978a88902f3f`
(48,390 bytes) and is checked against recomputed JSON by CI. The original
preflight retained receipt also passed unchanged, including its SHA-256.
Template classes are an actionable extraction frontier, **not** rendered text.

The emitted shape inventory remains diagnostic: all invocations are unresolved
until their exact identities, binding/expansion semantics and body inclusion
effects are independently tested. Preserve the last accepted #397 receipt if
a provider rate limit prevents a new capture; a CI run that does not complete
is NOT_RUN, not failed scientific parity.


### Trusov provisional standalone-template projection (accepted PR #400)

The accepted exact-source shape audit records **30 heading, 28 nop, 4 ВАР,
and 2 dynamic/parser invocations** across 150 pinned Pages. The accepted
scriptorium.robinson_trusov_projection probe reuses **one** historical Page
fetch to recompute the previously frozen preflight and shape observations and
produce a third, source-free per-Page ledger (counts, revisions, SHA-256 digests).
No projected wikitext or book prose is written to disk.

The deliberately **inferred, partial** plain-text projection handles only
standalone, no-argument nop lines as paragraph separators and
standalone, flat two-positional-argument heading lines with
a plain heading label. Inline/nested calls, extra heading arguments, all
ВАР orthography choices and parser/dynamic calls stay untouched and
explicitly unresolved. The candidate does **not** implement full Page
joining, MediaWiki's parser/cache or historical rendering and cannot
freeze a literary body, prove the >=300k corpus threshold or support
a measured two-translation comparison yet.

Primary semantics: [Wikisource Nop documentation](https://wikisource.org/wiki/Template:Nop/doc)
explains its paragraph-boundary purpose;
[Russian Wikisource Heading documentation](https://ru.wikisource.org/wiki/Шаблон:Heading/Документация)
describes the format and title arguments; and
[ВАР documentation](https://ru.wikisource.org/wiki/Шаблон:ВАР/Документация)
makes explicit that selection depends on historical vs modern orthography
(and Lua). These are **current documentation leads**, not proof of the
exact 2023 template revisions or reproduced historical output.

Run one bounded probe (ordinary Wikisource access required; outputs must be new paths):

    python -m scriptorium.robinson_trusov_projection \
      --graph corpus/candidates/source-edition-traces/defoe-robinson-crusoe-trusov-1775-ru.page-graph.json \
      --receipt corpus/candidates/source-edition-traces/defoe-robinson-crusoe-trusov-1775-ru.page-graph-receipt.json \
      --preflight-output build/repro/trusov-1775.content-preflight.json \
      --shapes-output build/repro/trusov-1775.template-shapes.json \
      --output build/repro/trusov-1775.projection.json

The [exact-head pinned-source verification](https://github.com/drevendev/Scriptorium/actions/runs/41592937429)
confirmed **58/64 provisional** template operations on all 150 oldids
(28 nop, 30 heading; four ВАР and two dynamic/parser calls unresolved).
The previously accepted preflight and shape receipts were recomputed unchanged.
Those operations are a **wikitext projection**, not a rendered source or a
measured book; the first-narrative body and character threshold remain NOT_RUN.

### Source-free joined projection identity (new PR candidate)

The next bounded extraction probe adds an independently versioned
**one-LF-between-projected-Pages** streaming SHA-256 and character count
to the same exact-source, single-pass CI run. It also counts the 149 synthetic
Page seams and source-free *alphabetic-edge* seams where both adjacent Page
fragments end/start with letters; these indicate potential word-continuation
review points, **not** verified broken words or an inferred hyphenation rule.
The full projected wikitext remains **transient**; the retained output contains
only digests, lengths, counters, pinned revision identities and scientific
unknown/NOT_RUN flags.

This synthetic join is not a MediaWiki/ProofreadPage rendering, normalized
literary-body hash, actual ≥300k text measurement, evidence that all chapters
are present, or print/FantLab edition identity. Until exact-head live CI has
captured and validated the new fields, the actual joined SHA/count and
alphabetic seam count remain **NOT_RUN**. Remaining four ВАР and two dynamic
template calls still require historically bound semantics; source-bound
first-narrative selection and print collation remain open. M2 remains **0/5**.

### Explicit orthography-branch preview for flat ВАР (merged PR #403)

The [Wikisource ВАР documentation](https://ru.wikisource.org/wiki/Шаблон:ВАР/Документация)
identifies the **first** positional argument as pre-reform spelling and the
**second** as modern spelling. This is a current documentation claim, not
a pin of the historical 2023 Lua module/template version used by the 150
Trusov Page revisions.

The exact oldid-verified [source-free invocation inventory](https://github.com/drevendev/Scriptorium/actions/runs/41402787490)
places the **four** ВАР calls on Pages **148–151**, with **two
anonymous arguments each**, no named arguments and no nested braces.
This identifies the shape, **not** the literal contents or line layout.

The independent **source-free preview** compares both choices for a
single flat, exactly two-argument ВАР call per line. Plain inline calls
are eligible, but nested/multiple templates, named parameters, HTML,
wiki links, empty or non-printable branches are left unresolved.
The existing conservative page projection remains unchanged; ВАР
invocations are **still counted as unresolved** for historical
rendering purposes. The new versioned diagnostic adds per-page and
whole-join digests of both hypothetical branches, plus the number of
unambiguous flat calls actually previewed. Every unpreviewable ВАР is
partitioned by a **source-free rejection category** (multiline,
multiple templates on a line, non-plain branch, unsupported shape).
Each row checks that previews plus refusals exactly match its pinned
ВАР invocation count; the diagnostic does not expose any argument values. It never writes prose.

Exact-head [CI #41640743857](https://github.com/drevendev/Scriptorium/actions/runs/41640743857)
confirmed **0/4** single-line eligible previews and **4/4 multiline refusals**
without drift in pinned oldids, previous shape receipts or projected-page identity.
A preview is neither verified MediaWiki rendering nor a literary-body
hash or a corpus admission. Two dynamic/parser calls, Page joins,
proofreading/orthographic conventions and print collation remain open.
M2 remains **0/5**.

### Bounded multiline ВАР preview experiment (issue #404, PR candidate)

The next diagnostic extends the two-branch preview to a single flat multiline
`{{ВАР|first|second}}` invocation in a bounded line span. It preserves anonymous
argument whitespace exactly, rejects calls above 4,096 characters / 12 LF
boundaries or with a branch above 2,048 characters, and refuses nested groups,
named/extra arguments, markup, comments, control characters or neighboring
template calls. The accepted conservative Page join and unresolved historical
invocation count remain unchanged. Separate per-page and joined SHA-256 digests,
flat versus multiline preview counts and residual refusal categories are emitted
without source text. Acceptance requires exact-head CI replay of all 150 oldids;
no specific live multiline count is claimed before that replay.

**Scientific limit:** this is a provisional source-free orthography branch
experiment, not a pinned 2023 MediaWiki renderer, a proven 1775 printed edition,
a complete first narrative, a size/admission gate, a measured second translation
or FantLab parity. The two parser/dynamic invocations and Page seam semantics
remain unresolved; M2 stays **0/5**.
