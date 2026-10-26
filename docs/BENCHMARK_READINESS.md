# Cross-work FantLab readiness — diagnostic preview

Generate deterministic **source-free** views from the retained catalog, frozen body
witnesses and FantLab reference metadata:

~~~sh
python -m scriptorium.benchmark_readiness --root . --format markdown
python -m scriptorium.benchmark_readiness --root . --format json --output /tmp/readiness.json
python -m scriptorium.benchmark_readiness --root . --format csv --output /tmp/readiness.csv
~~~

The output option creates new files only; an existing report is never overwritten.
No manuscripts are read, downloaded or uploaded. The report checks duplicate JSON
keys, five explicit candidate identities, rights evidence, cross-record FantLab
URL/work ID/date/count agreement, frozen body sizes and SHA-256 identities,
normalization profiles, and explicitly unknown analyzer-input identity.
Contradictions fail closed rather than yielding a misleading partial table.

The current **five frozen public candidates** are *Anna Karenina*, *The Brothers
Karamazov*, *The Silver Dove*, *The Hyperboloid of Engineer Garin* and *Running
on Waves*. The older parity catalog still lists the last candidate as
traced_not_frozen; this view uses its newer independent frozen literary-body
witness and exposes the catalog status without silently rewriting it.

This is a **readiness/character-count diagnostic**, not a FantLab parity test:
actual_minus_expected compares the frozen public transcription's characters
including spaces with FantLab's displayed character count. It is not proof of
matched texts or matched counting policy, even when numerically equal. Exact
FantLab analyzer-input identity remains **UNKNOWN**, M2 stays **0/5**, and
all other metric comparisons are **NOT_RUN** in this view. This is
**not a global evidence verdict**: the separate
[field-level metric matrix](BENCHMARK_METRIC_MATRIX.md) already validates 55
diagnostic/extension rows across three frozen works (70 numeric, 14 without actuals).
None establishes FantLab input identity or parity. No rounding rule
is inferred for unverified decimal metrics. Reuse the existing
[benchmark runner](../scriptorium/benchmark.py) and
[benchmark contract](BENCHMARKING.md) for actual field-by-field comparisons; do
not convert these character deltas into a parity claim.

For the separately retained Anna Karenina 28-row metric comparison, the reader validates
the exact saved `actual - expected` arithmetic (including Python floating-point
subtraction), not an approximately equal delta. This catches mutated numbers
within a previously permitted 1e-10 margin. It is a **stored-artifact integrity
check**, not FantLab display rounding evidence, source-identity proof, or a
new parity tolerance.

This incremental slice partially addresses issue #281. Closing the issue still
requires source-bound metrics across five independently matched works,
independent reference rounding/display evidence, and complete verified
expected/actual/delta artifacts using the unchanged M2 acceptance rules.
