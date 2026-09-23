# SCRIP-CORPUS-072 — exact Perelman PDF internal page-label probe

- Selected the retained 1913 Perelman popular-science candidate from the P2 corpus/provenance continuation because SCRIP-CORPUS-061 rejected page-count arithmetic and SCRIP-CORPUS-071 found no current Russian Wikisource Index surface for either frozen carrier.
- Added an exact-carrier hosted probe that re-verifies the frozen 223-page Commons PDF at 28,168,847 bytes / SHA-256 `3d87d22a42ad949654265e066f81211d7831e32c8b62b96c967cd4cd33e7ed61` before inspecting qpdf's source-free `pagelabels` JSON surface.
- Pinned the hosted inspection environment to Ubuntu 24.04 package `qpdf=11.9.0-1.1ubuntu0.1` (qpdf 11.9.0); upstream qpdf documents `pagelabels` as a top-level JSON array of `{index,label}` entries.
- Hosted exact-head capture run `35884908615` passed 6 focused regressions and reported **zero internal page-label entries** for the exact frozen PDF. A second authoring-context replay `35885190135` independently repeated the successful probe.
- Added repository-durable source-free evidence `perelman-entertaining-physics-book1-1913-ru.pdf-page-labels.json`, physical SHA-256 `16b4ba074221d7fa20cb044584886038989f43657988c6bd6b062774077915bd`, plus a byte-for-byte regeneration check in CI.
- Updated the public Perelman candidate surface: the current exact PDF has no `/PageLabels` shortcut capable of mapping bibliographic pagination to carrier pages, so the next admissible mapping route is exact-carrier facsimile evidence.
- No PDF bytes, page images, OCR, hidden text or literary source text are committed by this unit.
- PDF↔DjVu equivalence, literary-page selection, canonical extraction carrier, OCR correctness, literary-body freeze, selected-body >=300k proof, FantLab analyzer-input identity, diagnostic readiness and M2 remain closed; M2 stays 0/5.
- Independent exact-head review `5293616208` re-read all 8 changed files at `150eae46800f826de93dff00fb89494ee254394b`, independently recomputed the canonical artifact SHA-256, confirmed 22/22 exact-head PR workflows succeeded, and found no merge blocker or open review thread.
- PR #234 was marked Ready and squash-merged with expected-head protection as `2590d3dd234fde3d26d2659f448bf58f7c040965`, closing Issue #233 completed. SCRIP-CORPUS-072 is complete and normal P2 corpus/provenance selection may resume.
