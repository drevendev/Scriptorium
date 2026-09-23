# Perelman 1913 — exact PDF internal page-label probe

This companion records a source-free carrier-mapping result for the retained 1913 first-edition candidate *Entertaining Physics, Book 1*.

The exact frozen Commons PDF is 223 carrier pages, 28,168,847 bytes, SHA-256 `3d87d22a42ad949654265e066f81211d7831e32c8b62b96c967cd4cd33e7ed61`. After re-verifying that byte identity, the hosted probe uses pinned Ubuntu 24.04 `qpdf=11.9.0-1.1ubuntu0.1` and requests only qpdf's `pagelabels` JSON surface. The result contains **zero internal page-label entries**.

Canonical source-free machine evidence: [`source-edition-traces/perelman-entertaining-physics-book1-1913-ru.pdf-page-labels.json`](source-edition-traces/perelman-entertaining-physics-book1-1913-ru.pdf-page-labels.json), physical SHA-256 `16b4ba074221d7fa20cb044584886038989f43657988c6bd6b062774077915bd`.

## What this establishes

The exact PDF has no internal `/PageLabels` shortcut that can map the bibliographic pagination (`VIII, 211, [1] с.` from the retained pagination evidence) to carrier-page indexes.

## What this does not establish

It does **not** select literary pages, prove PDF↔DjVu page equivalence, verify OCR, select a canonical extraction carrier, freeze a literary body, prove the selected body is >=300k characters, identify FantLab's analyzer input, or advance M2. The next admissible mapping route is exact-carrier facsimile evidence from visible printed page numbers/front matter/end matter, optionally cross-checked against the retained DjVu page map.

No PDF bytes, page images, OCR, hidden text, or literary source text are committed by this probe.
