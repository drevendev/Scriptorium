# Road to Nowhere: alternate frozen-body diagnostic, not FantLab parity

This complete-book measurement targets ONLY the already frozen Wikisource /
az.lib.ru-derived **Дорога в никуда (Грин)** transcription (permanent revision
5585836). It is not the distinct, incompletely linked **Pravda 1965**-source
Wikisource family. The alternate text is public-domain within the recorded
original-Russian-work scope; rights and edition distinctions remain documented
in corpus/candidates/source-edition-traces/grin-road-nowhere-ru.json.

The deterministic extractor is scriptorium-road-nowhere-alt-wikisource-body-v1.
It freezes 442,656 characters including spaces, 825,899 UTF-8 bytes and both
raw/normalized SHA-256:
e33a28b8dcdb3ac339147c6587b27c182dd910784122b367db41bc93dfc2dbee.

The new command can rerun this exact revision through the existing source
extractor and produce a **source-free 29-field JSON diagnostic**:

    python -m scriptorium.road_nowhere_diagnostic \
      --revision-manifest corpus/candidates/source-edition-traces/grin-road-nowhere-ru.alternate-revision.json \
      --body-manifest corpus/candidates/source-edition-traces/grin-road-nowhere-ru.alternate-body.json \
      --output /tmp/road-nowhere-alternate-measurements.json

Network access to the original pinned revision is required. Input drift, source
hash mismatch, changed rights, missing values in mandatory metrics, unexpected
dictionary outputs and accidental source-family promotion fail closed. Output
is create-only. The PR workflow uploads **derived JSON only**, never the
wikitext or the transient literary body. CI artifacts must be independently
checked and retained before Reader publication.

FantLab's September 18, 2022 work27346 display reports **438,439 characters**
and **61,299 words**. These are the only two retained reference numbers here;
all other FantLab values remain UNKNOWN rather than zero. A +4,217-character
source difference is already established. The new measurements are
DIAGNOSTIC_SOURCE_UNMATCHED, not PASS. FantLab's exact source edition, uploaded
bytes and displayed rounding remain unknown. The primary Pravda-1965 family
is still not source-complete. **M2: 0/5**.

**Status at authorship:** source-frozen alternate body already exists; this PR
adds executable analysis and the on-demand source-free CI capture. New 29-row
results are NOT_RUN until exact-head CI succeeds and an independent later run
inspects the uploaded artifact. The public Reader remains at **7 measured of
10 listed editions** until the derived snapshot is reviewed and published.
Desktop/mobile and live Pages verification remain separate.
