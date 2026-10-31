# Private comparison of two Reader analyses

The `0.4.0a1` preview adds a complete local `analyze -> compare` path without
uploading manuscripts or report files. It uses the canonical 29-metric registry,
not a second analyzer or a synthetic fixture runtime.

```bash
scriptorium analyze first.txt --output first.json
scriptorium analyze second.txt --output second.json
scriptorium compare first.json second.json --output comparison.html
scriptorium compare first.json second.json --format json --output comparison.json
scriptorium compare first.json second.json --format csv --output comparison.csv
scriptorium compare first.json second.json --format markdown --output comparison.md
```

The Markdown report is a fully offline 29-row table with exact right-minus-left
values, explicit unavailable/incomparable statuses, source hashes, profile and
dictionary identities, and a clear **M2 0/5** scientific boundary. Its title and
all metadata are Markdown/HTML-escaped; it contains no manuscript text. This
presentation is source-free like the existing JSON, HTML and CSV formats.

Open the HTML locally. All formats preserve metric IDs, source digests, declared
algorithm/dependency identities and measurement units. HTML includes a keyboard
skip link, focusable scroll region, source details and a table alternative. Existing
outputs are never overwritten. Shell redirection is not create-only; prefer `--output`.

## Interpretation

Differences are **right minus left**. A percentage difference is in percentage
points, never relative percentage change. Unknown measurements remain unavailable;
different algorithm profiles make all rows incomparable. A different dictionary
makes only the five dictionary-dependent vocabulary metrics incomparable. Dictionary
identity is content-based, not JSON key-order-based. Revision labels are provenance,
not a replacement for algorithm versioning.

Input JSON decimals are retained as exact decimal observations; subtraction chooses
sufficient precision instead of rounding at the default Decimal context. The analyzer's
existing floating-point measurements are not retrospectively upgraded to exact science.

Reports and hashes are unauthenticated declarations. Validation catches contradictions,
not every possible forgery. Rerun analysis on the original bytes to verify a report.
Shared normalized digests and method identities cannot assert contradictory measurements;
dictionary changes do not excuse dialogue or punctuation drift.

## Rejection and privacy boundaries

Each UTF-8 report is limited to 8 MiB. Duplicate keys, nonfinite/oversized numbers,
unknown/missing fields, malformed digests, incorrect units/evidence statuses, missing
mandatory counts, impossible means, broken vocabulary partitions and inconsistent
punctuation rates are rejected. Symlinks and non-regular input files fail closed.
Create-only output uses the same atomic writer as the analyzer. Operational errors do
not print manuscript text or private paths. CSV protects text cells from formula-like
prefixes while retaining signed numeric differences. Hashes can identify known works;
share reports deliberately. No telemetry or external requests are made.

Short texts are valid inputs with the existing representativeness limitation. No corpus
entry, source edition identity, FantLab parity or M1-M5 completion is established by
this comparison. **M2 remains 0/5**, and AOT-lineage compatibility remains the target.

## Reproducible acceptance

`tests/test_compare.py` and `tests/test_imported_mean_integrity.py` construct their
reports with the real `build_local_analysis()`, not analyzer stubs. The Reader workflow
also builds the full repository wheel, installs it outside the checkout and runs
`tools/private_compare_smoke.py`: real texts, 29 rows, HTML/JSON/CSV, exact deltas,
deterministic output, create-only behavior and negative input rejection.

## Local browser Comparison Desk (issue #280)

The canonical site build includes `compare/index.html`. Analyze two UTF-8 texts
locally into JSON with the Reader, build the site, open the Comparison Desk and
choose the two report files. Only the current browser tab reads their bytes: no
network, telemetry, server storage, upload, cookies or persistent browser state.

The browser's 29 metric IDs, names, units and compatibility/evidence statuses are
generated at build time from the actual Python deterministic analyzer registry.
A bounded, duplicate-key-aware JSON parser preserves exact decimal *lexemes* and
distinguishes the JSON integer token `3` from `3.0` or `3e0`.
Counts, punctuation rates, method/dictionary identities, contradictory source
hashes, missing metrics and representativeness are checked before comparison.
Exports are source-free JSON and formula-neutralized CSV; values stay right-minus-left
with explicit units and reasons. Files must each be valid UTF-8 Reader reports no
larger than 8 MiB. For canonical repeatability or disabled JavaScript, use
`scriptorium compare` in the installed CLI.

The Python and browser comparison implementations use matching versioned contracts;
the Python implementation remains the canonical acceptance reference. Runtime
differential tests exercise 234 accepted/rejected report pairs and check exact
JSON/CSV exports. This does not authenticate imported hashes or establish copyright,
source edition, FantLab equivalence or corpus admission. M2 remains 0/5.
GitHub Pages activation remains separately gated.

## Printing the browser comparison

After loading two reports and choosing **Compare reports**, the browser's Print
command renders each of the 29 metric rows as a self-contained, two-column card.
The on-screen table still scrolls horizontally on narrow displays; on paper the
metric name, left/right values, units, exact difference, status and reason all
remain visible and labelled. The input controls and export buttons are omitted
from paper, not the results. A printout is **derived evidence**, not proof of
FantLab parity or authenticated source hashes. No manuscript bytes are uploaded
to print.

The print layout has source-level and isolated Chromium print/PDF checks.
Those are not a verified canonical Pages URL, nor complete desktop/mobile
accessibility acceptance for #283; actual published-route visual checks remain
separately gated.

## Keyboard and narrow-screen results

After choosing two valid local JSON reports and activating **Compare reports**, the
browser moves keyboard focus to the **Source-free comparison** heading, just before
the source hashes, export actions and complete 29-row table. A polite live status
also announces validation. Invalid or unsupported JSON leaves focus on the action
and explains the rejection without revealing manuscript text or file paths. Changing
a file during asynchronous validation discards the old result without stealing focus.

On narrow displays, the table remains a semantic eight-column table. Tab into its
labelled, focusable scroll region and use arrow keys to read columns horizontally.
A visible instruction names this interaction; paper output omits the scroll hint
and retains the independently tested labelled metric cards.

The Comparison Desk also provides a keyboard-accessible **Find a metric** search
field after two reports validate. Filtering matches metric labels, IDs and units
(case-insensitively); the live count announces matches and explains an empty result.
Clearing the field restores all 29 rows. Filtering only changes which rows are
visible on screen: **exports and print always include the complete 29-metric
comparison**, even when a filter is active. No text, filenames or queries are sent
outside the browser.

Automated Node DOM interaction tests cover success, invalid files and stale async
reads. They are **not** real desktop/mobile assistive-technology acceptance and do
not establish that GitHub Pages is deployed or live-verified. Issue #283 remains
open pending the genuine browser/keyboard/mobile checks.
