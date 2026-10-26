# Silver Dove · first reproducible field measurement

`scriptorium.silver_dove_diagnostic` replays the existing permanent
Wikisource revision `5588003` of Andrei Bely's *Silver Dove* through the
already-reviewed Silver Dove literary-body extractor. It refuses changed page
and body digests before running the existing, versioned deterministic analyzer.

Run from a repository checkout with network access to the public pinned revision:

```sh
python -m scriptorium.silver_dove_diagnostic \
  --manifest corpus/candidates/source-edition-traces/bely-silver-dove-ru.revisions.json \
  --output silver-dove-fields.json
```

The `Silver Dove measured field diagnostic` GitHub Action performs the same
replay and uploads a **source-free, derived-results-only** short-lived artifact.
It records all 29 Scriptorium metric fields (up to 24 measurable without a vocabulary
dictionary; five explicitly not run). Metrics requiring an observed dialogue
segment can remain unavailable when the replay has no such segment. It binds only the two already documented
FantLab 2022-09-19 display counts—549,050 characters and 83,369 words. Other
FantLab field references are **not retained**, not zero; even an apparently
matching value would not establish publication-rounding rules or source identity.

The canonical Wikisource body has 563,125 characters including spaces;
the public FantLab character display is 14,075 lower. This is a
**source-unmatched diagnostic delta**, not a discovered normalization correction.

No original source prose is saved in the report, repository or Action artifact;
the pinned replay holds text only transiently. `scriptorium-metrics-v4`
candidate values remain **inferred**; dictionary-free and POS-morphology
limitations remain explicit. No published result or M2 parity pass is claimed:
`fantlab_source_edition_match=unknown`, `m2_weight=0`, M2 **0/5**.

The successful pinned CI capture from 2026-10-26 is now retained exactly as
`corpus/candidates/diagnostics/bely-silver-dove-ru.json`, with the original
Git blob SHA-1 `88bfe95435be1b72703de65d314c6926b5f83a60`.
The matrix and Reader verify source witness, dated FantLab counts, profile, scientific
status and exact receipt bytes before displaying its 29 rows (24 numeric, five NOT_RUN).
All but two FantLab field reference values remain UNKNOWN; no M2 parity is claimed.
The artifact and built Reader are **not** deployed or LIVE_VERIFIED.
