# Scriptorium · Literary language reader

**[🌐 Open the interactive Scriptorium Reader (GitHub Pages) →](https://drevendev.github.io/Scriptorium/)**

**Tenth measured Russian novel — Dostoevsky's *Humiliated and Insulted*:** The [exact, source-free 29-field analysis](corpus/candidates/diagnostics/dostoevsky-humiliated-and-insulted-ru.retained.json) merged in #370 after the [pinned Wikisource replay](https://github.com/drevendev/Scriptorium/actions/runs/41111720059), oldid `5611473`: 713,925 characters including spaces, 118,157 words, 10,381 sentences, **24 numeric and five NOT_RUN** fields. This focused PR proposes the [tenth Reader card, charts and comparisons](https://drevendev.github.io/Scriptorium/?book=humiliated#measurements), making **10 measured / 12 catalogued books, 269 fields**. The URL awaits later merge and independent deployment/live verification. No literary prose is committed. Print edition NOT_RUN, FantLab input UNKNOWN, **M2 0/5**.

**Ninth measured Russian work — [Goncharov's *Oblomov* →](https://drevendev.github.io/Scriptorium/?book=oblomov#measurements):** The exact public-domain Wikisource az.lib witness `oldid=5724579`, **930,248 characters including spaces**, 147,447 words and 14,353 sentences, contributes **24 measured / five NOT_RUN** dictionary fields. The previous ninth Reader edition has its card and source-free JSON; the tenth-work integration extends the no-JavaScript CSV to **269 fields** (225 numeric, 44 unavailable) across ten measured works. [Source-free measurement](corpus/candidates/diagnostics/goncharov-oblomov-ru.json) preserves source SHA-256 and the four-part/46-chapter completeness gate. The claimed 1954 print collation was **NOT_RUN** and FantLab's input is **UNKNOWN**: diagnostic results only (**M2 0/5**). PR #368 was merged into `master` on 2026-10-30. An independent browser/HTTP check of the resulting live Pages deployment is still **NOT_RUN**. No literary prose is committed.

**Two-author rhythm preview — [Grin × Tolstoy, four complete Russian books →](https://drevendev.github.io/Scriptorium/voice/):** A source-bound, fully static Russian-language comparison computes eight word-count-weighted literary rates and per-work weighted population standard deviations using two separately measured novels per author. Inspect four bar comparisons, an eight-metric mean/dispersion table and the new 32-observation table showing all four individual books, plus a source-bound min–max comparison for eight metrics (two illustrated interval plots; observed ranges, not confidence intervals), then check source hashes or [derived JSON](assets/voice-preview.json); no literary prose or user text is uploaded. This is a small descriptive **extension preview**, not FantLab parity or a validated M3 author profile: only two works per author, no cross-validation, unknown FantLab input identity (**M2 0/5, M3 open**). GitHub reports a successful branch-root Pages deployment of merged #364 on 2026-10-30; direct HTTP/browser verification remains outstanding.


**[Native POS N uncertainty — measured Anna Karenina evidence →](https://drevendev.github.io/Scriptorium/n-uncertainty.html):** Source-free, hash-bound native pylem 0.0.18 measurements quantify 55,081 N-only tokens (20.45% of 269,358 Scriptorium tokens), 19,670 excluded mixed-N rows, exact per-cell conditional POS-bigram bounds and sentence-position bounds. Noun/cardinal labels remain unresolved, bounds are not jointly attainable, FantLab source identity is unknown and M2 remains 0/5. The new static page includes accessible tables, native lexical contrast controls and a linked JSON summary; a PR build alone does not establish live publication; the link requires a successful root-branch Pages deployment.

**Eighth measured Russian edition — Alexander Grin's *Road to Nowhere* (merged PR #360; live verification pending):** The independently verified source-free CI artifact captures 29 metrics (**24 actual, five NOT_RUN**) for the full Russian Wikisource az.lib alternate (oldid 5585836; 442,656 characters; raw/normalized SHA-256 `e33a28b8dcdb3ac339147c6587b27c182dd910784122b367db41bc93dfc2dbee`). The retained derivative keeps [the original CI run](https://github.com/drevendev/Scriptorium/actions/runs/40969367325), ZIP SHA-256 `55c39e7b0c4a69a9c86fe3afc7c1d9c63620c4f9d52eb23be4dd688cda6b39f0`, JSON SHA-256 `a0cfc008f9e8580a203e39c83a3e65755143c593038adaa275037bbed7dc1e92`, and two **source-unmatched diagnostic** count differences (+4,217 characters and +3,773 words). The Pravda 1965 source family is distinct and incomplete; FantLab input identity UNKNOWN, **M2: 0/5**. The eighth Reader card, charts and `?book=road#measurements` permalink are merged into `master`; a successful deploy and live HTTP/browser acceptance must still be checked independently. No literary prose is published.

**Russian-first public Reader (merged as PR #333; live HTTP not independently verified):** GitHub Pages uses `master / (root)`. The home page groups **12 Russian-language works**: ten with actual source-pinned observations and two clearly marked as work in progress. The 10 measured books provide **269 fields, 225 numeric observations and 44 explicitly unavailable values**. The root Reader's eight chart choices now include dialogue, narration and word lengths, remarks, commas and dashes. A keyboard-accessible expandable table now mirrors all eight charts, exposing source-backed numeric values and explicit missing data even without JavaScript (initial dialogue view). Beketova's two unavailable dialogue-length fields explicitly show **«нет данных»**, not a fabricated zero; all ten measured books remain visible and source-backed. Search, book-to-book rate comparisons, chart bars, JSON exports and source metadata are reader-facing; cross-language original/translation analysis is not yet present. The multi-route Python-generated Reader remains a **separate local/CI build** in `build/site`, rather than the root branch Pages experience; its retained FantLab matrix currently covers four measured books and one unmeasured source. The Hyperboloid generated route described below is separately measured and does not silently alter that matrix.

**Export the measured catalogue (root Reader):** The [pinned 269-field static CSV](assets/scriptorium-ru-measured-metrics.csv) works without JavaScript and is byte-for-byte checked against the verified interactive serializer in CI. After verifying the local source-free evidence snapshot, the interactive measurement registry also enables **Download all 269 fields (CSV)**. The UTF-8 file has one row per field across ten separately identified Russian editions, with 225 exact numeric observations and 44 empty numeric cells carrying explicit `not_run`/`unavailable` statuses. Each row includes original/analysis language, translator identity where applicable, edition/source SHA-256, evidence and FantLab reference URLs, measurement profile versions, units and reference availability. The 2 unmeasured research leads are not exported as measurements. All values remain diagnostic/extension only, FantLab input identity `UNKNOWN` and M2 **0/5**. CSV text cells are protected against spreadsheet-formula injection; nothing uploads private texts.

**Share a specific chart (root Reader):** `?metric=fantlab.punctuation.dash.per_1000_words#charts` opens the ten-book dash-rate view; each of the eight supported metrics has a visible direct link. The selector updates browser history and Back/Forward restores the graph. Unknown, foreign and inherited-object property names fall back to the pinned dialogue chart. These are **source-bound descriptive measurements**, not FantLab parity; the no-JavaScript page retains its original static dialogue table. Browser LIVE_VERIFIED remains outstanding.

**Chart ranking (Russian Reader):** All eight charts support optional **Sort by value**. The descending order is stable on ties; missing measurements stay last (not zero), and the accessible exact-value table follows the bars. Without JavaScript the catalog-order chart and table still work. Direct chart links preserve the metric, not this local sorting preference.

**Filter the Russian catalogue:** Once the source-free JSON passes validation, the twelve-book grid can show all editions, ten measured works, two preparation leads, or two named Russian translations (Beketova measured; Rachinsky still in preparation). These are source-bound filter counts, not new analysis. Without JavaScript or valid JSON, all eleven static cards and provenance links remain accessible and the filter stays hidden. This does not establish FantLab input identity (M2 0/5).

**Find a Russian edition by title, author or translator:** The source-verified catalogue now includes optional text search combined with the measured/pending/translation filter. It matches Russian display names, tolerates `е`/`ё`, reports empty results and keeps static cards and provenance links when JavaScript or validation is unavailable. This is metadata search, **not** full-text search or new scientific evidence.

**Share a filtered catalogue (root Reader):** `?catalog=translated&q=%D0%91%D0%B5%D0%BA%D0%B5%D1%82%D0%BE%D0%B2%D0%B0#books` opens Beketova's translated Russian edition after verified JSON loads. The visible direct link reflects active filter/search controls without transmitting input or modifying history as a user types. Reload and Back/Forward restore valid URL state. Foreign modes and oversized/control-character queries fall back safely; without JS or valid JSON all static books and source links remain available. Metadata search is not full-text search or FantLab parity.

**FantLab diagnostic differences in the Russian Reader:** The per-book measurement table now displays signed **Scriptorium − FantLab** arithmetic only where both pinned numbers exist. Integer differences are exact; fractional differences are shown to three decimal places (percentage-point units for percentages). Missing references, NOT_RUN measurements and Scriptorium-only extensions are not zeros. These are source-unmatched *diagnostics*, not benchmark PASS or M2 parity. Four source-backed example rows are available without JavaScript; complete selection requires validated JSON. Desktop/mobile/live visual verification is still pending.

**Print / Save as PDF:** The currently selected Russian chart now expands its exact-value, ten-book table only for print preview and restores the previous open/closed state afterward. The print stylesheet uses black text and wrap-safe full-precision values instead of relying on bar colors. This does not print eight charts simultaneously; select the metric you need first. With JavaScript unavailable, expand the initial dialogue table manually before printing. Desktop/mobile print rendering remains VISUAL_NOT_VERIFIED pending a real browser check.

**Seventh measured Russian work (merged to master in #342; HTTP unverified):** Tolstoy’s *Resurrection* has 29 source-frozen fields (24 numeric, five NOT_RUN) from 129 pinned revisions, body SHA-256, two public FantLab count references and original CI-artifact hashes. `?book=resurrection#measurements` is implemented in the root Reader; independent live-route verification remains outstanding. FantLab input identity is UNKNOWN, comparison DIAGNOSTIC_ONLY, M2 0/5. No source prose is published.

**Shareable book views (root Reader source):** Every measured Russian edition can now be opened directly in the same-page metric explorer, for example [Beketova's Russian translation](https://drevendev.github.io/Scriptorium/?book=beketova#measurements) or [Silver Dove](https://drevendev.github.io/Scriptorium/?book=silver#measurements). These addresses select only allow-listed, verified measurement records; pending/invalid IDs fall back to Anna Karenina. Back/forward, keyboard focus and source-JSON fallbacks are retained. The URL is a target for the existing branch Pages deployment **after the relevant commit is published**—the README link alone is not proof of live deployment. This public root navigation is separate from the generated Reader's multi-page routes.

**Shareable two-book comparisons (root Reader source):** `?left=anna&right=beketova#pairs` identifies exactly two measured Russian editions in the side-by-side rates table. Both selectors update browser history; Back/Forward and reload restore a valid pair. Invalid, pending, partial and duplicate URL pairs fall back to Anna Karenina × Brothers Karamazov. Selecting the same book in both in-page controls instead displays an error and hides the link. The URL cannot specify arbitrary data sources; M2 remains 0/5. The pair-link feature merged in #337 and its master Pages deployment workflow succeeded on 2026-10-27; browser/HTTP `LIVE_VERIFIED` remains outstanding.

**Source-free pair JSON and CSV exports (root Reader):** The comparison table can be downloaded with exactly the jointly measured rows, left/right values, numeric right-minus-left differences with explicit delta units (percentage points for percentages), original measurement units, versioned shared profiles, each edition and translator identity, immutable text hashes and links to the evidence records. The deterministic export labels `DIAGNOSTIC_ONLY`, unknown FantLab input identity and M2 0/5 explicitly; it includes **no literary text** and does not send data anywhere. The export is unavailable for duplicate, unmeasured or algorithm-incompatible pairs. The JSON comparison export merged in #338, but its live HTTP result is not independently verified. The additional CSV table uses the same validated measurements, percentage-point delta units, translators, edition/source SHA-256, complete shared algorithm profiles and evidence URLs. CSV text is quoted and spreadsheet-formula-neutralized; numbers remain numeric. CSV export was merged in #339; live browser/HTTP confirmation remains outstanding.

**Generated Reader stage — local/CI only:** The separately built `build/site/index.html` contains a measured-stage panel derived at build time from the retained FantLab evidence matrix: five works with numeric observations, 118 measured values, 24 unavailable actuals, and **M2 0/5** source-matched works. It links to the generated `build/site/evidence/fantlab/` table. **This specific stage panel and multi-route evidence view are not published by the branch-root Pages URL.** The public homepage has its own eight-book interactive charts, ten-title catalogue and source-free metric explorer. The full generated Reader additionally registers **Hyperboloid of Engineer Garin** at `build/site/works/hyperboloid-garin-measured/`: 29 pinned source-free fields (24 measured, five NOT_RUN), exact-value CSV/JSON and CI/source receipts. The same local/CI build now also contains a separately pinned **Beketova Russian translation** report at `build/site/works/captain-grant-beketova-measured/`: all **11 verified derived observations**, edition/translator attribution and source-free JSON/CSV exports. Both extra generated-only reports lack confirmed FantLab input identity or parity and do not change the branch Pages catalogue.

The separately built full Reader can show **real measured differences** between two books, independently search and filter
Anna Karenina's 28-row and Running on Waves' 27-row diagnostics, inspect Silver Dove and Brothers Karamazov's 29 fields each, filter their twenty
shared measured rates independently by metric name or family, examine a full-work
diagnostic, browse the source-free FantLab evidence matrix, or compare two of
your own Reader JSON reports privately in the browser. Charts and a visible exact-value table show retained, validated derived
measurements, units and links to methodology and scientific limitations. No manuscript is hosted or uploaded.

**GitHub Pages branch deployment (verified 2026-10-27):** GitHub reports `has_pages=true`. The GitHub-managed `pages build and deployment` workflow completed successfully on `master`, with the Jekyll checkout configured as `source: .`. The previous blocker was not lack of Pages administration: it was a missing root `index.html` and public assets. Merged PR #332 supplies them. A successful deployment is not a claim that the public site is already live **with the expected Reader** until an independent HTTP/browser check confirms it. The richer Python-built Reader remains available offline:

```bash
python -m scriptorium.site_renderer --repo-root . --output build/site
# Open build/site/index.html
```

The separate, historical *Actions artifact deployment* job remains guarded by `SCRIPTORIUM_PAGES_DEPLOY_ENABLED=true`, but is **not required** for GitHub's already configured branch Pages publication. Do not change the deployment gate or repository settings to make the root homepage work. See [#285](https://github.com/drevendev/Scriptorium/issues/285) for the distinction and [#284](https://github.com/drevendev/Scriptorium/issues/284) for unresolved software/data reuse licensing.

**Retained Resurrection field diagnostic (CI/replay and root Reader, source-free):** The 129 exact pinned Russian Wikisource chapters of Tolstoy's *Resurrection* can be replayed into **29 versioned Scriptorium fields** in one verified pass. The output retains numerical values, units, two publicly documented FantLab count references and signed deltas, with dictionary-dependent values as `NOT_RUN`. It includes no chapter prose, and explicitly records **unknown FantLab input edition, diagnostic-only comparison and M2 0/5**. CI creates separate create-only replay/field receipts; the verified source-free 29-row receipt is retained in master (24 numeric and five NOT_RUN). GitHub Pages live-route verification remains outstanding. Reproduce when the pinned source endpoint is reachable:

```bash
python -m scriptorium.resurrection_diagnostic \
  --manifest corpus/candidates/source-edition-traces/tolstoy-resurrection-ru.revisions.json \
  --receipt resurrection-replay-receipt.json --output resurrection-fields.json
```

**What the Russian-first demo shows:** ten source-frozen, measured Russian-language texts (including a separately identified translation by Alexandra A. Beketova), with 269 recorded fields / 225 numeric / 44 unavailable. Two further Russian-text candidates are listed as preparation only: Petersburg and Darwin's *Origin of Species* in Sergey Rachinsky's 1864 Russian translation. Twelve **catalogue entries include ten measured books and two unmeasured research candidates**. Translated texts keep named translators, original language, family, exact edition and source identity; a French original must not be silently treated as an English text. The English analyzer is a separate future module with zero measured original-language works today. The root Reading Room offers descriptive comparisons of normalized candidate metrics on the same pinned Russian algorithm profile; original-vs-translation and translation-vs-translation comparisons require independently verified per-version data. M2 FantLab parity remains **0/5**. Browser LIVE_VERIFIED requires independent HTTP/screenshot evidence; publication must not be inferred from CI builds alone. Root Pages deployment and the Python-built multi-route Reader are distinct.

**Understand the language of a text without uploading the manuscript.**
Scriptorium measures vocabulary, sentence length, dialogue and punctuation, then produces
readable offline reports and reproducible data. This **0.4.0a1 preview** adds private
comparison of two analyses to the canonical Reader and its real-work gallery.

## Language modules and translations

The Russian module (`ru`) is the initial product priority. Every analyzed literary body has an **analysis language** and an independent **edition identity**. A translated work additionally records the author's original language, a named translator and a specific edition/source family; another translator or translation revision becomes a separate identity, not another spelling of the title. The measured Russian translation of **Дети капитана Гранта** by **А. А. Бекетова** has 11 real derived fields, but no measured French original. The researched translation of **О происхождении видов** by **С. А. Рачинский** has no retained numeric fields, and its English source is not analyzed here. Never place invented English/French numbers into Russian graphs. See [versioned language/translation contract](docs/TRANSLATIONS_AND_LANGUAGE_MODULES.md).

**Coverage target:** 10 analyzed works, each individually rights-cleared, byte/source-frozen and measured. Reader integration candidate: 10 measured / 12 catalogued; the remaining two are labelled honestly and require separate reproducible measurements. This is unrelated to the stricter FantLab M2 source-matched parity requirement (0/5).

## Try your own text

With Python 3.13 or later, from this checkout:

```bash
python -m pip install .
scriptorium analyze manuscript.txt --format html --output report.html
scriptorium analyze manuscript.txt --output analysis.json
scriptorium analyze manuscript.txt --format csv --output metrics.csv
```

Open `report.html` locally. All **29 metric rows** retain their units and algorithm
profiles; unavailable measurements stay unknown. The report has readable metric names,
a four-value overview, exact numeric values and keyboard-accessible tables. JSON and
CSV include source digests, not manuscript content. Choose a new output filename for
each run: existing files are never overwritten.

No runtime dependencies, account, server or telemetry are required. Installation may
fetch build tools; see [offline wheel installation](docs/READER_PREVIEW.md).
`python -m scriptorium` exposes the same commands from a checkout.

## Analyze an unencrypted EPUB locally

Import an EPUB 2/3 with a standard XHTML reading-order spine without uploading
the book or writing its extracted chapters to disk:

```bash
scriptorium epub book.epub --output analysis.json --provenance-output epub-identity.json
scriptorium epub book.epub --format html --output analysis.html
scriptorium epub book.epub --format csv --output metrics.csv
```

The regular Reader **29-metric** reports work with `scriptorium compare`.
The separate source-free receipt records the **archive**, **extracted UTF-8
body** and **engine-normalized text** SHA-256 identities plus the versioned
extraction profile. EPUB reading order follows OPF spine order; unsupported
encrypted, malformed, unsafe or image-only books fail closed. No DRM bypass,
external network resources or embedded scripts are processed. This local
EPUB text projection is **not** FantLab edition/input parity or corpus admission.
[EPUB formats, safety limits and reproducibility](docs/PRIVATE_EPUB.md).

## Analyze a private batch (POSIX preview)

Select up to 16 UTF-8 manuscripts explicitly in a JSON manifest, then generate
source-free per-work reports and an HTML/JSON/CSV index locally:

```bash
printf '%s\n' '{"schema_version":"scriptorium-private-batch-manifest-v1","files":["first.txt","second.txt"]}' > manifest.json
scriptorium batch manifest.json --output-dir private-results
```

The manifest paths are relative to its directory. No implicit crawling, uploads,
overwrites or source-text publication. Failed items are marked unavailable,
never assigned zero metrics. Re-running an unchanged batch reuses identical
outputs; conflicting files fail closed. Use a private POSIX filesystem:
directory-relative no-follow operations are required. This workflow does not
admit works to the corpus or establish FantLab parity.
[Batch use, limits and exit codes](docs/PRIVATE_BATCH.md).

## Compare your own analyses

```bash
scriptorium analyze second-manuscript.txt --output second-analysis.json
scriptorium compare analysis.json second-analysis.json --output comparison.html
scriptorium compare analysis.json second-analysis.json --format json --output comparison.json
scriptorium compare analysis.json second-analysis.json --format csv --output comparison.csv
```

Open `comparison.html` for the same 29 measurements, explicit units, source identities
and **right minus left** differences. Percentage differences use percentage points.
Unknown measurements do not become zero; different methods or dictionaries are labelled
incomparable where applicable. JSON decimal observations and their differences retain
precision. Contradictory counts, means, punctuation rates and same-text results are rejected.
Imported JSON and hashes are declarations, not authenticated proof: rerun the analyzer
on the original bytes to verify them. [Comparison contract and examples](docs/PRIVATE_COMPARISON.md).

## Compare in your browser (private beta)

Build the canonical site with `scriptorium site --repo-root . --output build/site`
and open `build/site/compare/index.html`, or use the **Compare private reports**
action in the generated homepage. Select two local `scriptorium analyze` JSON
reports; no manuscripts or report bytes are uploaded. Inspect all 29 measurements,
incomparable/missing reasons, exact decimal right-minus-left differences, and
download source-free JSON/CSV. The browser validates the same versioned report
contract as the installed Python Reader and rejects duplicate keys, integer
lexeme spoofs, impossible counts, nonfinite values and changed units. Browser
support requires JavaScript; the offline `scriptorium compare` CLI always works.
[Browser validation and limitations](docs/PRIVATE_COMPARISON.md).

This is a **local build capability**, not a live GitHub Pages deployment. No private
manuscripts are included; imported report hashes are unauthenticated declarations.
Scientific/FantLab parity remains unverified (M2 0/5).

## Open a real literary result

The repository contains a source-free, historical full-work diagnostic for
**Anna Karenina**: **28 expected/actual/delta rows**, with 23 numeric results and five
unavailable values. No novel download is needed:

```bash
scriptorium diagnostic benchmarks/fantlab/work270306-wikisource-diagnostic.json \
  --title "Anna Karenina — full-work diagnostic" --output anna-report.html
scriptorium site --repo-root . --output build/site
```

Open `anna-report.html` or `build/site/index.html`. The canonical site retains the five
earlier evidence/report routes and the Reader 0.3 two-book comparison route.
**A successful local build is not a live GitHub Pages deployment.** The Pages activation
interlock is unchanged; this preview does not enable publishing by itself. Atomic site
replacement currently requires Linux `renameat2`; unsupported platforms fail without
deleting the previous build. Private text analysis and comparison are separate capabilities.

## Compare two already-analyzed books

No manuscript download or morphology setup is needed for the frozen **Running on Waves**
and **Children of Captain Grant — Beketova translation** comparison:

```bash
mkdir -p build
python -m scriptorium.full_work_gallery --repo-root . --format html > build/full-work-gallery.html
python -m scriptorium.full_work_gallery --repo-root . --format csv > build/full-work-evidence.csv
```

Open `build/full-work-gallery.html` for ten exact measurements and seven row-wise charts.
These are Scriptorium-side results, not FantLab parity or author-style scores. The pinned
canonical site route is `build/site/works/two-full-work-differences/index.html`, with
`measurements.json` and `measurements.csv` downloads. Navigation and export links have
44-pixel minimum touch targets; visible focus and reduced-motion styles are retained.
Newly approved replacement evidence must declare compatible source units before display;
legacy Grin diagnostics are not assigned invented source-unit fields.
Building this route does not prove GitHub Pages is deployed. Shell redirection replaces
its destination; use new filenames to keep older exports. [Method and limits](docs/FULL_WORK_GALLERY.md).

## Inspect FantLab reproduction readiness

Inspect **five frozen public literary sources** and the distance between their
character counts and the *displayed* FantLab counts, without downloading books:

~~~bash
python -m scriptorium.benchmark_readiness --root . --format markdown
python -m scriptorium.benchmark_readiness --root . --format json --output readiness.json
~~~

Each source-free report includes source rights/edition evidence, immutable body
hashes, dated FantLab references and explicit source-matching status. Differences
are **diagnostic only**: FantLab's analyzer-input identities remain unknown
and **M2 stays 0/5**. This character-count readiness command labels other
metrics NOT_RUN **in this view only**; it does not erase existing, independently
validated field-level observations in the metric matrix below.
[Readiness methodology, CSV and limitations](docs/BENCHMARK_READINESS.md).

To inspect **actual retained per-metric differences** rather than character counts alone,
run `python -m scriptorium.benchmark_metric_matrix --root . --format markdown`.
The source-free matrix validates **171 field-level diagnostic/extension rows**:
142 across the five core works (**five works with retained measurements**),
plus 29 *Resurrection* rows as a sixth, separately pinned source-unmatched
diagnostic. All **five** frozen works have field observations; none has an
established FantLab analyzer-input identity. *Anna Karenina* has 28 rows
(23 numeric, five without actuals), *Running on Waves* has 27
(23 numeric, four NOT_RUN), while *The Silver Dove*, *The Brothers Karamazov*
and *The Hyperboloid of Engineer Garin* each have 29 rows (24 numeric,
five dictionary-dependent NOT_RUN). Among these five core works, 118
actual values are measured and 24 remain unavailable. The Hyperboloid
rows reuse the already SHA-pinned, successful CI receipt and verified
499,066-character source body; its unmatched-reference differences are
+3,527 characters and +2,795 words, **not** a FantLab parity result.
The supplemental *Resurrection* contributes 29 fields (24 measured, five
NOT_RUN), with two retained FantLab counts and unmatched differences
+9,591 characters and +9,672 words. In total, the six diagnostics have
142 measured fields and 29 unavailable actuals. 
Other reference values and exact input identity remain
UNKNOWN; none establishes FantLab parity. Anna's historical rows include 4/4 general, 4/4 dialogue,
14/14 punctuation and 1/6 vocabulary measurements; its other five vocabulary
actuals are two NOT_RUN and three unresolved.

The generated evidence Reader displays all 29 Silver Dove, 29 Brothers Karamazov and 29 supplemental Resurrection fields in accessible static tables, and links to the existing independently validated 29-row Hyperboloid detail route,
including separate unknown FantLab references and an explicit extension marker.
It also labels metric units and percentage-point differences, and offers
**independent search/filter controls for both books** by metric name/ID,
family and availability. Tables and source-free JSON/CSV remain available
without JavaScript and in print. A separate **20-row side-by-side comparison**
shows only shared measured word/sentence lengths, punctuation rates and dialogue
percentages (Running on Waves minus Anna Karenina, percentage differences in
percentage points). Unlike total characters or vocabulary counts, these carry
explicit per-unit denominators, but remain **descriptive, source-unmatched
Scriptorium candidates**, not author-style or FantLab-parity evidence.
Neither retained work is source-matched to FantLab's analyzer input, displayed
rounding is unproven, and **M2 stays 0/5**.
Build the site with `scriptorium site --repo-root . --output build/site` and open
`build/site/evidence/fantlab/index.html` to browse the same verified five-work readiness evidence plus the separately labelled Resurrection diagnostic
and download its source-free JSON/CSV. The same page now also shows each
frozen work's character count, signed diagnostic difference from FantLab's
displayed count and source/edition/rights link. It also shows **signed
relative drift** as (frozen minus FantLab displayed) divided by FantLab
displayed, expressed in percent and rounded to two decimal places.
This display-only diagnostic is not a parity score and does not alter JSON/CSV.
These counts do not establish FantLab analyzer-input identity. The evidence page
also offers **source provenance JSON/CSV** downloads generated from the same
five validated readiness witnesses as the visible work table. The JSON contains
raw and normalized SHA-256 digests, reference dates and legal/source metadata;
the CSV retains raw digests and reference dates. No manuscript text is included.
The homepage links to this route.
This is a
**locally built** page, not a confirmed live GitHub Pages deployment.
[Field-level matrix and evidence checks](docs/BENCHMARK_METRIC_MATRIX.md).


To join a separately generated **source-free POS artifact from the same normalized
text** into a FantLab benchmark, add `--pos-metrics pos.json` to the
`python -m scriptorium.benchmark --reference ... --text ... --scriptorium-revision ...`
command. This adds **40 explicitly unresolved/diagnostic POS rows**, including
17 visible category counts and percentages, but never claims POS parity.
Unmatched text digests, profiles or inconsistent 17×17/20×17 structures are
rejected. The work488 FantLab category counts are not a simple partition of
defined words, and service-word actuals remain unknown.
[POS benchmark usage and evidence boundaries](docs/BENCHMARKING.md).

## What the results mean

FantLab-shaped metrics are **inferred compatibility candidates**, not demonstrated
parity. Scriptorium-only features are **extensions**. The historical Anna diagnostic
has no established identity match to FantLab's input text. **M2 remains 0/5**; none of
M1–M5 is declared complete by this preview. The AOT-lineage morphology target and
field-by-field parity criteria remain unchanged.

Texts shorter than 300,000 characters including spaces are valid inputs with explicit
representativeness limits. That length is a corpus-admission floor, not a guarantee of
quality; legal provenance and source identity require separate evidence. Source books,
private manuscripts and dictionary contents are not included in reports or uploaded.
Hashes can identify known works; share derived reports deliberately.

## Safety and reproducibility

The CLI bounds manuscripts to 32 MiB and dictionaries and comparison reports to 8 MiB
per file, rejects special files and symlinks, and uses a create-only atomic writer.
Operational errors do not echo private paths or source text. CSV neutralizes formula-like
**text** while preserving numeric cells; spreadsheet import/save behavior is not universally guaranteed.

```bash
python -m unittest discover -s tests -v
python -m pip wheel --no-deps . --wheel-dir dist
```

The Reader workflow runs the complete canonical suite, builds a full wheel and tests it
outside the checkout: actual manuscript analysis/comparison, HTML/JSON/CSV, historical
report, safe failures and deterministic source-free gallery/site. No analyzer stubs are
used in the private-comparison acceptance. Package, project and CLI versions must agree.
The full Python public API, morphology modules, benchmark data and corpus records remain
in place. No external package-registry release is performed by CI.

Site locks are persistent regular files whose kernel locks are released on process death.
Do not delete a lock file while a publisher could be using it. Legacy directory locks
from an interrupted older preview fail closed and are not automatically deleted.

## Documentation

[Reader installation and commands](docs/READER_PREVIEW.md) ·
[Local analysis and dictionaries](docs/LOCAL_ANALYSIS.md) ·
[Private comparison](docs/PRIVATE_COMPARISON.md) ·
[Private batch](docs/PRIVATE_BATCH.md) ·
[Frozen diagnostic methodology](docs/FROZEN_DIAGNOSTIC_REPORT.md) ·
[Five-work benchmark readiness](docs/BENCHMARK_READINESS.md) ·
[Canonical site and publication boundary](docs/FULL_WORK_SITE_REPORT.md) ·
[Roadmap and repository assessment](project/ROADMAP.md)

The detailed [Research and evidence index](RESEARCH_INDEX.md) retains project history,
corpus investigations and original reference links. Private EPUB and batch Reader
capabilities have been integrated into the repository; their inputs remain local.
The browser comparison is merged into master as a local-build capability;
public deployment remains unverified and separately gated. Code/data licensing and Pages activation retain separate gates (#284/#285).

Reader FantLab evidence now includes an offline-only metric explorer (label/ID, family and measurement availability) with a complete no-JavaScript/print table. Scientific source-match and parity status remain unchanged; see [benchmark evidence](docs/BENCHMARK_METRIC_MATRIX.md).
