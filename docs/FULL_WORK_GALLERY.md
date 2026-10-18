# Full-work Gallery — Scriptorium-only comparison

This source-free preview compares two frozen Russian-language full works: Alexander Grin's *Running on Waves* (363,819 characters) and Jules Verne's *The Children of Captain Grant* in Alexandra Beketova's translation (1,095,467 characters).

Run from the repository root on Python 3.13+:

```sh
mkdir -p build
python -m scriptorium.full_work_gallery --repo-root . --format html > build/full-work-gallery.html
python -m scriptorium.full_work_gallery --repo-root . --format csv > build/full-work-evidence.csv
python -m unittest discover -s tests -p 'test_gallery_release.py' -v
```

Both results are deterministic. They use already-frozen derived metrics and do not download books, run morphology, require telemetry, or publish manuscript text. The standalone HTML includes a labeled comparison chart and exact-value table; the CSV preserves numeric values, units and scientific labels. Shell redirection replaces its destination; use new filenames when preserving an earlier export. This differs from the create-only `scriptorium analyze --output` writer.

**Scientific boundaries:** FantLab's analyzer-input edition for *Running on Waves* is unestablished. No FantLab comparison is performed for the Beketova translation. The works' lengths exceed the 300,000-character corpus floor, but neither length nor diagnostic resemblance establishes parity. **M2 remains 0/5.** The three total-count metrics are not length-normalized style indicators; seven rate/mean metrics have their own row-wise scales.

The module verifies exact source JSON Git blob identities, metrics profile compatibility, translation identity, explicit unknown gates and source-free evidence. Changes to the frozen source require a deliberate review and pin update. The package workflow also runs the installed module outside the checkout and compares two HTML and CSV builds byte for byte.

This is an **offline preview**, not a new canonical Pages route. It does not modify the publication manifest or deployment permissions. Later site integration must use an explicit digest-pinned allow-list, review gates and the staged publisher. See the [roadmap](../project/ROADMAP.md).
