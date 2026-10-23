# Private EPUB ingestion · Reader 0.4 preview

Scriptorium can analyze a **local, unencrypted EPUB 2/3** whose reading-order spine
points to valid XHTML chapters. The importer is a bounded, standard-library
projection of the book's **linear spine** into UTF-8 text. It is not an EPUB
reader, OCR tool, JavaScript engine or DRM remover.

## Use an installed wheel


```bash
scriptorium epub my-book.epub --output analysis.json --provenance-output source-identity.json
scriptorium epub my-book.epub --format html --title 'Private reading' --output analysis.html
scriptorium epub my-book.epub --format csv --output analysis.csv
scriptorium compare analysis.json another-analysis.json --output comparison.html
```

The main JSON/HTML/CSV outputs use the *existing* 29-metric Reader analysis
contract. `analysis.json` is immediately accepted by the normal private comparison
command. The JSON contains the SHA-256 of the extracted UTF-8 body, **not** the
raw EPUB container. It never contains the manuscript's prose.

Supply `--provenance-output` to record all three identities in a separate
create-only, source-free file:

| Identity | Meaning |
| --- | --- |
| `archive_sha256` | SHA-256 of the exact original EPUB archive bytes |
| `extracted_body_sha256` | SHA-256 of the UTF-8, spine-ordered projected literary body; equals analysis `source.raw_sha256` |
| `normalized_sha256` | Canonical analyzer-normalized text identity; equals analysis `source.normalized_sha256` |
| `extraction_profile` | `scriptorium-epub-spine-xhtml-v1`; change this version if reading/extraction rules change |

The receipt also records container/body byte counts, linear spine count,
readable chapter count and `source_text_embedded=false`. Two distinct
EPUB containers can contain the same extracted text. A raw-book SHA does not
identify a translation, edition or FantLab's analysis input by itself.

## Supported input and reading order

- Requires a ZIP EPUB with `mimetype` as its first stored/uncompressed
  member, content `application/epub+zip`, one standard
  `META-INF/container.xml` OPF rootfile and a namespaced EPUB 2/3 OPF
  manifest/spine.
- Accepts **linear XHTML (`application/xhtml+xml`)** spine items.
  Processes them in OPF spine order, **not ZIP member order**.
  Nonlinear spine entries and unreferenced images/nav/resources are ignored.
- XHTML `<body>` contributes textual nodes in document order.
  Paragraphs, headings, list items and similar blocks create text boundaries;
  formatting tags retain their inline text. `<head>`, styles, scripts,
  navigation, media, forms and MathML/SVG bodies are skipped.
- Skips empty chapters; rejects a book without any readable body.
  Unsupported fixed-layout, image-only, unnamespaced HTML, non-XHTML spine
  resources, multi-root OPF and malformed XML fail closed rather than guessing.
- This is a deterministic **extracted text projection**, not an assertion of
  exact visual rendering or FantLab's upload/edition identity.
  Hidden or decorative XHTML outside the selected subset may affect other readers.

## Privacy, integrity and bounded resources

- **No upload, network fetch, browser execution, shell extraction or archive
  member writes.** The EPUB stays on your machine; reports are source-free.
- Rejected: symlinks to the input, ZIP member traversal/absolute/backslash
  paths, ambiguous/duplicate member paths or manifest identifiers, encrypted
  members, unsupported compression, remote/fragment spine hrefs, DOCTYPE/
  XML entity declarations, malformed container/OPF/XHTML, missing spine
  references and non-XHTML linear resources.
- Upper bounds: **32 MiB compressed archive**, **256 ZIP members**,
  **16 MiB per member**, **64 MiB total declared uncompressed bytes**,
  **150:1 compression ratio per member**, **128 linear spine documents**,
  and **32 MiB extracted UTF-8 body**. All selected reads also check their
  actual decompressed lengths.
- Files are read with the existing bounded Reader regular-file/no-final-
  symlink guard, and output uses create-only writes. No destination is
  overwritten. If multiple outputs are requested and a late output fails,
  an earlier created report may remain; use distinct unused output names
  and inspect/create the provenance receipt separately as needed.
- Generated report titles are user-supplied display text and may contain
  private information; choose an appropriate title or omit it.
- Extraction ignores stylesheet-driven presentation, CSS hiding and
  scripting. If trustworthy text-fidelity is essential, inspect the source
  edition separately before scientific claims.

## Scientific limits

The analyzer accepts excerpts and short works with explicit
representativeness warnings. Neither this importer nor an EPUB container hash
admits a work to the legal corpus, proves source-edition identity, or
establishes FantLab parity. Calibration requires **300,000 characters including
spaces**, lawful use evidence, source matching and the existing metric gate.
**M2 remains 0/5** until the independent parity criteria pass.

The synthetic test EPUBs contain only original short text and intentionally
hostile ZIP/XML inputs. No copyrighted full book is committed.
