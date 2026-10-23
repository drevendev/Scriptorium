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
```

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

The separate browser Comparison Desk prototype is tracked in #280 and is not advertised
as an integrated feature of this CLI. GitHub Pages activation remains separately gated.
