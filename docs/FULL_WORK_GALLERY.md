# Full-work Gallery — Scriptorium-only comparison

This independent, source-free preview compares two frozen Russian-language full works: Alexander Grin's *Running on Waves* (363,819 characters) and Jules Verne's *The Children of Captain Grant* in Alexandra Beketova's translation (1,095,467 characters).

Run from the repository root on Python 3.13+:

```sh
python -m scriptorium.full_work_gallery --repo-root . --format html > full-work-gallery.html
python -m scriptorium.full_work_gallery --repo-root . --format csv > full-work-evidence.csv
python -m unittest discover -s tests -p 'test_gallery_release.py' -v
```

Both results are deterministic. They use already-frozen derived metrics and do not download books, run morphology, require telemetry, or publish manuscript text. The standalone HTML includes a labeled comparison chart and exact-value table; the CSV preserves numeric values, units and scientific labels.

**Scientific boundaries:** FantLab's analyzer-input edition for *Running on Waves* is unestablished. No FantLab comparison is performed for the Beketova translation. The works' lengths exceed the 300,000-character corpus floor, but neither length nor diagnostic resemblance establishes parity. **M2 remains 0/5.** The three total-count metrics are not length-normalized style indicators; seven rate/mean metrics have their own row-wise scales.

The module verifies exact source JSON Git blob identities, metrics profile compatibility, translation identity, explicit unknown gates and source-free evidence. Changes to the frozen source require a deliberate review and pin update.

This is a **local/offline preview**. It does not modify the existing site publisher, publication manifest or Pages deployment permissions. A later site integration must use the existing signed/digested allow-list, review gates and staged publisher.
